---
name: feature-grouping-by-mass-defect
description: Use when you have a feature list with m/z values from HRMS data and need to identify homologous PFAS series to prioritize suspect screening.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  - MSConvert
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
  - build: coll_pfdeltascreen
    doi: 10.1007/s00216-023-05070-2
    title: pfdeltascreen
  dedup_kept_from: coll_pfdeltascreen
schema_version: 0.2.0
---

# feature-grouping-by-mass-defect

## Summary

Groups high-resolution mass spectrometry features into homologous series by computing Kendrick mass defect (KMD) values and clustering features with equivalent or near-equivalent KMD within a user-specified tolerance. This identifies structurally related PFAS compounds that differ by repeating units (e.g., CF₂) in non-target LC- or GC-HRMS workflows.

## When to use

Apply this skill when you have a feature list with m/z values from HRMS data and need to identify homologous PFAS series to prioritize suspect screening. Use it particularly when MS2 fragment data is unavailable or when you want to leverage systematic mass differences arising from repeating structural units (CF₂, CH₂) to group related compounds.

## When NOT to use

- Input is already a structurally annotated feature table with confirmed compound identities (KMD grouping is a prioritization heuristic, not a confirmation method).
- Data contains non-PFAS or structurally diverse analytes without repeating mass-defect units (KMD analysis is optimized for homologous series with systematic mass offsets).
- m/z values lack sufficient mass accuracy (< 2 ppm, typical for HRMS) or exact masses are unavailable; KMD depends on precise mass calculation.

## Inputs

- Feature list with m/z and exact mass values (Excel, CSV, or auto-detected from mzML via pyOpenMS)
- User-specified KMD tolerance threshold (e.g., 0.01–0.05 Da)
- Optional: mzML raw data file (for MS1 isotope pattern confirmation and RT context)

## Outputs

- Annotated feature table (Excel format) with KMD values and homologous series group assignments
- Interactive HTML plot: KMD vs. m/z with linked m/z vs. retention time visualization
- Series membership labels on features in RawDataVisualization tool

## How to apply

Parse the input feature list containing m/z values and exact masses. For each feature, calculate the Kendrick mass using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, converting exact mass to the Kendrick scale (e.g., CH₂ = 14.0157 Da for perfluorinated compounds, or CF₂ = 50.0035 Da for fluorinated series). Compute the Kendrick mass defect (KMD) as the difference between nominal Kendrick mass and exact Kendrick mass for each feature. Group or flag features with equivalent KMD values within a user-specified tolerance (typically 0.01–0.05 Da, tunable in PFΔScreen's interface) to identify series members. Output an annotated feature table with KMD values and series group assignments, often visualized alongside m/z-vs-retention-time plots to verify systematic RT-shifts consistent with homologous series.

## Related tools

- **PFΔScreen** (Python-based GUI tool that implements KMD analysis as one of three PFAS prioritization techniques (alongside MD/C-m/C and MS2 fragment analysis); orchestrates feature detection, KMD calculation, grouping, and interactive visualization.) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Python interface to C++ OpenMS library; performs automated feature detection from raw mzML data upstream of KMD calculation.)
- **MSConvert** (Vendor-neutral data conversion tool; generates mzML files from raw HRMS instrument data for input to PFΔScreen.)

## Evaluation signals

- Features within the same KMD group show systematic mass differences consistent with repeating CF₂ or CH₂ units (e.g., 50.0035 Da or 14.0157 Da increments).
- Grouped features display correlated retention times with predictable shifts along the chromatographic axis, visualized in the KMD-vs-m/z linked m/z-vs-RT plot.
- KMD values for group members fall within the user-specified tolerance threshold (default ≤ 0.01–0.05 Da) and remain stable across independent runs with identical parameters.
- Output Excel feature table contains non-null KMD and series group assignment columns for all input features; no features are dropped during KMD calculation.
- Interactive HTML plots render without data gaps and allow hover-inspection of feature annotations (m/z, RT, KMD, group ID) to confirm series membership.

## Limitations

- KMD analysis is a prioritization heuristic; it does not confirm chemical identity or rule out false positives. Structural ambiguity can arise when multiple homologous series co-elute or share similar KMD ranges.
- Accuracy depends on precise exact masses (typically ≤ 2 ppm mass error for HRMS); instrument calibration drift or poor mass resolution will degrade KMD clustering.
- User must empirically optimize the KMD tolerance threshold (0.01–0.05 Da typical); a threshold too tight will fragment true series, while too loose will merge unrelated features.
- KMD analysis assumes repeating structural units (CF₂, CH₂); compounds with irregular or non-halogenated heterocycles may not group coherently.
- Requires data-dependent acquisition (ddMS2) with centroided spectra; vendor-specific or non-centroided formats may not integrate correctly with pyOpenMS feature detection.

## Evidence

- [other] Calculate Kendrick mass for each feature using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, where exact mass is converted to the Kendrick scale (e.g., CH₂ = 14.0157 Da).: "Calculate Kendrick mass for each feature using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, where exact mass is converted to the Kendrick scale (e.g., CH₂ = 14.0157 Da)."
- [other] Compute Kendrick mass defect (KMD) as the difference between nominal Kendrick mass and exact Kendrick mass. Group or flag features with equivalent or near-equivalent KMD values (within user-specified tolerance) to identify homologous series members.: "Compute Kendrick mass defect (KMD) as the difference between nominal Kendrick mass and exact Kendrick mass. Group or flag features with equivalent or near-equivalent KMD values (within user-specified"
- [readme] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts): "a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts)"
- [readme] pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data. Optionally, custom feature lists can be included.: "pyOpenMS (Python interface to the C++ OpenMS library) is used for feature detection in MS raw data. Optionally, custom feature lists can be included."
