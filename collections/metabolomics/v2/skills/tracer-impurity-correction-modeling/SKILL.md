---
name: tracer-impurity-correction-modeling
description: Use when when processing LC-MS data from isotope labeling experiments where the tracer (13C, 2H, 15N, 18O, or 34S) has known isotopic impurity and you observe discrepancies between measured isotopologue abundances (FAM) and expected labeling patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - ElemCor
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
---

# tracer-impurity-correction-modeling

## Summary

Model and correct for isotopic impurity in stable isotope tracers by constructing and applying a correction matrix that maps measured fractional abundances of isotopologues (FAM) to true mass distribution vectors (MDV) in LC-MS isotope labeling experiments. This skill accounts for both naturally occurring background isotopes and deviation from theoretical tracer purity.

## When to use

When processing LC-MS data from isotope labeling experiments where the tracer (13C, 2H, 15N, 18O, or 34S) has known isotopic impurity and you observe discrepancies between measured isotopologue abundances (FAM) and expected labeling patterns. Apply this when tracer purity is ≤99% or when unlabeled reference samples are available to characterize instrumental resolution effects.

## When NOT to use

- If FAM have already been corrected by another method (e.g., IsoCor); avoid double-correction.
- If the tracer element is absent from the target metabolite's elemental composition; the algorithm will fail with an error.
- If instrument resolution is extremely high (>500,000 m/z) and natural isotope contribution is negligible; correction becomes nearly null and introduces unnecessary numerical overhead.

## Inputs

- Measured fractional abundances of isotopologues (FAM) from LC-MS, stored as column vectors in XLSX format
- Elemental composition and natural isotope abundance table for the target metabolite
- Tracer isotopic purity specification (percentage of desired isotope, e.g., 99% for 13C tracer)
- Optional: unlabeled reference sample FAM at the same instrument resolution
- Instrument mass analyzer type (e.g., Orbitrap) and nominal resolution (e.g., 140,000 or 280,000 m/z)

## Outputs

- Correction matrix (inverted linear transformation) mapping FAM to MDV
- Mass distribution vectors (MDV) for each compound and sample, corrected for natural isotopes and tracer impurity
- Isotopic enrichment values per compound
- Fold change of pool size estimates

## How to apply

First, define the elemental composition and natural isotope abundances of the target metabolite. Second, generate a theoretical isotope distribution matrix using multinomial expansion or convolution methods, accounting for all naturally occurring isotopes at their natural abundances. Third, incorporate the tracer's isotopic impurity profile (e.g., residual 12C in a 13C tracer) into the model. Fourth, construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV; the correction accounts for instrument resolution (140,000 to 280,000 m/z on Orbitrap analyzers) by using either mass difference theory (Ref. 2) or unlabeled sample calibration (Ref. 3). Fifth, validate by testing on simulated data with known labeling patterns or reference compounds. Apply the inverted correction matrix to your experimental FAM to recover MDV.

## Related tools

- **ElemCor** (Primary software tool implementing correction matrix approach; handles FAM input in XLSX format, accounts for resolution and tracer impurity, and outputs corrected MDV and enrichment) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- Corrected MDV sums to 1.0 across all isotopologues (M+0 through M+Nt) for each compound and sample.
- FAM and MDV are stored in separate sheets in the output XLSX file; visual inspection confirms that MDV values are lower at low m/z and higher at high m/z compared to raw FAM, consistent with natural isotope removal.
- When tested on simulated data with known labeling patterns (e.g., test_labelN_sim.xlsx), corrected enrichment values match expected theoretical enrichment within measurement uncertainty.
- Processing time is <60 seconds for typical metabolomics datasets on standard hardware (e.g., 2.6 GHz Core i7); timeout or error suggests incorrect tracer selection.
- Correction magnitude is monotonically dependent on instrument resolution: lower resolution (e.g., 140,000) produces larger corrections; higher resolution produces smaller corrections, approaching zero at >500,000 m/z.

## Limitations

- ElemCor requires correct tracer element selection; mismatched tracer (e.g., selecting C when 15N data are loaded) causes algorithm failure because some metabolites may lack the selected element.
- Labeled and unlabeled input files must have identical analytes, row counts, and column structure; mismatched file formats prevent processing.
- FAM length can differ from Nt + 1 (where Nt = number of tracer atoms), but ElemCor requires explicit specification; non-standard FAM lengths may produce unintuitive results.
- Installation requires MATLAB Compiler Runtime and network connectivity during setup; offline use is supported after initial installation.
- No version control or changelog is provided; tracking algorithm changes or reproducibility across tool versions is difficult.

## Evidence

- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be"
- [readme] ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3): "ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3)"
- [other] Define the elemental composition and natural isotope abundances for the target metabolite. Generate the theoretical isotope distribution matrix accounting for all naturally occurring isotopes using multinomial expansion or similar convolution method.: "Define the elemental composition and natural isotope abundances for the target metabolite. Generate the theoretical isotope distribution matrix accounting for all naturally occurring isotopes using"
- [other] Incorporate tracer isotopic impurity profiles into the isotope distribution model. Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV.: "Incorporate tracer isotopic impurity profiles into the isotope distribution model. Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV"
- [readme] In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected. In addition to 13C, 2H, and 15N, ElemCor allows 18O and 34S as the tracer element for correction. PLEASE MAKE SURE THE CORRECT TRACER IS SELECTED!: "In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected. In addition to 13C, 2H, and 15N, ElemCor allows 18O and 34S as the"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction perform by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
