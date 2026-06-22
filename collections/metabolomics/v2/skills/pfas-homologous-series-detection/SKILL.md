---
name: pfas-homologous-series-detection
description: Use when you have an m/z-resolved feature list from LC- or GC-HRMS analysis (either detected by pyOpenMS or provided as a custom Excel table) and need to prioritize potential PFAS compounds by identifying clusters of homologous structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  techniques:
  - tandem-MS
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

# PFAS Homologous Series Detection via Kendrick Mass Defect Analysis

## Summary

Detects homologous series of per- and polyfluoroalkyl substances (PFAS) in high-resolution MS feature lists by calculating Kendrick mass defect (KMD) values and grouping features with equivalent or near-equivalent KMD values within a user-specified tolerance. This prioritization technique identifies systematically related PFAS members that differ by repeating units (e.g., CF₂) and share characteristic chromatographic or spectroscopic signatures.

## When to use

Apply this skill when you have an m/z-resolved feature list from LC- or GC-HRMS analysis (either detected by pyOpenMS or provided as a custom Excel table) and need to prioritize potential PFAS compounds by identifying clusters of homologous structures. Trigger conditions: (1) input contains nominal and exact m/z values for detected features; (2) you seek to group features that are likely members of the same perfluorinated homolog series (differing by CF₂ units); (3) you want to reduce false positives by exploiting the characteristic mass defect signature of fluorinated compounds.

## When NOT to use

- Input is a raw mzML file without pre-computed m/z values; apply feature detection first using pyOpenMS before KMD calculation.
- Analysis targets non-fluorinated or weakly fluorinated compounds where the fluorine-specific mass defect is not pronounced; KMD analysis is optimized for perfluorinated structures.
- Feature list lacks both nominal and exact m/z values at sufficient mass accuracy (< 5 ppm); KMD calculation requires high-resolution mass measurements to distinguish genuine homolog series from random m/z clusters.

## Inputs

- Feature list with m/z values (nominal and exact mass) from LC- or GC-HRMS analysis
- Kendrick scale parameters (e.g., CH₂ = 14.0157 Da reference unit)
- User-specified KMD tolerance threshold (in millimass units)

## Outputs

- Annotated feature table (Excel format) with KMD values and homologous series group assignments
- Interactive HTML plot of KMD vs. m/z linked to m/z vs. retention time plot
- Grouped feature clusters representing suspected PFAS homologous series

## How to apply

For each feature in the input list, calculate the Kendrick mass using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, where exact mass is converted to the Kendrick scale with CH₂ = 14.0157 Da as the reference unit. Compute the Kendrick mass defect (KMD) as the difference between the nominal Kendrick mass and exact Kendrick mass for each feature. Group or flag features that have equivalent or near-equivalent KMD values within a user-adjustable tolerance threshold (typically a few millimass units). Features sharing the same KMD are suspected to be members of a homologous series; verify by inspecting m/z differences (should be multiples of ~49.9979 Da for CF₂ units). Output an annotated feature table with KMD values and series group assignments, then cross-validate using the interactive KMD vs. m/z plot (linked to retention time visualization) to confirm systematic chromatographic behavior expected of true homologs.

## Related tools

- **PFΔScreen** (Implements Kendrick mass defect analysis as one of three PFAS prioritization techniques (alongside MD/C-m/C and MS2 fragment analysis); provides GUI for KMD filtering, parameter adjustment, and interactive visualization of KMD vs. m/z plots.) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Detects features in LC- or GC-HRMS raw data (mzML format) prior to KMD analysis; provides m/z and retention time values required as input.)

## Evaluation signals

- KMD values for all features in the output table are calculated and reported; check that KMD = nominal_kendrick_mass − exact_kendrick_mass for a subset of entries.
- Features within the same homologous series group have equivalent KMD values within the specified tolerance (e.g., all members differ by < 0.005 Da in KMD).
- m/z differences between consecutive group members are close to multiples of 49.9979 Da (the Kendrick mass of one CF₂ unit); verify for at least 2–3 series per sample.
- Interactive KMD vs. m/z plot shows distinct vertical clusters (series groups) and the linked m/z vs. retention time plot shows systematic co-elution or regular RT shifts consistent with chromatographic behavior of chain isomers.
- Blank sample features (if provided) show different or absent KMD grouping patterns compared to the sample, confirming that detected series are not artifacts of instrumental or solvent background.

## Limitations

- KMD analysis assumes that all members of a homologous series share the same functional group and fluorination pattern; isomeric PFAS with identical mass but different structure will have identical KMD and cannot be distinguished by this method alone.
- The tolerance threshold for KMD grouping is user-dependent; values that are too lenient may merge unrelated features into false series, while overly stringent thresholds may split true series due to instrumental mass drift or calibration error.
- KMD analysis requires accurate m/z calibration (ideally < 5 ppm) in the high-resolution MS instrument; poor mass accuracy will result in unreliable KMD values and loss of homolog detection sensitivity.
- This method is optimized for fluorinated compounds and may yield high false-positive rates if applied to non-fluorinated backgrounds; always integrate MS2 fragment analysis and MD/C-m/C approach (also implemented in PFΔScreen) as orthogonal confirmation.
- The interpretation of KMD groups as true PFAS homologs still requires manual validation against retention time patterns, MS/MS spectra (diagnostic fragments), and isotope pattern consistency; the technique alone does not confirm chemical identity.

## Evidence

- [other] Calculate Kendrick mass for each feature using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, where exact mass is converted to the Kendrick scale (e.g., CH₂ = 14.0157 Da).: "Calculate Kendrick mass for each feature using the formula: Kendrick mass = (nominal mass / exact mass) × exact mass, where exact mass is converted to the Kendrick scale (e.g., CH₂ = 14.0157 Da)."
- [other] Compute Kendrick mass defect (KMD) as the difference between nominal Kendrick mass and exact Kendrick mass.: "Compute Kendrick mass defect (KMD) as the difference between nominal Kendrick mass and exact Kendrick mass."
- [other] Group or flag features with equivalent or near-equivalent KMD values (within user-specified tolerance) to identify homologous series members.: "Group or flag features with equivalent or near-equivalent KMD values (within user-specified tolerance) to identify homologous series members."
- [readme] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [readme] a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts): "a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts)"
