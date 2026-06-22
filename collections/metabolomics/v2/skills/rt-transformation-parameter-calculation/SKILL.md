---
name: rt-transformation-parameter-calculation
description: Use when you have centroided mzML or mzXML LC-MS files from a single batch run that exhibit systematic retention-time drift between samples, one or more designated QC reference file(s), and you need to harmonize RT coordinates across all samples before feature detection to reduce false positive and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# Retention Time Transformation Parameter Calculation

## Summary

Calculate pairwise retention-time shift functions between sample LC-MS chromatograms and a QC reference file using peak-matching or correlation-based alignment methods. This produces RT correction parameters that are subsequently applied to all scan times and feature retention times in each sample.

## When to use

You have centroided mzML or mzXML LC-MS files from a single batch run that exhibit systematic retention-time drift between samples, one or more designated QC reference file(s), and you need to harmonize RT coordinates across all samples before feature detection to reduce false positive and negative feature calls.

## When NOT to use

- Input files are already retention-time corrected or already aligned to a common RT scale.
- No designated QC file is available or all files are equally poor-quality.
- Chromatographic conditions differ drastically between samples (e.g., different columns, temperatures, flow rates), rendering a single QC reference frame inappropriate.
- Raw data are not in mzML or mzXML format, or are in profile (non-centroided) mode.

## Inputs

- mzML or mzXML LC-MS raw data files (centroided)
- Designated quality control (QC) reference file in mzML or mzXML format
- ROA window width parameter (seconds; default 30)
- Allowed delta m/z for ROA detection (default 0.001 Da)
- Intensity threshold coefficient for ROA detection (default 0.5%)
- Allowed delta m/z for XIC extraction (default 0.02 Da)

## Outputs

- Retention-time shift function(s) (RT correction parameters per sample)
- Alignment quality metrics (retention time deviation per sample)
- HTML plot of retention time deviation across all samples (optional)

## How to apply

Load the total ion chromatogram (TIC) or base peak chromatogram (BPC) from a designated QC reference file and extract it as the alignment template. Load the TIC/BPC from each sample file. Compute pairwise retention-time shift between each sample chromatogram and the QC reference using peak-matching or correlation-based alignment algorithms such as dynamic time warping or spline-based warping. The alignment operates within a specified ROA (Region of Alignment) window (default 30 seconds); adjust this width downward if chromatographic dead time is shorter. Set m/z tolerance for ROA detection (default 0.001 Da) narrowly, and m/z tolerance for XIC extraction (default 0.02 Da) wider to enable robust peak matching. Use an intensity threshold (default 0.5% of EWMA of TIC) to control the number of detected alignment anchors. The resulting RT shift function(s) describe how retention times must be adjusted in each sample to align with the QC reference frame.

## Related tools

- **MetCohort** (Performs RT transformation parameter calculation via automatic alignment and correction of retention time between LC-MS samples using QC file reference) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Retention time deviation plot shows near-zero or regular fluctuation across samples; extreme deviations indicate abnormal files or poor ROA matching.
- No warnings or errors during LOWESS fitting or local matching in alignment log.
- Computed RT shift functions are continuous and monotonic (RT must not decrease as original RT increases).
- After applying RT correction, sample chromatograms align with QC reference chromatogram with visual overlap of peak apex positions.
- Feature detection stage produces consistent feature counts and reduced RT variance for the same m/z features across samples (compared to uncorrected data).

## Limitations

- Quality of RT transformation depends critically on the QC reference file choice; abnormal or noisy QC reference files will propagate misalignment to all samples.
- Algorithm assumes unimodal or near-unimodal chromatographic profiles; highly complex or multimodal chromatograms may fail to align properly.
- ROA window width (default 30 s) must be manually reduced if chromatographic dead time is shorter, or alignment anchors will be sparse.
- Files with significantly noisy data or extreme retention-time shifts (e.g., >100 s from reference) may cause LOWESS fitting warnings and produce unreliable RT correction functions.
- Targeted extraction and feature detection of isomers or coeluting compounds may be degraded if RT transformation resolution is insufficient for resolving species.

## Evidence

- [other] How does MetCohort automatically correct retention time between LC-MS samples?: "MetCohort implements automatic retention time correction by requiring at least one file to be specified as a quality control (QC) file, then performing data correction as the first ordered step"
- [other] Workflow for computing and applying RT correction: "Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template. Load each sample mzML/mzXML file and extract"
- [readme] ROA window width parameter and adjustment: "Width of ROA window: The time width of the ROA window. Default is 30 seconds. If the dead time is less than 30 s, it should be reduced."
- [readme] m/z tolerance for ROA and XIC: "Allowed delta m/z of ROA: Allowed m/z deviation in the process of ROA detection. Because the ROA width is short, a relatively narrow value should be set. The default value is 0.001."
- [readme] Intensity threshold for ROA detection: "Intensity threshold of ROA: An intensity coefficient to control the numbers of detected ROAs. Specifically, the intensity at the center of a detected ROA should exceed a dynamic specified value,"
- [readme] Inspection of alignment quality: "Inspecting the deviation plot can help identify abnormal files. In most cases, the retention time deviation is near 0 or exhibits a regular fluctuation. If extreme deviations are observed in certain"
- [readme] Impact of alignment quality on feature detection: "Effective data alignment is a prerequisite for obtaining reliable results, as feature detection is based on the aligned data. A bad data alignment can reduce the feature numbers and negatively affect"
