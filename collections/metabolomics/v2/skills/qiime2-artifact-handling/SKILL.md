---
name: qiime2-artifact-handling
description: Use when you have raw mass-spectrometry files (MGF, BIOM, mzXML, mzML) or feature abundance tables from external tools (MZmine2, peak detection software) and need to convert them into QIIME 2's typed artifact format before running downstream plugins like q2-qemistree, diversity analyses, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - q2-qemistree
  - QIIME 2
  - MZmine2
derived_from:
- doi: 10.1038/s41589-020-00677-3
  title: qemistree
evidence_spans:
- A tool to build a tree of mass-spectrometry (LC-MS/MS) features to perform chemically-informed comparison of untargeted metabolomic profiles.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QIIME 2 Artifact Handling

## Summary

Import, format, and manage mass-spectrometry and feature table data into QIIME 2 artifact types (.qza) to enable standardized downstream analysis. This skill ensures data interoperability across QIIME 2 plugins and preserves metadata throughout metabolomic or metagenomic pipelines.

## When to use

You have raw mass-spectrometry files (MGF, BIOM, mzXML, mzML) or feature abundance tables from external tools (MZmine2, peak detection software) and need to convert them into QIIME 2's typed artifact format before running downstream plugins like q2-qemistree, diversity analyses, or comparative workflows. Use this when multiple datasets must be harmonized under a single metadata schema.

## When NOT to use

- Data is already in QIIME 2 artifact (.qza) format — proceed directly to analysis steps.
- MGF file contains only MS1 or lacks matching MS2 entries — artifact import will fail; repair the source file first.
- Feature table is unstructured or contains missing values without imputation — standardize and validate before import.

## Inputs

- BIOM file (feature abundance table)
- MGF file (mass-spectrometry features with MS1/MS2 spectra)
- TSV file (MS2 spectral library matches or chemical taxonomy)
- CSV file (feature metadata)

## Outputs

- QIIME 2 artifact (.qza) of type FeatureTable[Frequency]
- QIIME 2 artifact (.qza) of type MassSpectrometryFeatures
- QIIME 2 artifact (.qza) of type FeatureData[Molecules]

## How to apply

Use `qiime tools import` with explicit `--type` specification matching the data content: `FeatureTable[Frequency]` for BIOM feature abundance matrices, `MassSpectrometryFeatures` for MGF files containing MS1/MS2 spectra, or `FeatureData[Molecules]` for chemical structure annotations. Validate that MGF files contain both MS1 and MS2 entries with one-to-one correspondence before import; the tool will reject malformed files with specific error messages. Once imported as .qza artifacts, these become typed inputs to downstream QIIME 2 methods, ensuring schema validation and enabling deterministic outputs. For meta-analyses, import multiple datasets in the same order (e.g., CSI results, feature tables, MS2 matches) to maintain correspondence through multi-input commands.

## Related tools

- **QIIME 2** (Framework providing the `tools import` command and artifact type system for data standardization.) — https://docs.qiime2.org/
- **MZmine2** (Peak detection and feature extraction tool that produces MGF and BIOM inputs for QIIME 2 import.) — http://mzmine.github.io
- **q2-qemistree** (Downstream QIIME 2 plugin that consumes imported MassSpectrometryFeatures and FeatureTable[Frequency] artifacts.) — https://github.com/biocore/q2-qemistree

## Examples

```
qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency]
qiime tools import --input-path sirius.mgf --output-path sirius.mgf.qza --type MassSpectrometryFeatures
```

## Evaluation signals

- Artifact import succeeds without validation errors and .qza file is created with correct type annotation.
- Downstream QIIME 2 commands (e.g., `qiime qemistree compute-fragmentation-trees`) accept the imported artifact without type mismatch errors.
- Feature table dimensions (rows = features, columns = samples) and feature count are preserved from source; no silent data loss.
- For MGF import: verify MS1/MS2 correspondence by confirming artifact creation succeeds and diagnostic error messages appear if malformed.
- Meta-analysis inputs maintain row/column order and count consistency across paired CSI results, feature tables, and MS2 match tables when passed to `make-hierarchy`.

## Limitations

- QIIME 2 artifact import is strict about type specification and will reject mismatches or malformed files; the source file must be pre-validated for structure and completeness.
- MGF files lacking MS1 entries or with unmatched MS2 entries will cause import to fail; MZmine2 batch configuration must ensure both ion levels are output.
- Feature identifiers must be unique within a single dataset; overlapping row IDs from multiple datasets will cause collisions unless the import step or downstream merging renames them.
- Import does not impute missing values, normalize, or filter features; these preprocessing steps must occur either before import or via dedicated QIIME 2 plugins post-import.

## Evidence

- [readme] These input files can be obtained following peak detection in MZmine2. [Here](https://raw.githubusercontent.com/biocore/q2-qemistree/master/q2_qemistree/demo/batchQE-MZmine-2.33.xml) is an example MZmine2 batch file used to generate these.: "These input files can be obtained following peak detection in MZmine2."
- [readme] We [import](https://docs.qiime2.org/2018.11/tutorials/importing/) these files into the appropriate QIIME 2 artifact formats as follows: ... qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency] qiime tools import --input-path sirius.mgf --output-path sirius.mgf.qza --type MassSpectrometryFeatures: "qiime tools import --input-path feature-table.biom --output-path feature-table.qza --type FeatureTable[Frequency]"
- [readme] If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot this step before proceeding forward.: "If the MGF file has formatting errors (eg. no MS1 are included in the MGF, or if an MS1 entry does not have a corresponding MS2 entry), then an appropriate error message will help users troubleshoot"
- [other] Load the feature table (abundance matrix) and feature metadata (m/z, retention time, and/or spectral similarity annotations) into QIIME 2 artifact format.: "Load the feature table (abundance matrix) and feature metadata (m/z, retention time, and/or spectral similarity annotations) into QIIME 2 artifact format."
- [readme] The input CSI results, feature tables and MS2 match tables should have a one-to-one correspondence i.e CSI results, feature tables and MS2 match tables from all datasets should be provided in the same order.: "The input CSI results, feature tables and MS2 match tables should have a one-to-one correspondence i.e CSI results, feature tables and MS2 match tables from all datasets should be provided in the"
