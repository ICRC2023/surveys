# Surveys at ICRC2023

A set of scripts to analyze survey for the Diversity session.
We will use Python and Jupyter notebooks to create the analysis & plots.

## Surveys

- 2023-07-08 to 2023-07-22 : Pre-Conference survey for the diversity session
- 2023-09-15 to 2023-09-22 : Post-Conference survey

## GitHub URLs

- Repos : https://github.com/ICRC2023/surveys/
- Pages : https://www.icrc2023.org/surveys/

## TODO

1. GoogleスプレッドシートをCSV形式でダウンロードする（手動）
2. すべてのアンケート項目のヒストグラムを確認する
3. アンケート項目2つをクロス集計する

## Getting started

```console
$ git clone git@github.com:ICRC2023/surveys.git
$ cd surveys
$ poetry install
...（省略）...
Installing the current project: titanite (0.6.0)
$ poetry run ti --help
```

- ソースコードはGitHubで管理しています。リポジトリをクローンしてください。
- Poetryを使ってPythonの仮想環境を構築します。
- 任意の作業用ディレクトリに移動して、リポジトリをクローンする（``git clone``）
- 必要なパッケージをローカルな仮想環境（``.venv``）にインストールする（``poetry install``）
  - メインは``pandas``と``altair``、開発用に``pytest``と``ruff``
  - ドキュメント生成用に``sphinx``と``myst-nb``
  - 補助ツールに``commitizen``
- ``ti``（``titanite``）コマンドが使えることを確認する（``poetry run ti --help``）

## Sphinx + Jupyter Notebook

```console
$ task docs:build
Building...
$ task docs:serve
# http://localhost:8000 でドキュメントが自動更新されながら表示されます
```

- Sphinxを使ってドキュメントを生成します
- Taskfileを使うと簡単に操作できます
- ``MyST-NB``を使っているので、``notebooks/``以下のJupyter Notebookの結果も確認できます
- ``sphinx-autobuild``により、ファイル変更時に自動で再ビルドされます

## データの前処理

CSV形式でダウンロードしたGoogleスプレッドシートを前処理して、CSVファイルに変換する

### デフォルト（ICRC2023）での前処理

```console
$ cd sandbox
$ poetry run ti prepare ../data/raw_data/回答のスプレッドシート名.csv
Loaded config from: config.toml
Read data from: ../data/raw_data/20230720_icrc2023_diversity_presurvey_answers.csv
- Replace data
- Split data
- Sentiment Analysis ... done!
- Categorize data
- Binned data
Saved data to: ../data/test_data/prepared_data.csv
```

### プラグインシステムを使った前処理

**NEW**: `--plugin` オプションでアンケートスキーマを指定可能

```console
$ cd sandbox
$ poetry run ti prepare ../data/raw_data/survey.csv --plugin plugins.icrc2023.ICRC2023Schema
```

**プラグインの作成**：

`PLUGIN_DEVELOPMENT_GUIDE.md` を参照して、新しいアンケート用のプラグインを作成できます。
各プラグインは独立したスキーマで、以下を定義します：

- 値置換ルール（value replacements）
- 地理情報分割（geographic splitting）
- クラスタリング（clustering）
- ビン分割（binning）

## 回答日時を調べたい

```console
$ cd sandbox
$ ti response
Read data from: ../data/test_data/prepared_data.csv
Saved chart to: ../data/test_data/response.png
$ open ../data/test_data/response.png
```

- 引数なしで実行できます
- ``--read_from``で読み込むデータ（前処理済）を変更できます
- ``--write-dir``で作成した図を保存するディレクトリを変更できます（ファイル名は変更できません）

## ヒストグラムを作成したい（WIP）

```console
$ cd sandbox
$ ti histogram --read_from=../data/test_data/prepared_data.csv
```

## クロス集計したい

```console
$ cd sandbox
$ ti crosstab
Loaded config from: config.toml
Read data from: ../data/test_data/prepared_data.csv
- Categorize
- Binned
Saved data to: ../data/test_data/crosstab/q01-q02.csv
Saved chart to: ../data/test_data/crosstab/q01-q02.png
Saved data to: ../data/test_data/crosstab/q01-q03.csv
Saved chart to: ../data/test_data/crosstab/q01-q03.png
...
```

- 引数なしで実行できます（ただし、そのうち変えるかも？）
- ``--read_from``で読み込むデータ（前処理済）を変更できます
- ``--write-dir``で作成したデータと図を保存するディレクトリを変更できます（ファイル名は変更できません）
- ``--load_from``で読み込む設定ファイルを変更できます

## カイ二乗検定したい

```console
$ cd sandbox
$ ti chi2
Loaded config from: config.toml
Read data from: ../data/test_data/prepared_data.csv
- Categorize
- Binned
Saved data to: ../data/test_data/chi2_test/chi2_test.csv
Saved data to: ../data/test_data/chi2_test/chi2_test.json
Saved data to: ../data/test_data/chi2_test/chi2_test_p005.csv
Saved data to: ../data/test_data/chi2_test/chi2_test_p005.json
```

- 引数なしで実行できます（ただし、そのうち変えるかも？）
- ``--read_from``で読み込むデータ（前処理済）を変更できます
- ``--write-dir``で作成したデータと図を保存するディレクトリを変更できます（ファイル名は変更できません）
- ``--load_from``で読み込む設定ファイルを変更できます

## ``p < 0.05`` したい

