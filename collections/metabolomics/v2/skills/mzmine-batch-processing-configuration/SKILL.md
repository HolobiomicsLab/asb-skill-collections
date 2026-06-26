---
name: mzmine-batch-processing-configuration
description: Use when you have raw metabolomics data in mzML or mzXML format and need
  to extract ion features, align them across samples, and produce a normalized feature
  table for downstream statistical or chemotaxonomic analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MZmine
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.05.13.593988v1
  title: plantMASST
evidence_spans:
- MZmine inputs used for metabolomics processing
- the MZmine inputs used for metabolomics processing
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_plantmasst_2_cq
    doi: 10.1101/2024.05.13.593988v1
    title: plantMASST
  dedup_kept_from: coll_plantmasst_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.05.13.593988v1
  all_source_dois:
  - 10.1101/2024.05.13.593988v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MZmine Batch Processing Configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and apply MZmine batch processing parameters to perform automated metabolomics feature detection, alignment, and normalization on raw mass spectrometry data (mzML/mzXML format). This skill enables reproducible, high-throughput metabolomics workflows by translating documented input configurations into executable batch jobs.

## When to use

You have raw metabolomics data in mzML or mzXML format and need to extract ion features, align them across samples, and produce a normalized feature table for downstream statistical or chemotaxonomic analysis. Use this skill when the repository or study documentation provides MZmine batch input files (.xml or configuration dumps) that specify the processing parameters for feature detection, alignment, and normalization suitable for your biological context.

## When NOT to use

- Input is already a processed feature table or aligned feature matrix; do not re-process.
- Raw data is in a non-standard MS format (e.g., proprietary binary) not supported by MZmine import.
- No batch configuration file or processing parameters are available; manual parameter optimization would be needed instead.

## Inputs

- MZmine batch configuration file (.xml or input configuration dump)
- Raw metabolomics data files in mzML or mzXML format
- Study or repository documentation of expected feature extraction parameters

## Outputs

- Aligned metabolomics feature table (CSV or mzTab format)
- Feature annotations (m/z, retention time, intensity per sample)
- Processing log or quality report

## How to apply

Clone the plantMASST repository and locate the MZmine/ directory containing input configuration and batch files. Open MZmine and load the batch processing configuration file, which encodes parameters for feature detection (mass accuracy, RT tolerance), alignment (m/z and retention time windows), and normalization steps. Load your raw metabolomics data (mzML/mzXML format) and execute the batch workflow end-to-end. Export the processed feature table in a standardized tabular format (CSV or mzTab), which will contain m/z values, retention times, and intensity measurements aligned across all input samples. Validate the output table dimensions (number of features and samples) and verify feature counts match repository documentation or expected magnitude for your experimental design.

## Related tools

- **MZmine** (Batch processing engine for automated feature detection, retention time alignment, mass accuracy calibration, and normalization of liquid chromatography–mass spectrometry (LC–MS) data)

## Evaluation signals

- Output feature table dimensions (rows = features, columns = samples) are consistent with input sample count and expected feature complexity for the metabolomics platform.
- Feature table contains populated m/z, retention time, and intensity columns with no null entries in core fields.
- Exported file format (CSV or mzTab) is readable and parseable; schema matches documented feature table structure in repository or manuscript supplementary materials.
- Feature counts and intensity ranges match orders of magnitude reported in the plantMASST manuscript or prior analyses of the same biological material.
- Processing log reports successful completion of feature detection, alignment, and normalization stages with no critical errors or warnings.

## Limitations

- Batch configuration parameters are optimized for the specific MS instrument and chromatographic method used in plantMASST; transfer to other platforms or ionization modes may require parameter re-tuning.
- No changelog is documented in the repository, limiting traceability of configuration changes across versions.
- Batch processing assumes uniform raw data format and quality; corrupted or malformed mzML/mzXML files may cause pipeline failure or partial output.

## Evidence

- [intro] The repository contains MZmine inputs used for metabolomics processing as part of its organized collection of analysis materials.: "MZmine inputs used for metabolomics processing"
- [other] The workflow involves loading raw data, executing batch processing for feature detection, alignment, and normalization, then exporting a standardized feature table.: "Load raw metabolomics data (mzML/mzXML format) into MZmine using the repository's batch processing configuration. 3. Execute the MZmine batch workflow to perform feature detection, alignment, and"
- [readme] The repository README explicitly lists MZmine inputs and batch files as organized content.: "MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project."
- [intro] Repository is organized around MZmine inputs for metabolomics processing.: "It is organized around the main tables used in the study, the notebooks that generate figure panels, the MZmine inputs used for metabolomics processing, and the supplementary HTML outputs produced"
- [other] Validation step confirms output feature table content and dimensions are correct.: "Validate the output feature table dimensions and content against repository documentation or expected schema."
