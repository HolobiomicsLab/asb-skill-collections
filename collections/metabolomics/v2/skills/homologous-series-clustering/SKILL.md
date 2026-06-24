---
name: homologous-series-clustering
description: Use when you have a feature list (m/z, retention time, intensity) from
  HRMS data and want to identify potential PFAS homologous series for prioritization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0580
  tools:
  - Python
  - PFΔScreen
  - pandas
  - pyOpenMS
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

# homologous-series-clustering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group mass spectrometry features into homologous series by computing Kendrick mass defect (KMD) values and clustering features with similar KMD within a mass tolerance window. This technique is used to identify CF₂-repeating PFAS compounds in non-target HRMS workflows.

## When to use

Apply this skill when you have a feature list (m/z, retention time, intensity) from HRMS data and want to identify potential PFAS homologous series for prioritization. The skill is particularly valuable when you suspect CF₂ or other repeating-unit families in your data and want to group related features systematically rather than manually inspecting mass differences.

## When NOT to use

- Input is already a classified feature table with known compound annotations — clustering homologous series is a discovery/prioritization step, not a validation step.
- Data contains only singly-charged ions or highly fragmented peaks where intact m/z values are unreliable — KMD calculation requires accurate neutral mass.
- The repeating unit is not a standard mass difference (e.g., custom polymeric modifications) — the method assumes the repeating unit mass is known and constant.

## Inputs

- Feature list (pandas DataFrame or Excel table) with columns: m/z (exact mass), retention time, intensity
- Kendrick mass reference mass (default: 14.01565 for CH₂ unit)

## Outputs

- Enriched feature table with additional columns: Kendrick mass (KM), Kendrick mass defect (KMD), series_id (integer cluster label)
- Homologous series groups indexed by series_id

## How to apply

Load the feature list as a pandas DataFrame with exact mass values. For each feature, calculate Kendrick mass using KM = (exact_mass / 14.01565) × 14, where 14 represents the CH₂ unit mass. Compute KMD as the difference KMD = exact_mass − KM for each feature. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series). Assign each clustered group a unique series_id label. The rationale is that features belonging to the same homologous series share identical KMD values (reflecting the same basic molecular scaffold) but differ in their total mass by integer multiples of the repeating unit; the tight tolerance window isolates genuine series from noise.

## Related tools

- **PFΔScreen** (Complete PFAS prioritization workflow that implements KMD analysis alongside MD/C-m/C and MS2 fragment analysis for feature detection and clustering) — https://github.com/JonZwe/PFAScreen
- **pandas** (Data manipulation and DataFrame operations for loading feature lists and computing mass-based columns)
- **pyOpenMS** (Feature detection in raw MS data upstream of KMD clustering; provides the initial m/z and RT values)

## Examples

```
# Load feature list and compute KMD-based homologous series
import pandas as pd
features = pd.read_excel('feature_list.xlsx', columns=['m/z', 'RT', 'intensity'])
KM = (features['m/z'] / 14.01565) * 14
features['KMD'] = features['m/z'] - KM
features['series_id'] = (features.groupby(pd.cut(features['KMD'], bins=np.arange(features['KMD'].min(), features['KMD'].max(), 0.005))).ngroup())
features.to_excel('features_clustered.xlsx', index=False)
```

## Evaluation signals

- KMD values for all features in a series_id cluster fall within ±0.005 Da (or specified tolerance); no features are misassigned to the wrong cluster.
- Features within the same series differ by integer multiples of the repeating unit mass (e.g., 14 Da for CH₂, 50 Da for CF₂); mass gaps are consistent.
- Retention time profiles within a series show systematic shifts or coelution patterns consistent with homologs of differing chain length.
- Series_id assignments are reproducible when parameters (tolerance window, reference mass) are fixed; no stochastic variation in clustering.
- Output enriched feature table is valid Excel/CSV with no missing values in KMD or series_id columns; schema matches input with two new columns added.

## Limitations

- Tolerance window (typically ±0.005 Da) may need adjustment for lower-resolution MS instruments; too tight a window will fragment true series, too loose will merge unrelated clusters.
- The method assumes a single, constant repeating unit mass; it does not handle mixed or variable repeating units (e.g., CF₂ and CF₃ in the same series).
- Features with low intensity or near the mass spectrometer's detection limit may have m/z values with larger measurement error, leading to spurious KMD values and misclassification.
- Isotope peaks (e.g., ¹³C variants) are not automatically distinguished from different homologs and may create artifactual series if not pre-filtered.
- No built-in validation of whether grouped series represent genuine chemistry; biological or environmental significance must be assessed downstream.

## Evidence

- [other] Calculate Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass.: "Calculate Kendrick mass for each feature using the formula KM = (exact_mass / 14.01565) × 14, where 14 is the CH₂ unit mass."
- [other] Compute KMD as KMD = exact_mass − KM for each feature. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series).: "Compute KMD as KMD = exact_mass − KM for each feature. Cluster features into homologous series by grouping those with KMD values within a tolerance window (typically ±0.005 Da for CF₂ series)."
- [intro] PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences and diagnostic fragments in the MS2 data: "PFΔScreen uses several techniques for prioritization such as the MD/C-m/C approach, Kendrick mass defect (KMD) analysis and fragment mass differences"
- [readme] a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts): "a KMD vs. m/z with linked m/z vs. RT plot (to verify systematic RT-shifts)"
