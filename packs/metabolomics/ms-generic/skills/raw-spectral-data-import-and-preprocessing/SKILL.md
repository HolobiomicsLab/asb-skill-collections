---
name: raw-spectral-data-import-and-preprocessing
description: Use when you have raw metabolomics data in mzML or mzXML format and need to convert it into a normalized feature table (CSV or mzTab) via automated batch processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# raw-spectral-data-import-and-preprocessing

## Summary

Import raw mass spectrometry data (mzML/mzXML format) into MZmine and apply batch processing configuration to perform feature detection, alignment, and normalization for metabolomics analysis. This skill bridges raw instrumental output to a processed feature table suitable for downstream chemotaxonomic or comparative metabolomics work.

## When to use

You have raw metabolomics data in mzML or mzXML format and need to convert it into a normalized feature table (CSV or mzTab) via automated batch processing. Specifically use this skill when you have a validated MZmine batch configuration file available (as provided in the plantMASST repository) and want to reproducibly apply the same feature extraction, alignment, and normalization parameters across multiple datasets or replicates.

## When NOT to use

- Input is already a processed feature table or peak list — this skill performs raw-to-feature conversion; applying it to downstream outputs will re-process and introduce bias.
- No validated batch configuration is available or parameters are unknown — ad-hoc parameter selection defeats reproducibility and reproducibility is a core benefit of this skill.
- Data is in a format other than mzML/mzXML (e.g., raw vendor formats like .raw or .d) — MZmine requires open exchange formats; convert via ProteoWizard or vendor tools first.

## Inputs

- Raw mass spectrometry data files (mzML or mzXML format)
- MZmine batch processing configuration file (.xml or equivalent)

## Outputs

- Processed feature table (CSV or mzTab format)
- Feature metadata (m/z, retention time, intensity values)

## How to apply

Clone or locate the plantMASST repository and retrieve the MZmine batch configuration files from the MZmine/ directory. Load your raw spectral data (mzML/mzXML format) into MZmine and apply the batch processing workflow by importing the configuration file. Execute the batch to perform feature detection (peak picking), retention-time-based alignment, and intensity normalization as encoded in the configuration. Export the processed feature table in tabular format (CSV or mzTab standard). Validate output by checking feature table dimensions (number of features × samples), verifying non-zero intensity distributions, and confirming alignment consistency against repository documentation or expected schema.

## Related tools

- **MZmine** (Performs batch feature detection, alignment, and normalization on raw spectral data via configurable workflow engine)

## Evaluation signals

- Feature table has expected dimensions: number of features and samples match input dataset count; no zero-intensity rows or columns.
- Output file is valid CSV or mzTab with required columns (m/z, retention time, sample intensities) and no parsing errors.
- Feature intensity distribution is log-normal or exhibits expected dynamic range; extreme outliers or all-zero features flagged as anomalies.
- Retention time alignment is consistent: features from the same compound across replicates cluster within expected tolerance (typically ±0.5 min or per-configuration threshold).
- Output schema matches repository documentation or prior runs: column names, data types, and metadata fields consistent with plantMASST use cases.

## Limitations

- Batch processing parameters are fixed by the configuration file; retuning requires editing XML or creating new configurations — not suitable for exploratory parameter search.
- Alignment quality depends on input data quality and consistency; poor-quality or off-scale samples may not align correctly regardless of batch configuration.
- No changelog or version history provided in repository — unclear if batch configurations are stable across MZmine releases or if software version compatibility is documented.

## Evidence

- [other] Load raw metabolomics data (mzML/mzXML format) into MZmine using the repository's batch processing configuration.: "Load raw metabolomics data (mzML/mzXML format) into MZmine using the repository's batch processing configuration."
- [other] Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration.: "Execute the MZmine batch workflow to perform feature detection, alignment, and normalization as specified in the input configuration."
- [other] Export the processed feature table in a standardized tabular format (CSV or mzTab).: "Export the processed feature table in a standardized tabular format (CSV or mzTab)."
- [readme] MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project.: "MZmine/: input files and batch files for the metabolomics datasets used in as use cases in this project."
- [readme] It is organized around the main tables used in the study, the notebooks that generate figure panels, the MZmine inputs used for metabolomics processing, and the supplementary HTML outputs produced from the analyses used as use cases.: "MZmine inputs used for metabolomics processing"
