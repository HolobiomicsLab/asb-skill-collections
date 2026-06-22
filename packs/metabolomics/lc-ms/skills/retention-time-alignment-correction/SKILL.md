---
name: retention-time-alignment-correction
description: Use when when processing a batch of centroided mzML or mzXML LC-MS raw data files where chromatographic retention times drift between sample acquisitions (common in large-scale metabolomics studies).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
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

# retention-time-alignment-correction

## Summary

Automatic correction of retention time shifts between LC-MS samples using a quality control reference file to align chromatographic data before peak detection. This preprocessing step ensures that the same metabolite features appear at consistent retention times across all samples, improving feature detection accuracy and reducing false positives/negatives.

## When to use

When processing a batch of centroided mzML or mzXML LC-MS raw data files where chromatographic retention times drift between sample acquisitions (common in large-scale metabolomics studies). Use this skill before peak detection if you have designated at least one QC file to serve as an alignment reference and you observe retention time variability across the sample set that could cause the same metabolite to map to different m/z–RT coordinates.

## When NOT to use

- Input files are already aligned or feature table has been generated; apply this step only before peak detection, not as a post-hoc correction.
- LC-MS data are in non-centroided profile mode; MetCohort requires centroided data.
- No QC file is available or no single file can be reliably designated as a reference standard for alignment.

## Inputs

- Centroided LC-MS raw data files in mzML or mzXML format
- At least one file designated as a quality control (QC) reference file
- Optional: retention time crop range (in seconds) if auto-range detection is disabled

## Outputs

- Retention-time corrected mzML or mzXML files with updated scan time metadata
- HTML plot of retention time deviation across all samples
- Aligned sample data ready for downstream peak detection

## How to apply

Load your QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template. For each sample file, extract its TIC/BPC and compute the pairwise retention-time shift using peak-matching or correlation-based alignment (e.g., dynamic time warping or spline-based warping) against the QC reference. Apply the computed RT correction function to all mass spectral scan times and m/z feature retention times, writing corrected mzML/mzXML files with updated retention-time metadata to the output directory. Key parameters include the ROA (Regions of Alignment) window width (default 30 seconds, reduce if dead time is shorter), allowed delta m/z for ROA detection (default 0.001, tight tolerance), and intensity threshold for ROA detection (default 0.5% of EWMA-smoothed TIC). Export and inspect the retention time deviation plot (HTML) to identify abnormal files with extreme or irregular deviations that may indicate poor chromatographic conditions or misalignment.

## Related tools

- **MetCohort** (Performs automatic RT correction by alignment of TIC/BPC chromatograms and applies computed warping functions to scan times and feature RT values across all sample files.) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Retention time deviation plot shows near-zero or regular, bounded fluctuations across all samples, with no files exhibiting extreme outlier deviations (which indicate misalignment or abnormal chromatographic conditions).
- Corrected output files contain updated retention time metadata in scan headers; verify by comparing raw and corrected mzML/mzXML files for consistency in m/z but shifted or corrected RT values.
- Peak detection downstream reports increased feature count and reduced fragmentation of the same metabolite across samples at multiple RT positions, indicating improved alignment coherence.
- LOWESS fitting warnings in the alignment log are absent or minimal, suggesting robust local matching between reference and sample chromatograms.
- Inspection of extracted ion chromatograms (XIC) for known standards shows overlapping peak positions across sample files after correction, rather than drift.

## Limitations

- Alignment quality depends critically on selection of a representative QC file; switching reference files may produce different results and potentially introduce inconsistency in feature representation.
- ROA (Regions of Alignment) detection relies on peak-matching and may fail if the QC file contains noisy or sparse data, leading to poor alignment; inspection of TIC/BPC and deviation plots is essential for large-scale analyses.
- Dead time shorter than 30 seconds requires manual reduction of the ROA window width; default parameters may not suit all chromatographic methods.
- Extreme retention time shifts or files with significantly degraded signal may produce LOWESS fitting failures and require exclusion or manual parameter tuning (e.g., lowering intensity threshold from 0.5% to detect more ROAs).
- RT correction is applied globally across all scans and features; localized aberrations in chromatography (e.g., solvent artifact in one time window) are not corrected selectively.

## Evidence

- [other] MetCohort implements automatic retention time correction by requiring at least one file to be specified as a quality control (QC) file, then performing data correction as the first ordered step before peak detection on mzML or mzXML format LC-MS raw data.: "MetCohort implements automatic retention time correction by requiring at least one file to be specified as a quality control (QC) file, then performing data correction as the first ordered step"
- [other] Load the QC reference file and extract TIC/BPC as alignment template; compute pairwise RT shift using peak-matching or correlation-based alignment (dynamic time warping or spline-based warping); apply computed RT correction function to all scan times and feature RT in each sample file.: "1. Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template. 2. Load each sample mzML/mzXML file and"
- [readme] ROA window width default is 30 seconds; allowed delta m/z for ROA detection default is 0.001; intensity threshold for ROA detection default is 0.5% of EWMA-smoothed TIC.: "Width of ROA window: The time width of the ROA window. Default is 30 seconds. If the dead time is less than 30 s, it should be reduced. Allowed delta m/z of ROA: Allowed m/z deviation in the process"
- [readme] Inspecting the deviation plot can help identify abnormal files; extreme deviations suggest differences in chromatographic conditions or inappropriate ROAs; hovering over deviation lines in exported HTML identifies specific problematic files.: "Inspecting the deviation plot can help identify abnormal files. In most cases, the retention time deviation is near 0 or exhibits a regular fluctuation. If extreme deviations are observed in certain"
- [readme] Good alignment makes true features more easily identified and integrated; bad data alignment reduces feature numbers and negatively affects feature integration, demonstrating that alignment quality directly impacts downstream feature detection results.: "Effective data alignment is a prerequisite for obtaining reliable results, as feature detection is based on the aligned data. A bad data alignment can reduce the feature numbers and negatively affect"
