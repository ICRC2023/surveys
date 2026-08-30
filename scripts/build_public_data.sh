#!/usr/bin/env bash
# Regenerate the committed data/public/ extract from the raw export.
#
# The raw Google Forms CSV export lives only in data/downloaded/ (git-ignored).
# Run this after refreshing it or changing the anonymization rules. Output:
#   data/public/public_data.csv           - k-anonymized individual-level extract
#   data/public/aggregates/univariate/    - one suppressed frequency table per column
#   data/public/aggregates/bivariate/     - suppressed cross-tabs for the pairs below
#   data/public/chi2/                     - chi-square test statistics (no counts)
#
# See PLAN.md Phase 5.
set -euo pipefail

RAW="${1:-../data/downloaded/20230726_icrc2023_diversity_pre_survey.csv}"
PLUGIN="plugins.icrc2023.ICRC2023Schema"

cd "$(dirname "$0")/../sandbox"

echo ">> ti prepare (raw -> data/private/, individual-level, not committed)"
uv run ti prepare "$RAW" --plugin "$PLUGIN"

echo ">> ti anonymize (-> data/public/public_data.csv)"
uv run ti anonymize --plugin "$PLUGIN"

echo ">> ti aggregate (-> data/public/aggregates/)"
# Every per-question page shows a "by gender identity" cross-tab, so pair
# each response column with q02. Plus a few age (q01) breakdowns.
uv run ti aggregate --plugin "$PLUGIN" \
  --pair q01,q02 --pair q01,q05 --pair q01,q06 \
  --pair q05,q02 --pair q06,q02 --pair q07,q02 --pair q08,q02 \
  --pair q09,q02 --pair q11,q02 --pair q19,q02 \
  --pair q03_regional,q02 --pair q03_subregional,q02 \
  --pair q04_regional,q02 --pair q04_subregional,q02 \
  --pair q12_genderbalance,q02 --pair q12_diversity,q02 \
  --pair q12_equity,q02 --pair q12_inclusion,q02 \
  --pair q10_binned,q02 --pair q13_binned,q02 --pair q14,q02 \
  --pair q17_genderbalance,q02 --pair q17_diversity,q02 \
  --pair q17_equity,q02 --pair q17_inclusion,q02

echo ">> ti chi2 (-> data/public/chi2/, test statistics only)"
mkdir -p ../data/public/chi2
uv run ti chi2 \
  --read-from ../data/private/prepared_data.csv \
  --write-dir ../data/public/chi2/
rm -f ../data/public/chi2/*.json

echo ">> done. Review data/public/ before committing."
