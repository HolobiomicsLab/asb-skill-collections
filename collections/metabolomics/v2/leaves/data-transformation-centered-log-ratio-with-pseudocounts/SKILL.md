---
name: data-transformation-centered-log-ratio-with-pseudocounts
description: Use when you have raw microbiome (e.g., 16S rRNA or metagenomic) or metabolomic
  count tables (samples × features) and plan to train predictive models (e.g., MiMeNet,
  linear regression) that require normally distributed or near-normally distributed
  inputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3174
  tools:
  - MiMeNet
  - ADAM optimizer
  - scikit-learn
  - pandas
  - scipy
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1009021
  title: MiMeNet
evidence_spans:
- An MLPNN model is composed of multiple fully connected hidden layers composed of
  perceptrons
- MiMeNet is an integrative MLPNN, which trains models to accurately predict the metabolome
  based on a microbiome
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

# data-transformation-centered-log-ratio-with-pseudocounts

## Summary

Apply centered log-ratio (CLR) transformation with a pseudocount to compositional microbiome and metabolomic count data, converting them to log-scale relative abundances suitable for downstream regression and neural network modeling. This transformation addresses the compositional nature of sequencing data and prevents log(0) errors.

## When to use

You have raw microbiome (e.g., 16S rRNA or metagenomic) or metabolomic count tables (samples × features) and plan to train predictive models (e.g., MiMeNet, linear regression) that require normally distributed or near-normally distributed inputs. CLR transformation is particularly necessary when features sum to a constant per sample (compositional data) and zero counts are present.

## When NOT to use

- Input data is already in relative abundance or log-transformed form; applying CLR again will double-transform and distort relationships.
- Your model explicitly expects count data (e.g., Poisson or negative-binomial GLM); CLR transformation is incompatible with count-based likelihood functions.
- You are performing downstream analyses (e.g., WGCNA, correlation networks) that explicitly require or expect the original scale; verify that the tool accepts log-transformed input before applying CLR.

## Inputs

- raw microbiome count table (samples × microbial features, e.g., CSV with integer counts)
- raw metabolomic count table (samples × metabolite features, e.g., CSV with integer counts)

## Outputs

- centered log-ratio transformed microbiome abundance matrix (samples × microbial features, continuous values)
- centered log-ratio transformed metabolomic abundance matrix (samples × metabolite features, continuous values)

## How to apply

For each sample, add a pseudocount (typically 1) to all count values to avoid log(0) errors. Then compute the centered log-ratio: for each feature, divide its count (+ pseudocount) by the geometric mean of all features in that sample (+ pseudocount), then take the natural logarithm. The result is a feature-by-sample matrix of log-transformed, centered relative abundances. Apply this transformation identically to both training and validation/test data, or to paired microbiome–metabolomic datasets prior to filtering low-abundance features (e.g., those present in <10% of samples) and before feeding into neural network or regression models.

## Related tools

- **MiMeNet** (neural network framework that accepts CLR-transformed microbiome and metabolomic data as inputs for prediction and module discovery) — https://github.com/YDaiLab/MiMeNet
- **scikit-learn** (Python library used for preprocessing and cross-validation after CLR transformation)
- **pandas** (Python data manipulation library used to load and transform count matrices)
- **scipy** (Python scientific library providing geometric mean and log functions for CLR computation)

## Examples

```
python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -micro_norm None -metab_norm CLR -num_run_cv 10 -output results
```

## Evaluation signals

- No NaN or Inf values appear in the transformed matrix; verify geometric mean computation handles zero counts correctly via pseudocount addition.
- Transformed values are continuous (not integers) and span a range typical of log-scale data (e.g., from ~−10 to +10 depending on feature abundance).
- When fed to the neural network model (MiMeNet with ADAM optimizer and mean squared error loss), training loss converges and validation Spearman correlation coefficients for metabolites are comparable to those reported in the article (mean SCC > 0.25 for annotated metabolites on IBD data).
- Feature distributions post-transformation are approximately normal or symmetric (histograms or Q-Q plots), improving suitability for linear and neural network models.
- The same pseudocount value and CLR procedure are applied consistently across all training, validation, and external test sets to avoid data leakage and ensure reproducibility.

## Limitations

- The choice of pseudocount (typically 1) is somewhat arbitrary; sensitivity analysis may be warranted for datasets with extreme sparsity or very high-depth sequencing.
- CLR transformation does not recover absolute abundances; it preserves only relative information and compositional relationships within each sample.
- Not all metabolites may be associated with microbes after transformation, resulting in lower prediction correlations for some features and potentially lower overall mean Spearman correlation coefficients across all metabolites.
- The article notes that MiMeNet analysis is data-driven without incorporating mechanistic knowledge; CLR transformation alone does not add biological interpretability to unannotated metabolites.

## Evidence

- [other] Load IBD (PRISM) microbiome and metabolomic data, apply centered log-ratio transformation with pseudocount of 1, and filter features present in <10% of samples.: "Load IBD (PRISM) microbiome and metabolomic data, apply centered log-ratio transformation with pseudocount of 1, and filter features present in <10% of samples."
- [methods] Any input or output feature that is present in less than 10% of samples was removed. Additionally, microbial and metabolite features were transformed to either relative abundance (RA) or centered log-ratio (CLR).: "Any input or output feature that is present in less than 10% of samples was removed"
- [readme] MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial and metabolite features.: "MiMeNet will perform a compositional transformation to relative abundance or centered log-ratio and filter low abundant microbial and metabolite features."
- [readme] Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation.: "Transform the microbial features into relative abundance (RA) or center log-ratio (CLR). If the data is already transformed, apply 'None' to skip transformation."
- [readme] python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv -micro_norm None -metab_norm CLR: "python MiMeNet_train.py -micro data/IBD/microbiome_PRISM.csv -metab data/IBD/metabolome_PRISM.csv -external_micro data/IBD/microbiome_external.csv -external_metab data/IBD/metabolome_external.csv"
