---
name: ion-clustering-by-retention-time-and-mass
description: Use when your peak table contains suspected mispicked ions—ions with similar m/z and retention time that likely represent the same metabolite split across multiple features due to preprocessing errors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - R
  - mpactr
  - data.table
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
---

# ion-clustering-by-retention-time-and-mass

## Summary

Identify and merge incorrectly split isotopic patterns and detector artifacts by clustering ions with similar retention time and mass-to-charge ratios. This skill corrects mispicked peaks introduced during tandem MS/MS preprocessing, improving feature quality before downstream metabolomics analysis.

## When to use

Apply this skill when your peak table contains suspected mispicked ions—ions with similar m/z and retention time that likely represent the same metabolite split across multiple features due to preprocessing errors. Use it early in the filtering workflow after importing peak table and metadata but before applying group-based or replicability filters.

## When NOT to use

- Peak table is already manually curated or comes from a preprocessing tool that correctly handles isotope deconvolution.
- Input lacks retention time information or m/z values (clustering requires both dimensions).
- You need to preserve all original ion identities for later spectral library matching or compound annotation (merging by sum loses individual isotope patterns).

## Inputs

- peak_table (CSV from Progenesis or compatible MS preprocessing software)
- metadata file (sample annotations, group assignments)
- mpactr data object (created by import_data())

## Outputs

- filtered mpactr object with mispicked ions merged
- filter_summary object containing failed_ions and passed_ions lists
- similar_ions report (from get_similar_ions()) listing ion groups and their merged main ion identifiers

## How to apply

Load the peak table and metadata into an mpactr object using import_data(). Apply filter_mispicked_ions() with parameters: ringwin=0.5 (retention time window in minutes), isowin=0.01 (isotope m/z window), trwin=0.005 (expected m/z shift for isotopes), max_iso_shift=3 (maximum number of isotopic peaks to consider), merge_peaks=TRUE, and merge_method='sum' (sums abundances of merged ions). Extract the filtering summary using filter_summary(data, filter='mispicked') to report flagged similar-ion groups, merged count, and remaining ions. Optionally retrieve detailed groupings with get_similar_ions() to validate which ions were merged with their corresponding main ions. Use copy_object=FALSE for memory efficiency when chaining filters.

## Related tools

- **mpactr** (Primary R package providing filter_mispicked_ions(), filter_summary(), and get_similar_ions() functions for clustering and merging ions.) — https://github.com/mums2/mpactr
- **R** (Runtime environment and language for executing mpactr workflows and data manipulation.)
- **data.table** (Data structure and manipulation backend used by mpactr for efficient ion and group operations.)

## Examples

```
filter_mispicked_ions(data, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); summary <- filter_summary(data, filter='mispicked'); head(summary$passed_ions)
```

## Evaluation signals

- filter_summary() output shows number of ions flagged as similar and merged count is > 0 (indicating clustering occurred).
- Remaining ion count post-filtering is consistent with expected reduction (typically 5–15% of mispicked ions merged).
- Visualizing passed_ions by m/z and retention time shows no persistent clusters of ions within ringwin and isowin thresholds.
- get_similar_ions() groups contain ions with m/z differences matching expected isotope spacing (≈1 Da for C12/C13, etc.) and retention time within ringwin tolerance.
- Downstream statistical tests (fold change, t-tests) show improved effect sizes and reduced noise after filtering, compared to unfiltered data.

## Limitations

- Clustering quality is sensitive to parameter choice (ringwin, isowin, trwin); tuning may be needed for different MS platforms or chromatographic methods.
- merge_method='sum' combines abundances but discards individual isotope peak heights, losing information about isotope ratio fidelity.
- Does not distinguish between true isotopic patterns and co-eluting isomers; false merging can occur if two different metabolites share similar m/z and retention time.
- Requires both m/z and retention time dimensions; cannot be applied to MS/MS or ion mobility data alone without external alignment.
- Performance may degrade on very large peak tables (>100k features) due to all-pairwise clustering; copy_object=FALSE is essential for memory management.

## Evidence

- [abstract] filter_mispicked_ions with parameters ringwin, isowin, trwin, max_iso_shift, merge_peaks, merge_method: "filter_mispicked_ions(data2, ringwin = 0.5, isowin = 0.01, trwin = 0.005, max_iso_shift = 3, merge_peaks = TRUE, merge_method = "sum", copy_object = FALSE)"
- [abstract] filter_summary components and access method: "filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the"
- [methods] Detect ions with similar retention time and mass-to-charge: "Apply filter_mispicked_ions with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, and merge_method='sum' to detect ions with similar retention time and"
- [methods] Extract and retrieve detailed ion groups: "Extract the mispicked ion filtering summary using filter_summary(data, filter='mispicked') to report the number of ions flagged as similar, the number of ions merged, and the count of ions remaining"
- [abstract] Memory efficiency recommendation: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [readme] mpactr package purpose: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data."
- [readme] filter_mispicked_ions function description: "`filter_mispicked_ions()`: removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
