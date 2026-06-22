---
name: mass-spectrometry-chromatogram-generation
description: Use when after MS2 annotation and sample alignment have been completed in JPA, when you need to visualize ion chromatograms for quality control, validate feature identities, or export chromatographic evidence for specific metabolic features across multiple samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - JPA
  - R
  - XCMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-chromatogram-generation

## Summary

Extract and export extracted ion chromatograms (EICs) from aligned LC-MS feature data, generating time-vs-intensity traces for specified features across samples. This skill bridges feature annotation (MS2) and export, producing validated chromatogram files with metabolite metadata for downstream visualization and validation.

## When to use

After MS2 annotation and sample alignment have been completed in JPA, when you need to visualize ion chromatograms for quality control, validate feature identities, or export chromatographic evidence for specific metabolic features across multiple samples.

## When NOT to use

- Input data is not yet aligned across samples (alignment must be completed first; see Part 5: Alignment)
- Raw mass spectrometry data files are unavailable or in unsupported vendor formats
- Feature table has not undergone MS2 annotation (EIC export is positioned after MS2 annotation in the workflow)

## Inputs

- aligned feature table (data.frame with columns: mz, rt, rtmin, rtmax, maxo, sample, level)
- raw LC-MS data files (mzXML, or vendor formats compatible with MS-Convert)
- feature metadata (m/z values, retention times, sample assignments)

## Outputs

- EIC chromatogram files (CSV, netCDF, or mzML format)
- EIC data object (time vs. intensity traces per feature)
- exported chromatogram data with metadata headers (feature ID, m/z, RT, sample ID)

## How to apply

Load the aligned feature table (peaklist or feature matrix) from JPA's prior alignment step into R. Parse feature metadata including m/z, retention time, intensity, and sample assignments. For each feature or user-specified subset, query the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window (typically 10 ppm or 0.01 m/z units based on instrument resolution). Generate EIC objects representing time-vs-intensity traces for each feature across selected samples. Export the EIC data to supported formats (CSV, netCDF, or mzML-compatible) with metadata headers containing feature identifiers, m/z, retention time, and sample identifiers. Validate output files for correct row/column structure, metadata field presence, and data integrity before release.

## Related tools

- **JPA** (R package hosting EIC export module as Part 8 of metabolomics workflow; loads aligned feature data and coordinates chromatogram extraction and export) — https://github.com/HuanLab/JPA.git
- **R** (Runtime environment for JPA; required version 4.0.0 or above for loading JPA data structures and executing EIC extraction logic)
- **XCMS** (Upstream peak picking and alignment; provides feature table structure and raw data querying capabilities used by EIC export) — https://rdrr.io/bioc/xcms/man/

## Evaluation signals

- Output EIC files conform to declared format (CSV headers, netCDF structure, or mzML compliance) with no malformed rows or missing metadata fields
- EIC data contains exactly one time-vs-intensity trace per (feature, sample) pair, with trace length > 1 point
- Feature identifiers, m/z values, and retention times in output match source feature table exactly (no rounding or truncation artifacts)
- Mass tolerance window applied during ion extraction is within stated range (e.g., ±10 ppm or ±0.01 m/z for the feature's m/z)
- Sample identifiers in exported chromatograms correspond to input sample assignments and selected sample subset

## Limitations

- EIC export requires successful prior alignment; features not aligned across samples cannot be exported
- Raw mass spectrometry data must be in vendor format compatible with MS-Convert (mzXML, mzML); proprietary binary formats may require conversion first
- Mass tolerance window is fixed per function call; fine-tuning requires re-running extraction with adjusted parameters
- EIC export is positioned strictly after MS2 annotation in the JPA workflow; attempting export before annotation step completes will miss MS2-derived metadata

## Evidence

- [other] JPA includes an EIC export capability as part of its comprehensive metabolomics data processing workflow, positioned after MS2 annotation in the processing pipeline.: "JPA includes an EIC export capability as part of its comprehensive metabolomics data processing workflow, positioned after MS2 annotation in the processing pipeline."
- [other] Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures.: "Load aligned feature data (peaklist or feature matrix from prior JPA alignment step) into the R environment using JPA data structures."
- [other] For each feature or user-specified subset, extract ion chromatograms by querying the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window.: "For each feature or user-specified subset, extract ion chromatograms by querying the raw or processed mass spectrometry data at the feature's m/z value within a defined mass tolerance window."
- [other] Generate EIC chromatogram objects (time vs. intensity traces) for each feature across selected samples.: "Generate EIC chromatogram objects (time vs. intensity traces) for each feature across selected samples."
- [other] Export EIC data to file format(s) supported by JPA (e.g., CSV, netCDF, or mzML-compatible formats) with metadata headers including feature identifiers, m/z, retention time, and sample identifiers.: "Export EIC data to file format(s) supported by JPA (e.g., CSV, netCDF, or mzML-compatible formats) with metadata headers including feature identifiers, m/z, retention time, and sample identifiers."
- [other] Validate output files for integrity, correct row/column structure, and presence of required metadata fields.: "Validate output files for integrity, correct row/column structure, and presence of required metadata fields."
- [readme] JPA' is written in R and its source code is publicly available at https://github.com/HuanLab/JPA.git: "'JPA' is written in R and its source code is publicly available at https://github.com/HuanLab/JPA.git"
- [readme] To install `JPA` package R version 4.0.0 or above is required: "To install `JPA` package R version 4.0.0 or above is required"
