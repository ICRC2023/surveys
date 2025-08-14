# TODO - プロジェクト改善点

このドキュメントは、プロジェクトの品質向上と保守性改善のための課題をまとめています。

## 🚨 重要度：高（即座に対応が必要）

### 1. テストの修正
- [ ] **テストパスの修正** - 全15個のテストが相対パス問題で失敗
  - ファイル: `tests/test_config.py`, `tests/test_data.py`
  - 問題: `../sandbox/config.toml` パスが見つからない
  - 対応: テストファイル内の相対パスを絶対パスまたは適切な相対パスに修正
  - 影響: CI/CDパイプラインでのテスト実行が不可能

### 2. 依存関係の大幅更新
- [ ] **セキュリティパッケージの更新**
  - `certifi`: 2025.1.31 → 2025.8.3
  - `pillow`: 11.1.0 → 11.3.0
  - `numpy`: 2.2.4 → 2.3.2
  - その他50個以上のパッケージで更新が利用可能
- [ ] **更新手順の実行**
  ```bash
  git branch update-packages
  git checkout update-packages
  poetry show --outdated
  poetry add package@latest
  ```

## 📈 重要度：中（品質向上のため推奨）

### 3. 開発ツールの追加
- [ ] **コードカバレッジツールの導入**
  ```toml
  [tool.poetry.group.dev.dependencies]
  pytest-cov = "^5.0.0"
  ```
- [ ] **セキュリティチェックツールの追加**
  ```toml
  safety = "^3.0.0"
  ```
- [ ] **コードフォーマッターの設定**
  ```toml
  ruff = "^0.6.0"
  black = "^24.0.0"
  ```
- [ ] **型チェックツールの導入**
  ```toml
  mypy = "^1.11.0"
  ```

### 4. コード品質の改善
- [ ] **メイン実行部の修正**
  - ファイル: `titanite/cli.py:435`
  - 問題: `if __name__ == "__main__":` セクションのベストプラクティス違反
  - 対応: 適切な関数分離とエントリーポイントの設定

- [ ] **非推奨デコレータの整理**
  - ファイル: `titanite/config.py`
  - 問題: 6箇所で `@deprecated` デコレータ使用
  - 対応: 非推奨機能の完全削除または移行パスの明確化

- [ ] **長い関数の分割**
  - ファイル: `titanite/cli.py`
  - 対象: 200行を超える関数（`crosstabs`, `chi2`, `p005`など）
  - 対応: 単一責任原則に基づく関数分割

### 5. 型ヒントの追加
- [ ] **全モジュールでの型ヒント追加**
  - `titanite/cli.py`: 関数の引数・戻り値の型ヒント
  - `titanite/config.py`: クラスメソッドの型ヒント
  - `titanite/core.py`: データ処理関数の型ヒント
  - `titanite/preprocess.py`: 前処理関数の型ヒント

## 🔧 重要度：低（長期的な改善）

### 6. ドキュメントの改善
- [ ] **重複ドキュメントの統合**
  - 問題: `README.md` と `CLAUDE.md` の内容重複
  - 対応: 役割分担の明確化（README: プロジェクト概要、CLAUDE: 開発ガイド）

- [ ] **開発環境セットアップ手順の統一**
  - 現状: 複数箇所に散在する手順
  - 対応: 一元化された開発ガイドの作成

- [ ] **API ドキュメントの自動生成**
  - ツール: Sphinx + autodoc2（既に設定済み）
  - 対応: 型ヒント追加後のドキュメント品質向上

### 7. プロジェクト構造の最適化
- [ ] **設定ファイル管理の改善**
  - 現状: `sandbox/` ディレクトリに設定ファイル
  - 提案: プロジェクトルートまたは `config/` ディレクトリへの移動

- [ ] **テストデータの整理**
  - 現状: `data/test_data/` に大量のテストファイル
  - 対応: 不要ファイルの削除とテストデータの最小化

- [ ] **未使用ファイルの整理**
  - 対象: 古いJupyterノートブック、一時ファイル
  - 方法: Git履歴を確認して安全に削除

## 🔄 GitHub Actions / CI/CD改善

### 8. 自動化の強化
- [ ] **テスト自動実行の修正**
  - 現状: テストが失敗するためCIが機能しない
  - 対応: テストパス修正後の自動テスト復旧

- [ ] **品質チェックの追加**
  ```yaml
  # .github/workflows/quality.yml
  - name: Run Ruff
    run: poetry run ruff check .
  - name: Run MyPy
    run: poetry run mypy titanite/
  - name: Security Check
    run: poetry run safety check
  ```

- [ ] **依存関係更新の自動化**
  - Dependabot設定の見直し
  - 自動テスト通過時の自動マージ設定

## 📦 推奨パッケージ追加（優先度順）

```toml
[tool.poetry.group.dev.dependencies]
# 最優先
pytest-cov = "^5.0.0"          # テストカバレッジ
safety = "^3.0.0"              # セキュリティチェック

# 高優先度
ruff = "^0.6.0"                # 高速リンター・フォーマッター
mypy = "^1.11.0"               # 型チェック

# 中優先度
pre-commit = "^4.0.0"          # コミット前フック
black = "^24.0.0"              # コードフォーマッター（ruffで代替可能）

# 低優先度
bandit = "^1.7.0"              # セキュリティ静的解析
coverage = "^7.0.0"            # カバレッジレポート
```

## 🎯 アクションプラン（推奨実装順序）

### フェーズ1: 緊急対応（1-2日）
1. テストパスの修正
2. 最重要パッケージのセキュリティ更新

### フェーズ2: 開発環境整備（1週間）
1. 開発ツールの追加とセットアップ
2. GitHub Actions の修正
3. コード品質ツールの導入

### フェーズ3: コード改善（2-3週間）
1. 型ヒントの段階的追加
2. 長い関数の分割
3. 非推奨機能の整理

### フェーズ4: 長期改善（1-2ヶ月）
1. ドキュメント統合
2. プロジェクト構造最適化
3. 自動化の強化

---

## 注意事項

- **ブランチ戦略**: 大きな変更は必ず `update-packages` ブランチで実施
- **テスト**: 各改善後は必ずテスト実行を確認
- **コミットメッセージ**: Conventional Commits形式を維持
- **レビュー**: 重要な変更はPull Requestでレビューを実施

## 参考リンク

- [Poetry依存関係管理](https://python-poetry.org/docs/dependency-specification/)
- [Ruff設定ガイド](https://docs.astral.sh/ruff/)
- [MyPy型チェック](https://mypy.readthedocs.io/)
- [GitHub Actions Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)