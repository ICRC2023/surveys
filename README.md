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

## リポジトリ名について

リポジトリ名の``Titanite``は[チタン石](https://ja.wikipedia.org/wiki/%E3%83%81%E3%82%BF%E3%83%B3%E7%9F%B3)という鉱物の名前です。「スフェーン」という宝石としても知られているそうです。
光の当たり具合によってさまざまな色に見えるそうで「多様性」の意味をこめられるかなと思って採用しました。
