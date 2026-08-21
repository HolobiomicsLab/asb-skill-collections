---
name: preference-system-integration
description: Use when when a GUI widget (e.g., isotopes display, compound list, or
  analysis parameter panel) must show or hide content according to user selections
  stored in application preferences, and the current implementation either shows all
  content regardless of preference or lacks a preference-reading.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  tools:
  - git
  - qmake
  - make
  - Maven GUI
  - Qt5
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12080684
  title: MAVEN2
evidence_spans:
- git clone --recursive [redacted-email]:eugenemel/maven.git maven
- qmake -r build.pro
- make -j4
- 'Maven GUI: Metabolomics Analysis and Visualization Engine'
- Install the qt5 package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maven2_cq
    doi: 10.3390/metabo12080684
    title: MAVEN2
  dedup_kept_from: coll_maven2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12080684
  all_source_dois:
  - 10.3390/metabo12080684
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# preference-system-integration

## Summary

Integrate application preference settings into GUI widget rendering logic to dynamically filter or restrict displayed content based on user-selected options. This skill enables stateful, preference-driven UI behavior in metabolomics visualization tools.

## When to use

When a GUI widget (e.g., isotopes display, compound list, or analysis parameter panel) must show or hide content according to user selections stored in application preferences, and the current implementation either shows all content regardless of preference or lacks a preference-reading mechanism. Specifically triggered when reverse-engineering or implementing preference-filtering logic for widgets that should respect application-wide configuration state.

## When NOT to use

- Widget preferences are stored in transient UI state rather than persistent application preferences.
- The widget should always display all available content regardless of user settings (e.g., a reference database or legend).
- Preference filtering has already been implemented and is functioning correctly.

## Inputs

- Qt5 widget source code (typically .cpp and .h files in src/ directory)
- Application preference storage (configuration file or settings object)
- Widget display logic and rendering loop
- Preference selection metadata (list of enabled/selected items)

## Outputs

- Modified widget rendering code with integrated preference filter
- Recompiled executable with preference-driven display behavior
- Test results confirming widget visibility matches preference state

## How to apply

Locate the preference-selection mechanism (typically a settings dialog or configuration file) and the widget's display rendering loop (usually in the Qt5 paint or model-update method). Read the active/selected items from application preferences at widget initialization or on preference-change signals. Implement a filter that suppresses rendering of any item not in the selected set by wrapping the display loop in a conditional that checks each item against the preference set before rendering. Recompile using qmake and make, then manually test the widget to confirm visibility now matches preference selection. The filter must be applied consistently: either in the data model layer (preferred) or in the rendering layer, but not both, to avoid duplicate filtering.

## Related tools

- **Maven GUI** (Metabolomics visualization engine containing the isotopes widget and preference system to be integrated) — https://github.com/eugenemel/maven
- **Qt5** (GUI framework providing widget rendering, signal/slot preference change notifications, and data model filtering)
- **qmake** (Build system for compiling Qt5 projects after preference-filter implementation)
- **make** (Parallel compilation of modified source code (-j4 flag for multi-core builds))
- **git** (Version control for branching, committing preference-filter changes, and submitting pull requests) — https://github.com/eugenemel/maven

## Evaluation signals

- Widget rendering loop contains conditional check against preference set before displaying each item.
- Manual testing confirms items not in the preference selection are not rendered; selected items are rendered.
- Preference change events (e.g., signal/slot) trigger widget update and immediately reflect new visibility state.
- Code compiles without errors using qmake -r build.pro and make -j4.
- Diff of source code shows preference-read call at widget initialization or on preference-change signal, with filter logic applied in rendering loop.

## Limitations

- The provided README contains only build instructions and retirement notice; the isotopes widget preference-filtering mechanism is not documented in available source text.
- Implementation requires manual code inspection of the Maven GUI repository to locate preference storage and widget rendering code.
- Filter effectiveness depends on preference data format and consistency—if preferences are not persisted or are inconsistently accessed, the filter may not apply reliably.
- Qt5 signal/slot connections must be properly configured; if preference-change signals are not connected to widget update methods, preference changes will not trigger re-rendering.

## Evidence

- [other] How does the isotopes widget restrict its display to only those isotopes that have been selected in the application preferences?: "How does the isotopes widget restrict its display to only those isotopes that have been selected in the application preferences?"
- [other] Identify the preference-selection mechanism and the isotopes display rendering logic. Implement a filter that reads the active isotopes from application preferences and applies it to the isotopes widget display loop, suppressing rendering of any isotope not in the selected set.: "Identify the preference-selection mechanism and the isotopes display rendering logic. Implement a filter that reads the active isotopes from application preferences and applies it to the isotopes"
- [other] Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors.: "Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors."
- [other] Test the widget manually to confirm that isotope visibility now matches the preference selection.: "Test the widget manually to confirm that isotope visibility now matches the preference selection."
- [readme] Maven GUI: Metabolomics Analysis and Visualization Engine: "Maven GUI: Metabolomics Analysis and Visualization Engine"
