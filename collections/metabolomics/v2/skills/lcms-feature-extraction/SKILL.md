---
name: lcms-feature-extraction
description: Use when when you have raw LC-MS chromatographic data (mzML or vendor format) and need to identify and characterize all detectable peaks across the full retention time range for untargeted metabolomics or discovery workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lcms-feature-extraction

## Summary

Nontargeted peak detection and segmentation of raw LC-MS data (mzML or vendor formats) to extract chromatographic features with precise m/z, retention time, intensity, and peak width metadata. This skill produces a feature table suitable for downstream metabolomics analysis.

## When to use

When you have raw LC-MS chromatographic data (mzML or vendor format) and need to identify and characterize all detectable peaks across the full retention time range for untargeted metabolomics or discovery workflows. Apply this skill as the first processing step before feature annotation or statistical analysis.

## When NOT to use

- Input data is already a processed feature table (peaks already detected and segmented)
- Analysis requires targeted detection of known compounds only (use targeted peak detection instead)

## Inputs

- Raw LC-MS data file (mzML format)
- Raw LC-MS data file (vendor format)

## Outputs

- Feature table (CSV format)
- Feature table (feather format)
- Peak metadata table (m/z, retention time, intensity, peak width, quality metrics)

## How to apply

Load raw LC-MS data into MassCube and apply its nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. The algorithm performs peak segmentation to define precise peak boundaries and extract peak characteristics including m/z value, retention time, intensity, and peak width. Export the resulting feature table in tabular format (CSV or feather) containing all detected peaks with their metadata and quality metrics. The skill is grounded in MassCube's highly accurate peak detection and segmentation capabilities designed specifically for LC-MS feature extraction workflows.

## Related tools

- **masscube** (Python package that performs nontargeted peak detection, segmentation, and feature extraction from LC-MS data) — https://github.com/huaxuyu/masscube/

## Evaluation signals

- Feature table schema validation: output contains required columns (m/z, retention time, intensity, peak width) with numeric types and no null values in core fields
- Peak boundary precision: segmented peaks have well-defined start/end retention times with positive peak widths
- Feature count reasonableness: number of detected peaks scales appropriately with raw data complexity and instrument sensitivity
- Quality metrics presence: comprehensive feature quality evaluation metadata is populated for each detected peak
- No data loss: all peaks detected across the full retention time range are represented in the export

## Limitations

- Algorithm accuracy depends on raw data quality and instrument resolution; low-abundance or poorly resolved peaks may be missed or incorrectly segmented
- No changelog documentation available for version tracking and method validation across MassCube releases

## Evidence

- [readme] Peak detection capability: "Highly accurate nontargeted peak detection and segmentation."
- [other] Workflow steps: "1. Load raw LC-MS data (mzML or vendor format) into MassCube. 2. Apply nontargeted peak detection algorithm to identify chromatographic peaks across the full retention time range. 3. Perform peak"
- [readme] Feature quality evaluation: "Comprehensive feature quality evaluation."
- [readme] Tool description: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
