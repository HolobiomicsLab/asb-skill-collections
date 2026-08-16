---
name: fractional-abundance-transformation
description: Use when you have raw LC-MS fractional abundances of isotopologues (FAM)
  from a stable isotope labeling experiment (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0121
  tools:
  - ElemCor
  techniques:
  - LC-MS
  license_tier: open
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

# Fractional Abundance Transformation via Correction Matrix

## Summary

Transform measured fractional abundances of isotopologues (FAM) from LC-MS into corrected mass distribution vectors (MDV) by constructing and applying a correction matrix that accounts for naturally occurring isotopes, isotopic impurity from the tracer, and instrument resolution effects. This is essential for accurate quantification of isotopic labeling in metabolic flux analysis.

## When to use

You have raw LC-MS fractional abundances of isotopologues (FAM) from a stable isotope labeling experiment (e.g., 13C, 15N, 2H, 18O, or 34S tracer) and need to extract the true mass distribution vector (MDV) contribution from experimental labeling by removing confounding signals from natural isotope abundances and tracer impurity. Apply this skill when instrument resolution, elemental composition, and tracer purity are known or measurable.

## When NOT to use

- FAM data are already corrected (e.g., by another tool such as IsoCor or FluxFix); applying a second correction matrix will introduce over-correction artifacts.
- The tracer element is not present in the target metabolite formula; ElemCor will report an error and halt processing.
- Instrument resolution is not known or is drastically different from the parameters supplied; correction magnitude will be inaccurate.

## Inputs

- Measured fractional abundances of isotopologues (FAM) from LC-MS, typically length Nt+1 where Nt is the number of tracer atoms, but other lengths are acceptable
- Elemental composition of target metabolites
- Natural isotope abundances for all elements in the metabolite
- Tracer element identity (13C, 2H, 15N, 18O, or 34S) and isotopic purity (%)
- Instrument mass analyzer type (e.g., Orbitrap)
- Nominal instrument resolution (e.g., 140,000 or 280,000)
- Unlabeled (background) sample FAM data (optional; enables resolution effect correction)

## Outputs

- Mass distribution vectors (MDV) for each compound and sample, corrected for natural isotope contribution and tracer impurity
- Isotopic enrichment values per compound
- Fold change of pool size per compound (relative to unlabeled control, if provided)
- Correction matrix used for the transformation (for validation and reproducibility)
- Pre- and post-correction FAM and MDV for each analyte (typically saved in additional sheets of the input XLSX file)

## How to apply

Define the elemental composition and natural isotope abundance profile for each target metabolite. Generate the theoretical isotope distribution matrix by multinomial expansion or convolution, accounting for all naturally occurring isotopes at their natural abundances. Incorporate the tracer isotopic impurity profile into the model. Construct the correction matrix by inverting or solving the linear system that relates measured FAM to true MDV. The correction magnitude depends monotonically on instrument resolution: at extremely low resolution, the matrix approaches the combinatorial (IsoCor) limit; at extremely high resolution, minimal correction is applied. Apply the correction matrix to measured FAM data to obtain MDV. Validate by testing on reference or simulated data with known labeling patterns, ensuring that compounds contain the selected tracer element and that labeled and unlabeled files have identical analytes and row counts.

## Related tools

- **ElemCor** (Primary tool implementing correction matrix approach for FAM-to-MDV transformation, accounting for resolution effect, mass difference theory, and unlabeled sample profiles) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- MDV values for each isotopologue sum to 1.0 (mass balance invariant)
- Corrected MDV at M+0 is lower than measured FAM at M+0 (natural abundance correction reduces the zero-label population)
- Enrichment values are within expected range for the tracer dose and biological pathway (e.g., 0–100% 13C enrichment for a 13C tracer)
- Pre- and post-correction results shown in the graphic interface match the saved output sheets in the XLSX file
- Test on simulated data with known labeling patterns produces MDV that match the ground truth within numerical precision (typically <1% deviation)

## Limitations

- ElemCor requires MATLAB Compiler Runtime; source code collaboration needed for integration into non-MATLAB pipelines
- If the tracer element is not present in the compound formula, the algorithm will report a general error without specific diagnostics; users must manually verify tracer selection and compound elemental composition
- Processing time scales with the number of compounds and complexity of elemental composition; large datasets (thousands of metabolites) may require optimization
- Correction accuracy depends critically on accurate knowledge of instrument resolution, tracer isotopic purity, and elemental composition; misspecification of these parameters (e.g., selecting 13C as tracer when 15N data are loaded) leads to silent or obvious failures
- Current version provides only generic error messages; troubleshooting typically requires manual verification of tracer element, file format, and data alignment

## Evidence

- [readme] The fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling.: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV)"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, FAM must be corrected.: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] ElemCor is based on the correction matrix approach and uses two different approaches to account for resolution effect, mass difference theory, and unlabeled samples.: "ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3)"
- [readme] When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction performed by ElemCor is monotonically dependent on instrument resolution.: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] If the tracer element is not present in the compound, the algorithm will report an error.: "This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound."
- [readme] FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues, but ElemCor is able to handle FAM that has a length other than Nt + 1.: "FAM typically has a length of Nt + 1 to cover M+0, M+1, ..., M+Nt isotopologues. Here Nt stands for the number of tracer atoms. But ElemCor is able to handle FAM that has a length other than Nt + 1,"
- [readme] The final results include MDV, enrichment, and fold change of pool size for different compounds and samples, saved into additional sheets in the original XLSX file.: "The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples."
- [readme] In Step 2, unlabeled data loading is optional; when it is not performed, ElemCor runs based on mass difference theory only.: "Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only."
