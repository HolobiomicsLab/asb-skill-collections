---
name: peak-detection-in-lcms-data
description: Use when after retention-time correction has been completed on centroided LC-MS data (mzML or mzXML format) and you need to identify all detected peaks as a unified feature table across a cohort of samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MetCohort
  techniques:
  - LC-MS
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

# peak-detection-in-lcms-data

## Summary

Automated identification of chromatographic peaks across retention-time-corrected LC-MS samples to construct a feature table with m/z, retention time, and intensity values. This skill detects individual metabolic features for downstream annotation and statistical analysis in untargeted metabolomics workflows.

## When to use

Apply this skill after retention-time correction has been completed on centroided LC-MS data (mzML or mzXML format) and you need to identify all detected peaks as a unified feature table across a cohort of samples. Requires at least one quality control (QC) file to have been designated during data import and alignment.

## When NOT to use

- Input is already a feature table or integrated peak list — peak detection has already been performed.
- Raw data has not undergone retention-time correction or data alignment — peak detection requires aligned ROI matrices.
- No centroided LC-MS data available — peak detection expects centroid spectrum format, not profile mode.

## Inputs

- Retention-time-corrected LC-MS raw data (mzML or mzXML format)
- Designation of at least one quality control (QC) file
- Optional: targeted extraction table (xlsx format) for targeted peak detection

## Outputs

- Feature table with m/z, retention time, and intensity values
- Feature detection results in tabular format (CSV or mzTab)
- Chromatogram visualizations per detected feature
- Feature data export (xlsx or internal .pkd format for session persistence)

## How to apply

Peak detection operates on aligned raw data within a Regions of Interest (ROI) matrix constructed from QC file signals. Set the m/z deviation tolerance (delta m/z, default 0.01) to control mass resolution; use minimum continuous non-zero points (default 3, increase for high-noise small-scale experiments) and maximum peak width (default 15 seconds) to filter noise and resolve coelution. Specify the minimum number of non-zero peaks across samples (default 80%) to avoid spurious features, and set intensity threshold (default 50) to exclude low-abundance noise. Select a reference QC file to represent feature apex retention time and m/z. Use the entropy coefficient (default 0.8, lower for large-scale studies) to control feature scoring stringency. Peak detection integrates centWave-based ROI detection with dynamic boundary identification to achieve low false positive and false negative rates simultaneously.

## Related tools

- **MetCohort** (Integrated LC-MS data processing platform that executes peak detection using a robust centWave-based algorithm with ROI matrix construction and dynamic boundary identification for low false positive/negative rates) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Feature table contains no missing m/z, retention time, or intensity values for detected peaks across all samples.
- Feature intensity values fall within the specified minimum intensity threshold (default ≥50) and non-zero peaks meet the minimum sample requirement (default ≥80% of samples).
- Retention time and m/z of each feature match the apex position in the reference QC file used for feature representation.
- Chromatogram visualizations show detected peaks falling within the maximum peak width constraint (default ≤15 seconds) with shaded integration regions aligned to the specified ROI boundaries.
- Feature table can be exported and re-imported (.pkd format) without data loss, and export to xlsx format is valid and complete.

## Limitations

- Peak detection quality depends critically on data alignment quality; poor retention-time alignment reduces feature identification and integration accuracy (confirmed by comparison of alignment deviation plots).
- For small-scale sample analyses with few QC files, increasing minimum continuous non-zero points is necessary to reduce noise-driven false features.
- Isomeric and coeluting compounds may have reduced detection accuracy in untargeted mode; targeted extraction table can improve specificity but with trade-off in integration precision.
- Abnormal files with noisy or significantly different chromatographic conditions may cause LOWESS fitting warnings and incorrect local matching; manual inspection of retention-time deviation plots is required for large-scale studies.
- Feature representation (retention time and m/z) is fixed to the selected reference QC file; changing the reference file changes feature representation and may complicate inter-table feature matching.

## Evidence

- [other] Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis.: "Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis."
- [intro] With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously. Feature table of high quality is generated: "With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously. Feature table of high quality is generated"
- [readme] At least one file need to be specified as quality control (QC) file. Then data correction and peak detection should be performed in order.: "At least one file need to be specified as quality control (QC) file. Then data correction and peak detection should be performed in order."
- [readme] Delta m/z: Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01.: "Delta m/z: Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01."
- [readme] Minimum number of continuous non-zero points: Allowed minimum number of continuous non-zero points in the process of ROI detection with centWave algorithm. Default value is 3. In small-scale sample processing with a few QC files, the value should be increased to decrease noise.: "Minimum number of continuous non-zero points in the process of ROI detection with centWave algorithm. Default value is 3. In small-scale sample processing with a few QC files, the value should be"
- [readme] Maximum width of peak: Allowed maximum chromatographic width of detected features. Default value is 15 seconds.: "Maximum width of peak: Allowed maximum chromatographic width of detected features. Default value is 15 seconds."
- [readme] Minimum intensity of a feature: Allowed minimum intensity of a feature. If the maximum height of a feature in all the samples is lower than the value, the feature is filtered. Default value is 50.: "Minimum intensity of a feature: Allowed minimum intensity of a feature. If the maximum height of a feature in all the samples is lower than the value, the feature is filtered. Default value is 50."
- [readme] The retention time and m/z of one feature is represented by the retention time and m/z of the apex of the peak in the reference file.: "The retention time and m/z of one feature is represented by the retention time and m/z of the apex of the peak in the reference file."
- [readme] Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The default value is set to 0.8. For large-scale sample processing, users are advised to adjust this value lower.: "Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The"
- [readme] The quality of the alignment can significantly influence feature detection and integration. Therefore, it is necessary to manually inspect the alignment results during processing.: "The quality of the alignment can significantly influence feature detection and integration. Therefore, it is necessary to manually inspect the alignment results during processing."
- [readme] Good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration.: "Good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration."
