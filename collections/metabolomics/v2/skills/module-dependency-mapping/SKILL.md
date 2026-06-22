---
name: module-dependency-mapping
description: Use when you need to understand or document the structural organization of an object-oriented codebase—specifically when developers require a map of which modules depend on others, where extension points (abstract classes, interfaces, factory patterns) exist, or when preparing to extend or refactor.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - Git
  - PlantUML
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
---

# Module-Dependency Mapping

## Summary

Extract and visualize the class hierarchy, inheritance relationships, and composition structure of an object-oriented software project to identify extension points and module boundaries. This skill enables developers to navigate modular codebases and locate specific classes or abstract interfaces for improvement or extension.

## When to use

Apply this skill when you need to understand or document the structural organization of an object-oriented codebase—specifically when developers require a map of which modules depend on others, where extension points (abstract classes, interfaces, factory patterns) exist, or when preparing to extend or refactor specific subsystems. Use it to validate that a software project adheres to modular object-oriented design principles and to identify the entry points for adding new functionality.

## When NOT to use

- Input is a non-object-oriented or procedural codebase without clear class structures or inheritance hierarchies.
- The goal is to analyze runtime behavior or data flow rather than static structural relationships.
- You need to track dynamic plugin loading or runtime type resolution that is not statically analyzable.

## Inputs

- Git repository URL (object-oriented Python, Java, or similar language)
- Source code directory tree with class and module definitions
- Project documentation or design specifications (optional)

## Outputs

- Structured class diagram in PlantUML or graphical format
- Module dependency graph identifying composition and inheritance edges
- Annotated list of extension points (abstract classes, interfaces, factories)
- Documentation mapping public classes to their module locations

## How to apply

Clone the target repository using Git. Perform static analysis of the source code to identify all class definitions, method signatures, inheritance chains, and composition relationships. Extract module boundaries, public APIs, and extension mechanisms such as abstract classes, interfaces, and factory patterns that serve as extension points. Generate a structured class diagram (using PlantUML or equivalent format) that visualizes the module hierarchy, class relationships, and explicitly marks developer-facing extension points. Validate the resulting diagram against the source code to ensure all public classes, documented extension mechanisms, and inheritance/composition edges are represented accurately.

## Related tools

- **Docker** (Container environment for reproducible static analysis and code parsing of the target repository)
- **Git** (Version control system used to clone and retrieve the source code repository) — https://github.com/rmallol/clomet
- **PlantUML** (Diagram generation tool for rendering extracted class relationships as formal UML class diagrams)

## Evaluation signals

- All public classes and modules documented in the project are present in the generated diagram.
- Inheritance relationships and composition edges match the actual source code hierarchy without omissions or false edges.
- Extension points (abstract classes, interfaces, factory patterns) are explicitly labeled and match the source code's documented extension mechanisms.
- Diagram validation step confirms that every public class and composition/inheritance relationship in the diagram exists in the source code.
- Developers can use the diagram to correctly identify which modules to extend or improve without requiring additional source code inspection.

## Limitations

- Static analysis cannot capture dynamically loaded classes, runtime polymorphism via reflection, or plugin architectures that are not statically resolvable.
- Accuracy depends on the clarity and consistency of the source code's object-oriented structure; poorly designed or legacy procedural code may not yield meaningful diagrams.
- The extracted diagram represents the current snapshot of the codebase; it must be regenerated if significant architectural changes occur.
- Documentation of extension points relies on the presence of explicit abstract classes, interfaces, or design patterns in the source; implicit extension mechanisms may be missed.

## Evidence

- [readme] The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
- [readme] we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend: "we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend"
- [other] Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns): "Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns)"
- [other] Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points: "Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points"
- [other] Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented: "Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented"
