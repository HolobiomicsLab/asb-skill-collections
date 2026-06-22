---
name: naturally-occurring-isotope-contribution-accounting
description: Use when you have raw fractional abundances of measured isotopologues (FAM) from LC-MS instruments in an isotope labeling experiment and need to correct them to obtain true mass distribution vectors (MDV) reflecting only the contribution from the isotopic tracer.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0625
  tools:
  - ElemCor
  - IsoCor
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

# naturally-occurring-isotope-contribution-accounting

## Summary

Account for naturally occurring isotopes and isotopic impurity from tracers when correcting LC-MS fractional abundances of measured isotopologues (FAM) to obtain accurate mass distribution vectors (MDV) in stable isotope labeling experiments. This skill is essential because FAM measurements are contaminated by background isotopic contributions that must be modeled and removed before labeling enrichment can be calculated.

## When to use

Use this skill when you have raw fractional abundances of measured isotopologues (FAM) from LC-MS instruments in an isotope labeling experiment and need to correct them to obtain true mass distribution vectors (MDV) reflecting only the contribution from the isotopic tracer. Specifically, apply it when naturally occurring isotopes (e.g., background ¹³C, ¹⁵N, ¹⁸O) or isotopic impurity from the tracer itself are known or suspected to contaminate the measured abundances, obscuring the true labeling pattern.

## When NOT to use

- Input FAM is already corrected or comes from a low-resolution instrument where naturally occurring isotope contribution is negligible.
- Tracer identity is unknown or cannot be determined from the experimental design; ElemCor requires explicit tracer specification and will fail or produce meaningless results if the tracer element is absent from a compound's formula.
- Input data are not in XLSX format or do not follow the standard column-vector layout (one compound per column); the software will not parse malformed files.

## Inputs

- XLSX spreadsheet with FAM (fractional abundances of measured isotopologues) vectors, one column per compound
- Tracer element identity (¹³C, ²H, ¹⁵N, ¹⁸O, or ³⁴S)
- Isotopic purity of the tracer nutrient (as a percentage or fraction)
- Nominal instrument resolution (e.g., 140000 or 280000 FWHM for Orbitrap)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- MDV (mass distribution vectors): corrected isotopologue abundances reflecting tracer labeling only
- Isotopic enrichment values per compound
- Fold change of metabolite pool size (optional)
- XLSX file with original and corrected data in separate sheets

## How to apply

Load labeled sample FAM data (in XLSX format with one column vector per compound) and specify the tracer element (¹³C, ²H, ¹⁵N, ¹⁸O, or ³⁴S), its isotopic purity, and the nominal instrument resolution of the mass analyzer (e.g., 140,000 or 280,000 for Orbitrap). ElemCor uses the correction matrix method combined with either mass-difference theory or unlabeled-sample approach to model how naturally occurring isotopes and impurity distribute across isotopologues at the instrument's measured resolution. Apply the selected correction algorithm (mass-difference theory is recommended when unlabeled samples are unavailable) to transform each FAM vector into a corrected MDV. The correction magnitude depends monotonically on instrument resolution: extremely low resolution yields results identical to IsoCor (combinatoric-only correction), while high resolution performs minimal correction because resolution blurring is minimal.

## Related tools

- **ElemCor** (Primary software implementing mass-difference theory and unlabeled-sample correction approaches to account for naturally occurring isotope and impurity contributions in LC-MS isotope labeling data) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Prior correction tool using combinatorics without resolution-effect modeling; ElemCor extends this approach by incorporating instrument resolution)

## Evaluation signals

- Corrected MDV values sum to 1.0 (conservation of mass) and MDV[0] (unlabeled isotopologue) is reduced relative to raw FAM[0], indicating successful subtraction of naturally occurring background.
- MDV length matches Nt + 1 (where Nt is the number of tracer atoms) or is appropriately handled if FAM has non-standard length; software accepts both standard and non-standard FAM lengths.
- Isotopic enrichment values are physically plausible (0 ≤ enrichment ≤ 100%) and consistent with the expected tracer labeling pattern and tracer purity.
- Correction magnitude scales monotonically with instrument resolution: higher resolution yields smaller corrections (closer to raw FAM), lower resolution yields larger corrections (approaching IsoCor-like behavior).
- Processing time is <1 minute on typical CPU (2.6 GHz Core i7 or equivalent); timeouts or errors suggest incorrect tracer element selection or malformed input data.

## Limitations

- Software requires correct tracer element selection; if the tracer is not present in a compound's chemical formula, the algorithm will report an error and fail to process that compound.
- Labeled and unlabeled sample files must have identical analytes and row counts; mismatched structure prevents processing.
- The unlabeled-sample correction approach requires collection of parallel unlabeled control samples, which may not always be available; mass-difference theory is the fallback when unlabeled data are absent.
- Software only prints a general error message in the current version; troubleshooting requires manual verification of tracer selection, file location, and data format.
- MATLAB Compiler Runtime or MATLAB installation is required to run the compiled executable; the tool is not portable to non-Windows environments without source code modification.

## Evidence

- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling.: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be"
- [readme] ElemCor is based on the correction matrix and uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples. ElemCor corrects and improves the numerical schemes of both methods.: "ElemCor is based on the correction matrix and uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples. ElemCor corrects and improves the numerical"
- [readme] In Step 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only. In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected.: "Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only. In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4,"
- [readme] IsoCor performs correction based on combinatorics without considering resolution effect. When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound."
