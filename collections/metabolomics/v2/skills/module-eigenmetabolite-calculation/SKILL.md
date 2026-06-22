---
name: module-eigenmetabolite-calculation
description: Use when after metabolic correlation modules have been identified via hierarchical clustering with dynamic branch cutting on a biweight midcorrelation matrix. Apply this skill when you need a single representative abundance profile per module to correlate against sample traits (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2885
  tools:
  - MetaboDiff
  - WGCNA
  - R
  - R (stats::prcomp or similar)
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder and Horvarth
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# module-eigenmetabolite-calculation

## Summary

Calculate eigenmetabolites (first principal components) as representative profiles for metabolic co-expression modules identified by hierarchical clustering and dynamic tree cutting. This condenses high-dimensional module abundance patterns into single composite metabolite vectors suitable for downstream correlation analysis with sample phenotypes.

## When to use

After metabolic correlation modules have been identified via hierarchical clustering with dynamic branch cutting on a biweight midcorrelation matrix. Apply this skill when you need a single representative abundance profile per module to correlate against sample traits (e.g., tumor vs. normal, genetic background) without losing module-level structure.

## When NOT to use

- Module structure is weak or membership is ambiguous (e.g., many singletons or poorly defined branches from dynamic tree cutting)—consider re-tuning clustering parameters or soft-thresholding power β before computing eigenmetabolites.
- Sample count is very small (n < 5) relative to metabolite count within a module—eigenmetabolite PCA estimates become unstable; use raw module mean abundance instead.
- Metabolites within a module lack biological coherence (e.g., no shared SUB_PATHWAY annotation)—eigenmetabolite may not represent a true co-regulatory program.

## Inputs

- Metabolic module assignments (color/ID vector mapping metabolites to modules)
- Normalized metabolite abundance matrix (samples × metabolites) from MultiAssayExperiment assay
- Module membership metadata

## Outputs

- Eigenmetabolite matrix (samples × modules, one composite profile per module)
- Module eigenvector loadings (contribution weights of each metabolite to its module's eigenmetabolite)
- Module connectivity statistics (kME values correlating each metabolite to its eigenmetabolite)

## How to apply

For each identified metabolic module, compute the first principal component (eigenmetabolite) across all member metabolites using their normalized abundance values from the MultiAssayExperiment object. The eigenmetabolite serves as a composite summary of co-regulated metabolite behavior within the module. Extract the module eigenvector scores for each sample and use these as continuous variables in subsequent trait correlation analyses (e.g., Pearson correlation with phenotype or clinical outcome). The eigenmetabolite inherits the module's biological coherence—modules with high module connectivity (kME values) and strong pathway annotation demonstrate robust signal. Validate by confirming that metabolites within the module show high correlation with the calculated eigenmetabolite; low correlations suggest either weak module structure or a need to revisit clustering parameters.

## Related tools

- **WGCNA** (Provides moduleEigengenes() function and related module correlation utilities for computing and analyzing eigenmetabolites) — https://labs.genetics.ucla.edu/horvath/CoexpressionNetwork/Rpackages/WGCNA/
- **MetaboDiff** (Wraps WGCNA functionality and manages metabolic module assignments within MultiAssayExperiment framework; calculates eigenvector profiles for modules) — https://github.com/andreasmock/MetaboDiff
- **R (stats::prcomp or similar)** (Underlying principal component analysis engine for computing first eigenvector of module metabolite abundance matrix)

## Examples

```
library(WGCNA); module_eigengenes <- moduleEigengenes(expr = normalized_metabolite_matrix, colors = module_color_vector)$eigengenes
```

## Evaluation signals

- Eigenmetabolite eigenvector loadings show high correlation (|r| > 0.6) with constituent metabolites' normalized abundances, confirming the principal component captures module structure.
- Module connectivity (kME) values—percentage of metabolites within each module with kME > 0.7 (i.e., high correlation to their eigenmetabolite)—are documented; modules with <50% high-kME metabolites indicate weak coherence.
- Eigenmetabolite variance explained matches or exceeds the variance of raw module mean abundance, demonstrating that PCA weighting adds no artificial inflation.
- Eigenmetabolites show differential abundance (p-value from t-test or ANOVA) or phenotypic correlation (r, p-value) consistent with module SUB_PATHWAY annotation and prior biological knowledge.
- Dendrogram branch heights and module color assignments are reproducible across re-runs with identical clustering parameters, ensuring eigenmetabolite stability.

## Limitations

- Eigenmetabolite interpretation depends critically on module quality; poorly separated or mis-assigned metabolites corrupt the first principal component and weaken downstream phenotype associations.
- Soft thresholding power β=3 (used in the source study) may not generalize to all metabolite datasets; over- or under-thresholding alters module membership and thus eigenmetabolite values. Sensitivity analysis on β is recommended.
- Eigenmetabolites are linear combinations; non-linear metabolic interactions or condition-specific co-regulation are not captured. Consider supplementing with per-module correlation heatmaps or pathway enrichment analysis.
- When module size is very small (n=5 metabolites, the minimum threshold in the study), eigenmetabolite estimates have high variance; bootstrapping or cross-validation is advisable for confidence intervals.
- Eigenmetabolites are sample-specific but not inherently comparable across studies unless metabolite measurement platforms, normalization schemes, and clinical phenotypes are harmonized.

## Evidence

- [methods] Apply hierarchical clustering with dynamic branch cutting to identify metabolic co-expression modules: "Perform hierarchical clustering on the dissimilarity matrix to construct the dendrogram. 5. Apply dynamic branch cutting with minimum module size of 5 metabolites to identify clusters."
- [methods] Biweight midcorrelation is the similarity measure used to build the dissimilarity matrix: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
- [methods] Module assignments are extracted from the dendrogram as a color vector: "Extract the module color vector and module assignment from the dendrogram. 7. For each module, identify the most abundant SUB_PATHWAY annotation and assign module names accordingly."
- [intro] MetaboDiff provides exploration of sample traits in metabolic correlation networks: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
- [methods] Normalized and imputed MultiAssayExperiment object is the standard input container: "Load the normalized and imputed MultiAssayExperiment object (norm_imputed assay). 2. Compute biweight midcorrelation similarity matrix across all metabolites."
