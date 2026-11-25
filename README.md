# collect-renpho-records-app-skill

RENPHO（体組成計）の測定を取得し、Notionの「体重記録」DBへ、まだ入っていない分だけ記録するアプリケーションスキル。

## 必要なもの

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) か [Codex](https://developers.openai.com/codex)
- [uv](https://docs.astral.sh/uv/)
- RENPHO Health のアカウント
- Notion のワークスペースと、測定を記録するDB（列は [conventions/notion-db.md](conventions/notion-db.md)）
- `SKILL.md` の frontmatter の `metadata.dependencies` に書いてある依存するスキル

## インストール

Claude Code では、次のようにクローンする。

```bash
git clone https://github.com/junyatakechi/collect-renpho-records-app-skill.git ~/.claude/skills/collect-renpho-records-app-skill
```

Codex では、`~/.claude/skills/` を `~/.agents/skills/` に替えてクローンする。

特定のプロジェクトだけで使うなら、`<プロジェクト>/.claude/skills/`（Codex は `<プロジェクト>/.agents/skills/`）の中でクローンする。

## セットアップ

1. 依存するスキルを、このスキルと同じ `skills/` フォルダに並べて置く。スクリプトが隣のフォルダから道具を読む。
2. 依存するスキルの README の「セットアップ」を、先に済ませる。RENPHOのパスワードは自分でファイルに書き込み、AIエージェントに渡さない。
3. 記録先のDBに、Notion の Integration を接続する。
4. `.env.example` のキーを、プロジェクトのフォルダ直下（AIエージェントを起動するフォルダ）の `.env` に足し、値を埋める。キーの中身は `.env.example` のコメントにある。`.env` はプロジェクトのスキルで共有する。
5. 書き込まずに確かめる。Codex では、`~/.claude/skills/` を `~/.agents/skills/` に替える。

   ```bash
   cd <プロジェクトのフォルダ>   # .env のあるフォルダ
   uv run ~/.claude/skills/collect-renpho-records-app-skill/scripts/sync_renpho_to_notion.py --dry-run
   ```

RENPHOは1つのアカウントに1つのセッションしか持てないため、初めてログインしたときにスマホアプリがログアウトされる。以降は保存したtokenを使い回す。ただし、アプリでログインし直すとこちらのtokenが無効になり、次の同期で再ログインして、アプリがまたログアウトされる。

アプリがログアウトしている間の測定は、RENPHOに上がらない。同期がログインしたと伝えたら、スマホでアプリを開いてログインし直す。溜まっていた測定がまとめて上がり、次の同期で記録先に入る。

## 使い方

スキル名だけを指定して呼ぶ。指名しないと、このスキルは読み込まれない。Codex では、例の `/` を `$` に替えて指名する。

```
/collect-renpho-records-app-skill
```
