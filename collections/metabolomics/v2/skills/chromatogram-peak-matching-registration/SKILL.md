---
name: chromatogram-peak-matching-registration
description: Use when you have multiple LC-MS samples in mzML or mzXML format with variable retention times, at least one designated as a quality control (QC) reference file, and you need to correct for RT drift before peak/feature detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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

# chromatogram-peak-matching-registration

## Summary

Align retention times across LC-MS sample chromatograms by computing pairwise shifts between sample total ion chromatograms (TIC) or base peak chromatograms (BPC) and a quality control reference using peak-matching or correlation-based warping. This preprocessing step corrects systematic RT drift before feature detection, improving feature consistency across a batch.

## When to use

Apply this skill when you have multiple LC-MS samples in mzML or mzXML format with variable retention times, at least one designated as a quality control (QC) reference file, and you need to correct for RT drift before peak/feature detection. Use this if samples show visible RT deviations in their chromatograms (e.g., from instrument drift, temperature variation, or column degradation) that would cause the same feature to be detected at different retention times across samples.

## When NOT to use

- Input files are not in mzML or mzXML format (e.g., raw vendor formats or already-processed feature tables)
- No quality control (QC) file is available or designated
- Samples are from orthogonal chromatographic methods or fundamentally different instrumental conditions where a single reference alignment is invalid

## Inputs

- mzML or mzXML format LC-MS raw data files (centroided)
- At least one file designated as quality control (QC) reference file
- Optional: retention time crop range in seconds if non-default chromatographic gradient is used

## Outputs

- Retention time corrected mzML or mzXML files with updated scan time metadata
- Retention time deviation plot (HTML file) showing RT shift for each sample relative to QC reference
- Alignment quality report identifying abnormal files or LOWESS fitting warnings

## How to apply

First, load the QC reference file (mzML or mzXML) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template. Load each sample file and extract its corresponding TIC or BPC. Compute pairwise retention-time shifts between each sample chromatogram and the QC reference using peak-matching or correlation-based alignment methods such as dynamic time warping or spline-based warping. Apply the resulting RT correction function to all mass spectral scan times and m/z feature retention times in each sample. Finally, write corrected mzML/mzXML files with updated retention-time metadata to the output directory. Inspect the exported retention time deviation plot (HTML) to identify abnormal files before proceeding to feature detection, as poor alignment directly degrades downstream peak integration and feature count.

## Related tools

- **MetCohort** (Implements automatic retention time correction via peak-matching and correlation-based alignment (dynamic time warping or spline warping) on mzML/mzXML LC-MS data using QC file as reference; outputs corrected mzML/mzXML and RT deviation plots) — https://github.com/JunYang2021/MetCohort

## Examples

```
cd path_to_MetCohort/src && python MetCohort.py  # Launch GUI; specify QC file(s), select Data Alignment stage, choose reference QC file, set ROA window width (default 30 s) and allowed m/z deviations (0.001 for ROA, 0.02 for XIC), enable plot export, click Run to generate corrected mzML files and RT deviation HTML.
```

## Evaluation signals

- Retention time deviation plot shows shifts ≤ expected instrumental drift (typically < ±60 s over full gradient); no extreme outliers or erratic trajectories
- Corrected chromatograms (TIC/BPC) from different samples visually align when overlaid, with no phase-shifted peaks
- HTML deviation plot does not contain LOWESS fitting warnings, which indicate failed or unreliable local alignment
- Downstream feature detection (after RT correction) shows consistent retention times for the same feature across QC replicates (e.g., within ±5 s for typical 20–30 min gradients)
- Corrected mzML/mzXML files retain identical peak count and intensity profiles as originals, with only scan/feature retention time metadata modified

## Limitations

- Alignment quality depends critically on the choice of QC reference file; abnormal or noisy QC files will propagate misalignment to all samples
- Poor alignment can result from fundamentally incompatible ROAs (regions of alignment) if samples differ drastically in ionization efficiency or matrix composition
- Requires centroided (not profile) data; vendor raw formats must be converted to mzML/mzXML prior to alignment
- If chromatographic gradient includes blank or undesired signal at beginning or end, retention time crop range must be manually specified; auto-crop may fail
- Dynamic time warping and spline warping may over-correct or under-correct severe RT drift if peak morphology differs substantially between samples and QC

## Evidence

- [other] MetCohort implements automatic retention time correction by requiring at least one file to be specified as a quality control (QC) file, then performing data correction as the first ordered step before peak detection on mzML or mzXML format LC-MS raw data.: "MetCohort implements automatic retention time correction by requiring at least one file to be specified as a quality control (QC) file, then performing data correction as the first ordered step"
- [other] Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template. Load each sample mzML/mzXML file and extract its TIC or BPC. Compute pairwise retention-time shift between each sample chromatogram and the QC reference using peak-matching or correlation-based alignment (e.g., dynamic time warping or spline-based warping). Apply the computed RT correction function to all mass spectral scan times and m/z feature retention times in each sample file.: "Compute pairwise retention-time shift between each sample chromatogram and the QC reference using peak-matching or correlation-based alignment (e.g., dynamic time warping or spline-based warping)."
- [readme] The quality of the alignment can significantly influence feature detection and integration. Therefore, it is necessary to manually inspect the alignment results during processing. Users are encouraged to export the plot of retention time deviation during the data alignment stage.: "The quality of the alignment can significantly influence feature detection and integration. Therefore, it is necessary to manually inspect the alignment results during processing."
- [readme] In the HTML file exported from MetCohort, users can hover the cursor over the abnormal deviation line to identify the specific file. Upon examining the TICs (Total Ion Chromatograms) of the files, it was found that the abnormal files contained significantly noisy data. Identifying such abnormal files is crucial for large-scale sample analyses.: "Upon examining the TICs (Total Ion Chromatograms) of the files, it was found that the abnormal files contained significantly noisy data."
- [readme] For some experiments having blank or undesired signal at the beginning or ending of chromatographic gradient, users can uncheck the box of Auto range and set the real retention time in Crop retention time in seconds.: "For some experiments having blank or undesired signal at the beginning or ending of chromatographic gradient, users can uncheck the box of Auto range and set the real retention time in Crop retention"
