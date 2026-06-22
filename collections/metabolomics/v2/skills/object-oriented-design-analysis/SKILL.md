---
name: object-oriented-design-analysis
description: Use when you need to understand or document the extensibility architecture of a modular OOP codebase—specifically when developers must identify which classes, interfaces, or modules to extend or improve, or when onboarding contributors to a project whose documentation does not explicitly expose its.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - PlantUML
  - Git
derived_from:
- doi: 10.1021/acs.jproteome.2c00602
  title: CloMet
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clomet_cq
    doi: 10.1021/acs.jproteome.2c00602
    title: CloMet
  dedup_kept_from: coll_clomet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00602
  all_source_dois:
  - 10.1021/acs.jproteome.2c00602
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# object-oriented-design-analysis

## Summary

Extract and visualize the class diagram structure of an object-oriented modular software system to identify extension points, inheritance relationships, and module boundaries that guide developer contributions. This skill enables navigation of complex codebases designed with OOP standards by making the inheritance hierarchy, composition patterns, and factory/abstract class extension mechanisms explicit.

## When to use

Apply this skill when you need to understand or document the extensibility architecture of a modular OOP codebase—specifically when developers must identify which classes, interfaces, or modules to extend or improve, or when onboarding contributors to a project whose documentation does not explicitly expose its class hierarchy and extension points.

## When NOT to use

- The codebase is not object-oriented or uses only functional/procedural paradigms with minimal class abstraction.
- The source code is unavailable, obfuscated, or compiled-only (no parsed symbols available).
- The goal is runtime profiling or performance optimization rather than structural documentation for extension.

## Inputs

- Git repository URL or local source tree
- Object-oriented source code (e.g., Python, Java, C++)
- Project documentation or comments describing extension mechanisms

## Outputs

- Structured class diagram (PlantUML, UML, or equivalent format)
- List of identified extension points (abstract classes, interfaces, factory patterns)
- Module hierarchy and composition map
- Validation report confirming diagram accuracy against source code

## How to apply

Clone the target repository and perform static source code analysis to identify all class definitions, method signatures, inheritance chains, and composition relationships. Extract abstract classes, interfaces, factory patterns, and other extension mechanisms that represent intentional developer hook points. Parse these relationships into a structured format (PlantUML or equivalent) that visualizes the module hierarchy and class dependencies, ensuring that public classes and documented extension mechanisms are represented. Validate the resulting diagram against the source code to confirm completeness and accuracy of the hierarchy and identified extension points.

## Related tools

- **Docker** (Containerization and reproducible environment for running static analysis tools and code parsing)
- **PlantUML** (Generating and visualizing UML class diagrams from extracted class relationships)
- **Git** (Cloning and version control of the source repository for analysis)

## Evaluation signals

- All public classes and their documented extension mechanisms (abstract classes, interfaces) appear in the generated diagram.
- Inheritance chains are acyclic and match the static source code analysis results.
- Factory patterns and composition relationships are correctly labeled and traceable to source method/field definitions.
- The diagram is validated against source code without discrepancies in class boundaries or method signatures.
- Developer extension points (e.g., abstract methods, factory interfaces) are explicitly marked and linked to source locations.

## Limitations

- Static analysis cannot detect runtime polymorphism or dynamic class instantiation that relies on reflection or string-based lookup.
- The diagram represents the declared structure but does not capture undocumented or implicit extension patterns outside the formal OOP contract.
- Large codebases may produce diagrams too complex to render or interpret without hierarchical filtering or sub-module isolation.
- Changes to the source code after diagram generation require re-analysis and re-validation to maintain diagram accuracy.

## Evidence

- [other] CloMet class diagram extraction and validation: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
- [other] Task workflow for class diagram reconstruction: "Parse the source code using static analysis to identify all classes, modules, and their inheritance/composition relationships"
- [other] Purpose and scope of the extracted diagram: "we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend"
- [other] Extension point identification in class structures: "Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns)"
- [other] Validation requirement for diagram accuracy: "Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented"
