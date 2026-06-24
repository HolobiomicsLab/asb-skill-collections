---
name: feature-attribution-score-interpretation-neural-networks
description: Use when after training a neural network model (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_3957
  - http://edamontology.org/topic_0091
  tools:
  - MiMeNet
  - neural networks
  - ADAM optimizer
  - TensorFlow
  - scikit-learn
  - Matplotlib / Seaborn
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
- An MLPNN model is composed of multiple fully connected hidden layers
- we present MiMeNet, a neural network framework for modeling microbe-metabolite relationships
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function.
- MiMeNet was trained using the ADAM optimizer and the mean squared error (MSE) loss
  function
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

# feature-attribution-score-interpretation-neural-networks

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and interpret neural network feature attribution scores to identify significant microbe-metabolite interactions and construct functional modules. This skill transforms raw model weights into biologically interpretable interaction scores that reveal which microbial features drive metabolite predictions.

## When to use

After training a neural network model (e.g. MiMeNet MLPNN) to predict metabolite abundances from microbiome data and obtaining predictions on held-out test folds, use this skill to move beyond predictive accuracy toward mechanistic understanding: identify which specific microbes contribute most to predicting each well-predicted metabolite, group microbes and metabolites with similar interaction patterns into functional modules, and generate hypotheses about underlying microbe-metabolite relationships. Apply this skill when you have well-predicted metabolites (SCC > 95th percentile background threshold) and want to illuminate the network structure rather than just evaluate classification performance.

## When NOT to use

- Input contains no well-predicted metabolites (all metabolite SCCs fall below 95th percentile threshold) — model may be too weak or data too noisy to support mechanistic interpretation.
- Neural network model has not been adequately cross-validated or evaluated; feature attributions from a single non-validated fit may not generalize.
- Goal is purely predictive (e.g., building a black-box metabolite abundance predictor for external application) rather than interpretive — use model evaluation metrics (MSE, SCC, classification accuracy) instead.

## Inputs

- Trained neural network model(s) from cross-validation iterations (e.g., 10 iterations × 10 folds = 100 models)
- Network weights or activation gradients from MLPNN hidden and output layers
- Spearman correlation coefficient (SCC) predictions for each metabolite on held-out test folds
- Background SCC distribution (from shuffled/null model cross-validations)
- Well-predicted metabolite list (metabolites with SCC > 95th percentile of background)

## Outputs

- Microbe-metabolite feature attribution score matrix (microbes × well-predicted metabolites)
- Filtered/thresholded attribution score matrix (scores with |value| ≥ 0.25 for visualization)
- Microbe module assignments (clusters of microbes with similar attribution patterns)
- Metabolite module assignments (clusters of well-predicted metabolites with similar microbe drivers)
- Module-based interaction network (bipartite graph linking microbe modules to metabolite modules)
- Scatterplots or heatmaps comparing attribution scores across modules or samples

## How to apply

First, construct a score matrix of microbe-metabolite feature attributions derived from the trained neural network weights, computing one attribution score per microbe-metabolite pair across all well-predicted metabolites. Filter this matrix to retain only microbes with at least one significant attribution score (absolute value above the 97.5 percentile of background correlations) and set interaction visualization thresholds (e.g., remove scores with absolute value < 0.25). Then biclustering algorithm (e.g., spectral or consensus clustering) on the filtered score matrix to identify coherent groups of microbes and metabolites that co-vary in their interaction strengths, yielding microbe and metabolite modules. These modules group features with similar functional or interaction signatures; annotated metabolites within a module can then help infer the function of unannotated co-clustered metabolites. Evaluate module robustness by checking that well-predicted metabolites cluster together and that module membership is consistent across cross-validation folds.

## Related tools

- **MiMeNet** (Neural network framework that trains MLPNN models, generates background distributions, and constructs feature attribution score matrices for microbe-metabolite interpretation) — https://github.com/YDaiLab/MiMeNet
- **TensorFlow** (Deep learning framework underlying MiMeNet MLPNN model training and weight extraction for attribution scoring)
- **scikit-learn** (Provides clustering and biclustering algorithms (e.g., spectral clustering) to partition microbe-metabolite attribution score matrix into functional modules)
- **Matplotlib / Seaborn** (Visualization of scatterplots comparing attribution scores, heatmaps of module membership, and network diagrams)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR -net_params results/IBD/network_parameters.txt -annotation data/IBD/metabolome_annotation.csv -labels data/IBD/diagnosis_PRISM.csv -num_run_cv 10 -output IBD
```

## Evaluation signals

- Feature attribution scores are derived from neural network weights and fall within a bounded range; significance threshold (97.5 percentile) is computed relative to empirical background distribution from shuffled cross-validations.
- Microbes retained in the filtered score matrix have at least one significant attribution score; total microbe count matches statement like 'We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite'.
- Modules exhibit biological coherence: annotated metabolites co-cluster with unannotated metabolites, and microbes within a module share known functional roles or taxonomic relationships.
- Module membership is stable across cross-validation folds: microbe-metabolite pairs appearing in modules at iteration i also appear in iteration j (robustness check).
- Visualization thresholds (e.g., |score| ≥ 0.25) are applied uniformly; resulting module network is sparse and interpretable (not a dense hairball).

## Limitations

- Feature attribution scores are data-driven and do not incorporate mechanistic knowledge of microbial metabolism; observed associations may be confounded or indirect rather than causal.
- Not all metabolites associate with microbes, so some metabolites will have lower prediction correlations and fewer or weaker attribution scores; modules derived from low-SCC metabolites may be unreliable.
- Attribution scores depend on neural network architecture (hidden layer size, regularization, dropout) and hyperparameter tuning; different architectures may yield different module structures.
- Longitudinal or time-series data may inflate apparent correlation thresholds and alter module structure; implication for dataset-specific threshold calibration not fully explored.
- Biclustering and module assignment are unsupervised; no ground truth exists for validating module biological correctness without independent functional annotation.

## Evidence

- [results] score matrix interpretation and module construction: "MiMeNet constructs a score matrix of microbe-metabolite feature attributions between the microbes and well-predicted metabolites. Then MiMeNet biclusters the score matrix into microbial and"
- [methods] significance threshold for attribution scores: "Any feature attribution score in the observed dataset with an absolute value above the threshold was considered significant"
- [methods] well-predicted metabolite threshold: "We then defined a metabolite as well-predicted if its SCC is above the 95th percentile of the background correlations"
- [results] background distribution generation: "MiMeNet then generates a background distribution of SCCs through multiple iterations of shuffling the dataset and performing a cross-validation on the shuffled set"
- [results] microbe filtering and network visualization: "We identified 163 microbes that had at least one significant attribution score with a well-predicted metabolite"
- [methods] visualization threshold application: "For visualization we removed any score whose absolute value was less than 0.25"
- [results] module-based network construction: "construct a module-based interaction network"
- [discussion] feature attribution and module interpretation rationale: "the feature attribution scores derived from the network weights could be used to construct modules"
