# PLAN.md - Titanite アーキテクチャ再設計

このドキュメントは、titanite モジュールを汎用的なアンケート処理フレームワークに進化させるための実装計画です。

## ビジョン

**汎用的なGoogle Forms対応アンケート処理フレームワーク**を実現し、ICRC2023をテンプレートとしながら、他のアンケートプロジェクトでも再利用できる設計にする。

---

## 現状分析

### 汎用的な部分（フレームワーク化候補）
- CSVローダー（`skiprows=1` の処理）
- タイムスタンプ変換
- 地理情報の分割（`/` で区切られたデータ）
- カテゴリ型変換（Pydantic + TOML設定）
- 感情分析（TextBlob）
- クロス集計・統計分析

### プロジェクト固有の部分（プラグイン化候補）
- `replace_data()`: q03/q04/q14 の値置換ルール
- `cluster_data()`: 4つのクラスタ定義（q01, q13, q01q02, q13q14）
- `binned_data()`: q10/q13 のビン分割設定
- `sentiment_data()`: 自由記述列の指定（q15-q22）
- スキーマ定義: CATEGORICAL_HEADERS, NUMERICAL_HEADERS

---

## 推奨アーキテクチャ

```
titanite/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── loader.py           # CSVローダー（汎用）
│   ├── schema.py           # スキーマベースクラス（テンプレート）
│   ├── processor.py        # 処理パイプライン（汎用）
│   └── validators.py       # バリデーション（汎用）
│
├── plugins/
│   ├── __init__.py
│   └── icrc2023/           # ICRC2023プロジェクト用プラグイン
│       ├── __init__.py
│       ├── schema.py       # ICRC2023スキーマ定義
│       ├── rules.py        # ICRC2023固有ルール（replace, cluster, binned）
│       └── config.toml     # アンケート設定
│
├── cli.py                  # CLI（プラグイン選択可能に更新）
├── analysis.py
├── core.py
└── config.py               # 現在の Config, Data クラス（互換性維持）

```

---

## セキュリティ・プライバシー要件

**アンケート回答のセンシティブ性が高いため、以下を厳格に実装する。**

### 1. オリジナルデータの隔離

**原則**: オリジナルの回答データはリポジトリに保存しない

- ✅ **許可**: `data/raw_data/` は `.gitignore` で除外
- ✅ **許可**: ローカルマシンでのみ処理
- ❌ **禁止**: CSVファイルをコミット
- ❌ **禁止**: GitHub/GitLabにアップロード

**.gitignore設定**（確認・更新が必要）

```gitignore
# 生のアンケートデータ（絶対に漏洩させない）
data/raw_data/*.csv
data/raw_data/*.xlsx
data/raw_data/*.json

# 処理途中の機密データ
data/test_data/prepared_data.csv
data/test_data/categorical_data.csv
data/test_data/sentiment_data.csv
data/test_data/*_data.csv

# 自動生成されたキャッシュ
.cache/
*.tmp
__pycache__/
.pytest_cache/
```

### 2. 処理済み・公開可能なデータ

**許可範囲**: 以下のみリポジトリに保存
- ✅ クロス集計結果（n < 5 は抑制）
- ✅ 統計検定結果（p値、カイ二乗統計量）
- ✅ 分析結果・グラフ（個人識別できない集約データ）
- ✅ ドキュメント・報告書

**テストデータ**:
- ✅ ダミー・合成データ（実際の回答ではない）のみ使用
- `data/test_data/` に最小限のテストCSV を保持可能

### 3. セキュアなワークフロー

**段階1: ローカル処理**

```bash
# 生データはローカルのみ
cd sandbox
poetry run ti prepare ../data/raw_data/SENSITIVE_SURVEY.csv
# ↓ 出力: prepared_data.csv（ローカルのみ）
```

**段階2: 分析・要約**

```bash
# 集約・統計データのみを抽出
poetry run ti chi2
poetry run ti crosstabs
# ↓ 出力: chi2_test.csv, crosstab/*.png（中間結果）
```

**段階3: 公開用データ準備**

```python
# 統計結果だけを抽出してJSON化
# n < 5のセルは削除
# 個人識別可能な列は削除
# プライバシーレビュー実施
```

### 4. リスク軽減策

#### A. ファイルアクセス制御

