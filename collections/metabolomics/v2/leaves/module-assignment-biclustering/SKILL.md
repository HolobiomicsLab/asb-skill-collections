---
name: module-assignment-biclustering
description: Use when you have a trained neural network model of microbiome-metabolome
  associations and have derived a feature attribution score matrix (microbes × metabolites)
  quantifying the strength of each microbe-metabolite interaction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_3697
  tools:
  - Seaborn clustermap
  - Python
  - Cytoscape
  - Hierarchical clustering (Euclidean distance, complete linkage)
  - Consensus clustering
  - Python (Numpy, Pandas, Scikit-learn)
  license_tier: open
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- linkage using Seaborn’s clustermap function in
- using Python's sci-kit-learn package
- Networks showing microbe and metabolite modules and the interactions between them
  were constructed using Cytoscape
- Networks showing the modules and the interactions between them were constructed
  using Cytoscape
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mimenet_cq
    doi: 10.1371/journal.pcbi.1009021
    title: MiMeNet
  dedup_kept_from: coll_mimenet_cq
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

# Reconstruct microbe-metabolite functional modules by clustering the feature attribution matrix

## Summary

This skill uses biclustering on normalized microbe-metabolite feature attribution score matrices to group microbes and metabolites into co-occurrence modules with similar interaction patterns. The method identifies optimal cluster numbers via consensus clustering across multiple trained models, enabling discovery of functional relationships in microbiome-metabolome networks.

## When to use

Apply this skill when you have a trained neural network model of microbiome-metabolome associations and have derived a feature attribution score matrix (microbes × metabolites) quantifying the strength of each microbe-metabolite interaction. Use it specifically after identifying well-predicted metabolites and filtering to retain only microbes with at least one significant attribution score, to reveal the underlying modular structure of the interaction network.

## When NOT to use

- The feature attribution score matrix has not been normalized or contains raw correlation values without background-derived thresholds.
- Microbes or metabolites have not been filtered; the matrix still contains features with no significant associations across the network.
- The input matrix is sparse or extremely small (fewer than 5 microbes or metabolites per cluster), which may lead to unstable hierarchical clustering and unreliable consensus matrices.

## Inputs

- Normalized feature attribution score matrix S* (microbes × metabolites, values in [−1, 1])
- Background distribution of attribution scores from shuffled cross-validation iterations
- Significant attribution threshold (e.g., 97.5th percentile of background)
- Set of well-predicted metabolites (filtered by SCC cutoff from background distribution)
- Set of microbes with at least one significant attribution score to well-predicted metabolites

## Outputs

- Optimal microbe cluster number k₁*
- Optimal metabolite cluster number k₂*
- Module membership assignments for microbes (microbe ID → module ID)
- Module membership assignments for metabolites (metabolite ID → module ID)
- Module feature vectors (average normalized abundance of members within each module)
- Consensus clustering matrices and CDF curves for all k values tested

## How to apply

First, normalize the feature attribution score matrix by dividing each element by the significant threshold score (e.g., 97.5th percentile) derived from a background distribution of shuffled data, then clip all values to the range [−1, 1]. Second, perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage. Third, for each candidate cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all cross-validation folds (e.g., 100 trained models). Fourth, calculate the cumulative distribution function (CDF) of each consensus matrix and compute the area under the curve. Fifth, determine the optimal microbe cluster number k₁* and metabolite cluster number k₂* by selecting the largest k where the proportional change in area between consecutive k values (Δk) exceeds a threshold (e.g., 0.025). Finally, perform final biclustering using the normalized score matrix with k₁* and k₂* to assign microbes and metabolites to their final module memberships.

## Related tools

- **Seaborn clustermap** (Performs hierarchical clustering on matrix rows and columns with Euclidean distance and complete linkage to initialize clustering for consensus step.)
- **Hierarchical clustering (Euclidean distance, complete linkage)** (Core algorithm for grouping microbes and metabolites based on attribution score similarity; integrated into consensus clustering loop across multiple models.)
- **Consensus clustering** (Aggregates clustering results across 100 cross-validated model iterations to compute stability metrics (consensus matrices and CDF-based area metrics) for cluster number selection.)
- **Python (Numpy, Pandas, Scikit-learn)** (Matrix normalization, threshold computation, CDF calculation, and cluster assignment logic.) — https://github.com/YDaiLab/MiMeNet
- **Cytoscape** (Network visualization of module-based interaction graphs derived from biclustering results.)

