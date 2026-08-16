---
name: feature-missingness-threshold-filtering
description: Use when after loading and formatting raw peak-picked LC-MS metabolomics
  data frames (via metabData constructor) when you need to eliminate features with
  poor sample coverage before feature alignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - metabCombiner
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-missingness-threshold-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove low-abundance or sparsely-detected metabolomic features from LC-MS datasets by applying a sample-wise missingness threshold. This filtering step eliminates features detected in fewer than a specified percentage of samples, reducing noise and improving feature quality before downstream alignment and scoring.

## When to use

Apply this skill after loading and formatting raw peak-picked LC-MS metabolomics data frames (via metabData constructor) when you need to eliminate features with poor sample coverage before feature alignment. Triggers: (1) raw peak table contains features with sporadic detection across replicates or sample groups; (2) you aim to reduce false positives and focus on robust, reproducibly-detected metabolites; (3) downstream alignment or scoring steps are sensitive to feature sparsity.

## When NOT to use

- Input is already a curated, published feature table with hand-verified annotations (missingness filtering may discard biologically-relevant rare features).
- Experimental design intentionally includes sparse, low-abundance metabolites as biological endpoints (e.g., disease biomarkers detected in only 10% of samples; strict missingness filtering would eliminate them).
- Data has already been filtered for missingness upstream; applying redundant thresholds risks over-filtering and loss of reproducible signal.

## Inputs

- raw peak-picked LC-MS data frame with mz, rt, id, adduct, and sample columns
- misspc parameter: numeric threshold (0–100) indicating minimum sample detection percentage

## Outputs

- metabData object: formatted and filtered feature table with features below misspc threshold removed
- retained feature count: number of features passing missingness filter

## How to apply

Within the metabData formatting workflow, invoke the missingness filter by specifying the `misspc` argument (a percentage threshold, e.g., 50%). The filter scans all sample columns for each feature and counts the proportion of non-missing values (detections). Features whose detection frequency falls below the `misspc` threshold are removed from the formatted metabData object. The rationale is that features present in only a small fraction of samples are likely artifacts, instrument noise, or biological outliers; retaining only features meeting the threshold ensures robust m/z and retention time mappings for subsequent pairwise alignment. Typical thresholds range from 50–80% depending on experimental design (e.g., loose for exploratory work, strict for targeted follow-up).

## Related tools

- **metabCombiner** (R package providing metabData constructor and missingness filter implementation for LC-MS metabolomics data formatting and filtering) — https://github.com/hhabra/metabCombiner
- **R** (execution environment for metabCombiner and data frame manipulation)

## Examples

```
metabData(plasma20, mz='mz', rt='rt', id='id', adduct='adduct', samples='CHEAR', misspc=50)
```

## Evaluation signals

- Verify that all retained features have detection frequency ≥ misspc threshold across sample columns; audit marginal cases near threshold boundary.
- Compare feature count before and after filtering; report percentage of features eliminated and confirm it aligns with expected sparsity of input dataset.
- Inspect downstream m/z grouping and pairwise alignment step: if missingness filtering succeeded, feature-pair detection should show stable, non-spurious alignments without artefactual m/z clustering.
- Confirm that no sample columns are entirely empty (all-missing) in the output metabData; presence of such a column indicates filter logic error.
- Cross-check that the misspc parameter used matches the analysis plan; missingness filter should be applied only once per dataset to avoid cascade effects.

## Limitations

- Missingness threshold is global across all sample columns; the filter does not account for sample-group-specific sparsity patterns (e.g., biomarkers present only in disease subgroup may be filtered if they are rare in the entire cohort).
- Filter operates on detection (non-missing) status only; it does not consider intensity or signal-to-noise ratio, so a feature detected in many samples at very low abundance may pass the threshold but be uninformative.
- Threshold choice (misspc value) is user-defined and not data-driven; no principled guidance is provided in the article for selecting optimal thresholds for different experimental designs.
- Filtering is irreversible within the metabData object; users must retain the original data frame if downstream reanalysis with different thresholds is anticipated.

## Evidence

- [intro] The missingness filter eliminates features below some threshold percentage indicated by the *misspc* argument.: "The missingness filter eliminates features below some threshold percentage indicated by the *misspc* argument."
- [methods] For samples and extra fields, metabData searches for all columns containing any of the keywords in the respective arguments, with regular expressions accepted for any indicated field.: "for samples and extra fields, [metabData] searches for all columns containing any of the keywords in the respective arguments, with regular expressions accepted for any indicated field."
- [intro] metabCombiner determines possible feature pair alignments and validates them through pairwise similarity scoring.: "`metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
