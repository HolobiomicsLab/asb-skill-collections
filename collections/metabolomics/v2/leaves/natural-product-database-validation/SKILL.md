---
name: natural-product-database-validation
description: Use when after curating and integrating structure-organism pairs from
  multiple source databases, and before publishing or using the dataset for computational
  research. Apply this skill when you have aggregated organism counts binned by structural
  diversity (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - R
  - 1_sampling.R
  - 2_validating.R
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

# natural-product-database-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate curated natural products databases by comparing observed organism-structure distributions against reference benchmarks and detecting discrepancies in binned counts. This skill ensures data integrity across large structure-organism pair collections before downstream computational chemistry applications.

## When to use

After curating and integrating structure-organism pairs from multiple source databases, and before publishing or using the dataset for computational research. Apply this skill when you have aggregated organism counts binned by structural diversity (e.g., organisms with exactly 1 structure, 1–10 structures, 10–100 structures, >100 structures) and need to validate these counts match expected reference distributions or previously published benchmarks.

## When NOT to use

- Input is raw, uncurated structure-organism pairs with known duplicates or inconsistent organism naming—first apply standardization and taxonomy cleaning steps.
- Reference benchmark values are unavailable or were derived from a different data model or time period; validation requires a stable, documented baseline.
- The goal is only to count total unique structures or organisms, not to understand their distribution—use simple aggregation instead of binned validation.

## Inputs

- Flat file of structure-organism pairs (TSV/CSV with columns: organism_id, structure_id, structure_count or equivalent)
- Reference benchmark counts (prior publication or curated baseline values)
- Organism metadata (taxonomy, cleaning status, curation version)

## Outputs

- Binned organism count table (4 bins: exactly 1 / 1–10 / 10–100 / >100 structures)
- Validation report comparing observed vs. reference counts with discrepancy flags
- Summary statistics (total organisms validated, percentage match, outlier organisms)

## How to apply

Load the integrated structure-organism pair table (e.g., the LOTUS flat file containing 484,174 unique 2D structure-organism pairs) into a data frame. Group organisms by their unique structure count and bin them into discrete categories (exactly 1 structure, 1–10 structures, 10–100 structures, and >100 structures). Count the number of organisms in each bin. Compare observed binned counts against reference values from the literature or prior curation cycles (e.g., 7,354 / 21,490 / 10,683 / 374). Report any absolute or percentage discrepancies and investigate root causes (e.g., duplicate removal, taxonomy cleaning, structure sanitization artifacts). Use R for grouping, binning, and aggregation operations.

## Related tools

- **R** (Grouping organisms by unique structure count, binning, and aggregation; statistical comparison of observed vs. reference distributions) — https://github.com/lotusnprod/lotus-processor
- **1_sampling.R** (Sampling and validation of curated data before final publication) — https://github.com/lotusnprod/lotus-processor
- **2_validating.R** (Post-sampling validation and discrepancy reporting) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load LOTUS 2D pairs, group by organism, count structures per organism, bin, and validate
lotus_df <- read.csv('interim/tables/3_curated/table.tsv.gz', sep='\t')
org_struct_counts <- lotus_df %>% group_by(organism_id) %>% summarise(struct_count = n_distinct(structure_id))
binned <- org_struct_counts %>% mutate(bin = case_when(struct_count == 1 ~ '1', struct_count <= 10 ~ '1-10', struct_count <= 100 ~ '10-100', TRUE ~ '>100')) %>% group_by(bin) %>% summarise(count = n())
print(binned); # Compare to reference: c(7354, 21490, 10683, 374)
```

## Evaluation signals

- Observed organism counts in each bin match or are within acceptable tolerance (e.g., <1% absolute difference) of reference values (7,354 / 21,490 / 10,683 / 374 for LOTUS 2D data).
- Total organism count sums to 42,166 (or the expected total for your dataset) across all four bins with no gaps or overlaps.
- No organisms are assigned to multiple bins (mutually exclusive binning).
- Discrepancies are documented with root cause (e.g., removal of duplicates, taxonomy updates, structure sanitization), not unexplained.
- The validation report is reproducible: re-running the workflow on the same input produces identical binned counts.

## Limitations

- Binning is discrete and does not capture the full distribution shape—examine percentile plots or kernel density estimates for nuanced analysis.
- Reference benchmarks may be outdated if source databases or curation rules change; update baselines periodically.
- Validation detects *statistical* discrepancies but not semantic errors (e.g., incorrect organism names, conflated species). Pair with taxonomy cleaning and manual review.
- Large datasets (>100,000 organisms) may have slow grouping operations in R; consider vectorization or database backends for extreme scale.

## Evidence

- [readme] LOTUS provides documented structure-organism pairs: "*LOTUS* is a comprehensive collection of documented structure-organism pairs."
- [methods] LOTUS dataset size and scope: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [methods] Validation binning task definition: "Group organisms by unique 2D structure count and bin into four categories: exactly 1 structure, 1–10 structures, 10–100 structures, and >100 structures."
- [methods] Validation against reference counts: "Validate the observed counts against the reported reference values (7,354, 21,490, 10,683, 374) and report any discrepancies or confirmation."
- [methods] Sampling and validation workflow step: "3_analyzing – sampling and validation of curated data"
