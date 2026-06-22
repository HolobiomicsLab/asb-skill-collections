---
name: lc-ms-data-calibration
description: Use when when you have paired LC-MS measurements from labeled and unlabeled samples of the same analytes, and you need to isolate the true isotopic labeling contribution by removing confounding signal from naturally occurring isotopes and tracer isotopic impurity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - ElemCor
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s12859-019-2669-9
  title: ElemCor
evidence_spans:
- ElemCor is a software tool to correct LC-MS data in isotope labeling experiments.
- ElemCor is a software tool to correct LC-MS data in isotope labeling experiments
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_elemcor_cq
    doi: 10.1186/s12859-019-2669-9
    title: ElemCor
  dedup_kept_from: coll_elemcor_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-019-2669-9
  all_source_dois:
  - 10.1186/s12859-019-2669-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Unlabeled-Sample Resolution-Effect Correction for LC-MS Isotopologue Abundances

## Summary

Correct fractional abundances of measured isotopologues (FAM) from LC-MS data using unlabeled sample reference measurements to account for naturally occurring isotopes, isotopic impurity, and instrument resolution effects, yielding accurate mass distribution vectors (MDV) for isotope labeling experiments.

## When to use

When you have paired LC-MS measurements from labeled and unlabeled samples of the same analytes, and you need to isolate the true isotopic labeling contribution by removing confounding signal from naturally occurring isotopes and tracer isotopic impurity. This approach is particularly valuable when instrument resolution (e.g., Orbitrap at 140,000–280,000) is moderate to high, such that resolution effects significantly distort observed isotopologue peak heights.

## When NOT to use

- Unlabeled reference samples are not available or do not match the analyte roster of labeled samples — use mass difference theory approach instead.
- The tracer element is not present in all compounds of interest — ElemCor will report an error and fail to process.
- Input FAM data are already corrected or are expressed as absolute abundances rather than fractional abundances.

## Inputs

- XLSX spreadsheet with fractional abundances of measured isotopologues (FAM) from labeled samples
- XLSX spreadsheet with corresponding unlabeled sample FAM reference measurements
- Tracer element identity (13C, 2H, 15N, 18O, or 34S)
- Isotopic purity of tracer nutrient (%)
- Nominal instrument resolution (numeric value, e.g., 140000 or 280000)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Mass distribution vectors (MDV) for each analyte and sample, corrected for resolution effects and naturally occurring isotopes
- Isotopic enrichment values per compound
- Fold change of pool size for different compounds and samples
- FAM and MDV before and after correction, stored in additional sheets within the original XLSX file

## How to apply

Load raw FAM data from labeled samples and corresponding unlabeled sample reference measurements in XLSX format into ElemCor. Specify the tracer element (13C, 2H, 15N, 18O, or 34S), its isotopic purity, and the nominal instrument resolution. ElemCor applies the unlabeled-samples correction algorithm (Reference 3 approach), which uses the unlabeled reference to empirically quantify resolution-induced peak spreading and isotopic interference. The software computes a correction matrix that transforms FAM into MDV by subtracting the unlabeled contribution. Validate the corrected MDV output for numerical stability, consistency across replicate compounds, and expected isotopic enrichment ranges. The correction amount scales monotonically with instrument resolution: extremely low resolution yields minimal correction, while extremely high resolution yields near-zero correction.

## Related tools

- **ElemCor** (Implements unlabeled-sample resolution-effect correction algorithm to transform FAM into MDV) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- MDV values sum to 1.0 (or close, accounting for numerical precision) for each analyte.
- Isotopic enrichment is non-negative and remains within expected bounds for the labeled tracer (typically 0–100% excess atom percent or similar metric).
- FAM and MDV before/after correction are visually and numerically consistent: after correction, labeled samples show higher enrichment in higher isotopologues (M+n) compared to unlabeled controls.
- Processing completes without error within ~10–60 seconds (as reported for example files on a 2.6 GHz Core i7 or 1.5 GHz Core i5).
- Corrected MDV differ from uncorrected FAM in a direction and magnitude proportional to the specified instrument resolution: higher resolution produces larger corrections.

## Limitations

- Software requires MATLAB Compiler Runtime installation; MATLAB itself is not required but binary files must be run from the download folder and remain offline-capable only after initial installation.
- The current version prints only generic error messages; troubleshooting relies on checking tracer element selection, file location, and consistency of analyte roster between labeled and unlabeled files.
- FAM data must have the same length (number of isotopologues) and the same set of compounds/analytes in both labeled and unlabeled input files; mismatches cause silent or cryptic failures.
- The correction is sensitive to correct tracer element selection: selecting the wrong tracer (e.g., C or S when 15N data are loaded) causes the algorithm to fail or produce invalid results for compounds lacking that element.

## Evidence

- [readme] the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only.: "Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only."
- [readme] The example files shown in Fig. 2 can be processed within 10 seconds on a 2.6GHz Core i7 processor, and 20 seconds on a 1.5GHz Core i5 processor.: "The example files shown in Fig. 2 can be processed within 10 seconds on a 2.6GHz Core i7 processor, and 20 seconds on a 1.5GHz Core i5 processor."
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly."
- [readme] Check if the labeled and unlabeled files have the same analytes and the same number of rows.: "Check if the labeled and unlabeled files have the same analytes and the same number of rows."
