---
name: lc-ms-spectral-data-import
description: Use when you have raw LC-MS/MS spectral data in .mgf format (or vendor-specific
  raw data that can be converted to .mgf via MZmine or similar tools) and need to
  prepare it for interactive exploration using the specXplore dashboard.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Jupyter Notebook
  - specXplore
  - ms2deepscore
  - matchms
  - MZmine
  - ms2query
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specxplore
    doi: 10.1021/acs.analchem.3c04444
    title: specxplore
  dedup_kept_from: coll_specxplore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04444
  all_source_dois:
  - 10.1021/acs.analchem.3c04444
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS spectral data import

## Summary

Convert raw LC-MS/MS spectral data in .mgf format into a serialized specXplore session data object through an interactive Jupyter notebook pipeline. This skill bridges raw mass spectral acquisition output and downstream interactive visualization by validating input format, computing similarity embeddings, and persisting a structured session object to disk.

## When to use

You have raw LC-MS/MS spectral data in .mgf format (or vendor-specific raw data that can be converted to .mgf via MZmine or similar tools) and need to prepare it for interactive exploration using the specXplore dashboard. Apply this skill when you want to leverage t-SNE embedding and ms2deepscore-based similarity scoring to create an overview representation of mass spectral relationships before visualization.

## When NOT to use

- Input data is already in a pre-processed specXplore session format or dashboard-ready serialized object.
- Raw data is in vendor-specific binary format (e.g., .raw, .d) without conversion to .mgf first.
- Feature identifiers are missing or cannot be standardized to 'feature_id' key in spectra metadata.
- Operating system is Windows and ms2deepscore ARM64 reliability issues on macOS are a concern (see known issues).

## Inputs

- .mgf file with MS/MS spectral data and metadata
- Feature identifiers (expected key: 'feature_id') in spectra metadata
- Pre-trained model files for ms2query, ms2deepscore, and spec2vec (mode-specific: positive or negative)

## Outputs

- Serialized specXplore session data object (saved to hard drive)
- t-SNE embedding coordinates for overview visualization
- ms2deepscore similarity matrix
- Session metadata and spectra index

## How to apply

Launch a Jupyter notebook environment within a conda environment containing specXplore and its dependencies (Python 3.8+). Load a .mgf file containing MS/MS spectra, ensuring the file includes a feature identifier with the key 'feature_id' (rename if necessary using matchms.Spectrum or a text editor). Execute the specXplore importing pipeline to process the spectral data, which computes t-SNE embedding and ms2deepscore similarity scores. Serialize the resulting specXplore session data object and save it to the hard drive as a .pkl or similar format. Verify that the session object contains the required metadata fields and that t-SNE coordinates and similarity matrices are populated before passing the object to the specXplore dashboard session instance.

## Related tools

- **Jupyter Notebook** (Interactive environment for executing the specXplore importing pipeline and processing spectral data)
- **specXplore** (Python dashboard tool and importing pipeline for LC-MS/MS spectral data processing and session object creation) — https://github.com/kevinmildau/specXplore
- **ms2deepscore** (Computes deep-learning-based similarity scores for mass spectra used in t-SNE embedding) — https://github.com/matchms/ms2deepscore
- **matchms** (Python library for spectrum metadata manipulation and feature identifier renaming) — https://matchms.readthedocs.io/
- **MZmine** (Vendor-independent tool for converting raw mass spectrometry data to .mgf format) — https://mzmine.github.io/mzmine_documentation/
- **ms2query** (Provides pre-trained model and library files required by the importing pipeline)

## Examples

```
jupyter-notebook demo.ipynb (within conda environment with specXplore installed; then replace mgf filepath with your own .mgf file and execute the notebook cells to process spectral data and create the session object)
```

## Evaluation signals

- Session data object is successfully serialized and saved to disk without errors or warnings.
- t-SNE embedding coordinates are computed and stored (verify dimensionality: 2D or 3D coordinates for all spectra).
- ms2deepscore similarity matrix is populated and symmetric, with values in expected range [0, 1].
- Feature identifiers in the session object match input .mgf spectra and correspond to 'feature_id' metadata key.
- Session object can be loaded and passed directly to specXplore dashboard instance without requiring re-processing.

## Limitations

- specXplore currently requires .mgf formatted files; raw vendor-specific formats must be converted upstream (via MZmine, etc.).
- Feature identifier key must be exactly 'feature_id' in spectra metadata; manual renaming is required if the input uses a different key.
- Pre-trained model and library files are mode-specific (positive or negative ion mode); incorrect model selection will produce unreliable ms2deepscore similarity predictions.
- macOS ARM64 systems have a known issue with ms2deepscore (issue #199) where similarity predictions may not match results on Windows or Intel-based systems, without error or warning messages.
- Installation and execution on Windows requires Microsoft Visual C++ Redistributable and Cython backend; current version is known to fail on Windows systems.
- t-SNE embedding computation is sensitive to hyperparameters and random seed; results may vary across runs unless seed is fixed.

## Evidence

- [readme] The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter notebooks using the specXplore importing pipeline.: "The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter"
- [readme] The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration.: "The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration."
- [readme] specXplore currently requires a .mgf formatted file with MS/MS spectral data. To generate a .MGF file from your raw data please refer to processing options in your vendor specific software or the workflows described in MZmine.: "specXplore currently requires a .mgf formatted file with MS/MS spectral data. To generate a .MGF file from your raw data please refer to processing options in your vendor specific software or the"
- [readme] Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id'.: "Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id'."
- [readme] SpecXplore is a python dashboard tool for adjustable LC-MS/MS spectral data exploration. It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore.: "SpecXplore is a python dashboard tool for adjustable LC-MS/MS spectral data exploration. It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on"
- [readme] Warning: users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems.: "Warning: users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not"
- [readme] To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data.: "To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data."
