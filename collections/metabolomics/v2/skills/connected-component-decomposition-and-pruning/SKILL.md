---
name: connected-component-decomposition-and-pruning
description: Use when after identifying pairwise feature connections via correlation
  and retention-time windowing, when you need to partition the feature space into
  coherent groups where each feature has sufficient connectivity to its peers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - notame
  - R
  - Biobase
  - find_connections
  - assign_cluster_id
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo10040135
  title: notame
- doi: 10.1093/bioinformatics/btr597
  title: ''
evidence_spans:
- This package can be used to analyze preprocessed LC-MS data in non-targeted metabolomics
- library(notame)
- reads them to R, conducts additional preprocessing and statistical analyses
- '```MetaboSet``` is built upon the ```ExpressionSet``` class from the Biobase package
  by Bioconductor'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_notame_cq
    doi: 10.3390/metabo10040135
    title: notame
  dedup_kept_from: coll_notame_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo10040135
  all_source_dois:
  - 10.3390/metabo10040135
  - 10.1093/bioinformatics/btr597
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# connected-component-decomposition-and-pruning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Decompose a feature correlation graph into connected components and iteratively prune nodes to enforce a minimum degree threshold, isolating groups of co-eluting or highly correlated metabolic features. This produces pruned clusters suitable for downstream assignment of cluster identifiers.

## When to use

After identifying pairwise feature connections via correlation and retention-time windowing, when you need to partition the feature space into coherent groups where each feature has sufficient connectivity to its peers. Apply this when features suspected of originating from the same metabolite should be grouped before assignment of canonical cluster identifiers.

## When NOT to use

- If the input is not a graph structure but an already-clustered feature table (use assign_cluster_id directly instead).
- If all features should remain ungrouped or if no connectivity criterion is meaningful for your analysis.
- If retention-time information is absent or unreliable, making correlation graphs too sparse to form coherent components.

## Inputs

- correlation graph or edge list (from find_connections output)
- feature identifiers (Feature_ID)
- degree threshold (numeric, 0–1, e.g., 0.8)
- retention-time window specification (if re-running connections)

## Outputs

- cluster membership assignments (connected components with pruned structure)
- node degree metrics (connectivity counts per feature)
- pruned graph structure (features and edges meeting degree threshold)

## How to apply

Execute find_clusters() on the output of find_connections() (a graph of correlated feature pairs within a retention-time window, e.g. ±1 s). Set a degree threshold (e.g., 0.8) to define the minimum connectivity requirement. The function decomposes the correlation graph into connected components, then iteratively removes nodes (features) that fall below the degree threshold until all remaining nodes satisfy the criterion. Nodes removed in early pruning iterations are reassigned to lower-priority clusters or flagged as singletons. Rationale: enforcing minimum degree ensures robust, densely-connected clusters less prone to outlier inclusion; iterative pruning avoids cascade effects from isolated features.

## Related tools

- **notame** (provides find_clusters() function for connected-component decomposition and degree-based pruning of feature correlation graphs) — https://github.com/hanhineva-lab/notame
- **find_connections** (upstream function that generates the correlation graph input (feature pairs meeting correlation threshold and RT window)) — https://github.com/hanhineva-lab/notame
- **assign_cluster_id** (downstream function that labels pruned clusters and assigns identifiers based on feature with highest median peak area) — https://github.com/hanhineva-lab/notame
- **R** (runtime environment for notame and graph operations)

## Examples

```
clusters <- find_clusters(connections, degree_threshold = 0.8)
```

## Evaluation signals

- Verify that the number of connected components returned equals or exceeds the number of input clusters before pruning (decomposition is complete).
- Check that all remaining nodes in each component have degree ≥ the threshold; inspect node degrees to confirm pruning was enforced.
- Confirm that the Cluster_ID column is subsequently populated by assign_cluster_id() with unique identifiers for each component.
- Validate that within-cluster features share high correlation (r ≥ 0.9 per the find_connections threshold) and overlapping retention times (±1 s window).
- Compare cluster sizes and composition before and after pruning; verify that singletons or very sparse nodes were handled (removed or isolated) as expected.

## Limitations

- The degree threshold is user-defined and data-dependent; overly stringent thresholds may fragment biologically coherent clusters, while lenient thresholds may retain spurious associations.
- Iterative pruning is sensitive to the initial graph structure; if correlation thresholds in find_connections are too low or the RT window too wide, downstream clustering may conflate unrelated features.
- Features with genuinely low connectivity (e.g., rare metabolites or poorly ionized compounds) may be discarded by degree pruning even if they are true signals.
- The method assumes that high correlation and RT co-elution reliably indicate shared metabolite origin; this assumption can fail for multiply-charged ions, in-source fragments, or neutral-loss adducts that do not cluster identically.

## Evidence

- [other] Execute find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion.: "Run find_clusters() with degree threshold 0.8 on the connections output to decompose the graph into connected components and prune nodes iteratively until each node meets the minimum degree criterion"
- [other] find_clusters, and assign_cluster_id functions operate together to group related metabolic features and assign cluster identifiers: "find_connections, find_clusters, and assign_cluster_id functions operate together to group related metabolic features and assign cluster identifiers"
- [readme] A novel method for clustering similar molecular features: "A novel method for clustering similar molecular features"
- [readme] The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst: "The algorithm for clustering molecular features originating from the same compound is based on MATLAB code written by David Broadhurst"
