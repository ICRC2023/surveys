# CLI Commands

Complete reference for titanite command-line interface.

## General

### `ti --help`

Display help message and list all available commands.

### `ti --version`

Show version number.

## Configuration

### `ti config`

Show current survey configuration.

**Options:**
- `--questions` - Display question definitions
- `--choices` - Display available choices/categories

**Example:**

```bash
poetry run ti config --questions
poetry run ti config --choices
```

## Data Preparation

### `ti prepare`

Preprocess raw CSV data from Google Forms and generate prepared data.

**Usage:**

```bash
poetry run ti prepare <input_file> [OPTIONS]
```

**Options:**
- `--plugin PLUGIN_NAME` - Specify survey schema (e.g., `plugins.icrc2023.ICRC2023Schema`)
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti prepare ../data/raw_data/survey.csv
poetry run ti prepare data.csv --plugin plugins.icrc2023.ICRC2023Schema
```

**Outputs:**
- `prepared_data.csv` - Full processed dataset
- `categorical_data.csv` - Categorical variables only
- `sentiment_data.csv` - Sentiment analysis scores

## Analysis Commands

### `ti chi2`

Run chi-square tests for all variable pairs to identify statistical associations.

**Usage:**

```bash
poetry run ti chi2 [OPTIONS]
```

**Options:**
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti chi2
```

### `ti p005`

Extract significant correlations (p < 0.05) for a specific column.

**Usage:**

```bash
poetry run ti p005 <column_name> [OPTIONS]
```

**Options:**
- `--save` - Save results to CSV file
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti p005 q13 --save
```

### `ti crosstabs`

Create cross-tabulation analysis for all variable pairs.

**Usage:**

```bash
poetry run ti crosstabs [OPTIONS]
```

**Options:**
- `--save` - Save results to file
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti crosstabs --save
```

### `ti crosstab`

Create cross-tabulation for a single pair of variables.

**Usage:**

```bash
poetry run ti crosstab [OPTIONS]
```

**Note:** Currently in development (WIP).

## Visualization Commands

### `ti response`

Create a timeline heatmap of survey responses.

**Usage:**

```bash
poetry run ti response [OPTIONS]
```

**Options:**
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti response
```

### `ti hbars`

Create histograms for all variables.

**Usage:**

```bash
poetry run ti hbars [OPTIONS]
```

**Options:**
- `--save` - Save visualizations to file
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti hbars --save
```

### `ti hbar`

Create histogram for a single variable.

**Usage:**

```bash
poetry run ti hbar [OPTIONS]
```

**Note:** Currently in development (WIP).

## Text Analysis

### `ti comments`

Extract and analyze free-text responses (questions q15-q22).

**Usage:**

```bash
poetry run ti comments [OPTIONS]
```

**Options:**
- `--read_from PATH` - Custom input directory
- `--write-dir PATH` - Custom output directory
- `--load_from PATH` - Custom data directory

**Example:**

```bash
cd sandbox
poetry run ti comments
```

## Working Directory

Most commands operate from the `sandbox/` directory where `config.toml` is located:

```bash
cd sandbox
poetry run ti <command>
```

Alternatively, use `--read_from`, `--write-dir`, and `--load_from` flags to specify custom directories when running from elsewhere.
