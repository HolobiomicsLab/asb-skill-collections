---
name: qt-widget-rendering-control
description: Use when you need to restrict a Qt widget's display to a subset of its managed items—such as filtering isotope species in a metabolomics visualization—where the active subset is defined by application preferences stored outside the widget itself.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - git
  - qmake
  - make
  - Maven GUI
  - Qt5
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# qt-widget-rendering-control

## Summary

Control Qt widget visibility and rendering by implementing preference-based filtering logic that selectively enables or suppresses display of widget elements based on application state. This skill is essential when a GUI component must adapt its visible content to match user-configured preferences without re-architecting the underlying widget.

## When to use

Apply this skill when you need to restrict a Qt widget's display to a subset of its managed items—such as filtering isotope species in a metabolomics visualization—where the active subset is defined by application preferences stored outside the widget itself. Use it when the widget's rendering loop iterates over all available items but only a filtered set should be visible to the user.

## When NOT to use

- The widget data is already pre-filtered at load time and stored only for visible items—rendering-time filtering would be redundant.
- Application preferences are not yet accessible from the widget context or require a major architectural refactor to expose.
- The widget uses a model–view architecture (e.g., QAbstractItemModel) where filtering should instead be implemented in a proxy model layer.

## Inputs

- Qt widget source code (.cpp, .h files)
- Application preference data structure (active items/isotopes list)
- Maven GUI project build configuration (build.pro, .pro files)

## Outputs

- Modified widget rendering logic with integrated preference filter
- Recompiled Qt executable with selective rendering applied
- Widget displaying only preference-selected items

## How to apply

Locate the widget's source code in the Maven GUI codebase (typically under src/ in the Qt project tree). Identify both the preference-selection mechanism (how active items are stored in application state) and the widget's display rendering logic (the loop that draws or populates each item). Implement a filter that reads the active items from application preferences and applies it to the rendering loop, suppressing output for any item not in the selected set. Verify correctness by recompiling the project using `qmake -r build.pro` and `make -j4`, then test the widget manually to confirm that item visibility now matches the preference selection. This approach avoids re-filtering data at load time by gating visibility at render time.

## Related tools

- **qmake** (Qt project build configuration tool; used to generate platform-specific makefiles before compilation)
- **make** (Build automation; invoked with -j4 flag to compile the Maven GUI project in parallel)
- **git** (Version control; used to clone the eugenemel/maven repository and manage feature branches for code submission)
- **Qt5** (GUI framework; provides the widget rendering engine and preference API used to implement selective visibility)
- **Maven GUI** (Host application and metabolomics visualization engine; contains the isotopes widget and preference store to be modified) — https://github.com/eugenemel/maven

## Evaluation signals

- Compilation succeeds with no errors when running `qmake -r build.pro && make -j4`
- Manual testing confirms that only isotopes present in the application preference set are rendered in the widget
- Isotopes absent from preferences are not drawn or appear grayed/hidden in the widget display
- Toggling preferences in the application dynamically updates widget visibility without requiring restart
- Code review on the pull request confirms the filter logic correctly reads and applies the preference set without side effects

## Limitations

- The task card notes that no implementation details were found in the provided README text—actual widget and preference API locations must be discovered by source code inspection.
- Performance impact of rendering-time filtering depends on the number of items and complexity of the preference lookup; for very large datasets, pre-filtering at load time may be preferable.
- Changes must pass both Travis (macOS) and Appveyor (Windows) CI pipelines; Linux builds have been retired as of 20241105.

## Evidence

- [other] Identify the preference-selection mechanism and the isotopes display rendering logic. 4. Implement a filter that reads the active isotopes from application preferences and applies it to the isotopes widget display loop, suppressing rendering of any isotope not in the selected set.: "Identify the preference-selection mechanism and the isotopes display rendering logic. Implement a filter that reads the active isotopes from application preferences and applies it to the isotopes"
- [other] Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors.: "Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors."
- [other] Test the widget manually to confirm that isotope visibility now matches the preference selection.: "Test the widget manually to confirm that isotope visibility now matches the preference selection."
- [intro] Maven GUI: Metabolomics Analysis and Visualization Engine: "Maven GUI: Metabolomics Analysis and Visualization Engine"
- [readme] As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor: "As of 20241105, linux builds have been retired, and both mac os and windows executable are now produced by Appveyor"
