---
name: organism-count-distribution-analysis
description: Use when you have a flat file of structure-organism pairs (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3307
  tools:
  - R
  - dplyr / tidyr (R packages)
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

# organism-count-distribution-analysis

## Summary

Partitions organisms in a structure-organism pair dataset into four bins by the count of unique 2D chemical structures each organism contains, enabling characterization of structural diversity across the organismal taxonomy. This skill is essential for validating the completeness and composition of natural products databases and understanding which organisms have been most extensively characterized chemically.

## When to use

Apply this skill when you have a flat file of structure-organism pairs (e.g., the LOTUS dataset with 484,174 unique 2D structure-organism pairs across 42,166 organisms) and need to assess how many organisms fall into categories of low (1 structure), moderate (1–10 structures), high (10–100 structures), or very high (>100 structures) structural characterization. Use it to validate reported organism distributions or to identify undercharacterized or overrepresented organisms in the database.

## When NOT to use

- Input is 3D structures only, not 2D: the method bins by 2D structure count specifically; 3D structures require separate analysis or are out of scope.
- Organism identifiers are not consistent or standardized: grouping and counting will produce spurious or inflated bin counts if organism names or IDs are duplicated, mislabeled, or span different taxonomic levels.
- Structure-organism pairs are not deduplicated: if the input contains duplicate pairs, the count will inflate and misrepresent true organism-level diversity.

## Inputs

- LOTUS flat file (or similar structure-organism pair table): TSV/CSV with columns for organism identifier and 2D structure identifier
- organism count reference values (optional): numerical targets (e.g., 7,354 / 21,490 / 10,683 / 374) for validation

## Outputs

- organism count distribution table: four-row table with bin labels, organism counts per bin, and proportions
- validation report: comparison of observed counts vs. reference values, with flagged discrepancies

## How to apply

Load the structure-organism pairs flat file into a data frame (e.g., R tibble). Group by organism identifier and count the number of unique 2D structures per organism. Bin organisms into four mutually exclusive categories: exactly 1 structure, 1–10 structures (inclusive of lower bound, exclusive of upper), 10–100 structures, and >100 structures. Count the number of organisms in each bin. Compare observed counts against reference values (if available) to identify discrepancies that may indicate data quality issues, missing entries, or curation artifacts. Report counts and proportions for each bin to characterize the distribution of structural characterization effort across the organismal diversity.

## Related tools

- **R** (primary tool for loading flat file, grouping by organism, counting unique structures, binning, and generating distribution statistics) — https://github.com/lotusnprod/lotus-processor
- **dplyr / tidyr (R packages)** (group_by, summarize, and count operations for organism-level aggregation; referenced implicitly in lotus-processor R workflows) — https://github.com/lotusnprod/lotus-processor

## Evaluation signals

- Organism counts per bin sum to the total number of organisms (42,166 in LOTUS); no organisms are dropped or duplicated across bins.
- Bin boundaries are mutually exclusive and exhaustive: no organism falls into more than one bin, and all organisms with ≥1 structure are assigned to a bin.
- Observed organism counts match or closely align with reported reference values (7,354 / 21,490 / 10,683 / 374); discrepancies are documented and explained (e.g., database version, filtering criteria).
- Distribution is plausible: the majority of organisms typically fall into the 1–10 or 10–100 range (moderate characterization), with a small tail at >100 structures (intensively studied organisms).
- Reproducibility check: running the same grouping and binning logic on the same input file yields identical counts across runs.

## Limitations

- The method is sensitive to organism identifier standardization: non-unique or mislabeled organism IDs will inflate or deflate bin counts. External taxonomic verification (e.g., via OTL as in lotus-processor step 5_addingOTL) may be required.
- Structure deduplication upstream is assumed: if the input contains duplicate structure-organism pairs, the count will overestimate the true structural diversity per organism.
- The four-bin scheme (1, 1–10, 10–100, >100) is arbitrary. The thresholds may not align with biological or chemical definitions of 'characterization completeness'; domain knowledge is required to interpret bin assignments.
- Cross-database variation: LOTUS integrates data from 31 initial open databases; curation and coverage bias across source databases may skew organism distributions, making some organisms appear artificially over- or under-characterized.
- Temporal bias: older organisms with historical literature records may cluster in the >100 bin, while recently discovered organisms may cluster in the 1–10 bin, conflating curation effort with biological novelty.

## Evidence

- [methods] 484,174 unique 2D structure-organism pairs across 42,166 organisms: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [other] Four organism bins: 1 structure, 1–10 structures, 10–100 structures, and >100 structures: "Group organisms by unique 2D structure count and bin into four categories: exactly 1 structure, 1–10 structures, 10–100 structures, and >100 structures."
- [other] Reference organism counts for validation: 7,354 / 21,490 / 10,683 / 374: "Validate the observed counts against the reported reference values (7,354 / 21,490 / 10,683 / 374) and report any discrepancies or confirmation."
- [other] Load LOTUS flat file into a data frame and group by organism: "Load the LOTUS flat file (484,174 unique 2D structure-organism pairs across 42,166 organisms) into a data frame."
