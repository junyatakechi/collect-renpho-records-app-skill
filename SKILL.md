---
name: renpho-collection-app
description: "文脈: RENPHOの記録。種類: アプリケーションスキル。使う場面: 名前で指名されたときだけ使い、会話の内容からは選ばない。"
metadata:
  version: "0.2.1"
  repository: "https://github.com/junyatakechi/renpho-collection-app"
---

# RENPHOの測定の記録

## このスキルが守る一番のこと

**切り出した判断は、このスキルに書かない。下の判断の委任表の判断先の、外部のロジックスキルに委ねる。**
ここにあるのは、測定をNotionに記録するために、どの判断を外部に委ね、何を実行するかだけ。
まだ切り出していない判断は、このスキルの `references/` に判断ファイルの形で置き、判断の委任表から指す。
RENPHOの癖（ログインでアプリが落ちる・単位が返らない・同じ測定が重複する）は、どれも renpho-api-generic-logic の判断と道具が持つ。ここで写したり、言い換えて書き直したりしない。

もう1つは、**ロジックスキルに無い判断を一般論で埋めない**こと。
判断が無いときは「判断が無い」と書き、本人に聞く。とくに、RENPHOの応答を見て「この項目はたぶん○○」と推測で列を足さない。

## 判断の委任表

記録で必要になる判断について、何を（聞きたい事）、どの判断先に、どんな答えの形で聞くか。**中核の判断（core-logic）・一般的な判断（generic-logic）・まだ切り出していない判断を、別々の表に分けて持つ。** 中核の判断は差し替えて別の人の視点を使うもの、一般的な判断は共有して育てるもの、まだ切り出していない判断は切り出す候補で、差し替え方も見直す時期も違うため。

- **聞きたい事はこのスキルが持つ。** 判断ファイルは問いを持たない。聞きたい事に判断ファイルで答えられないときは、ロジックスキルが「判断が無い」と返す。
- **答えの形はこのスキルが決める。**
- **材料はロジックスキルが求める。** 何を渡すかは、聞いたときにロジックスキルが返す「求める材料」に従う。このスキルは、ロジックスキルの判断ファイルを自分で読まない。
- **聞くときは、聞きたい事・判断先・欲しい答えの形の3つを伝える。**
- 判断先は、スキルのフォルダからの判断ファイルのパスで書く。差し替えるときは、判断先の列と、使用するリポジトリ表の行だけを書き換える。聞きたい事と答えの形は変えない。
- 判断先の版の2桁目が上がったら、手順とスクリプトを合わせてから、使用するリポジトリ表の版を更新する。3桁目だけが上がったときは、このスキルを直さない。
- 差し替える前に、差し替え先の判断ファイルが、聞きたい事に答えられるかを確かめる。

### 中核の判断（core-logic）

無し。記録には、人によって答えが分かれる判断が無い。測定の読み方（体組成が当てになるか、など）は、記録を読む側の評価のスキルが core-logic に聞く。

### 一般的な判断（generic-logic）

| 聞きたい事 | 判断先 | 欲しい答えの形 |
|---|---|---|
| RENPHOに、いつ・どう接続すれば、スマホアプリを落とさずに済むか | `renpho-api-generic-logic/references/session.md` | 接続を省く条件と、クライアントの作り方（道具の使い方） |
| RENPHOの道具を、どの入口から呼ぶか | `renpho-api-generic-logic/references/client-usage.md` | 呼ぶ関数の順と、呼び出し側で書かないこと（道具の使い方） |
| 認証情報が無い・ログインに失敗したとき、どうするか | `renpho-api-generic-logic/references/credentials.md` | 利用者に案内すること・Claudeがしてはいけないこと |
| 測定の日付と時刻を、どの項目から取るか | `renpho-api-generic-logic/references/measured-time.md` | 使う項目と、それを返す道具の関数（道具の使い方） |
| 1回の測定で残る複数のレコードを、どう記録するか | `renpho-api-generic-logic/references/session-collapse.md` | 畳み方と窓の幅、それを済ませる道具の関数（道具の使い方） |
| 体組成が測れなかった測定を、どう記録するか | `renpho-api-generic-logic/references/missing-composition.md` | 記録する項目と空にする項目、それを済ませる道具の関数（道具の使い方） |
| 重複を防ぐ一意キーを、何で、どの型で持つか | `renpho-api-generic-logic/references/record-id.md` | キーと列の型、差分の取り方 |
| 列を足すとき、どのキーが何で、どの項目に列を作るか | `renpho-api-generic-logic/references/field-units.md` | キー・意味・単位の表と、確かめ方（道具の使い方） |
| RENPHOのAPIが失敗したとき、どこを見るか | `renpho-api-generic-logic/references/unofficial-api.md` | 認証の失敗かプロトコルの破損かと、次にすること |
| Notionを読み書きするとき、道具をどう呼ぶか | `notion-cli-generic-logic/references/client-usage.md` | どの入口から呼ぶかと、呼び出し側で書かないこと（道具の使い方） |
| 記録先のDBの列を足す・変えるとき、どう進めるか | `notion-cli-generic-logic/references/schema-change.md` | 進め方と、守ること（道具の使い方） |
| 記録したあと、何を確かめ、崩れていたらどう直すか | `notion-cli-generic-logic/references/write-verification.md` | 確かめることと直し方（道具の使い方） |