```python
# titanite/core/security.py
class SecureDataHandler:
    """
    機密データの処理を厳格に管理
    """

    @staticmethod
    def load_sensitive_data(filepath: Path) -> pd.DataFrame:
        """
        生データをメモリにロード（ファイルは上書きしない）
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")

        # メモリ内でのみ処理
        data = pd.read_csv(filepath)
        return data

    @staticmethod
    def suppress_small_cells(data: pd.DataFrame, threshold: int = 5) -> pd.DataFrame:
        """
        セル抑制: n < threshold のセルを削除
        プライバシー保護のためクロス集計結果に適用
        """
        # 実装例
        return data[data["count"] >= threshold]

    @staticmethod
    def anonymize_for_publication(data: pd.DataFrame) -> pd.DataFrame:
        """
        公開用データの匿名化
        - 個人識別可能な列を削除
        - タイムスタンプを集約
        - 自由記述テキストを削除
        """
        safe_columns = [col for col in data.columns
                       if col not in ["timestamp", "q15", "q16", "q18", "q20", "q21", "q22"]]
        return data[safe_columns]
```

#### B. ログ・出力管理

```python
# titanite/core/processor.py
class SurveyProcessor:
    def process(self, df: pd.DataFrame, config: Config,
                secure_mode: bool = True) -> pd.DataFrame:
        """
        secure_mode=True: 個人情報をログに出力しない
        """
        if secure_mode:
            logger.info(f"Processing {len(df)} responses")
            # ❌ 個人データをログに出力しない
            # logger.debug(df.head())  # 危険

        # 処理...
        return df
```

#### C. メモリクリーンアップ

```python
# 処理完了後、機密データをメモリから削除
import gc

def cleanup_sensitive_data(data: pd.DataFrame):
    """
    機密データをメモリから確実に削除
    """
    del data
    gc.collect()
```

### 5. CI/CD セキュリティ

**GitHub Actions設定** (`.github/workflows/`)

```yaml
name: Secure Processing

on: [push, pull_request]

jobs:
  check-sensitive-files:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for sensitive files
        run: |
          # raw_data/ にCSVが含まれていないか確認
          if find data/raw_data -name "*.csv" -o -name "*.xlsx" 2>/dev/null | grep -q .; then
            echo "❌ ERROR: Sensitive data files detected in raw_data/"
            exit 1
          fi
          echo "✅ No sensitive data files found"

      - name: Run tests (no real data)
        run: |
          poetry run pytest
```

### 6. ドキュメント・チェックリスト

**開発者向け安全宣言**

