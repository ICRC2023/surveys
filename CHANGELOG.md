## 0.5.0 (2023-09-17)

### Feat

- **data/main_data/**: 発表用の図を追加した
- **docs/notebooks/demographics/q01_age_group.ipynb**: demographicsを確認するノートブックを追加した
- **titanite/cli.py**: hbarコマンドを追加した
- **titanite/config.py**: Data.matches: 総当たりしたカラムを取得する機能を追加した
- **titanite/core.py**: hbar: ヒストグラムを追加した
- **titanite/preprocess.py**: クラスター分割を追加した

### Fix

- **.gitignore**: PDFを除外した（一時的）
- **config.toml**: clusterのカテゴリを追加した
- **data/test_data/categorical_data.csv**: 相関を集計するためのデータを追加した
- **data/test_data/chi2_test/chi2_test.csv**: chi2したデータを追加した
- **data/test_data/prepared_data.csv**: クラスターを追加した
- **data/test_data/prepared_data.csv**: 集約データを更新した
- **data/test_data/sentiment_data.csv**: 感情分析用のデータを追加した
- **docs/notebooks/10_chi2_map.ipynb**: ファイルを移動した
- **docs/notebooks/chi2_map.ipynb**: ファイル名を変更した
- **docs/notebooks/chi2_test_map.ipynb**: ヒートマップを作成するw関数をシンプルにした
- **docs/notebooks/chi2_test_map.ipynb**: ファイル名を変更した
- **docs/notebooks/demographics.ipynb**: パスを変更した
- **docs/notebooks/demographics.ipynb**: プロットのサイズを変更した
- **docs/notebooks/demographics.ipynb**: 円グラフの周囲に値を表示した
- **docs/notebooks/demographics.ipynb**: 微修正した
- **docs/notebooks/demographics.ipynb**: 読み込むデータのパスを修正した
- **docs/notebooks/demographics.ipynb**: 軸ラベルのフォントサイズを大きくした
- **docs/notebooks/demographics/demographics.ipynb**: 1次元の軸のデモグラフィックを追加した
- **docs/notebooks/demographics/demographics.ipynb**: demographicsを1次元で確認するノートブックを追加した
- **docs/notebooks/icrc2023_diversity.ipynb**: ファイルを移動した
- **docs/notebooks/responses.ipynb**: メールした日を追加した
- **docs/notebooks/responses.ipynb**: 回答数の推移を追加した
- **docs/notebooks/wip/q01_age_group.ipynb**: パスを変更した
- **docs/notebooks/wip/q12q17_bubblechart.ipynb**: q12とq17のバブル図を作成した
- **notebooks**: ノートブックを整理した
- **notebooks/00_config.ipynb**: ちょっと更新した
- **notebooks/00_config.ipynb**: 設定オプションをデータフレームにする
- **notebooks/02_insight.ipynb**: 箱ひげ図を追加した
- **notebooks/02_response.ipynb**: responseを分離した
- **notebooks/03_hbar.ipynb**: ヒストグラムの確認
- **notebooks/06_cluster.ipynb**: クラスター分割
- **notebooks/06_cluster.ipynb**: クラスタを確認するノートを追加した
- **notebooks/06_cluster.ipynb**: 新しいクラスタを見つけて確認中
- **notebooks/10_chi2_map.ipynb**: p値マップを追加した
- **notebooks/10_chi2_map.ipynb**: カイ二乗検定のp値マップを追加した
- **notebooks/10_chi2_map.ipynb**: 保存する画像ファイルの名前を変更した
- **notebooks/10_chi2_map.ipynb**: 相関関系の図を追加した
- **notebooks/10_chi2_map.ipynb**: 色の順番を反対にした
- **notebooks/10_quick_summary.ipynb**: 再実行した
- **notebooks/10_stats.ipynb**: 参加者の内訳を確認した
- **notebooks/icrc2023_diversity.ipynb**: q04（出身地）もクラスタにしてみた
- **notebooks/icrc2023_diversity.ipynb**: 画像のサイズを変更した
- **notebooks/icrc2023_diversity.ipynb**: 発表で使う図を作るノートブックを作成した
- **notebooks/icrc2023_diversity.ipynb**: 発表用のノートブックを更新した
- **notebooks/q01_age.ipynb**: 年齢との相関を確認した
- **notebooks/q02_gender.ipynb**: 再実行した
- **notebooks/q15_sentiment.ipynb**: 感情分析を追加した
- **pyproject.toml**: add deprecated
- **pyproject.toml**: update loguru
- **renamed**: docs/notebooks -> docs/logbooks に変更した
- **renamed**: 画像のファイル名を変更した
- **sandbox/config.toml**: アンケートに関係する全体の数値を追記した
- **sandbox/config.toml**: 新しい設定オプションを追加した
- **sandbox/config.toml**: 質問の番号キーを修正した
- **titanite/cli.py**: configコマンドを整理した
- **titanite/cli.py**: crosstabsからchi2を分離した
- **titanite/cli.py**: crosstabsコマンドの保存先を変更した
- **titanite/cli.py**: hbarコマンドを追加した
- **titanite/cli.py**: hbarコマンドを追加した
- **titanite/cli.py**: p < 0.05 のデータをカラムごとに作成できるようにした
- **titanite/cli.py**: p005: 引数チェックを追加した
- **titanite/cli.py**: prepare: Configクラス変更に伴う修正をした
- **titanite/cli.py**: prepare: 前処理で残すデータ形式を追加した
- **titanite/cli.py**: validなリストを追加した
- **titanite/cli.py**: 保存するパスを修正した
- **titanite/cli.py**: 微修正
- **titanite/config.py**: Config: optionsのメンバー変数を追加した
- **titanite/config.py**: Config.load_toml: ファイルの存在確認を追加した
- **titanite/config.py**: countを削除；responseと重複
- **titanite/config.py**: Data: ヘッダを扱う内部変数を整理した
- **titanite/config.py**: Data.read: カウント用のカラムを追加した
- **titanite/config.py**: Dataクラスにconfigメソッドを追加した
- **titanite/config.py**: matches: ignore -> valid に置き換えた
- **titanite/config.py**: カテゴリに関する内部変数を変更した
- **titanite/config.py**: カラム名を数値型とカテゴリ型にわけた
- **titanite/config.py**: 使わなくなった変数をコメントアウトした
- **titanite/config.py**: 廃止予定のメッセージ（のデコレータ）を追加した
- **titanite/config.py**: 設定を読み込む部分を見直した
- **titanite/core.py**: clusterのカラムを追加した
- **titanite/core.py**: comment_data: q11でソートした
- **titanite/core.py**: crosstab_loop: chi2のデータフレームにx軸とy軸のカラム名を追加した
- **titanite/core.py**: group_data, group_hbar: 全体的に書き換えた
- **titanite/core.py**: hbar, hbar_loop: 追加した
- **titanite/core.py**: hbar: ヒストグラム機能を追加した
- **titanite/core.py**: response: ヒートマップに戻した
- **titanite/preprocess.py**: categorical_data: クラスター分類をカテゴリ型に変換する処理を追加した
- **titanite/preprocess.py**: categorical_data: リファクタリング
- **titanite/preprocess.py**: categorical_data: 変換マップを追加した
- **titanite/preprocess.py**: save_data: 相関を確認する用と感情分析用のデータに分けて保存することにした
- **titanite/preprocess.py**: クラスターを追加した
- **titanite/preprocess.py**: クラスタの条件を修正した
- **titanite/preprocess.py**: 前処理の手順を修正した
- **typst**: 極性に合わせて文字色を変更した
- **typst/data**: symlinkを追加した
- **typst/q15.typ**: 感情分析について追記した
- **typst/questions.typ**: 質問票を作成した
- **typst/questions.typ**: 質問表を更新した
- **typst/questions.typ**: 質問表を更新した
- **typst/slide.typ**: 微修正
- **typst/slide.typ**: 更新した
- **typst/slide.typ**: 確認したことを追加した
- **typst/slide.typ**: 読み込むファイルのバスを修正した

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
