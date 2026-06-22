---
name: spatial-segmentation-shrunken-centroids
description: Use when apply SSC when you have preprocessed and normalized MS imaging data (e.g., after TIC normalization and peak processing) and need to discover spatially distinct metabolite regions without prior tissue annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3379
  tools:
  - SpaMTP
  - dplyr
  - R
  - Cardinal
  - Seurat
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(dplyr)
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spatial Shrunken Centroids (SSC) Segmentation

## Summary

Spatial shrunken centroids (SSC) is an unsupervised clustering method for mass spectrometry imaging that identifies spatially coherent metabolite regions by combining feature selection with adaptive spatial weighting. It produces k tissue-specific clusters with tunable sparsity to control feature selection stringency.

## When to use

Apply SSC when you have preprocessed and normalized MS imaging data (e.g., after TIC normalization and peak processing) and need to discover spatially distinct metabolite regions without prior tissue annotation. SSC is appropriate when you want to balance feature selection (via sparsity parameters) with spatial coherence (via adaptive radius weighting) to avoid over-segmentation or loss of localized signals.

## When NOT to use

- Input is already a tissue-labeled or manually annotated region map — use supervised classification instead.
- Data has not been normalized (TIC) or peak-filtered — SSC requires preprocessed intensities to avoid artifacts.
- Spatial coordinates are missing or unreliable — SSC depends on pixel adjacency; non-spatial clustering may be more appropriate.
- You need to preserve all original features equally — SSC sparsity parameters will remove low-weight features, reducing dimensionality by design.

## Inputs

- Normalized and peak-processed Cardinal object (mzImage or imagingExperiment)
- Preprocessed feature matrix with TIC normalization and peak filtering applied
- Spatial coordinates (x, y pixel positions for each spectrum)

## Outputs

- SSC cluster assignments (vector of cluster membership per spectrum/pixel)
- Spatial segmentation map (image showing cluster regions)
- Feature importance scores per cluster (from sparsity-penalized centroids)
- Annotated Cardinal object with SSC results attached
- Converted Seurat object with SSC assay and metadata for downstream analysis

## How to apply

After loading a normalized and peak-processed Cardinal object, run spatial shrunken centroids segmentation with adaptive weights, specifying a spatial radius (e.g., radius=2 pixels), the target number of clusters (e.g., k=8), and a sequence of sparsity parameters (e.g., s=2,4,8,16,32,64) to explore feature selection trade-offs. The adaptive weights incorporate spatial neighborhood information within the specified radius. Select the optimal sparsity parameter by examining cluster stability and interpretability (e.g., s=32 for moderate feature selection). Annotate the resulting SSC clusters back to the Cardinal object using the annotation function with the chosen radius, k, and sparsity, then convert to a Seurat object for downstream statistical and pathway analysis.

## Related tools

- **Cardinal** (Provides the imagingExperiment data structure, feature normalization (TIC), peak processing, and the SSC segmentation function with adaptive spatial weighting) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **SpaMTP** (Wraps Cardinal segmentation results and provides downstream functions for differential metabolite expression, pathway analysis, and visualization on annotated SSC clusters) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Post-segmentation platform for statistical testing (differential expression), clustering visualization, and integrative multi-omics analysis of SSC-annotated metabolite data)

## Examples

```
# After loading and normalizing Cardinal object:
ssc_result <- spatialShrunkenCentroids(pig206_cardinal, r=2, k=8, s=32, weights='adaptive')
annotated_cardinal <- add_ssc_annotation(pig206_cardinal, r=2, k=8, s=32, result=ssc_result)
seurat_obj <- CardinalToSeurat(annotated_cardinal)
```

## Evaluation signals

- Cluster counts match the specified k parameter and cluster assignments span all k values (no empty clusters after filtering).
- Spatial segmentation map shows contiguous or near-contiguous regions; large salt-and-pepper noise suggests radius or k may be misspecified.
- Feature importance (sparsity) gradually increases from s=2 to s=64; monotonic trends confirm sparsity parameter sweep is working.
- Clusters correlate with known tissue boundaries or metabolite gradients (validated by co-localization with reference metabolites or histology if available).
- Differential metabolite expression within top-ranked clusters (after SSC annotation) shows expected fold-changes (e.g., > 1.5–2× for biologically relevant metabolites).

## Limitations

- SSC requires pre-specification of k clusters; no automatic k-selection algorithm is described. Over- or under-specification leads to fragmented or merged regions.
- Sparsity parameters (s) must be manually tuned; no principled criterion for optimal s is provided beyond visual inspection or downstream validation.
- Performance on very large datasets (>10,000 spectra) or high-resolution imaging is not characterized; computational cost may scale with spatial radius and k.
- SSC assumes Euclidean spatial neighborhoods; irregular tissue shapes or large holes may violate the adaptive weighting model.
- The method is sensitive to preprocessing quality; incomplete normalization or peak detection errors propagate into segmentation artifacts.

## Evidence

- [other] Run spatial shrunken centroids (SSC) segmentation with adaptive weights, radius=2, k=8 clusters, and sparsity parameters s=2,4,8,16,32,64.: "Run spatial shrunken centroids (SSC) segmentation with adaptive weights, radius=2, k=8 clusters, and sparsity parameters s=2,4,8,16,32,64."
- [other] Annotate SSC results back to the Cardinal object using add_ssc_annotation(r=2,k=8,s=32).: "Annotate SSC results back to the Cardinal object using add_ssc_annotation(r=2,k=8,s=32)."
- [other] Convert the processed Cardinal object to a SpaMTP Seurat object using CardinalToSeurat().: "Convert the processed Cardinal object to a SpaMTP Seurat object using CardinalToSeurat()."
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis."
- [other] Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks.: "Apply TIC normalization followed by peakProcess with SNR threshold=3, sampleSize=0.1, tolerance=0.5 mz to generate 687 cleaned peaks."
