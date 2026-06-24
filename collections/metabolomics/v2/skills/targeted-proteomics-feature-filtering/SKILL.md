---
name: targeted-proteomics-feature-filtering
description: Use when you have loaded transition group chromatogram data from sqMass
  files and need to restrict the analyte selection dropdowns (protein, peptide, charge
  state) to only those features passing a specified Q-value threshold (default 1%),
  or when you need to selectively display or hide MS1 and MS2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SqMassLoader
  - massdash.plotting.InteractivePlotter
  - massdash.peakPickers.MRMTransitionGroupPicker
  - massdash.peakPickers.pyMRMTransitionGroupPicker
  - massdash.structs.FeatureMap
  - massdash.loaders.ResultsLoader
  - Bokeh
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- 'Chromatogram Loaders: Raw data stores chromatograms, this allows for faster loading
  however since extraction has already been performed by the upstream analysis tool.
  This includes SqMassLoader'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Targeted Proteomics Feature Filtering

## Summary

Filter extracted ion chromatogram (XIC) features by statistical quality thresholds (Q-value) and trace type to isolate high-confidence peptide identifications for visualization and peak boundary analysis in DIA mass spectrometry workflows. This skill enables selective display of analytes meeting user-defined confidence cutoffs, reducing noise and focusing downstream analysis on validated results.

## When to use

Apply this skill when you have loaded transition group chromatogram data from sqMass files and need to restrict the analyte selection dropdowns (protein, peptide, charge state) to only those features passing a specified Q-value threshold (default 1%), or when you need to selectively display or hide MS1 and MS2 traces to isolate specific mass spectrometry data types for visualization or peak picking.

## When NOT to use

- Input data are already collapsed into a consensus feature table or have been pre-filtered upstream; re-filtering introduces redundancy and may lose resolution.
- Q-value calculations are absent or unreliable in the input metadata; filtering on incomplete or uncalibrated scores will produce misleading analyte selections.
- The analysis goal is exploratory discovery of novel or low-confidence features; a strict Q-value cutoff (1%) may exclude valuable weak signals.

## Inputs

- sqMass file containing pre-extracted transition group chromatograms
- Feature metadata table (retention time, intensity, Q-value per analyte)
- Q-value threshold parameter (float, default 0.01)
- Trace filter settings (MS1 enabled/disabled, MS2 enabled/disabled)

## Outputs

- Filtered analyte selection dropdowns (protein, peptide, charge state)
- Filtered chromatogram dataset (subset of input)
- Interactive Bokeh figure with only filtered traces rendered
- Legend entries and hover metadata for filtered traces only

## How to apply

Initialize the XIC workflow by loading transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values) from sqMass files via SqMassLoader. Apply a Q-value filter at a user-defined significance level (typically 1% false discovery rate); only features with Q-values below this threshold are populated in the analyte selection dropdowns. Optionally apply secondary trace-type filters to display or hide MS1 and MS2 traces independently. After filtering, configure the InteractivePlotter to render only the filtered chromatogram traces in Bokeh figures. Verify filtering success by checking that the dropdown menus contain only expected analytes and that the rendered traces match the selected filter parameters.

## Related tools

- **SqMassLoader** (Loads transition group chromatogram data and feature metadata from sqMass files) — https://github.com/Roestlab/massdash
- **massdash.plotting.InteractivePlotter** (Renders filtered chromatogram traces as interactive Bokeh figures after Q-value and trace-type filtering) — https://github.com/Roestlab/massdash
- **Bokeh** (Provides interactive visualization toolkit for chromatogram plots with filtering-aware legend and hover metadata)
- **massdash.structs.FeatureMap** (Data structure holding retention time, intensity, Q-value, and MS1/MS2 trace assignments for filtering operations) — https://github.com/Roestlab/massdash
- **massdash.loaders.ResultsLoader** (Loads search result files containing feature identification results and Q-value assignments) — https://github.com/Roestlab/massdash

## Examples

```
# Load XIC data, filter by Q-value, and render filtered chromatogram
from massdash.loaders import SqMassLoader
from massdash.plotting import InteractivePlotter
loader = SqMassLoader('data.sqMass')
feature_map = loader.load()
filtered_map = feature_map.filter_by_qvalue(qvalue_threshold=0.01)
plotter = InteractivePlotter(filtered_map, ms1_enabled=True, ms2_enabled=True)
fig = plotter.plot()
fig.show()
```

## Evaluation signals

- Analyte dropdown menus contain only features with Q-value ≤ the specified threshold (default 1%); no features above the cutoff are visible.
- Rendered Bokeh figure displays only the chromatogram traces corresponding to filtered analytes; traces from filtered-out features are absent from the plot.
- Interactive legend correctly reflects the filtered trace set; muting/unmuting traces works only on the subset of traces that passed filtering.
- Hover metadata on chromatogram peaks displays correct apex retention time, apex intensity, and Q-value for each filtered feature, consistent with input metadata.
- MS1/MS2 trace filter toggles correctly show or hide the corresponding trace type; toggling MS1 off removes all singly-charged precursor traces while MS2 traces remain visible.

## Limitations

- Q-value calculation reliability depends on search engine calibration and the representative nature of the decoy database; poorly calibrated Q-values lead to over- or under-filtering.
- Fixed threshold (1% default) may be inappropriately stringent or permissive for datasets with extreme peptide abundance ranges or for exploratory analyses where low-confidence hits have biological relevance.
- Filtering is applied only to analyte selection UI; peak boundary overlay (from OpenSwath or on-the-fly peak picking) is not automatically filtered and may display for features below the Q-value threshold if explicitly requested.
- Trace smoothing is applied after filtering; smoothed traces from filtered-out analytes are not visualized, but smoothing parameters are not re-optimized for the filtered subset.

## Evidence

- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns (protein, peptide, charge state).: "Filter analytes by Q-value threshold (default 1%) and populate analyte selection dropdowns"
- [other] Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings in plotting controls.: "Apply optional trace smoothing and MS1/MS2 trace filtering based on user settings"
- [other] Load transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values).: "Load transition group chromatogram data and associated feature metadata (retention time, intensity, Q-values)"
- [other] The sidebar provides settings to control results at a specified Q-value cutoff: "The sidebar provides settings to control results at a specified Q-value cutoff"
