---
name: kendrick-mass-defect-calculation
description: Use when you have a feature list from LC- or GC-HRMS analysis (with m/z,
  retention time, and exact mass columns) and you want to detect homologous series
  of PFAS compounds that repeat by CF₂ mass increments (typically ≈34 Da).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PFΔScreen
  - pyOpenMS
  - pandas
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Kendrick Mass Defect (KMD) Calculation and Homologous Series Detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Kendrick mass defect analysis computes KMD values for each feature in a mass spectrometry dataset to group them into CF₂ homologous series, a characteristic pattern of perfluorinated compounds (PFAS). This calculation enables systematic clustering of features that differ by repeating CF₂ units and facilitates prioritization of PFAS candidates in non-target HRMS screening.

## When to use

Apply this skill when you have a feature list from LC- or GC-HRMS analysis (with m/z, retention time, and exact mass columns) and you want to detect homologous series of PFAS compounds that repeat by CF₂ mass increments (typically ≈34 Da). Use it as part of PFAS prioritization when MD/C-m/C filtering alone is insufficient or when you want to verify systematic mass shifts across coeluting features.

## When NOT to use

- Input is already a confirmed homologous series with known structure — KMD analysis is exploratory and unnecessary for validation
- Features are from non-PFAS compounds or organisms with no expected CF₂ repeating units; KMD clustering will produce spurious groupings
- Feature list lacks exact mass or has poor mass accuracy (>5 ppm); KMD calculation requires high-precision m/z values to distinguish homologs

## Inputs

- Feature list (CSV, Excel, or pandas DataFrame) with columns: m/z, retention time, exact mass, intensity
- Tolerance threshold for KMD grouping (default ±0.005 Da)

## Outputs

- Annotated feature table with appended KMD and series_id columns (CSV or Excel)
- Interactive HTML plot: KMD vs. m/z with linked m/z vs. retention time (to verify systematic RT shifts)
- Homologous series cluster assignments indexed by series_id

## How to apply

Load the feature list as a pandas DataFrame with columns for exact mass, m/z, retention time, and intensity. For each feature, compute the Kendrick mass using the formula KM = (exact_mass / 14.01565) × 14, where 14.01565 is the monoisotopic mass of CH₂ and 14 is the nominal mass used as the Kendrick reference unit. Calculate KMD as the difference KMD = exact_mass − KM for each feature. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂-based series, though this may vary by application). Assign each cluster a unique series_id label. Output the enriched feature table with appended KMD and series_id columns. Verify clustering by inspecting m/z vs. retention time plots: coeluting features with similar KMD values and incrementing m/z differences of ~34 Da indicate true homologous series.

## Related tools

- **PFΔScreen** (Complete non-target PFAS screening pipeline that implements KMD analysis alongside MD/C-m/C prioritization and MS2 fragment matching) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Feature detection in raw LC/GC-HRMS data prior to KMD calculation; reads mzML files and generates feature lists)
- **pandas** (Data loading, manipulation, and export of feature lists; vectorized KMD calculation)

## Examples

```
# After loading feature list as df with columns ['exact_mass', 'm/z', 'rt', 'intensity']
df['kendrick_mass'] = (df['exact_mass'] / 14.01565) * 14
df['kmd'] = df['exact_mass'] - df['kendrick_mass']
df['series_id'] = (df['kmd'].diff().abs() > 0.005).cumsum()
df.to_csv('features_with_kmd_and_series.csv', index=False)
```

## Evaluation signals

- KMD values are computed consistently (no NaN or infinite values); check that (exact_mass / 14.01565) does not return zero or near-zero denominators
- Clustered features within a series_id have KMD differences ≤ tolerance threshold (±0.005 Da) and m/z differences corresponding to CF₂ increments (~34 Da per step)
- Features assigned to the same series_id show coelution in retention time (within expected chromatographic peak width) and display incremental m/z shifts on the KMD vs. m/z plot
- Output feature table has no duplicate or orphaned series_ids; each feature belongs to exactly one series or is flagged as singleton (series_id = 0 or null)
- Interactive HTML plot shows linked m/z vs. RT and KMD vs. m/z views with systematic RT shifts for true homologous series, enabling manual verification

## Limitations

- KMD calculation assumes CF₂ (mass 33.9898) as the repeating unit; other repeating units (e.g., CF, CF₃, or sulfonate modifications) will have different Kendrick reference masses and require separate parameterization
- Tolerance window (±0.005 Da) is a heuristic and may require adjustment for low-resolution or noisy data; wider tolerances risk false positive grouping of unrelated features
- KMD analysis alone cannot distinguish between isomeric PFAS with identical masses; MS2 fragment confirmation and retention time trends are needed for confident structure assignment
- Coeluting non-PFAS compounds or background features with coincidental mass patterns may form spurious homologous series; blank subtraction and MD/C-m/C filtering must be applied upstream to reduce false positives

## Evidence

- [other] Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass: "Calculate Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass."
- [other] KMD = exact_mass − KM for each feature; cluster features by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series): "Compute KMD as KMD = exact_mass − KM for each feature. 4. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series)."
- [other] PFΔScreen uses KMD analysis as one of several prioritization techniques for PFAS feature detection: "PFΔScreen implements Kendrick mass defect (KMD) analysis as one of several prioritization techniques for PFAS feature detection in non-target HRMS data."
- [other] Assign series_id label and output enriched feature table with KMD and series_id columns: "Assign each feature a series_id label and output the enriched feature table with KMD and series_id columns."
- [readme] Interactive HTML plot: KMD vs. m/z with linked m/z vs. RT plot to verify systematic RT-shifts: "a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts)"
