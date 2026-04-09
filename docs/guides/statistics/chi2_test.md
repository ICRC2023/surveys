# Chi-Square Test

Understanding chi-square tests for categorical association analysis.

## Overview

The chi-square test is a statistical test used to determine whether there is a significant association between two categorical variables. In titanite, chi-square tests are used to identify relationships in survey data.

**When to use:**
- Analyzing associations between categorical variables (e.g., gender vs. department)
- Testing independence of two categorical variables
- Identifying which variable pairs have statistically significant relationships

## The Chi-Square Statistic

The chi-square statistic (χ²) measures how much the observed frequencies differ from what we would expect if there were no association between variables:

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

Where:
- **O** = Observed frequency (actual count in data)
- **E** = Expected frequency (count if variables were independent)

## Interpreting Results

### P-value

The p-value indicates the probability that the observed association occurred by chance:

- **p < 0.05** - Statistically significant association (reject null hypothesis of independence)
- **p ≥ 0.05** - No significant association (cannot reject null hypothesis)

**Interpretation:**
- Small p-value (e.g., p = 0.001): Very unlikely to occur by chance → Strong evidence of association
- Large p-value (e.g., p = 0.5): Likely to occur by chance → No evidence of association

### Degrees of Freedom

Degrees of freedom (df) indicate the flexibility in the data:

$$df = (rows - 1) \times (columns - 1)$$

More rows/columns = more degrees of freedom = larger χ² value needed for significance.

### Effect Size

The chi-square statistic alone doesn't indicate strength of association. Use Cramér's V for effect size:

$$V = \sqrt{\frac{\chi^2}{n \times (k - 1)}}$$

Where:
- **χ²** = Chi-square statistic
- **n** = Sample size
- **k** = Minimum of (rows, columns)

**Interpretation:**
- **V < 0.1** - Negligible association
- **0.1 ≤ V < 0.3** - Weak association
- **0.3 ≤ V < 0.5** - Moderate association
- **V ≥ 0.5** - Strong association

## Using in Titanite

### Running Chi-Square Tests

Test all variable pairs:

```bash
cd sandbox
poetry run ti chi2
```

This generates a matrix showing:
- Chi-square statistic for each pair
- P-value
- Degrees of freedom
- Effect size (Cramér's V)

### Extracting Significant Results

Extract only pairs with p < 0.05:

```bash
poetry run ti p005 q13 --save
```

This saves significant correlations for a specific column (e.g., q13).

### Interpreting Output

Example output:

```
Variable Pair: q01 vs q02
χ² = 15.42
p = 0.0008
df = 2
V = 0.245 (weak association)
```

**Interpretation:**
- Strong statistical evidence (p = 0.0008) of association between q01 and q02
- Weak practical effect (V = 0.245)
- Knowing q01 slightly improves prediction of q02, but not dramatically

## Example Analysis

### Survey Scenario

**Question:** Is there an association between gender (q01) and field of study (q05)?

**Data:**

|        | Physics | Biology | Chemistry |
|--------|---------|---------|-----------|
| Male   | 45      | 20      | 25        |
| Female | 30      | 35      | 40        |
| Other  | 5       | 10      | 8         |

### Calculate Expected Frequencies

Under independence (no association):

$$E_{ij} = \frac{(\text{row total}) \times (\text{column total})}{\text{grand total}}$$

Total respondents = 218

Expected males in Physics:
$$E = \frac{90 \times 80}{218} = 33.0$$

### Chi-Square Calculation

$$\chi^2 = \frac{(45-33)^2}{33} + \frac{(20-27)^2}{27} + ... = 8.47$$

With df = 4 (3-1) × (3-1), this gives p ≈ 0.076

**Conclusion:** No statistically significant association at p < 0.05 level.

## Assumptions and Limitations

### Required Assumptions

1. **Independence of observations** - Each respondent counted once
2. **Categorical variables** - Data must be categorical, not continuous
3. **Sufficient sample size** - Generally need n ≥ 20
4. **Expected cell frequencies** - Typically need E ≥ 5 for most cells

If assumptions violated:
- Use Fisher's exact test for small samples
- Consider exact chi-square test for sparse tables
- Combine categories if E < 5 in many cells

### Limitations

- **Chi-square tests for association, not causation** - Significant association doesn't mean one variable causes the other
- **Sensitive to sample size** - Large datasets can show "significant" associations with small practical effect
- **Multiple comparisons problem** - Testing many pairs increases chance of false positives

## Multiple Comparisons Correction

When running many chi-square tests, use Bonferroni correction:

**Adjusted p-value threshold:**
$$p_{adjusted} = \frac{p_{original}}{n_{tests}}$$

Example: Testing 50 variable pairs
$$p_{adjusted} = \frac{0.05}{50} = 0.001$$

Only accept associations with p < 0.001 to maintain overall significance level of 0.05.

Titanite implements this correction in `chi2` and `p005` commands.

## Common Pitfalls

### 1. Confusing Association with Causation

```
Finding: High p < 0.05 correlation between coffee consumption and heart disease

Possible explanations:
- Coffee causes heart disease (unlikely)
- Heart disease causes coffee avoidance (reverse causation)
- Age confounds both (older people drink more coffee AND have more heart disease)
```

### 2. Ignoring Effect Size

```
Chi-square test: p = 0.02, V = 0.08 (negligible effect)

Interpretation:
- Statistical significance: YES (unlikely due to chance)
- Practical significance: NO (effect too weak to matter)
```

### 3. Multiple Comparisons Without Correction

Testing 100 variable pairs:
- Expected false positives: 100 × 0.05 = 5 spurious significant results
- Always apply multiple comparisons correction

### 4. Violating Assumptions

Small expected cell frequencies:
- Combining rare categories
- Using Fisher's exact test instead
- Reporting warnings appropriately

## Further Reading

- [Chi-square test guide](https://en.wikipedia.org/wiki/Chi-squared_test)
- [Effect size in chi-square tests](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)
- [Multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem)

## See Also

- [Clustering](clustering.md) - Creating composite variables
- [Binning](binning.md) - Converting continuous data for chi-square tests
