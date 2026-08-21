---
name: class-hierarchy-extraction
description: Use when you need to understand the extensibility surface of a modular
  object-oriented codebase, particularly when planning to contribute new modules,
  extend existing functionality, or onboard developers unfamiliar with the architecture.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - Git
  - PlantUML
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# class-hierarchy-extraction

## Summary

Extract and visualize the class hierarchy, inheritance relationships, and module boundaries from object-oriented source code to identify extension points and developer entry points for software enhancement. This skill enables developers to navigate modular architectures and locate abstract classes, interfaces, and factory patterns suitable for extension.

## When to use

Apply this skill when you need to understand the extensibility surface of a modular object-oriented codebase, particularly when planning to contribute new modules, extend existing functionality, or onboard developers unfamiliar with the architecture. Use it specifically when the software is designed to meet OOP standards and explicitly supports community-driven extension.

## When NOT to use

- Source code is not structured using object-oriented design principles or lacks public class definitions and interfaces.
- Software is not designed for modularity or community extension — refactoring may be required before this skill adds value.
- Input is already a pre-compiled, closed-source binary without accessible source code.

## Inputs

- Git repository URL or local source tree
- Object-oriented source code (Java, Python, C++, or similar)
- Software architecture documentation (if available)

## Outputs

- Class hierarchy diagram (PlantUML, UML, or equivalent structured format)
- Annotated extension points (abstract classes, interfaces, factory patterns)
- Module boundary map showing composition and inheritance relationships

## How to apply

Clone the target repository using Git, then perform static analysis on the source code to identify all class definitions, method signatures, inheritance chains, and composition relationships. Extract public classes, abstract base classes, interfaces, and documented extension mechanisms (factory patterns, plugin architectures, abstract methods). Generate a structured diagram in PlantUML or equivalent format that represents the module hierarchy and relationship tree, explicitly marking extension points where developers can inject custom behavior. Validate the generated diagram against the source code to ensure all public classes and their documented extension mechanisms are present and accurately represented.

## Related tools

- **Docker** (Containerized environment for running static analysis and code parsing tools without local dependency conflicts)
- **Git** (Version control for cloning and accessing the source repository)
- **PlantUML** (Diagram generation and visualization tool for rendering class hierarchies and UML relationships)

## Evaluation signals

- All public classes present in source code appear in the generated diagram without omissions
- Inheritance and composition relationships in the diagram match the actual parent-child and has-a relationships in the code
- Extension points (abstract classes, interfaces, factory patterns) are explicitly annotated and match documentation
- Module boundaries are clearly delineated, allowing developers to locate specific components for modification
- Diagram passes validation check: static analysis re-run produces identical or semantically equivalent class definitions

## Limitations

- Static analysis may miss runtime polymorphism, dynamic type loading, or reflection-based extension mechanisms not visible in source.
- Effectiveness depends on code quality and documentation; poorly documented extension points may not be identified automatically.
- Large codebases may produce visually complex diagrams that require hierarchical filtering or modularization to remain readable.
- No changelog or versioning metadata found for CloMet; diagram may not reflect evolution of extension points across releases.

## Evidence

- [readme] The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
- [readme] we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend: "we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend"
- [other] Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns): "Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns)"
- [other] Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points: "Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points"
- [other] Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented: "Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented"
