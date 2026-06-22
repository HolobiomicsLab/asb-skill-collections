---
name: confidence-score-thresholding-in-proteomics
description: Use when when loading search results from Data-Independent Acquisition (DIA) mass spectrometry workflows (e.g., output from OpenSwath or similar feature detection tools) and you need to restrict the analyte pool to those meeting a strict false-discovery rate (FDR) threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResultsLoader
  - MassDash
  - OpenSwath
  techniques:
  - tandem-MS
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

# Confidence-Score Thresholding in Proteomics

## Summary

Apply a stringent Q-value cutoff (typically ≤1%) to filter feature identifications in mass spectrometry search results, retaining only high-confidence analytes for downstream visualization and analysis. This skill ensures that only statistically robust peptide and protein identifications populate selection interfaces and analysis workflows.

## When to use

When loading search results from Data-Independent Acquisition (DIA) mass spectrometry workflows (e.g., output from OpenSwath or similar feature detection tools) and you need to restrict the analyte pool to those meeting a strict false-discovery rate (FDR) threshold. Apply this skill when populating drop-down selection boxes in interactive dashboards or when filtering feature lists prior to peak picking, chromatogram extraction, or quantitation to ensure only statistically justified identifications are analyzed.

## When NOT to use

- Input data are already pre-filtered to a stringent Q-value cutoff or contain only high-confidence identifications; applying an additional 1% threshold may over-filter and leave no analytes available.
- The analysis requires retention of lower-confidence identifications for exploratory or validation purposes (e.g., hypothesis generation or assay development); a 1% cutoff is too restrictive.
- Input file lacks Q-value or confidence score columns; the filter cannot be applied without this metadata.

## Inputs

- Search results file containing feature identifications and Q-value scores (e.g., output from OpenSwath, DIA-MS search software)
- Q-value threshold parameter (default 0.01 or 1%)
- Analyte metadata fields: protein identifier, peptide sequence, precursor charge state

## Outputs

- Filtered analyte collection indexed hierarchically by protein → peptide → charge state
- Populated drop-down selection boxes (GUI) or analyte lookup table (programmatic interface)
- Optional: count or ratio of analytes passing vs. rejected by Q-value filter

## How to apply

Load search results file containing feature identification data and associated Q-value scores using a format-appropriate loader (e.g., ResultsLoader in MassDash). Apply a Q-value filter with a threshold of 1% (≤0.01), removing all analytes with Q-value > 1%. Extract analyte metadata (protein name, peptide sequence, charge state) for each passing feature and construct hierarchical lookup structures indexed by protein, then peptide, then charge state. Return the filtered analyte collection for dynamic population of GUI selection interfaces or downstream computational workflows. The 1% threshold balances stringent quality control against practical analyte availability; adjust upward (e.g., to 5%) only if the filtered pool becomes too sparse for the intended analysis.

## Related tools

- **MassDash** (Provides ResultsLoader and hierarchical GUI selection interface; applies Q-value filter at load time to populate drop-down analyte lists) — https://github.com/Roestlab/massdash
- **ResultsLoader** (Parses search results file and extracts feature identification data and Q-values for filtering) — https://github.com/Roestlab/massdash
- **OpenSwath** (Upstream DIA feature detection and scoring tool; produces search results with Q-value scores consumed by this filter)

## Examples

```
# Using MassDash Python API to filter search results by Q-value
from massdash import ResultsLoader
results = ResultsLoader('search_results.tsv')
filtered_analytes = results.filter_by_qvalue(threshold=0.01)
analyte_dict = filtered_analytes.to_hierarchical_dict()  # protein → peptide → charge
```

## Evaluation signals

- Analyte count after filtering is ≤ count before filtering; rejected analytes all have Q-value > 0.01.
- All analytes in the filtered output have Q-value ≤ 0.01; no analytes with Q-value > 0.01 remain.
- Drop-down selection boxes contain only analytes from the filtered pool; users cannot select any analyte with Q-value > 1%.
- Hierarchical lookup structure is correctly indexed: protein → peptide → charge state; no missing or malformed entries.
- Filter operation completes without errors or warnings; log or console output confirms threshold applied (e.g., 'Filtered 1000 analytes to 250 passing Q-value ≤ 0.01').

## Limitations

- The 1% Q-value threshold is a fixed default; datasets with sparse high-confidence identifications or very lenient search parameters may result in few or zero analytes passing the filter. Practitioners may need to adjust the threshold upward or investigate upstream search calibration.
- Q-value filtering assumes the search results file includes a Q-value or FDR column. If Q-values are missing or malformed, the filter will fail or skip filtering silently; robust error handling is required.
- This skill filters at the feature level (peptide precursor + charge) and does not account for protein-level FDR or multi-peptide inference; a high-confidence feature may belong to an ambiguous protein group. Complementary protein-level validation is recommended for high-stakes analyses.
- The threshold does not account for dataset-specific characteristics (e.g., MS instrument type, sample complexity, search software parameterization); a 1% cutoff may be too strict or too lenient depending on context.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%: "Apply Q-value filter with threshold of 1% (≤0.01) to retain only high-confidence identifications, removing all analytes with Q-value > 1%"
- [other] Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures: "Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface"
- [other] Load search results file containing feature identification data and associated Q-value scores using massdash loaders: "Load search results file containing feature identification data and associated Q-value scores using massdash loaders (e.g., ResultsLoader or format-specific loader matching the upstream software)"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
