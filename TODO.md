# TODO

コード品質・保守性の改善タスク。プロジェクト全体の設計方針と、進行中の
大きな作業は `PLAN.md` を参照。

## コード品質

### 型ヒントの追加

`core/` は概ね型付け済み。以下が未整備:

- `titanite/cli.py` — 一部のコマンドの引数・戻り値
- `titanite/config.py` — `Config` / `Data` のメソッド
- `titanite/analysis.py` — 集計・可視化関数
- `titanite/preprocess.py` — レガシー前処理（プラグイン移行が済めば縮小できる）

### 静的型チェック（mypy）

- `mypy` を dev グループに追加
- まず `titanite/core/` と `plugins/` だけ通す設定にして、段階的に広げる
- `ci.yml` の quality ジョブに追加

### `titanite/config.py` の `@deprecated` 整理

`categorical()` など旧 API が `@deprecated` のまま残り、`cli.py` の
`prepare`（非プラグイン経路）が依存している。移行パスを明確にして削除する。

### `titanite/cli.py` の長い関数の分割

`crosstabs` / `chi2` / `p005` が集計・保存・作図を1関数で抱えている。
ヘルパーに切り出す。

### レガシー `preprocess.py` の縮小

`preprocess.py` は `ICRC2023Schema` に無い旧ロジック（`replace_data` /
`cluster_data` / `binned_data`）を持ち、`cli.py prepare` の
`--plugin` なし経路で使われている。プラグイン経路に一本化し、薄い
後方互換シムだけ残す。

## テスト

- `tests/test_data.py` の 2 テストは `data/test_data/prepared_data.csv`
  （filter-repo で除去済み）を読むため skip 中。`data/public/public_data.csv`
  または合成 fixture で書き直す
- `analysis.py` / `cli.py` / `preprocess.py` のカバレッジが低い
  （`ci.yml` で term レポートは出るが、増やす）

## 依存管理

- Python 3.12 / 3.13 への移行検討（現状 `requires-python = ">=3.11"`）
- 依存更新は `update-packages` ブランチで（GitHub Actions の制約）。
  古くなったら main から切り直す

## 完了済み（参考）

- Poetry → uv 移行（#198）
- Taskfile によるタスク自動化
- pre-commit（ruff / ruff-format / commitizen + 機密データガード）
- `pytest-cov` を CI に（`ci.yml`、閾値ゲートなし）
- CLAUDE.md / AGENTS.md の統合、README リフレッシュ
- Phase 5-7（プライバシー・ワークフロー・ドキュメント分離）— `PLAN.md` 参照
