---
name: developer-extension-point-identification
description: Use when when you need to onboard developers into a modular, object-oriented
  codebase (such as CloMet) and want to pinpoint specific classes, abstract interfaces,
  or factory patterns that serve as official extension points rather than requiring
  developers to read through entire source trees.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0081
  - http://edamontology.org/topic_2259
  tools:
  - Docker
  - PlantUML
  - Git
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

# Developer Extension Point Identification

## Summary

Extract and visualize a software project's class structure, inheritance hierarchies, and modular boundaries to identify where developers can safely extend or improve functionality without breaking the core system. This skill enables navigation of object-oriented designs that follow documented extension patterns (abstract classes, interfaces, factory patterns).

## When to use

When you need to onboard developers into a modular, object-oriented codebase (such as CloMet) and want to pinpoint specific classes, abstract interfaces, or factory patterns that serve as official extension points rather than requiring developers to read through entire source trees. Use this skill when the project README or documentation explicitly states that modularity and extensibility are design goals.

## When NOT to use

- The project is not designed for modular extension (monolithic or tightly coupled architecture) — use generic code review instead.
- Source code is not available or is obfuscated — static analysis will not work.
- The codebase lacks documented extension patterns or abstract interfaces — extension points may not exist or may be implicit and fragile.

## Inputs

- Source code repository (e.g., GitHub git URL)
- Project README or design documentation mentioning modularity goals
- Source files in standard object-oriented language (Java, Python, C++, etc.)

## Outputs

- Class diagram in PlantUML or graphical format
- Annotated list of extension points (abstract classes, interfaces, factory patterns)
- Module hierarchy map showing composition and inheritance relationships
- Developer guide or reference document identifying which classes to extend for common tasks

## How to apply

Clone the source repository and use static code analysis (parsing, not execution) to enumerate all classes, method signatures, and module boundaries. Prioritize discovery of abstract classes, interface definitions, and factory pattern implementations, as these represent intended extension points. Construct a structured class diagram (using PlantUML or equivalent) that visualizes the inheritance hierarchy, composition relationships, and module boundaries with clear labels for extension points. Validate the generated diagram against the source code to confirm all public classes and their documented extension mechanisms are represented. Document the rationale for each extension point (e.g., 'extend this abstract class to add new data harmonization strategies').

## Related tools

- **Docker** (Containerizes the CloMet environment to ensure reproducible cloning, parsing, and analysis of the source code without dependency conflicts)
- **PlantUML** (Generates and renders structured class diagrams from extracted class definitions and relationships to visualize module hierarchies and extension points)
- **Git** (Clones the CloMet repository to local disk for static analysis and source code parsing) — https://github.com/rmallol/clomet

## Evaluation signals

- Every public class, interface, and abstract class from the source code is represented in the final diagram with correct inheritance and composition links.
- All extension points (abstract classes with at least one abstract method, interfaces, and factory pattern implementations) are explicitly labeled and documented with their intended use cases.
- The diagram validates against source code: spot-check a subset of classes by comparing diagram relationships to actual source method signatures and inheritance declarations.
- Developers new to the project can identify 'where to add a new metabolomics data harmonizer' or similar task by reading the diagram without consulting the full source tree.
- No private/internal classes are included unless they are part of a documented extension path; the diagram focuses on the public API surface intended for extension.

## Limitations

- Static analysis cannot detect runtime polymorphism or dynamic extension mechanisms (e.g., plugin systems relying on reflection or configuration files) — extension points may be incomplete if the project uses these patterns.
- The quality of the diagram depends on code clarity and naming conventions; poorly documented classes or obfuscated inheritance chains will produce diagrams that do not guide extension effectively.
- Abstract base classes and interfaces alone do not guarantee they are intended extension points; confirmation against README or design docs is required to filter out internal abstractions.
- The README states 'No changelog found', so historical evolution of extension points or deprecated patterns may not be documented; developers must cross-reference with Git history if they need to understand why extension points were added or removed.

## Evidence

- [other] CloMet's class diagram was released to enable developers to navigate its modular object-oriented structure and identify specific modules for improvement or extension.: "we have released the class diagram of the software, so developers can go directly to those modules that they want to improve/extend"
- [readme] CloMet is designed with modular OOP structure as an explicit enabler for extension.: "The software has been designed in such a modular way meeting the Object Oriented Programming standards to facilitate the extension of its capabilities"
- [other] The workflow includes parsing source code to identify extension points such as abstract classes, interfaces, and factory patterns.: "Extract class definitions, method signatures, and module boundaries that represent extension points (abstract classes, interfaces, factory patterns)"
- [other] The workflow requires static analysis and diagram generation in PlantUML format.: "Parse the source code using static analysis to identify all classes, modules, and their inheritance/composition relationships"
- [other] Validation of the diagram against source code is a required quality check.: "Validate the diagram against source code to ensure all public classes and their documented extension mechanisms are represented"