```markdown
## セキュリティ承認事項

このプロジェクトに関わる全開発者は以下を確認：

- [ ] `data/raw_data/` はGitに含まれない（.gitignore確認）
- [ ] ローカルマシンでのみ処理（リモートサーバー不使用）
- [ ] コミット前に `git status` で機密ファイルがないか確認
- [ ] 分析結果公開前に プライバシーレビュー実施
- [ ] 作業完了後、ローカルCSVを削除（`rm data/raw_data/*.csv`）
```

---

## 詳細設計

### 1. `titanite/core/schema.py` - スキーマベースクラス

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

class SurveySchema(ABC):
    """
    アンケートスキーマのベースクラス

    サブクラスで以下を定義する：
    - categorical_headers: カテゴリ型カラムのリスト
    - numerical_headers: 数値型カラムのリスト
    - free_text_columns: 自由記述カラムのリスト
    - replace_rules: 値置換ルール
    - cluster_rules: クラスタリング定義
    - bin_rules: ビン分割定義
    """

    categorical_headers: list[str] = []
    numerical_headers: list[str] = []
    free_text_columns: list[str] = []

    @abstractmethod
    def get_replace_rules(self) -> dict:
        """値置換ルール"""
        pass

    @abstractmethod
    def get_cluster_rules(self) -> list[dict]:
        """クラスタリング定義"""
        pass

    @abstractmethod
    def get_bin_rules(self) -> list[dict]:
        """ビン分割定義"""
        pass
```

### 2. `plugins/icrc2023/schema.py` - ICRC2023スキーマ

```python
from titanite.core.schema import SurveySchema

class ICRC2023Schema(SurveySchema):
    """ICRC2023ダイバーシティセッション調査"""

    categorical_headers = [
        "q01", "q02", "q03_regional", "q03_subregional",
        "q04_regional", "q04_subregional", "q05", "q06", "q07",
        "q08", "q09", "q10_binned", "q11",
        "q12_genderbalance", "q12_diversity", "q12_equity",
        "q12_inclusion", "q13_binned", "q14",
        "q17_genderbalance", "q17_diversity", "q17_equity",
        "q17_inclusion", "q19",
    ]

    numerical_headers = [
        "q10", "q13",
        "q15_polarity", "q15_subjectivity",
        "q16_polarity", "q16_subjectivity",
        # ... etc
    ]

    free_text_columns = ["q15", "q16", "q18", "q20", "q21", "q22"]

    def get_replace_rules(self) -> dict:
        return {
            "q03": {
                "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
                "Oceania": "Oceania / Oceania",
            },
            "q04": {
                "Prefer not to answer": "Prefer not to answer / Prefer not to answer",
                "Oceania": "Oceania / Oceania",
            },
            "q14": {"No Interest": "No interest"},
        }

    def get_cluster_rules(self) -> list[dict]:
        return [
            {
                "name": "q01_clustered",
                "description": "Age cluster: <40s vs >=40s",
                "apply": lambda df: self._cluster_q01(df),
            },
            # ... 他の3つのクラスタ
        ]

    def get_bin_rules(self) -> list[dict]:
        return [
            {
                "column": "q10",
                "bins": [-1, 0, 1, 2, ..., 25],
                "labels": ["Prefer not to answer", "0", "1", ..., "10+"],
            },
            # ... q13_binned
        ]

    @staticmethod
    def _cluster_q01(df):
        # q01クラスタリングロジック
        pass
```

### 3. `titanite/core/processor.py` - 汎用処理パイプライン

```python
class SurveyProcessor:
    """
    スキーマベースのアンケート処理パイプライン
    """

    def __init__(self, schema: SurveySchema):
        self.schema = schema

    def process(self, df: pd.DataFrame, config: Config) -> pd.DataFrame:
        """フルパイプライン実行"""
        df = self._add_timestamp(df)
        df = self._add_response_counter(df)
        df = self._apply_replace_rules(df)
        df = self._split_geographic_data(df)
        df = self._apply_cluster_rules(df)
        df = self._apply_bin_rules(df)
        df = self._categorize_data(df, config)
        df = self._sentiment_analysis(df)
        return df

    def _apply_replace_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """スキーマの置換ルールを適用"""
        rules = self.schema.get_replace_rules()
        for column, replace_map in rules.items():
            if column in df.columns:
                df[column] = df[column].replace(replace_map)
        return df

    def _apply_cluster_rules(self, df: pd.DataFrame) -> pd.DataFrame:
        """スキーマのクラスタリングルールを適用"""
        rules = self.schema.get_cluster_rules()
        for rule in rules:
            df[rule["name"]] = rule["apply"](df)
        return df

    # ... 他のメソッド
```

### 4. `titanite/cli.py` - プラグイン対応CLIに更新

```python
@app.command()
def prepare(
    read_from: str,
    plugin: str = typer.Option("icrc2023", help="Survey plugin name"),
    write_dir: str = "../data/test_data/",
    load_from: str = "config.toml",
) -> None:
    """
    Prepare data with specified survey plugin.

    Parameters
    ----------
    read_from : str
        Path to raw CSV file from Google Forms
    plugin : str, optional
        Plugin name (e.g., 'icrc2023'), by default "icrc2023"
    write_dir : str, optional
        Output directory, by default "../data/test_data/"
    load_from : str, optional
        Config file path, by default "config.toml"
    """
    # プラグインをロード
    schema = _load_schema(plugin)

    # 処理実行
    config = Config(load_from=load_from)
    config.load()

    logger.info(f"Read data from: {read_from}")
    data = pd.read_csv(read_from, skiprows=1)

    processor = SurveyProcessor(schema)
    data = processor.process(data, config)

    # 保存
    fname = Path(write_dir) / "prepared_data.csv"
    data.to_csv(fname, index=False)
    save_data(data, write_dir)

def _load_schema(plugin_name: str):
    """プラグインからスキーマを動的ロード"""
    import importlib
    module = importlib.import_module(f"titanite.plugins.{plugin_name}.schema")
    return module.ICRC2023Schema()  # または getattr で動的に
```

---

## 実装フェーズ

### Phase 1: 基盤整備（1-2週間）

**目標**: `titanite/core/` に汎用部分を整理

1. `core/schema.py` を作成：スキーマベースクラス定義
2. `core/processor.py` を作成：汎用処理パイプライン
3. 既存コード（preprocess.py）から汎用部分を抽出
4. 後方互換性の確保（既存APIは変更しない）

**成果物**:
- 汎用スキーマフレームワーク
- 汎用処理パイプライン
- テスト（既存テストが全て通る）

### Phase 2: ICRC2023プラグイン化（1-2週間）

**目標**: ICRC2023固有ロジックをプラグインに移行

1. `plugins/icrc2023/schema.py` を作成
2. `plugins/icrc2023/rules.py` に ルール定義を移動
3. 既存 `preprocess.py` からロジックを抽出・統合
4. `plugins/icrc2023/config.toml` を配置

**成果物**:
- ICRC2023プラグイン
- 既存ワークフローと同等の動作確認

### Phase 3: CLI更新（1週間）

**目標**: プラグイン選択可能なCLIに更新

1. `cli.py` の `prepare()` に `--plugin` オプション追加
2. `_load_schema()` 関数実装
3. ヘルプ・ドキュメント更新

**成果物**:
- 動的プラグイン対応CLI
- ドキュメント更新

### Phase 4: 検証・最適化（1週間）

**目標**: フレームワークの汎用性確認

1. テストスイート拡充（スキーマ・プロセッサ単位テスト）
2. ドキュメント整備
3. パフォーマンス測定
4. 他のアンケート例でテスト（シミュレーション）

**成果物**:
- 包括的なテスト
- 開発者向けドキュメント（新規プラグイン作成ガイド）

---

## メリット

| 観点 | メリット |
|------|----------|
| **再利用性** | 新規アンケート追加時：`plugins/*/` 追加だけで OK |
| **保守性** | ICRC2023ロジックが独立、他の更新の影響を受けない |
| **拡張性** | スキーマ継承で新ルール追加が簡単 |
| **テスト性** | スキーマ・プロセッサが分離、単体テスト効率向上 |
| **可読性** | ドメイン固有ロジックが明確に分離 |
| **学習効果** | 他チームが新規アンケート実装する際のテンプレート |

---

## リスクと対策

| リスク | 対策 |
|--------|------|
| 既存コードの破壊 | Phase 2の終了まで既存API互換性維持 |
| パフォーマンス低下 | Phase 4で計測・最適化 |
| プラグイン複雑度 | ドキュメント・テンプレート充実 |
| マイグレーション漏れ | チェックリスト作成・レビュー |

---

## Phase 5: プライバシー要件の実施（最優先）

Phase 1-4 でフレームワーク（`core/`, `plugins/icrc2023/`, `SecureDataHandler`）は実装済み。
しかし本章「セキュリティ・プライバシー要件」の**実施が未完**で、以下の状態が残っている。

### 現状の問題（2026-08 レビューで判明）

- リポジトリは **PUBLIC**（`https://github.com/ICRC2023/surveys`）
- `data/test_data/prepared_data.csv`（295行・58列）が **平文でコミット済み**
  - 個票（1行 = 1回答者）のまま、集計されていない
  - 自由記述の原文 `q15/q16/q18/q20/q21/q22` と日本語訳 `*_ja` を含む
  - `timestamp`（秒単位）を含む
  - 準識別子の組み合わせ（年代 × 性別 × 勤務地域）で 53/295 人が一意
  - 自由記述に職場・大学名の言及があり、公開参加者名簿との照合で特定可能
