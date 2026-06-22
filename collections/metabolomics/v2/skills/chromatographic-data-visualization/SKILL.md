---
name: chromatographic-data-visualization
description: Use when after peak detection has been completed and a feature table has been generated in MetCohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  tools:
  - MetCohort
derived_from:
- doi: 10.1021/acs.analchem.4c04906
  title: MetCohort
evidence_spans:
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data processing tool for large-scale metabolomics and exposomics
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data processing tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metcohort_cq
    doi: 10.1021/acs.analchem.4c04906
    title: MetCohort
  dedup_kept_from: coll_metcohort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04906
  all_source_dois:
  - 10.1021/acs.analchem.4c04906
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-data-visualization

## Summary

Visualization of detected features and their chromatographic profiles in LC-MS metabolomics data, enabling quality assessment of peak detection and integration results. This skill validates feature detection output by plotting retention time traces, m/z profiles, and integration boundaries across the sample cohort.

## When to use

After peak detection has been completed and a feature table has been generated in MetCohort. Use this skill when you need to inspect detected features for accuracy, verify integration boundaries are correctly placed around true peaks, identify problematic features or files with poor peak picking, and confirm that retention time alignment has been successful before exporting results for downstream annotation.

## When NOT to use

- Input data has not yet undergone peak detection — visualize only after feature detection is complete
- Raw, uncorrected LC-MS data — retention time alignment must be performed first for meaningful chromatographic visualization
- Feature table is from a different tool or pipeline not integrated with MetCohort — visualization assumes MetCohort's internal data structures and ROI matrix

## Inputs

- Feature table with detected peaks (retention time, m/z, intensity values)
- Aligned LC-MS data (mzML or netCDF format, post-correction)
- Peak detection results and integration boundaries

## Outputs

- Extracted ion chromatogram (XIC) plots for selected features across samples
- Retention time deviation plot (HTML) showing alignment quality per file
- Visual confirmation of integration regions and peak boundaries
- Quality assessment report identifying problematic features or samples

## How to apply

Load the feature table generated after MetCohort's peak detection stage into the View Results interface. Select individual features from the feature table to display their extracted ion chromatograms (XICs) across samples; MetCohort displays chromatograms for up to 50 randomly selected files to conserve memory. Examine the shaded integration region for each feature to verify it correctly spans the peak apex and excludes noise or neighboring peaks. Inspect retention time consistency across samples post-alignment by observing whether peak positions cluster tightly; large deviations suggest alignment problems. Export the retention time deviation plot (HTML) from the data alignment stage to identify and flag abnormal files with extreme retention time shifts. Use these visualizations to decide whether to adjust feature detection parameters (e.g., entropy coefficient, intensity threshold, delta m/z) and reprocess, or proceed to export the feature table.

## Related tools

- **MetCohort** (Performs peak detection, generates feature table, and provides integrated visualization interface for chromatographic data and integration results) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Integration regions (shaded areas) visually align with true peak apexes; no regions extend into noise or adjacent peaks
- Retention time deviation plot shows peak positions clustered within ±5–10 s around reference file, with no file exhibiting extreme outlier deviations
- Peak profiles across samples display similar chromatographic width and shape, indicating successful retention time alignment
- Feature intensity and m/z values remain stable across samples for genuine features; spurious features show erratic or near-zero intensities
- Abnormal files identified in deviation plot can be cross-checked against TIC (total ion chromatogram) for data quality issues (e.g., noise, baseline instability)

## Limitations

- Visualization is limited to up to 50 randomly sampled files to manage memory; large cohorts may not show complete picture of feature consistency
- Visual inspection is subjective; systematic outlier detection requires manual examination of retention time deviation plot or external quality control scripts
- Poor data alignment upstream significantly degrades feature visualization quality and can mask true features or create false positives, requiring re-alignment with adjusted parameters
- Visualization does not quantify feature quality metrics (e.g., false positive/negative rates); relies on manual judgment combined with parameter tuning

## Evidence

- [intro] Finally, feature detection results are visualized in the software and can be saved for subsequent analysis.: "Finally, feature detection results are visualized in the software and can be saved for subsequent analysis."
- [readme] After the feature detection stage, users can view the results on the View results page of the window. When a feature is selected in the feature table, its chromatograms are displayed. To conserve memory usage, chromatograms for a random selection of up to 50 files are shown. The shaded region in the chromatograms represents the integration region of the feature.: "When a feature is selected in the feature table, its chromatograms are displayed. To conserve memory usage, chromatograms for a random selection of up to 50 files are shown. The shaded region in the"
- [readme] Users are encouraged to export the plot of retention time deviation during the data alignment stage. The plot of retention time deviation will be included the exported file directory as an HTML file.: "Users are encouraged to export the plot of retention time deviation during the data alignment stage. The plot of retention time deviation will be included the exported file directory as an HTML file."
- [readme] We can check the effectiveness of data alignment from the retention time deviation plot. If the time deviation does not correspond to the actual retention time shift along the time axis, the data are not well aligned.: "We can check the effectiveness of data alignment from the retention time deviation plot. If the time deviation does not correspond to the actual retention time shift along the time axis, the data are"
- [readme] Inspecting the deviation plot can help identify abnormal files. In most cases, the retention time deviation is near 0 or exhibits a regular fluctuation.: "Inspecting the deviation plot can help identify abnormal files. In most cases, the retention time deviation is near 0 or exhibits a regular fluctuation."
