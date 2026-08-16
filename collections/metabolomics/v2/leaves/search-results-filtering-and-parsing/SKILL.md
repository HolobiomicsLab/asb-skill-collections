---
name: search-results-filtering-and-parsing
description: Use when you have loaded DIA mass spectrometry search results containing
  feature identification data with associated Q-value scores, and you need to restrict
  the analytes available in selection drop-downs to those meeting a quality cutoff
  (typically 1% FDR equivalent) before visualization or manual.
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

# search-results-filtering-and-parsing

## Summary

Load mass spectrometry search results (feature identification data with Q-value scores) and filter analytes by a stringent quality threshold to populate hierarchical drop-down selection interfaces in data exploration workflows. This skill ensures that only high-confidence identifications are exposed to downstream visualization and analysis.

## When to use

You have loaded DIA mass spectrometry search results containing feature identification data with associated Q-value scores, and you need to restrict the analytes available in selection drop-downs to those meeting a quality cutoff (typically 1% FDR equivalent) before visualization or manual inspection. Apply this skill when you want to present users with only confident identifications and avoid cluttering the interface with low-confidence features.

## When NOT to use

- Input is already a curated/pre-filtered feature table with no Q-value metadata available — skip to direct lookup indexing.
- Analysis goal requires inspection of low-confidence features (e.g., sensitivity study, decoy validation) — relax or disable the Q-value threshold.
- Downstream tool requires all results regardless of quality (e.g., benchmarking against external gold standard) — apply filtering after that step.

## Inputs

- Search results file containing feature identification data (format: upstream software output, e.g. OpenSwath, DIA-NN)
- Feature Q-value scores (per-feature FDR estimates)
- Analyte metadata: protein identifiers, peptide sequences, charge states

## Outputs

- Filtered analyte collection (passing Q-value ≤ 0.01)
- Hierarchical lookup structure indexed by protein → peptide → charge state
- Populated drop-down selection options for GUI (three-level)
- Retained feature identification records with metadata

## How to apply

First, load the search results file using a format-specific MassDash loader (e.g., ResultsLoader) that parses the upstream software output and retains feature Q-value metadata. Apply a Q-value filter with a threshold of 1% (≤0.01), removing all analytes with Q-value > 1%. For each passing feature, extract the analyte metadata (protein name, peptide sequence, charge state) and build hierarchical lookup structures indexed by protein → peptide → charge state. Return this filtered collection to the GUI layer for dynamic population of the three-level drop-down selection boxes. The rationale is that the 1% Q-value threshold provides a stringent quality gate, balancing sensitivity and specificity for confident analyte identification in interactive exploration.

## Related tools

- **MassDash** (Modular Python package and Streamlit GUI that loads search results, applies Q-value filtering, and exposes filtered analytes via hierarchical drop-down selection) — https://github.com/Roestlab/massdash
- **ResultsLoader** (MassDash format-specific loader that parses feature identification data and Q-value scores from upstream software output) — https://github.com/Roestlab/massdash
- **Streamlit** (Web-based GUI framework used by MassDash to render the three-level drop-down selection interface)

## Evaluation signals

- Verify that all returned analytes have Q-value ≤ 0.01 (no analyte with Q-value > 1% passes the filter).
- Confirm that the hierarchical lookup is non-null and contains at least one protein entry for each passing feature.
- Check that drop-down options are sorted or indexed consistently by protein, then peptide, then charge state (no duplicate entries).
- Validate that the count of filtered analytes is ≤ count of input analytes (monotonic decrease or equality).
- Spot-check a sample of filtered records to ensure metadata (protein name, peptide sequence, charge state) is complete and non-null.

## Limitations

- Q-value threshold (1%) is a fixed cutoff; may be overly stringent for low-abundance analytes or underly stringent for high-variance features. Users may need to adjust the threshold in the sidebar after inspection.
- Filtering depends on accurate Q-value computation from the upstream search engine; errors in Q-value calculation propagate directly.
- Hierarchical indexing assumes unique protein–peptide–charge-state combinations; redundancy or collision in this key space may silently drop or merge analytes.
- No support for post-search re-ranking or machine learning-based rescoring within this filter step; limited to the upstream Q-values.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications: "Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%"
- [other] Load search results file containing feature identification data and associated Q-value scores using massdash loaders: "Load search results file containing feature identification data and associated Q-value scores using massdash loaders (e.g., ResultsLoader or format-specific loader matching the upstream software)"
- [other] Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures: "Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
