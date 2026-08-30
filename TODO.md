# TODO - プロジェクト改善点

このドキュメントは、プロジェクトの品質向上と保守性改善のための課題をまとめています。

## 🚨 重要度：最優先（プライバシー）

### 0. 公開リポジトリからの機密データ除去

- **優先度**: 最優先（他の全タスクに先行）
- **背景**: リポジトリは PUBLIC。`data/test_data/prepared_data.csv`（295行の個票）が
  自由記述の原文（q15/q16/q18/q20/q21/q22）と日本語訳（`*_ja`）、`timestamp`（秒単位）を
  含んだ状態でコミット済み。準識別子の組み合わせと公開参加者名簿の照合で個人特定が可能。
  さらに `docs/` の 26 個の .ipynb がこの CSV を直接読み、CI（`static.yml`）が myst-nb で
  実行して GitHub Pages に公開している。
- **詳細な対応計画**: `PLAN.md` の「Phase 5: プライバシー要件の実施」を参照
- **チェックリスト**:
  - [ ] `git rm --cached data/test_data/*.csv data/test_data/chi2_test/*.csv`
  - [ ] `.gitignore` に `data/**/*.csv` `data/**/*.json` を追加（PLAN.md 72-91 行を反映）
  - [ ] 公開中の GitHub Pages を精査（q15/q16/q18 ノートが自由記述原文を出力していないか、
        n<5 のクロス集計表が出ていないか）。必要なら Pages デプロイを一時停止
  - [ ] `ti anonymize` コマンドを実装（`SecureDataHandler` を実パイプラインに接続）
  - [ ] 匿名化・集計済みの `public_data.csv` を生成してコミット対象にする
  - [ ] ノート 26 個の `f_csv` 参照を `public_data.csv` に一括置換
  - [ ] CI / pre-commit に機密ファイル検出ガードを追加（PLAN.md 212-238 行を反映）
  - [ ] 公開リポジトリのため履歴からの完全除去（`git filter-repo`）を実施するか
        ICRC2023 Diversity Group と協議

## ✅ 完了項目

以下の項目はすでに実装されているため、参考までに記載します。

- ✅ **テストパスの修正** - `Path(__file__).parent.parent`を使った絶対パスに修正済み
- ✅ **テスト自動実行の修正** - PRテストCIが正常に動作
- ✅ **コードフォーマッターの設定** - ruff（0.15.9）が導入済み
- ✅ **依存関係の大幅更新** - poetry.lockが最新版に更新済み（2026-04-07）
- ✅ **Taskfile.ymlの追加** - タスク自動化が実装済み
- ✅ **CLAUDE.mdの整理** - 開発ガイドが最新化済み

## 📈 重要度：高（推奨）

### 1. 型ヒントの追加
- **優先度**: 高
- **対象**: 全モジュール
- **詳細**:
  - `titanite/cli.py`: 関数の引数・戻り値の型ヒント
  - `titanite/config.py`: クラスメソッドの型ヒント
  - `titanite/core.py`: データ処理関数の型ヒント
  - `titanite/preprocess.py`: 前処理関数の型ヒント
  - `titanite/analysis.py`: 統計分析関数の型ヒント
- **メリット**: IDE support向上、バグ検出、ドキュメント自動生成

### 2. 開発ツールの追加

- **pytest-cov**：テストカバレッジレポート
  ```bash
  poetry add --group dev pytest-cov
  task test:coverage
  ```
- **mypy**：静的型チェック
  ```bash
  poetry add --group dev mypy
  poetry run mypy titanite/
  ```
- **safety**：セキュリティ脆弱性チェック
  ```bash
  poetry add --group dev safety
  poetry run safety check
  ```

### 3. コード品質の改善

- [ ] **非推奨デコレータの整理**
  - ファイル：`titanite/config.py`
  - 現状：6箇所で`@deprecated`デコレータ使用
  - 対応：非推奨機能の完全削除または移行パスの明確化

- [ ] **長い関数の分割**
  - ファイル：`titanite/cli.py`
  - 対象：複雑な処理を持つ関数（`crosstabs`、`chi2`、`p005`など）
  - 対応：単一責任原則に基づく関数分割とヘルパー関数の作成

### 4. GitHub Actions / CI/CD改善

