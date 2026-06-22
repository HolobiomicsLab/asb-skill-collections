---
name: spectral-noise-filtering
description: Use when immediately after extracting ion chromatograms (EICs) by binning mass spectral data across the full m/z range from raw LC/HRMS files (mzML, mzXML, or netCDF format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - IDSL.IPA
  - R
  - xcms
  - MZmine 2
  techniques:
  - GC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-noise-filtering

## Summary

Filter mass spectral noise from extracted ion chromatogram (EIC) candidates during the initial stage of untargeted LC/HRMS data processing. This skill removes low-intensity background signals and non-significant peaks to retain only genuine chemical signals for downstream peak detection.

## When to use

Apply this skill immediately after extracting ion chromatograms (EICs) by binning mass spectral data across the full m/z range from raw LC/HRMS files (mzML, mzXML, or netCDF format). Use it when processing population-scale untargeted studies where raw data contains substantial instrumental noise and when you need to reduce false positives before peak detection and property evaluation.

## When NOT to use

- Input is already a peak feature table or aligned peak matrix — filtering is part of the initial LC/HRMS processing stage, not applicable to downstream aligned data.
- Data has already been processed through complete peak detection and annotation — re-filtering at that stage would remove valid signals.
- Targeted analysis with known m/z-RT pairs where you want to preserve low-intensity but biologically relevant signals — this skill is designed for untargeted discovery where noise reduction takes priority.

## Inputs

- raw LC/HRMS data files (mzML format)
- raw LC/HRMS data files (mzXML format)
- raw LC/HRMS data files (netCDF/CDF format)
- m/z-binned intensity matrices across full mass range
- user-configured noise intensity threshold parameters

## Outputs

- filtered EIC candidates with m/z, retention time, and intensity metadata
- significance-ranked extracted ion chromatograms
- noise-filtered dataset ready for peak detection stage

## How to apply

After loading raw LC/HRMS data and generating initial EIC candidates via m/z binning, apply intensity thresholding to remove signals below a noise floor. The IDSL.IPA workflow implements this as part of its first algorithmic stage by binning mass spectral data across the full m/z range, then filtering to retain only significant EIC candidates based on intensity criteria. The threshold parameters are user-configurable via the IPA parameter spreadsheet (IDSL.IPA uses parameter-driven selection). Retain EIC candidates that exceed the signal-to-noise cutoff while discarding noise-dominated chromatographic bins. This reduces computational burden on subsequent peak detection and improves specificity by eliminating low-confidence signals before peak shape analysis and property calculation.

## Related tools

- **IDSL.IPA** (primary R package implementing spectral noise filtering as first algorithmic stage in EIC candidate generation pipeline) — https://github.com/idslme/IDSL.IPA
- **R** (runtime environment for IDSL.IPA noise filtering and parameter-driven data processing)
- **xcms** (comparative peak picking tool; IDSL.IPA outperforms it in terms of sensitivity and specificity for noise-filtered peak detection)
- **MZmine 2** (comparative peak picking tool; IDSL.IPA outperforms it in terms of sensitivity and specificity for noise-filtered peak detection)

## Examples

```
library(IDSL.IPA); IPA_workflow("Address of the IPA parameter spreadsheet")
```

## Evaluation signals

- Verify that all retained EIC candidates exceed the configured intensity threshold parameter and that no candidates below threshold remain in output.
- Confirm output EIC candidates include valid m/z, retention time, and intensity metadata for each bin retained.
- Check that the number of EIC candidates is substantially reduced compared to raw binned data, indicating effective noise removal without over-filtering.
- Validate downstream peak detection results show improved specificity (fewer false positive peaks) and maintain or improve sensitivity compared to unfiltered data, as reported in the IDSL.IPA publication.
- Ensure output is compatible with downstream IDSL.IPA modules (peak detection, peak property evaluation) by verifying file format and metadata structure.

## Limitations

- Noise threshold parameters must be empirically tuned per instrument platform and ESI polarity mode; no universal threshold is provided in the article.
- Over-aggressive intensity filtering may remove genuine low-abundance metabolites or minor isotopologues; balance between noise reduction and chemical completeness requires domain knowledge.
- The skill is designed for untargeted small-molecule LC/HRMS data; applicability to other MS modalities (e.g., GC/MS, MALDI, ion mobility) is not discussed.
- IDSL.IPA achieves noise filtering via parameter-driven thresholding, but the article does not detail how threshold values should be selected for new datasets or mass spectrometers not represented in the reference case study (ST002263).

## Evidence

- [other] Apply intensity thresholding and noise filtering to retain only significant EIC candidates.: "Apply intensity thresholding and noise filtering to retain only significant EIC candidates."
- [other] Extract ion chromatograms by binning mass spectral data across the full m/z range to identify candidate signals.: "Extract ion chromatograms by binning mass spectral data across the full m/z range to identify candidate signals."
- [readme] algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation: "algorithms covering extracted ion chromatogram (EIC) candidate generation, peak detection, peak property evaluation"
- [readme] Parameter selection through a user-friendly and well-described parameter spreadsheet: "Parameter selection through a user-friendly and well-described parameter spreadsheet"
- [readme] IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms in terms of sensitivity, specificity and speed: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, xcms in terms of sensitivity, specificity and speed"
