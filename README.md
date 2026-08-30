# Surveys at ICRC2023

ICRC2023 ダイバーシティセッションの参加者アンケートを分析するためのスクリプト集です。
Python で書かれたプラグイン型のサーベイ処理フレームワーク **Titanite** を中心に、
前処理・匿名化・統計解析・可視化までを一通り行います。

## Surveys

- 2023-07-09 to 2023-07-21 : Pre-Conference survey for the diversity session
- 2023-09-15 to 2023-09-22 : Post-Conference survey
- 参加者 1,406 名のうち 295 名から回答

## GitHub URLs

- Repos : https://github.com/ICRC2023/surveys/
- Pages : https://www.icrc2023.org/surveys/
  - サーベイ結果レポート（Quarto）: ルート
  - Titanite フレームワークドキュメント（Zensical）: `/titanite/`

## ディレクトリ構成

- `titanite/` : メインの Python パッケージ（`cli.py`, `config.py`, `core/`, `analysis.py`, `preprocess.py`）
- `plugins/` : アンケートごとのスキーマプラグイン（例: `plugins/icrc2023/ICRC2023Schema`）
- `sandbox/` : `config.toml` と CLI の作業ディレクトリ
- `data/`
  - `downloaded/` : Google フォームからの生エクスポート（**git 管理外**）
  - `private/` : 個票レベルのパイプライン出力（**git 管理外**）
  - `public/` : 匿名化・集計済みの公開用データ（コミット可）
- `docs/` : Titanite フレームワークドキュメント（Zensical, `zensical.toml`）
- `reports/` : ICRC2023 サーベイ結果レポート（Quarto, `reports/_quarto.yml`、`data/public/` のみ参照）
- `notebooks/` : 開発用・分析用ノートブック
- `Taskfile.yml` : 定型作業の自動化
- `pyproject.toml`, `uv.lock` : 依存関係管理

## Getting started

```console
$ git clone git@github.com:ICRC2023/surveys.git
$ cd surveys
$ uv sync --all-groups
...（省略）...
Installing the current project: titanite (0.7.0)
$ uv run ti --help
```

- ソースコードは GitHub で管理しています。リポジトリをクローンしてください。
- uv を使って Python の仮想環境（`.venv`）を構築します（`uv sync --all-groups`）。
  - メインは `pandas` と `altair`、統計に `scipy`、感情分析に `textblob`
  - 開発用に `pytest` と `ruff`、`pre-commit`、`commitizen`、`marimo`
  - ドキュメント生成用に `zensical`（レポートは別途 Quarto CLI が必要）
- `ti`（`titanite`）コマンドが使えることを確認する（`uv run ti --help`）

## Taskfile

定型作業は Taskfile にまとめてあります。`task` で一覧を確認できます。

```console
$ task test              # pytest を実行
$ task format             # ruff で整形
$ task lint               # ruff で lint
$ task pre-commit         # pre-commit フックを実行
$ task docs:serve         # Titanite ドキュメントをローカル配信（Zensical, http://localhost:8000）
$ task docs:build         # Titanite ドキュメントを site/ にビルド
$ task reports:preview    # サーベイ結果レポートをローカルプレビュー（Quarto）
$ task reports:render     # サーベイ結果レポートを reports/_site/ にレンダリング
$ task deps:outdated      # 更新可能なパッケージを確認
$ task deps:update        # 依存関係を更新
$ task nb:edit            # marimo ノートブックを編集モードで起動
$ task nb:run             # marimo ノートブックを実行モードで起動
```

## ドキュメント

独立した 2 つのサイトがあります。

- **Titanite フレームワークドキュメント** — Zensical（`zensical.toml`）、ソースは `docs/`
  ```console
  $ task docs:serve   # http://localhost:8000 で自動リロード
  $ task docs:build   # site/ に一度だけビルド
  ```
- **ICRC2023 サーベイ結果レポート** — Quarto（`reports/_quarto.yml`）、ソースは `reports/`、参照するのは `data/public/` のみ
  ```console
  $ task reports:preview   # ローカルプレビュー
  $ task reports:render    # reports/_site/ にビルド（reports/_freeze/ を利用）
  ```

CI（`.github/workflows/`）が両サイトを `https://www.icrc2023.org/surveys/` にデプロイします
（レポートはルート、フレームワークドキュメントは `/titanite/`）。