- 同期のたびに聞くのは無い。セッション・入口・認証情報と測定の記録の判断は、`scripts/sync_renpho_to_notion.py` を書いたときに聞き、返ってきた道具の使い方どおりに呼んでいる。スクリプトを直すとき・判断先の版が上がったときに聞き直す。
- 列の判断は、列を足す・変えるときだけ聞く。APIの失敗の判断は、同期が失敗したときだけ聞く。
- 返ってきた道具の使い方に従い、どちらのロジックスキルの道具も写さず、自分で呼ぶ。
- 一般的な判断は差し替えるより、新しく踏んだ落とし穴を判断先のスキルに足して育てる。

### まだ切り出していない判断（このスキル）

| 聞きたい事 | 判断先 | 欲しい答えの形 |
|---|---|---|
| 誰に頼まれたかで、RENPHOへの接続を省くかをどう変えるか | `renpho-collection-app/references/request-source.md` | `--max-age-hours` を付けるかと、渡す時間 |
| 初めての同期・列を変えた直後に、何で確かめるか | `renpho-collection-app/references/first-sync-check.md` | 先に流すオプション |
| 記録先に数日分の体重が無いとき、同期漏れとして扱うか | `renpho-collection-app/references/missing-days.md` | 扱う / 扱わない |
| 記録先のDBを、新しく作るか | `renpho-collection-app/references/keep-existing-db.md` | 作る / 作らない と、その理由 |
| 常に空の項目・重複する項目に、列を作るか | `renpho-collection-app/references/unused-fields.md` | 列を作らない項目 |

- このスキルの判断ファイルは、このスキルが自分で読んで当てはめる。
- 齟齬が見つかったら、ここが切り出す候補になる。切り出すときは、判断ファイルをロジックスキルへ移し、行を上の表へ移して判断先を書き換える。

## 使用するリポジトリ表

判断の委任表の判断先に出てくるスキルを、どこから取るか。版はこの表だけで持つ。

| スキル名 | リポジトリのURL | 版 |
|---|---|---|
| `renpho-api-generic-logic` | https://github.com/junyatakechi/renpho-api-generic-logic | 0.1.x |
| `notion-cli-generic-logic` | https://github.com/junyatakechi/notion-cli-generic-logic | 0.2.x |

- 版は、そのスキルの版（`metadata.version`）の先頭2桁に、`.x` を付けた形（例：`0.2.x`）。3桁目はどの版でもよいことを表す。3桁目だけが上がった版は、この表を直さずにそのまま使う。3桁目は、呼び出し側が何も合わせなくてよい変更だけで上がるため。
- 判断先を別の人のスキルに差し替えるときは、この表の行も差し替える。

## 手順

1. 設定を確かめる
2. 同期する
3. 報告する

### 1. 設定を確かめる

次の3つが要る。どれかが無いと、スクリプトがエラーで止まる。止まったら先へ進まず、README の「セットアップ」を案内する。**RENPHOのパスワードをチャットで受け取らない。**

| 合図 | 足りないもの |
|---|---|
| `~/.claude-skills-env/renpho-collection-app.env に RENPHO_COLLECTION_DB_URL が無い` | 記録先のDBのURL |
| `RENPHO_EMAIL / RENPHO_PASSWORD が設定されていません。`・`RENPHOへのログインに失敗しました` | RENPHOの認証情報（renpho-api-generic-logic の認証情報の扱いの判断に聞く） |
| `Notion token file not found`・`NOTION_TOKEN is not set`・記録先のDBで404 | Notionのトークン、または記録先のDBへのIntegrationの接続 |

### 2. 同期する

```bash
cd <skill-dir>
uv run scripts/sync_renpho_to_notion.py --dry-run          # 書き込まず件数と内訳だけ
uv run scripts/sync_renpho_to_notion.py                    # 未取り込み分を全て同期
uv run scripts/sync_renpho_to_notion.py --start-date 2026-07-30
uv run scripts/sync_renpho_to_notion.py --limit 3          # 先頭N件だけ（少数テスト用）
uv run scripts/sync_renpho_to_notion.py --max-age-hours <時間>  # 接続を省くとき
```

- `--max-age-hours` を付けるか・何時間にするかは、まだ切り出していない判断（`references/request-source.md`）に聞く。記録先の最新の測定がその時間以内なら、RENPHOに接続しない。
- 初めての同期・列を変えた直後の確かめ方は、まだ切り出していない判断（`references/first-sync-check.md`）に聞く。
- **冪等性は `RENPHO ID` 列で担保している。** 何度実行しても重複しない。期間の指定は要らず、常に全件を取って差分だけを入れる。
- 何をどの列に書くかは [conventions/notion-db.md](conventions/notion-db.md) にある。列を足す・変えるときは、判断の委任表の列の判断に聞いてから、スクリプトの定数とNotion側を同時に直す。
- 記録先に数日分の体重が無いときの扱いは、まだ切り出していない判断（`references/missing-days.md`）に聞く。

### 3. 報告する

チャットへは、作成した件数・スキップした件数・体組成なしの件数を返す。依頼元のスキルから頼まれたときは、依頼元が欲しい結果を満たしたか確かめられるように、同じ内容を返す。

- **RENPHOにログインしたときは、必ず伝える。** 出力に `※ RENPHOにログインしました` があれば、スマホアプリがログアウトされたので、アプリで再ログインしてもらう。
- `--max-age-hours` で接続しなかったときは、その旨と記録先の最新の測定が何時間前かを伝える。
- 実行結果には、聞いたロジックスキルの名前と、実際に使った版（実行時に判断先の `metadata.version` を読んだ3桁）を添えられるようにしておく。どの判断で記録したかを後から辿るため。
