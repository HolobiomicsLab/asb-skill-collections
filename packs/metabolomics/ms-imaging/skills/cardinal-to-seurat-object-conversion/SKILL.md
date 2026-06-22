---
name: cardinal-to-seurat-object-conversion
description: Use when after completing Cardinal-based preprocessing (feature summarization, TIC normalization, peak processing, spatial segmentation, and SSC annotation), use this conversion when you need to leverage Seurat's downstream statistical methods—such as differential metabolite expression testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_0092
  tools:
  - Cardinal
  - SpaMTP
  - Seurat
  - dplyr
  - R
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- library(Cardinal)
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(Seurat)
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

# cardinal-to-seurat-object-conversion

## Summary

Convert a processed Cardinal object (containing mass-spectrometry imaging data with spatial annotations and segmentation results) into a SpaMTP-compatible Seurat object to enable downstream statistical analysis, metabolite annotation, and integrative spatial-omics workflows. This bridging step unifies spatial metabolomics data with the mature Seurat ecosystem for differential expression, pathway analysis, and visualization.

## When to use

After completing Cardinal-based preprocessing (feature summarization, TIC normalization, peak processing, spatial segmentation, and SSC annotation), use this conversion when you need to leverage Seurat's downstream statistical methods—such as differential metabolite expression testing, pathway analysis, or integration with spatial transcriptomics—or when you plan to apply SpaMTP's metabolite annotation and visualization functions that operate on Seurat objects.

## When NOT to use

- Cardinal object has not yet been preprocessed with TIC normalization, peakProcess, and SSC segmentation—convert only after all Cardinal-native analyses are complete.
- Input data are already in Seurat format or from a different spatial-omics platform (e.g., Visium 10x) unrelated to Cardinal MS imaging workflows.
- You require advanced Cardinal-specific functions (e.g., spatial shrunken centroids refinement with custom weight matrices) that have no Seurat equivalent; stay in Cardinal for those operations.

## Inputs

- Cardinal object with processed spatial metabolomics data (post-peakProcess, post-SSC annotation)
- Spatial coordinates (x, y positions from spectra)
- SSC segmentation results (cluster assignments, e.g., k=8 clusters with sparsity parameters)
- Peak intensity matrix (e.g., 687 cleaned m/z features × 4,959 spectra)

## Outputs

- Seurat object compatible with SpaMTP
- Seurat assays containing intensity matrices and spatial metadata
- Seurat metadata slots populated with SSC cluster assignments and spatial coordinates
- Object ready for AnnotateSM(), CreatePathwayAssay(), and ImageDimPlot() operations

## How to apply

Use the CardinalToSeurat() function to convert the fully annotated Cardinal object (containing spatial coordinates, peak intensities, and SSC cluster assignments) into a Seurat object. The conversion preserves the spatial metadata (cluster labels, coordinates) and intensity matrices as assays in the resulting Seurat object. Verify that the Seurat object retains the expected number of features (e.g., 687 cleaned peaks) and spatial dimensions (e.g., 4,959 spectra), and confirm that cluster annotations from SSC (e.g., k=8 clusters with sparsity parameter s=32) are accessible via the Seurat metadata or dimensional reductions. This enables immediate use of SpaMTP functions like CreatePathwayAssay(), AnnotateSM(), and ImageDimPlot() on the converted object.

## Related tools

- **Cardinal** (Source data structure; provides spatial MS imaging object with preprocessed intensities, coordinates, and SSC cluster annotations to be converted) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **SpaMTP** (Target ecosystem; provides CardinalToSeurat() conversion function and downstream metabolite annotation, pathway analysis, and visualization functions that operate on the converted Seurat object) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (Target container class; the output Seurat object inherits Seurat's statistical, dimensional reduction, and visualization methods for spatial-omics analysis)
- **R** (Execution environment for the CardinalToSeurat() function call and downstream SpaMTP/Seurat operations)

## Examples

```
seurat_obj <- CardinalToSeurat(cardinal_obj)
```

## Evaluation signals

- Seurat object is successfully created and passes class validation (inherits 'Seurat' and 'SeuratObject').
- Peak count and spatial dimensions are preserved: Seurat object contains exactly 687 features (cleaned m/z values) and 4,959 cells (spectra); dimensions match pre-conversion Cardinal object.
- SSC cluster assignments (k=8 clusters with sparsity s=32) are accessible via Seurat metadata (e.g., [redacted-email]$clusters or seurat_obj[[]]$clusters) and match the Cardinal source exactly.
- Intensity assay is correctly populated and normalized; mean intensity across all spectra and features is non-zero and consistent with pre-conversion TIC-normalized Cardinal intensities.
- Downstream SpaMTP functions (CreatePathwayAssay, AnnotateSM, ImageDimPlot) execute without error on the converted object and produce expected outputs (e.g., pathway annotations, m/z-matched metabolites, spatial plots).

## Limitations

- The conversion is one-directional; changes made in Seurat downstream analyses cannot be back-propagated to the original Cardinal object.
- Conversion may lose highly specialized Cardinal metadata or custom spatial weights from SSC if those fields are not explicitly mapped to Seurat's metadata or assay slots; verify that all necessary SSC parameters (radius=2, k=8, s=32) are preserved in the Seurat object.
- Seurat's default assay structure and slot organization differ from Cardinal's; users accustomed to Cardinal's direct accessor functions may need to adapt to Seurat's $ and [[ ] ] syntax.
- The article's provided workflow does not detail error handling or validation steps for the CardinalToSeurat() function; edge cases (e.g., malformed Cardinal objects, missing cluster assignments) are not addressed.

## Evidence

- [methods] 6. Convert the processed Cardinal object to a SpaMTP Seurat object using CardinalToSeurat().: "Convert the processed Cardinal object to a SpaMTP Seurat object using CardinalToSeurat()."
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis. Build on the foundation of a Seurat Class Object, this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression and pathway analysis, and (3) integrative spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis. Build on the foundation of a"
- [methods] 5. Annotate SSC results back to the Cardinal object using add_ssc_annotation(r=2,k=8,s=32).: "Annotate SSC results back to the Cardinal object using add_ssc_annotation(r=2,k=8,s=32)."
- [methods] 4. Run spatial shrunken centroids (SSC) segmentation with adaptive weights, radius=2, k=8 clusters, and sparsity parameters s=2,4,8,16,32,64.: "Run spatial shrunken centroids (SSC) segmentation with adaptive weights, radius=2, k=8 clusters, and sparsity parameters s=2,4,8,16,32,64."