## データパイプライン

```
data/downloaded/*.csv   (生データ, git 管理外)
        │  ti prepare
        ▼
data/private/prepared_data.csv   (個票, フリーテキスト含む, git 管理外)
        │  ti anonymize / ti aggregate
        ▼
data/public/public_data.csv, data/public/aggregates/   (公開用, コミット可)
```

`data/private/` は個票レベルのデータで、絶対にコミットしません。
分析コマンド（`chi2`, `crosstabs`, `hbars`, `p005`, `comments`, `response`）は
デフォルトで `../data/private/prepared_data.csv` を読み込みます。

## CLI コマンド

CLI は `sandbox/` ディレクトリから、`config.toml` を参照して実行します。
ほとんどのコマンドは `--read_from` / `--write-dir` / `--load_from` に対応しています。

- `ti config` : 設定を表示（`--questions`, `--choices`）
- `ti prepare` : 生 CSV を前処理して `prepared_data.csv` を生成
  - `--plugin PLUGIN_NAME` でアンケートスキーマを指定（例: `plugins.icrc2023.ICRC2023Schema`）
  - `--plugin` なしの場合は従来の後方互換ワークフロー
- `ti anonymize` : `prepared_data.csv` から公開可能な個票データを生成
  - フリーテキスト列と `_ja` 翻訳を削除（感情スコアは保持）
  - `timestamp` を日単位に丸める
  - k 匿名性（デフォルト `--k 5`）を疑似識別子に適用
  - 出力: `data/public/public_data.csv`
- `ti aggregate` : `prepared_data.csv` から抑制済み頻度表を生成
  - 各カテゴリ列の `univariate/<col>.csv`、`--pair X,Y`（繰り返し可）でクロス集計
  - `--threshold`（デフォルト 5）未満のセルは抑制
  - 出力: `data/public/aggregates/`
- `ti comments` : フリーテキスト回答（q15-q22）を抽出・分析
- `ti response` : 回答日時のヒートマップを作成
- `ti hbar` / `ti hbars` : ヒストグラム（単一 / 全変数）
- `ti crosstab` / `ti crosstabs` : クロス集計（単一 / 全ペア）
- `ti chi2` : 全変数ペアのカイ二乗検定
- `ti p005` : 指定カラムと相関がある（`p < 0.05`）項目を抽出（`--save` で図を保存）

### 前処理の例

```console
$ cd sandbox
$ uv run ti prepare ../data/downloaded/survey.csv
Loaded config from: config.toml
Read data from: ../data/downloaded/survey.csv
- Replace data
- Split data
- Sentiment Analysis ... done!
- Categorize data
- Binned data
Saved data to: ../data/private/prepared_data.csv

# プラグインを指定する場合
$ uv run ti prepare ../data/downloaded/survey.csv --plugin plugins.icrc2023.ICRC2023Schema
```

### 統計解析・可視化の例

```console
$ cd sandbox
$ uv run ti response                # 回答日時のタイムライン
$ uv run ti hbars                   # 全変数のヒストグラム
$ uv run ti crosstabs               # 全ペアのクロス集計
$ uv run ti chi2                    # 全ペアのカイ二乗検定
$ uv run ti p005 q13 --save         # q13 と相関がある項目（p < 0.05）
```

## プラグインシステム

新しいアンケートに対応するには、`SurveySchema` 抽象クラスを実装したプラグインを作成します。
各スキーマは値置換ルール・地理情報分割・クラスタリング・ビン分割を定義します。
詳細は [`PLUGIN_DEVELOPMENT_GUIDE.md`](PLUGIN_DEVELOPMENT_GUIDE.md) を参照してください。

```console
$ cd sandbox
$ uv run ti prepare ../data/downloaded/survey.csv --plugin plugins.your_survey.YourSurveySchema
```

## クラスター

- クラスター用のカラムを追加する
  - 複雑な分割はせず、それぞれの項目で `Group1`、`Group2` の 2 分割（＋`Others`）にする
- `q01` : 40 歳を境目に若手（<=30s）、シニア（>=40s）のグループ？
- `q13 - q14` : `< 20% & Poor` と `>=30% & Good` のグループ？

## ノートブック

データはまずノートブックで確認しています。目的別に 2 つのディレクトリに分けています。
Marimo への移行を進めており、`task nb:edit` / `task nb:run` で起動できます。

