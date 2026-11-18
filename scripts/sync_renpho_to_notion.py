#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pycryptodome>=3.15"]
# ///
"""renpho-collection-app-skill: RENPHO → Notion「体重記録」DBの同期。

使い方:
  uv run scripts/sync_renpho_to_notion.py --dry-run          # 書き込まず件数と内訳だけ表示
  uv run scripts/sync_renpho_to_notion.py                    # 未取り込み分を全て同期
  uv run scripts/sync_renpho_to_notion.py --start-date 2026-07-30
  uv run scripts/sync_renpho_to_notion.py --limit 3          # 先頭N件だけ(初回の少数テスト用)
  uv run scripts/sync_renpho_to_notion.py --max-age-hours <時間>  # 他のスキルから頼まれたとき

**判断はこのスキルに持たない。** RENPHO側の事情(セッション・測定時刻・単位・同一測定の集約・
欠測・IDの型)は renpho-api-generic-logic-skill の判断と道具に、Notionの呼び方は
notion-cli-generic-logic-skill の判断と道具に従う。どちらの道具も写さず、importして呼ぶ。
このスキルが持つのは、導入先の環境(記録先のDB・列名)と手順だけ。

冪等性は「RENPHO ID」列で担保する。既にそのIDのページがあればスキップするので、
何度実行しても重複しない。
"""
import argparse
import os
import sys
from datetime import datetime, timedelta

_SKILLS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS, "renpho-api-generic-logic-skill", "scripts"))
sys.path.insert(0, os.path.join(_SKILLS, "notion-cli-generic-logic-skill", "scripts"))
import renpho_records  # noqa: E402
from renpho_api import RenphoError  # noqa: E402
from renpho_env import open_client, token_issued_at  # noqa: E402
from notion_client import (  # noqa: E402
    NotionError, create_page, data_source_id_from_url, env_file_path, load_env, query_data_source,
)
from notion_props import date_prop, number_prop, rich_text_prop, title_prop  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

JST = renpho_records.JST
ENV_DB_KEY = "RENPHO_COLLECTION_DB_URL"

# ---------------------------------------------------------------- 記録先の列(導入先の環境)
# 記録先の「体重記録」DBの列名。conventions/notion-db.md が説明で、ここが正。
# 列を足す前に renpho-api-generic-logic-skill の項目の意味と単位の判断に聞き、
# 列名を変えたらNotion側と同時にここを直す(notion-cli-generic-logic-skill のスキーマの変更の判断)。
TITLE_COLUMN = "Name"          # 測定日の YYYY-MM-DD
DATE_COLUMN = "対象日時"       # 測定時刻(JST)
ID_COLUMN = "RENPHO ID"        # 一意キー。必ずテキスト
VALUE_COLUMNS = {              # RENPHOのキー → number列
    "weight":        "体重(kg)",
    "bmi":           "BMI",
    "bodyfat":       "体脂肪率(%)",
    "water":         "体水分率(%)",
    "muscle":        "骨格筋量(kg)",
    "sinew":         "筋肉量(kg)",
    "bone":          "骨量(kg)",
    "bmr":           "基礎代謝(kcal)",
    "visfat":        "内臓脂肪レベル",
    "subfat":        "皮下脂肪率(%)",
    "protein":       "タンパク質率(%)",
    "bodyage":       "体年齢",
    "fatFreeWeight": "除脂肪体重(kg)",
    "TW":            "標準体重(kg)",
    "WC":            "体重コントロール(kg)",
    "resistance":    "生体インピーダンス(Ω)",
    "bodytype":      "体型分類",
}


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def data_source_id():
    url = load_env().get(ENV_DB_KEY)
    if not url:
        raise NotionError(f"環境変数にも {env_file_path()} にも {ENV_DB_KEY} が無い。"
                          "README の「セットアップ」を参照")
    return data_source_id_from_url(url)


def check_columns():
    """道具が返しうるキーに、列の対応が全部あるか。

    **知らないキーが来たら落とす。** 黙って捨てると「入れたつもりで入っていない」という
    最も気づきにくい壊れ方をするため、対応の漏れは同期の前に止める。
    """
    missing = [k for k in renpho_records.FIELD_KEYS if k not in VALUE_COLUMNS]
    if missing:
        raise SystemExit(f"Error: VALUE_COLUMNS に対応が無いRENPHOのキー: {', '.join(missing)}。"
                         "列を足すか、対応を書いてから同期する")


def to_properties(row):
    """renpho_records.normalize() の値 → Notionプロパティ。"""
    at = row["measured_at"]
    props = {
        TITLE_COLUMN: title_prop(at.strftime("%Y-%m-%d")),
        DATE_COLUMN: date_prop(at.isoformat(timespec="seconds")),
        ID_COLUMN: rich_text_prop(row["id"]),
    }
    for key, value in row["values"].items():
        props[VALUE_COLUMNS[key]] = number_prop(value)
    return props


def _plain(prop):
    """rich_text / date プロパティを素の文字列にする。"""
    if not prop:
        return None
    if prop["type"] == "date":
        return (prop["date"] or {}).get("start")
    if prop["type"] in ("rich_text", "title"):
        return "".join(x["plain_text"] for x in prop[prop["type"]]) or None
    return None


