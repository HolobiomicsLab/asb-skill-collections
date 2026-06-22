---
name: q-value-based-confidence-filtering
description: Use when after loading feature identification results (e.g., from OpenSwath or other DIA search engines) when you need to display only confident peptide precursors and their chromatograms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SqMassLoader
  - massdash.plotting.InteractivePlotter
  - massdash.peakPickers.MRMTransitionGroupPicker
  - massdash.peakPickers.pyMRMTransitionGroupPicker
  - massdash.structs.FeatureMap
  - massdash.loaders.ResultsLoader
  - Streamlit
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- 'Chromatogram Loaders: Raw data stores chromatograms, this allows for faster loading however since extraction has already been performed by the upstream analysis tool. This includes SqMassLoader'
- InteractivePlotter
- MRMTransitionGroupPicker
- pyMRMTransitionGroupPicker
- FeatureMap
- ResultsLoader
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

# q-value-based-confidence-filtering

## Summary

Filter feature identification results by q-value threshold to retain only high-confidence peptide identifications in DIA mass spectrometry data. This skill controls false discovery rate and populates analyte selection interfaces with only statistically validated features.

## When to use

Apply this skill after loading feature identification results (e.g., from OpenSwath or other DIA search engines) when you need to display only confident peptide precursors and their chromatograms. Use it when the input feature table contains mixed-confidence hits and you want to exclude low-confidence identifications (typically those with q-value ≥ 1%) before visualization or downstream analysis.

## When NOT to use

- Input feature table is already pre-filtered to a single confidence level (filtering is redundant).
- Analysis requires visualization of all features regardless of statistical confidence (e.g., exploratory inspection of low-confidence hits).
- Q-value scores are not available or not computed by the search engine (threshold cannot be applied).

## Inputs

- Feature identification results with q-value scores (FeatureMap or ResultsLoader output)
- Raw DIA mass spectrometry data file or directory
- Transition group metadata (protein, peptide, charge state, retention time, intensity)

## Outputs

- Filtered analyte list (protein, peptide, charge state tuples meeting q-value threshold)
- Filtered transition group chromatogram dataset
- Populated analyte selection dropdowns in UI
- Interactive Bokeh chromatogram figures with only confident features

## How to apply

Load feature metadata containing q-value scores from search results (e.g., via ResultsLoader or FeatureMap structures). Apply a q-value threshold cutoff—the article and massdash codebase use 1% as default—to filter the analyte population before populating dropdown menus for protein, peptide, and charge state selection. This filtering step occurs after feature loading but before rendering interactive visualizations, ensuring only statistically validated features appear in the user interface. The q-value threshold is configurable in the sidebar plotting controls, allowing users to experiment with stricter or more permissive cutoffs. Verify filtering success by confirming that the number of selectable analytes matches the count of features passing the q-value threshold and that hover metadata (Q-value, apex intensity, retention time) on rendered chromatograms shows no values exceeding the threshold.

## Related tools

- **massdash.loaders.ResultsLoader** (Loads feature identification results including q-value scores from search output files) — https://github.com/Roestlab/massdash
- **massdash.structs.FeatureMap** (Data structure that holds analyte metadata (q-values, retention times, intensities) used for filtering and selection) — https://github.com/Roestlab/massdash
- **massdash.plotting.InteractivePlotter** (Renders filtered analyte data as interactive Bokeh figures after q-value filtering is applied) — https://github.com/Roestlab/massdash
- **Streamlit** (GUI framework that exposes q-value threshold control in sidebar and populates filtered analyte dropdown menus)

## Evaluation signals

- Number of selectable analytes in dropdown menus equals count of features with q-value ≤ threshold
- All rendered chromatogram traces and hover metadata show q-values ≤ the applied threshold
- Changing the threshold value in the sidebar updates the analyte list and removes/restores features as expected
- Features with q-value > threshold do not appear in any visualization or dropdown selection
- Peak metadata (apex retention time, apex intensity, Q-value) displayed on hover conforms to the threshold constraint

## Limitations

- Q-value calculation depends on the accuracy and calibration of the upstream search engine; biased or incorrectly calibrated q-values will produce misleading filtered results.
- Default 1% q-value threshold may be too permissive for very large feature tables or too strict for sparse data; no guidance provided in the article for threshold selection on a per-dataset basis.
- Filtering is applied globally to all analytes; the article does not describe per-peptide, per-protein, or per-charge-state conditional thresholds.
- Q-value filtering alone does not account for other quality metrics (e.g., retention time prediction error, isotope pattern quality) that might also warrant exclusion.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
- [other] Load search results — the file path for search result files containing feature identification results: "the file path for search result files containing feature identification results"
- [other] Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state): "Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns"