- `.gitignore` の `test_data` パターンは非アンカーだが `data/test_data/*.csv` は無視されていない
  （本章 72-91 行の `.gitignore` 設定が未適用）
- `SecureDataHandler`（`suppress_small_cells` / `anonymize_for_publication`）は実装済みだが
  **パイプラインのどこからも呼ばれていない**（tests 以外に使用箇所なし）
- `docs/` の **26 個の .ipynb** が `data/test_data/prepared_data.csv` を直接読む
- CI（`.github/workflows/static.yml`）が `main` への push ごとに myst-nb でノートを実行し、
  その出力（自由記述の引用・n<5 のクロス集計表を含みうる）を **GitHub Pages で公開**

### 対応方針（案1: 匿名化済みデータをコミット）

`SecureDataHandler` を実パイプラインに組み込み、公開しても安全な派生ファイルを生成する。

```text
raw CSV                (ローカルのみ、.gitignore)
   ↓ ti prepare
prepared_data.csv      (ローカルのみ、.gitignore)  ← 個票 + 自由記述原文
   ↓ ti anonymize      ← 新規コマンド: SecureDataHandler を通す
public_data.csv        (コミット可)  ← timestamp除去 / q15-q22除去 / *_ja除去 / n<5セル秘匿
```

### タスク

