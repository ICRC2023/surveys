# Clustering

Creating composite variables from multiple survey questions.

## Overview

Clustering combines information from multiple related questions into a single derived variable. This is useful for:

- **Simplifying analysis** - Reduce dimensionality by grouping related questions
- **Capturing multidimensional concepts** - A single concept (e.g., "career stage") may require multiple questions
- **Improving statistical power** - Combining questions increases information per variable
- **Handling missing data** - Can use partial information when some responses are missing

## Clustering in Titanite

### Defining Cluster Rules

Clusters are defined in your survey plugin:

```python
from titanite.core import ClusterRule

def get_cluster_rules(self) -> list[ClusterRule]:
    return [
        ClusterRule(
            name="gender_cluster",
            description="Combined gender identity and expression",
            source_columns=["q01", "q02"],
            aggregation_func="combine",
        ),
    ]
```

### ClusterRule Parameters

- **name** - Output column name
- **description** - Human-readable description
- **source_columns** - Input columns to combine
- **aggregation_func** - How to combine values

## Aggregation Methods

### 1. Combine (String Concatenation)

Combines values from multiple columns into a single value:

```python
ClusterRule(
    name="gender_cluster",
    source_columns=["q01", "q02"],  # gender_identity, gender_expression
    aggregation_func="combine",
)
```

**Example:**

| q01 (Identity) | q02 (Expression) | Result (gender_cluster) |
|---|---|---|
| Man | Masculine | Man - Masculine |
| Woman | Feminine | Woman - Feminine |
| Non-binary | Masculine | Non-binary - Masculine |

**Use case:** Capturing multiple dimensions of gender identity in a single variable.

### 2. Majority Vote

Selects the most common value across source columns:

```python
ClusterRule(
    name="diversity_focus",
    source_columns=["q10", "q11", "q12"],  # Multiple diversity questions
    aggregation_func="majority_vote",
)
```

**Example:**

| q10 | q11 | q12 | Result (majority_vote) |
|---|---|---|---|
| Yes | Yes | No | Yes |
| Yes | No | No | No |
| Maybe | Maybe | Maybe | Maybe |

**Use case:** Determining overall sentiment when multiple related yes/no questions exist.

**Handling ties:**
- If no clear majority, uses first column value
- If all different, uses first column value

### 3. Concatenate

Similar to combine but with different formatting:

```python
ClusterRule(
    name="career_path",
    source_columns=["q05", "q06", "q07"],
    aggregation_func="concatenate",
)
```

**Example:**

| q05 | q06 | q07 | Result |
|---|---|---|---|
| Academia | Physics | 5 years | Academia - Physics - 5 years |

**Use case:** Creating detailed categorical variable from multiple dimensions.

## ICRC2023 Example: Gender Ratio Clustering

The ICRC2023 survey combines gender identity (q01) and gender expression (q02):

```python
ClusterRule(
    name="q13q14_clustered",
    description="Gender identity and expression clustering",
    source_columns=["q13", "q14"],  # (or q01, q02)
    aggregation_func="combine",
)
```

This creates categories like:
- "Man - Masculine"
- "Woman - Feminine"
- "Non-binary - Masculine"
- "Transgender Man - Masculine"
- etc.

### Statistical Analysis

Once created, `q13q14_clustered` is treated as a categorical variable:

```bash
# Chi-square tests including clustered variable
poetry run ti chi2

# Cross-tabulations with clustered variable
poetry run ti crosstabs

# Visualizations
poetry run ti hbars
```

## Creating Effective Clusters

### 1. Choose Related Questions

Combine questions measuring the same concept:

```python
# Good - Both measure gender identity
ClusterRule(
    source_columns=["gender_identity", "gender_expression"],
    aggregation_func="combine",
)

# Bad - Unrelated questions
ClusterRule(
    source_columns=["gender", "field_of_study"],
    aggregation_func="combine",
)
```

### 2. Document the Purpose

```python
ClusterRule(
    name="career_stage",
    description="Combines years of experience and seniority level",
    source_columns=["experience_years", "job_level"],
    aggregation_func="majority_vote",
)
```

### 3. Consider Interpretability

Will the output be easy to interpret?

```python
# Clear output
ClusterRule(
    name="gender_cluster",
    source_columns=["q01", "q02"],
    aggregation_func="combine",
    # Output: "Man - Masculine", "Woman - Feminine", etc.
)

# Unclear output
ClusterRule(
    name="derived_factor",
    source_columns=["q05", "q06", "q07", "q08", "q09"],
    aggregation_func="majority_vote",
    # Output: Too many dimensions, hard to interpret
)
```

### 4. Handle Missing Values

Specify how to handle rows where source columns have missing values:

