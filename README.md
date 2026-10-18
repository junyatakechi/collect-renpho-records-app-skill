# renpho-collection-app

RENPHO（体組成計）の測定を取得し、Notionの「体重記録」DBへ記録する、アプリケーションスキル。
体重・体脂肪率・骨格筋量・基礎代謝など17項目を、まだ入っていない分だけ記録する。

RENPHO側の判断（スマホアプリを落とさないセッションの扱い・単位・同じ測定の重複など）は [renpho-api-generic-logic](https://github.com/junyatakechi/renpho-api-generic-logic) に、Notionの呼び方は [notion-cli-generic-logic](https://github.com/junyatakechi/notion-cli-generic-logic) に委ね、どちらの道具も部品として呼ぶ。このスキルが持つのは、記録先のDB・列名と手順。まだ切り出していない判断は `references/` に置く。

## 中身

- [SKILL.md](SKILL.md): 判断の委任表・使用するリポジトリ表と、設定の確認・同期・報告の手順
- [conventions/notion-db.md](conventions/notion-db.md): 記録先のDBと列（この環境での記録の取り決め）
- [references/](references/): まだ切り出していない判断。1判断1ファイル
- [scripts/sync_renpho_to_notion.py](scripts/sync_renpho_to_notion.py): RENPHOから取り、Notionへ記録する

## 必要なもの

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) と [uv](https://docs.astral.sh/uv/)
- [renpho-api-generic-logic](https://github.com/junyatakechi/renpho-api-generic-logic)（RENPHOの判断と道具）
- [notion-cli-generic-logic](https://github.com/junyatakechi/notion-cli-generic-logic)（Notionの判断と道具）
- 3つのスキルは、同じ `skills/` フォルダに並べて置く（スクリプトが隣のフォルダから道具を読む）
- 測定を記録するNotionのDB（列は [conventions/notion-db.md](conventions/notion-db.md)）

## インストール

```bash
git clone https://github.com/junyatakechi/renpho-api-generic-logic.git ~/.claude/skills/renpho-api-generic-logic
```

```bash
git clone https://github.com/junyatakechi/notion-cli-generic-logic.git ~/.claude/skills/notion-cli-generic-logic
```

```bash
git clone https://github.com/junyatakechi/renpho-collection-app.git ~/.claude/skills/renpho-collection-app
```

## セットアップ

1. renpho-api-generic-logic の README の「セットアップ」で、RENPHOの認証情報を用意する。**パスワードは自分でファイルに書き込み、Claudeに渡さない。**
2. notion-cli-generic-logic の README の「セットアップ」で、Notionのトークンを用意し、記録先のDBにIntegrationを接続する。
3. `.env.example` のキーを、プロジェクトのフォルダ直下（Claude Code を起動するフォルダ）の `.env` に足し、値を埋める。`.env` はプロジェクトのスキルで共有する。

| キー | 中身 |
|---|---|
| `RENPHO_COLLECTION_DB_URL` | 測定を記録するNotionのDBのURL |

4. 書き込まずに確かめる。

   ```bash
   cd <プロジェクトのフォルダ>   # .env のあるフォルダ
   uv run ~/.claude/skills/renpho-collection-app/scripts/sync_renpho_to_notion.py --dry-run
   ```

RENPHOは1つのアカウントに1つのセッションしか持てないため、初めてログインしたときにスマホアプリがログアウトされる。以降は保存したtokenを使い回すので、ログアウトは起きない。

## 使い方

| 頼み方 | Claudeがすること |
|---|---|
| 「体重計のデータを取り込んで」「RENPHOを同期して」 | まだ入っていない測定をRENPHOから取り、Notionに記録する |
| 「体重記録を最新にして」「体組成を記録して」 | 同上 |

評価のスキルから評価の前に呼ばれるときは、記録先が十分新しければRENPHOに接続しない（スマホアプリを落とさないため）。

チャットには、作成した件数・スキップした件数と、RENPHOにログインしたかどうかを返す。
