# Titanite

Diversityセッションの事前アンケートを集計するためのスクリプト群です。
PythonとJupyterノートブックを使って集計＆プロット作成します。

# TODO

1. GoogleスプレッドシートをCSV形式でダウンロードする（手動）
2. すべてのアンケート項目のヒストグラムを確認する
3. アンケート項目2つをクロス集計する

# 事前準備

```console
$ ghq git@github.com:ICRC2023/diversity.git
$ cd $ghqのルート/ICRC2023/diversity
$ poetry shell
$ poetry install
```

- ``ghq``を使ってリポジトリをクローンする（普通に``git clone``でもOK）
- ``poetry``を使ってPythonの仮想環境を構築する
  - メインは``pandas``と``altair``、 開発用に``jupyterlab``
  - 補助ツールに``commitizen``と``pysen``


# プロットの作成

Altairのギャラリーからサンプルを見繕っておきました

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
