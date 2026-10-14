# 初めての同期・列を変えた直後の確かめ方

## 求める材料

無し。

## 答え

1. **初めての同期・列を変えた直後は、先に `--dry-run` と `--limit 3` で確かめる。**

## 道具

```bash
cd <skill-dir>
uv run scripts/sync_renpho_to_notion.py --dry-run
uv run scripts/sync_renpho_to_notion.py --limit 3
```

## 理由

記録なし。

## 却下した案

記録なし。

## 当てはまる範囲と限界

- 理由が記録されていない（未決）。