## Evaluation signals

- Optimal cluster numbers k₁* and k₂* are identified where Δk (proportional change in CDF area) exceeds the 0.025 threshold; confirm that the selected k values are the largest k satisfying this criterion, not arbitrary choices.
- All normalized attribution scores lie within [−1, 1]; verify no out-of-range values remain after clipping.
- Each module contains at least one microbe and one metabolite with non-zero mean module feature values; confirm no empty or singleton modules are created.
- Consensus matrices are symmetric and have values in [0, 1] representing the proportion of co-clustering across 100 models; verify that high-confidence modules (consensus values close to 1) correspond to stable, reproducible groupings.
- Module enrichment analysis using Wilcoxon rank-sum test (P < 0.05) shows statistically significant differences in module feature abundance between phenotype groups (e.g., IBD vs. healthy), validating that modules capture biologically meaningful variation.

## Limitations

- Consensus clustering and optimal k selection depend critically on the number of cross-validation iterations and the choice of area-change threshold (Δk = 0.025); different thresholds or fewer models may yield different cluster numbers and module assignments.
- The method assumes that microbes and metabolites with similar feature attribution patterns represent genuine functional relationships, but does not incorporate mechanistic prior knowledge or validated biochemical interactions; data-driven modules may reflect statistical correlations rather than direct or indirect causal mechanisms.
- Hierarchical clustering with complete linkage is sensitive to outliers and may fragment large clusters if a few microbes or metabolites have atypical attribution profiles; alternative linkage criteria (e.g., average or Ward) were not evaluated.
- The normalized attribution score matrix only captures microbe-to-metabolite associations learned by the neural network; microbes or metabolites not well-represented in the training data or with weak associations are filtered out beforehand, reducing the scope of the modular decomposition.
- Longitudinal or replicate samples (as noted in soil biocrust data) may inflate prediction correlations and shift the significant attribution threshold, potentially affecting module boundaries and stability.

## Evidence

- [other] MiMeNet uses biclustering on the microbe-metabolite attribution score matrix to group microbes and metabolites into modules: "MiMeNet uses biclustering on the microbe-metabolite attribution score matrix to group microbes and metabolites into modules, identifying 8 modules of microbes and 8 modules of metabolites, with"
- [other] Normalize the feature attribution score matrix S_i by dividing by the significant threshold score: "Normalize the feature attribution score matrix S_i by dividing by the significant threshold score from background distribution and clip values to range [-1, 1]."
- [other] Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap: "Perform hierarchical clustering separately on microbe rows and metabolite columns using Euclidean distance and complete linkage with Seaborn's clustermap."
- [other] For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models: "For each fixed cluster number k ranging from 2 to 20, generate a k-clustering and compute a consensus matrix by averaging connectivity matrices across all 100 trained models."
- [other] Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by selecting the largest k where the proportional change in area (Δk) exceeds 0.025 threshold: "Determine optimal cluster numbers k₁* (microbes) and k₂* (metabolites) by selecting the largest k where the proportional change in area (Δk) exceeds 0.025 threshold."
- [other] Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships: "Bicluster the normalized score matrix S* using k₁* and k₂* to assign microbes and metabolites to their final module memberships."
- [methods] a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant: "a threshold was set at the 97.5 percentile. Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [results] We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [results] we determine if a module is enriched for one patient group (IBD or healthy) by comparing the average normalized feature values of the members within the module between the two groups using the IBD: "we determine if a module is enriched for one patient group (IBD or healthy) by comparing the average normalized feature values of the members within the module between the two groups"
- [abstract] MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
- [discussion] Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge: "Although the MiMeNet analysis is data-driven without incorporating mechanistic knowledge, these types of evidence obtained from the integrative analysis of metagenomes and metabolomes could be used"
