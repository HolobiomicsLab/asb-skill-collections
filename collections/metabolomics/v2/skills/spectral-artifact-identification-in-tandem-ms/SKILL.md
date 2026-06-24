---
name: spectral-artifact-identification-in-tandem-ms
description: Use when you have a raw or preprocessed peak table from tandem MS/MS
  data (e.g., from Progenesis QI, MS-DIAL, or Bruker Metaboscape) and observe features
  that may represent detector artifacts, incorrectly merged/split isotopic patterns,
  or sample carryover contaminants (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mpactr
  - MPACT (Python GUI)
  - ggplot2
  - plotly
  - data.table
  techniques:
  - LC-MS
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-artifact-identification-in-tandem-ms

## Summary

Identify and remove spectral artifacts—including mispicked ions (incorrectly split isotopic patterns), in-source fragments, and group-specific contaminants—from tandem MS peak tables using computational filters prior to downstream metabolomics analysis. This skill is essential because mass spectrometry preprocessing can introduce peak selection errors that confound biological interpretation.

## When to use

Apply this skill when you have a raw or preprocessed peak table from tandem MS/MS data (e.g., from Progenesis QI, MS-DIAL, or Bruker Metaboscape) and observe features that may represent detector artifacts, incorrectly merged/split isotopic patterns, or sample carryover contaminants (e.g., solvent blanks showing unexplained ion abundance). Use it after import but before statistical comparison, correlation, or fold-change analysis.

## When NOT to use

- Input is already a high-confidence curated feature table or a post-statistical results table (e.g., differential abundance output); re-filtering may remove valid discoveries.
- Raw tandem MS data has not yet been preprocessed into a peak table (use peak-picking software like MS-DIAL or Progenesis first).
- Analysis includes intentional study of in-source fragments or isotopic fine structure; artifact removal would eliminate the signal of interest.

## Inputs

- peak_table_file (CSV format, e.g. cultures_peak_table.csv: m/z, retention time, intensity columns)
- metadata_file (CSV format with sample identifiers and group assignments)
- mpactr object (in-memory R object after import_data())

## Outputs

- filtered peak table (feature matrix with artifacts removed)
- filter_summary report (counts of passed_ions, failed_ions, ions flagged or merged per filter)
- similar_ions groups (mapping of mispicked ions to their merged parent ions)
- interactive plot (m/z vs. retention time with filter fate overlay using ggplot/plotly)

## How to apply

First, load the peak table and metadata into an mpactr object using import_data(). Then systematically apply artifact filters in sequence: (1) filter_mispicked_ions() with ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, and merge_peaks=TRUE to detect ions with similar retention time and m/z that likely represent incorrectly split isotopic patterns; (2) filter_group(group_to_remove='Solvent_Blank') and filter_group(group_to_remove='Media') to remove features overrepresented in blank/vehicle samples relative to biological groups; (3) filter_cv(cv_threshold=0.2) to flag non-reproducible features with high coefficient of variation between technical replicates; and (4) filter_insource_ions() to remove fragment ions created in the ionization interface. After each filter step, use filter_summary() with the appropriate filter name to extract passed_ions and failed_ions counts, and optionally retrieve get_similar_ions() to inspect which ions were merged. The rationale is that MS preprocessing introduces predictable errors in specific mass ranges and retention time windows; filtering by isotopic coherence, group membership, and replicate reproducibility recovers high-confidence features.

## Related tools

- **mpactr** (R package providing filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions(), filter_summary(), and get_similar_ions() functions; core artifact-removal engine) — https://github.com/mums2/mpactr
- **MPACT (Python GUI)** (Original desktop application for spectral artifact identification; supports Progenesis, MS-DIAL, Bruker Metaboscape, and GNPS peak table formats) — https://github.com/BalunasLab/mpact
- **ggplot2** (Visualization of input features and their filter fate by m/z and retention time)
- **plotly** (Interactive plot generation for exploring features failing individual filters)
- **data.table** (Efficient in-memory manipulation of large peak tables during filtering)

## Examples

```
filter_mispicked_ions(data, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); filter_summary(data, filter='mispicked')
```

## Evaluation signals

- filter_summary() output shows non-zero passed_ions count and reasonable failed_ions proportions (typically 5–30% of input features removed by mispicked filter, depending on preprocessing quality).
- Interactive m/z vs. retention time plot shows filtered ions are distributed across the chemical space (not clustered in suspect m/z or RT ranges), indicating filters are not over-removing.
- get_similar_ions() output confirms that merged mispicked ions have consistent delta-m/z consistent with expected isotope shifts (e.g., ~1.003 for 13C, ~2.004 for 18O).
- Technical replicate correlation (calculated with cor() or Hmisc on filtered feature matrix) is higher post-filtering than pre-filtering, indicating reduced noise.
- Fold-change analysis between biological groups (using get_group_averages() or t-tests) on filtered vs. unfiltered tables shows more stable p-values and fewer false-positive hits in blanks.

## Limitations

- filter_mispicked_ions() parameters (ringwin, isowin, trwin, max_iso_shift) are tuned for typical metabolomics workflows; extreme mass ranges, high-resolution orbitrap data, or untargeted lipidomics may require manual adjustment.
- filter_cv() with cv_threshold=0.2 assumes technical replicates are present in the dataset; singleton samples cannot be evaluated for reproducibility.
- filter_group() removes features overrepresented in blanks but cannot distinguish true carryover from biological enrichment in control groups; manual inspection of get_group_averages() is recommended.
- The reference-semantics implementation (copy_object=FALSE) modifies the input mpactr object in place; create a copy beforehand if you need to compare unfiltered vs. filtered results.
- Filters are independent and order-dependent; applying filters in different sequences may yield different final feature counts. The article recommends a fixed workflow (mispicked → group → cv → insource) but users may customize.

## Evidence

- [methods] Filter_mispicked_ions explanation and parameters: "Apply filter_mispicked_ions with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, and merge_method='sum' to detect ions with similar retention time and"
- [abstract] Filter summary and component extraction: "The filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the"
- [methods] In-source ion and group filtering: "If you would like to remove insource ions fragments, you can do so with mpactr's `filter_insource_ions()`. We will check our feature table for mispicked ions, remove solvent blank and media blanks"
- [methods] CV filter and replicability rationale: "filter_cv(cv_threshold = 0.2) to remove non-reproducible features, or those that are inconsistent between technical replicates"
- [abstract] Memory efficiency and filter chaining: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [readme] README: Package purpose and scope: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data."
- [readme] README: Mispicked ions definition: "`filter_mispicked_ions()`: removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
