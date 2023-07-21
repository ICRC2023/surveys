## 0.2.0 (2023-07-21)

### Feat

- **data/typst**: 自由回答のTypstテンプレートを追加した
- **titanite/cli.py**: コマンド名 create -> prepare に変更した
- **titanite/preprocess.py**: 自由回答の感情分析を追加した
- **titanite/preprocess.py**: 自由回答の自動翻訳を追加した

### Fix

- **data/typst/**: Typstテンプレートのヘッダー形式とデータ名を修正した
- **notebooks/01_preprocess.ipynb**: 感情解析のサンプルを追加した
- **notebooks/10_quick_summary.ipynb**: クロス集計の結果に合計（margins）を追加した
- **notebooks/10_quick_summary.ipynb**: q10とq13の回答をビン分割した
- **notebooks/10_quick_summary.ipynb**: クロス集計の項目をitertoolsを使って総当たりにした
- **notebooks/10_quick_summary.ipynb**: ヒストグラムを積み上げグラフ（割合）に変更した
- **notebooks/20_interest.ipynb**: Q19用のノートブックを作成した
- **notebooks/30_comments.ipynb**: 自由記述の出力をJSON形式に変更した
- **report/slide.typ**: カイ二乗検定を追記した
- **report/slide.typ**: レポートの書式を変更した
- **sandbox/app.py**: streamlitを追加した
- **sandbox/app.py**: ヒートマップを追加した
- **titanite/cli.py**: デフォルトの出力ファイル名を変更した
- **titanite/core.py**: group_dataの引数を変更した
- **titanite/preprocess.py**: 処理経過の進捗バーを追加した

### Build

- **pyproject.toml**: add scipy
- **pyproject.toml**: add streamlit
- **pyproject.toml**: add textblob
- **pyproject.toml**: add tqdm

## 0.1.2 (2023-07-16)

### Fix

- **notebooks**: ノートブックを更新した
  - 00_config.ipynb
  - 02_insight.ipynb
  - 05_others.ipynb
  - 10_quick_summary.ipynb
  - 20_gender.ipynb
  - comments.ipynb
- **renamed**:
  - core.py -> preprocess.pyに変更した
- **sandbox/config.toml**:
  - 地域名の並びを変更した
- **titanite/core.py**:
  - group_data
  - heatmap
- **titanite/preprocess.py**:
  - 回答が整数値のカラムをint型に変換した

### Build

- **pyproject.toml**: add geopandas

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
