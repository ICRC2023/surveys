# Configuration

Customize survey settings and data processing through configuration files.

## Configuration File

The main configuration file is located at:

```
sandbox/config.toml
```

This file defines:
- Survey question mappings
- Categorical variables and their valid choices
- Numerical variables for statistical analysis
- Data processing rules

## Configuration Structure

### Questions Section

Defines the mapping between question IDs and descriptions:

```toml
[questions]
q01 = "Gender identity"
q02 = "Gender expression"
q03 = "Geographic region"
# ... more questions
```

### Categorical Headers

Lists variables that should be treated as categorical (discrete) data:

```toml
[categorical_headers]
default = ["q01", "q02", "q03_regional", "q03_subregional"]
```

These variables are used for chi-square tests and categorical analysis.

### Numerical Headers

Lists variables that should be treated as numerical (continuous) data:

```toml
[numerical_headers]
default = ["q10", "q13", "sentiment_score"]
```

### Data Rules

Define transformations applied during data preparation:

```toml
[data_rules]
# Define categorical values for specific questions
# Define clustering rules for derived columns
# Define binning rules for numerical data
```

## Using Custom Configuration

### Load Custom Config

To use a custom configuration file:

```bash
cd custom_directory
poetry run ti config --load_from /path/to/config
```

### Output Configuration

Specify output directory for processed data:

```bash
poetry run ti prepare data.csv --write-dir /path/to/output
```

### Input Directory

Specify custom input directory:

```bash
poetry run ti prepare data.csv --read_from /path/to/input
```

## Configuration with Plugins

When using a custom survey schema with the `--plugin` option, you can still override configuration:

```bash
poetry run ti prepare data.csv \
  --plugin plugins.custom_survey.CustomSchema \
  --load_from /path/to/config
```

## Survey Schema Configuration

The survey schema (defined in plugins) determines:

1. **Value Replacements** - Standardize response values
2. **Geographic Splitting** - Split regional data into components
3. **Clustering Rules** - Create derived composite columns
4. **Binning Rules** - Convert numerical data to categories

See [Plugin Development](../developer/plugin-development.md) for details on schema customization.

## Best Practices

1. **Version Control** - Keep configuration files in Git
2. **Separate Configs** - Use different configs for different surveys
3. **Document Changes** - Comment configuration changes in commits
4. **Validate Data** - Run `ti config` to verify configuration is loaded correctly
5. **Test First** - Test configuration with sample data before processing large datasets

## Troubleshooting

### Configuration Not Found

Ensure the `config.toml` file exists in your current directory or specify the path:

```bash
poetry run ti config --load_from /path/to/config
```

### Invalid Categories

Check that all categorical variables are properly defined in `config.toml`:

```bash
poetry run ti config --choices
```

### Missing Questions

Verify that all question IDs in data match those defined in configuration:

```bash
poetry run ti config --questions
```
