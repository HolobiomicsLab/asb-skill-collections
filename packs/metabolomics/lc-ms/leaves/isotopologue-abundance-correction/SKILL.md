---
name: isotopologue-abundance-correction
description: 'Use when you have LC-MS data from isotope labeling experiments where FAM measurements must be transformed to MDV values. Specifically, apply this when: (1) you have measured fractional abundances of isotopologues (FAM) in XLSX format from a high-resolution instrument (e.g., Orbitrap);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopologue-abundance-correction

## Summary

Correct measured fractional abundances of isotopologues (FAM) from LC-MS instruments to obtain mass distribution vectors (MDV) that represent true isotopic labeling contributions, accounting for naturally occurring isotopes and isotopic impurity. ElemCor implements two resolution-effect correction approaches: mass-difference theory and unlabeled-sample reference methods.

## When to use

Use this skill when you have LC-MS data from isotope labeling experiments where FAM measurements must be transformed to MDV values. Specifically, apply this when: (1) you have measured fractional abundances of isotopologues (FAM) in XLSX format from a high-resolution instrument (e.g., Orbitrap); (2) your instrument's nominal resolution is known (e.g., 140,000 or 280,000); (3) you have labeled sample data and optionally unlabeled sample reference measurements; (4) you need to account for contributions from naturally occurring isotopes and isotopic impurity from the tracer element.

## When NOT to use

- Your instrument resolution is extremely low (< ~50,000 FWHM); ElemCor converges to IsoCor (combinatoric correction only) and provides minimal added value.
- Your FAM data are already corrected, normalized to MDV, or in a non-XLSX format that cannot be ingested by ElemCor.
- Your tracer element is not present in the molecular formula of some compounds; the algorithm will fail with an error.

## Inputs

- XLSX spreadsheet with FAM (fractional abundances of measured isotopologues) columns, one per sample, with rows for each compound
- Optional: XLSX spreadsheet with unlabeled sample reference FAM measurements, same analytes and row count as labeled data
- Tracer element identifier (13C, 2H, 15N, 18O, 34S)
- Nominal instrument resolution (integer, e.g., 140000, 280000)
- Mass analyzer type (e.g., Orbitrap)
- Isotopic purity of tracer nutrient (fractional, 0–1)

## Outputs

- Mass distribution vectors (MDV) for each compound and sample, appended to input XLSX file
- Isotopic enrichment values per compound
- Fold change of pool size for each compound
- Graphical visualization of FAM-to-MDV correction for each compound (displayed in ElemCor GUI)

## How to apply

Load labeled sample FAM data in XLSX format into ElemCor, specifying the tracer element (13C, 2H, 15N, 18O, or 34S), mass analyzer type (e.g., Orbitrap), and nominal instrument resolution. If unlabeled samples are available, also load those reference measurements to enable the unlabeled-sample resolution-effect correction method; otherwise, ElemCor will use mass-difference theory alone. The correction algorithm applies either mass-difference-theory modeling or unlabeled-sample-based calibration to account for naturally occurring isotopes and isotopic impurity, then transforms the corrected FAM into MDV values. Verify that the correct tracer element is selected, as mismatches (e.g., loading 15N data but selecting C as tracer) cause processing errors. The tool produces corrected MDV, isotopic enrichment, and fold change metrics, which are automatically appended to the input XLSX file.

## Related tools

- **ElemCor** (Primary tool for correcting LC-MS FAM data and generating corrected MDV outputs using mass-difference theory or unlabeled-sample reference methods) — https://github.com/4dsoftware/elemcor
- **IsoCor** (Predecessor tool for combinatoric isotope correction (without resolution-effect modeling); ElemCor extends IsoCor by accounting for instrument resolution)

## Evaluation signals

- Corrected MDV sums to 1.0 (or very close, within floating-point tolerance ~1e-6) for each compound and sample.
- MDV length is Nt + 1, where Nt is the number of tracer atoms (e.g., for 13C-labeled glucose with 6 carbons, MDV length = 7).
- Processing completes within expected time (~10–20 seconds for typical datasets on modern processors); timeout or error suggests wrong tracer element was selected.
- Graphical display and output XLSX sheet show smooth, physically plausible MDV distributions (no negative abundances, no implausible isotopic enrichment).
- If unlabeled samples were provided, FAM corrections are more aggressive than mass-difference-theory-only; if not provided, only mass-difference theory is applied without error.

## Limitations

- Software requires MATLAB Compiler Runtime installation; MATLAB itself is not required, but the compiled binary is platform-specific.
- The current version prints only generic error messages; troubleshooting requires manual verification of tracer element, file location, and analyte consistency between labeled and unlabeled samples.
- If labeled and unlabeled XLSX files do not have identical analytes and row counts, the tool will fail.
- FAM data must be in XLSX format; other spreadsheet formats (CSV, ODS) are not supported.
- ElemCor produces no output changelog or audit trail; reproducibility depends on documenting input parameters externally.

## Evidence

- [readme] ElemCor is a software tool to correct LC-MS data in isotope labeling experiments. Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional abundances of measured isotopologues (FAM) collected from the instrument must be corrected to obtain mass distribution vectors (MDV) that correspond to the contribution from isotopic labeling.: "ElemCor is a software tool to correct LC-MS data in isotope labeling experiments. Due to the contribution of naturally occurring isotopes and isotopic impurity from the tracer, the fractional"
- [readme] ElemCor is based on the correction matrix (Ref. 1) and uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3). ElemCor corrects and improves the numerical schemes of both methods (Ref. 4).: "uses two different approaches to account for resolution effect, mass different theory (Ref. 2), and unlabeled samples (Ref. 3)"
- [readme] In Steps 1 and 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only. In Step 3, isotopic purity of nutrient and nominal instrument resolution are specified. In Step 4, the tracer element is selected.: "In Steps 1 and 2, labeled and unlabeled data are loaded. Step 2 is optional, and when it is not performed, ElemCor runs based on mass difference theory only"
- [readme] PLEASE MAKE SURE THE CORRECT TRACER IS SELECTED! In Step 5, the mass analyzer is selected. Then the loaded data are analyzed and isotopic enrichment is calculated for each compound in Step 6.: "PLEASE MAKE SURE THE CORRECT TRACER IS SELECTED! In Step 5, the mass analyzer is selected."
- [readme] The final results are previewed in the graphic interface. They are automatically saved into additional sheets in the original XLSX file. The final results include, MDV, enrichment, and fold change of pool size for different compounds and samples.: "They are automatically saved into additional sheets in the original XLSX file. The final results include, MDV, enrichment, and fold change of pool size"
- [readme] IsoCor performs correction based on combinatorics without considering ressolution effect. When instrument resolution is extremely low, ElemCor is identical to IsoCor. When instrument resolution is extremely high, ElemCor performs no correction at all.: "IsoCor performs correction based on combinatorics without considering ressolution effect. When instrument resolution is extremely low, ElemCor is identical to IsoCor."
- [readme] If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula, and the algorithm will report error if the tracer element is not present in the compound.: "If the 15N data are loaded, but C or S is selected as tracer, then the software tool would not run properly. This is because some compounds may not have C or S in their formula"
