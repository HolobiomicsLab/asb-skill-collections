---
name: network-module-interaction-scoring
description: Use when after biclustering a normalized microbe-metabolite feature attribution
  score matrix into distinct functional modules, use this skill to summarize pairwise
  module interactions by aggregating scores between all microbe-metabolite pairs from
  different modules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_2885
  - http://edamontology.org/topic_3697
  tools:
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - scikit-learn
  - MiMeNet
  - Python
  - Consensus clustering
  - Wilcoxon rank-sum test
  - Python (Pandas, NumPy, SciPy)
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- Weighted correlation network analysis (WGCNA) of microbial features was performed
  using the WGCNA library in R
- compared the microbial modules in the IBD (PRISM) dataset identified by MiMeNet
  to those identified by the Weighted Correlation Network Analysis (WGCNA)
- using Seaborn's clustermap function in Python
- using Cytoscape
- using Python's sci-kit-learn package
- linkage using Seaborn’s clustermap function in
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  - build: coll_mimenet_cq
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

# Network Module Interaction Scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a module-based interaction network by aggregating microbe-metabolite feature attribution scores within and between biclustered functional modules. This skill quantifies the strength and direction of interactions across module boundaries, enabling visualization and interpretation of higher-order community structure.

## When to use

After biclustering a normalized microbe-metabolite feature attribution score matrix into distinct functional modules, use this skill to summarize pairwise module interactions by aggregating scores between all microbe-metabolite pairs from different modules. This is particularly useful when you have well-predicted metabolites (Spearman correlation above the 95th percentile of background) and want to move from pair-wise interactions to coarser module-level interaction networks suitable for biological interpretation or network visualization.

## When NOT to use

- The input feature attribution scores have not yet been normalized to [-1, 1] or do not derive from a trained neural network model—use raw MLPNN weights or untrained correlation matrices instead.
- Microbes and metabolites have not been clustered into modules yet; construct modules via consensus clustering on normalized scores before attempting interaction scoring.
- Your goal is to preserve and interpret every individual microbe-metabolite pair interaction—aggregating to module level will lose resolution.

## Inputs

- Biclustered module membership assignments (microbe module IDs and metabolite module IDs)
- Normalized microbe-metabolite feature attribution score matrix (values in [-1, 1] range)
- Well-predicted metabolite list (filtered by 95th percentile correlation threshold)
- Optional: metabolite functional annotations

## Outputs

- Module interaction network edge list (source_module, target_module, interaction_score)
- Module interaction network statistics (edge counts, score distribution, module degree)
- Network visualization (e.g., Cytoscape-compatible format or adjacency matrix)
- Module annotation summary (functional enrichment or metabolite class per module)

## How to apply

For each pair of modules (one containing microbes, one containing metabolites), compute the mean or sum of the absolute values of normalized attribution scores (range [-1, 1]) between all microbe-metabolite pairs spanning the two modules. To reduce visualization clutter and focus on strong interactions, apply a filtering threshold—the MiMeNet study recommends removing any interaction score with absolute value less than 0.25. The resulting edge list represents directed or weighted edges in a module interaction graph, where node degree and edge weight can be interpreted as the strength of functional coupling between modules. Optionally, annotate modules using metabolite annotations (if available) to map functional roles to network structure.

## Related tools

- **Cytoscape** (Visualization and interactive exploration of module-level interaction networks) — https://cytoscape.org
- **scikit-learn** (Consensus clustering and hierarchical clustering used to define modules from attribution scores) — https://scikit-learn.org
- **Seaborn clustermap** (Heatmap visualization of aggregated module interaction scores) — https://seaborn.pydata.org
- **MiMeNet** (Source neural network model for computing feature attribution scores and biclustering modules) — https://github.com/YDaiLab/MiMeNet

## Examples

```
# After consensus-clustered module assignments (k*=5 microbe modules, k**=3 metabolite modules) and normalized scores in S* (shape: 163 microbes × 52 metabolites), compute module interaction edge list:
import pandas as pd
module_interactions = []
for m_idx in range(5):  # microbe modules
    for met_idx in range(3):  # metabolite modules
        microbes_in_module = microbe_assignments[microbe_assignments == m_idx].index
        metabolites_in_module = metabolite_assignments[metabolite_assignments == met_idx].index
        scores = S_normalized.loc[microbes_in_module, metabolites_in_module].values
        mean_score = scores.mean()
        if abs(mean_score) >= 0.25:
            module_interactions.append({'microbe_module': m_idx, 'metabolite_module': met_idx, 'interaction_score': mean_score})
edge_list = pd.DataFrame(module_interactions)
edge_list.to_csv('module_interactions.txt', sep='\t', index=False)
```

## Evaluation signals

- Edge list is non-empty and contains module pairs with interaction scores that span the full [-1, 1] range (not all zeros or identical values).
- After filtering by threshold (e.g., |score| < 0.25), remaining edges have scores whose absolute value is consistently ≥ 0.25; no spurious low-magnitude edges remain.
- Module interaction network degree distribution is consistent with biological expectation: most modules have a small number of significant partners (hub-and-spoke or modular topology rather than complete graph).
- Positive and negative attribution scores are preserved in the interaction edge list, allowing interpretation of cooperative vs. antagonistic module relationships.
- Network visualization (Cytoscape or adjacency matrix) shows clear visual separation between high- and low-interaction module pairs, with module size proportional to member counts.

## Limitations

- Module interaction scores are data-driven and do not incorporate mechanistic knowledge of metabolism or microbial physiology; strong module interactions may be correlative rather than causal.
- Aggregation to module level discards information about individual microbe-metabolite relationships, making it difficult to pinpoint specific driver species or compounds.
- Interaction scores depend heavily on the choice of consensus clustering threshold (Δk cutoff for selecting k* and k**); different thresholds may yield different module boundaries and thus different interaction networks.
- Not all metabolites may be truly associated with microbes; some low-correlation metabolites filtered out at the 95th percentile threshold may harbor real interactions masked by noise, leading to incomplete module interaction networks.
- Network inference is limited by the quality and completeness of input microbiome and metabolome data; missing or poorly quantified features will bias both attribution scores and module structure.

## Evidence

- [methods] Construct microbe-metabolite feature attribution score matrix and bicluster into modules: "MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites. Then MiMeNet biclusters the score matrix into microbial and"
- [methods] Filter interaction scores by absolute value threshold of 0.25 for visualization: "For visualization we removed any score whose absolute value was less than 0.25"
- [results] Compute module interactions by aggregating feature attribution scores: "construct a module-based interaction network"
- [methods] Use Cytoscape for module interaction network visualization: "tools: neural networks, WGCNA, Seaborn clustermap, Cytoscape, Python scikit-learn"
- [abstract] Feature attribution scores derived from network weights range from positive to negative: "Positive attribution scores indicate microbes that contribute positively to metabolite abundance prediction, while negative scores indicate negative contributions"
- [methods] Well-predicted metabolites threshold at 95th percentile of background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
