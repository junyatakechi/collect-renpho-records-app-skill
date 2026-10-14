---
name: renpho-collection-app
description: RENPHO（体組成計）の測定を取得し、Notionの「体重記録」DBへ記録するアプリケーションスキル。体重・BMI・体脂肪率・体水分率・骨格筋量・筋肉量・骨量・基礎代謝・内臓脂肪・皮下脂肪・タンパク質・体年齢・除脂肪体重など17項目を同期する。「体重計のデータを取り込んで」「RENPHOを同期して」「体組成を記録して」「体重記録を最新にして」のように言われたときや、評価のスキル（diet-process-evaluation-app など）から評価の前の最新化として呼ばれたときに使う。RENPHO側の判断（セッション・測定時刻・単位・同一測定の集約・欠測・IDの型）は外部の generic-logic（renpho-api-generic-logic）に、Notionの呼び方は notion-cli-generic-logic に委ね、どちらの道具も写さず自分で呼ぶ。このスキルが持つのは、聞きたい事・判断先・欲しい答えの形と、記録先のDB・列名・手順だけ。取得した測定の解釈・評価はしない。
metadata:
  version: "0.1.0"
  repository: "https://github.com/junyatakechi/renpho-collection-app"
  dependencies: "github:junyatakechi/renpho-api-generic-logic/renpho-api-generic-logic@^0.1.0, github:junyatakechi/notion-cli-generic-logic/notion-cli-generic-logic@^0.1.0"
---

# RENPHOの測定の記録

## このスキルが守る一番のこと

**切り出した判断は、このスキルに書かない。下の判断の委任表の判断先の、外部のロジックスキルに委ねる。**
ここにあるのは、測定をNotionに記録するために、どの判断を外部に委ね、何を実行するかだけ。
RENPHOの癖（ログインでアプリが落ちる・単位が返らない・同じ測定が重複する）は、どれも renpho-api-generic-logic の判断と道具が持つ。ここで写したり、言い換えて書き直したりしない。

もう1つは、**ロジックスキルに無い判断を一般論で埋めない**こと。
判断が無いときは「判断が無い」と書き、本人に聞く。とくに、RENPHOの応答を見て「この項目はたぶん○○」と推測で列を足さない。

## 判断の委任表

記録で必要になる判断について、何を（聞きたい事）、どの判断先に、どんな答えの形で聞くか。

- **聞きたい事はこのスキルが持つ。** 判断ファイルは問いを持たない。聞きたい事に判断ファイルで答えられないときは、ロジックスキルが「判断が無い」と返す。
- **答えの形はこのスキルが決める。材料はロジックスキルが求める。** 何を渡すかは、聞いたときにロジックスキルが返す「求める材料」に従う。
- **聞くときは、聞きたい事・判断先・欲しい答えの形の3つを伝える。** 版は伝えず、実行結果に残すために使う。
- 版は、判断先のロジックスキルの `metadata.version`。判断先の判断ファイルが変わったら、手順とスクリプトを合わせてから版を更新する。

### 中核の判断（core-logic）

無し。記録には、人によって答えが分かれる判断が無い。測定の読み方（体組成が当てになるか、など）は、記録を読む側の評価のスキルが core-logic に聞く。

### 一般的な判断（generic-logic）

| 聞きたい事 | 判断先 | 版 | 欲しい答えの形 |
|---|---|---|---|
| RENPHOに、いつ・どう接続すれば、スマホアプリを落とさずに済むか | `renpho-api-generic-logic/references/session.md` | 0.1.0 | 接続を省く条件と、クライアントの作り方（道具の使い方） |
| RENPHOの道具を、どの入口から呼ぶか | `renpho-api-generic-logic/references/client-usage.md` | 0.1.0 | 呼ぶ関数の順と、呼び出し側で書かないこと（道具の使い方） |
| 認証情報が無い・ログインに失敗したとき、どうするか | `renpho-api-generic-logic/references/credentials.md` | 0.1.0 | 利用者に案内すること・Claudeがしてはいけないこと |
| 測定の日付と時刻を、どの項目から取るか | `renpho-api-generic-logic/references/measured-time.md` | 0.1.0 | 使う項目と、それを返す道具の関数（道具の使い方） |
| 1回の測定で残る複数のレコードを、どう記録するか | `renpho-api-generic-logic/references/session-collapse.md` | 0.1.0 | 畳み方と窓の幅、それを済ませる道具の関数（道具の使い方） |
| 体組成が測れなかった測定を、どう記録するか | `renpho-api-generic-logic/references/missing-composition.md` | 0.1.0 | 記録する項目と空にする項目、それを済ませる道具の関数（道具の使い方） |
| 重複を防ぐ一意キーを、何で、どの型で持つか | `renpho-api-generic-logic/references/record-id.md` | 0.1.0 | キーと列の型、差分の取り方 |
| 列を足すとき、どのキーが何で、どの項目に列を作るか | `renpho-api-generic-logic/references/field-units.md` | 0.1.0 | キー・意味・単位の表と、確かめ方（道具の使い方） |
| RENPHOのAPIが失敗したとき、どこを見るか | `renpho-api-generic-logic/references/unofficial-api.md` | 0.1.0 | 認証の失敗かプロトコルの破損かと、次にすること |
| Notionを読み書きするとき、道具をどう呼ぶか | `notion-cli-generic-logic/references/client-usage.md` | 0.1.2 | どの入口から呼ぶかと、呼び出し側で書かないこと（道具の使い方） |
| 記録先のDBの列を足す・変えるとき、どう進めるか | `notion-cli-generic-logic/references/schema-change.md` | 0.1.2 | 進め方と、守ること（道具の使い方） |

