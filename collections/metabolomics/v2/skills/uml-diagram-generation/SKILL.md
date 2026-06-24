---
name: uml-diagram-generation
description: Use when when you have access to a modular object-oriented codebase and
  need to map its class hierarchy, composition relationships, and extension mechanisms
  (abstract classes, interfaces, factory patterns) in order to guide developers toward
  specific modules to improve or extend.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3362
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Docker
  - Git
  - PlantUML
  license_tier: open
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

# UML Diagram Generation

## Summary

Extract class structures, inheritance relationships, and module boundaries from object-oriented source code and generate a visual UML class diagram that identifies extension points for developers. This skill enables navigation of modular software architecture and facilitates targeted extension or improvement of specific components.

## When to use

When you have access to a modular object-oriented codebase and need to map its class hierarchy, composition relationships, and extension mechanisms (abstract classes, interfaces, factory patterns) in order to guide developers toward specific modules to improve or extend. Particularly applicable when the software is designed to be extended by a developer community.

## When NOT to use

- Input is a procedural or functional codebase without clear class hierarchies or extension-point design patterns
- The software has not been intentionally designed for modular extension by external developers
- Source code is unavailable or too obfuscated for static analysis

## Inputs

- Git repository URL (object-oriented source code)
- Source code files (Java, Python, C++, or other OO language)
- Project documentation or README describing extension mechanisms

## Outputs

- UML class diagram (PlantUML format or equivalent)
- Structured diagram file representing module hierarchy and relationships
- Developer-facing documentation identifying extension points

## How to apply

Clone the target repository using Git and parse its source code using static analysis tools to identify all class definitions, method signatures, inheritance chains, and composition relationships. Extract module boundaries and public extension points (abstract classes, interfaces, and design patterns that enable pluggable behavior). Generate a structured diagram in PlantUML or equivalent visualization format that represents the module hierarchy, class relationships, and documented developer extension points. Validate the generated diagram against the source code to ensure all public classes and their documented extension mechanisms are represented, then publish the diagram alongside developer contribution guidance to enable targeted module improvements.

## Related tools

- **Docker** (Container environment for reproducibly installing and running static analysis and diagram generation pipelines)
- **Git** (Version control system for cloning and accessing the target repository source code)
- **PlantUML** (Diagram-as-code tool for generating structured UML class diagrams from extracted class relationships)

## Evaluation signals

- All public classes and their inheritance relationships are represented in the generated diagram
- Extension points (abstract classes, interfaces, factory patterns) are visually identified and annotated
- Diagram validates against source code: spot-check 5–10 randomly selected classes confirms method signatures and relationships match the source
- Developers can navigate from the diagram to specific modules they wish to extend, indicating correct module boundary representation
- Composition and inheritance chains are acyclic and follow documented OO design patterns

## Limitations

- Static analysis may miss or misrepresent runtime-generated classes or dynamically loaded modules
- Diagram readability degrades with very large codebases; modularity must be pre-existing in the source design
- Extension points are only discoverable if the original developers explicitly used standard OO patterns (interfaces, abstract classes); implicit extension mechanisms may be omitted
- No changelog or versioning was found for CloMet, so diagram accuracy depends on the Git commit or release version specified at extraction time

## Evidence

- [readme] The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities.: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
- [readme] we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend.: "we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend"
- [other] Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns).: "Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns)"
- [other] Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points.: "Generate a structured class diagram in PlantUML or equivalent format that visualizes the module hierarchy, class relationships, and developer extension points"
- [other] Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented.: "Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented"
