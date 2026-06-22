---
name: phenotype-pathway-association-ranking
description: Use when after computing a pathway dysregulation score matrix (PDSmatrix) from metabolite-pathway associations, apply this skill when you need to reduce the pathway feature space to those most predictive or explanatory of a phenotype label.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Lilikoi v2.0
  - R
derived_from:
- doi: 10.1093/gigascience/giaa162
  title: Lilikoi V2.0
evidence_spans:
- The new Lilikoi v2.0 R package has implemented a deep-learning method for classification, in addition to popular machine learning methods.
- Lilikoi v2.0 is a modern, comprehensive package to enable metabolomics analysis in R programming environment.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lilikoi_v2_0_cq
    doi: 10.1093/gigascience/giaa162
    title: Lilikoi V2.0
  dedup_kept_from: coll_lilikoi_v2_0_cq
schema_version: 0.2.0
---

# phenotype-pathway-association-ranking

## Summary

Rank and filter metabolic pathways by their information-gain relevance to a phenotype using the Lilikoi featuresSelection function. This skill identifies which pathways in a pathway dysregulation score (PDS) matrix are most significantly associated with the phenotype of interest, enabling downstream machine learning and prognosis modeling on the most informative features.

## When to use

After computing a pathway dysregulation score matrix (PDSmatrix) from metabolite-pathway associations, apply this skill when you need to reduce the pathway feature space to those most predictive or explanatory of a phenotype label. Use it as a prerequisite to machine learning classification or prognosis prediction to avoid overfitting and improve interpretability of pathway-phenotype relationships.

## When NOT to use

- Input is already a pre-filtered pathway feature set; re-filtering may remove biologically validated associations.
- Phenotype is continuous (regression target) rather than categorical; information-gain is designed for classification contexts.
- PDSmatrix is sparse or contains many zero/missing values; feature selection may become unstable.

## Inputs

- PDSmatrix: pathway-by-sample matrix of dysregulation scores (numeric matrix or data frame)
- Phenotype labels: vector of class assignments or phenotype values aligned to matrix columns

## Outputs

- selected_Pathways_Weka: filtered and ranked list of pathways with information-gain scores exceeding threshold

## How to apply

Load the PDSmatrix (pathway-by-sample feature matrix) and phenotype labels into R. Apply lilikoi.featuresSelection() with the information-gain method and a threshold of 0.50 to rank pathways by their mutual information with the phenotype. Pathways exceeding the threshold are retained in the selected_Pathways_Weka output; those below are filtered out. The threshold of 0.50 balances feature selectivity with retention of biologically meaningful pathways. Information-gain scoring reflects how much knowledge each pathway's values reduce uncertainty about the phenotype class, making it suitable for categorical phenotypes. Export the ranked selected pathways and their scores for use in downstream regression, machine learning, or visualization workflows.

## Related tools

- **Lilikoi v2.0** (R package hosting lilikoi.featuresSelection() function for information-gain feature ranking) — https://github.com/lanagarmire/lilikoi2
- **R** (Programming environment for loading data, executing featuresSelection, and exporting results)

## Examples

```
selected_Pathways_Weka <- lilikoi.featuresSelection(PDSmatrix, threshold = 0.50, method = "gain")
```

## Evaluation signals

- Output file selected_Pathways_Weka is non-empty and contains only pathways with information-gain scores ≥ 0.50.
- All selected pathways are present in the input PDSmatrix (no spurious or out-of-bounds identifiers).
- Information-gain scores are ranked in descending order; top pathways show strongest phenotype association.
- Number of selected pathways is substantially reduced from input (e.g., >50% filtering), indicating effective dimensionality reduction.
- Selected pathways are biologically plausible for the phenotype (cross-check with literature or pathway databases like KEGG).

## Limitations

- Information-gain method is sensitive to class imbalance; phenotypes with skewed label distributions may yield biased rankings.
- Threshold of 0.50 is empirically chosen and may require tuning for different datasets or phenotypes.
- Method captures univariate pathway–phenotype associations; does not identify higher-order or synergistic pathway interactions.
- Pathway definitions depend on upstream metabolite-to-pathway mapping accuracy; errors in annotation propagate to feature selection.

## Evidence

- [other] featuresSelection function and information-gain threshold: "lilikoi.featuresSelection(PDSmatrix,threshold= 0.50,method="gain")"
- [other] Input PDSmatrix and phenotype context: "Apply the information-gain method for feature selection with threshold 0.50 in Lilikoi v2.0 to rank and filter pathways by their relevance to the phenotype."
- [readme] Downstream use in machine learning: "Select the most signficant pathway related to phenotype. ... Machine learning"
- [other] Output naming and purpose: "producing selected_Pathways_Weka as output"
- [readme] Data transformation prerequisite: "Transform metabolites into pathway using pathtracer algorithm PDSmatrix=lilikoi.PDSfun(Metabolite_pathway_table)"