- [ ] **ワークフロー全体の再編** — 詳細は `PLAN.md`「Phase 6: GitHub Actions ワークフロー再編」を参照
  - 現状 5 本（branch / pr_test / quality / static / update_changelog）を
    `ci.yml` / `pages.yml` / `changelog.yml`（+ 任意 `release.yml`）の 3〜4 本に整理
  - PR での品質チェック二重実行を解消（`pr_test.yml` を `quality.yml` に統合）
  - `static.yml` を `workflow_run` トリガーにして、CI 成功後のみ Pages デプロイ
  - CI に `pytest --cov` を追加（カバレッジ劣化の検知）
  - `update_changelog.yml` の main 直 push を PR 化、`permissions` を明示
  - `guard` ジョブを `data/**` 全体 + 自由記述列を持つ CSV に拡張（Phase 5 タスク7と共通）

- [ ] **品質チェック自動化**（上記再編の中で扱う）
  ```yaml
  # .github/workflows/quality.yml（新規作成）
  - name: Run Ruff
    run: poetry run ruff check .
  - name: Run MyPy
    run: poetry run mypy titanite/
  - name: Security Check
    run: poetry run safety check
  ```

## 📚 重要度：中（長期改善）

### 5. ドキュメントの改善

- [ ] **titanite ドキュメントとアンケート結果ドキュメントの分離** — 詳細は `PLAN.md`「Phase 7: ドキュメントの分離」を参照
  - titanite（`docs/` + API）→ Zensical + mkdocstrings
  - アンケート結果（`docs/survey/` + `docs/diversity/`）→ `reports/`（Quarto、ノート埋め込み、`freeze: true`）
  - Sphinx / myst-nb / sphinx-autodoc2 は撤去
  - CI が個票 CSV なしでビルドできる状態にする（Phase 5・6 と連動）

- [ ] **APIドキュメントの充実**
  - ツール：Zensical + mkdocstrings（Phase 7 で移行）
  - 対応：型ヒント追加後のドキュメント品質向上

- [ ] **開発ガイドの統一**
  - README.mdとAGENTS.md/CLAUDE.mdの役割分担が明確化済み（AGENTS.md に統合）
  - 今後：ドキュメント分離（Phase 7）に合わせて更新

### 6. プロジェクト構造の最適化

- [ ] **テストデータの整理**
  - 現状：`data/test_data/`に大量のテストファイル
  - 対応：不要ファイルの削除とテストデータの最小化
  - ⚠️ このうち機密 CSV の除去は「重要度：最優先」の項目 0 で扱う（先にそちらを実施）
  - テストは fixture（`tests/test_integration_real_world.py` の合成データ）で完結しており、
    実 CSV への依存はない。ノート用データは項目 0 の `public_data.csv` に移行

- [ ] **未使用ファイルの整理**
  - 対象：古いJupyterノートブック、一時ファイル
  - 方法：Git履歴を確認して安全に削除

### 7. 依存関係管理の改善

- [ ] **Pythonバージョンのアップグレード検討**
  - 現状：Python 3.11（`pyproject.toml`：`python = "~3.11"`）
  - 検討：3.12/3.13への段階的移行

- [ ] **uvへの移行検討**
  - CLAUDE.mdに言及：「Future migration to `uv` planned」
  - 状態：計画段階
  - 時期：Poetryの十分な成熟後

## 🔍 参考：最新パッケージ状況

以下は最後のパッケージ更新時点（2026-04-07）での情報です。

### 主要ライブラリ
- pandas：2.3.3（最新）
- altair：6.0.0（最新）
- scipy：1.17.1（最新）
- pytest：9.0.2（最新）
- ruff：0.15.9（最新）

### セキュリティアップデート
最後の更新で以下を含む100+パッケージが更新されました：
- certifi：最新版
- pillow：最新版
- numpy：2.4.4

---

## 実装順序の推奨

### Phase 1：型ヒント追加（推奨）
```bash
git worktree add ../worktrees/add-types -b feat/add-type-hints
cd ../worktrees/add-types
# 各モジュールに型ヒントを追加
task test
task lint
```

### Phase 2：開発ツール追加
```bash
git worktree add ../worktrees/add-tools -b feat/add-dev-tools
cd ../worktrees/add-tools
poetry add --group dev pytest-cov mypy safety
task test
```

### Phase 3：CI/CD改善

- `.github/workflows/quality.yml`作成
- 自動品質チェック実装

### Phase 4：コード最適化

- 非推奨機能の整理
- 長い関数の分割
- テストデータの整理

---

## 参考リンク

- [Poetry依存関係管理](https://python-poetry.org/docs/dependency-specification/)
- [Ruff設定ガイド](https://docs.astral.sh/ruff/)
- [MyPy型チェック](https://mypy.readthedocs.io/)
- [GitHub Actions Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
