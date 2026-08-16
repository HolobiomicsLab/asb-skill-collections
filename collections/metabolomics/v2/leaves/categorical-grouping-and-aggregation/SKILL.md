---
name: categorical-grouping-and-aggregation
description: 'Use when you have a flat table of structure-organism pairs or entity
  records and need to summarize their distribution across categorical bins (e.g.,
  organism counts binned by number of associated structures in categories: 1, 1–10,
  10–100, >100).'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
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
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
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

# categorical-grouping-and-aggregation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group entities (organisms, structures, or references) by a discrete categorical attribute and count or aggregate members within each group to summarize distributions and validate against reference benchmarks. This skill is essential for validating curated datasets against published counts and understanding the composition of large structure-organism pair collections.

## When to use

Apply this skill when you have a flat table of structure-organism pairs or entity records and need to summarize their distribution across categorical bins (e.g., organism counts binned by number of associated structures in categories: 1, 1–10, 10–100, >100). Use it to validate curated data against known reference values or to characterize the shape of a collection.

## When NOT to use

- Input is already a pre-aggregated frequency table or summary statistic; re-grouping would lose granularity.
- Categorical bins are not pre-defined or their boundaries are arbitrary; the skill requires substantive binning logic grounded in domain knowledge.
- The dataset is too large to fit in memory; consider streaming or database-backed grouping instead.

## Inputs

- Flat reference table (TSV or data frame) with structure-organism pairs
- Grouping attribute (e.g., organism identifier)
- Aggregation function (count or cardinality of unique structures per organism)
- Categorical bin boundaries (e.g., [1, 1-10, 10-100, >100])

## Outputs

- Contingency table or frequency distribution (entity counts per bin)
- Summary statistics (mean, median, range of entities per category)
- Validation report (observed vs. reference counts with discrepancy flagging)

## How to apply

Load the flat reference table (e.g., LOTUS structure-organism pairs: 484,174 unique 2D pairs across 42,166 organisms) into a data frame. Group records by the target categorical attribute (e.g., organisms grouped by their unique structure count). Bin grouped results into pre-defined categories (e.g., exactly 1 structure, 1–10, 10–100, >100 structures). Count the number of entities falling into each bin. Compare observed counts against published or reference values; report any discrepancies or confirmation of expected distributions. This approach validates data integrity and characterizes collection composition.

## Related tools

- **R** (Perform data frame grouping, binning, and aggregation via dplyr or base R group-by-count workflows) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Alternative grouping and aggregation via pandas.groupby() and cut() binning functions) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# R: Load LOTUS flat file and bin organisms by structure count
lotus_df <- read.table('lotus_structure_organism_pairs.tsv.gz', header=TRUE)
org_counts <- lotus_df %>% group_by(organism_id) %>% summarize(n_structures = n_distinct(structure_id))
binned <- org_counts %>% mutate(bin = case_when(n_structures == 1 ~ '1', n_structures <= 10 ~ '1-10', n_structures <= 100 ~ '10-100', TRUE ~ '>100')) %>% group_by(bin) %>% summarize(count = n())
```

## Evaluation signals

- Observed counts in each bin match the reference values (7,354 / 21,490 / 10,683 / 374 for LOTUS 2D structures) or explicitly justify discrepancies.
- Sum of all bin counts equals the total number of entities in the input table (e.g., 42,166 organisms).
- Bin boundaries are mutually exclusive and exhaustive (no entities fall outside or between bins).
- Distributions show expected shape (e.g., majority of organisms contain few structures, few organisms contain many).
- Reproducibility: re-running the grouping on the same input produces identical counts.

## Limitations

- Binning is sensitive to choice of category boundaries; small changes to thresholds (e.g., 1–10 vs. 1–11) can shift counts between adjacent bins.
- Extremely large tables (>10 million rows) may require memory-efficient streaming or database backends; in-memory data frames in R/Python may be slow or fail.
- The skill does not handle missing or inconsistent categorical values; data quality pre-processing (cleaning, standardization) is a prerequisite.
- Results are descriptive, not inferential; aggregation alone does not test statistical hypotheses or establish causation.

## Evidence

- [methods] Group organisms by unique 2D structure count and bin into four categories: exactly 1 structure, 1–10 structures, 10–100 structures, and >100 structures.: "Group organisms by unique 2D structure count and bin into four categories: exactly 1 structure, 1–10 structures, 10–100 structures, and >100 structures"
- [methods] Validate the observed counts against the reported reference values (7,354, 21,490, 10,683, 374) and report any discrepancies or confirmation.: "Validate the observed counts against the reported reference values (7,354, 21,490, 10,683, 374) and report any discrepancies or confirmation"
- [methods] Load the LOTUS flat file (484,174 unique 2D structure-organism pairs across 42,166 organisms) into a data frame.: "Load the LOTUS flat file (484,174 unique 2D structure-organism pairs across 42,166 organisms) into a data frame"
- [methods] 588694 | 484174 (3D|2D) unique referenced structure-organism pairs: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