- 同期のたびに聞くのは無い。上の3つ（セッション・入口・認証情報）と測定の記録の判断は、`scripts/sync_renpho_to_notion.py` を書いたときに聞き、返ってきた道具の使い方どおりに呼んでいる。スクリプトを直すとき・判断先の版が上がったときに聞き直す。
- 列の判断は、列を足す・変えるときだけ聞く。APIの失敗の判断は、同期が失敗したときだけ聞く。
- 返ってきた道具の使い方に従い、どちらのロジックスキルの道具も写さず、自分で呼ぶ。
- 一般的な判断は差し替えるより、新しく踏んだ落とし穴を判断先のスキルに足して育てる。

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
uv run scripts/sync_renpho_to_notion.py --max-age-hours 6  # 他のスキルから呼ぶときはこれ
```

- **他のスキルから評価の前に呼ばれるときは、`--max-age-hours` を必ず付ける。** 記録先の最新の測定がその時間以内なら、RENPHOに接続しない。何時間にするかは呼び出し側が決める。根拠は renpho-api-generic-logic のセッションとトークンの判断。
- **ユーザーから直接頼まれたときは付けない。** 頼まれたのは「最新にすること」なので、取りに行く。
- 初めての同期・列を変えた直後は、先に `--dry-run` と `--limit 3` で確かめる。
- **冪等性は `RENPHO ID` 列で担保している。** 何度実行しても重複しない。期間の指定は要らず、常に全件を取って差分だけを入れる。
- 何をどの列に書くかは [references/notion-db.md](references/notion-db.md) にある。列を足す・変えるときは、判断の委任表の列の判断に聞いてから、スクリプトの定数とNotion側を同時に直す。
- 体重が数日入っていない期間は「測っていない」のであって、同期漏れではない。

### 3. 報告する

チャットへは、作成した件数・スキップした件数・体組成なしの件数を返す。

- **RENPHOにログインしたときは、必ず伝える。** 出力に `※ RENPHOにログインしました` があれば、スマホアプリがログアウトされたので、アプリで再ログインしてもらう。
- `--max-age-hours` で接続しなかったときは、その旨と記録先の最新の測定が何時間前かを伝える。
- 実行結果には、聞いたロジックスキルの名前と版（判断の委任表の版）を添えられるようにしておく。どの判断で記録したかを後から辿るため。

## 実行環境の癖（Windows / Git Bash）

- `python` で直接叩かず、`uv run` で起動する。スクリプト先頭のインラインメタデータで `pycryptodome` が入る。
- `TZ=Asia/Tokyo` は使わない（ゾーン名の解決に失敗し、黙ってUTCになる）。スクリプトはJSTを `+09:00` の固定オフセットで持っている。
- 一時ファイルは `/tmp` ではなくスクラッチパッドの絶対パスを使う（Windows版の `python` は `/tmp/foo` を `C:\tmp\foo` と解釈する）。

## 他のスキルとの分担

| スキル | 担当 |
|---|---|
| renpho-api-generic-logic | RENPHO Health の非公式APIを扱うときの一般的な判断と、APIを呼ぶ道具・認証情報 |
| notion-cli-generic-logic | Notionを扱うときの一般的な判断と、Notion REST APIを呼ぶ道具・トークン |
| 評価のスキル（diet-process-evaluation-app など） | 記録された測定を読み、意味づけする。このスキルを評価の前に呼ぶ |
| このスキル | 何を記録するために、どの判断を聞き、何を実行するか。記録先のDBと列名 |
