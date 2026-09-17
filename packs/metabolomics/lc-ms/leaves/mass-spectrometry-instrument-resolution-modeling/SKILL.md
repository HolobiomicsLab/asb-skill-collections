---
name: mass-spectrometry-instrument-resolution-modeling
description: Use when when correcting LC-MS fractional abundances of measured isotopologues
  (FAM) from isotope labeling experiments where instrument resolution (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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

# mass-spectrometry-instrument-resolution-modeling

## Summary

Model and correct for instrument resolution effects in LC-MS isotope labeling data using mass-difference theory to transform measured fractional abundances (FAM) into accurate mass distribution vectors (MDV). This approach accounts for naturally occurring isotopes and tracer isotopic impurity contributions that distort measured isotopologue peaks.

## When to use

When correcting LC-MS fractional abundances of measured isotopologues (FAM) from isotope labeling experiments where instrument resolution (e.g., 140,000 or 280,000 m/Δm on an Orbitrap) causes peak overlap and isotopic impurity from the tracer, and you need accurate mass distribution vectors (MDV) to quantify true isotopic labeling contribution. This is required before metabolic flux analysis calculations.

## When NOT to use

- Input FAM data are already corrected or represent MDV directly—do not re-correct.
- Instrument resolution is unknown or unmeasured; the correction is monotonically dependent on resolution specification and will produce meaningless results if specified resolution is incorrect.
- Tracer element is not present in all compounds in the dataset—select a different tracer or subset the data.

## Inputs

- Labeled sample FAM data (XLSX spreadsheet, columns = samples, rows = compounds, values = fractional abundances M+0 to M+Nt)
- Nominal instrument resolution (integer, e.g., 140000 or 280000)
- Tracer element identifier (13C, 2H, 15N, 18O, or 34S)
- Mass analyzer type (e.g., Orbitrap)
- Isotopic purity of nutrient/tracer (fraction or percentage)
- Unlabeled sample FAM data (XLSX, same structure; optional)

## Outputs

- Corrected mass distribution vectors (MDV) for each compound and sample
- Isotopic enrichment values per compound
- Fold-change in pool size relative to unlabeled baseline (if unlabeled data provided)
- Updated XLSX file with MDV and enrichment in new sheets

## How to apply

Load labeled sample FAM data (XLSX format, one column vector per compound) and specify the nominal instrument resolution and tracer element (13C, 2H, 15N, 18O, or 34S). Apply the mass-difference-theory correction matrix, which models naturally occurring isotope abundances and tracer isotopic impurity as linear contributions to the measured FAM. The algorithm solves for corrected MDV values by inverting or regularizing the correction matrix; the method is resolution-dependent—at extremely low resolution it converges to combinatorial correction (IsoCor), and at extremely high resolution performs minimal correction. Optionally load unlabeled sample FAM data to improve correction robustness. Verify that the selected tracer element is present in all compound formulas before executing, as missing tracer atoms will cause algorithm failure.

## Related tools

- **ElemCor** (Primary software tool implementing mass-difference-theory correction with GUI for loading FAM data, specifying resolution and tracer, and exporting corrected MDV and enrichment values.) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Reference combinatorial correction tool; ElemCor converges to IsoCor behavior at extremely low instrument resolution.)

## Evaluation signals

- MDV values sum to 1.0 (or 100%) for each compound and sample; detect arithmetic or numerical instability.
- Corrected MDV values lie in the feasible range [0, 1] with no negative or >1 entries.
- As instrument resolution increases, the magnitude of correction decreases monotonically (less correction applied at very high resolution, more at moderate resolution).
- Processing completes within ~1 minute for typical datasets (e.g., test files with ~100 compounds); if >1 minute, suspect incorrect tracer element specification.
- Unlabeled sample MDV (if provided) clusters near M+0 (low enrichment); labeled sample MDV should show enrichment in higher mass isotopologues consistent with tracer labeling patterns.

## Limitations

- Requires correct tracer element specification; missing tracer atoms in compound formulas cause algorithm failure and cryptic error messages.
- FAM input must have matching analytes and row count between labeled and unlabeled files; mismatches prevent processing.
- XLSX file must be in the same directory as the ElemCor executable; file path handling is rigid.
- Current version provides only generic error messages; troubleshooting requires manual inspection of tracer selection and file format.
- Method assumes instrument resolution is uniform across the mass range; real Orbitrap resolution varies with m/z.

## Evidence

- [readme] FAM and MDV explanation: "the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic"
- [readme] Naturally occurring isotopes and tracer impurity: "Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM)"
- [readme] Mass-difference theory as one of two approaches: "uses two different approaches to account for resolution effect, mass different theory, and unlabeled samples"
- [readme] Resolution-dependent correction behavior: "When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all. Therefore, the amount of correction"
- [readme] Tracer element selection requirement: "PLEASE MAKE SURE THE CORRECT TRACER IS SELECTED! In Step 5, the mass analyzer is selected."
- [readme] Test data resolution and format: "They are simulated from XCalibur with N and S as trace elements, and at nominal instrument resolutions of 140,000 and 280,000, respectively. Both are from Orbitrap analyzer."
- [readme] Tracer element atom presence requirement: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula"
