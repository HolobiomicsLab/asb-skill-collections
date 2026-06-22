---
name: biclustering-for-omics-features
description: Use when you have a normalized matrix of feature attribution scores (microbes × metabolites) derived from a trained neural network, and you want to partition both microbes and metabolites simultaneously into co-clusters that share similar interaction patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3174
  tools:
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - scikit-learn consensus clustering
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- Weighted correlation network analysis (WGCNA) of microbial features was performed using the WGCNA library in R
- compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet to those identified by the Weighted Correlation Network Analysis (WGCNA)
- using Seaborn's clustermap function in Python
- using Cytoscape
- using Python's sci-kit-learn package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009021
  all_source_dois:
  - 10.1371/journal.pcbi.1009021
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# biclustering-for-omics-features

## Summary

Biclustering partitions rows (microbes) and columns (metabolites) of a normalized feature attribution score matrix into functional modules, grouping features with similar interaction patterns to illuminate the underlying structure of microbe-metabolite interaction networks.

## When to use

You have a normalized matrix of feature attribution scores (microbes × metabolites) derived from a trained neural network, and you want to partition both microbes and metabolites simultaneously into co-clusters that share similar interaction patterns. This is appropriate when you seek to discover modules of microbes and metabolites that interact together, rather than clustering features independently.

## When NOT to use

- Your input is a raw, un-normalized correlation matrix or distance matrix; attribution scores must first be filtered (97.5 percentile threshold) and normalized to [-1, 1].
- You have fewer than ~2 metabolites or microbes to cluster; consensus clustering requires sufficient features to estimate stable clustering structure.
- The feature attribution matrix is sparse (>50% zeros) and lacks sufficient co-variation patterns; biclustering may produce artifacts when co-occurrence is rare.

## Inputs

- Normalized feature attribution score matrix (microbes × metabolites, values in [-1, 1])
- Background distribution of attribution scores (for threshold calculation)
- List of well-predicted metabolites (those above 95th percentile correlation threshold)

## Outputs

- Microbe cluster assignments (k* clusters)
- Metabolite cluster assignments (k** clusters)
- Functional modules (bicluster membership assignments)
- Module interaction network edge list

## How to apply

First, normalize all significant feature attribution scores to the range [-1, 1] by dividing by the 97.5 percentile threshold from a background distribution. Perform hierarchical clustering on the normalized attribution scores using Euclidean distance and complete linkage, then apply consensus clustering with k ranging from 2 to 20, calculating the cumulative distribution function (CDF) area for each k and selecting k* as the largest k where Δk (proportional change in area) exceeds a 0.025 threshold. Repeat this consensus clustering procedure independently for metabolites to identify k**. Finally, bicluster the normalized score matrix using k* for rows (microbes) and k** for columns (metabolites) to partition the data into final functional modules. This approach ensures biologically meaningful co-clustering by identifying the optimal number of clusters separately for each dimension based on consensus stability.

## Related tools

- **scikit-learn consensus clustering** (Performs hierarchical clustering with Euclidean distance and complete linkage, calculates CDF area for k-selection)
- **WGCNA** (Alternative module detection method for comparison; groups features by correlation-based network analysis)
- **Seaborn clustermap** (Visualization of biclustered heatmaps showing module structure and interaction patterns)
- **Cytoscape** (Network visualization of module-based interaction networks and inter-module connections)

## Examples

```
# From MiMeNet README: performs biclustering on normalized attribution matrix via internal consensus clustering
python MiMeNet_train.py -micro microbiome.csv -metab metabolome.csv -output results/ -num_run_cv 10 -num_cv 10 -threshold 0.025
```

## Evaluation signals

- Δk threshold exceeded: verify that selected k* and k** correspond to the largest k value where Δk (proportional change in CDF area) exceeds 0.025, confirming consensus stability.
- Non-empty modules: all k* × k** bicluster partitions should be non-empty; if any module contains zero features, k values may be too large or data insufficiently structured.
- Score matrix coverage: module assignments should account for all microbes with ≥1 significant attribution score (|score| ≥ 97.5 percentile) and all well-predicted metabolites (SCC ≥ 95th percentile of background).
- Module interpretability: modules should show strong within-module correlation in attribution scores; mean |score| within modules should exceed mean |score| between modules.
- Consistency with network structure: module interaction network should reflect the directionality and magnitude of normalized attribution scores (positive vs. negative scores corresponding to distinct module types).

## Limitations

- Biclustering results depend critically on the choice of k range and Δk threshold (0.025); sensitivity analysis on this threshold is recommended, as different thresholds may yield different module counts.
- The method assumes that microbes and metabolites with similar attribution patterns are functionally related, but attribution scores are derived from a data-driven neural network and do not incorporate mechanistic or metabolic knowledge.
- Longitudinal or temporally structured datasets (e.g., soil wetting time-series) may exhibit higher consensus clustering thresholds, potentially inflating k values and fragmenting modules; biological context should guide interpretation.
- Modules derived from one dataset may not generalize to external cohorts; external validation is necessary to confirm module robustness across populations or environments.

## Evidence

- [other] Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules.: "Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules."
- [other] Apply consensus clustering with k ranging from 2 to 20; calculate cumulative distribution function area for each k and select k* as the largest k where Δk (proportional change in area) exceeds 0.025 threshold.: "apply consensus clustering with k ranging from 2 to 20; calculate cumulative distribution function area for each k and select k* as the largest k where Δk (proportional change in area) exceeds 0.025"
- [other] Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage.: "Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage"
- [abstract] MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
- [abstract] trained models are then used to derive microbe-metabolite feature scores, which are used for clustering microbes and metabolites into functional modules: "trained models are then used to derive microbe-metabolite feature scores, which are used for clustering microbes and metabolites into functional modules"
- [discussion] We also observed a higher threshold value for the soil data, which may be due to the longitudinal observations: "We also observed a higher threshold value for the soil data, which may be due to the longitudinal observations"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