### モジュールの開発・確認（`notebooks/development/`）

titanite のモジュール開発・動作確認用です。

- `00_config.ipynb`, `00_read_data.ipynb`
- `01_preprocess.ipynb`
- `02_insight.ipynb`, `02_response.ipynb`
- `03_crosstab.ipynb`, `03_hbar.ipynb`
- `04_chi2_test.ipynb`
- `05_others.ipynb`
- `06_cluster.ipynb`

### 調査分析（`notebooks/analysis/`）

ICRC2023 アンケートの分析・結果確認用です。

- `10_quick_summary.ipynb`, `10_stats.ipynb`, `30_comments.ipynb`
- `q01_age.ipynb`, `q02_gender.ipynb`, `q03_region.ipynb`
- `q12_group_initiatives.ipynb`, `q13_gender_ratio.ipynb`, `q13q14_clustered.ipynb`
- `q15_sentiment.ipynb`, `q17_individual_initiatives.ipynb`, `q19_interest.ipynb`

## プロットの作成

Altair のギャラリーからサンプルを見繕っておきました。

- 数値型 vs 数値型 → 散布図（`mark_point`）
- カテゴリ型 vs 数値型 → 箱ヒゲ図（`mark_boxplot`）
- カテゴリ型 vs カテゴリ型 → ヒートマップ（`mark_rect`）
- テキスト表示（`mark_text`）

- [ヒストグラム](https://altair-viz.github.io/gallery/simple_histogram.html)
- [散布図のマトリックス](https://altair-viz.github.io/gallery/scatter_matrix.html)
- [散布図とヒストグラム](https://altair-viz.github.io/gallery/scatter_marginal_hist.html)
- [ラベル付きの円グラフ](https://altair-viz.github.io/gallery/pie_chart_with_labels.html)
- [2次元ヒストグラム／ヒートマップ](https://altair-viz.github.io/gallery/histogram_heatmap.html)
- [バブル図](https://altair-viz.github.io/gallery/table_bubble_plot_github.html)
- [地図](https://altair-viz.github.io/gallery/choropleth.html)

## リポジトリ名について

リポジトリ名の `Titanite` は[チタン石](https://ja.wikipedia.org/wiki/%E3%83%81%E3%82%BF%E3%83%B3%E7%9F%B3)という鉱物の名前です。「スフェーン」という宝石としても知られているそうです。
光の当たり具合によってさまざまな色に見えるそうで「多様性」の意味をこめられるかなと思って採用しました。

![](./docs/_static/titanite.png)

## Update packages

パッケージを更新するときは `update-packages` ブランチを作成してください。
GitHub Actions が実行されるブランチを制限してあり、`main` 以外のブランチ名は `update-packages` だけ許可してあります。

```console
$ git checkout -b update-packages
$ task deps:outdated
$ task deps:update
$ task test
$ git add uv.lock
$ git commit -m "build(uv.lock): update dependencies"
$ git push origin update-packages
```

## セキュリティ・プライバシー

このプロジェクトは ICRC2023 のダイバーシティセッションの参加者アンケートを扱っており、個人を特定できる情報を含んでいます。

**重要な注意事項：**

- ✅ **生データ**（`data/downloaded/`）はローカルのみで処理
- ✅ **個票データ**（`data/private/`）は絶対にコミットしない
- ✅ `.gitignore` で CSV ファイルをリポジトリから除外
- ✅ 公開は `ti anonymize`（k 匿名性）と `ti aggregate`（セル抑制 n < 5）を経た `data/public/` のみ
- ✅ 分析結果の公開前に必ずプライバシーレビューを実施

**禁止事項：**

- ❌ 生データ・個票データのアップロード（GitHub / 外部サービス）
- ❌ ログへの個人情報含有
- ❌ プライバシーレビューなしの公開

### 品質管理

- **Pre-commit フック**: コミット時に自動チェック（lint, format, secret detection, 個票データのガード）
- **テスト**: `task test` / `uv run pytest`（69 テストでフレームワーク全体をカバー）
- **Conventional Commits**: commitizen によるコミットメッセージの自動検証

詳細は [`AGENTS.md`](AGENTS.md)、[`CLAUDE.md`](CLAUDE.md)、[`PLUGIN_DEVELOPMENT_GUIDE.md`](PLUGIN_DEVELOPMENT_GUIDE.md) を参照してください。
