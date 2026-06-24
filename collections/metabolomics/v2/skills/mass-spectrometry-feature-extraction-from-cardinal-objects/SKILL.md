---
name: mass-spectrometry-feature-extraction-from-cardinal-objects
description: Use when you have a Cardinal MSImagingExperiment object (e.g., from imzML
  or Analyze 7.5 files) and need to retrieve the complete set of m/z values and their
  intensities for annotation against metabolite databases (HMDB, Lipidmaps) or for
  statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0091
  tools:
  - SpaMTP
  - Cardinal
  - R
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- library(Cardinal)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-extraction-from-cardinal-objects

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract all m/z features and their metadata from a Cardinal MSImagingExperiment object to produce a feature table suitable for downstream annotation and analysis. This skill converts raw imaging MS data into a standardized feature matrix compatible with metabolite database matching.

## When to use

You have a Cardinal MSImagingExperiment object (e.g., from imzML or Analyze 7.5 files) and need to retrieve the complete set of m/z values and their intensities for annotation against metabolite databases (HMDB, Lipidmaps) or for statistical analysis. Typical trigger: you want to know how many features are available for annotation (e.g., 'How many of my 767,528 detected m/z values can be annotated with ppm_error=3?').

## When NOT to use

- Input is already a pre-processed feature table (e.g., CSV or data.frame of annotated m/z values) — use directly for downstream analysis instead.
- You only need to work with a single targeted m/z value — use FindNearestMZ() or SearchAnnotations() directly instead.
- Data are from untargeted LC-MS in flow (not imaging) — use mzML import and xcms or other LC-MS feature detection pipelines instead of Cardinal.

## Inputs

- Cardinal MSImagingExperiment object
- imzML or Analyze 7.5 imaging MS file (loaded into Cardinal)

## Outputs

- featureData data.frame (rows = m/z features, columns = mz, and optional metadata)
- integer: total count of detected m/z features
- intensity matrix (pixels × features)

## How to apply

Use the featureData() accessor function on the Cardinal MSImagingExperiment object to extract the feature annotation table, which contains m/z values and other metadata. The number of rows in this table represents the total number of MS features detected across all pixels. This extraction is mandatory before calling downstream annotation functions like AnnotateSM() or AnnotateBigData(), as those functions require the m/z vector and intensity matrix as inputs. Verify that the extracted table includes columns for observed m/z, and optionally retention time if LC-MS data. The total feature count serves as the denominator for calculating annotation success rates after matching against reference databases.

## Related tools

- **Cardinal** (MS imaging data container and accessor; provides MSImagingExperiment class and featureData() extraction method) — https://github.com/Vitek-Lab/Cardinal3-vignettes
- **SpaMTP** (High-level wrapper and extension of Cardinal for integrated spatial-omics analysis; inherits featureData() extraction and passes features to AnnotateSM() for annotation) — https://github.com/GenomicsMachineLearning/SpaMTP

## Examples

```
featureData(cardinal_obj) # Extract feature metadata; nrow() returns total m/z feature count; pass mz column to AnnotateSM(cardinal_obj, db = HMDB_db, ppm_error = 3)
```

## Evaluation signals

- featureData() returns a non-empty data.frame with nrow equal to the total feature count (e.g., 767,528 rows for the example dataset).
- The extracted m/z column contains numeric values in the expected range (typically 50–2000 m/z for metabolomics) with no missing values.
- Row count of featureData() matches the ncol() of the intensity matrix (pixels × features alignment check).
- Downstream annotation functions (AnnotateSM, AnnotateBigData) successfully accept the extracted m/z vector without dimension or type errors.
- Annotation success rate (annotated features / total features) is >0 and plausible for the chosen database and ppm_error threshold (e.g., 67,060 / 767,528 ≈ 8.7% for HMDB with ppm=3).

## Limitations

- featureData() extraction does not perform m/z recalibration or deisotoping; isotope and adduct variants are treated as separate features, inflating the total count.
- The method is memory-intensive for very large imaging datasets (>10 GB); consider subsetting pixels or m/z ranges before full extraction if working on resource-constrained systems.
- No direct quality control filtering (e.g., by signal-to-noise ratio or pixel prevalence) is applied during extraction; further filtering should follow before annotation to reduce noise.
- Missing or malformed featureData metadata (e.g., if the imaging file lacks proper m/z calibration) will propagate into annotations and yield spurious matches.

## Evidence

- [methods] Extract all m/z values from the Cardinal MSImagingExperiment object (767,528 features) using featureData().: "Extract all m/z values from the Cardinal MSImagingExperiment object (767,528 features) using featureData()"
- [methods] Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'. Return the annotated results data.frame and verify the row count equals the reported 67,060 annotated m/z values.: "Call AnnotateBigData with parameters: db=HMDB_db, ppm_error=3, adducts=c('M-H','M+Cl'), polarity='negative'. Return the annotated results data.frame and verify the row count equals the reported"
- [readme] SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis.: "SpaMTP inherits functionalities from two well established R packages (Cardinal and Seurat) to present a user-friendly platform for integrative spatial-omics analysis."
- [readme] mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression and pathway analysis: "mass-to-charge ratio (m/z) metabolite annotation, (2) various downstream statistical analysis including differential metabolite expression"
