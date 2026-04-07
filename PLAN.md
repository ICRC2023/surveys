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

## 次のステップ

1. このPLAN.mdをレビュー・承認する
2. Phase 1の詳細なTODOリストを作成
3. 開発開始

---

## 参考資料

- 現在の `preprocess.py` 構造
- `sandbox/config.toml` ICRC2023設定
- 既存テスト（`tests/test_*.py`）
