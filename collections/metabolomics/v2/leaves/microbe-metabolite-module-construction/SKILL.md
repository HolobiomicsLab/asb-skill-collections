---
name: microbe-metabolite-module-construction
description: Use when when you have trained multi-layer perceptron neural network
  models on paired microbiome-metabolome data (from ≥10-fold cross-validation iterations)
  and need to identify functional modules—groups of microbes and metabolites with
  co-varying or synergistic relationships—for systems-level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0203
  tools:
  - WGCNA
  - Seaborn clustermap
  - Cytoscape
  - Python scikit-learn
  - TensorFlow
  - scikit-learn
  license_tier: open
  provenance_tier: literature
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

# Microbe-Metabolite Module Construction via Biclustering

## Summary

Constructs functional modules of microbes and metabolites by biclustering normalized feature attribution scores derived from trained neural network weights, grouping organisms and compounds that share similar interaction patterns and metabolic roles.

## When to use

When you have trained multi-layer perceptron neural network models on paired microbiome-metabolome data (from ≥10-fold cross-validation iterations) and need to identify functional modules—groups of microbes and metabolites with co-varying or synergistic relationships—for systems-level biological interpretation beyond individual predictive correlations.

## When NOT to use

- Input data has not been filtered to retain only well-predicted metabolites (Spearman r > 95th percentile of background); biclustering will include spurious or weakly-predicted features.
- Microbiome-metabolome dataset pairs are unpaired (samples do not have simultaneous microbial and metabolomic measurements); attribution scores will be uninformative.
- Linear or elastic net models were used instead of neural networks; Olden's method for multi-layer weight matrices cannot be applied.

## Inputs

- Trained MLPNN weight matrices from ≥10 cross-validation iterations (100 models from 10 iterations of 10-fold CV)
- Well-predicted metabolite subset (those with Spearman correlation above 95th percentile of background)
- Normalized microbe-metabolite feature attribution score matrix

## Outputs

- Normalized microbe-metabolite attribution score matrix (values in [−1, 1])
- Microbe module membership assignments (k* clusters)
- Metabolite module membership assignments (k** clusters)
- Module interaction network edge list with attribution scores ≥ 0.25 in absolute value

## How to apply

First, extract weight matrices from all hidden layers of trained MLPNN models and compute microbe-metabolite feature attribution scores using Olden's method (element-wise product of weight matrices across layers). Generate a mean attribution matrix by averaging scores across all trained models, then apply a 97.5 percentile absolute-value threshold to identify significant scores; filter out microbes with no significant attributions to any well-predicted metabolite. Normalize all retained scores to [−1, 1] by dividing by the 97.5 percentile threshold. Apply hierarchical clustering (Euclidean distance, complete linkage) to the normalized score matrix, then perform consensus clustering with k ranging from 2 to 20, selecting k* (for microbes) and k** (for metabolites) as the largest k where the proportional change in cumulative distribution function area (Δk) exceeds 0.025. Finally, bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final consensus modules, outputting module membership assignments and the module interaction network.

## Related tools

- **TensorFlow** (Neural network framework for training MLPNN models and extracting weight matrices)
- **scikit-learn** (Hierarchical clustering and consensus clustering implementation)
- **WGCNA** (Comparison method for validating identified microbial modules)
- **Seaborn clustermap** (Visualization of clustered attribution score matrix)
- **Cytoscape** (Network visualization of module-based interaction graph)

## Evaluation signals

- Module membership is reproducible across multiple consensus clustering runs (Δk threshold consistently selects same k* and k**)
- All microbes in final output have ≥1 significant attribution score (absolute value > 97.5 percentile) with at least one well-predicted metabolite; no microbes with all scores below threshold remain
- Attribution score matrix row and column sums are non-zero for all module members (no zero-score rows or columns remain after biclustering)
- Module interaction network contains only edges with |score| ≥ 0.25 (for visualization); raw output includes all normalized scores
- k* and k** satisfy Δk > 0.025 for cumulative distribution function area; verify that selecting k+1 would yield Δk ≤ 0.025

## Limitations

- Attribution scores are derived data-dependently from the neural network weights and do not incorporate mechanistic or stoichiometric metabolic knowledge; modules reflect learned correlations, not necessarily causal relationships.
- Not all metabolites may be genuinely associated with microbes in the biologically relevant sense; metabolites with lower prediction correlations (r < 95th percentile of background) are excluded, potentially hiding important but weak associations.
- Biclustering performance is sensitive to the consensus clustering threshold (Δk = 0.025); different thresholds may yield different k* and k** values, affecting module granularity and composition.
- Threshold generalizability may vary by ecosystem: empirical threshold values (97.5 percentile, 95th percentile, Δk cutoff) were optimized for the IBD, cystic fibrosis, and soil datasets studied; application to novel environments may require threshold re-optimization.

## Evidence

- [other] MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members share similar attribution patterns.: "MiMeNet computes feature attribution scores for all microbe-metabolite pairs from trained MLPNN network weights, then applies biclustering to group microbes and metabolites into modules where members"
- [other] Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model.: "Calculate microbe-metabolite feature attribution scores S using Olden's method by multiplying weight matrices across layers (S = ∏ W_l for l ∈ L), producing one score matrix per trained model."
- [other] Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores (absolute value above threshold).: "Generate mean attribution matrix S* by averaging all 100 S_i matrices, then flatten into a feature vector and apply 97.5 percentile threshold to identify significant attribution scores (absolute"
- [other] Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage, then apply consensus clustering with k ranging from 2 to 20; calculate cumulative distribution function area for each k and select k* as the largest k where Δk (proportional change in area) exceeds 0.025 threshold.: "Perform hierarchical clustering on normalized attribution scores using Euclidean distance and complete linkage, then apply consensus clustering with k ranging from 2 to 20; calculate cumulative"
- [other] Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules.: "Bicluster the normalized score matrix using k* and k** to partition rows (microbes) and columns (metabolites) into final functional modules."
- [abstract] trained models are then used to derive microbe-metabolite feature scores, which are used for clustering microbes and metabolites into functional modules: "trained models are then used to derive microbe-metabolite feature scores, which are used for clustering microbes and metabolites into functional modules"
- [abstract] MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
- [methods] Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [methods] We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [methods] For visualization we removed any score whose absolute value was less than 0.25: "For visualization we removed any score whose absolute value was less than 0.25"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis"
- [discussion] since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites: "since not all metabolites may be associated with microbes, some metabolites will have lower prediction correlations, which resulted in an overall lower mean correlation across all metabolites"
