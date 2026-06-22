---
name: false-positive-annotation-filtering
description: Use when after high-scoring spectral library matching (e.g., EQ module output) of LC-MS/MS data yields candidate lipid annotations; when spectral similarity alone produces false positives and you have computed relative retention time intervals across species cohorts;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - LipidIN LCI module
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
---

# false-positive-annotation-filtering

## Summary

Apply the Lipid Categories Intelligence (LCI) model using three relative retention time (RRT) rules to re-evaluate high-confidence spectral matches and filter false positive lipid annotations, reducing estimated false discovery rate to 5.7% while maintaining coverage of 8923 lipids across multiple species.

## When to use

After high-scoring spectral library matching (e.g., EQ module output) of LC-MS/MS data yields candidate lipid annotations; when spectral similarity alone produces false positives and you have computed relative retention time intervals across species cohorts; when reducing false discovery rate while preserving true lipid identifications is critical for downstream biomarker discovery or comparative lipidomics.

## When NOT to use

- Input consists of single-species or single-sample LC-MS/MS data with no retention time intervals across cohorts to compute RRT rules.
- Candidate annotations already have very low error rates (< 1%) from targeted or high-resolution methods where RRT filtering would add unnecessary complexity.
- Mass spectrometry data lacks reliable retention time calibration or normalization across runs, making RRT comparisons unreliable.

## Inputs

- Candidate lipid annotations from spectral library matching (e.g., EQ module output with secondary matching scores)
- Relative retention time (RRT) values extracted from LC-MS/MS runs across multiple species or sample cohorts
- Preprocessed mass spectrometry data in .rda format (output from data preprocessing module)

## Outputs

- Filtered lipid predictions with false discovery rate (FDR) metric
- Lipid coverage statistics (count of unique lipid identifications passing RRT-based filtering)
- CSV-formatted identification results with re-evaluated match confidence

## How to apply

Load spectral query results (candidate lipid annotations with matching scores from secondary mass spectrometry library matching). Extract relative retention time (RRT) values for each candidate lipid and compute RRT intervals across your species or sample cohorts. Apply the three RRT rules from the Lipid Categories Intelligence model as heuristic filters that use secondary matching scores as prior information to re-evaluate candidates. Aggregate predictions and compute false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications) across all samples. Export filtered lipid predictions with FDR metric and coverage statistics. The method relies on the principle that true lipids exhibit consistent RRT behavior across related species, while false positives do not.

## Related tools

- **LipidIN LCI module** (Implements the three RRT rules to conduct heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches and filter false positives) — https://github.com/LinShuhaiLAB/LipidIN
- **XCMS** (Processes mass spectrometry data for nonlinear peak alignment, matching, and identification prior to LCI filtering)
- **CAMERA** (Performs compound spectra extraction and annotation of LC-MS data sets that feed into the LCI filtering pipeline)

## Examples

```
source('LCI.r'); LCI(filename='QC_POS1.rda')
```

## Evaluation signals

- Achieved false discovery rate (FDR) matches or is lower than the 5.7% benchmark reported across the same lipid classes and species.
- Lipid coverage (count of unique lipid identifications) remains ≥ 8900 lipids or is consistent with the species and cohort size tested.
- Exported CSV results contain FDR scores and pass schema validation: each annotation row has a matching score, RRT interval classification, and binary pass/fail flag from RRT rules.
- Visual inspection: boxplots or scatter plots of RRT values for filtered lipids should show tight clustering within species, while rejected candidates show scattered or outlier RRT behavior.
- Comparison to unfiltered spectral matches confirms that the number of false positives is substantially reduced (estimated by comparing to orthogonal validation or manual inspection of a random sample).

## Limitations

- Requires multi-species or multi-cohort LC-MS/MS data with reliable retention time normalization; single-run or single-species data cannot compute RRT intervals and will fail.
- Performance depends on the quality and breadth of the reference lipid hierarchical library; incomplete or biased libraries may cause true lipids to be misclassified as false positives.
- The three RRT rules are heuristic and may over-filter in organisms or lipid classes with non-standard retention time patterns, or under-filter in matrices with extreme retention time drift.
- Data format conversion from mzML to .rda for the LCI module takes approximately 2 minutes and requires substantial disk I/O; processing very large batches may be time-intensive.

## Evidence

- [other] Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives.: "Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives."
- [readme] The Lipid Categories Intelligence (LCI) Module: Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches.: "Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches."
- [readme] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [other] Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts.: "Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts."
- [other] Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications).: "Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications)."
