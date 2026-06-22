---
name: structure-organism-pair-binning
description: Use when when you have loaded a structure-organism pairs table from a natural products database (e.g., LOTUS) and need to answer questions about the distribution of chemical diversity—specifically, how many unique 2D structures appear in exactly 1 organism versus many organisms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0602
  tools:
  - R
  - Python 3
  - lotus-processor
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
---

# Structure-Organism-Pair Binning

## Summary

Partition a dataset of unique 2D structures by their prevalence across organisms into discrete frequency bins (1 organism, 1–10 organisms, 10–100 organisms, >100 organisms), enabling comparative analysis of chemical diversity and organism–structure associations. This skill is essential for characterizing the breadth of natural product chemistry coverage in curated structure-organism databases.

## When to use

When you have loaded a structure-organism pairs table from a natural products database (e.g., LOTUS) and need to answer questions about the distribution of chemical diversity—specifically, how many unique 2D structures appear in exactly 1 organism versus many organisms. This binning reveals prevalence patterns and validates the comprehensiveness of the curation.

## When NOT to use

- The input is already pre-aggregated by organism (e.g., a table of organism-level statistics rather than raw structure-organism pairs).
- You are binning organisms by their structure counts rather than binning structures by their organism counts (use the inverse workflow instead).
- The structure-organism table is incomplete or lacks standardized structure or organism identifiers, making unique counting unreliable.

## Inputs

- LOTUS flat file or equivalent structure-organism pairs table (TSV/CSV format with ≥2 columns: structure identifier and organism identifier)
- Reference gold-standard bin counts (optional, for validation)

## Outputs

- Four-bin frequency table: counts of unique 2D structures in each prevalence bin (1, 1–10, 10–100, >100 organisms)
- Summary report documenting bin membership and any discrepancies from reference values
- Optionally: list of structures assigned to each bin for downstream analysis

## How to apply

Load the 2D structure-organism pairs table (e.g., the LOTUS flat file containing 484,174 unique structure-organism pairs across 42,166 organisms). For each unique 2D structure, count the number of distinct organisms in which it appears. Group structures by these organism counts and assign each structure to one of four frequency bins: singleton structures (appearing in exactly 1 organism), low-diversity structures (2–10 organisms), medium-diversity structures (11–100 organisms), and high-diversity structures (>100 organisms). Count the total number of structures in each bin. Compare the observed bin membership counts against published reference values (or gold-standard counts from a validation cohort) to detect curation discrepancies or confirm reproducibility. Report bin membership totals and any structures that fall outside expected ranges.

## Related tools

- **R** (Primary language for loading, grouping, and counting structure-organism pairs; generating summary tables and validation reports) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Alternative language for data frame manipulation and binning; can integrate with SMILES sanitization and structure validation pipelines) — https://github.com/lotusnprod/lotus-processor
- **lotus-processor** (Comprehensive workflow management system that standardizes, curates, and analyzes structure-organism pairs; provides reference data and validation harness) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load LOTUS 2D structure-organism pairs and bin structures by organism prevalence
data <- read.csv('lotus_pairs_2d.tsv', sep='\t')
struct_counts <- data %>% group_by(structure_id) %>% summarise(n_organisms = n_distinct(organism_id))
bins <- struct_counts %>% mutate(bin = case_when(n_organisms == 1 ~ '1', n_organisms <= 10 ~ '1-10', n_organisms <= 100 ~ '10-100', TRUE ~ '>100')) %>% group_by(bin) %>% summarise(count = n())
print(bins)
```

## Evaluation signals

- Observed bin counts match published reference values (e.g., 484,174 total structures correctly partitioned into reported counts for each bin).
- Sum of all bin membership counts equals the total number of unique structures in the input table (accounting closure).
- No structures are assigned to multiple bins; each structure appears in exactly one bin based on its organism count.
- Bin boundaries are respected: all structures in the '1' bin have organism_count = 1; all in '1–10' have 2 ≤ organism_count ≤ 10, etc.
- Summary report identifies any structures with organism counts that fall outside expected ranges or contradict organism-level metadata.

## Limitations

- The binning depends on the accuracy and completeness of the underlying structure-organism pairs table; missing or misidentified pairs will distort bin membership counts.
- Structure identifiers must be canonical and deduplicated (e.g., standardized SMILES or InChI); if the same chemical structure is represented by multiple identifiers, organism counts will be underestimated.
- Organism identifiers must also be standardized; synonyms or misspellings can cause artificial fragmentation of organism counts across structures.
- The fixed bin boundaries (1, 1–10, 10–100, >100) may obscure fine-grained variation in prevalence; consider also reporting deciles or continuous prevalence distributions for detailed analyses.
- This binning reflects only documented structure-organism pairs in the database, not true ecological or biosynthetic prevalence; biased sampling in the source databases will propagate to the bins.

## Evidence

- [other] task_002 describes binning unique 2D structures by organism prevalence: "Group all unique 2D structures by their associated organism count. 3. Bin structures into four frequency bins: singleton structures (1 organism), low-diversity structures (2–10 organisms),"
- [other] LOTUS data scale and composition: "Load the LOTUS 2D structure-organism pairs table from the published flat file. 2. Group all unique 2D structures by their associated organism count."
- [other] Reference values for validation: "Count the number of structures in each bin and compare against the reported gold-standard counts. 5. Generate a summary report documenting bin membership counts and any discrepancies."
- [other] LOTUS dataset scale: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [readme] Tools recommended in README: "what you need is: - R - Python 3 - Java >= 17"
