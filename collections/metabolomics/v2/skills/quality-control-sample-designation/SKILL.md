---
name: quality-control-sample-designation
description: Use when when importing a new batch of centroided mzML or mzXML LC-MS files into MetCohort, before any data alignment or feature detection is performed. At least one file must be designated as QC to enable ROA detection and alignment;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# quality-control-sample-designation

## Summary

Designation of quality control (QC) files from a cohort of LC-MS raw data files prior to retention time alignment and feature detection. QC files are used to construct the region-of-alignment (ROA) matrix and determine feature ranges, making their selection critical for downstream data correction and peak detection accuracy.

## When to use

When importing a new batch of centroided mzML or mzXML LC-MS files into MetCohort, before any data alignment or feature detection is performed. At least one file must be designated as QC to enable ROA detection and alignment; users should label all QC files (or representative QC files if a subset) to ensure robust alignment reference selection.

## When NOT to use

- If all samples are biological/experimental samples with no QC replicates — at least one QC file is mandatory for MetCohort processing
- If raw data files are not centroided or are in formats other than mzML/mzXML — MetCohort requires pre-processed centroided data
- If the experiment does not require retention time alignment or ROI-based feature detection — QC designation is specific to MetCohort's workflow

## Inputs

- Centroided LC-MS raw data files (mzML or mzXML format)
- Sample metadata or experimental design indicating which files are quality control samples

## Outputs

- Labelled QC file set registered in MetCohort project
- Reference file designation for ROA detection
- ROA matrix constructed from QC file data

## How to apply

During the Data Import stage in MetCohort, upload all pending LC-MS files (in mzML or mzXML format) to the window and explicitly label the files that represent quality control samples. The software uses labelled QC files to perform ROI detection, which determines the construction of the ROA matrix and establishes the retention time and m/z ranges for features. When selecting a reference file for retention time alignment in the subsequent Data Alignment stage, choose from the labelled QC files. For large-scale analyses, users may select only representative QC files rather than all available samples, balancing computational efficiency with alignment robustness. The choice of reference file can affect alignment results, so it is recommended to inspect the retention time deviation plot after alignment to verify data quality.

## Related tools

- **MetCohort** (LC-MS data processing software that uses designated QC files to construct ROA matrix and perform data alignment and feature detection) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- At least one file is successfully labelled as QC in the MetCohort interface
- ROA detection proceeds without error on the selected QC files
- Retention time deviation plot can be generated and exported, showing expected alignment behavior (near 0 or regular fluctuation) for QC files
- Feature table is generated with high quality, indicating low false positive and false negative rates
- Abnormal files are identifiable in the deviation plot and can be investigated or excluded from downstream analysis

## Limitations

- QC file selection significantly influences retention time alignment quality; poor QC file choice or contaminated QC samples can lead to misalignment and reduced feature detection accuracy
- For experiments with very short dead times (< 30 seconds), the default ROA window width must be adjusted, which may require reconsidering which files serve as robust QC references
- If QC files contain noisy or significantly degraded data, the ROA matrix may be constructed poorly, leading to warnings during LOWESS fitting and incorrect feature boundaries
- The same reference file should ideally be used for both raw data alignment and feature detection to maintain consistency; switching reference files between stages can reduce feature matching reliability

## Evidence

- [intro] At least one file need to be specified as quality control (QC) file.: "At least one file need to be specified as quality control (QC) file."
- [readme] In Data Import stage, all the pending files (in mzML or mzXML format) need to be uploaded to the window. The QC files can be labelled. ROI detection is only performed on the labelled QC files, which determine the construction of ROI matrix and ranges of features.: "In Data Import stage, all the pending files (in mzML or mzXML format) need to be uploaded to the window. The QC files can be labelled. ROI detection is only performed on the labelled QC files, which"
- [readme] Users can select all the files as QC or only the representative files.: "Users can select all the files as QC or only the representative files."
- [readme] In Data Alignment stage, users should select one reference file from labelled QC files for ROA detection. Changing the reference file may change the alignment results.: "In Data Alignment stage, users should select one reference file from labelled QC files for ROA detection. Changing the reference file may change the alignment results."
- [readme] Inspecting the deviation plot can help identify abnormal files. Upon examining the TICs (Total Ion Chromatograms) of the files, it was found that the abnormal files contained significantly noisy data.: "Upon examining the TICs (Total Ion Chromatograms) of the files, it was found that the abnormal files contained significantly noisy data."
