## 0.1.2 (2023-07-16)

### Fix

- **notebooks**: ノートを追加した
- **titanite/core.py**: ヒートマップをつくる関数を追加した
- **titanite/preprocess.py**: 回答が整数値のカラムをint型に変換した
- **pyproject.toml**: add geopandas
- **titanite/core.py**: グループ化する関数を追加した
- **titanite/core.py**: グループ化するコマンドを追加した
- **notebooks/20_gender.ipynb**: ジェンダーを軸にして分析するノートブックを追加した
- **notebooks/10_quick_summary.ipynb**: 前処理をcategorical_dataに置き換えた
- **notebooks/00_config.ipynb**: volumesセクションの確認を追加した
- **sandbox/config.toml**: 地域名の並びを変更した
- **renamed**: ファイル名をpreprocess.pyに変更した
- **renamed**: ノートブックの名前を変更した
- **notebooks/comments.ipynb**: コメントを整理するためのノートブックを作成した

## 0.1.1 (2023-07-16)

### Fix

- **.gitignore**:
  - ignore macOS, Python related files
  - ignore files with "tmp_" prefix
- **notebooks/config.ipynb**:
  - 設定ファイル（config.toml）を読み込むときの手順を整理した
- **notebooks/others.ipynb**:
  - それぞれの回答の相関を確かめている
- **notebooks/preprocess.ipynb**:
  - データを前処理するときの手順を整理した
- **notebooks/quick_summary.ipynb**:
  - とりあえず集計できるか確かめた
- **sandbox/config.toml**:
  - 設定ファイルを用意した
  - カテゴリーを追加した
  - データ置き場を追加した
- **titanite/__init__.py**:
  - __version__を追加した
  - config.Configを追加した
  - core.preprocess_dataを追加した
  - core.categorical_dataを追加した
- **titanite/cli.py**:
  - cli.configを追加した
  - cli.createを追加した
- **titanite/config.py**:
  - config.Configクラスを作成した
  - 引数を修正した（confdを削除した）
  - 設定ファイルを確認できるようにした（show）
  - 設定ファイルからカテゴリー型を作成できるようにした（categories）
- **titanite/core.py**:
  - データを前処理できるようにした（preprocess_data）
  - データをカテゴリー型に変換できるようにした（categorical_data）

### Build

- **pyproject.toml**: added altair
- **pyproject.toml**: added commitizen
- **pyproject.toml**: added jupyterlab
- **pyproject.toml**: added loguru
- **pyproject.toml**: added pandas
- **pyproject.toml**: added pytest
- **pyproject.toml**: added typer
- **pyproject.toml**: added vl-convert-python
- **pyproject.toml**: added pydantic