1. **[緊急] 追跡中の機密 CSV を除去**
   - `git rm --cached data/test_data/*.csv data/test_data/chi2_test/*.csv`
   - `.gitignore` に `data/**/*.csv` `data/**/*.json` を明示追加（本章 72-91 行を反映）
   - 公開リポジトリのため、履歴からの完全除去（`git filter-repo`）を実施するか要判断
     - 実施する場合、既存クローン・フォークの扱いを ICRC2023 Diversity Group と協議
2. **[緊急] 公開中の GitHub Pages を精査**
   - `q15_*.ipynb` `q16_*.ipynb` `q18_*.ipynb` が自由記述の原文を出力していないか確認
   - 出力していれば、原文を出さず件数・感情スコア分布・カテゴリ集計に作り替え
   - n<5 のクロス集計表がそのまま出ていないか確認
   - 精査完了まで Pages デプロイを一時停止するか要判断
3. **`ti anonymize` コマンドを実装** — ✅ 完了（PR: feat/ti-anonymize）
   - `SecureDataHandler` に `generalize_timestamp` / `k_anonymize` /
     `build_public_dataset` を追加（既存 3 メソッドは非変更）
   - `SurveySchema` に `quasi_identifiers` / `public_drop_columns` を追加、
     `ICRC2023Schema` で `["q01", "q02", "q03_regional"]` /
     地域詳細列 + `response` を指定
   - 自由記述列（`free_text_columns`）と `_ja` 翻訳を削除、感情スコアは保持
   - `timestamp` を日付粒度に丸め（`dt.floor("D")`）
   - k=5 の k-匿名化で 295 → 245 行（残 83%）
   - 出力 `data/public/public_data.csv`（コミット対象）
   - 個票の抜け道になる `q03/q04` の subregional は落とす。subregional 粒度の
     内訳は次項の集計データ（方式A）で n<5 秘匿して公開する
4. **方式A: 集計データ公開コマンドを実装**（別 PR）
   - `suppress_small_cells` で n<5 セルを伏せた集計 CSV を生成
   - q03/q04 の subregional 内訳、demographics、少数セルはこちらで扱う
5. **`ti prepare` の出力パスを見直し**
   - `prepared_data.csv` は `.gitignore` 対象ディレクトリ（例: `data/local/`）に出す
   - `write_dir` のデフォルトを変更
6. **ノート 26 個の参照先を一括置換**
   - q01〜q14 の 23 ノート: `f_csv` を `.../public_data.csv` に置換
   - q03/q04/demographics の 3 ノート: 方式A の集計 CSV を読む形に改修
   - 自由記述系ノート（q15/q16/q18）は 2. の作り替えで対応
7. **CI ガードを追加**（本章 212-238 行を反映）
   - `data/` 配下に個票 CSV（自由記述列を持つ CSV）が含まれていないかチェックするジョブ
   - pre-commit フックにも同等のチェックを追加

### 成果物

- コミット可能な `public_data.csv`（匿名化済み・集計済み）
- `ti anonymize` コマンドとそのテスト
- 自由記述を露出しないよう作り替えた q15/q16/q18 ノート
- CI / pre-commit の機密ファイル検出ガード
- 履歴クリーンアップの実施記録（実施する場合）

---

## 次のステップ

1. このPLAN.mdをレビュー・承認する
2. **Phase 5 を最優先で着手**（プライバシー要件の実施）
3. Phase 1 の詳細な TODO リストを作成（型ヒント等の品質改善は Phase 5 完了後）
4. 開発開始

---

## 参考資料

- 現在の `preprocess.py` 構造
- `sandbox/config.toml` ICRC2023設定
- 既存テスト（`tests/test_*.py`）
