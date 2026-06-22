---
name: mass-distribution-vector-calculation
description: Use when you have raw LC-MS fractional abundances (FAM) data from isotope labeling experiments and need to obtain true mass distribution vectors (MDV) that represent only the isotopic labeling contribution.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - ElemCor
  - IsoCor
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

# mass-distribution-vector-calculation

## Summary

Transform measured fractional abundances of isotopologues (FAM) from LC-MS into corrected mass distribution vectors (MDV) by accounting for naturally occurring isotopes and isotopic impurity from the tracer. This correction is essential to extract true isotopic labeling contributions in stable isotope labeling experiments.

## When to use

Use this skill when you have raw LC-MS fractional abundances (FAM) data from isotope labeling experiments and need to obtain true mass distribution vectors (MDV) that represent only the isotopic labeling contribution. The input FAM must be in XLSX format with columns corresponding to compounds and rows representing M+0, M+1, …, M+Nt isotopologues, where Nt is the number of tracer atoms. Apply this skill before performing downstream metabolic flux analysis or enrichment calculations.

## When NOT to use

- Input FAM data are already corrected or have been processed by another correction tool without documentation of the method used.
- The tracer element is not present in the elemental composition of one or more target compounds (will cause algorithm error).
- FAM values do not sum to approximately 1.0 across all isotopologues (M+0 through M+Nt) for each sample, indicating malformed input data.

## Inputs

- Labeled sample fractional abundances of measured isotopologues (FAM) in XLSX format
- Unlabeled sample reference measurements in XLSX format (optional)
- Isotopic purity specification of nutrient tracer
- Nominal instrument resolution (e.g., 140,000 or 280,000)
- Mass analyzer type (e.g., Orbitrap)
- Tracer element identity (13C, 2H, 15N, 18O, or 34S)
- Elemental composition of target metabolites

## Outputs

- Mass distribution vectors (MDV) representing true isotopic labeling contribution
- Isotopic enrichment values for each compound and sample
- Fold change of pool size for different compounds and samples
- Corrected results stored in additional sheets of the input XLSX file
- Visual preview of FAM and MDV before and after correction in graphic interface

## How to apply

Load labeled sample FAM data (XLSX format) into ElemCor and specify the tracer element (13C, 2H, 15N, 18O, or 34S), the elemental composition of target metabolites, and the nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap). Optionally load unlabeled sample reference data to apply resolution-effect correction. ElemCor constructs a correction matrix by inverting the linear system that relates measured FAM to true MDV, accounting for naturally occurring isotopes and isotopic impurity profiles. The correction magnitude is monotonically dependent on instrument resolution: at extremely low resolution it behaves like IsoCor (combinatorics only), and at extremely high resolution performs minimal correction. Validate corrected MDV output for consistency and numerical stability, and verify that the tracer element is actually present in each compound formula.

## Related tools

- **ElemCor** (Primary software tool that implements correction matrix approach and dual resolution-effect correction methods (mass difference theory and unlabeled samples) to transform FAM to MDV) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Reference correction tool using combinatorics without resolution-effect consideration; ElemCor converges to IsoCor behavior at extremely low instrument resolution)

## Evaluation signals

- Corrected MDV values sum to 1.0 across all isotopologues (M+0 through M+Nt) for each compound and sample.
- MDV enrichment values are monotonically dependent on instrument resolution: lower resolution yields larger corrections; higher resolution yields corrections approaching zero.
- When unlabeled sample data are provided, the resolution-effect correction reduces systematic bias introduced by naturally occurring isotopes and tracer impurity.
- Processing completes within 1 minute on standard hardware (2.6 GHz Core i7 or equivalent); failure to complete suggests incorrect tracer element selection.
- Visual comparison of FAM vs. MDV in the graphic interface shows expected smoothing/spreading of abundance distribution after correction, consistent with the resolution and isotopic composition of the target compound.

## Limitations

- The software requires that labeled and unlabeled sample files have identical compounds and row counts; mismatches cause processing failure.
- ElemCor is sensitive to tracer element selection; specifying a tracer (e.g., 13C) that is not present in a compound formula, or loading data from a different tracer (e.g., 15N), will trigger an error.
- The correction matrix approach assumes linear relationships between measured FAM and true MDV; highly nonlinear or saturated mass spectra may produce unstable results.
- Installation requires network connection during MATLAB Compiler Runtime setup; subsequent use is offline-compatible.
- Current version provides only generic error messages; troubleshooting relies on manual verification of tracer selection, file location, and file format (XLSX).

## Evidence

- [readme] the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3).: "ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3)."
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] the algorithm will report error if the tracer element is not present in the compound: "the algorithm will report error if the tracer element is not present in the compound"
- [readme] FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues. Here Nt stands for the number of tracer atoms.: "FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues. Here Nt stands for the number of tracer atoms."
- [readme] The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples.: "The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples."
