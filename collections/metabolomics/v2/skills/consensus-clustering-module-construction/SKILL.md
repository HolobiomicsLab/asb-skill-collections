---
name: consensus-clustering-module-construction
description: Use when after training a neural network model on paired microbiome-metabolome data and extracting microbe-metabolite feature attribution scores for significant interactions (e.g., at the 97.5th percentile threshold).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0625
  tools:
  - Elastic Net
  - MiMeNet
  - TensorFlow or PyTorch
  - scikit-learn
  - Seaborn
  - Python
  - consensus clustering
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- we benchmarked MiMeNet against other general regression models, i.e., Random Forest (RF), multivariate Elastic Net, and canonical correlation analysis (CCA) models
- MiMeNet (Microbiome-Metabolome Network), a multi-layer perceptron (MLPNN)
- MiMeNet uses paired microbiome and metabolome data for model training. Microbiome abundance features (green) are used to train a neural network to predict metabolite abundance features (blue).
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss function.
- MelonnPan and NED models were obtained from their respective GitHub repositories and executed using default parameters as according to their tutorials. Random Forest, multivariate Elastic Net, and
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Consensus-clustering module construction

## Summary

Group microbes and metabolites with similar interaction patterns into functional modules by biclustering normalized feature attribution score matrices, using consensus clustering with data-driven k* selection. This recovers the latent structure of microbe-metabolite interaction networks and enables module-level biomarker discovery.

## When to use

After training a neural network model on paired microbiome-metabolome data and extracting microbe-metabolite feature attribution scores for significant interactions (e.g., at the 97.5th percentile threshold). Use this skill when you want to group co-interacting microbes and metabolites to illuminate functional relationships, especially when individual microbial or metabolite annotations are sparse or when you seek to validate predicted modules against known disease states.

## When NOT to use

- Attribution score matrix contains <10 significant microbe-metabolite interactions; consensus clustering requires sufficient data density to recover meaningful structure.
- Background distribution was not generated (i.e., no shuffled cross-validation performed); modules would lack statistical grounding and risk spurious clustering.
- Microbes or metabolites have already been pre-assigned to known pathways or functional categories and you seek to validate only those assignments rather than discover de novo structure.

## Inputs

- Normalized microbe-metabolite feature attribution score matrix (S; rows=microbes, columns=well-predicted metabolites, values ∈ [−1, 1])
- Background threshold scores derived from 100+ shuffled cross-validation iterations
- Sample phenotype labels (optional, for enrichment testing)

## Outputs

- Microbial module assignments (microbe ID → module ID)
- Metabolomic module assignments (metabolite ID → module ID)
- Module-level interaction network (edges connect microbes and metabolites within modules)
- Module enrichment statistics (Wilcoxon rank-sum p-values per module, mean feature values by phenotype)

## How to apply

Construct a normalized feature attribution score matrix S by: (1) dividing all significant interaction scores by the background threshold identified from shuffled data and clipping values to [−1, 1]; (2) biclustering S using consensus clustering, determining the optimal number of clusters (k*) via area-under-cumulative-distribution-function (CDF) analysis with Δk threshold of 0.025; (3) extracting the resulting microbial and metabolomic module membership from the bicluster rows and columns. The rationale is that co-clustering scores reflect shared microbe-metabolite interaction patterns; normalization by background thresholds ensures modules are robust to data-specific noise; the Δk threshold balances cluster granularity against overfitting. Validate modules by testing enrichment for phenotypic labels (e.g., IBD vs. healthy) using Wilcoxon rank-sum test on mean normalized feature values within each module.

## Related tools

- **MiMeNet** (Neural network framework that trains models to produce feature attribution scores and orchestrates consensus clustering module construction) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (Provides clustering algorithms and statistical tests (Wilcoxon rank-sum) used in module construction and enrichment validation)
- **consensus clustering** (Core algorithm for deriving stable, robust microbial and metabolomic modules from normalized attribution matrices)
- **Seaborn** (Visualization of module-level interaction networks and enrichment heatmaps)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -annotation data/IBD/metabolome_annotation.csv -labels data/IBD/diagnosis_PRISM.csv -num_run_cv 10 -output IBD
```

## Evaluation signals

- Module size distribution is reasonable (not all microbes/metabolites in one cluster, not singleton clusters); median module size >2 members suggests k* selection was effective.
- Modules show statistically significant enrichment for at least one phenotype (Wilcoxon p<0.05 for ≥1 module), indicating modules capture biological signal beyond noise.
- Normalized attribution scores within modules are higher in magnitude than between-module scores; within-module mean |score| > between-module mean |score|.
- Modules remain stable across repeated consensus clustering runs (Adjusted Rand Index >0.8 between subsampled runs) or across different k* selection thresholds (Δk ∈ [0.02, 0.03]).
- Module members share annotated metabolic pathways or known microbe-metabolite interactions, validating inferred co-clustering against external knowledge.

## Limitations

- Consensus clustering assumes interaction patterns are truly modular; if microbe-metabolite interactions form a single continuum or highly interconnected network, clustering may produce artificial partitions.
- Module membership is deterministic only for the k* selected via CDF-Δk; small changes in background threshold or data composition may alter k*, affecting downstream module assignments.
- Modules are constructed from normalized attribution scores, not raw counts or absolute interaction strength; scores in [−1, 1] obscure quantitative differences in microbe-metabolite effect sizes.
- Not all metabolites may be associated with microbes; metabolites with truly microbe-independent biology will form singleton or noise-dominated modules, inflating false cluster count.
- Module enrichment tests (Wilcoxon rank-sum) assume independent samples; longitudinal or repeated-measure designs may violate assumptions and require stratified or mixed-model alternatives.

## Evidence

- [results] construct a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted: "using the learned network weights obtained from cross-validation training, MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted"
- [methods] normalize and clip attribution scores to construct modules: "We normalized the values in each feature attribution score matrix Si by dividing the significant threshold score identified from the background and clipped values to be between -1 and 1"
- [methods] area-under-CDF with Δk threshold for k* determination: "construct microbial and metabolite modules via consensus clustering (k* determined by area-under-CDF with Δk threshold=0.025)"
- [results] bicluster score matrix into modules: "Then MiMeNet biclusters the score matrix into microbial and metabolomic modules"
- [methods] Wilcoxon rank-sum test for module enrichment: "we determine if a module is enriched for one patient group (IBD or healthy) by comparing the average normalized feature values of the members within the module between the two groups using the IBD"
- [abstract] MiMeNet can group microbes and metabolites with similar interaction patterns: "MiMeNet can group microbes and metabolites with similar interaction patterns and functions to illuminate the underlying structure of the microbe-metabolite interaction network"
- [readme] README consensus clustering via biclustering: "This interaction score matrix is biclustered into microbe and metabolite modules, grouping sets of microbes and metabolites with similar interaction patterns."
