---
name: metabolomics-feature-detection-and-alignment
description: Use when you have raw metabolomics mass spectrometry data in mzML or mzXML format and need to extract, align, and normalize metabolic features across multiple samples or conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MZmine
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2024.05.13.593988v1
  title: plantMASST
evidence_spans: []
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

# metabolomics-feature-detection-and-alignment

## Summary

This skill reconstructs and executes MZmine batch workflows to perform untargeted feature detection, alignment, and normalization on raw metabolomics data (mzML/mzXML format), producing a processed feature table suitable for downstream chemotaxonomic or comparative analysis.

## When to use

You have raw metabolomics mass spectrometry data in mzML or mzXML format and need to extract, align, and normalize metabolic features across multiple samples or conditions. This skill is appropriate when you have access to a documented MZmine batch configuration (as in the plantMASST repository) or when you need to set up feature detection pipelines for untargeted metabolomics workflows.

## When NOT to use

- Input is already a processed feature table or aligned/normalized feature matrix.
- Raw data is in a format other than mzML/mzXML (e.g., vendor-specific binary formats without conversion).
- No validated or documented batch configuration is available and you lack expertise to optimize MZmine parameters for your specific instrument and sample type.

## Inputs

- Raw metabolomics data files (mzML or mzXML format)
- MZmine batch processing configuration file (.xml or equivalent)
- MZmine input parameter specification (mass tolerance, retention time range, intensity thresholds)

## Outputs

- Processed feature table (CSV or mzTab format)
- Aligned and normalized metabolomics feature matrix
- Feature metadata (m/z, retention time, intensity statistics)

## How to apply

Clone or download the MZmine input configuration and batch files from the plantMASST repository (github.com/helenamrusso/plantmasst, specifically the MZmine/ directory). Load your raw metabolomics data (mzML/mzXML format) into MZmine and apply the repository's batch processing configuration to perform feature detection (peak picking), alignment across samples, and normalization. Execute the complete batch workflow to generate a processed feature table (exported in CSV or mzTab tabular format). The batch configuration encodes parameters for mass accuracy, retention time windows, and intensity thresholds tuned for the plantMASST use cases; validate that your feature table dimensions and content match the expected schema documented in the repository or inferred from the lineage and main study tables.

## Related tools

- **MZmine** (Performs feature detection, alignment, and normalization of raw metabolomics mass spectrometry data via batch processing workflows)

## Evaluation signals

- Output feature table has consistent column structure (m/z, retention time, intensity columns) matching the expected schema from plantMASST main tables.
- Feature table dimensions (number of features × number of samples) are consistent with the number of input raw data files and expected metabolomic complexity.
- Mass accuracy of detected features falls within the specified tolerance window (typically ≤ 5 ppm for high-resolution MS).
- Retention time alignment shows minimal drift across samples; peak alignment statistics should indicate successful alignment (few unaligned features, low m/z deviation between aligned peaks).
- Exported CSV/mzTab file can be loaded and parsed correctly; no missing values in critical columns (m/z, RT, intensity) unless explicitly expected.

## Limitations

- MZmine batch processing parameters are instrument- and sample-type-specific; parameters tuned for plantMASST use cases may not be optimal for other metabolomics datasets.
- The repository contains no changelog, making it difficult to track parameter evolution or validate reproducibility across repository versions.
- Feature detection and alignment performance depend on raw data quality (signal-to-noise ratio, dynamic range); poor-quality data may yield incomplete or misaligned features.
- Batch processing workflow assumes standard mzML/mzXML input format; vendor-specific or non-standard formats require prior conversion.

## Evidence

- [other] Clone the plantMASST repository from github.com/helenamrusso/plantmasst and locate the MZmine input configuration/batch files.: "Clone the plantMASST repository from github.com/helenamrusso/plantmasst and locate the MZmine input configuration/batch files."
- [other] Load raw metabolomics data (mzML/mzXML format) into MZmine using the repository's batch processing configuration.: "Load raw metabolomics data (mzML/mzXML format) into MZmine using the repository's batch processing configuration."
- [other] Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration.: "Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration."
- [other] Export the processed feature table in a standardized tabular format (CSV or mzTab).: "Export the processed feature table in a standardized tabular format (CSV or mzTab)."
- [readme] MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project.: "MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project."
