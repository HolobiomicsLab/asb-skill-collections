---
name: qc-reference-chromatogram-extraction
description: Use when when processing a batch of LC-MS samples in mzML or mzXML format
  where at least one file has been designated as a quality control (QC) file, extract
  its TIC or BPC before performing retention time correction.
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
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c04906
  title: MetCohort
evidence_spans:
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data
  processing tool for large-scale metabolomics and exposomics
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data
  processing tool
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC Reference Chromatogram Extraction

## Summary

Extract total ion chromatogram (TIC) or base peak chromatogram (BPC) from a quality control (QC) reference file in mzML/mzXML format to serve as the alignment template for retention time correction across LC-MS sample batches. This is a prerequisite step that establishes the chromatographic baseline against which all sample files will be aligned.

## When to use

When processing a batch of LC-MS samples in mzML or mzXML format where at least one file has been designated as a quality control (QC) file, extract its TIC or BPC before performing retention time correction. Use this step when sample chromatograms are expected to have retention time drift or shift that must be corrected relative to a stable QC reference before peak detection.

## When NOT to use

- Input files are already retention-time-corrected or pre-aligned.
- No quality control (QC) file has been designated or available in the sample batch.
- Input data are in centroided mzXML/mzML format but lack sufficient scan-level metadata (retention time, m/z arrays) needed for chromatogram extraction.

## Inputs

- mzML or mzXML format LC-MS raw data file designated as QC reference
- Specification of chromatogram type (TIC or BPC)

## Outputs

- Extracted total ion chromatogram (TIC) or base peak chromatogram (BPC) profile from QC reference file
- Alignment template for retention time shift computation

## How to apply

Load the designated QC reference file (mzML or mzXML format) into MetCohort. Extract either the total ion chromatogram (TIC) or base peak chromatogram (BPC) from the QC file—the choice depends on whether you prioritize signal from all m/z values or only the most intense peak at each retention time. The extracted chromatogram serves as the alignment template. This chromatographic profile is then used for pairwise retention-time shift computation between each sample's TIC/BPC and the reference using peak-matching or correlation-based alignment methods (e.g., dynamic time warping or spline-based warping). The extraction must occur before peak detection to ensure that all downstream feature detection operates on retention-time-corrected data.

## Related tools

- **MetCohort** (Performs QC chromatogram extraction, retention time alignment, and feature detection on LC-MS raw data) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Extracted chromatogram profile has non-zero intensity values across the full retention time range of the QC sample.
- TIC or BPC chromatogram can be visually inspected in MetCohort's interface and exported as an HTML alignment plot.
- Pairwise retention time shifts computed between sample and QC chromatograms are within expected range (typically near 0 or exhibit regular fluctuation, not extreme deviations).
- Retention time deviation plot identifies the QC file as the reference with zero or minimal deviation from itself.
- Corrected sample files written to output directory contain updated retention-time metadata aligned to the QC reference scale.

## Limitations

- If the designated QC file contains noisy data or unusual chromatographic profiles, extracted chromatogram may result in poor alignment and abnormal retention time deviations in downstream samples.
- Choice between TIC and BPC chromatogram type may affect alignment quality; TIC is more robust but BPC may be sharper for high-intensity features.
- Extraction assumes files are centroided and in mzML or mzXML format; non-centroided or other formats will fail.
- If retention time range is not manually adjusted (via 'Crop retention time' parameter) to exclude dead time or undesired signal at gradient beginning/end, extracted chromatogram may include noisy regions that degrade alignment.

## Evidence

- [other] Load the QC reference file and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template.: "Load the QC reference file (mzML or mzXML format) and extract its total ion chromatogram (TIC) or base peak chromatogram (BPC) as the alignment template."
- [readme] MetCohort can realize automatic correction of retention time between samples.: "MetCohort can realize automatic correction of retention time between samples and precise feature detection."
- [readme] At least one file must be designated as a quality control (QC) file before processing.: "At least one file need to be specified as quality control (QC) file."
- [readme] Data correction and peak detection must be performed in order.: "Then data correction and peak detection should be performed in order."
- [readme] ROI detection is performed on labelled QC files to determine the construction of ROI matrix.: "ROI detection is only performed on the labelled QC files, which determine the construction of ROI matrix and ranges of features."
- [readme] Retention time deviation plot helps identify abnormal files and verify alignment quality.: "The plot of retention time deviation will be included the exported file directory as an HTML file."
