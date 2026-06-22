---
name: isotope-display-logic-modification
description: Use when when isotope visibility in the Maven GUI isotopes widget does not respect user selections made in application preferences, or when you need to restrict the widget display to a user-configured subset of available isotopes without modifying the underlying data model.
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

# isotope-display-logic-modification

## Summary

Modify the isotopes widget rendering logic in Maven GUI to filter and display only those isotopes that have been selected in the application's preference store. This skill involves locating the widget's display loop, implementing a preference-read mechanism, and applying a suppression filter to non-selected isotopes.

## When to use

When isotope visibility in the Maven GUI isotopes widget does not respect user selections made in application preferences, or when you need to restrict the widget display to a user-configured subset of available isotopes without modifying the underlying data model.

## When NOT to use

- The isotopes widget already correctly filters based on preferences — verify the current behavior first.
- Your use case requires modifying the underlying metabolite data model rather than just the display layer.
- You need to persist new isotope selections — this skill only implements filtering of existing preferences, not preference creation or modification UI.

## Inputs

- Maven GUI source tree (git repository clone)
- isotopes widget source code file
- application preferences/settings store
- list of user-selected isotopes from preferences

## Outputs

- modified isotopes widget source code
- recompiled Maven GUI binary
- feature branch with pull request for code review

## How to apply

Clone the eugenemel/maven repository recursively using git to access the Maven GUI source tree. Locate the isotopes widget source code in the src/ directory, identifying both the preference-selection mechanism (typically a Qt QSettings or preference store) and the display rendering loop. Implement a filter that reads the currently active isotope selections from application preferences and applies it during the widget rendering phase, suppressing rendering of any isotope not present in the selected set. Recompile using qmake -r build.pro followed by make -j4 to verify compilation succeeds. Manually test the widget to confirm isotope visibility now matches the preference selection state. Finally, commit changes to a feature branch and submit a pull request for code review.

## Related tools

- **git** (Clone the eugenemel/maven repository recursively to access source code) — https://github.com/eugenemel/maven
- **qmake** (Generate Qt makefiles for the Maven GUI project configuration)
- **make** (Compile the modified Maven GUI source with parallel jobs)
- **Maven GUI** (The metabolomics analysis and visualization engine containing the isotopes widget to be modified) — https://github.com/eugenemel/maven
- **Qt5** (GUI framework used by Maven GUI; provides QSettings and widget rendering mechanisms)

## Evaluation signals

- Recompilation produces no errors or warnings using qmake -r build.pro and make -j4.
- Manual widget testing shows that only isotopes present in the application preferences are rendered in the isotopes widget display.
- Isotopes absent from the preference selection set are completely suppressed (not rendered or grayed out).
- Toggling isotope selections in application preferences immediately reflects in the widget display after widget refresh.
- Code review approval and successful merge to main branch without regressions in related widgets or functionality.

## Limitations

- The provided source material (README) contains only a retirement notice and build status; no actual widget implementation details or preference API documentation are available, requiring inspection of the live source tree.
- This skill modifies only the display layer; if the underlying data model or preference serialization changes, the filter logic may require adjustment.
- Linux builds have been retired as of 20241105; testing and compilation are now only supported on macOS and Windows via Appveyor.

## Evidence

- [other] How does the isotopes widget restrict its display to only those isotopes that have been selected in the application preferences?: "How does the isotopes widget restrict its display to only those isotopes that have been selected in the application preferences?"
- [other] Locate the isotopes widget source code in the Maven GUI codebase (typically in the src/ directory tree). Identify the preference-selection mechanism and the isotopes display rendering logic. Implement a filter that reads the active isotopes from application preferences and applies it to the isotopes widget display loop, suppressing rendering of any isotope not in the selected set.: "Locate the isotopes widget source code in the Maven GUI codebase (typically in the src/ directory tree). Identify the preference-selection mechanism and the isotopes display rendering logic."
- [other] Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors.: "Recompile the project using qmake -r build.pro and make -j4 to verify no compilation errors."
- [other] Test the widget manually to confirm that isotope visibility now matches the preference selection.: "Test the widget manually to confirm that isotope visibility now matches the preference selection."
- [readme] Maven GUI: Metabolomics Analysis and Visualization Engine: "Maven GUI: Metabolomics Analysis and Visualization Engine"
