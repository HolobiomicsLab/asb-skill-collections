---
name: mass-error-threshold-calibration
description: Use when you have isolated TIC peak regions and need to extract ion chromatograms
  (EICs) for XCMS parameter estimation via the EICparams function. Use it specifically
  when your mass analyzer's measurement accuracy is known (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - AutoTuner
  - XCMS
  - MSconvert
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-error-threshold-calibration

## Summary

Calibrate absolute mass error thresholds for ion chromatogram extraction during XCMS parameter estimation by setting the massThresh parameter to filter EICs based on analytical instrument capabilities. This threshold determines which ions are retained during per-EIC parameter extraction from isolated TIC peak regions.

## When to use

Apply this skill when you have isolated TIC peak regions and need to extract ion chromatograms (EICs) for XCMS parameter estimation via the EICparams function. Use it specifically when your mass analyzer's measurement accuracy is known (e.g., qTOF, Orbitrap, or FTICR instruments) and you need to set a filtering criterion that reflects the instrument's absolute mass error tolerance to avoid spurious ion matches.

## When NOT to use

- Input has already been processed through XCMS peak picking or feature detection — massThresh calibration is a pre-processing step for parameter tuning, not a post-hoc filter on detected features.
- Mass analyzer type or measurement accuracy is unknown — threshold calibration depends on knowing the instrument's inherent mass error capabilities; setting massThresh arbitrarily without this context will produce unreliable parameter estimates.
- Only a single or two samples are available — AutoTuner is designed for at least 3 samples to derive robust statistical parameter estimates; insufficient sample size invalidates threshold tuning.

## Inputs

- AutoTuner object containing isolated TIC peak regions (from prior isolatePeaks step)
- Raw mass spectral data in mzML, mzXML, or CDF format (preprocessed by MSconvert)

## Outputs

- Parameter estimate object containing nine tuned XCMS-relevant parameters derived from gap-filtered EICs

## How to apply

Before invoking EICparams on isolated TIC peak regions, determine the massThresh parameter as an absolute mass error tolerance (in m/z units) that exceeds your mass analyzer's typical measurement accuracy. For example, if your instrument has ±5 ppm accuracy, convert this to absolute m/z error and set massThresh slightly above this value (e.g., 0.005 m/z for low-mass ranges). Pass this calibrated massThresh to EICparams along with useGap=TRUE to enable gap-based refinement during chromatogram extraction. The function uses this threshold to filter ion chromatograms within each isolated peak region, retaining only ions within the mass error window before deriving the nine XCMS-relevant parameter estimates. Higher massThresh values relax filtering (retaining more ions), while lower values tighten it (removing noise and spurious peaks); the choice directly affects the robustness of downstream parameter estimates.

## Related tools

- **AutoTuner** (Main R package providing EICparams function and parameter tuning workflow; massThresh is a key control parameter for EIC filtering within this framework) — https://github.com/KujawinskiLaboratory/Autotuner
- **XCMS** (Downstream metabolomics data processing software whose parameters (nine XCMS-relevant parameters) are estimated and tuned via AutoTuner's massThresh-calibrated EIC extraction)
- **MSconvert** (Preprocessing tool to convert raw mass spectrometer proprietary formats (.raw, .d, etc.) into open formats (mzML, mzXML, CDF) required by AutoTuner before EICparams can be applied)
- **R** (Execution environment for AutoTuner package and EICparams function invocation)

## Examples

```
EICparams(autoTunerObject, massThresh=0.005, useGap=TRUE)
```

## Evaluation signals

- Verify that massThresh is set to a value greater than the analytical capabilities (mass error) of the mass analyzer; thresholds that are too tight (smaller than instrument accuracy) will filter out true signal, while thresholds that are too loose (much larger than accuracy) will retain noise and spurious ions.
- Check that the returned parameter estimate object contains exactly nine distinct XCMS-relevant parameters with non-null, numeric values; missing or NA values indicate filtering was too aggressive or too permissive.
- Confirm that when useGap=TRUE is enabled, gap-based filtering produces more stable parameter estimates across multiple isolated TIC peak regions compared to raw EIC extraction, evidenced by lower variance in parameter values across replicates.
- Validate downstream XCMS peak picking performance: lower false positive and false negative rates in feature detection indicate the calibrated massThresh produced appropriate parameter estimates.
- Compare parameter estimates derived from different massThresh values to ensure the chosen threshold yields a local optimum in parameter stability (minimal sensitivity to small threshold variations).

## Limitations

- massThresh calibration depends on accurate knowledge of the mass analyzer's measurement accuracy; estimates based on manufacturer specifications alone may not reflect actual instrument performance under field conditions.
- The absolute mass error model (fixed m/z tolerance) does not account for ppm-dependent error that increases with m/z; for very wide m/z ranges (e.g., lipids and small metabolites in the same analysis), a single massThresh may be suboptimal across mass regions.
- AutoTuner requires at least 3 samples of raw untargeted metabolomics data; studies with fewer samples cannot reliably tune parameters or calibrate massThresh via statistical inference.
- No changelog is maintained for the project, limiting ability to track changes in parameter estimation logic or threshold behavior across AutoTuner versions.
- Parameter tuning via massThresh is tested on qTOF, Orbitrap, and FTICR instruments; performance on other mass analyzer types (e.g., quadrupole, ion trap) is not explicitly validated in the literature.

## Evidence

- [other] EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error): "EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error)"
- [intro] Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [intro] The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer: "The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer."
- [other] when useGap=TRUE, the function applies gap-based filtering to refine parameter estimates: "when useGap=TRUE, the function applies gap-based filtering to refine parameter estimates, producing an object containing parameter estimates for downstream use in XCMS."
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
- [readme] AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF): "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
