---
name: ground-truth-ordinal-validation
description: Use when after running retention-order prediction on a test or evaluation dataset, when you have both predicted retention orderings (from RankSVM, SVR, or similar ordinal regressors) and experimentally validated ground-truth retention orders from the same chromatographic system(s).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3407
  tools:
  - evaluation_scenarios_main.py
  - RankSVM
  - SVR (Support Vector Regression)
  - scipy, numpy, pandas, scikit-learn
  - ECCB2018.Rmd
derived_from:
- doi: 10.1093/bioinformatics/bty590
  title: LC retention order prediction
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lc_retention_order_prediction_cq
    doi: 10.1093/bioinformatics/bty590
    title: LC retention order prediction
  dedup_kept_from: coll_lc_retention_order_prediction_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty590
  all_source_dois:
  - 10.1093/bioinformatics/bty590
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ground-truth-ordinal-validation

## Summary

Validate retention-order predictions against experimental ground-truth orderings using ranking-specific metrics (Spearman correlation, ranking accuracy). This skill ensures that predicted liquid-chromatography retention orders for metabolites match the observed experimental rankings from reference chromatographic systems.

## When to use

After running retention-order prediction on a test or evaluation dataset, when you have both predicted retention orderings (from RankSVM, SVR, or similar ordinal regressors) and experimentally validated ground-truth retention orders from the same chromatographic system(s). Use this skill to quantify prediction fidelity and system transfer performance.

## When NOT to use

- Ground-truth retention orders are unavailable or have not been experimentally validated from the target chromatographic system.
- Predicted outputs are not yet in rank or preference format (e.g., raw continuous regression scores without ordinal conversion).
- The evaluation is of absolute retention time prediction rather than ordinal retention-order prediction; use continuous regression metrics (RMSE, MAE) instead.

## Inputs

- predicted retention orders (ranked list or pairwise preference scores from RankSVM or SVR model)
- ground-truth experimental retention orders (reference chromatographic system rankings for metabolites)
- configuration JSON specifying molecular features, kernels, and evaluation scenarios
- evaluation scenario parameters (single-system baseline, all-on-one transfer, training data percentages)

## Outputs

- ranking evaluation metrics (Spearman correlation coefficient, ranking accuracy per system/scenario)
- results summary table (predicted vs. ground-truth retention orders with performance scores)
- HTML or static results report (visualized performance across systems and feature representations)
- structured results directory (organized by estimator, scenario, system set, and molecular features)

## How to apply

Load the predicted retention orders and ground-truth orderings (both as ranked lists or pairwise preference relationships) into the repository's evaluation scripts. Compute ranking-specific metrics: Spearman rank correlation coefficient (to assess monotonic agreement between predicted and observed rank positions), and ranking accuracy (fraction of correctly ordered pairs, or percentage of metabolites within acceptable rank tolerance). Compare results across scenarios (single-system baseline, cross-system transfer, varying training-data percentages) to identify performance gaps and transferability bottlenecks. Generate a results summary table or HTML report (following the pattern in results/ECCB2018.html) that visualizes predicted vs. ground-truth retention orders side-by-side, with performance scores stratified by system and feature representation.

## Related tools

- **evaluation_scenarios_main.py** (orchestrates retention-order prediction experiments and computes ranking metrics (Spearman correlation, ranking accuracy) against ground-truth orderings for multiple scenarios and system configurations) — github.com/aalto-ics-kepaco/retention_order_prediction
- **RankSVM** (ordinal regression estimator that learns pairwise preference relationships between metabolite retention orders; predictions are validated by this skill) — github.com/aalto-ics-kepaco/retention_order_prediction
- **SVR (Support Vector Regression)** (continuous regression estimator for retention-order prediction; outputs are converted to ordinal rankings for validation) — github.com/aalto-ics-kepaco/retention_order_prediction
- **scipy, numpy, pandas, scikit-learn** (Python libraries for ranking metric computation, data manipulation, and statistical evaluation)
- **ECCB2018.Rmd** (R Markdown script that reproduces results tables and generates HTML/visualization reports comparing predicted and ground-truth retention orders) — github.com/aalto-ics-kepaco/retention_order_prediction

## Examples

```
python src/evaluation_scenarios_main.py ranksvm baseline_single 10 -1 results/raw/PredRet/v2/config.json 2 False
```

## Evaluation signals

- Spearman rank correlation coefficient between predicted and ground-truth orderings is ≥ 0.7 (strong monotonic agreement) for within-system baseline; correlation degrades predictably for out-of-system transfer scenarios.
- Ranking accuracy (fraction of correctly ordered metabolite pairs or percentage within acceptable rank tolerance) matches or exceeds the baseline and cross-system results reported in Table 3 and Table 4 of the paper for equivalent feature/system configurations.
- Results tables and performance scores are reproducible when the same configuration.json and scenario parameters are re-executed (determinism check).
- Performance degradation follows expected patterns: single-system baseline > all-on-one transfer with target system in training (LTSO=True) > all-on-one transfer without target system (LTSO=False), as reported in the paper.
- Results are correctly organized into the expected directory structure (results/PredRet/v2/final/ranksvm_slacktype=.../baseline_single or all_on_one, etc.) and match the schema shown in the Usage section.

## Limitations

- Evaluation requires experimentally validated ground-truth retention orders; predictions cannot be validated against missing or incomplete orderings.
- Ranking metrics (Spearman correlation, ranking accuracy) assume ordinal relationships but do not capture absolute retention-time errors; use continuous regression metrics if absolute time prediction is the primary goal.
- Cross-system transfer performance depends on training-system diversity and overlap; transfer to novel chromatographic systems not represented in the training set may yield degraded ranking accuracy.
- The evaluation does not account for ties or near-ties in ground-truth retention times; borderline orderings may artificially inflate or deflate correlation coefficients.
- Hyperparameter search (via joblib parallelization) can produce minor non-determinism if random seeds are not fixed; results reproducibility may require explicit seed control.

## Evidence

- [other] Capture predicted retention orders and compare against ground-truth orderings using the repository's evaluation metrics (ranking accuracy, Spearman correlation, or similar).: "Capture predicted retention orders and compare against ground-truth orderings using the repository's evaluation metrics (ranking accuracy, Spearman correlation, or similar)."
- [readme] All experiments of the paper can be reproduced by using the [evaluation_scenarios_main.py](src/evaluation_scenarios_main.py) script with the proper parameters: "All experiments of the paper can be reproduced by using the evaluation_scenarios_main.py script with the proper parameters"
- [readme] The scripts run out of the box, if all the package dependencies are sattisfied.: "The scripts run out of the box, if all the package dependencies are sattisfied."
- [readme] [Summary of the results](results/ECCB2018.html) shown in the paper (File needs to be downloaded and opened with a web-browser.).: "Summary of the results shown in the paper (File needs to be downloaded and opened with a web-browser.)"
- [readme] Single system used as training and target. Different percentage of data used for trainging. | Figure 4 (stroked lines): "Single system used as training and target with different percentage of data used for training compared across scenarios."
