---
name: cluster-based-candidate-prioritization
description: Use when after mass-to-charge matching has produced a large table of
  candidate KEGG metabolites with multiple adduct assignments per feature. Use it
  when you observe that multiple candidate ions co-elute and share similar intensity
  profiles, suggesting they derive from the same parent metabolite;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides
  tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cluster-based-candidate-prioritization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill groups co-eluting LC-MS features by intensity correlation and retention time proximity, then filters candidate metabolite annotations to retain only quasi-molecular adducts while removing in-source fragments and low-frequency adducts. It reduces annotation ambiguity by enforcing cluster-level coherence and adduct plausibility.

## When to use

Apply this skill after mass-to-charge matching has produced a large table of candidate KEGG metabolites with multiple adduct assignments per feature. Use it when you observe that multiple candidate ions co-elute and share similar intensity profiles, suggesting they derive from the same parent metabolite; or when your candidate table contains many in-source fragments and rare adducts that add noise without improving annotation specificity.

## When NOT to use

- Input is already a single-adduct, validated metabolite list (clustering adds no value).
- You lack reliable retention time or intensity correlation data (clustering requires co-elution signals).
- Your analysis goal requires comprehensive enumeration of all fragments and adducts (filtering removes legitimate minor species).

## Inputs

- Annotated feature table with KEGG candidate identifiers and adduct assignments (from matching stage)
- Feature intensity matrix (for computing co-elution correlation)
- Retention time vector for each feature
- Optional: user-specified list of quasi-molecular adducts to retain

## Outputs

- Filtered candidate table (MH.Tab) with cluster group identifiers (pcgroup) and quasi-molecular adduct candidates only
- Cluster membership assignments for each retained feature

## How to apply

First, apply the mWISE featuresClustering function to group features with high intensity correlation and retention time proximity, generating cluster identifiers (pcgroup). Merge these identifiers into your annotated feature table as a new column. Then apply the clusterBased.filter function to each cluster, specifying quasi-molecular adducts of interest (MH, MNa, MK, etc.). If no specific list is provided, the function defaults to quasi-molecular adducts plus any observed adducts with frequency > 0.1. This threshold can be adjusted; a higher threshold (e.g., 0.2) removes rarer adducts more aggressively. The output is a filtered table containing only cluster-validated candidates, reducing false positives and redundancy while preserving the most plausible molecular ion assignments.

## Related tools

- **mWISE** (Provides featuresClustering and clusterBased.filter functions for grouping co-eluting features and filtering by quasi-molecular adduct class.) — https://dev.b2s.club/b2slab/mWISE
- **R** (Execution environment for mWISE functions.)
- **CAMERA** (Source of default adduct and fragment definitions used to build mWISE's adduct table.)
- **cliqueMS** (Contributed methodology informing adduct and fragment classification defaults in mWISE.)

## Examples

```
# In R using mWISE:
features_clustered <- featuresClustering(annotated_table, intensity_matrix, rt_vector)
filtered_table <- clusterBased.filter(features_clustered, quasi_molecular_adducts = c('MH', 'MNa', 'MK'), frequency_threshold = 0.1)
```

## Evaluation signals

- Cluster identifiers (pcgroup) are present in output table and are consistent within co-eluting feature groups.
- All retained candidates are annotated with quasi-molecular adducts (MH, MNa, MK, etc.); no in-source fragments or unspecified adducts remain unless explicitly whitelisted.
- Candidate count per feature decreases (typically by 50–80%) after filtering compared to pre-clustering table.
- Candidate metabolites within a cluster share similar intensity ratios across all samples (high within-cluster correlation), confirming co-occurrence.
- Filtering preserves the highest-frequency or user-specified quasi-molecular adduct for each feature while removing singletons or low-frequency adducts.

## Limitations

- Clustering relies on retention time and intensity correlation; poor peak resolution or missing intensity values degrade cluster quality.
- The default 0.1 frequency threshold is data-dependent; small sample cohorts may eliminate rare but genuine adducts; large cohorts may retain noise.
- Isomeric or isobaric metabolites co-eluting by chance may be incorrectly merged into the same cluster.
- Filtering is conservative and may remove valid minor adducts (e.g., [M+NH4]+ in ammonia-rich solvents) if their observed frequency falls below the threshold.

## Evidence

- [other] The featuresClustering function groups co-eluting features and merges the cluster assignments (pcgroup) into the annotated table.: "The featuresClustering function groups co-eluting features and merges the cluster assignments (pcgroup) into the annotated table."
- [other] The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts, optionally using adducts with observed frequency higher than 0.1 if no specific quasi-molecular list is provided, producing the filtered MH.Tab output.: "The clusterBased.filter function then filters candidates by retaining only those with quasi-molecular adducts, optionally using adducts with observed frequency higher than 0.1 if no specific"
- [other] Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity.: "Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity."
- [other] Apply mWISE clusterBased.filter function to each cluster, retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency adducts (observed frequency ≤ 0.1 threshold).: "Apply mWISE clusterBased.filter function to each cluster, retaining only features assigned to quasi-molecular adducts (MH, MNa, MK, etc.) and filtering out in-source fragments and low-frequency"
- [intro] clustering and filtering the potential KEGG candidates: "clustering and filtering the potential KEGG candidates"
