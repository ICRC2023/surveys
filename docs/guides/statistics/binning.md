# Binning

Converting continuous numerical data into categorical bins.

## Overview

Binning (also called discretization) converts continuous numerical variables into categorical ranges. This is useful for:

- **Categorical analysis** - Chi-square tests require categorical data
- **Interpretability** - "Age 25-35" is easier to interpret than 28.4
- **Handling skewed distributions** - Can group sparse tails
- **Reducing noise** - Small measurement differences are grouped together
- **Simplifying visualization** - Reduces number of unique values

## Binning in Titanite

### Defining Bin Rules

Bins are defined in your survey plugin:

```python
from titanite.core import BinRule

def get_bin_rules(self) -> list[BinRule]:
    return [
        BinRule(
            source_column="age",
            target_column="age_group",
            bins=[0, 18, 30, 40, 50, 65, 100],
            labels=["<18", "18-30", "30-40", "40-50", "50-65", "65+"],
        ),
    ]
```

### BinRule Parameters

- **source_column** - Input numerical column
- **target_column** - Output categorical column name
- **bins** - Bin edges (inclusive left, exclusive right except last)
- **labels** - Category labels for each bin

## Binning Methods

### 1. Equal-Width Binning

Divide range into equal-sized intervals:

```python
BinRule(
    source_column="income",
    target_column="income_category",
    bins=[0, 25000, 50000, 75000, 100000, 500000],
    labels=["0-25k", "25-50k", "50-75k", "75-100k", "100k+"],
)
```

**Example:**

| Income | Bin Range | Category |
|---|---|---|
| 15000 | 0 - 25000 | 0-25k |
| 45000 | 25000 - 50000 | 25-50k |
| 85000 | 75000 - 100000 | 75-100k |

**Use case:** Income level, age, test scores with natural boundaries.

**Advantages:**
- Simple and intuitive
- Preserves absolute magnitude differences
- Easy to interpret bin boundaries

**Disadvantages:**
- May have empty or very small bins if data is skewed
- Extreme values can create very large bins

### 2. Equal-Frequency Binning

Divide data so each bin has approximately equal number of observations:

```python
# Create quartiles (4 bins with equal frequencies)
import pandas as pd

data_binned = pd.qcut(
    df["income"],
    q=4,  # Number of bins
    labels=["Q1 (Low)", "Q2", "Q3", "Q4 (High)"],
)
```

**Example:**

| Income | Percentile | Category |
|---|---|---|
| 15000 | 0-25% | Q1 (Low) |
| 42000 | 25-50% | Q2 |
| 68000 | 50-75% | Q3 |
| 95000 | 75-100% | Q4 (High) |

**Use case:** Dividing participants into comparable groups (quartiles, deciles).

**Advantages:**
- Each bin has equal sample size
- Better statistical power per bin
- Works well with skewed distributions

**Disadvantages:**
- Bin edges appear arbitrary (not natural boundaries)
- Same range in different bins with different densities

### 3. Natural Breaks Binning

Group using natural boundaries in the data:

```python
# Find natural clusters in data
# Example: Age groups based on life stages
bins = [0, 25, 35, 50, 65, 100]
labels = ["Student", "Early Career", "Mid Career", "Senior", "Retirement"]
```

**Use case:** Demographic categories with natural definitions.

## ICRC2023 Example

The ICRC2023 survey uses equal-width binning for age grouping:

```python
BinRule(
    source_column="q10",  # Numerical age
    target_column="q10_binned",
    bins=[0, 25, 35, 50, 65, 100],
    labels=["<25", "25-35", "35-50", "50-65", "65+"],
)
```

### Using Binned Variables

Once created, `q10_binned` is treated as categorical:

```bash
# Chi-square tests with binned variables
poetry run ti chi2

# Visualize distribution
poetry run ti hbars
```

## Binning Workflow

### Step 1: Explore Data Distribution

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("prepared_data.csv")

# Examine distribution
print(df["age"].describe())
# count    295.000000
# mean      42.300000
# std       13.200000
# min       18.000000
# 25%       32.000000
# 50%       42.000000
# 75%       52.000000
# max       78.000000

# Visualize
plt.hist(df["age"], bins=20)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()
```

### Step 2: Choose Binning Strategy

**Equal-width (natural age boundaries):**
```python
bins = [0, 25, 35, 50, 65, 100]
labels = ["<25", "25-35", "35-50", "50-65", "65+"]
```

**Equal-frequency (quartiles):**
```python
percentiles = df["age"].quantile([0, 0.25, 0.5, 0.75, 1.0])
# Returns: [18, 32, 42, 52, 78]
bins = percentiles.tolist()
labels = ["Q1", "Q2", "Q3", "Q4"]
```

### Step 3: Define Bin Rule

```python
def get_bin_rules(self) -> list[BinRule]:
    return [
        BinRule(
            source_column="q10",
            target_column="q10_age_group",
            bins=[0, 25, 35, 50, 65, 100],
            labels=["<25", "25-35", "35-50", "50-65", "65+"],
        ),
    ]
```

### Step 4: Process and Validate

```bash
# Process data
poetry run ti prepare data.csv

