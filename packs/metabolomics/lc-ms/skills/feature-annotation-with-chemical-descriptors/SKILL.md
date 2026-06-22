---
name: feature-annotation-with-chemical-descriptors
description: Use when you have a feature list (m/z values, retention times, and optionally molecular formulas or neutral masses) from LC- or GC-HRMS data and need to rapidly identify features matching characteristic chemical signatures (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pyOpenMS
  - OpenMS
  - MSConvert
  - PFΔScreen
  techniques:
  - LC-MS
derived_from:
- doi: 10.1007/s00216-023-05070-2
  title: pfdeltascreen
evidence_spans:
- PFΔScreen is an open-source Python based non-target screening software tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pfdeltascreen_cq
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-05070-2
  all_source_dois:
  - 10.1007/s00216-023-05070-2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-annotation-with-chemical-descriptors

## Summary

Annotate mass spectrometry features with computed chemical descriptors (mass defect, normalized mass defect ratios, Kendrick mass defect) to enable prioritization and filtering of candidate compounds. This skill enriches feature lists with dimensionless or normalized chemical properties that support targeted screening of analytes with specific structural patterns, such as PFAS.

## When to use

You have a feature list (m/z values, retention times, and optionally molecular formulas or neutral masses) from LC- or GC-HRMS data and need to rapidly identify features matching characteristic chemical signatures (e.g., repeating fluorinated units in PFAS, or other persistent structural motifs). Apply this skill when you want to assign computed chemical properties—rather than rely solely on spectral matching—to flag features for further manual or automated interrogation.

## When NOT to use

- Input is already a fully annotated or verified compound library; use this skill for de novo feature prioritization in non-target or suspect screening workflows only.
- Your data are in vendor-specific binary formats (not converted to mzML) and you lack pyOpenMS or MSConvert infrastructure; the feature annotation step requires centroided, quality-controlled m/z and intensity values.
- You are performing targeted quantification of known compounds with reference standards; this skill is optimized for discovery/prioritization, not quantitation.

## Inputs

- Feature list (CSV or Excel) with m/z, retention time, and optionally molecular formula or neutral mass per feature
- mzML file (vendor-independent raw HRMS data in centroided, data-dependent acquisition format) — optional if custom feature list is provided
- User-defined threshold parameters for MD/C, m/C, and KMD ranges (if applicable)

## Outputs

- Annotated feature list (CSV or Excel) with computed descriptors: mass defect (MD), MD/C ratio, m/C ratio, KMD (if applicable), and priority flag
- Interactive HTML plots: MD/C vs. m/C scatter plot, m/z vs. retention time, KMD vs. m/z (with linked m/z vs. RT for coelution verification), m/C histogram
- Flagged high-priority feature subset ready for MS² fragment analysis or manual curation

## How to apply

Load your feature list into Python as a tabular structure (CSV or Excel) containing at minimum m/z and retention time; optionally include molecular formula or neutral mass per feature. For each feature, compute mass defect (MD) as the difference between exact mass and the nearest integer mass. If molecular formula is available, extract or infer the carbon count (C); otherwise use a default heuristic. Calculate MD/C (mass defect normalized to carbon count) and m/C (exact mass normalized to carbon count) ratios. Optionally compute Kendrick mass defect (KMD) by remapping the mass scale to integer masses of CH₂ units, enabling detection of homologous series with systematic retention time or m/z shifts. Apply user-defined threshold ranges on these descriptors (e.g., MD/C > 0.45 and m/C within 150–200 for typical PFAS) to annotate each feature with a priority flag. Write the augmented feature list (with all computed descriptors and flags) to output CSV or Excel for downstream filtering, visualization, or manual inspection.

## Related tools

- **pyOpenMS** (Feature detection and mass defect computation from raw mzML spectra; Python interface to C++ OpenMS library for m/z calibration and peak picking) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Underlying C++ library for feature detection, mass calibration, and spectral alignment in HRMS data) — https://github.com/OpenMS/OpenMS
- **MSConvert** (Vendor-independent conversion of raw HRMS data to mzML format required for feature annotation workflow) — http://proteowizard.sourceforge.net/
- **PFΔScreen** (Complete Python GUI application implementing MD/C-m/C annotation, KMD analysis, and integrated MS² fragment analysis for PFAS feature prioritization) — https://github.com/JonZwe/PFAScreen

## Evaluation signals

- All features in input list receive computed MD, MD/C, m/C, and (optionally) KMD values; no missing or null descriptors in output.
- Descriptor values lie within expected ranges for the analyte class: for PFAS, MD/C typically > 0.45, m/C typically 150–200 (units: Da/C); verify against known reference standards if available.
- Priority flags (high/low or ranked score) correlate with manual inspection or reference databases: features flagged as high-priority should exhibit MS² fragmentation patterns consistent with target structures (e.g., CF₂ and CF₃ fragments for PFAS).
- MD/C vs. m/C scatter plot shows expected clustering or linear relationship for homologous series; KMD vs. m/z plot reveals equidistant spacing consistent with CH₂ repeats or CF₂ units.
- Retention time and m/z coelution patterns (inspected in interactive m/z vs. RT and KMD-linked plots) are consistent with known chromatographic behavior and structural relationships (e.g., longer-chain PFAS typically elute later).

## Limitations

- Accuracy of carbon count inference: if molecular formula is unavailable, heuristics (e.g., assuming average carbon content) may misclassify features; explicit formula input strongly recommended.
- Threshold selection is user-dependent and analyte-class-specific; MD/C and m/C cutoffs for PFAS may not apply to other persistent organic pollutants or metabolites. No automated threshold recommendation is provided; users must consult literature or validation sets.
- MD/C-m/C approach alone does not distinguish structural isomers or confirm identity; false positives can occur if isobars or non-target compounds share similar mass defect signatures. MS² fragment analysis or complementary spectroscopic data are required for confirmation.
- Requires centroided, high-quality HRMS data; uncalibrated or low-resolution spectra will produce unreliable mass defect values and degrade descriptor utility.
- Runtime and memory scale with feature count; the README reports <1 minute for 4000 spectra, but very large datasets (>10,000 features) may require parameter optimization or feature pre-filtering.

## Evidence

- [other] For each feature, compute the mass defect (MD) as the difference between the exact mass and the nearest integer mass.: "For each feature, compute the mass defect (MD) as the difference between the exact mass and the nearest integer mass."
- [other] Calculate MD/C as MD divided by carbon count, and m/C as exact mass divided by carbon count.: "Calculate MD/C as MD divided by carbon count, and m/C as exact mass divided by carbon count."
- [other] Apply the MD/C and m/C thresholds defined in PFΔScreen to flag features as high-priority PFAS candidates.: "Apply the MD/C and m/C thresholds defined in PFΔScreen to flag features as high-priority PFAS candidates."
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [readme] The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters.: "The overall rather short runtime (e.g., less than one minute in case of 4000 spectra per sample for the whole workflow), allows a convenient adjustment of input parameters."
- [other] Write the annotated feature list with MD/C, m/C, and priority flag to output CSV.: "Write the annotated feature list with MD/C, m/C, and priority flag to output CSV."
