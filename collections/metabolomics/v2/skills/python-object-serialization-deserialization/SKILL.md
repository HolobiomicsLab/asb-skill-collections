---
name: python-object-serialization-deserialization
description: Use when when you have completed spectral data preprocessing in Jupyter notebooks and generated a specXplore session data object saved to disk, use this skill to restore that object into a live specXplore dashboard session instance for interactive LC-MS/MS spectral data exploration, without.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3373
  tools:
  - Python
  - specXplore
  - Jupyter notebooks
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans:
- SpecXplore is a python dashboard tool for adjustable LC-MS/MS spectral data exploration
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

# Python Object Serialization and Deserialization

## Summary

Load a serialized Python session data object from disk and instantiate it into an active dashboard session instance to enable interactive visualization. This skill bridges persistent storage and runtime exploration by reconstructing in-memory objects from saved state.

## When to use

When you have completed spectral data preprocessing in Jupyter notebooks and generated a specXplore session data object saved to disk, use this skill to restore that object into a live specXplore dashboard session instance for interactive LC-MS/MS spectral data exploration, without re-running the preprocessing pipeline.

## When NOT to use

- Input spectral data is in raw .mgf or .mzML format and has not yet been processed through the specXplore Jupyter notebook importing pipeline.
- The saved session object is corrupted, incompatible with the current specXplore package version, or missing required model/library files for ms2deepscore similarity scoring.
- You need to modify preprocessing parameters (e.g., t-SNE hyperparameters, ms2deepscore scoring) — regenerate the session object in Jupyter instead of deserializing a cached version.

## Inputs

- specXplore session data object file (serialized Python object, saved to hard drive)
- specXplore package with dashboard dependencies installed in active Python environment

## Outputs

- Active specXplore dashboard session instance (interactive Dash application)
- Accessible dashboard UI with t-SNE embedding, network views, similarity heatmaps, and fragmentation overview maps

## How to apply

Load the saved specXplore session data object file from the hard drive using Python's deserialization mechanisms (e.g., pickle or the specXplore import utilities). Instantiate a specxplore dashboard session layer by passing the deserialized session object as the initialization argument. Verify that the dashboard-session architecture layer initializes without errors by checking for any exceptions during instantiation. Confirm that the interactive dashboard application becomes responsive and accessible to user input interactions (clicking nodes, hovering for info, triggering overlays). The rationale is that the session object encapsulates all preprocessed spectral data, embeddings, and metadata from the Jupyter notebook stage, so direct feeding into the dashboard avoids redundant computation and enables rapid exploration.

## Related tools

- **Python** (Host language for object deserialization, session instantiation, and dashboard session layer setup)
- **specXplore** (Dashboard framework that accepts deserialized session objects and provides interactive visualization of LC-MS/MS spectral data) — https://github.com/kevinmildau/specXplore
- **Jupyter notebooks** (Preprocessing environment where session data objects are created and saved to disk before deserialization)

## Examples

```
from specxplore import SpecXploreSession; import pickle; session_obj = pickle.load(open('my_session.pkl', 'rb')); dashboard = SpecXploreSession(session_obj).run()
```

## Evaluation signals

- The deserialized session object is a valid Python object with expected attributes (e.g., spectral data, embeddings, metadata) accessible without AttributeError.
- Dashboard session instantiation completes without exceptions or warnings related to missing dependencies or incompatible object schemas.
- The dashboard UI renders and becomes responsive: nodes are clickable, hover text displays node information, and overlay/add-on buttons trigger visualizations.
- Interactive features work as expected: selecting nodes in the t-SNE overview, using ctrl+click for multi-node selection, and changing settings in the settings panel do not raise errors.
- Serialized session object file size and modification timestamp on disk remain consistent with the preprocessing output, indicating no corruption or partial deserialization.

## Limitations

- specXplore currently fails on Windows systems; deserialization and dashboard instantiation are only reliable on macOS and Linux.
- Pre-trained ms2deepscore model and library files must be available in the expected directory structure, or dashboard initialization will fail even if the session object deserializes successfully.
- On macOS ARM64 systems, ms2deepscore similarity predictions in the deserialized session object may be unreliable due to issue 199 in the ms2deepscore package; results will not match Windows, Ubuntu, or Intel macOS outputs.
- Session objects serialized with older specXplore package versions may not deserialize correctly into newer dashboard versions; compatibility is not guaranteed across releases.

## Evidence

- [intro] Loading saved session data from disk and initializing the dashboard: "A saved specXplore session data object is loaded from the hard drive and fed directly into a specxplore dashboard session instance to enable visual exploration of the spectral data."
- [intro] Two-stage workflow: preprocessing creates session object, deserialization enables dashboard: "The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter"
- [readme] Dashboard instantiation from saved session object: "can be fed directly into a specxplore dashboard session instance for visual exploration."
- [readme] Windows platform limitation for deserialization and dashboard use: "Please note that the current version of specXplore works on Macos and Linux but fails in windows."
- [readme] ms2deepscore ARM64 reliability issue affecting deserialized session data: "users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in"
- [readme] Model files required for successful session instantiation: "To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data. Model and library files for"
