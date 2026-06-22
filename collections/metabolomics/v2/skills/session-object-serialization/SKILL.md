---
name: session-object-serialization
description: Use when after you have processed raw LC-MS/MS spectral data through the specXplore importing pipeline in a Jupyter notebook and produced an in-memory specXplore session data object containing t-SNE embeddings (based on ms2deepscore similarity scores) and associated spectral metadata.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - specXplore
  - Jupyter notebooks
  - ms2deepscore
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
---

# session-object-serialization

## Summary

Serialize and persist a specXplore session data object (containing processed LC-MS/MS spectral embeddings, similarity scores, and metadata) to disk as a file artifact that can be loaded into the interactive dashboard for visual exploration. This step bridges the offline Jupyter preprocessing stage and the online dashboard visualization stage.

## When to use

After you have processed raw LC-MS/MS spectral data through the specXplore importing pipeline in a Jupyter notebook and produced an in-memory specXplore session data object containing t-SNE embeddings (based on ms2deepscore similarity scores) and associated spectral metadata. Use this skill when you need to save that processed object to disk so it can be loaded and reused by the specXplore dashboard instance without recomputing the expensive embedding and similarity calculations.

## When NOT to use

- You are still in the active Jupyter preprocessing notebook and have not yet finished building the session data object (i.e., embeddings or similarity scores have not been computed).
- You only intend to visualize data once in a single Jupyter session and do not need to preserve the session for later reuse or sharing.
- The input LC-MS/MS data has not been converted to .mgf format with feature identifiers keyed as 'feature_id' — serialization will fail or produce incomplete metadata.

## Inputs

- specXplore session data object (in-memory Python object from the importing pipeline)
- output file path (string)

## Outputs

- serialized specXplore session data file saved to hard drive (binary/proprietary format)
- file path to the persisted session object

## How to apply

Within the Jupyter notebook environment where the specXplore importing pipeline has produced a session data object, call the pipeline's serialization method to write the object to the hard drive as a persistent file. The exact serialization method (e.g., pickle, HDF5, or proprietary format) is handled by the specXplore library; you specify an output file path. The saved file should include the t-SNE embedding coordinates, ms2deepscore similarity matrix, feature identifiers (keyed as 'feature_id'), and any overlay or addon metadata. Verify the file was written to disk and is non-empty before proceeding to load it in the dashboard. The rationale is that t-SNE embedding and ms2deepscore computation are computationally expensive; serialization allows you to compute once and reuse many times across interactive dashboard sessions.

## Related tools

- **specXplore** (Provides the session data object structure, importing pipeline, and serialization interface for persisting processed spectral data.) — https://github.com/kevinmildau/specXplore
- **Jupyter notebooks** (Interactive environment in which the specXplore importing pipeline runs and from which the session data object is serialized to disk.)
- **ms2deepscore** (Provides the similarity scores computed during the importing pipeline that are embedded in the serialized session data object.)

## Evaluation signals

- A file is successfully written to the specified output path on the hard drive with non-zero file size.
- The file can be read back into a Jupyter notebook and deserialized into a valid specXplore session data object without errors.
- The deserialized object contains expected keys and structures: t-SNE coordinates (2D or higher), ms2deepscore similarity matrix, feature identifiers keyed as 'feature_id', and spectral metadata.
- The deserialized session object can be fed directly into a specXplore dashboard session instance and renders correctly without requiring re-computation of embeddings or similarity scores.
- File timestamps and size remain consistent across multiple reads, confirming persistence and integrity.

## Limitations

- specXplore importing pipeline and serialization currently fail on Windows systems; works reliably only on macOS and Linux.
- On macOS arm64 (Apple Silicon) computers, ms2deepscore similarity predictions may be unreliable due to issue #199 in the ms2deepscore package; this affects the quality of serialized session data but does not cause errors or warnings.
- Serialized session objects are dependent on the version of specXplore used to create them; backward/forward compatibility across versions is not documented.
- The .mgf input file must have feature identifiers keyed as 'feature_id'; if this key is absent or misnamed, the importing pipeline will not populate metadata correctly in the serialized object.

## Evidence

- [intro] The pipeline produces a specXplore session data object that is saved to the hard drive: "The pipeline produces a specXplore session data object that is saved to the hard drive"
- [intro] can be fed directly into a specxplore dashboard session instance for visual exploration: "can be fed directly into a specxplore dashboard session instance for visual exploration"
- [readme] The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter notebooks using the specXplore importing pipeline.: "The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter"
- [readme] specXplore currently requires a .mgf formatted file with MS/MS spectral data: "specXplore currently requires a .mgf formatted file with MS/MS spectral data"
- [readme] Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id': "Feature lists should always contain some form of feature identifier, and specXplore expects the feature identifier key to be 'feature_id'"