```console
$ cd sandbox
$ ti p005 カラム名 --save
- Categorize
- Binned
Saved data to ../data/test_data/p005/カラム名/chi2_test_p005_カラム名.csv
Saved data to ../data/test_data/p005/カラム名/chi2_test_p005_カラム名.json
Saved chart to ../data/test_data/p005/カラム名/カラム名-相手カラム名.png
```

- 引数にカラム名を指定し、相関がある（＝``p < 0.05``）の項目を確認できます
  - カラム名はデータフレームにある項目を使ってください
  - ただし、クロス集計から除外対象にしている項目は使えません
  - 範囲外の値を指定した場合はエラーが出て終了します
- ``--read_from``で読み込むデータ（前処理済）を変更できます
- ``--write-dir``で作成したデータと図を保存するディレクトリを変更できます（ファイル名は変更できません）
- ``--load_from``で読み込む設定ファイルを変更できます
- ``--save``で図を保存します

## クラスター

- クラスター用のカラムを追加する
  - 複雑な分割はせず、それぞれの項目で``Group1``、``Group2``の2分割（＋``Others``）にする
- ``q01`` : 40歳を境目に若手（<=30s）、シニア（>=40s）のグループ？
- ``q13 - q14`` : ``< 20% & Poor`` と ``>=30% & Good``のグループ？

## Jupyterノートブック

データはまずノートブックで確認しています。
いくつかのノートブックは整理が必要です。

### モジュールの開発・確認

- ``00_config.ipynb``
- ``01_preprocess.ipynb``
- ``02_insight.ipynb``
- ``03_crosstab.ipynb``
- ``05_others.ipynb``

### とりあえず分析

- ``10_quick_summary.ipynb``
- ``30_comments.ipynb``

### クロス集計の詳細を確認

- ``q02_gender.ipynb``
- ``q19_gender.ipynb``

## プロットの作成

Altairのギャラリーからサンプルを見繕っておきました

- 数値型 vs 数値型 → 散布図（``mark_point``）
- カテゴリ型 vs 数値型 → 箱ヒゲ図（``mark_boxplot``）
- カテゴリ型 vs カテゴリ型 → ヒートマップ（``mark_rect``）
- テキスト表示（``mark_text``）

- [ヒストグラム](https://altair-viz.github.io/gallery/simple_histogram.html)
- [散布図のマトリックス](https://altair-viz.github.io/gallery/scatter_matrix.html)
- [散布図とヒストグラム](https://altair-viz.github.io/gallery/scatter_marginal_hist.html)
- [ラベル付きの円グラフ](https://altair-viz.github.io/gallery/pie_chart_with_labels.html)
- [2次元ヒストグラム／ヒートマップ](https://altair-viz.github.io/gallery/histogram_heatmap.html)
- [バブル図](https://altair-viz.github.io/gallery/table_bubble_plot_github.html)
- [地図](https://altair-viz.github.io/gallery/choropleth.html)

## リポジトリ名について

リポジトリ名の``Titanite``は[チタン石](https://ja.wikipedia.org/wiki/%E3%83%81%E3%82%BF%E3%83%B3%E7%9F%B3)という鉱物の名前です。「スフェーン」という宝石としても知られているそうです。
光の当たり具合によってさまざまな色に見えるそうで「多様性」の意味をこめられるかなと思って採用しました。

![](./docs/_static/titanite.png)

## Update packages

パッケージを更新するときは``update-packages``ブランチを作成してください。
GitHub Actionsが実行されるブランチを制限してあり、``main``以外のブランチ名は``update-packages``だけ許可してあります。

### Taskfileを使った更新方法（推奨）

```console
$ git checkout -b update-packages
$ task deps:check
$ task deps:update
$ task test
$ git add poetry.lock
$ git commit -m "build(poetry.lock): update dependencies"
$ git push origin update-packages
```

### 個別パッケージを更新する場合

```console
$ git checkout -b update-packages
$ poetry show --outdated
$ poetry add パッケージ名@latest
$ git add pyproject.toml poetry.lock
$ git commit -m "build(pyproject.toml): updated パッケージ名: x.y.z -> X.Y.Z"

$ poetry add パッケージ名@latest --group docs
$ git add pyproject.toml poetry.lock
$ git commit -m "build(pyproject.toml): updated パッケージ名(docs): x.y.z -> X.Y.Z"
```

## セキュリティ・プライバシー

### データ保護

このプロジェクトは ICRC2023 のダイバーシティセッションの参加者アンケートを扱っており、個人を特定できる情報を含んでいます。

**重要な注意事項：**

- ✅ **生データ** (`data/raw_data/`) はローカルのみで処理
- ✅ `.gitignore` で CSV ファイルをリポジトリから除外
- ✅ 分析結果の公開前に必ずプライバシーレビュー実施
- ✅ セル抑制（n < 5 の場合は非表示）を実装

**禁止事項：**

- ❌ 生データのアップロード（GitHub/外部サービス）
- ❌ ログへの個人情報含有
- ❌ プライバシーレビューなしの公開

### 品質管理

- **Pre-commit フック**: コミット時に自動チェック（lint, format, secret detection）
- **テストカバレッジ**: 69個のテストで完全カバレッジ
- **Conventional Commits**: コミットメッセージの自動検証

詳細は `CLAUDE.md` と `PLUGIN_DEVELOPMENT_GUIDE.md` を参照してください。
