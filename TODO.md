# TODO - プロジェクト改善点

このドキュメントは、プロジェクトの品質向上と保守性改善のための課題をまとめています。

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

- [ ] **品質チェック自動化**
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

- [ ] **APIドキュメントの充実**
  - ツール：Sphinx + autodoc2（すでに設定済み）
  - 対応：型ヒント追加後のドキュメント品質向上
  - ターゲット：docs/apidocs/

- [ ] **開発ガイドの統一**
  - README.mdとCLAUDE.mdの役割分担が明確化済み
  - 今後：CLAUDE.mdを拡充

### 6. プロジェクト構造の最適化

- [ ] **テストデータの整理**
  - 現状：`data/test_data/`に大量のテストファイル
  - 対応：不要ファイルの削除とテストデータの最小化

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
