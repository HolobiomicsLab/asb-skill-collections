---
name: isotopologue-distribution-matrix-construction
description: Use when when you have measured fractional abundances of isotopologues
  (FAM) from LC-MS in an isotope labeling experiment and need to correct them to obtain
  true mass distribution vectors (MDV) that reflect only the labeling contribution,
  accounting for background from naturally occurring isotopes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - ElemCor
  - IsoCor
  - FluxFix
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

# Reconstruct the correction matrix for natural isotope abundance correction of FAM

## Summary

Construct a correction matrix that transforms measured fractional abundances of isotopologues (FAM) into corrected mass distribution vectors (MDV) by accounting for naturally occurring isotopes and isotopic impurity from the tracer. This matrix-based approach enables accurate quantification of isotopic labeling contributions in LC-MS experiments.

## When to use

When you have measured fractional abundances of isotopologues (FAM) from LC-MS in an isotope labeling experiment and need to correct them to obtain true mass distribution vectors (MDV) that reflect only the labeling contribution, accounting for background from naturally occurring isotopes and tracer impurity. Essential when instrument resolution is neither extremely low nor extremely high, as the correction magnitude depends monotonically on resolution.

## When NOT to use

- FAM data are already corrected or are already presented as MDV; applying the matrix again will introduce errors.
- Tracer element identity is unknown or has not been pre-selected; the algorithm will fail or produce nonsensical enrichment if a compound lacks the chosen tracer element.
- Instrument resolution is extremely low (< ~10,000) or extremely high (infinite), as the correction becomes identical to combinatoric-only methods or vanishes entirely, making the matrix approach redundant.

## Inputs

- Elemental composition of target metabolite (e.g., C6H12O6 for glucose)
- Natural isotope abundances table for all elements in the metabolite
- Tracer element identity and isotopic purity (e.g., 13C purity ≥99%)
- Nominal instrument mass resolution (e.g., 140,000 or 280,000)
- Measured fractional abundances of isotopologues (FAM) vector from LC-MS
- Unlabeled sample FAM (optional, improves correction accuracy)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Correction matrix (square matrix mapping FAM to MDV space)
- Mass distribution vector (MDV) for each compound and sample
- Isotopic enrichment values (atom percent excess or mole fraction)
- Fold change of metabolite pool size (where applicable)

## How to apply

First, define the elemental composition and natural isotope abundances for your target metabolite. Second, generate the theoretical isotope distribution matrix using multinomial expansion or convolution to account for all naturally occurring isotopes at your instrument's nominal resolution (140,000–280,000 for Orbitrap). Third, incorporate the tracer element's isotopic purity profile into the model—this is critical and must match the actual tracer used (13C, 2H, 15N, 18O, or 34S). Fourth, construct the correction matrix by inverting or solving the linear system that maps measured FAM to true MDV; if unlabeled sample data are available, include them to improve accuracy via the mass difference theory approach. Finally, validate by testing on reference or simulated data with known labeling patterns, verifying that MDV values fall within expected ranges and that enrichment calculations are sensible.

## Related tools

- **ElemCor** (Software tool that implements the correction matrix approach with two methods (mass difference theory and unlabeled sample normalization) to correct FAM to MDV for isotope labeling experiments) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Predecessor tool performing correction via combinatorics alone, without accounting for resolution effect; ElemCor improves upon its numerical schemes)
- **FluxFix** (Related tool for automatic isotopologue normalization in metabolic tracer analysis)

## Evaluation signals

- Correction matrix is square (dimensions n × n, where n = number of isotopologues measured) and invertible; determinant is non-zero.
- MDV sums to 1.0 ± 1e-6 for each compound (mass conservation check).
- MDV M+0 value for unlabeled samples is ≈ natural abundance baseline; labeled samples show expected enrichment shift consistent with tracer purity and labeling pattern.
- Enrichment values are non-negative and ≤ 100% atom percent excess; fold-change values are positive and within biologically plausible ranges (typically 0.5–5).
- Validation on reference simulated data (provided test files: test_labelN_sim.xlsx, test_labelS_sim.xlsx) produces MDV within ±2% of ground truth for N and S tracers at 140k and 280k resolution.

## Limitations

- Algorithm requires correct tracer element to be pre-selected; if FAM data contain 15N labeling but 13C is selected as the tracer, the tool fails or produces incorrect results because some compounds may lack the chosen element.
- Only supports five tracer elements: 13C, 2H, 15N, 18O, and 34S; other stable isotopes are not implemented.
- FAM length must be compatible with the metabolite composition; FAM vectors of atypical length (not Nt+1, where Nt = number of tracer atoms) require special handling and may reduce numerical stability.
- Correction magnitude is monotonically dependent on instrument resolution; extremely low resolution (< 10k) converges to combinatoric-only methods, and extremely high resolution (infinite) produces no correction, limiting applicability range.
- Processing time scales with compound complexity; some pathological cases may exceed 1 minute on standard hardware if the tracer element is absent in unexpected ways.

## Evidence

- [readme] the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) must be corrected: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [other] Generate the theoretical isotope distribution matrix accounting for all naturally occurring isotopes using multinomial expansion or similar convolution method.: "Generate the theoretical isotope distribution matrix accounting for all naturally occurring isotopes using multinomial expansion or similar convolution method"
- [other] Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV.: "Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV"
- [readme] ElemCor uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all"
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula"
