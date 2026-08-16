---
name: resolution-effect-correction-unlabeled-samples
description: Use when when you have paired LC-MS data from both labeled (isotope-tracer
  dosed) and unlabeled (control) samples of the same analytes, and you want to correct
  FAM to true MDV while accounting for resolution effects from the mass spectrometer
  (especially relevant for high-resolution instruments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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

# Resolution-effect correction using unlabeled-sample reference method

## Summary

Correct LC-MS fractional abundances of measured isotopologues (FAM) to obtain mass distribution vectors (MDV) by applying the unlabeled-sample reference approach, which accounts for naturally occurring isotopes and isotopic impurity contributions using measured unlabeled control data rather than mass difference theory.

## When to use

When you have paired LC-MS data from both labeled (isotope-tracer dosed) and unlabeled (control) samples of the same analytes, and you want to correct FAM to true MDV while accounting for resolution effects from the mass spectrometer (especially relevant for high-resolution instruments like Orbitraps where resolution effects are substantial).

## When NOT to use

- When unlabeled reference samples are not available; use mass difference theory method instead.
- When FAM data have already been corrected using another method (e.g., IsoCor output); avoid double-correction.
- When the tracer element is absent from one or more compounds in the dataset, as ElemCor will report errors during processing.

## Inputs

- Fractional abundances of measured isotopologues (FAM) from labeled samples in XLSX format (columns = samples, rows = isotopologues m+0 through m+Nt)
- Fractional abundances of measured isotopologues (FAM) from unlabeled (control) samples in XLSX format (same analytes and row count as labeled data)
- Isotopic purity of tracer nutrient (scalar, typical range 0.9–0.99)
- Nominal instrument resolution (e.g., 140000 or 280000 for Orbitrap)
- Tracer element identifier (13C, 2H, 15N, 18O, or 34S)
- Mass analyzer type (e.g., Orbitrap)

## Outputs

- Mass distribution vectors (MDV) for each compound and sample, representing true isotopic labeling contribution (corrected FAM)
- Isotopic enrichment values for each compound
- Fold change of pool size for different compounds and samples
- Corrected data saved in additional sheets within the original XLSX file

## How to apply

Load both labeled sample FAM data and corresponding unlabeled sample reference measurements in XLSX format into ElemCor. Specify the isotopic purity of the nutrient tracer, the nominal instrument resolution (e.g., 140,000 or 280,000 for Orbitrap), and select the tracer element (13C, 2H, 15N, 18O, or 34S). ElemCor applies the unlabeled-sample correction algorithm (Reference 3 approach) by using the measured isotopologue abundances from unlabeled samples to empirically model and remove resolution-induced cross-contributions between m/z bins. The algorithm then transforms the corrected FAM into MDV representing only the contribution from isotopic labeling. Validate the corrected MDV output for numerical stability and consistency with expected isotope enrichment patterns.

## Related tools

- **ElemCor** (Primary execution tool that implements the unlabeled-sample correction algorithm and generates corrected MDV and enrichment outputs) — https://github.com/4dsoftware/elemcor

## Evaluation signals

- MDV values are normalized (sum to 1.0) and lie in [0, 1] per compound per sample.
- Corrected MDV shows expected enrichment pattern consistent with the tracer isotope applied (e.g., peak shift toward higher m/z for 13C labeling).
- Unlabeled sample MDV should remain near m+0 ≈ 1.0 with minimal enrichment in higher isotopologues, confirming reference correction was applied.
- Processing completes within ~10–60 seconds on standard hardware without error messages; timeouts or errors typically indicate wrong tracer element selection.
- Fold change in pool size is a positive scalar; negative or zero values indicate algorithmic failure.

## Limitations

- Both labeled and unlabeled files must contain the same set of analytes and the same number of rows; mismatches cause processing failure.
- Tracer element must be present in all compounds; absence in any compound causes the algorithm to fail.
- Current version provides only generic error messages; troubleshooting requires manual verification of tracer selection and file consistency.
- XLSX file must reside in the same directory as the ElemCor executable.
- At extremely low instrument resolution, unlabeled-sample correction approaches IsoCor behavior; at extremely high resolution, minimal correction is performed.

## Evidence

- [readme] Fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling.: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM): "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] ElemCor uses two different approaches to account for resolution effect, mass difference theory, and unlabeled samples: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] In Steps 1 and 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only.: "In Steps 1 and 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only."
- [readme] The final results are previewed in the graphic interface. They are automatically saved into additional sheets in the original XLSX file. The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples.: "The final results are previewed in the graphic interface. They are automatically saved into additional sheets in the original XLSX file. The final results include, MDV, enrichment, and fold change of"
- [readme] Check if the labeled and unlabeled files have the same analytes and the same number of rows.: "Check if the labeled and unlabeled files have the same analytes and the same number of rows."
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm"
