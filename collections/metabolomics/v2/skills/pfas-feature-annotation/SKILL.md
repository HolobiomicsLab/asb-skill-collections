---
name: pfas-feature-annotation
description: Use when when you have a feature list (m/z, retention time, intensity)
  from LC- or GC-HRMS non-target screening and need to identify PFAS-like homologous
  series characterized by CF₂ (14 Da) repeating units.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
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

# Kendrick mass defect (KMD) analysis for homologous-series detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

KMD analysis groups features from non-target HRMS data into CF₂ homologous series by computing normalized mass defects and clustering features within a narrow tolerance window. This enables prioritization of potential PFAS compounds by identifying characteristic repeating mass patterns.

## When to use

When you have a feature list (m/z, retention time, intensity) from LC- or GC-HRMS non-target screening and need to identify PFAS-like homologous series characterized by CF₂ (14 Da) repeating units. Use this skill when suspect-based screening is insufficient and you want to group related unknown features for prioritization.

## When NOT to use

- Input is already a manually curated suspect list with known PFAS structures — use targeted screening instead.
- Features have low mass accuracy (>5 ppm error) — KMD clustering requires precise exact mass to distinguish homologs from noise.
- Data is profile-mode (not centroided) or from low-resolution MS — KMD analysis depends on accurate centroided m/z values.

## Inputs

- Feature list (pandas DataFrame or Excel table with columns: exact m/z, retention time, intensity)
- Tolerance threshold for KMD window (default ±0.005 Da)

## Outputs

- Annotated feature table with KMD column (computed mass defect values)
- Series_id column assigning each feature to a homologous cluster
- Interactive HTML plot: KMD vs. m/z with linked m/z vs. retention time visualization

## How to apply

Load the feature list as a pandas DataFrame with exact m/z values. For each feature, calculate Kendrick mass using KM = (exact_mass / 14.01565) × 14, where 14 represents the CH₂ unit mass used as the normalization basis. Compute KMD as the difference KMD = exact_mass − KM for each feature. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series). Assign each cluster a series_id label and append KMD and series_id columns to the enriched feature table. The rationale is that true PFAS homologs share identical KMD values while differing by multiples of 14 Da in exact mass, creating a fingerprint detectable by this algebraic transformation.

## Related tools

- **PFΔScreen** (GUI-based orchestrator that implements KMD analysis as part of automated PFAS prioritization workflow) — https://github.com/JonZwe/PFAScreen
- **pyOpenMS** (Feature detection in raw MS data (upstream preprocessing that generates m/z, RT, intensity features for KMD analysis))
- **pandas** (DataFrame manipulation for KMD calculation and homolog clustering)

## Examples

```
kmd_values = (feature_df['exact_mass'] / 14.01565) * 14; feature_df['KMD'] = feature_df['exact_mass'] - kmd_values; clusters = feature_df.groupby(pd.cut(feature_df['KMD'], bins=np.arange(feature_df['KMD'].min() - 0.005, feature_df['KMD'].max() + 0.005, 0.01))); feature_df['series_id'] = clusters.ngroup()
```

## Evaluation signals

- KMD values within each series cluster differ by <0.01 Da (all features in a group share nearly identical mass defect).
- Consecutive features in the same series differ by exactly 14 Da (or integer multiples thereof) in exact m/z, verifying CF₂ repeatability.
- Retention time trend: features in the same homologous series show systematic retention time shifts correlating with increasing chain length (detectible in the interactive KMD vs. m/z linked RT plot).
- Series_id uniqueness: each feature is assigned to exactly one series; no orphaned or multi-assigned features.
- Tolerance window consistency: all features within a cluster meet the ±0.005 Da KMD criterion; features outside clusters exceed it.

## Limitations

- KMD analysis assumes all homologs in a series differ by integer multiples of 14 Da; structural PFAS variants with different functional groups (e.g., sulfonic acid vs. carboxylic acid) may not cluster together despite related structures.
- Tolerance threshold (±0.005 Da) is empirically tuned for CF₂ series; other homolog types (e.g., CHF₂, CF₃ chains) may require different thresholds not addressed in the article.
- False positives can occur when unrelated features accidentally share similar KMD values; KMD alone does not confirm PFAS identity — must be combined with MS2 fragment analysis and diagnostic fragments for prioritization.
- Requires high mass accuracy (ideally sub-ppm) to resolve small KMD differences; lower-accuracy instruments may produce overlapping clusters.

## Evidence

- [other] Calculate Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass.: "Calculate Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass."
- [other] Compute KMD as KMD = exact_mass − KM for each feature.: "Compute KMD as KMD = exact_mass − KM for each feature."
- [other] Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series).: "Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series)."
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data"
- [intro] Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra: "Raw mass spectrometric data can be included vendor-independently in the mzML format (data-dependent acquisition with centroided spectra"
- [readme] A KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts): "A KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts)"
