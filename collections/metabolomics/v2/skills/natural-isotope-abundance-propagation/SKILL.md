---
name: natural-isotope-abundance-propagation
description: Use when you have LC-MS fractional abundances of measured isotopologues (FAM) from a stable isotope labeling experiment and need to recover the true mass distribution vectors (MDV) that reflect only the contribution from the isotopic tracer. Use this skill when naturally occurring isotopes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# natural-isotope-abundance-propagation

## Summary

Correct measured fractional abundances of isotopologues (FAM) from LC-MS data to obtain true mass distribution vectors (MDV) by accounting for naturally occurring isotopes and isotopic impurity from the tracer. This correction is essential for accurate quantification of isotopic labeling in metabolic flux analysis.

## When to use

You have LC-MS fractional abundances of measured isotopologues (FAM) from a stable isotope labeling experiment and need to recover the true mass distribution vectors (MDV) that reflect only the contribution from the isotopic tracer. Use this skill when naturally occurring isotopes (e.g., ¹³C background in ¹²C-enriched samples, ¹⁵N background) and isotopic impurity from the tracer contaminate your raw measurements, and you must account for both instrument resolution effects and unlabeled sample backgrounds.

## When NOT to use

- FAM data already corrected by another method (e.g., already normalized to MDV by IsoCor or FluxFix)—applying this skill a second time will over-correct.
- Tracer element is absent from the target metabolite formula—the algorithm will report an error and halt execution.
- Input data use a format other than XLSX or are not organized with one column vector per compound sample.

## Inputs

- Measured fractional abundances of isotopologues (FAM) from LC-MS as XLSX spreadsheet (labeled samples)
- Unlabeled sample data as XLSX spreadsheet (optional, for background normalization)
- Elemental composition of target metabolite
- Natural isotope abundances for elements in metabolite
- Tracer isotopic purity specification (e.g., atom percent excess or mole fraction)
- Nominal instrument resolution (e.g., 140,000 or 280,000)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Corrected mass distribution vectors (MDV) for each compound and sample
- Isotopic enrichment values
- Fold change of pool size relative to reference
- Visualizations of FAM vs. MDV before and after correction
- Results stored in new sheets within the input XLSX file

## How to apply

Construct a correction matrix that maps measured FAM to true MDV by (1) defining the elemental composition and natural isotope abundances for the target metabolite; (2) generating the theoretical isotope distribution matrix using multinomial expansion to account for all naturally occurring isotopes; (3) incorporating tracer isotopic impurity profiles into the model; (4) inverting or solving the linear system relating measured FAM to true MDV; and (5) applying the correction matrix to your experimental FAM data. The correction is resolution-dependent: specify the nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap analyzers) and select the correct tracer element (¹³C, ²H, ¹⁵N, ¹⁸O, or ³⁴S). Optionally load unlabeled sample data to account for background signal; if omitted, correction uses mass difference theory alone. Store results (MDV, enrichment, fold change) in separate sheets of the input XLSX file and validate against reference or simulated data with known labeling patterns.

## Related tools

- **ElemCor** (Implements the correction matrix method to map FAM to MDV; accounts for resolution effect, mass difference theory, and unlabeled samples; improves numerical schemes over predecessor methods.) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- MDV sums to 1.0 (or very close, within floating-point tolerance) for each compound and sample after correction.
- Corrected MDV for unlabeled or reference samples with zero tracer enrichment returns M+0 ≈ 1.0 and M+k ≈ 0 for k > 0.
- FAM and MDV profiles differ visibly in the graphical interface, with MDV showing sharper labeling patterns when resolution effect is significant; no visible change indicates extremely high instrument resolution.
- Processing time is <1 minute on modern hardware (2.6 GHz Core i7 or equivalent); timeouts suggest incorrect tracer element selection.
- Enrichment values (atom percent excess) are consistent with known labeling patterns in positive controls or simulated datasets.

## Limitations

- FAM length must be at least 1 (M+0) and at most Nt + 1 (where Nt = number of tracer atoms); values outside this range may produce spurious results. ElemCor can handle non-standard FAM lengths, but validity depends on the input data.
- Correction is monotonically dependent on instrument resolution: at extremely low resolution, ElemCor behaves identically to combinatorics-only methods (e.g., IsoCor); at extremely high resolution, no correction is applied.
- Labeled and unlabeled input files must contain identical analytes and row counts; mismatches cause the algorithm to fail with a generic error message.
- Only supports single tracer elements (¹³C, ²H, ¹⁵N, ¹⁸O, or ³⁴S) per run; dual-tracer experiments require separate corrections or external preprocessing.
- The current version provides limited diagnostic output; if processing fails, troubleshooting requires manual verification of tracer selection, file location, and format compliance.

## Evidence

- [readme] the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3): "ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3)"
- [readme] In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected. In addition to 13C, 2H, and 15N, ElemCor allows 18O and 34S as the tracer element: "isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected. In addition to 13C, 2H, and 15N, ElemCor allows 18O and 34S"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all"
- [other] Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV.: "Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV"
- [readme] Check if correct tracer element is selected... If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula"
- [readme] FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues. Here Nt stands for the number of tracer atoms. But ElemCor is able to handle FAM that has a length other than Nt + 1, and the answer is Yes.: "FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues. Here Nt stands for the number of tracer atoms"
