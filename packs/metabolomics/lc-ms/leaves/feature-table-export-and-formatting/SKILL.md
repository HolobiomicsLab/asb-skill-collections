---
name: feature-table-export-and-formatting
description: Use when after completing feature detection, alignment, and optional filtering (blank subtraction, QC reproducibility, feature occurrence thresholds) in MZmine2 or Optimus, and you need to prepare the feature table and MS/MS spectra for GNPS-based molecular networking, bioassay integration, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZmine2
  - Optimus
  - OpenMS
  - GNPS
  - Jupyter notebook
  techniques:
  - LC-MS
  - direct-infusion-MS
  - MS-imaging
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- '[Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)'
- or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-export-and-formatting

## Summary

Export aligned LC-MS/MS feature detection results into standardized quantification matrices and spectral files suitable for downstream molecular networking and bioassay integration. This skill bridges feature detection/alignment (MZmine2 or Optimus) and network annotation (GNPS) by packaging m/z, retention time, and per-sample intensity data into formats compatible with MS/MS spectral matching and bioassay-guided analysis.

## When to use

After completing feature detection, alignment, and optional filtering (blank subtraction, QC reproducibility, feature occurrence thresholds) in MZmine2 or Optimus, and you need to prepare the feature table and MS/MS spectra for GNPS-based molecular networking, bioassay integration, or downstream statistical analysis in R/Python. Use this skill when your LC-MS/MS experiment has yielded a unified feature list across all samples and you must hand off quantified features to external analysis platforms or Jupyter-based post-processing.

## When NOT to use

- Input is already a fully formatted feature table with validated compound annotations (level 3+ MSI); re-export risks losing manually curated metadata.
- MS/MS spectra are unavailable or deliberately excluded from the analysis (e.g., direct-infusion or targeted metabolomics with no fragmentation data).
- The downstream tool (e.g., a custom statistical pipeline) requires a non-standard format that contradicts GNPS or bioassay integration requirements; export once and validate schema compatibility first.

## Inputs

- aligned feature list (MZmine2 or Optimus output: mzML, NetCDF, or Optimus project file)
- per-sample intensity data across all samples post-alignment
- MS/MS spectra associated with detected features
- optional: list of molecules of interest for putative annotation (CSV or GNPS export)

## Outputs

- feature quantification matrix (CSV): m/z, RT, and per-sample abundances
- MS/MS spectral file (.MGF format) with feature identifiers
- optional: putatively annotated feature list (level 2 MSI)

## How to apply

Export the aligned feature list from MZmine2 or Optimus with columns for m/z, retention time (RT), and normalized or raw abundance values per sample, ensuring all optional filtering steps (e.g., exclusion of features from blank runs, removal of rarely observed features, QC reproducibility checks) have been applied beforehand. Simultaneously export a .MGF (mascot generic format) file containing MS/MS spectral summaries linked to each feature. Verify that feature identifiers are consistent across the CSV quantification table and the .MGF file, and that the table includes only features with associated MS/MS scans if downstream GNPS matching is planned. The CSV should be formatted with features as rows and samples as columns; check that no missing values are left unfilled (use zero-fill or interpolation as appropriate per your study design). Convert to the expected GNPS input schema if needed, documenting any normalization method applied (TIC, internal standards, or QC-based).

## Related tools

- **MZmine2** (performs initial feature detection, alignment, and quantification; exports CSV quantification matrix and .MGF spectral file) — http://mzmine.github.io/
- **Optimus** (alternative workflow for LC-MS feature detection, alignment, quantification, optional filtering, and export to CSV and .MGF for GNPS submission) — https://github.com/MolecularCartography/Optimus
- **OpenMS** (underlying algorithmic library used by Optimus for state-of-the-art feature detection and quantification) — http://www.openms.de
- **GNPS** (downstream platform for MS/MS spectral matching, molecular networking, and integration with putative annotation from the exported .MGF and metadata) — http://gnps.ucsd.edu
- **Jupyter notebook** (post-processing and integration of exported feature table with bioassay data for bioactive molecular network analysis) — https://github.com/DorresteinLaboratory/Bioactive_Molecular_Networks

## Evaluation signals

- CSV quantification matrix contains all expected columns (m/z, RT, sample intensities) with no null values for row identifiers; row count matches feature count post-filtering.
- .MGF file parses without errors and contains MS/MS spectra linked to feature m/z and RT via consistent identifier fields across both files.
- Feature identifiers in CSV and .MGF are one-to-one aligned; no orphaned spectra or missing entries.
- Abundance values are non-negative and fall within expected ranges for your normalization method (e.g., 0–1 for TIC-normalized, or raw instrument counts); check for unrealistic outliers.
- Round-trip test: re-import the exported CSV and .MGF into GNPS or a validation script and confirm downstream processing proceeds without schema or identifier conflicts.

## Limitations

- MS/MS validation of putative annotations (level 2 MSI) is not automatically provided by MZmine2 or Optimus; manual or in-silico confirmation (e.g., Sirius, MS-FINDER) is required for higher confidence.
- Export does not include retention time correction or drift compensation across instrument sessions; if RT calibration is needed, apply it before export or document the limitation in downstream reporting.
- Large datasets (hundreds of LC-MS runs) may produce very large .MGF files; some GNPS submissions have practical file-size or upload limits; consider batch splitting if necessary.
- Optional filtering steps (blank subtraction, QC reproducibility, feature occurrence thresholds) must be configured correctly before export; incorrect filter settings are not flagged during export itself.

## Evidence

- [other] Export the processed feature table with m/z, retention time, and per-sample abundance columns to a quantification file.: "Export the processed feature table with m/z, retention time, and per-sample abundance columns to a quantification file."
- [readme] The workflow relies on open bioinformatic tools, such MZmine2 or Optimus (using OpenMS), a Jupyter notebook, and the GNPS web-platform.: "The workflow relies on open bioinformatic tools, such [MZmine2]... or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)...and the GNPS web-platform"
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS; a .MGF file containing the MS/MS spectral summary.: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS; a .MGF file containing"
- [readme] Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest. This implements a molecular identification at the level putatively annotated compounds, corresponding to the level 2 of the Metabolomics Standards Initiative.: "Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest...corresponding to the level 2 of the Metabolomics Standards Initiative"
- [readme] The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries available at GNPS.: "The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries available at GNPS."
