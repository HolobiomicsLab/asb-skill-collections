---
name: isotopic-impurity-accounting
description: Use when when analyzing LC-MS data from stable isotope labeling experiments where measured isotopologue abundances are contaminated by naturally occurring isotopes and tracer isotopic impurity, and you have access to unlabeled sample reference measurements to empirically model these confounding.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ElemCor
  techniques:
  - LC-MS
  - NMR
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

# Implement the unlabeled-sample resolution-effect correction approach

## Summary

Correct LC-MS fractional abundances of measured isotopologues (FAM) for naturally occurring isotopes and isotopic impurity from the tracer using unlabeled sample reference measurements, producing accurate mass distribution vectors (MDV) that represent true isotopic labeling contribution.

## When to use

When analyzing LC-MS data from stable isotope labeling experiments where measured isotopologue abundances are contaminated by naturally occurring isotopes and tracer isotopic impurity, and you have access to unlabeled sample reference measurements to empirically model these confounding contributions at your instrument's measured resolution.

## When NOT to use

- Input FAM data already corrected or derived from non-MS instruments (e.g., NMR) — this skill is specific to LC-MS resolution-dependent contamination.
- Unlabeled sample reference measurements are unavailable or do not match the labeled sample analyte list and row count — the algorithm requires paired labeled/unlabeled data.
- Tracer element is not present in the compound molecular formula — ElemCor will fail if the selected tracer (e.g., 15N) is absent from compounds in the dataset.

## Inputs

- LC-MS fractional abundances of measured isotopologues (FAM) in XLSX format (columns = samples, rows = compounds, values = M+0 to M+Nt abundances)
- Unlabeled sample reference measurements in XLSX format (same structure as labeled samples)
- Tracer element identifier (13C, 2H, 15N, 18O, or 34S)
- Nutrient isotopic purity (percentage or fraction)
- Nominal instrument resolution (integer, e.g., 140000 or 280000)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Mass distribution vectors (MDV) representing corrected isotopic labeling contribution
- Isotopic enrichment values for each compound
- Fold change of pool size (optional metabolite pool analysis)
- Corrected FAM and MDV for each compound-sample pair (saved in additional XLSX sheets)

## How to apply

Load raw LC-MS FAM data and corresponding unlabeled sample reference measurements into ElemCor in XLSX format. Specify the tracer element (13C, 2H, 15N, 18O, or 34S), isotopic purity of the nutrient, and nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap analyzers). Apply the unlabeled-sample correction algorithm (Reference 3 approach), which uses the unlabeled samples to empirically account for resolution-dependent contamination rather than relying on theoretical mass difference calculations alone. The algorithm generates a correction matrix that transforms FAM to corrected MDV by subtracting the measured contribution from naturally occurring isotopes and isotopic impurity. Validate that corrected MDVs sum to 1.0, show numerical stability, and exhibit enrichment patterns consistent with the labeling design.

## Related tools

- **ElemCor** (Software tool that implements the unlabeled-sample resolution-effect correction algorithm and transforms FAM to MDV) — github.com/4dsoftware/elemcor

## Examples

```
# Open ElemCor GUI: double-click ElemCor.exe → Step 1: Load labeled XLSX → Step 2: Load unlabeled XLSX → Step 3: Set isotopic purity (%) and resolution (e.g., 140000) → Step 4: Select tracer (13C, 15N, etc.) → Step 5: Select mass analyzer (Orbitrap) → Step 6: Run correction; MDV output saved to new sheet in input file.
```

## Evaluation signals

- Corrected MDV for each compound sums to 1.0 (mass conservation check)
- Isotopic enrichment values are non-negative and ≤100% (or ≤1.0 if normalized)
- MDV before and after correction are visually distinct in the ElemCor graphical interface, with correction magnitude inversely related to instrument resolution (higher resolution → smaller correction)
- No error messages reported for tracer element presence or file format; processing completes within 1 minute on standard hardware (2.6 GHz Core i7)
- Fold-change pool size values are positive and consistent with expected metabolic perturbations from the labeling design

## Limitations

- ElemCor requires MATLAB Compiler Runtime installation; MATLAB itself is not required but binary is Windows-only without custom compilation.
- The unlabeled-sample method assumes unlabeled and labeled samples have identical chemical composition and chromatographic behavior; systematic differences in ionization or column performance will degrade correction accuracy.
- FAM length must be matched between labeled and unlabeled files; ElemCor can handle FAM of length other than Nt+1 but labeled and unlabeled files must agree on row count and analyte order.
- Processing time and numerical stability depend on correct selection of tracer element; selecting the wrong tracer (e.g., 15N when 13C is present) causes algorithm failure or erroneous results.
- Current ElemCor version prints only generic error messages; troubleshooting requires manual verification of tracer selection, file path, and data format.

## Evidence

- [readme] naturally occurring isotopes and isotopic impurity from the tracer contribution: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] two different approaches to account for resolution effect: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] unlabeled samples as correction reference method: "Unlabeled samples (Ref. 3). ElemCor corrects and improves the numerical schemes of both methods"
- [readme] steps in workflow for unlabeled-sample approach: "In Step 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only."
- [readme] resolution-dependent correction magnitude: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] MDV output and validation: "The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples."
- [readme] tracer element selection requirement: "PLEASE MAKE SURE THE CORRECT TRACER IS SELECTED! In Step 5, the mass analyzer is selected."
- [readme] numerical stability and file matching requirement: "Check if the labeled and unlabeled files have the same analytes and the same number of rows."
