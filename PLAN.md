# PLAN.md

titanite フレームワークの設計方針と、残っている作業のトラッカー。
実装済みの詳細は各 PR とコミット履歴を参照。

## ビジョン

汎用的な Google Forms 対応アンケート処理フレームワーク。ICRC2023 を最初の
プラグインとしながら、他のアンケートプロジェクトでも再利用できる設計。

## 現状のアーキテクチャ

```
titanite/
├── core/
│   ├── schema.py      # SurveySchema（抽象基底）+ SplitColumnRule / ClusterRule / BinRule
│   ├── processor.py   # SurveyProcessor（スキーマ駆動の前処理パイプライン）
│   └── security.py    # SecureDataHandler（匿名化・秘匿）
├── cli.py             # ti コマンド群（--plugin でスキーマ選択）
├── analysis.py        # 集計・可視化
├── preprocess.py      # レガシー前処理（プラグイン非経由の後方互換）
└── config.py          # Config / Data（TOML 設定）

plugins/icrc2023/
└── schema.py          # ICRC2023Schema（replace / split / cluster / bin +
                       #   quasi_identifiers / public_drop_columns / public_mask_columns）
```

### データフロー（プライバシー境界）

```
data/downloaded/    raw Google Forms CSV（.gitignore、コミット不可）
   │ ti prepare
data/private/       個票 + 自由記述 + sentiment（.gitignore、コミット不可）
   │ ti anonymize                     │ ti aggregate / ti chi2
data/public/                          data/public/aggregates/, data/public/chi2/
  public_data.csv                       単変量/二変量の頻度表、検定統計量
  （k=5 匿名化、自由記述なし、           （n<5 セル秘匿）
   subregional なし、日付粒度）
   ↑ すべて data/public/ はコミット可
```

- `data/raw_data/` / `data/test_data/` は旧ディレクトリ、廃止済み（`.gitkeep` のみ）

### ドキュメント

| サイト | ツール | ソース | 公開 URL |
|--------|--------|--------|----------|
| titanite フレームワーク | Zensical（`zensical.toml`） | `docs/` | `www.icrc2023.org/surveys/titanite/` |
| ICRC2023 アンケート結果 | Quarto（`reports/_quarto.yml`） | `reports/` | `www.icrc2023.org/surveys/` |

`static.yml` が両方をビルドして単一 Pages アーティファクトにマージ。CI
（`ci.yml`）成功後のみデプロイ（`workflow_run` トリガー）。

## 完了したフェーズ

- **Phase 1-4**: フレームワーク化（`core/`, `plugins/`, プラグイン対応 CLI）
- **Phase 5**: プライバシー要件の実施
  - 個票 CSV を `git filter-repo` で全履歴・全タグから除去（#221 で追跡停止、
    その後 filter-repo で完全除去。バックアップ `surveys-backup-20260830-222318.git`）
  - `ti anonymize` / `ti aggregate`（#215, #223, #228）
  - `data/private/` への出力パス統一（#220）
  - `scripts/check_sensitive_data.py` を CI + pre-commit に（#222）
  - 日本語訳（`_ja` カラム）は廃止（`TextBlob.translate` が現行版で削除されたため）
- **Phase 6**: ワークフロー再編
  - `pr_test.yml` / `branch.yml` / `quality.yml` を `ci.yml` に統合（#231）
  - `static.yml` を `workflow_run`（CI 成功後）ゲートに（#231）
  - `update_changelog.yml` を PR ベースに（#235）
- **Phase 7**: ドキュメント分離
  - titanite → Zensical（#218）、`docs/titanite/*` を `docs/*` に引き上げ（#232）
  - アンケート結果 → Quarto `reports/`（#219, #225-#229）
  - Sphinx 撤去、公開デプロイを Zensical + Quarto に切り替え（#230）

## 残っている作業

### プライバシー（Phase 5 の残り）

- [ ] **公開中の Pages の目視精査**: 移行後の Quarto サイトに自由記述の
      原文や n<5 のセルが出ていないか。自由記述ページは件数と感情スコアのみ
      表示する設計だが、実物を確認する
- [ ] **`data/main_data/*.png` の精査**: `q13-q03_clustered.png` /
      `q13-q04_clustered.png` / `q14-q13_clustered.png` / `chi2*.png` が
      n<5 のセルを可視化していないか。している場合は差し替えるか削除する
- [ ] **リポジトリ管理者のアクション**（filter-repo の後始末）
  - Diversity Group メンバーへ周知（既存クローンは無効、再クローン or
    `git fetch && git reset --hard origin/main`）
  - GitHub Support にキャッシュパージを依頼
  - `update-packages` 運用ブランチは次回必要時に main から切り直す

### ドキュメント（Phase 7 の残り）

- [ ] **`reports/` の残りページ**: クラスタ系（`q01_clustered` 等）、
      集約ノート（demographics / icrc2023_diversity / chi2_test_map 相当）、
      post-survey の分析ページ
- [ ] **`docs/releases/v0.7.0.md` のリンク切れ**: `../../README.md` /
      `../../CLAUDE.md` / `../../PLUGIN_DEVELOPMENT_GUIDE.md` が Zensical
      サイトで 404（ビルドは exit 0）。GitHub blob URL に張り替える

### CI（Phase 6 タスク5、任意）

- [ ] **`release.yml`**: `workflow_dispatch` で
      `cz bump --changelog --check-consistency` → タグ push → GitHub Release。
      `pyproject` ↔ `titanite/__init__.py` のバージョン整合を検証

### コード品質（TODO.md 参照）

- [ ] 型ヒントの追加（`cli.py` / `config.py` / `analysis.py` / `preprocess.py`）
- [ ] `mypy` の導入
- [ ] `config.py` の `@deprecated` メソッドの整理
- [ ] `cli.py` の長い関数（`crosstabs` / `chi2` / `p005`）の分割

## 参考

- `sandbox/config.toml` — ICRC2023 の設問・選択肢定義
- `PLUGIN_DEVELOPMENT_GUIDE.md` — 新規プラグインの作り方
- `tests/` — フレームワークと ICRC2023Schema のテスト
