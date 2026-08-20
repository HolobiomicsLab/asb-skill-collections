---
name: numerical-method-scheme-analysis
description: Use when when correcting LC-MS isotope labeling data and existing numerical
  schemes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ElemCor
  - IsoCor
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numerical-method-scheme-analysis

## Summary

Analyze and improve numerical schemes used in isotope labeling data correction methods, comparing algorithmic approaches (mass-difference theory vs. unlabeled-samples) to identify computational stability improvements and resolution-effect handling. This skill is essential when existing correction methods produce artifacts or instabilities, particularly at varying instrument resolutions.

## When to use

When correcting LC-MS isotope labeling data and existing numerical schemes (e.g., combinatorial approaches like IsoCor) produce inconsistent or unstable MDV values across different instrument resolutions, or when two competing algorithmic approaches (mass-difference theory and unlabeled-samples correction) need to be evaluated for accuracy and computational robustness.

## When NOT to use

- Input FAM data are already verified to be free from naturally occurring isotope and isotopic impurity contributions—in this case, MDV values need no correction.
- Instrument resolution is unknown or cannot be specified; the method's accuracy depends critically on accurate nominal resolution input.
- The tracer element is not present in all compounds in the dataset; the algorithm will report errors if a selected tracer element (e.g., 13C) is absent from some analyte formulas.

## Inputs

- LC-MS fractional abundances of measured isotopologues (FAM) in XLSX format
- Labeled sample data (e.g., test_labelN_sim.xlsx, test_labelS_sim.xlsx)
- Unlabeled sample data (optional, e.g., test_unlabelN_sim.xlsx, test_unlabelS_sim.xlsx)
- Source code implementing mass-difference-theory and unlabeled-samples approaches
- Instrument resolution specifications (nominal value, e.g., 140,000 or 280,000 for Orbitrap)
- Isotopic purity of tracer nutrient
- Tracer element identifier (13C, 2H, 15N, 18O, or 34S)

## Outputs

- Mass distribution vectors (MDV) for each compound and sample after correction
- Isotopic enrichment values
- Technical documentation with mathematical formulation and assumptions
- Numerical scheme comparison report (stability, accuracy, computational cost)
- Corrected XLSX file with MDV results in additional sheets
- Processing time benchmarks on reference hardware (e.g., 2.6 GHz Core i7)

## How to apply

Extract the mathematical formulation and numerical implementation of both correction approaches from source code and documentation. Compare how each scheme handles naturally occurring isotope contributions and isotopic impurity modeling, particularly the discretization and solution strategies for the correction matrix system. Document assumptions about instrument resolution effects (e.g., how peak overlap is modeled) and identify numerical instabilities or approximations. Validate improvements by running test datasets at known nominal resolutions (e.g., 140,000 and 280,000 for Orbitrap analyzers) and confirming that MDV outputs are monotonically dependent on instrument resolution—if resolution is extremely low, results should approach combinatorial methods; if extremely high, correction should approach zero. Measure processing time and stability across compounds with varying numbers of tracer atoms.

## Related tools

- **ElemCor** (Reference implementation of mass-difference-theory and unlabeled-samples numerical schemes; source for algorithm extraction and validation testing) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Baseline combinatorial correction method without resolution-effect modeling; used to validate that ElemCor numerical schemes reduce to IsoCor behavior at extreme low resolution)

## Evaluation signals

- MDV values are monotonically dependent on instrument resolution: at extremely low resolution, results match combinatorial methods (IsoCor); at extremely high resolution, correction approaches zero.
- Processing time on reference hardware (2.6 GHz Core i7) is <10 seconds for example datasets; timing scales predictably with number of compounds and tracer atoms.
- Corrected MDV values in output XLSX file sum to 1.0 for each compound and sample (mass balance constraint).
- Enrichment calculations derived from MDV are consistent across both correction approaches (mass-difference theory and unlabeled-samples) when both are applied.
- Numerical stability is verified: identical input files produce identical MDV outputs across multiple runs; no NaN or Inf values appear in output unless tracer element is absent from a compound formula.

## Limitations

- ElemCor currently prints only generic error messages; troubleshooting requires manual verification of tracer element selection and file format compliance (XLSX must be in same directory as executable).
- Unlabeled-samples approach is optional; when omitted, only mass-difference theory is applied, reducing correction robustness at moderate resolutions.
- The method assumes all compounds in labeled and unlabeled files have identical analyte sets and row counts; mismatches cause processing failures.
- FAM vector length is typically Nt+1 (where Nt = number of tracer atoms) but ElemCor can handle other lengths; non-standard lengths may require manual validation of interpretation.
- Processing time may exceed 1 minute if the wrong tracer element is selected (e.g., 15N data analyzed with C or S selected as tracer), producing no meaningful error context.

## Evidence

- [intro] ElemCor uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [intro] ElemCor corrects and improves the numerical schemes of both methods: "ElemCor corrects and improves the numerical schemes of both methods"
- [intro] Naturally occurring isotopes and isotopic impurity from the tracer contribute to measured isotopologue abundances: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] The example files shown in Fig. 2 can be processed within 10 seconds on a 2.6GHz Core i7 processor: "The example files shown in Fig. 2 can be processed within 10 seconds on a 2.6GHz Core i7 processor"
- [readme] Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only: "Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only"
- [readme] In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified.: "In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified."
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm"