# Verify binning
poetry run ti config --choices
# Check that q10_age_group has expected categories

# View distribution
poetry run ti hbars
# Visualize binned variable
```

## Best Practices

### 1. Choose Appropriate Bin Count

- **Too few bins** - Lose information, oversimplify
- **Too many bins** - Create sparse cells, hard to interpret

**Rule of thumb:**
- Small dataset (n < 100): 3-4 bins
- Medium dataset (n = 100-1000): 5-8 bins
- Large dataset (n > 1000): 8-15 bins

### 2. Use Meaningful Boundaries

Choose bin edges that are interpretable:

```python
# Good - Natural life stages
bins = [0, 25, 35, 50, 65, 100]

# Bad - Arbitrary decimal values
bins = [0, 23.4, 41.8, 59.2, 100]
```

### 3. Check for Empty Bins

Verify each bin has at least a few observations:

```python
binned_data = pd.cut(df["age"], bins=[0, 25, 35, 50, 65, 100])
print(binned_data.value_counts())
# Should see counts for all categories
```

If a bin is empty, consider merging adjacent bins.

### 4. Document Rationale

Explain why you chose specific bin boundaries:

```python
BinRule(
    source_column="experience_years",
    target_column="career_stage",
    bins=[0, 2, 5, 10, 50],
    labels=["Entry (0-2yr)", "Junior (2-5yr)", "Senior (5-10yr)", "Principal (10+yr)"],
    # Boundaries chosen based on typical career progression milestones
)
```

### 5. Handle Edge Cases

What happens with extreme values?

```python
# Include wide range for last bin
bins = [0, 25, 35, 50, 65, 1000]  # Large upper bound
labels = ["<25", "25-35", "35-50", "50-65", "65+"]

# Or use inf
import numpy as np
bins = [0, 25, 35, 50, 65, np.inf]
```

### 6. Validate Statistical Properties

After binning, check that analysis is meaningful:

```bash
# View contingency table
poetry run ti crosstabs

# Check cell sizes are adequate (n ≥ 5)
# If small cells exist, consider merging bins
```

## Handling Special Cases

### Skewed Distributions

For data with most values concentrated in one region:

```python
# Income data: Most people earn <$100k, few earn >$500k
bins = [0, 25000, 50000, 75000, 100000, 150000, 500000]
labels = ["<25k", "25-50k", "50-75k", "75-100k", "100-150k", "150k+"]

# Or use equal-frequency binning
import pandas as pd
df["income_quartile"] = pd.qcut(df["income"], q=4)
```

### Highly Discrete Data

For variables with limited precision (e.g., Likert scale 1-5):

```python
# Don't bin - already categorical!
# If you must bin, group adjacent categories:
bins = [0.5, 2.5, 3.5, 5.5]
labels = ["Low (1-2)", "Medium (3)", "High (4-5)"]
```

### Missing Values

Handle missing values appropriately:

```python
BinRule(
    source_column="score",
    target_column="score_category",
    bins=[0, 50, 75, 100],
    labels=["Low", "Medium", "High"],
    # Missing values in source_column become NaN in target_column
)
```

## Common Issues

### Sparsity After Binning

Too many bins creates cells with very few observations:

**Problem:**
```python
# Creates 10 categories, some with <5 observations
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
```

**Solution:**
- Reduce number of bins
- Use equal-frequency binning instead
- Merge small cells before analysis
- Report cell sizes with results

### Information Loss

Binning discards information about exact values:

**Problem:**
```python
# Can no longer see if age 34 vs 35
bins = [0, 25, 35, 50, 65, 100]
# Both map to category "25-35"
```

**Solution:**
- Keep original numerical variable for sensitivity analysis
- Use appropriate bin width to minimize loss
- Consider whether hypothesis requires exact values

### Arbitrary Boundaries

Different bin choices can lead to different conclusions:

**Example:** Testing association between age and field of study

**Option 1 - Wide bins:**
```python
bins = [0, 30, 60, 100]
# May find no association
```

**Option 2 - Narrow bins:**
```python
bins = [0, 25, 35, 45, 55, 65, 100]
# May find association
```

**Solution:**
- Choose bins before seeing results (avoid HARKing)
- Justify bin boundaries theoretically
- Test sensitivity to bin choice
- Document decisions in analysis

## Mathematical Details

### Binning Formula

For equal-width binning:

$$\text{bin} = \left\lfloor \frac{x - x_{min}}{(x_{max} - x_{min}) / n_{bins}} \right\rfloor$$

Where:
- x = value to bin
- x_min, x_max = range of data
- n_bins = number of bins

### Chi-Square Power After Binning

Binning reduces statistical power compared to continuous analysis, but enables categorical tests:

- Chi-square power depends on bin count and distribution
- More bins = more power, but sparser cells
- Fewer bins = less power, but stable cells

Use 5-8 bins to balance these considerations.

## See Also

- [Chi-Square Test](chi2_test.md) - Using binned variables for association tests
- [Clustering](clustering.md) - Creating composite variables
- [Plugin Development](../developer/plugin-development.md) - Implementing bin rules