def notion_data_age_hours(ds_id):
    """記録先の最新測定が何時間前かを返す。直近14日に1件も無ければNone。

    RENPHOへの接続を省けるかの判定にだけ使う。判定を誤って同期をスキップすると
    データが欠けるので、取得や解釈に失敗したら「古い」側(None)に倒す。
    """
    since = (datetime.now(JST) - timedelta(days=14)).strftime("%Y-%m-%d")
    try:
        pages = query_data_source(ds_id, {
            "filter": {"property": DATE_COLUMN, "date": {"on_or_after": since}},
            "sorts": [{"property": DATE_COLUMN, "direction": "descending"}],
        })
    except NotionError:
        return None
    stamps = [s for s in (_plain(p["properties"].get(DATE_COLUMN)) for p in pages) if s]
    if not stamps:
        return None
    try:
        at = datetime.fromisoformat(max(stamps))
    except ValueError:
        return None
    if at.tzinfo is None:
        at = at.replace(tzinfo=JST)
    return (datetime.now(JST) - at).total_seconds() / 3600


def existing_ids(ds_id):
    """取り込み済みのRENPHO IDの集合。"""
    ids = set()
    for page in query_data_source(ds_id, {}):
        text = (_plain(page["properties"].get(ID_COLUMN)) or "").strip()
        if text:
            ids.add(text)
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-date", help="この日以降の測定のみ同期 YYYY-MM-DD")
    ap.add_argument("--end-date", help="この日までの測定のみ同期 YYYY-MM-DD")
    ap.add_argument("--limit", type=int, help="同期する最大件数(新しい順)。初回の少数テスト用")
    ap.add_argument("--session-window", type=int, default=renpho_records.SESSION_WINDOW_MIN,
                    help=f"同一セッションとみなす分数(既定{renpho_records.SESSION_WINDOW_MIN}分)。0で集約しない")
    ap.add_argument("--dry-run", action="store_true", help="Notionに書き込まない")
    ap.add_argument("--max-age-hours", type=float, metavar="N",
                    help="記録先の最新測定がN時間以内なら、RENPHOに一切接続せず終了する。"
                         "他のスキルから毎回呼ぶときに指定する(既定は無指定＝必ず取りに行く)")
    args = ap.parse_args()

    check_columns()
    ds_id = data_source_id()

    # RENPHOはアカウントに1セッションしか持てず、ログインするたびにアプリ側が
    # ログアウトされる。記録先が十分新しいなら、そもそも接続しないのが一番効く
    # (renpho-api-generic-logic-skill のセッションとトークンの判断)。
    if args.max_age_hours is not None:
        age = notion_data_age_hours(ds_id)
        if age is not None and age <= args.max_age_hours:
            log(f"記録先の最新測定は {age:.1f}時間前。"
                f"--max-age-hours {args.max_age_hours} 以内なのでRENPHOには接続しません。")
            return
        log(f"記録先の最新測定は {'なし' if age is None else f'{age:.1f}時間前'}。同期します。")

    client = open_client(log=lambda m: log(f"  {m}"))
    if client.token:
        log("保存済みトークンを使用します(有効ならログインしません)")
    else:
        log("保存済みトークンが無いためRENPHOにログインします")
    client.ensure_auth()
    records = client.get_measurements()
    log(f"RENPHOから {len(records)}件 取得")
    # 測っていないのか、アプリから上がっていないのかを見分ける材料(references/missing-days.md)。
    latest = renpho_records.measured_at(records[0]) if records else None  # 新しい順
    issued = token_issued_at(client.token)

    if args.session_window:
        before = len(records)
        records = renpho_records.collapse_sessions(records, args.session_window)
        log(f"同一セッションを集約: {before}件 → {len(records)}件"
            f"({args.session_window}分以内の連続測定は最後の1件に)")

    rows = [renpho_records.normalize(r) for r in records]
    if args.start_date:
        rows = [r for r in rows if r["measured_at"].strftime("%Y-%m-%d") >= args.start_date]
    if args.end_date:
        rows = [r for r in rows if r["measured_at"].strftime("%Y-%m-%d") <= args.end_date]
    if args.start_date or args.end_date:
        log(f"期間で絞り込み: {len(rows)}件")

    log("Notionの取り込み済みIDを確認中...")
    known = existing_ids(ds_id)
    log(f"  取り込み済み: {len(known)}件")

    todo = [r for r in rows if r["id"] not in known]
    skipped = len(rows) - len(todo)
    if args.limit:
        todo = todo[: args.limit]
        log(f"--limit により先頭{len(todo)}件のみ処理します")

    log(f"新規 {len(todo)}件 / スキップ(取り込み済み) {skipped}件")

    created = 0
    no_comp = 0
    for row in sorted(todo, key=lambda r: r["measured_at"]):  # 古い順に入れる
        props = to_properties(row)
        if not row["has_body_composition"]:
            no_comp += 1
        label = f"{row['measured_at'].strftime('%Y-%m-%d %H:%M')}  {row['values'].get('weight')}kg" \
                f"{'' if row['has_body_composition'] else '  (体組成なし・体重のみ)'}"
        if args.dry_run:
            log(f"  [dry-run] 作成予定 {label} / 項目数{len(props)}")
            continue
        create_page({"parent": {"data_source_id": ds_id}, "properties": props})
        created += 1
        log(f"  作成 {label}")

    log("=== 完了 ===")
    log(f"作成 {created}件 / スキップ {skipped}件 / うち体組成なし {no_comp}件")
    log(f"この同期でログインしたか: {'した' if client.logged_in else 'しない(保存済みtokenで通った)'}")
    log(f"保存済みtokenの発行: {issued.isoformat(timespec='minutes') if issued else '(読めない)'}")
    log(f"RENPHOの最新の測定: {latest.isoformat(timespec='minutes') if latest else 'なし'}")
    if args.dry_run:
        log("(dry-run のため実際には書き込んでいません)")


if __name__ == "__main__":
    try:
        main()
    except (RenphoError, NotionError) as e:
        sys.exit(f"Error: {e}")
