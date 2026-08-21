---
name: dynamic-branch-cutting-module-detection
description: Use when after constructing a hierarchical dendrogram from a biweight
  midcorrelation dissimilarity matrix of metabolite measurements, when your dendrogram
  exhibits complicated structure (multiple scales, varying branch heights) that would
  be poorly captured by a single fixed-height cutoff, and you.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - WGCNA
  - R
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder
  and Horvarth
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

# Dynamic Branch-Cutting Module Detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify metabolic co-expression modules from hierarchical dendrograms using adaptive branch-cutting thresholds rather than fixed height cutoffs, enabling robust detection of metabolite clusters even on complex dendrograms. This skill partitions normalized metabolite abundance data into functionally coherent modules annotated by pathway membership.

## When to use

Apply this skill after constructing a hierarchical dendrogram from a biweight midcorrelation dissimilarity matrix of metabolite measurements, when your dendrogram exhibits complicated structure (multiple scales, varying branch heights) that would be poorly captured by a single fixed-height cutoff, and you need to assign each metabolite to exactly one module for downstream trait association or pathway enrichment.

## When NOT to use

- Input dissimilarity matrix was not computed from biweight midcorrelation or lacks robustness to outliers.
- Module assignments are already available from prior analysis; re-clustering would discard existing biological interpretation.
- Dendrogram is simple and unimodal; a constant height cutoff would be faster and equally interpretable.

## Inputs

- hierarchical dendrogram object from hclust()
- biweight midcorrelation dissimilarity matrix (1 − adjacency)
- metabolite annotation table (rowData with SUB_PATHWAY field, optional)

## Outputs

- module color vector (one color per metabolite)
- module assignment table (metabolite ID → module name/color)
- module summary statistics (size, pathway composition)

## How to apply

Begin with a hierarchical clustering dendrogram computed from a dissimilarity matrix (1 − adjacency, where adjacency is derived from biweight midcorrelation with soft-thresholding power β=3). Apply the dynamic branch cutting algorithm (developed by Langfelder et al.) to automatically detect cluster boundaries at variable heights across the tree. Set a minimum module size threshold (e.g., 5 metabolites) to filter out small, potentially spurious clusters. Extract the module color vector and metabolite-to-module assignments from the output. Optionally, annotate each module by identifying its most abundant SUB_PATHWAY label from the rowData annotation. The dynamic method outperforms constant height cutoffs on dendrograms with heterogeneous branching structure, as it adapts the cutting threshold to local branch topology.

## Related tools

- **WGCNA** (Implements cutreeDynamic() function for dynamic branch cutting and module definition on hierarchical dendrograms.)
- **MetaboDiff** (Wraps WGCNA dynamic branch cutting workflow for metabolomics, handles MultiAssayExperiment object input and outputs named module assignments.) — https://github.com/andreasmock/MetaboDiff
- **R** (Runtime environment; required version ≥ 4.0.2 for MetaboDiff compatibility.)
- **MultiAssayExperiment** (Data container for normalized, imputed metabolite abundance assay and rowData annotation; input to module detection workflow.)

## Examples

```
# After loading norm_imputed MultiAssayExperiment and computing biweight midcorr. dissimilarity:
# library(WGCNA); dynamicTreeCut::cutreeDynamic(dendro=hc, distM=dissim_matrix, minClusterSize=5, method='hybrid')
```

## Evaluation signals

- Module size distribution respects minimum threshold (all modules ≥ 5 metabolites); no singleton or very small clusters remain.
- Module color assignments are consistent and unique: every metabolite belongs to exactly one module, and colors are visually distinct in dendrogram plots.
- Module pathway composition is coherent: most metabolites in a module share the same or related SUB_PATHWAY label, indicating biological relevance.
- Dendrogram visualization shows branch colors matching module assignments; cutting positions adapt locally to branch heights and cluster tightness, not locked to a single horizontal line.
- Module assignments are stable under small perturbations: recomputing with slightly altered soft-threshold power (β=2.5–3.5) yields similar module boundaries and pathway coherence.

## Limitations

- Dynamic branch cutting requires manual setting of minimum module size; no automatic data-driven choice for this threshold is provided in the article.
- Module quality depends critically on upstream correlation metric choice (biweight midcorrelation); if raw data contain systematic biases or unmodeled batch effects, dendrogram structure may be misleading.
- Pathway annotation (SUB_PATHWAY) is optional and tied to external databases (SMPDB, KEGG, HMDB, ChEBI); metabolites without annotation cannot contribute to module naming and require manual interpretation.
- The method assumes metabolites are the only clustering variables; it does not account for sample-level traits or phenotypes during module detection—trait association is performed post-hoc.

## Evidence

- [methods] dynamic branch cutting definition: "We employed the dynamic branch cut method developed by Langfelder and colleagues, as constant height cutoffs exhibit suboptimal performance on complicated dendrograms."
- [methods] module detection parameters: "modules are detected by applying a branch cutting method with a minimal module size of 5 metabolites"
- [methods] biweight midcorrelation rationale: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
- [methods] module naming by pathway: "For each module, identify the most abundant SUB_PATHWAY annotation and assign module names accordingly."
- [readme] key functionality in package: "MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
