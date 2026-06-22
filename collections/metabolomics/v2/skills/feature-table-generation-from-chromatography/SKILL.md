---
name: feature-table-generation-from-chromatography
description: Use when after retention-time correction and alignment of centroided mzML or mzXML LC-MS files across a sample cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
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
---

# feature-table-generation-from-chromatography

## Summary

Peak detection on retention-time-corrected LC-MS data to generate a quantitative feature table with retention time, m/z, and intensity values for each detected metabolite feature across all samples. This is a critical downstream step after data alignment that produces the input matrix for metabolite annotation and statistical analysis.

## When to use

After retention-time correction and alignment of centroided mzML or mzXML LC-MS files across a sample cohort. Apply this skill when you have aligned raw data and need to identify and integrate chromatographic peaks into a unified feature matrix with consistent m/z and retention time coordinates across all samples.

## When NOT to use

- Input data is already a feature table or intensity matrix — this skill is for peak detection, not re-processing existing feature tables.
- Raw LC-MS data has not yet been retention-time corrected or aligned — apply data correction/alignment before feature detection.
- Raw data files are not centroided or are in non-standard formats (MetCohort requires centroided mzML or mzXML).

## Inputs

- Retention-time-corrected LC-MS data in mzML or mzXML format
- At least one quality control (QC) file designated for reference

## Outputs

- Feature table in CSV or mzTab tabular format containing retention time, m/z, and intensity for each feature across all samples
- Optional: Feature table in xlsx or proprietary .pkd format for visualization and import/export within MetCohort

## How to apply

Load the RT-corrected LC-MS data into MetCohort and configure feature detection parameters based on your chromatographic conditions and sample size. Select a reference QC file to define feature m/z and retention time coordinates. Configure the centWave algorithm parameters: set 'minimum number of continuous non-zero points' (default 3, increase for small sample sets to reduce noise), 'maximum number of continuous zero points' (default 10, controls ROI time length), 'delta m/z' for ROI detection (default 0.01, can be narrowed post-alignment), and 'maximum width of peak' (default 15 seconds). Set 'minimum number of non-zero peaks in a feature' to 80% by default to filter features present in most samples. Adjust the 'entropy coefficient' (0–1, default 0.8) to control the score threshold; lower values for large-scale sample sets. Optionally specify a targeted extraction table in xlsx format for isomer or coeluting compound analysis. Run feature detection to generate the feature matrix, then export results as CSV or mzTab for downstream analysis.

## Related tools

- **MetCohort** (LC-MS data processing platform that performs robust peak detection, feature detection, and feature table generation using integrated centWave algorithm with low false positive and false negative rates) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Feature table contains non-zero entries for features detected in at least 80% of samples (or the specified minimum threshold), indicating consistent feature presence across the cohort.
- Retention time and m/z values in the feature table fall within expected ranges for the chromatographic method and instrument mass resolution.
- Visual inspection of chromatographic integration regions (displayed in MetCohort UI) confirms that shaded integration boundaries align with detected peak summits and do not split or merge adjacent peaks.
- Low proportion of features with maximum intensity below the 'minimum intensity of a feature' threshold (default 50), indicating appropriate noise filtering.
- Feature table can be successfully exported and re-imported without data loss; retention time deviation plot shows no extreme outliers indicating problematic alignment of source files.

## Limitations

- Feature detection quality depends critically on prior data alignment quality; poor retention time correction leads to reduced feature numbers and degraded integration.
- The entropy coefficient (0–1) and other parameters require manual tuning based on sample set size and chromatographic complexity; default settings may not be optimal for all analyses.
- Isomers and coeluting compounds may exhibit worse feature detection and integration accuracy in targeted extraction mode compared to untargeted mode.
- Results are sensitive to the choice of reference QC file; changing the reference file may change feature alignment across samples.
- Dead time at the beginning or end of the chromatographic gradient must be manually cropped to avoid spurious features; this requires prior inspection of TIC data.

## Evidence

- [other] Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis.: "Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis."
- [other] Generate a feature table containing detected peaks with retention time, m/z, and intensity values.: "Generate a feature table containing detected peaks with retention time, m/z, and intensity values."
- [intro] MetCohort can realize automatic correction of retention time between samples and precise feature detection.: "MetCohort can realize automatic correction of retention time between samples and precise feature detection."
- [intro] With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously.: "With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously."
- [readme] Minimum number of continuous non-zero points in the process of ROI detection with centWave algorithm. Default value is 3. In small-scale sample processing with a few QC files, the value should be increased to decrease noise.: "Minimum number of continuous non-zero points in the process of ROI detection with centWave algorithm. Default value is 3. In small-scale sample processing with a few QC files, the value should be"
- [readme] Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01. Actually, it can be adjusted to be narrower following data alignment to enhance the peak resolution in feature detection.: "Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01. Actually, it can be adjusted to be narrower following data alignment to enhance the peak"
- [readme] Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The default value is set to 0.8. For large-scale sample processing, users are advised to adjust this value lower.: "Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The"
- [readme] good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration.: "good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration."
