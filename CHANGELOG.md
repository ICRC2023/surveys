## 0.4.1 (2023-07-23)

### Fix

- **data/test_data/prepared_data.csv**
  - メインデータを追加した
- **notebooks**
  - 01_preprocess.ipynb: カテゴリ型にキャストする方法を修正した
  - 04_chi2_test.ipynb: データフレームに画像のパスを追加した
  - q02_gender.ipynb: ジェンダーとの相関を確認した
  - q03_region.ipynb: 地域との相関を確認した
  - q12_group_initiatives.ipynb: グループの取り組みとの相関を確認した
  - q17_indiviudal_initiatives.ipynb: 個人の意識との相関を確認した
  - q13_gender_ratio.ipynb: グループ内の女性研究者の比率との相関を確認した
  - q19_interest.ipynb: 科学に興味をもった時期との相関を確認した
- **sandbox/config.toml**
  - 研究分野（実験／理論）のカテゴリにOthersを追加した
- **titanite/cli.py**:
  - カイ二乗検定の結果をJSONで保存できるようにした
  - コメントの分析結果をCSVで保存できるようにした
- **titanite/config.py**
  - crostab_ignore: クロス集計の総当たり確認の対象からq03とq04を除外した
  - crosstab_headers: クロス集計の相手となるカラム名を取得する機能を追加した
  - crosstab_data: 引数を追加した
  - comment_data: クラスター属性にカラム名を追加した
  - comment_data: コメントのデータ処理だけにした（ファイル保存をやめた）
  - crosstab_heatmap: グラフのフォントサイズを大きくした
  - crosstab_heatmap: 0より大きい部分だけテキスト表示するようにした
- **titanite/preprocess.py**:
  - binned_data: ビンのラベルにパーセントを追加した
- **typst/q18.typ**:
  - コメントの極性によって色が変わるようにした
- **typst/slide.typ**:
  - カイ二乗検定のJSONを追加した
  - クロス集計した結果を追加した
  - scipyのコードサンプルを短くした
  - フッターにページ番号が表示されるように修正した

## 0.4.0 (2023-07-22)

### Feat

- **titanite/core.py**: crosstab_loopを追加した

### Fix

- **notebooks**
  - 04_chi2_test.ipynb: p値を確認するノートブックを作った
- **titanite/cli.py**
  - crosstabsコマンドにsaveフラグを追加した
  - カイ二乗検定の結果をCSVに保存することにした

## 0.3.0 (2023-07-22)

### Feat

- **titanite/cli.py**: クロス集計用のコマンドを追加した
- **titanite/config.py**: 前処理したデータを読み込むクラスを追加した
- **titanite/core.py**: クロス集計する機能を追加した
- **titanite/preprocess.py**: ビン分割する関数を追加した

### Fix

- **notebooks**
  - 03_crosstab.ipynb: クロス集計するメソッドを作った
  - q02_gender.ipynb: カイ二乗検定のp値も確認した
  - q19_interest.ipynb: Q19の相関も確認した
  - renamed: ノートブックの名前を変更した
- **titanite/cli.py**:
  - Dataクラスで読み込むようにした
  - responseコマンドの説明を追加した
  - 前処理したデータのファイル名のデフォルト値を変更した
- **titanite/config.py**:
  - クロス集計から除外するカラムを追加した
- **titanite/core.py**:
  - クロス集計でカテゴリ型を維持するようにした
  - クロス集計する関数の引数を変更した
- **titanite/preprocess.py**:
  - 元データのカラム名を変更した

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
