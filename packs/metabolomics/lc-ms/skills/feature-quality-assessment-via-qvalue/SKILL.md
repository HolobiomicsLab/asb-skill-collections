---
name: feature-quality-assessment-via-qvalue
description: Use when you have loaded search results from an upstream proteomics database search (e.g., OpenSwath, DIA-NN) containing feature identification data with Q-value scores, and you need to populate analyte dropdown menus or restrict downstream analysis to only statistically confident identifications.
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
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- ResultsLoader
- MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-quality-assessment-via-qvalue

## Summary

Filter Data-Independent Acquisition mass spectrometry search results to retain only high-confidence peptide/protein identifications by applying a stringent Q-value threshold (≤1%), removing lower-confidence analytes from downstream selection and analysis. This quality gate restricts the analyte pool available for visualization and peak picking to meet statistical rigor standards.

## When to use

Apply this skill when you have loaded search results from an upstream proteomics database search (e.g., OpenSwath, DIA-NN) containing feature identification data with Q-value scores, and you need to populate analyte dropdown menus or restrict downstream analysis to only statistically confident identifications. Use it before building hierarchical lookup structures for multi-level selection interfaces or before applying visualization and peak-picking workflows.

## When NOT to use

- Search results file is missing Q-value scores or equivalent confidence metrics — the filter cannot operate without statistical rigor measures.
- Downstream analysis explicitly requires low-confidence identifications for sensitivity studies or exploratory proteomics in poorly-characterized organisms.
- Input data has already been pre-filtered by the upstream search engine at a different Q-value threshold; re-applying this skill may unnecessarily restrict analyte pools or conflict with prior filtering decisions.

## Inputs

- search results file (output from proteomics database search engine with feature identifications and Q-value scores)
- Q-value threshold parameter (default: 0.01 for 1% FDR cutoff)

## Outputs

- filtered analyte collection indexed by protein, peptide sequence, and charge state
- hierarchical lookup structures for three-level dropdown selection interface
- high-confidence feature metadata (protein, peptide, charge state) passing Q-value cutoff

## How to apply

Load search results containing feature identification data and associated Q-value scores using a format-specific loader (e.g., ResultsLoader or MassDash loaders matching the upstream search engine output). Apply a Q-value filter with a threshold of 1% (≤0.01), which removes all analytes with Q-value > 0.01, retaining only the high-confidence subset. For each passing feature, extract analyte metadata (protein, peptide sequence, charge state) and build hierarchical lookup structures indexed by protein → peptide → charge state. Return the filtered analyte collection for dynamic population of GUI selection boxes or for downstream peak-picking and visualization. The 1% threshold reflects a widely-adopted standard for false discovery rate control in proteomics; stricter thresholds (e.g., 0.1%) may be appropriate for high-stakes studies but will reduce the available analyte pool.

## Related tools

- **MassDash** (host application that implements Q-value filtering for analyte selection and provides ResultsLoader to ingest search results) — https://github.com/Roestlab/massdash
- **ResultsLoader** (MassDash module that loads search results files and extracts feature identification data with Q-value scores) — https://github.com/Roestlab/massdash
- **Streamlit** (GUI framework for rendering filtered dropdown selection boxes and interactive analyte selection interface)

## Evaluation signals

- All returned analytes have Q-value ≤ 0.01 (1%); spot-check the filtered collection to confirm no analytes exceed the threshold.
- Hierarchical lookup structure is correctly indexed: protein → peptide → charge state; verify structure can be queried at each level.
- Dropdown menus in the GUI display only the filtered analyte set; verify menu population reflects the filtered collection, not the full unfiltered input.
- Record the number of analytes passing the filter versus total input analytes; document the retention rate to assess filtering stringency.
- Downstream visualization and peak-picking workflows operate only on analytes from the filtered collection; confirm no unfiltered analytes are inadvertently processed.

## Limitations

- The 1% Q-value threshold is a fixed standard; some high-throughput or exploratory studies may require adjustment, but the article does not describe dynamic threshold tuning.
- Q-value calculations depend on correct implementation in the upstream search engine; errors in score computation or multiple-testing correction will propagate into the filtered results.
- Filtering is applied uniformly to all analytes regardless of protein class, peptide length, or charge state; no stratified or conditional filtering strategies are described.
- MassDash provides settings to control results at a specified Q-value cutoff in the sidebar, but the mechanism for non-standard thresholds is not detailed in the provided context.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%.: "Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%."
- [other] Load search results file containing feature identification data and associated Q-value scores using massdash loaders: "Load search results file containing feature identification data and associated Q-value scores using massdash loaders (e.g., ResultsLoader or format-specific loader matching the upstream software)"
- [other] Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures: "Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface."
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
