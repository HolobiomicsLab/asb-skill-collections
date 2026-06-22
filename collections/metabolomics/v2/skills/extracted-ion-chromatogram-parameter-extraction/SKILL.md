---
name: extracted-ion-chromatogram-parameter-extraction
description: Use when after isolating TIC peak regions via sliding window analysis and peak expansion (isolatePeaks), apply this skill when you need dataset-specific XCMS parameter estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - XCMS
  - Autotuner
  - MSconvert
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autotuner_parameter_selection_cq
    doi: 10.1101/812370
    title: AutoTuner parameter selection
  dedup_kept_from: coll_autotuner_parameter_selection_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/812370
  all_source_dois:
  - 10.1101/812370
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Extracted-Ion Chromatogram Parameter Extraction

## Summary

Extract and estimate nine XCMS-relevant parameters from isolated TIC peak regions by processing individual extracted ion chromatograms with mass error filtering and optional gap-based refinement. This skill produces tuned parameter estimates suitable for downstream untargeted metabolomics data processing.

## When to use

After isolating TIC peak regions via sliding window analysis and peak expansion (isolatePeaks), apply this skill when you need dataset-specific XCMS parameter estimates. Trigger conditions: you have an AutoTuner object containing isolated TIC regions, you require absolute mass error thresholds tailored to your mass analyzer's capabilities, and you want statistical inference-derived parameter values rather than generic defaults.

## When NOT to use

- Input data has not been converted to open formats (mzML, mzXML, or CDF) — AutoTuner requires preprocessed mass spectral data, typically via MSconvert
- Fewer than 3 raw mass spectrometry samples are available — AutoTuner requires multiple samples to derive robust parameter estimates via statistical inference
- Peak regions have not yet been isolated via TIC sliding window analysis — EICparams depends on isolated TIC peak regions from isolatePeaks

## Inputs

- AutoTuner object containing isolated TIC peak regions
- massThresh parameter value (absolute mass error threshold in Da)
- useGap flag (boolean)

## Outputs

- Parameter estimate object containing nine tuned XCMS parameters

## How to apply

Invoke the EICparams function on an AutoTuner object containing isolated TIC peak regions from a prior isolatePeaks step. Set the massThresh parameter to an absolute mass error threshold appropriate for your mass analyzer (e.g., 0.005 for high-resolution instruments); this threshold filters ion chromatograms by mass accuracy. Enable useGap=TRUE to apply gap-based filtering during chromatogram extraction, which refines parameter estimates by handling signal discontinuities. The function then extracts individual extracted ion chromatograms from each isolated region and derives nine distinct XCMS parameters via statistical inference. Capture the returned parameter estimate object, which contains the tuned values ready for XCMS processing.

## Related tools

- **XCMS** (Target metabolomics data processing software for which EICparams derives tuned parameter estimates)
- **Autotuner** (R package containing the EICparams function and managing the AutoTuner object workflow) — https://github.com/KujawinskiLaboratory/Autotuner
- **MSconvert** (Converts raw mass spectrometry data from proprietary instrument formats (e.g., .mzML, .mzXML, .CDF) for input to AutoTuner)
- **R** (Programming language and runtime for executing EICparams and AutoTuner workflows)

## Examples

```
# After isolatePeaks has returned an AutoTuner object
parameter_estimates <- EICparams(autotuner_object, massThresh=0.005, useGap=TRUE)
```

## Evaluation signals

- Parameter estimate object is non-empty and contains exactly nine distinct XCMS parameters derived from the input isolated TIC regions
- All parameter values fall within expected ranges for the given mass analyzer type (qTOF, Orbitrap, or FTICR)
- When useGap=TRUE is enabled, the refined parameter estimates show reduced variance compared to useGap=FALSE, indicating effective gap-based filtering
- Downstream XCMS processing using the returned parameter estimates produces feature tables with fewer false positives and higher reproducibility across replicates than default XCMS parameters
- massThresh filtering removes ion chromatograms exceeding the specified absolute mass error, confirming mass accuracy filtering was applied

## Limitations

- AutoTuner has been tested primarily on qTOF, Orbitrap, and FTICR mass analyzers; applicability to other analyzer types is not documented
- Requires R version 3.6 or greater; older R installations will not support the package
- Parameter tuning depends on the quality and diversity of input samples; datasets with poor chromatographic separation or unusual ionization patterns may yield unreliable estimates
- No changelog is available in the repository, making it difficult to track which versions introduced bug fixes or changes to EICparams behavior

## Evidence

- [other] EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error); when useGap=TRUE, the function applies gap-based filtering to refine parameter estimates, producing an object containing parameter estimates for downstream use in XCMS.: "EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error); when useGap=TRUE, the function applies gap-based"
- [intro] Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters.: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters"
- [intro] In order to estimate parameters from the raw data, the user should run the EICparams function: "In order to estimate parameters from the raw data, the user should run the EICparams function"
- [intro] The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer.: "The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer"
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers"
- [readme] For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)"
