---
name: spectral-feature-clustering-by-intensity-correlation
description: Use when you have an annotated LC-MS feature table with KEGG candidate matches and adduct assignments (output from the matching stage), and you need to disambiguate which features co-elute and correlate in intensity, signaling a common metabolite origin before applying adduct-based filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-feature-clustering-by-intensity-correlation

## Summary

Group co-eluting LC-MS features by intensity correlation and retention time proximity to identify features likely originating from the same metabolite. This clustering step reduces annotation complexity and enables downstream quasi-molecular adduct filtering.

## When to use

You have an annotated LC-MS feature table with KEGG candidate matches and adduct assignments (output from the matching stage), and you need to disambiguate which features co-elute and correlate in intensity, signaling a common metabolite origin before applying adduct-based filtering.

## When NOT to use

- Input features have not yet been matched to a compound database (matching stage must precede clustering).
- Retention time information is missing or unreliable, making proximity-based grouping invalid.
- Features are from a targeted assay with pre-known metabolite identities; clustering is unnecessary.

## Inputs

- annotated feature table with KEGG candidates and adduct assignments
- intensity matrix (features × samples)
- retention time vector

## Outputs

- annotated feature table with pcgroup (cluster group) identifiers merged as a new column

## How to apply

Apply the mWISE featuresClustering function to group features based on intensity correlation and retention time proximity. The function assigns cluster identifiers (pcgroup) to each feature, which are then merged into the annotated table as a new column. These cluster assignments serve as the basis for downstream cluster-based filtering: features within each cluster are then retained only if assigned to quasi-molecular adducts (MH, MNa, MK, etc.), with optional filtering of low-frequency adducts (observed frequency ≤ 0.1 threshold). The clustering rationale is that co-eluting, correlated features likely represent the same molecular species, so filtering by adduct type within clusters reduces spurious in-source fragments and improves candidate confidence.

## Related tools

- **mWISE** (provides featuresClustering function to group co-eluting features by intensity correlation and retention time proximity) — https://dev.b2s.club/b2slab/mWISE
- **R** (execution environment for mWISE clustering functions)
- **CAMERA** (source of default adduct and fragment table used for downstream cluster-based filtering)

## Examples

```
# Load annotated feature table with KEGG matches; apply featuresClustering
KeggCandidates.Tab <- featuresClustering(featureTable = annotated.peaks, intensity.matrix = intensity.data, rt.vector = retention.times)
```

## Evaluation signals

- pcgroup column is present in output table with unique integer identifiers; no NAs in cluster assignments for features that passed matching.
- Features within the same cluster exhibit retention time proximity (e.g., differ by < threshold, typically seconds to a minute).
- Features within the same cluster show intensity correlation (e.g., Pearson r > 0.7 or similar co-elution criterion) across samples.
- Downstream cluster-based filtering correctly retains only quasi-molecular adducts per cluster and applies the 0.1 frequency threshold consistently.
- No decrease in valid feature count due to clustering itself; filtering occurs only in the subsequent clusterBased.filter step.

## Limitations

- Clustering accuracy depends on retention time precision and sample-to-sample intensity correlation; poor LC stability or low dynamic range can degrade grouping quality.
- Features from isomeric or isobaric metabolites may incorrectly cluster together if they co-elute and show similar intensity patterns.
- The method does not account for metabolite-specific fragmentation patterns; fragments of different adducts from the same compound may be split across clusters if they are spatially or temporally separated.
- Optimal intensity correlation and retention time proximity thresholds are not explicitly specified in the article and may require method tuning for different MS platforms or experimental conditions.

## Evidence

- [other] The featuresClustering function groups co-eluting features and merges the cluster assignments (pcgroup) into the annotated table.: "The featuresClustering function groups co-eluting features and merges the cluster assignments (pcgroup) into the annotated table."
- [other] Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity.: "Apply mWISE featuresClustering function to group co-eluting features based on intensity correlation and retention time proximity."
- [intro] the features that may come from the same metabolite are clustered using the `featuresClustering` function: "the features that may come from the same metabolite are clustered using the `featuresClustering` function"
- [intro] clustering and filtering the potential KEGG candidates: "clustering and filtering the potential KEGG candidates"
