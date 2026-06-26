---
name: feature-specificity-calculation
description: Use when when you have a quantitative feature table from MZmine2/MZmine3
  with peak area and m/z data aligned across multiple extract samples, and you need
  to identify which features are characteristic of individual samples (high specificity)
  versus ubiquitous across the extract set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - Ion Identity
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical
  classes new to the species'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-specificity-calculation

## Summary

Calculate the proportion of samples in which each MS/MS feature is present to filter features by specificity threshold, enabling identification of sample-specific non-annotated features for downstream prioritization. This metric underpins the Feature Component score in natural product novelty assessment.

## When to use

When you have a quantitative feature table from MZmine2/MZmine3 with peak area and m/z data aligned across multiple extract samples, and you need to identify which features are characteristic of individual samples (high specificity) versus ubiquitous across the extract set. Apply this skill before calculating the Feature Component to retain only features exceeding your specificity threshold (e.g., ≥90%).

## When NOT to use

- Input is not aligned across samples (e.g., each sample has been processed independently without cross-sample feature correspondence) — specificity cannot be computed without alignment.
- Feature table is from non-MS/MS instruments or does not include retention time and m/z information — specificity calculation requires consistent m/z and RT anchors.
- You have already applied strict annotation-based filtering and removed all unannotated features — specificity filtering is only meaningful on the raw feature set.

## Inputs

- MZmine2 or MZmine3 quantitative feature table (Peak area, row m/z, row retention time columns)
- Sample set (multiple extracts with aligned features)

## Outputs

- Feature specificity table (feature ID, specificity proportion per feature)
- Filtered feature list (features meeting min_specificity threshold)
- Specificity breakdown per sample (count and list of specific features retained)

## How to apply

Load the quantitative feature table from MZmine2 or MZmine3 format, retaining only 'Peak area', 'row m/z', and 'row retention time' columns. For each feature across all samples in the extract set, compute specificity as the proportion of samples where that feature is detected (present with non-zero peak area). Compare this proportion against a user-defined min_specificity threshold (e.g., 90%); retain only features meeting or exceeding this threshold. Optionally, apply Ion Identity grouping beforehand to reduce redundant features from the same compound. Document the specificity value for each retained feature; this enables subsequent annotation filtering and Feature Component ratio calculation as (count of specific non-annotated features) / (total features in sample).

## Related tools

- **MZmine2** (Source of quantitative feature table (Peak area, m/z, retention time))
- **MZmine3** (Alternative source of quantitative feature table in same format)
- **Ion Identity** (Optional pre-processing to group redundant features before specificity calculation)

## Examples

```
# In Inventa notebook or Python: for each feature, compute specificity as count(samples where feature is present) / total_samples; filter features where specificity >= 0.90; compute FC = count(specific unannotated features) / count(total features in sample)
```

## Evaluation signals

- All features in the input table have a specificity value computed (0.0 to 1.0 range)
- Feature count after filtering by min_specificity threshold is ≤ feature count before filtering
- For each retained feature, the specificity value is ≥ min_specificity threshold (e.g., ≥0.90)
- Samples that had few or common features show lower counts of 'specific' features; samples with unique features show higher counts
- Sum of specific features per sample aligns with Feature Component denominator (total features in sample after alignment)

## Limitations

- Specificity is a relative metric: threshold choice (e.g., 90%) is user-defined and affects results; no universal optimal value is established.
- Features with low intensity or borderline peak detection may be marked as absent in some samples due to instrument sensitivity, inflating specificity estimates.
- Features resulting from technical artifacts, contaminants, or isotopologues are not distinguished by specificity alone; annotation and quality filtering remain necessary.
- Specificity calculation requires complete cross-sample feature alignment; missing values (e.g., features below LOD in some samples) must be handled consistently (typically treated as absent).

## Evidence

- [methods] Compute feature specificity for each feature as the proportion of samples in the extract set where that feature is present; retain features exceeding min_specificity threshold (e.g., 90%).: "Compute feature specificity for each feature as the proportion of samples in the extract set where that feature is present; retain features exceeding min_specificity threshold (e.g., 90%)."
- [methods] Load the quantitative feature table from MZmine2 or MZmine3, extracting peak area, m/z, and retention time columns.: "Load the quantitative feature table from MZmine2 or MZmine3, extracting peak area, m/z, and retention time columns."
- [methods] The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."
- [other] Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features.: "Inventa is capable to performe the calcultions based on the results from Ion Identity, reducing the total number of features."
- [readme] if you did export any other column, like identities, etc, please remove manually or add the corresponding lines in the funcion quand_table(): "if you did export any other column, like identities, etc, please remove manually or add the corresponding lines in the funcion quand_table()"
