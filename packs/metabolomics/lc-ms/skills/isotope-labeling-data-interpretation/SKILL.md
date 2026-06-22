---
name: isotope-labeling-data-interpretation
description: Use when you have LC-MS FAM measurements from an isotope-labeling experiment and need to correct them to obtain true MDV values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Implement the mass difference theory resolution-effect correction approach

## Summary

Apply mass-difference theory to correct LC-MS fractional abundances of measured isotopologues (FAM) into mass distribution vectors (MDV) by accounting for naturally occurring isotopes, isotopic impurity, and instrument resolution effects. This approach transforms raw instrument data into accurate representations of metabolic labeling contributions.

## When to use

You have LC-MS FAM measurements from an isotope-labeling experiment and need to correct them to obtain true MDV values. Specifically, use this skill when: (1) your instrument resolution is neither extremely low nor extremely high (ElemCor performs correction monotonically dependent on resolution); (2) you cannot obtain or do not want to use unlabeled sample data; or (3) you want to apply a mathematically principled approach grounded in mass-difference theory rather than combinatorial methods.

## When NOT to use

- Your input FAM are already corrected or are pool-size normalized; do not apply this skill to already-processed MDV data.
- You have extremely low instrument resolution and combinatorial correction (IsoCor-style) is sufficient; ElemCor becomes identical to IsoCor under such conditions.
- The tracer element is not present in one or more compounds in your dataset; the algorithm will report an error and fail to process.

## Inputs

- LC-MS fractional abundances of measured isotopologues (FAM) in XLSX format with one column per sample and one row per compound
- Isotopic purity specification for the tracer element
- Nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap)
- Tracer element identifier (13C, 2H, 15N, 18O, or 34S)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Mass distribution vectors (MDV) corrected for naturally occurring isotopes and isotopic impurity
- Isotopic enrichment values per compound and sample
- Fold change of pool size per compound and sample
- XLSX file with original FAM and corrected MDV in separate sheets for comparison

## How to apply

Extract the mathematical formulation of the mass-difference-theory method from ElemCor source code and documentation, including how naturally occurring isotopes and isotopic impurity contributions are modeled in relation to instrument resolution. Load your LC-MS data in XLSX format with FAM as column vectors corresponding to all compounds in each sample. Specify the isotopic purity of the nutrient tracer, the nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap analyzers), and select the correct tracer element (13C, 2H, 15N, 18O, or 34S). ElemCor will apply the mass-difference-theory correction algorithm—which corrects and improves the numerical schemes of prior methods—to transform FAM measurements into corrected MDV values. The output MDV, enrichment, and fold-change metrics are saved to additional sheets in your input XLSX file and displayed in the graphic interface for compound-by-compound verification.

## Related tools

- **ElemCor** (Primary tool implementing mass-difference theory correction for LC-MS isotope-labeling data; performs numerical scheme improvements over existing methods and outputs corrected MDV from FAM input) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- Corrected MDV values sum to 1.0 across all isotopologue masses (M+0, M+1, ..., M+Nt) for each compound and sample.
- MDV enrichment values are consistent with the known or expected labeling pattern from the tracer element and isotopic purity.
- FAM and MDV are both displayed for the same compound in the graphic interface, showing visually that naturally occurring isotope peaks have been attenuated in the MDV relative to FAM.
- Processing completes within expected time (≤1 minute for typical datasets on standard processors) without error messages about missing tracer elements.
- Comparison with combinatorial (IsoCor-style) correction shows monotonically increasing differences as instrument resolution increases from extremely low to extremely high values.

## Limitations

- FAM must have length Nt + 1 to cover M+0 through M+Nt isotopologues; while ElemCor can technically handle other lengths, results may be unpredictable.
- All compounds in labeled and unlabeled datasets must be identical and have the same number of rows; mismatches will cause processing failure.
- The tracer element must be present in every compound; if a compound lacks the selected tracer element (e.g., S-free compound when 34S is selected as tracer), the algorithm will error.
- Results are highly sensitive to correct tracer element selection; selecting the wrong tracer (e.g., C when 15N data were loaded) will produce incorrect or no output.
- No changelog is available; version history and bug-fix details are not documented.

## Evidence

- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be"
- [readme] ElemCor uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] ElemCor corrects and improves the numerical schemes of both methods: "ElemCor corrects and improves the numerical schemes of both methods"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] In Step 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only.: "Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only."
- [readme] In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified.: "In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified."
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm"
