---
name: fold-change-calculation
description: Use when after completing statistical tests (t-test, Mann–Whitney U, or ANOVA) on matched lipid abundances grouped by experimental condition or sample category, and before compiling final results tables.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0621
  tools:
  - Python (pandas, NumPy, SciPy)
  - R (base stats, tidyverse, or similar)
  - pandas
  - NumPy
  - SciPy
  - R base stats / tidyverse
  - edgeR.R
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
---

# fold-change-calculation

## Summary

Calculate fold-change values comparing lipid abundances between experimental groups to quantify the magnitude of differential expression. Fold-change is a normalized effect-size metric essential for ranking and interpreting the biological significance of lipid abundance differences beyond statistical p-values.

## When to use

After completing statistical tests (t-test, Mann–Whitney U, or ANOVA) on matched lipid abundances grouped by experimental condition or sample category, and before compiling final results tables. Fold-change is required when the analysis goal includes identifying which lipids show the largest magnitude of change between groups, or when ranking lipids by biological effect size for validation or functional interpretation.

## When NOT to use

- Input data has not yet been grouped by experimental condition or validated for matching — fold-change requires prior grouping and alignment steps.
- Sample sizes per group are very small (n < 2 per group) — fold-change ratios become unstable and are uninterpretable without adequate replication.
- The analysis goal is hypothesis-free exploratory clustering or dimensionality reduction rather than ranking lipids by differential abundance — fold-change is not necessary for those workflows.

## Inputs

- Matched lipid abundance table (output from matching step, one row per lipid, one column per sample)
- Experimental group or sample category assignments (metadata linking samples to conditions)
- Group-level descriptive statistics (mean and standard deviation per lipid per group, pre-computed)

## Outputs

- Fold-change values table (one row per lipid, columns for lipid identifier, log₂ fold-change, direction of change)
- Compiled results table (lipid identifier, group means, test statistics, adjusted p-values, fold-change values, effect sizes)

## How to apply

For each lipid, compute fold-change as the ratio of mean abundance in one experimental group to mean abundance in a comparison group (e.g., treatment / control). Log-transform the fold-change values (typically log₂ scale) to render ratios symmetric around zero and facilitate visualization and interpretation. Pair each fold-change value with its corresponding adjusted p-value and test statistic in the results table so that both statistical significance and effect magnitude can be evaluated together. Use fold-change thresholds (e.g., |log₂ FC| > 1) in downstream filtering only after confirming statistical significance (adjusted p-value < 0.05) to avoid inflated false-positive rates.

## Related tools

- **pandas** (Data frame manipulation and grouping; compute mean abundances per group and calculate fold-change ratios)
- **NumPy** (Vectorized arithmetic for log-transforming fold-change values and element-wise group ratio calculations)
- **SciPy** (Complementary statistical functions (already used for t-tests and Mann–Whitney U); supports effect-size computations)
- **R base stats / tidyverse** (Alternative environment for group-based fold-change calculation and results table assembly)
- **edgeR.R** (R script provided in CLAW workflow for downstream differential abundance analysis and visualization of fold-change values) — github.com/chopralab/CLAW

## Examples

```
import pandas as pd; import numpy as np; grouped = df.groupby('condition')['lipid_abundance'].mean(); log2_fc = np.log2(grouped['treatment'] / grouped['control']); results = pd.DataFrame({'lipid_id': lipid_ids, 'log2_fold_change': log2_fc, 'adj_pvalue': p_values})
```

## Evaluation signals

- Fold-change values are symmetric around zero (on log scale) and reflect the directionality of change: positive log₂ FC indicates group A > group B, negative indicates group A < group B.
- Fold-change magnitudes correlate with statistical test results: lipids with large |log₂ FC| and small adjusted p-values (e.g., < 0.05) are prioritized; lipids with small |log₂ FC| may have high p-values despite statistical significance.
- No division-by-zero or NaN values in fold-change columns; all group means used in ratio calculations are positive and non-zero.
- Results table rows are consistent (one row per unique lipid identifier) and fold-change column length matches number of lipids.
- Fold-change values are properly paired with their corresponding p-values and test statistics in the same row, enabling joint filtering on statistical and effect-size thresholds.

## Limitations

- Fold-change is sensitive to small denominator values (low control/baseline abundance); pseudocount addition or prior regularization may be necessary for lipids with near-zero abundance in one group.
- Fold-change alone does not account for variance or measurement noise; a lipid with large fold-change but high within-group variability may not be reproducible. Always pair fold-change with adjusted p-values.
- Log₂ transformation of fold-change assumes symmetry; extreme fold-changes (e.g., >100-fold) may compress visual range in plots and warrant additional scaling or thresholding strategies.

## Evidence

- [other] Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change, Cohen's d).: "Perform statistical tests (e.g., t-test, Mann–Whitney U, or ANOVA as appropriate to study design) to compare lipid abundances between groups, computing p-values and effect sizes (e.g., fold-change,"
- [other] Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values.: "Compile results into a structured table with one row per lipid, including lipid identifier, group means, test statistics, adjusted p-values, and fold-change values."
- [other] Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group.: "Calculate descriptive statistics (mean, standard deviation, median) for each lipid within each group."
- [readme] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
