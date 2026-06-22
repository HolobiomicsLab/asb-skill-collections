---
name: peak-table-deconvolution
description: Use when your peak table contains ions with similar retention time and mass-to-charge ratios that likely represent isotopic patterns incorrectly split during preprocessing or detector artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - data.table
  - mpactr
  - MPACT
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
- library(data.table)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-deconvolution

## Summary

Reconstruct and systematically extract passing and failing ions from a peak table by applying the mispicked-ions filter, which identifies and merges incorrectly split isotopic patterns and detector artifacts. This skill enables detection of high-quality MS1 features by correcting peak selection errors introduced during tandem MS/MS preprocessing.

## When to use

Apply this skill when your peak table contains ions with similar retention time and mass-to-charge ratios that likely represent isotopic patterns incorrectly split during preprocessing or detector artifacts. Use it after importing peak table and metadata but before downstream statistical analyses, when you need to reduce false positives from fragmentation, isotopic multiplexing, or peak-picking errors that inflate feature counts.

## When NOT to use

- Peak table is already a deduplicated feature table (post-MS/MS preprocessing); mispicked filtering is a preprocessing step, not a downstream transformation.
- Your data lacks sufficient technical replicate structure or retention time metadata; the filter requires m/z and RT dimensions to identify similar ions.
- You need to preserve all detected ions for hypothesis generation or exploratory analysis without quality filtering; this skill removes candidate ions and is lossy.

## Inputs

- peak_table (CSV formatted, e.g., from Progenesis QI or MS-DIAL; rows=ions, columns=m/z, retention time, sample abundances)
- metadata_file (sample-level annotations with group labels)
- mpactr object created by import_data()

## Outputs

- filtered_peak_table (ions post-mispicked filtering with merged similar ions)
- filter_summary object (components: failed_ions with flagged similar-ion groups, passed_ions, counts of merged and remaining ions)
- similar_ions object from get_similar_ions() (detailed mapping of which ions were merged)

## How to apply

Load the peak table and metadata into an mpactr object using import_data(). Apply filter_mispicked_ions() with parameters ringwin=0.5 (retention time window in minutes), isowin=0.01 (isotopic mass window in Da), trwin=0.005 (retention time deviation tolerance), max_iso_shift=3 (maximum isotope shifts tolerated), merge_peaks=TRUE, and merge_method='sum' to detect and merge ions representing the same compound. Extract the filtering summary using filter_summary(data, filter='mispicked') to report flagged similar-ion groups, count of merged ions, and ions remaining post-filtering. Optionally retrieve detailed similar-ion groups with get_similar_ions() to audit which ions were merged with their corresponding main ions. Use reference semantics (copy_object=FALSE) for memory efficiency when chaining filters.

## Related tools

- **mpactr** (Core R package implementing filter_mispicked_ions(), filter_summary(), and get_similar_ions() functions for deconvolving and reconstructing peak tables) — https://github.com/mums2/mpactr
- **MPACT** (GUI and batch-processing tool for mispicked-ion filtering and related MS1 feature correction; supports Progenesis, MS-DIAL, and Bruker peak lists) — https://github.com/BalunasLab/mpact
- **data.table** (Dependency for efficient tabular data manipulation within mpactr workflows)

## Examples

```
filter_mispicked_ions(data, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); filter_summary(data, filter='mispicked')
```

## Evaluation signals

- filter_summary(data, filter='mispicked') returns non-zero counts for flagged similar ions and merged peaks, and passed_ions count is less than input ion count, indicating effective deconvolution.
- get_similar_ions() output shows coherent groupings (ions merged share m/z within isowin and RT within trwin, differing by ≤max_iso_shift isotope shifts).
- Post-filtering peak table retains expected primary ions and removes artefactual duplicates; verify via manual inspection of m/z clusters or by comparing to reference standard compounds.
- No errors or warnings in filter_mispicked_ions() execution; verify reproducibility by rerunning with same parameters and confirming identical merged-ion sets.
- Downstream correlation or t-test analyses show improved signal-to-noise (higher inter-replicate correlation, lower within-group CV) after mispicked filtering vs. unfiltered table.

## Limitations

- Parameter tuning (ringwin, isowin, trwin, max_iso_shift) is dataset- and instrument-specific; no universal default set applies across all ionization modes and mass analyzers.
- Merging strategy (merge_method='sum') assumes abundances are additive; appropriate for count/intensity but not for other derived metrics (e.g., retention time should be averaged, not summed).
- Filter may incorrectly merge true co-eluting isomers or isobars if they fall within the m/z and RT windows; manual audit of get_similar_ions() output is recommended for high-stakes identifications.
- Requires sufficient data quality (low RT and m/z measurement error); very high mass resolution or low-quality peak picking may reduce filter efficacy.
- Cannot distinguish between isotopic patterns and adducts; if your samples contain both, additional domain knowledge or multi-step filtering (e.g., filter_insource_ions()) may be needed.

## Evidence

- [other] The filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the mispicked filter): "filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the"
- [other] filter_mispicked_ions with parameters ringwin, isowin, trwin, max_iso_shift, merge_peaks, merge_method detect ions with similar retention time and mass-to-charge that likely represent incorrectly split isotopic patterns or detector artifacts: "detect ions with similar retention time and mass-to-charge that likely represent incorrectly split isotopic patterns or detector artifacts"
- [abstract] We recommend using the default copy_object = FALSE as this makes for an extremely fast and memory-efficient way to chain mpactr filters together: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [readme] mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data"
- [readme] filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing"
- [methods] To import these data into R, use the mpactr function import_data(), which has the arguments: peak_table_file_path and metadata_file_path: "use the mpactr function `import_data()`, which has the arguments: `peak_table_file_path` and `metadata_file_path`"
