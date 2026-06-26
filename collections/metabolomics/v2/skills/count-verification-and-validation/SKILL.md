---
name: count-verification-and-validation
description: Use when you have grouped unique 2D chemical structures by organism prevalence
  and need to confirm that the counts in each frequency bin (singleton, low-diversity,
  medium-diversity, high-diversity) match published or curated reference values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3070
  tools:
  - R
  - Python 3
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]], 280[[3_cleaningAndEnriching/stereocounting.py]]
- R - Python 3 - Java >= 17
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Count Verification and Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that binned frequency counts of unique chemical structures match gold-standard reference counts across organism-prevalence categories. This skill ensures data integrity in large structure-organism pair datasets by detecting discrepancies between computed and expected distributions.

## When to use

Apply this skill when you have grouped unique 2D chemical structures by organism prevalence and need to confirm that the counts in each frequency bin (singleton, low-diversity, medium-diversity, high-diversity) match published or curated reference values. Use it as a final validation step after binning structure-organism pair data to detect loss, duplication, or miscategorization during processing.

## When NOT to use

- Input structures are already pre-binned or aggregated; you have only bin-level counts without raw pair data.
- No gold-standard or reference counts are available for comparison; validation requires a target benchmark.
- 3D structures or stereoisomer-resolved data; this skill is designed specifically for 2D structure-organism pairs.

## Inputs

- LOTUS 2D structure-organism pairs table (flat file format)
- Gold-standard bin membership counts (reference values)

## Outputs

- Count verification report (TSV or JSON)
- Bin membership counts by frequency category
- Discrepancy log (deviations from gold-standard)
- Summary statistics (per-bin counts and percentage agreement)

## How to apply

Load the LOTUS 2D structure-organism pairs table and count unique structures in each of four frequency bins: singleton structures (appearing in 1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures (>100 organisms). For each bin, compare the computed count against the gold-standard counts documented in the LOTUS publication. Generate a summary report listing bin membership counts and flagging any discrepancies. Document the nature and magnitude of deviations (e.g., percentage difference, absolute count difference) to assess whether further investigation into the processing pipeline is warranted.

## Related tools

- **R** (Primary scripting language for grouping structures, binning by organism count, and generating summary reports with dplyr/tidyr.) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Alternative scripting language for count aggregation and discrepancy detection via pandas or custom binning logic.) — https://github.com/lotusnprod/lotus-processor

## Examples

```
Rscript count_verification.R --input interim/tables/3_curated/table.tsv.gz --output validation/bin_counts.tsv --gold_standard docs/reference_counts.json
```

## Evaluation signals

- Computed bin counts exactly match (or fall within ±5%) the published gold-standard values for each frequency category.
- Total structure count across all bins equals the documented unique 2D structure count (153,956 in LOTUS).
- Discrepancy report is generated and reviewed; zero discrepancies or all flagged discrepancies have documented root causes in the processing log.
- No structures appear in multiple bins (mutually exclusive categorization); each structure is binned exactly once.
- Bin boundaries are correctly applied: singleton = 1, low-diversity = 2–10, medium-diversity = 11–100, high-diversity >100.

## Limitations

- Validation depends on the accuracy of the gold-standard reference counts; if the reference itself contains errors, this skill will not detect them.
- Discrepancies may arise from differences in how organisms are taxonomically classified or deduplicated; compare organism curation procedures before concluding a data integrity failure.
- The skill does not diagnose the root cause of discrepancies; it only detects and reports them. Further investigation of the processing pipeline (standardization, cleaning, integration steps) is required to resolve deviations.
- Large datasets (>100K structures) may require binning to be done iteratively or in memory-efficient chunks if computing resources are constrained.

## Evidence

- [other] Group all unique 2D structures by their associated organism count, bin structures into frequency categories, and count membership in each bin.: "Group all unique 2D structures by their associated organism count. 3. Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms),"
- [other] Count the number of structures in each bin and compare against published reference counts.: "Count the number of structures in each bin and compare against the reported gold-standard counts. 5. Generate a summary report documenting bin membership counts and any discrepancies."
- [other] LOTUS contains 153,956 unique 2D curated structures as reference benchmark.: "231330 | 153956 (3D|2D) unique curated structures"
- [readme] R is used for data integration and summarization tasks in LOTUS processing.: "R - Python 3 - Java >= 17"
