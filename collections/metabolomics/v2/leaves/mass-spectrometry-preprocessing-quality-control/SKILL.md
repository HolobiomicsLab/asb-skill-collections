---
name: mass-spectrometry-preprocessing-quality-control
description: Use when immediately after importing raw peak tables and metadata from
  MS preprocessing software (e.g., Progenesis, MS-DIAL, Bruker Metaboscape).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - R
  - mpactr
  - MPACT
  - data.table
  - ggplot2 and plotly
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

# mass-spectrometry-preprocessing-quality-control

## Summary

A systematic workflow to filter and validate MS1 peak tables by detecting and removing mispicked ions, group-overrepresented features, non-reproducible peaks, and in-source fragments. This skill ensures high-quality feature tables for downstream metabolomics analysis by correcting errors introduced during tandem MS/MS preprocessing.

## When to use

Apply this skill immediately after importing raw peak tables and metadata from MS preprocessing software (e.g., Progenesis, MS-DIAL, Bruker Metaboscape). Use it when your data contains technical replicates, multiple sample groups (including blanks), and when you need to identify isotopic patterns that were incorrectly split, features contaminated by solvent or media blanks, or irreproducible features before statistical analysis or metabolite identification.

## When NOT to use

- Input is already a curated, published feature table from a repository (e.g., MassBank, GNPS library); re-filtering may remove intentional, validated features.
- Data lacks technical replicates or sample grouping metadata; filter_cv() and filter_group() require these to function meaningfully.
- Peak table originates from targeted MS analysis (e.g., multiple reaction monitoring) rather than untargeted discovery; mispicked-ion and in-source filtering are designed for discovery MS1 peak picking errors.

## Inputs

- peak_table (CSV or format-specific export from Progenesis, MS-DIAL, or Bruker Metaboscape)
- metadata file (sample annotations, group assignments, replicate designations)
- mpactr object (created by import_data())

## Outputs

- filtered peak table (ions passing all quality filters)
- filter_summary report (passed_ions, failed_ions, counts by filter type)
- similar_ions groups (from get_similar_ions() — mapping of merged ions to parent ions)
- interactive filter-fate visualization (m/z vs. retention time scatter with filter outcome coloring)

## How to apply

Load peak_table and metadata files into an mpactr object using import_data(). Apply filter_mispicked_ions() with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum' to detect ions with similar retention time and m/z that represent incorrectly split isotopic patterns or detector artifacts. Extract summary statistics using filter_summary(data, filter='mispicked') to confirm the count of ions flagged, merged, and remaining. Then apply filter_group() to remove features overrepresented in solvent and media blanks (relative ion abundance > 0.01), filter_cv() with cv_threshold=0.2 to remove non-reproducible features between technical replicates, and optionally filter_insource_ions() to remove in-source fragment ions. Use copy_object=FALSE (default) for memory efficiency when chaining filters. Visualize filter outcomes using interactive scatter plots (m/z vs. retention time colored by filter fate) to confirm filters are not systematically removing features at particular m/z or retention time ranges.

## Related tools

- **mpactr** (primary R package providing import_data(), filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions(), filter_summary(), and get_similar_ions() functions) — https://github.com/mums2/mpactr
- **MPACT** (original Python/Anaconda GUI application for data import and peak filtering; provides comparable filter logic for mispicked ions, group removal, and in-source fragmentation) — https://github.com/BalunasLab/mpact
- **data.table** (used internally and for user manipulation of peak and metadata tables within R environment)
- **ggplot2 and plotly** (create interactive scatter plots showing m/z vs. retention time and filter fates to visually confirm filters are not biased toward specific mass or retention time ranges)

## Examples

```
import_data('cultures_peak_table.csv', 'cultures_metadata.csv', format='Progenesis') |> filter_mispicked_ions(ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE) |> filter_group(group_to_remove='Solvent_Blank') |> filter_group(group_to_remove='Media') |> filter_cv(cv_threshold=0.2) -> filtered_data; filter_summary(filtered_data, filter='mispicked')
```

## Evaluation signals

- filter_summary() output shows expected numbers of ions flagged and merged by mispicked filter (typically 5–15% of input features); check that ion count after filtering is reasonable (>50% of input features retained).
- get_similar_ions() groups show clustered m/z and retention time differences within expected windows (Δm/z < 0.5 Da, ΔRT < 0.005 min) and isotope mass shifts consistent with 1–3 mass units.
- Interactive scatter plot reveals no systematic removal bias: features removed should be scattered across m/z and retention time space, not clustered in specific regions.
- Technical replicate correlation (calculated via filter_cv()) improves post-filtering; correlations between technical replicates should increase after removal of low-cv features.
- Solvent and media blank features are eliminated or reduced to background levels; remaining features in blank samples show relative ion abundance < 0.01 relative to other groups.

## Limitations

- Filter parameters (ringwin, isowin, trwin, max_iso_shift) are optimized for Orbitrap or high-resolution Q-TOF instruments and may require tuning for lower-resolution instruments (e.g., ion trap, triple quadrupole).
- The mispicked-ion filter assumes that isotopic patterns follow expected mass shifts (1–3 Da intervals); non-standard adducts or unusual isotopic ratios may not be detected.
- filter_group() and filter_cv() depend on correct metadata annotation (sample grouping, replicate designation); misannotated replicates or groups will produce incorrect filtering decisions.
- Memory efficiency gains from copy_object=FALSE (reference semantics) mean that filtering operations modify the input object in-place; users must explicitly save intermediate results if iterative exploration is planned.
- The workflow does not address features arising from sample carryover or cross-contamination between non-blank samples; group-based filtering is most effective when blanks are included.

## Evidence

- [readme] The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data.: "The goal of mpactr is to correct for errors that occur during the pre-processing of raw tandem MS/MS data."
- [readme] filter_mispicked_ions() removes mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing.: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
- [abstract] We recommend using the default copy_object = FALSE as this makes for an extremely fast and memory-efficient way to chain mpactr filters together: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [abstract] filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions and passed_ions: "filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the"
- [methods] Detect ions with similar retention time and m/z using specified window and threshold parameters for merge detection: "filter_mispicked_ions with parameters: ringwin, isowin, trwin, max_iso_shift, merge_peaks, merge_method"
- [methods] This data needs to be filtered prior to downstream analyses because of limitations in mass spectrometry detection capabilities.: "This data needs to be filtered prior to downstream analyses because of limitations in mass spectrometry detection capabilities."
