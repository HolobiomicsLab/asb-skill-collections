---
name: metabolomic-data-structure-formatting
description: Use when after peak detection in MZmine2 has produced an MGF file (containing
  MS1 and MS2 spectra) and a feature abundance table (CSV or BIOM), but before running
  q2-qemistree tree construction or any QIIME 2-based metabolomic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - q2-qemistree
  - MZmine2
  - QIIME 2
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed
  comparison of untargeted metabolomic profiles.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_qemistree_cq
    doi: 10.1038/s41589-020-00677-3
    title: qemistree
  dedup_kept_from: coll_qemistree_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41589-020-00677-3
  all_source_dois:
  - 10.1038/s41589-020-00677-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-data-structure-formatting

## Summary

Convert raw mass-spectrometry metabolomic data into standardized QIIME 2 artifact formats (FeatureTable[Frequency] and MassSpectrometryFeatures) to enable downstream chemical tree construction and phylogenetic diversity analysis. This skill bridges peak-detection pipelines (MZmine2) and chemically-informed feature comparison.

## When to use

Apply this skill after peak detection in MZmine2 has produced an MGF file (containing MS1 and MS2 spectra) and a feature abundance table (CSV or BIOM), but before running q2-qemistree tree construction or any QIIME 2-based metabolomic analysis. Use it when you have LC-MS/MS untargeted metabolomic profiles that need to be harmonized into a standard artifact format for reproducible, tool-agnostic downstream processing.

## When NOT to use

- Data is already in QIIME 2 artifact format (.qza files) — skip import and proceed directly to tree construction.
- MGF file lacks MS2 spectra or has unmatched MS1 entries — troubleshoot peak detection in MZmine2 first.
- Feature table contains pre-aggregated or taxonomically classified rows — formatting assumes unaggregated MS1 features only.

## Inputs

- MGF file with MS1 and MS2 spectra (from MZmine2 peak detection)
- Feature abundance table in CSV or BIOM format (peak areas per sample, from MZmine2)

## Outputs

- QIIME 2 artifact of type MassSpectrometryFeatures (.qza)
- QIIME 2 artifact of type FeatureTable[Frequency] (.qza)

## How to apply

First, export the peak-detection results from MZmine2 as two files: (1) an MGF file containing both MS1 and MS2 spectral information, and (2) a feature abundance table in CSV or BIOM format. Validate the MGF file for completeness—ensure every MS1 entry has a corresponding MS2 entry and that no formatting errors are present. Then, import both files into QIIME 2 artifact format using `qiime tools import`, specifying the MGF as type `MassSpectrometryFeatures` and the abundance table as type `FeatureTable[Frequency]`. QIIME 2 will validate schema compliance and report errors if MS1/MS2 pairing is incomplete or if the feature table has malformed entries, halting the import if needed. This produces standardized, versioned artifacts suitable for meta-analyses and reproducible comparative metabolomic workflows.

## Related tools

- **MZmine2** (Upstream peak detection and MS feature extraction; produces MGF and feature abundance tables consumed by this formatting skill) — http://mzmine.github.io
- **QIIME 2** (Artifact framework and validation engine; `qiime tools import` performs the format conversion and schema validation) — https://docs.qiime2.org

## Examples

```
qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency] && qiime tools import --input-path sirius.mgf --output-path sirius.mgf.qza --type MassSpectrometryFeatures
```

## Evaluation signals

- QIIME 2 import command completes without schema validation errors and produces .qza artifacts with correct type annotations.
- MGF file validation passes: all MS1 entries have corresponding MS2 entries (error message reports unmatched pairs if present).
- Feature table dimensions match between input CSV/BIOM and output artifact (sample count, feature count, abundance range preserved).
- Artifact can be successfully read and queried using `qiime qemistree` subcommands in downstream tree-building steps.
- Metadata (m/z, retention time, spectral similarity) embedded in MGF headers survive import and are accessible in artifact.
- No features are silently dropped or renamed during import (output feature count equals input feature count).

## Limitations

- MGF formatting errors (missing MS1/MS2 pairings, malformed headers) will halt import with an error message; troubleshooting must occur upstream in MZmine2.
- QIIME 2 import does not validate chemical plausibility of m/z or retention time values; garbage-in garbage-out holds.
- Feature table must have samples as columns and features (MS1 m/z × RT combinations) as rows; transpose-then-import if reversed.
- Only ~70–90% of MS1 features typically receive downstream fingerprint predictions in q2-qemistree due to MS2 spectral quality and user-defined tolerances (e.g., ppm-max, zodiac-threshold); features without fingerprints are filtered out post-hierarchy construction.
- SIRIUS version compatibility: q2-qemistree was initially developed for SIRIUS 4.0.1 and has been adapted for versions ≥4.4.29; older or newer versions may fail.

## Evidence

- [readme] To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1. An MGF file with both MS1 and MS2 information.: "To generate a tree that relates the MS1 features in your experiment, we need to pre-process mass-spectrometry data (.mzXML, .mzML or .mzDATA files) using MZmine2 and produce the following inputs: 1."
- [readme] If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot this step before proceeding forward.: "If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot"
- [readme] We import these files into the appropriate QIIME 2 artifact formats as follows: qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency]: "We import these files into the appropriate QIIME 2 artifact formats as follows: qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency]"
- [other] Load the feature table (abundance matrix) and feature metadata (m/z, retention time, and/or spectral similarity annotations) into QIIME 2 artifact format.: "Load the feature table (abundance matrix) and feature metadata (m/z, retention time, and/or spectral similarity annotations) into QIIME 2 artifact format."
- [readme] MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1 features) in an experiment: "MS1 features without fingerprints are filtered out of this feature table. This is done because SIRIUS predicts molecular substructures for a subset of features (typically for 70-90% of all MS1"
