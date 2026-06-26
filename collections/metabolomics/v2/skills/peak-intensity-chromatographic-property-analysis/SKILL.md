---
name: peak-intensity-chromatographic-property-analysis
description: Use when you have a filtered MS-DIAL peak list (post-generic filtering)
  containing m/z, retention time, and peak intensity metrics, and you need to group
  LC-MS features into clusters to reduce redundancy before parental signal extraction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-intensity-chromatographic-property-analysis

## Summary

Computes feature similarity in LC-MS data by analyzing peak shape and chromatographic properties (m/z, retention time, peak intensity) using the MS-DIAL peak character estimation algorithm. This similarity metric is the foundation for grouping co-eluting or chemically related features into clusters prior to parental signal extraction.

## When to use

Apply this skill when you have a filtered MS-DIAL peak list (post-generic filtering) containing m/z, retention time, and peak intensity metrics, and you need to group LC-MS features into clusters to reduce redundancy before parental signal extraction. Use it when working with data-dependent (DDA) or data-independent (DIA) acquisition modes that require feature deconvolution.

## When NOT to use

- Input is already a post-clustering, annotated feature table with parental signals resolved
- Data contain MS1-only spectra without MS/MS information (MS-CleanR will crash at the first step)
- Peak list has not undergone generic filtering (blank subtraction, background removal, mass defect filtering) — apply generic filters first

## Inputs

- MS-DIAL peak list (post-generic filtering) with m/z, retention time, and peak intensity columns
- Peak intensity time-series data for each feature
- Chromatographic retention time values
- Sample ionization mode metadata (positive, negative, or both)

## Outputs

- Feature similarity network (pairwise similarity matrix)
- Feature clusters with cluster ID assignments
- Clustered feature table with cluster membership annotations
- Optional merged cluster assignments (PI + NI modes combined)

## How to apply

Load the filtered MS-DIAL peak list containing m/z, retention time, and peak intensity metrics for each feature. Apply the MS-DIAL peak character estimation algorithm to compute pairwise feature similarity based on peak shape characteristics and chromatographic co-elution patterns. Construct a feature similarity network from these pairwise scores. Apply multi-level optimization of the modularity algorithm to partition the network into feature clusters. Optionally merge clusters across positive and negative ionization modes if both are present in the data. Assign cluster IDs to all features and export the clustered feature table with cluster membership annotations for downstream parental signal extraction.

## Related tools

- **MS-DIAL** (Source tool providing peak list, m/z/RT/intensity data, and peak character estimation algorithm implementation) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Wrapper that loads MS-DIAL output, orchestrates feature similarity computation, and performs modularity-based clustering) — https://github.com/eMetaboHUB/MS-CleanR

## Evaluation signals

- Feature similarity scores are symmetric and bounded (0 to 1 or normalized range) — validate pairwise matrix properties
- All features in the input peak list are assigned exactly one cluster ID — no unassigned or duplicate assignments
- Clusters are non-overlapping partitions of the feature set — verify set union equals input feature count
- Co-eluting features (similar RT and peak shape) are grouped in the same cluster — spot-check a subset manually or via RT/m/z visualization
- If PI and NI modes are merged, cluster sizes and membership remain stable before/after merge step — compare pre/post-merge annotations

## Limitations

- Requires at least 3 blank and 3 QC samples identified in the MS-DIAL sample list for accurate background and signal estimation
- Avoid spaces and hyphens in sample or class names; avoid single-letter class names (known bug)
- All features without MS/MS spectra are discarded during the first (generic filtering) step — MS1-only data will cause crash
- The modularity optimization algorithm is greedy and heuristic — cluster assignments may vary slightly across random seeds or parameter tuning
- Active development of MS-CleanR has ceased; tool will not be maintained beyond current version due to integration of similar functionality into MS-DIAL 5.x

## Evidence

- [other] MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties: "Apply MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties."
- [readme] Feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [other] Load the filtered MS-DIAL peak list (post-generic filtering) containing m/z, retention time, and peak intensity metrics for each feature: "Load the filtered MS-DIAL peak list (post-generic filtering) containing m/z, retention time, and peak intensity metrics for each feature."
- [other] Construct a feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters: "Construct a feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters."
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained: "Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained."
