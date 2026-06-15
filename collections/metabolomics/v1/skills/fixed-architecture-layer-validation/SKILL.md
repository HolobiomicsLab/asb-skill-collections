---
name: fixed-architecture-layer-validation
description: Use when after loading a specXplore session data object file from the hard drive and instantiating a dashboard session layer with it, validate that the architecture layer has initialized without errors and that the interactive dashboard is responsive to user input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - specXplore
  - ms2deepscore
  - Jupyter notebooks
derived_from:
- doi: 10.1021/acs.analchem.3c04444
  title: specxplore
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specxplore
    doi: 10.1021/acs.analchem.3c04444
    title: specxplore
  dedup_kept_from: coll_specxplore
schema_version: 0.2.0
---

# fixed-architecture-layer-validation

## Summary

Verification that a specXplore dashboard session instance initializes correctly and becomes accessible after loading a saved session data object from disk. This skill ensures the dashboard–session architecture layer is functional and responsive before interactive exploration begins.

## When to use

After loading a specXplore session data object file from the hard drive and instantiating a dashboard session layer with it, validate that the architecture layer has initialized without errors and that the interactive dashboard is responsive to user input. Apply this skill as a critical checkpoint in the two-stage specXplore workflow, between session object creation/loading and user interaction.

## When NOT to use

- The session data object file is corrupted, missing required model or library files (e.g., ms2query positive/negative mode models), or was created under incompatible specXplore versions.
- Running on Windows without Microsoft Visual C++ Redistributable or Cython backend dependencies properly installed; specXplore currently fails in Windows environments.
- The input .mgf spectral data file lacks the required 'feature_id' metadata key; the session object will be incomplete and dashboard instantiation will fail or produce non-functional state.

## Inputs

- specXplore session data object (saved to disk; format: Python pickle or equivalent serialized object)
- specxplore.dashboard.session module/class

## Outputs

- Initialized and accessible specXplore dashboard session instance
- Rendered interactive dashboard application with t-SNE overview, node selection capability, and overlay/add-on view controls

## How to apply

Load the serialized specXplore session data object from disk using Python, then instantiate the specxplore dashboard session layer by passing that loaded object into the dashboard session constructor. After instantiation, perform three checks: (1) verify that no exceptions or error messages are raised during dashboard initialization; (2) confirm that the dashboard application becomes accessible and can render its primary visualization components (t-SNE embedding, overlay and add-on view panels, hover textbox); and (3) test basic interactivity by simulating node selections, mouse hovers, and button clicks to confirm the dashboard responds to input events without freezing or crashing. Success means the architecture layer is stable and ready for downstream analytical exploration.

## Related tools

- **specXplore** (Python dashboard tool and session architecture layer for interactive LC-MS/MS spectral data visualization and exploration) — https://github.com/kevinmildau/specXplore
- **ms2deepscore** (Produces mass spectral similarity scores used to generate t-SNE embeddings for the dashboard overview representation)
- **Jupyter notebooks** (Environment for running the specXplore importing pipeline to process spectral data and create the session data object prior to dashboard instantiation)

## Examples

```
# Load session object and instantiate dashboard
from specxplore.dashboard import session as dashboard_session
import pickle

with open('my_specxplore_session.pkl', 'rb') as f:
    loaded_session = pickle.load(f)

app = dashboard_session.SpecXploreDashboard(loaded_session)
app.run()
```

## Evaluation signals

- No Python exceptions or traceback errors are raised during dashboard session instantiation.
- The dashboard application window opens and renders the t-SNE embedding panel, settings panel, node hover textbox, and button controls without blank or malformed UI regions.
- Clicking on a node in the t-SNE overview successfully selects it and updates visual feedback (e.g., node highlight or color change); holding Ctrl and clicking selects multiple nodes without error.
- Hovering over nodes displays metadata in the textbox below the t-SNE panel; metadata text updates without lag or incomplete data.
- Pressing overlay or add-on view buttons (e.g., for similarity heatmaps, fragmentation maps, network views) produces valid visualizations without crashing, and changing settings in the settings panel and re-pressing buttons correctly redraws the visualization.

## Limitations

- specXplore currently works only on macOS and Linux; installation and execution fails on Windows due to Cython backend and C++ compiler dependencies not being properly resolved in the Windows environment.
- On macOS arm64 systems, ms2deepscore (version dependency issue #199) produces unreliable similarity predictions that do not match results on Intel, Windows, or Ubuntu systems, and this issue produces no error messages, silently corrupting the t-SNE embedding and all downstream dashboard visualizations.
- Dashboard session instantiation requires pre-trained model and library files (ms2query, ms2deepscore, spec2vec models for positive or negative mode) to be installed in separate folders; missing or mismatched model files will cause instantiation to fail or produce incomplete session state.
- The .mgf input spectral data file must contain a 'feature_id' metadata key in every spectrum; if the key is missing or named differently, the session object creation will fail or the dashboard will display incomplete/incorrect feature information.

## Evidence

- [other] A saved specXplore session data object is loaded from the hard drive and fed directly into a specxplore dashboard session instance to enable visual exploration of the spectral data.: "a saved specXplore session data object is loaded from the hard drive and fed directly into a specxplore dashboard session instance to enable visual exploration of the spectral data"
- [readme] The specXplore workflow is separated into two stages. First, the user needs to process their spectral data in order to create a specxplore session data object. This is done in interactive Jupyter notebooks using the specXplore importing pipeline. The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration.: "The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration"
- [other] Verify that the dashboard-session architecture layer initializes without errors. Confirm that the interactive dashboard application becomes accessible and responsive to user input.: "Verify that the dashboard-session architecture layer initializes without errors. Confirm that the interactive dashboard application becomes accessible and responsive to user input"
- [readme] Before the specXplore workflow can be used, the package and its dependencies need to be installed using the guidelines below. Please note that the current version of specXplore works on Macos and Linux but fails in windows.: "the current version of specXplore works on Macos and Linux but fails in windows"
- [readme] Warning: users making use of macos arm64 computers should be aware of issue 199 for ms2deepscore. The current ms2deepscore package version may lead to ms2deepscore similarity predictions that are not in accordance with results on other systems (windows, ubuntu, macos intel). This issue does not result in any errors or warning messages, but makes ms2deepscore results unreliable!: "This issue does not result in any errors or warning messages, but makes ms2deepscore results unreliable!"
- [readme] To run ms2query, ms2deepscore, and spec2vec, model and library files are required. Pre-trained models are available via ms2query for both positive and negative mode data. Model and library files for positive or negative mode should be put into separate folders. The importing pipeline requires the appropriate model files to function.: "The importing pipeline requires the appropriate model files to function"
- [readme] specXplore expects the feature identifier key to be 'feature_id'. Renaming the feature identifying key in a .MGF file is possible using matchms, specifically the matchms.Spectrum module which provides a means of adding metadata keys to existing spectra in Python.: "specXplore expects the feature identifier key to be 'feature_id'"
