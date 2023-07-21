## 0.2.0 (2023-07-21)

### Feat

- **titanite/cli.py**: コマンド名を変更した: create -> prepare
- **data/typst**: 自由記述をPDFに変換するTypstのテンプレを追加した
- **titanite/preprocess.py**: 自由記述を自動翻訳することにした
- **titanite/preprocess.py**: 自由記入に対して感情分析できるようにした

### Fix

- **notebooks/10_quick_summary.ipynb**: crosstabに合計（margins）も追加した
- **report/slide.typ**: レポートの書式を変更した
- **notebooks/10_quick_summary.ipynb**: クロス集計を総当たりにした
- **notebooks/30_comments.ipynb**: データを更新した
- **report/slide.typ**: カイ二乗検定を追記した
- **pyproject.toml**: add scipy
- **notebooks/20_interest.ipynb**: Q19用のノートブックを作成した
- **notebooks/10_quick_summary.ipynb**: q10とq13をビンにした（仮）
- **report/slide.typ**: 報告用資料を更新した
- **report/slide.typ**: 拡張子を修正した
- **report/slide.type**: スライド用のTypstファイルを作成した
- **notebooks/10_quick_summary.ipynb**: 出力を全消し
- **notebooks/01_preprocess.ipynb**: q10とq13の回答をビン分割しようとしている
- **data/typst/**: コメント分析を更新した
- **titanite/cli.py**: デフォルトの出力ファイル名を変更した
- **data/typst/**: ヘッダーの形式とデータ名を修正した
- **titanite/preprocess.py**: 処理の経過を表示した
- **titanite/preprocess.py**: 進捗バーを追加した
- **pyproject.toml**: add tqdm
- **titanite/preprocess.py**: 自動翻訳時のデバッグ表示をオフにした
- **data/typst/q21.typ**: 読み込むデータ名を修正した
- **notebooks/10_quick_summary.ipynb**: データを更新した
- **notebooks/30_comments.ipynb**: 自由記述をJSONで書き出すことにした
- **notebooks/01_preprocess.ipynb**: 感情解析のサンプルを追加した
- **titanite/preprocess.py**: 自由記述を感情分析する関数を追加した（テスト中）
- **pyproject.toml**: add textblob
- **notebooks/10_quick_summary.ipynb**: 積み上げグラフ（割合）に変更してみた
- **notebooks/10_quick_summary.ipynb**: データを更新した
- **sandbox/app.py**: ヒートマップを追加した
- **notebooks/30_comments.ipynb**: ノートを修正した
- **sandbox/app.py**: streamlit appを追加した
- **pyproject.toml**: add streamlit
- **renamed**: ファイル名を変更した
- **notebooks/05_others.ipynb**: mark_pointで作ってみた
- **titanite/core.py**: group_dataの引数を変更した

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
