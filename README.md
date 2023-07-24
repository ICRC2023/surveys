# Titanite

Diversityセッションの事前アンケートを集計するためのスクリプト群です。
PythonとJupyterノートブックを使って集計＆プロット作成します。

## TODO

1. GoogleスプレッドシートをCSV形式でダウンロードする（手動）
2. すべてのアンケート項目のヒストグラムを確認する
3. アンケート項目2つをクロス集計する

## 事前準備

```console
$ git clone git@github.com:ICRC2023/diversity.git
$ cd diversity
$ poetry shell
(venv) $ poetry install
...（省略）...
Installing the current project: titanite (0.1.0)
$ ti --help
```

- 任意の作用用ディレクトリに移動して、リポジトリをクローンする（``git clone``）
- Pythonの仮想環境をローカルに構築する（``poetry shell``）
- 必要なパッケージをローカルな仮想環境（``.venv``）インストールする（``poetry install``）
  - メインは``pandas``と``altair``、 開発用に``jupyterlab``
  - 補助ツールに``commitizen``と``pysen``
- ``ti``（``titanite``）コマンドが使えることを確認する（``ti --help``）

## データの前処理

CSV形式でダウンロードしたGoogleスプレッドシートを前処理して、CSVファイルに変換する

```console
$ cd sandbox
$ ti prepare ../data/raw_data/回答のスプレッドシート名.csv
Loaded config from: config.toml
Read data from: ../data/raw_data/20230720_icrc2023_diversity_presurvey_answers.csv
- Replace data
- Split data
- Sentiment Analysis ... done!
- Categorize data
- Binned data
Saved data to: ../data/test_data/prepared_data.csv
```

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
```

- 引数にカラム名を指定し、相関がある（＝``p < 0.05``）の項目を確認できます
  - カラム名はデータフレームにある項目を使ってください
  - ただし、クロス集計から除外対象にしている項目は使えません
  - 範囲外の値を指定した場合はエラーが出て終了します
- ``--read_from``で読み込むデータ（前処理済）を変更できます
- ``--write-dir``で作成したデータと図を保存するディレクトリを変更できます（ファイル名は変更できません）
- ``--load_from``で読み込む設定ファイルを変更できます
- ``--save``で図を保存します

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
