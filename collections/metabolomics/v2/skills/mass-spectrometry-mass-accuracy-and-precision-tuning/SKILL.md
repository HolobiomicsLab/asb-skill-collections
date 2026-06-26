---
name: mass-spectrometry-mass-accuracy-and-precision-tuning
description: Use when when extracting and validating chromatographic peaks for target
  molecules from centroided mzML files, particularly when working with multiple isotopologues
  and adducts where mass tolerance directly affects whether predicted isotopologues
  are correctly grouped and detected as part of the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - mzRAPP
  - enviPat
  - R
  - MSconvert
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing
  (NPP)
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided
  for all (enviPat predicted) isotopologues
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-mass-accuracy-and-precision-tuning

## Summary

Configure mass accuracy and precision parameters for LC-HRMS peak extraction to ensure isotopologue detection and validation in benchmark dataset generation. These parameters control the tolerance windows for matching theoretical m/z values to observed peaks and determine whether isotopologues are clustered into single chromatograms.

## When to use

When extracting and validating chromatographic peaks for target molecules from centroided mzML files, particularly when working with multiple isotopologues and adducts where mass tolerance directly affects whether predicted isotopologues are correctly grouped and detected as part of the same peak.

## When NOT to use

- When working with profile (non-centroided) mzML files; centroiding must be performed first via MSconvert.
- When instrument mass resolution is unknown or not available; resolution must be provided to correctly scale m/z tolerance windows across the mass range.
- When target molecules lack retention time boundaries or known molecular composition; mass tolerance alone cannot reliably distinguish co-eluting peaks.

## Inputs

- centroided mzML files
- target file CSV with molecular formulas (SumForm_c) and retention time boundaries
- instrument resolution model or custom resolution list (R vs m/z calibration)

## Outputs

- validated benchmark dataset CSV with detected peaks, isotopologues, and adducts
- quality metrics: peak detection rate (%), degenerated isotopologue ratio (%)
- extraction parameters log documenting applied mz precision and accuracy

## How to apply

Set two complementary mass tolerance parameters in mzRAPP: (1) mz precision [ppm] defines the maximum spread of mass peaks in the m/z dimension to be considered part of the same chromatogram (clustering tolerance), and (2) mz accuracy [ppm] defines the maximum difference between the theoretical accurate m/z and observed m/z for peak matching. Both must be calibrated to the instrument's mass resolution, which is specified via the selected instrument model (e.g., OrbitrapXL, Velos, VelosPro_R60000@400) to apply correct resolution-dependent window calculations. Typical starting values are 5–6 ppm for both; these must be validated by inspecting whether all predicted isotopologues for target molecules are detected and whether isotopologue ratios pass correlation and bias filters.

## Related tools

- **mzRAPP** (primary interface for configuring and applying mass accuracy/precision parameters to extract and validate isotopologue peaks from mzML files) — https://github.com/YasinEl/mzRAPP
- **enviPat** (predicts isotopologue patterns and m/z values for target molecules given instrument resolution; predictions are matched against observed peaks using configured mass accuracy tolerance)
- **MSconvert** (upstream tool for converting vendor mass spectrometry files to centroided mzML format required by mzRAPP)

## Examples

```
library(mzRAPP); callmzRAPP(); # In Generate Benchmark tab: set instrument='OrbitrapXL,Velos,VelosPro_R60000@400', mz_precision=6, mz_accuracy=5, then process mzML files
```

## Evaluation signals

- All predicted isotopologues for target molecules are grouped into single chromatograms (no spurious splitting); verify by checking that each target has one continuous extracted ion chromatogram per adduct.
- Detected peaks match retention time boundaries (user.rtmin/user.rtmax); peaks outside these windows are rejected even if mass-matched.
- Isotopologue ratio bias filter (<30%) and peak shape correlation (Pearson r ≥0.85 vs most abundant isotopologue) are satisfied; degenerated isotopologue ratio should remain <20% for well-tuned parameters.
- Peak detection rate across sample groups is consistent (83–99% reported for XCMS/MZmine2); systematic variation suggests mass tolerance is too loose (false positives) or too tight (false negatives).
- Benchmark size and composition match known molecule count; processing all 30 MTBLS267 _POS.mzML files should yield 47 molecules with 157 features and ~2870 peaks total.

## Limitations

- Mass tolerance parameters are instrument- and mass-range-dependent; a single setting may not be optimal across all m/z values if instrument resolution is poor or non-linear.
- If mz precision is set too tight (<4 ppm), natural isotope spacing may be unresolved and isotopologues split into separate chromatograms; if too loose (>8 ppm), neighboring molecular species may be co-grouped.
- Retention time boundaries (user.rtmin/user.rtmax) are still required to disambiguate co-eluting isobars; mass tolerance alone is insufficient for reliable peak assignment.
- The 30% isotopologue ratio bias and 0.85 correlation cutoffs are fixed in mzRAPP; masses tuned far outside instrument specifications may fail these downstream filters even if peaks are detected.
- Profile-mode or poorly centroided data will yield unreliable m/z estimates and mass tolerance tuning will be ineffective.

## Evidence

- [methods] mz precision and mz accuracy parameters: "Configure extraction parameters: lowest isotopologue 0.05, minimum 6 scans per peak, 6 ppm mass precision, 5 ppm mass accuracy."
- [readme] mass tolerance for chromatogram clustering: "Maximum spread of mass peaks in the mz dimension to be still considered part of the same chromatogram."
- [readme] instrument resolution specification: "This is necessary in order to apply the correct mass resolution for any given m/z value when isotopologues are predicted for different molecular formulas."
- [readme] validation against isotopologue predictions: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files."
- [methods] isotopologue ratio bias filtering threshold: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
