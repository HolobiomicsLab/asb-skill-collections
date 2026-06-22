---
name: mass-spectrometry-imaging-data-loading
description: Use when you have raw or preprocessed MS imaging data archived as an RDS file or from a Zenodo deposit that includes the full m/z feature set (e.g., 10,200 m/z values spanning 150–1000 m/z range) and spectrum count (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SpaMTP
  - dplyr
  - R
  - Cardinal
  - Zenodo
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
  - build: coll_dimple_cq
    doi: 10.1101/2025.09.22.677919v1
    title: DIMPLE
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
---

# Mass Spectrometry Imaging Data Loading

## Summary

Load and initialize unprocessed MS imaging data (e.g., from Zenodo) into a Cardinal object, establishing the raw feature matrix, m/z axis, and spatial coordinates for downstream processing. This is the foundational step that materializes the high-dimensional m/z × spectrum matrix before normalization or peak refinement.

## When to use

You have raw or preprocessed MS imaging data archived as an RDS file or from a Zenodo deposit that includes the full m/z feature set (e.g., 10,200 m/z values spanning 150–1000 m/z range) and spectrum count (e.g., 4,959 spectra), and you need to load it into an R environment as a Cardinal object to begin the SpaMTP/Cardinal pipeline.

## When NOT to use

- Input is already a processed feature table (e.g., 687 cleaned peaks post-peakProcess) — use this skill only on unprocessed data.
- Data is in LC-MS format without spatial coordinates — this skill is specific to imaging data with (x, y) pixel information.
- Object is already instantiated in memory as a Cardinal or Seurat object — use this skill only for initial file I/O.

## Inputs

- Cardinal RDS file from Zenodo or local archive
- Unprocessed MS imaging data (imzML format or equivalent)
- URL or file path to raw imaging dataset

## Outputs

- Cardinal imaging object with m/z feature matrix
- Spatial coordinates (pixel grid) attached to object
- Raw m/z axis and spectrum intensities ready for downstream processing

## How to apply

Use Cardinal's data import functions (e.g., readRDS() with a Zenodo URL, or readImzML() for imzML files) to instantiate a Cardinal imaging object. Verify that the loaded object contains the expected number of m/z features and spectra (e.g., 10,200 m/z features, 4,959 spectra). The object should preserve the m/z axis (typically 150–1000 m/z range for metabolomics) and spatial coordinates (x, y pixel indices). This raw object is then passed downstream to summarizeFeatures(), TIC normalization, and peakProcess for peak refinement.

## Related tools

- **Cardinal** (Primary R package for MS imaging object instantiation and data structure; provides readRDS() and readImzML() import functions.) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **R** (Runtime environment for executing Cardinal loading commands and readRDS() file I/O.)
- **Zenodo** (Cloud repository hosting archived MS imaging datasets; Cardinal can load RDS files directly from Zenodo URLs.) — https://zenodo.org

## Examples

```
pig206 <- readRDS(url("https://zenodo.org/records/XXXXXX/files/pig206_unprocessed.RDS?download=1")); pig206
```

## Evaluation signals

- Verify object class is 'MSImageSet' or equivalent Cardinal imaging object.
- Confirm feature count matches expected m/z dimensionality (e.g., 10,200 features for pig206 dataset).
- Confirm spectrum count matches expected spatial replicates (e.g., 4,959 spectra for pig206).
- Inspect m/z axis range to confirm expected range (e.g., 150–1000 m/z for metabolomics).
- Verify spatial coordinates are present and non-degenerate (pixel grid intact).

## Limitations

- Loading may fail if Zenodo URL is expired or file format is corrupted; always verify URL accessibility before pipeline execution.
- Cardinal object structure assumes uniform m/z binning and rectangular pixel grid; non-standard imaging geometries may require custom preprocessing.
- Memory constraints apply for very large datasets (>50,000 spectra or >100,000 m/z features); consider subsampling or chunked loading for such cases.
- imzML files require auxiliary .ibd binary files to be co-located; loading will fail if .ibd is missing or inaccessible.

## Evidence

- [other] Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000).: "Load the unprocessed pig206 Cardinal object from Zenodo (10,200 m/z features, 4,959 spectra, m/z range 150–1000)"
- [readme] Build on the foundation of a Seurat Class Object, this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression and pathway analysis, and (3) integrative spatial-omics analysis.: "Build on the foundation of a Seurat Class Object, this package has three major functionalities which include; (1) mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical"