```python
ClusterRule(
    name="gender_cluster",
    source_columns=["q01", "q02"],
    aggregation_func="combine",
    handle_missing="drop",  # Drop if any value missing
    # or "keep" - include NaN in output
    # or "skip_column" - skip missing columns
)
```

## Cluster Analysis Workflow

### Step 1: Define Clusters in Plugin

```python
# plugins/your_survey/schema.py
def get_cluster_rules(self) -> list[ClusterRule]:
    return [
        ClusterRule(
            name="experience_cluster",
            source_columns=["years_exp", "current_level"],
            aggregation_func="combine",
        ),
    ]
```

### Step 2: Prepare Data

```bash
poetry run ti prepare data.csv --plugin plugins.your_survey.YourSchema
```

Check output columns:
```bash
ls prepared_data.csv
# Should include "experience_cluster" column
```

### Step 3: Analyze Clusters

```bash
poetry run ti chi2           # Test associations with clusters
poetry run ti crosstabs      # Cross-tabulations
poetry run ti hbars          # Visualizations
```

### Step 4: Interpret Results

Examine how the clustered variable associates with other variables:

```bash
poetry run ti p005 experience_cluster --save
```

This shows which variables are significantly associated with the cluster.

## Advanced Clustering

### Conditional Clustering

Apply different rules based on conditions:

```python
def get_cluster_rules(self) -> list[ClusterRule]:
    return [
        ClusterRule(
            name="gender_cluster",
            source_columns=["q01", "q02"],
            aggregation_func="combine",
            condition=lambda row: row["q01"] != "prefer_not_to_answer",
            # Only cluster if q01 was answered
        ),
    ]
```

### Weighted Clustering

Weight some columns more heavily:

```python
ClusterRule(
    name="importance_score",
    source_columns=["q10", "q11"],
    aggregation_func="weighted_combine",
    weights=[0.7, 0.3],  # q10 counts 70%, q11 counts 30%
)
```

### Hierarchical Clustering

Create clusters based on other clusters:

```python
def get_cluster_rules(self) -> list[ClusterRule]:
    return [
        # First level
        ClusterRule(
            name="gender_cluster",
            source_columns=["q01", "q02"],
            aggregation_func="combine",
        ),
        # Second level - uses first cluster
        ClusterRule(
            name="gender_by_field",
            source_columns=["gender_cluster", "q05"],
            aggregation_func="combine",
        ),
    ]
```

## Best Practices

### 1. Start Simple

Begin with straightforward combinations before complex hierarchies:

```python
# Good - Start here
ClusterRule(
    source_columns=["q01", "q02"],
    aggregation_func="combine",
)

# More complex - Add later
ClusterRule(
    source_columns=["gender_cluster", "q05", "q06"],
    aggregation_func="majority_vote",
)
```

### 2. Validate Results

After creating clusters, verify they make sense:

```bash
# View unique cluster values
poetry run ti config --choices
# Look for "your_cluster" column

# Check distribution
poetry run ti hbars --save
# Visualize cluster distribution
```

### 3. Test Independence

Ensure clustered variable isn't just repeating information:

```bash
# Chi-square test source columns with other variables
poetry run ti chi2
# Compare results before and after clustering
```

### 4. Document Decisions

Include rationale in schema:

```python
ClusterRule(
    name="gender_cluster",
    description="Combines gender identity (q01) and expression (q02) "
                "as they are interdependent aspects of gender",
    source_columns=["q01", "q02"],
    aggregation_func="combine",
)
```

## Common Issues

### Too Many Categories

Combining many questions creates too many output categories:

**Problem:**
```python
ClusterRule(
    source_columns=["q01", "q02", "q03"],  # 5 × 5 × 5 = 125 categories
    aggregation_func="combine",
)
```

**Solution:** Use `majority_vote` instead of `combine`, or limit to 2-3 source columns.

### Missing Value Explosion

Missing values in any source column affects entire cluster:

**Problem:** If q01 or q02 is missing, entire cluster is missing.

**Solution:** Handle gracefully:
```python
ClusterRule(
    source_columns=["q01", "q02"],
    aggregation_func="combine",
    handle_missing="skip_column",  # Ignore missing columns
)
```

### Imbalanced Categories

Some cluster combinations have many cases, others have few:

**Problem:** Small cell sizes reduce statistical power.

**Solution:**
- Combine rare categories
- Use cell suppression (n < 5)
- Report effect size, not just p-values

## See Also

- [Binning](binning.md) - Converting numerical data
- [Chi-Square Test](chi2_test.md) - Testing cluster associations
- [Plugin Development](../developer/plugin-development.md) - Implementing cluster rules
