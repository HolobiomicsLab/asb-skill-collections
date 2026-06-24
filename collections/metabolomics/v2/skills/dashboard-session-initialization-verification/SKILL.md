---
name: dashboard-session-initialization-verification
description: Use when after loading a specXplore session data object (saved .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - specXplore
  - Jupyter notebooks
  - Python
  techniques:
  - LC-MS
  license_tier: restricted
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

# dashboard-session-initialization-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that a specXplore dashboard session instance correctly initializes and becomes accessible after loading a saved session data object from disk. This skill confirms the integrity of the session reconstruction workflow and readiness for interactive visual exploration.

## When to use

After loading a specXplore session data object (saved .pkl or equivalent file) from disk in a Jupyter notebook or Python environment, use this skill to validate that the dashboard-session architecture layer has instantiated without errors and that the interactive dashboard is responsive to user input before proceeding with visual exploration.

## When NOT to use

- Input spectral data is not yet processed into a session data object; use the Jupyter importing pipeline first to create the session file.
- Running on Windows without Microsoft Visual C++ Redistributable and Cython backend installed; current specXplore version fails on Windows.
- Session data object is corrupted or incompatible with the installed specXplore version; validate file integrity before attempting initialization.

## Inputs

- specXplore session data object file (saved to disk by the Jupyter importing pipeline)
- Python runtime environment with specXplore package and dependencies installed

## Outputs

- Instantiated specXplore dashboard session object
- Interactive dashboard widget rendered in Jupyter notebook
- Verification report confirming initialization success and UI responsiveness

## How to apply

Load the specXplore session data object file from the hard drive using Python file I/O, then instantiate the specxplore dashboard session layer by passing the loaded session object as a constructor argument. Verify initialization by checking for absence of runtime exceptions during instantiation and confirming that the dashboard object has expected attributes (e.g., methods for rendering visualizations, node selection handlers). Test responsiveness by simulating user interactions such as clicking on nodes in the t-SNE embedding or hovering to trigger hover-text callbacks. The dashboard should render without lag and display interactive UI elements (buttons, settings panel, visualization canvas) within the Jupyter notebook cell.

## Related tools

- **specXplore** (Provides the dashboard session class and initialization framework for loading and visualizing LC-MS/MS spectral data) — https://github.com/kevinmildau/specXplore
- **Jupyter notebooks** (Runtime environment in which the specXplore session data object is loaded and the dashboard session is instantiated for interactive exploration)
- **Python** (Language for loading session data objects from disk and instantiating the dashboard session layer)

## Examples

```
from specxplore import SpecXploreSession; import pickle; session = pickle.load(open('my_specxplore_session.pkl', 'rb')); dashboard = SpecXploreSession(session); dashboard.show()
```

## Evaluation signals

- No exceptions or error messages during dashboard session instantiation; session object is successfully passed to the constructor.
- Dashboard widget renders visibly in the Jupyter notebook cell with a t-SNE embedding visualization and interactive overlays visible.
- Node selection works: clicking on a node in the t-SNE overview selects it and updates internal selection state; hovering displays node information in the textbox below the main panel.
- UI controls are responsive: settings panel allows parameter adjustment and buttons trigger visualization updates without lag.
- All expected visualization panels appear (t-SNE embedding, hover textbox, add-on visualization area below) and match layout described in the README.

## Limitations

- Current version of specXplore fails on Windows; installation and initialization are only supported on macOS and Linux.
- macOS arm64 (Apple Silicon) users should be aware of ms2deepscore issue #199: similarity predictions may be unreliable on affected systems, which indirectly affects specXplore dashboard displays built from those scores, without raising errors or warnings.
- Dashboard initialization requires pre-computed model and library files (e.g., from ms2query for positive/negative mode); missing model files will cause pipeline failures before session data is created.
- Session data object file format and specXplore package version must be compatible; mismatches may cause instantiation errors or unexpected behavior.

## Evidence

- [other] Load the specXplore session data object file from disk using Python file I/O; instantiate dashboard session layer with loaded object; verify initialization without errors; confirm responsive UI.: "Load the specXplore session data object file from disk using Python. Instantiate the specXplore dashboard session layer with the loaded session object. Verify that the dashboard-session architecture"
- [readme] Session data object workflow and dashboard instantiation.: "The pipeline produces a specXplore session data object that is saved to the hard drive and can be fed directly into a specxplore dashboard session instance for visual exploration."
- [readme] Dashboard interaction and UI verification.: "Clicking on a node in the t-SNE overview selects it. Hovering over a node will display node information in a textbox below the main t-SNE panel. With appropriate node selections made, the various"
- [readme] Jupyter notebook integration for dashboard instantiation.: "To open the demo notebook, make sure to use conda activate specxplore_environment to activate the environment with all specXplore dependencies installed, and run the jupyter-notebook command. From"
- [readme] Windows platform unsupported; macOS and Linux only.: "Please note that the current version of specXplore works on Macos and Linux but fails in windows."
