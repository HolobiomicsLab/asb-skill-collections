---
name: modularity-optimization-clustering
description: Use when after MS-DIAL peak character estimation has grouped LC-MS features into preliminary clusters based on peak shape and chromatographic similarity, and you need to select a single representative parental feature from each cluster to reduce redundancy before MS-FINDER annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MS-CleanR
  - MS-DIAL
  - MS-FINDER
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
---

# modularity-optimization-clustering

## Summary

Apply multi-level optimization of modularity algorithm to cluster LC-MS features and extract parental (representative) signals from feature groups. This skill identifies the highest-modularity feature within each cluster to serve as the consensus representative for downstream annotation.

## When to use

After MS-DIAL peak character estimation has grouped LC-MS features into preliminary clusters based on peak shape and chromatographic similarity, and you need to select a single representative parental feature from each cluster to reduce redundancy before MS-FINDER annotation. Use this skill when your goal is to collapse feature clusters (isotopes, adducts, in-source fragments) into non-redundant parental signals suitable for metabolite annotation.

## When NOT to use

- Input features have not yet been clustered by MS-DIAL peak character estimation; apply peak character estimation first.
- You require all features (including isotopes and adducts) for subsequent analysis rather than a reduced set of parental signals.
- Data contain MS1-only measurements without MS/MS spectra; MS-CleanR will discard such features in the first step.

## Inputs

- Pre-clustered feature table with MS-DIAL peak character estimation cluster assignments
- Feature metadata including m/z, retention time, peak intensity, and cluster ID
- Feature similarity network or adjacency matrix from peak character estimation

## Outputs

- Parental feature table (one representative feature per cluster)
- Feature-to-cluster mapping with modularity scores
- Structured output file compatible with MS-FINDER input format

## How to apply

Load the pre-clustered feature set output from the MS-DIAL peak character estimation step, which contains grouped LC-MS features with cluster membership annotations. Apply the multi-level optimization of modularity algorithm to each cluster independently, computing modularity scores for each feature within the cluster based on its intra-cluster connectivity and inter-cluster isolation. Select the feature with the highest modularity score from each cluster as the parental signal representative—this feature maximizes the strength of connections within its cluster relative to the rest of the network. Compile and export the set of extracted parental features (one per cluster) to a structured output file preserving cluster IDs and modularity scores. This reduces the feature table while retaining the most representative signal from each group of related species.

## Related tools

- **MS-DIAL** (Performs initial peak character estimation and feature clustering; required v4.00 or higher) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Implements multi-level optimization of modularity algorithm for parental signal extraction and exports results for downstream annotation) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-FINDER** (Accepts extracted parental features for in silico annotation using hydrogen rearrangement rules; required v3.30 or higher) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Output feature table contains exactly one feature per input cluster (cluster membership is one-to-one with selected parental features).
- Modularity scores are normalized and monotonically ranked; the selected feature from each cluster has the maximum modularity score within that cluster.
- Parental features retain m/z, retention time, and intensity metadata compatible with MS-FINDER input schema.
- Number of output features equals the number of input clusters; no clusters lack a representative and no feature appears twice.
- Exported output file structure matches MS-CleanR specifications for downstream MS-FINDER querying without format conversion errors.

## Limitations

- Requires pre-clustered input from MS-DIAL peak character estimation; algorithm depends on cluster quality and peak similarity metrics upstream.
- Modularity optimization is computationally intensive for datasets with >10,000 features per cluster or very deep cluster hierarchies; scaling may degrade performance.
- Selection of the highest-modularity feature assumes that network centrality correlates with biological relevance; features with lower modularity but higher intensity or biological significance may be discarded.
- The skill does not handle ambiguous tie-breaking when multiple features within a cluster have identical modularity scores; implementation details are not fully specified in the README.
- No changelog available; version-specific behavior changes or improvements relative to prior releases are undocumented.

## Evidence

- [readme] feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
- [other] Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation. Apply the multi-level optimization of modularity algorithm to each cluster to identify and rank representative parental features by modularity score.: "Load the pre-clustered feature set (output from feature clustering step) containing grouped LC-MS features based on MS-DIAL peak character estimation. Apply the multi-level optimization of modularity"
- [other] Select the highest-modularity feature from each cluster as the parental signal representative.: "Select the highest-modularity feature from each cluster as the parental signal representative."
- [other] Compile and export the set of extracted parental features to a structured output file for downstream MS-FINDER annotation.: "Compile and export the set of extracted parental features to a structured output file for downstream MS-FINDER annotation."
- [readme] Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher): "Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher)"
