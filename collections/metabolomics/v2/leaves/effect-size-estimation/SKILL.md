---
name: effect-size-estimation
description: Use when after performing statistical tests (t-test, Mann–Whitney U,
  ANOVA) on matched lipid abundance data grouped by experimental condition, to report
  not only whether differences are statistically significant but also the magnitude
  and direction of change.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - SciPy (scipy.stats)
  - pandas
  - NumPy
  - R base stats / tidyverse
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- statistical analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  dedup_kept_from: coll_claw_mrm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05039
  all_source_dois:
  - 10.1021/acs.analchem.4c05039
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# effect-size-estimation

## Summary

Quantify the magnitude of differences in lipid abundances between experimental groups by computing effect sizes (fold-change, Cohen's d) alongside statistical tests. Effect sizes complement p-values to assess biological or practical significance independent of sample size.

## When to use

After performing statistical tests (t-test, Mann–Whitney U, ANOVA) on matched lipid abundance data grouped by experimental condition, to report not only whether differences are statistically significant but also the magnitude and direction of change. Use this when you need to distinguish large but noisy differences from small but consistent ones, or when communicating results to stakeholders who need interpretable magnitude metrics.

## When NOT to use

- Input lipid abundance data has not yet been matched or aligned across samples — effect size requires paired or aligned measurements.
- No clear grouping or experimental design exists (e.g., continuous phenotype, no categorical contrasts to compare).
- Sample sizes are extremely small (n < 3 per group) where effect size estimates become unreliable.

## Inputs

- matched lipid abundance table (data frame with lipid identifiers, sample identifiers, and normalized abundance values)
- grouping metadata (experimental condition or sample category assignments)
- group-wise mean abundances and standard deviations (computed in prior descriptive statistics step)

## Outputs

- structured results table with one row per lipid, including lipid identifier, group means, fold-change values, Cohen's d or equivalent effect size, test statistics, and adjusted p-values
- CSV file with compiled effect size and statistical results ready for downstream filtering and visualization

## How to apply

Once you have computed p-values from comparative statistical tests between groups, calculate fold-change as the ratio of mean lipid abundance in one group relative to another (e.g., treated/control). Simultaneously compute Cohen's d or similar standardized effect size to account for pooled variance and sample size. Include both metrics in the results table alongside group means and test statistics. Fold-change is intuitive and scale-dependent; Cohen's d is unitless and comparable across lipids. Report effect sizes in the final CSV export alongside adjusted p-values to enable filtering by both statistical and biological significance thresholds.

## Related tools

- **SciPy (scipy.stats)** (compute effect sizes (Cohen's d) and standardized test statistics from group means and variances)
- **pandas** (organize matched lipid abundances into grouped data frames and compute group means for fold-change calculation)
- **NumPy** (vectorized arithmetic for fold-change ratios and effect size aggregation across lipid features)
- **R base stats / tidyverse** (alternative environment for effect size calculation and results compilation in tabular format)

## Examples

```
import pandas as pd; import numpy as np; from scipy.stats import ttest_ind; groups = df.groupby('condition')['abundance']; fc = groups.mean().iloc[1] / groups.mean().iloc[0]; cohens_d = (groups.mean().iloc[1] - groups.mean().iloc[0]) / np.sqrt((groups.std()**2).mean()); results = pd.DataFrame({'lipid_id': lipid_ids, 'fold_change': fc, 'cohens_d': cohens_d}); results.to_csv('effect_sizes.csv', index=False)
```

## Evaluation signals

- Fold-change values are numeric and span a reasonable range (typically 0.5 to 2.0 or ±1 on log scale for lipids with subtle changes; >2 or <0.5 for marked shifts); no NaN or infinite values.
- Cohen's d or equivalent effect size is unitless and typically in range [−3, +3] for biological comparisons; sign aligns with direction of fold-change.
- Effect size table has one row per unique lipid identifier; no duplicates or missing values in key columns (lipid ID, fold-change, effect size, p-value).
- Lipids with large effect sizes (|Cohen's d| > 0.8) also show low adjusted p-values (q < 0.05), and vice versa; large effect sizes with high p-values should be flagged as potential candidates for validation.
- CSV export is properly delimited, with headers matching schema (lipid identifier, group means, fold-change, Cohen's d, test statistic, adjusted p-value) and consistent numeric formatting.

## Limitations

- Fold-change is asymmetric (2-fold up vs. 0.5-fold down); log-transformation or symmetric metrics (e.g., log2 fold-change) may be preferable for visualization.
- Cohen's d assumes approximately normal distribution within groups; for highly skewed lipid abundances, non-parametric effect size alternatives (rank-biserial correlation) should be considered.
- Effect size magnitude thresholds (e.g., 'small', 'medium', 'large') are context-dependent and discipline-specific; no universal cutoff exists for lipidomics.
- Multiple lipids are tested; even with FDR correction on p-values, effect size distributions may be inflated by multiple comparison bias.

## Evidence

- [other] Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change, Cohen's d).: "Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change,"
- [other] Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values.: "Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values."
- [readme] The workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns.: "The workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns."
