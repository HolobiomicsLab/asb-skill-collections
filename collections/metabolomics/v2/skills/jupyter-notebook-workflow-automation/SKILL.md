---
name: jupyter-notebook-workflow-automation
description: Use when when you have raw LC-MS/MS spectral data in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Jupyter notebooks
  - specXplore
  - ms2deepscore
  - matchms
  - MZmine3
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans:
- processed in interactive Jupyter notebooks using the specXplore importing pipeline
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

# jupyter-notebook-workflow-automation

## Summary

Automate multi-stage LC-MS/MS spectral data processing pipelines within Jupyter notebooks to generate serialized session data objects for downstream visualization. This skill enables interactive, reproducible preprocessing of mass spectral data with integrated model inference and metadata validation.

## When to use

When you have raw LC-MS/MS spectral data in .mgf format that needs to be converted into a specXplore session data object for interactive dashboard exploration, and you want to iterate on preprocessing parameters, apply ms2deepscore similarity embeddings, and validate feature identifiers within a single interactive notebook environment before committing results to disk.

## When NOT to use

- Input data is already in specXplore session format or has been previously serialized — skip directly to dashboard loading.
- Raw instrument vendor files (Thermo .raw, AB .d, Waters .raw) have not been converted to .mgf format — pre-process via vendor software or MZmine3 export first.
- You are running on Windows and encounter the known ms2deepscore incompatibility — wait for upstream package fixes or use macOS/Linux systems where the workflow is validated.

## Inputs

- .mgf spectral data file containing MS/MS fragmentation patterns with feature metadata
- Pre-trained ms2query model files (positive or negative ionization mode) from Zenodo
- Feature identifier metadata (must contain 'feature_id' key)

## Outputs

- Serialized specXplore session data object (saved to hard drive)
- t-SNE embedding representation of mass spectral similarities based on ms2deepscore
- Processed spectral dataset ready for downstream dashboard visualization

## How to apply

Launch a Jupyter notebook within a conda environment containing specXplore and its dependencies (including ms2deepscore). Load raw .mgf spectral data files using specXplore's importing pipeline functions, ensuring that feature identifiers are keyed as 'feature_id' (rename using matchms.Spectrum if necessary). Execute the importing pipeline, which applies ms2deepscore to compute t-SNE embeddings of mass spectral similarities and constructs a session data object. Iteratively adjust preprocessing parameters and re-run cells to validate output quality. Finally, serialize the session data object and save it to disk as a persistent file. Verify that the saved object can be loaded directly into a specXplore dashboard instance without errors.

## Related tools

- **specXplore** (Python package providing the importing pipeline, session data object serialization, and t-SNE/ms2deepscore integration for LC-MS/MS spectral preprocessing) — https://github.com/kevinmildau/specXplore
- **ms2deepscore** (Computes neural-network-based similarity scores between mass spectra and generates t-SNE embeddings for overview representation)
- **Jupyter notebooks** (Interactive execution environment for running the specXplore importing pipeline with cell-by-cell parameter iteration and validation)
- **matchms** (Utility library (matchms.Spectrum module) for renaming and adding metadata keys to spectral objects when feature_id key is missing or incorrectly named) — https://matchms.readthedocs.io/en/latest/
- **MZmine3** (Vendor-agnostic data processing tool for converting raw LC-MS/MS files to .mgf format with GNPS/FBMN export options) — https://mzmine.github.io/mzmine_documentation/

## Examples

```
jupyter-notebook demo.ipynb  # (after conda activate specxplore_environment) to open the example notebook, then replace the demo.mgf filepath with your own .mgf file and execute cells sequentially to process spectral data and save the session object
```

## Evaluation signals

- Serialized session data object loads successfully into specXplore dashboard instance without deserialization errors or missing attributes.
- t-SNE embedding dimensions match expected shape (typically 2D for visualization); no NaN or infinite values present in coordinates.
- Feature identifiers in processed object are uniformly keyed as 'feature_id' with no missing or duplicate values in the dataset.
- ms2deepscore similarity scores fall within expected range [0, 1] and show reasonable clustering of spectrally similar compounds in t-SNE plot.
- Notebook execution is reproducible: re-running all cells with identical input .mgf file and model files produces byte-identical session object.

## Limitations

- Requires pre-trained model and library files from ms2query (separate download from Zenodo); workflow fails silently if these are missing or in incorrect folder structure.
- Input .mgf file must contain 'feature_id' metadata key; absence or incorrect naming will cause pipeline failure. Manual renaming via text editor or matchms.Spectrum is required as a workaround.
- On macOS ARM64 (Apple Silicon) systems, ms2deepscore v0.2.x produces unreliable similarity predictions compared to Intel/Windows/Linux systems due to known issue #199 in ms2deepscore; no error message is raised, causing silent data corruption.
- Currently does not work on Windows platforms; installation and full workflow validation completed only on macOS and Linux.
- Requires C++ compilers (Cython backend) and ANACONDA environment management; installation can fail on systems lacking appropriate developer tools or compiler chains.

## Evidence

- [readme] First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter notebooks using the specXplore importing pipeline.: "the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter notebooks using the specXplore importing pipeline"
- [readme] The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration.: "The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance"
- [readme] specXplore currently requires a .mgf formatted file with MS/MS spectral data. Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id'.: "specXplore currently requires a .mgf formatted file with MS/MS spectral data. Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to"
- [readme] To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data.: "To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data"
- [readme] users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems.: "users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in"
- [readme] Please note that the current version of specXplore works on Macos and Linux but fails in windows.: "the current version of specXplore works on Macos and Linux but fails in windows"
- [readme] It joins a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore: "a t-SNE embedding that serves as an overview representation of mass spectral similarities based on ms2deepscore"
- [readme] Renaming the feature identifying key in a .MGF file is possible using matchms, specifically the matchms.Spectrum module which provides a means of adding metadata keys to existing spectra in Python.: "Renaming the feature identifying key in a .MGF file is possible using matchms, specifically the matchms.Spectrum module which provides a means of adding metadata keys to existing spectra"
