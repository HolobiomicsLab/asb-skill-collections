---
name: validated-dataset-integrity-verification
description: Use when you have received a validated dataset (e.g., interim/tables/4_analysed/platinum.tsv.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Python 3
  license_tier: restricted
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
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

# validated-dataset-integrity-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify the structural and semantic integrity of a validated dataset by independently reproducing key aggregation metrics (unique entities, deduplicated pairs) and confirming they match reported values. This skill ensures that downstream analyses rely on accurate, consistently counted data.

## When to use

Use this skill when you have received a validated dataset (e.g., interim/tables/4_analysed/platinum.tsv.gz) and need to confirm that the reported summary counts—unique structures, unique organisms, unique structure-organism pairs, and their format-specific breakdowns (3D vs. 2D)—are reproducible and correct before performing downstream analysis or publishing findings.

## When NOT to use

- Input dataset has not undergone formal curation or validation; use exploratory data profiling instead.
- No published or reference counts exist to compare against; this skill requires a ground-truth target.
- Dataset is already known to be corrupted or incomplete; prioritize data repair before verification.

## Inputs

- validated dataset table (TSV/CSV, e.g., platinum.tsv.gz)
- specification of expected counts for structures, organisms, and pairs

## Outputs

- structured summary table (CSV or TSV) with rows for each metric (unique structures 3D, unique structures 2D, unique organisms, unique pairs 3D, unique pairs 2D) and columns for count value, data format, and match status vs. reported aggregate

## How to apply

Load the validated dataset using R or Python and programmatically extract, deduplicate, and count the following distinct entities: (1) structure identifiers (SMILES, InChI, or nominal identifiers), counted separately for 3D and 2D representations; (2) organism taxonomy identifiers, deduplicated across all records; (3) structure-organism pair combinations, also separately for 3D and 2D formats. Compare the computed counts against the reported aggregates (e.g., 231330 unique 3D structures, 153956 unique 2D structures, 42166 unique organisms, 588694 total and 484174 3D|2D unique pairs for the LOTUS platinum dataset). The rationale is that deduplication counts serve as a stable, reproducible fingerprint of dataset composition; if counts diverge from published values, it signals either data corruption, parsing errors, or an inconsistency in the curation pipeline that must be resolved before analysis.

## Related tools

- **R** (Data loading, deduplication, and aggregation of structure and organism identifiers) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Alternative platform for dataset loading, entity extraction, and count validation) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R
library(data.table)
pt <- fread('interim/tables/4_analysed/platinum.tsv.gz')
cat('Unique 3D structures:', nrow(unique(pt[format=='3D', .(structure_id)])), '\nUnique 2D structures:', nrow(unique(pt[format=='2D', .(structure_id)])), '\nUnique organisms:', nrow(unique(pt[, .(organism_id)])), '\nUnique pairs (3D):', nrow(unique(pt[format=='3D', .(structure_id, organism_id)])), '\n')
```

## Evaluation signals

- Computed unique structure count (3D) matches reported value (231330 for LOTUS platinum); same for 2D (153956).
- Computed unique organism count matches reported value (42166 for LOTUS platinum).
- Computed unique structure-organism pair counts match reported totals (588694 overall, 484174 in 3D|2D format for LOTUS platinum).
- Summary table exports cleanly and contains no NULL or inconsistent rows; format consistency (e.g., no mixed case in format labels) is preserved.
- Deduplication logic is reproducible: running the same script twice on the same input yields identical counts.

## Limitations

- Counts depend critically on correct parsing of structure identifiers (SMILES, InChI) and organism taxonomy fields; malformed or missing values will skew aggregates.
- The skill verifies count reproducibility but does not validate the semantic correctness of individual structure–organism associations or detect erroneous curation.
- Format-specific deduplication (3D vs. 2D) requires that the dataset explicitly encodes structure dimensionality; missing or ambiguous format annotations will cause misclassification.
- No changelog or version history is documented in the LOTUS processor repository; unable to trace whether reported counts correspond to the current dataset snapshot.

## Evidence

- [methods] Load the validated platinum dataset (interim/tables/4_analysed/platinum.tsv.gz) using R or Python.: "Load the validated platinum dataset (interim/tables/4_analysed/platinum.tsv.gz) using R or Python."
- [methods] The LOTUS platinum dataset contains 231330 unique curated structures in 3D and 153956 in 2D format from 42166 unique organisms, with 588694 unique referenced structure-organism pairs (484174 in 3D|2D format).: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [methods] Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations.: "Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations."
- [methods] Validate counts match the reported aggregates: 231330 (3D) and 153956 (2D) unique curated structures; 42166 unique organisms; 588694 (3D) and 484174 (2D) unique referenced structure-organism pairs.: "Validate counts match the reported aggregates: 231330 (3D) and 153956 (2D) unique curated structures; 42166 unique organisms; 588694 (3D) and 484174 (2D) unique referenced structure-organism pairs."
- [methods] Export counts to a structured summary table (CSV or TSV) with rows for each metric and columns for count value and data format.: "Export counts to a structured summary table (CSV or TSV) with rows for each metric and columns for count value and data format."
- [readme] *LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
