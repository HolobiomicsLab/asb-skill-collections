---
name: drop-down-interface-population-from-filtered-data
description: Use when you have search results from DIA mass spectrometry data containing
  feature Q-value scores and need to restrict the analyte choices available to users
  in a GUI to only those meeting a 1% feature Q-value threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResultsLoader
  - MassDash
  - Streamlit
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- ResultsLoader
- MassDash is a modular and flexible python package that has a streamlit graphical
  user interface (GUI)
- ':mod:`massdash.loaders`: Classes for loading data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# drop-down-interface-population-from-filtered-data

## Summary

Populate hierarchical drop-down selection boxes in a mass spectrometry visualization dashboard by loading search results, applying a stringent Q-value quality filter (≤1%), and extracting and indexing analyte metadata (protein, peptide sequence, charge state) to enable constrained selection of high-confidence identifications.

## When to use

You have search results from DIA mass spectrometry data containing feature Q-value scores and need to restrict the analyte choices available to users in a GUI to only those meeting a 1% feature Q-value threshold. This is appropriate when building an interactive selection interface where false identifications must be excluded to prevent downstream analysis on low-confidence features.

## When NOT to use

- Search results already contain only pre-filtered high-confidence features (filtering would be redundant and risk over-restricting the analyte space).
- User analysis workflow requires visualization of low-confidence identifications for diagnostic or quality-control purposes (the 1% threshold would hide potentially informative lower-confidence hits).
- Drop-down interface is not part of the workflow; analytes are selected programmatically or through other means that do not require hierarchical GUI selection.

## Inputs

- Search results file containing feature identification data with Q-value scores (format-specific to upstream DIA software, e.g. OpenSwath output)
- MassDash ResultsLoader or compatible format-specific loader

## Outputs

- Filtered analyte collection indexed by protein, peptide, and charge state
- Hierarchical lookup structure suitable for dynamic population of three-level drop-down selection interface
- Set of high-confidence analytes meeting 1% Q-value cutoff

## How to apply

Load search results using a MassDash format-specific loader (e.g., ResultsLoader) that parses feature identification data and associated Q-value scores. Apply a Q-value filter with a threshold of ≤0.01 (1%), removing all analytes with Q-value > 1% to retain only high-confidence identifications. Extract analyte metadata—protein identifier, peptide sequence, and precursor charge state—from each passing feature. Build a hierarchical lookup structure indexed by protein→peptide→charge state that can be efficiently queried by the GUI. Return this indexed analyte collection to dynamically populate the three-level drop-down selection boxes. Verify filtering correctness by spot-checking that all retained analytes have Q-value ≤0.01 and that the resulting dropdown contents match expected analyte counts at each hierarchical level.

## Related tools

- **MassDash** (Python package providing loaders, filtering infrastructure, and GUI framework (Streamlit) for populating and rendering hierarchical drop-down selection boxes) — https://github.com/Roestlab/massdash
- **ResultsLoader** (MassDash loader module that parses search results files and extracts feature identification data and Q-value scores for filtering) — https://github.com/Roestlab/massdash
- **Streamlit** (Web framework used by MassDash to render interactive drop-down selection components in the GUI)

## Evaluation signals

- All retained analytes have Q-value ≤ 0.01; no analyte with Q-value > 0.01 appears in the filtered collection.
- Drop-down contents at each hierarchical level (protein, peptide, charge state) match expected analyte counts after filtering; spot-check a sample of proteins to verify peptide and charge state subsets are complete and correct.
- Lookup index is queryable and returns correct sublists when traversing the hierarchy (e.g., selecting a protein returns all peptides for that protein; selecting a peptide returns all charge states for that peptide).
- GUI drop-down boxes populate correctly without errors; no missing or duplicate analyte entries in any selection tier.
- Comparison of pre-filter and post-filter analyte counts confirms that the number of retained analytes is less than or equal to the starting count, with no negative or anomalous values.

## Limitations

- The 1% Q-value threshold is fixed in MassDash; if a different stringency is required, configuration or code modification is needed. The article does not describe a user-configurable Q-value parameter for the drop-down interface population step.
- Filtering applies only to analytes populated in the selection interface; it does not affect other visualizations or analyses that may display lower-confidence features via other MassDash panels.
- If search results lack Q-value information or use a non-standard Q-value encoding, the loader may fail to parse the file or produce incorrect filtering; compatibility with the upstream DIA software format is assumed.
- The hierarchical structure (protein→peptide→charge) may become inefficient for very large analyte sets (e.g., >10,000 unique proteins), potentially affecting GUI responsiveness.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%.: "Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%"
- [other] Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface.: "Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface"
- [other] Return filtered analyte collection indexed by protein, peptide, and charge state for dynamic population of the GUI selection boxes.: "Return filtered analyte collection indexed by protein, peptide, and charge state for dynamic population of the GUI selection boxes"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
- [other] Load search results file containing feature identification data and associated Q-value scores using massdash loaders (e.g., ResultsLoader or format-specific loader matching the upstream software).: "Load search results file containing feature identification data and associated Q-value scores using massdash loaders (e.g., ResultsLoader or format-specific loader matching the upstream software)"
