---
name: statistical-score-distribution-analysis
description: Use when when you have run the same mass spectrum through molecular formula assignment under different parameter settings (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - matplotlib
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
---

# statistical-score-distribution-analysis

## Summary

Extract and compare statistical properties (mean, median, standard deviation, min, max) of molecular formula assignment scores across different parameterization modes to assess how algorithmic choices affect annotation behavior and confidence distributions.

## When to use

When you have run the same mass spectrum through molecular formula assignment under different parameter settings (e.g., first_hit=True vs first_hit=False, or different database search modes) and need to quantify whether the parameter choice systematically shifts the assignment score landscape rather than just count totals.

## When NOT to use

- Input is a single assignment mode with no comparative parameterization — use descriptive statistics instead.
- Scores are missing or non-numeric in one or more modes — preprocessing/validation required first.
- Assignment count alone is the only quantity of interest; this skill targets distribution shape, not cardinality.

## Inputs

- Molecular formula assignment results (extracted from SearchMolecularFormulas output) under two or more parameter configurations
- Score vector(s) associated with each assignment mode

## Outputs

- Comparison summary table (CSV format) with mean, median, std, min, max for each mode
- Statistical test results (p-values, KS statistic, or similar)
- Visualization(s) (histogram, box-plot, or violin-plot overlays showing score distributions by mode)

## How to apply

Load assignment results from each parameterization mode as separate datasets. For each mode, extract the score field from all molecular formula assignments. Compute the full suite of descriptive statistics (mean, median, std, min, max) on the score distribution for each mode. Tabulate these statistics side-by-side in a comparison table, then visualize using histogram or box-plot overlays to reveal distributional shifts, spread changes, and outlier behavior. Use statistical tests (e.g., Kolmogorov–Smirnov test) to assess whether distributions differ significantly, and report effect sizes. Save the comparison table as CSV for downstream reporting.

## Related tools

- **CoreMS** (Execute SearchMolecularFormulas with parameterized first_hit setting and extract score arrays from results) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Load, aggregate, and tabulate score statistics (mean, median, std, min, max) into comparison DataFrames)
- **numpy** (Compute statistical measures (mean, median, std, percentiles) on score vectors)
- **matplotlib** (Generate histogram and box-plot visualizations to compare score distributions across modes)

## Examples

```
import pandas as pd; import numpy as np; results_first_hit = [...]; results_all_hits = [...]; stats = pd.DataFrame({'Mode': ['first_hit=True', 'first_hit=False'], 'Mean': [np.mean(results_first_hit['scores']), np.mean(results_all_hits['scores'])], 'Median': [np.median(results_first_hit['scores']), np.median(results_all_hits['scores'])], 'Std': [np.std(results_first_hit['scores']), np.std(results_all_hits['scores'])], 'Min': [np.min(results_first_hit['scores']), np.min(results_all_hits['scores'])], 'Max': [np.max(results_first_hit['scores']), np.max(results_all_hits['scores'])]}); stats.to_csv('score_comparison.csv', index=False)
```

## Evaluation signals

- Comparison table contains exactly one row per parameterization mode with columns for mean, median, std, min, max populated with numeric values.
- Score vectors are non-empty and numeric for all modes; no NaN or missing values in computed statistics.
- Visualizations show clear separation or overlap between score distributions, consistent with reported mean/median differences.
- Statistical test p-value is reported; if p < 0.05, distributions are significantly different and parameterization choice matters.
- CSV file is well-formed (UTF-8, proper delimiters) and loadable into downstream analysis tools.

## Limitations

- Comparison is only meaningful if both assignment modes process the same input spectrum and use compatible scoring schemes; mixing incompatible scores will yield misleading comparisons.
- Small sample sizes (few assignments in one mode) reduce statistical power; consider minimum threshold (e.g., n ≥ 10 assignments per mode) before interpreting results.
- Score distributions may be skewed or multimodal, in which case median and quartiles are more robust than mean; visualize distributions before drawing conclusions.

## Evidence

- [other] Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode.: "Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode."
- [other] SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes.: "SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes."
- [other] Generate a comparison summary table contrasting the two assignment modes and save as CSV.: "Generate a comparison summary table contrasting the two assignment modes and save as CSV."
