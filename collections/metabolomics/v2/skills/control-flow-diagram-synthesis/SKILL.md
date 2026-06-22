---
name: control-flow-diagram-synthesis
description: Use when when you need to understand how a multi-instrument mass spectrometry platform (such as mzmine) selectively routes data to different processing pipelines based on declared input type (LC, GC, IMS, or MS Imaging).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mzmine
  - JDK 25
  - JavaFX 24
derived_from:
- doi: 10.1038/s41467-021-23953-9
  title: iimn
evidence_spans:
- mzmine is an open-source software for mass spectrometry data processing
- JDK version-25-blue
- JavaFX version-24
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iimn
    doi: 10.1038/s41467-021-23953-9
    title: iimn
  dedup_kept_from: coll_iimn
schema_version: 0.2.0
---

# control-flow-diagram-synthesis

## Summary

Synthesize control-flow diagrams and pseudocode from conditional branching logic in a source codebase to document how input data types (LC, GC, IMS, MS Imaging) are routed to distinct processing modules. This skill reconstructs dispatcher patterns, parameter checks, and fallback behavior to produce a visual or textual artifact that maps input classification to module dispatch.

## When to use

When you need to understand how a multi-instrument mass spectrometry platform (such as mzmine) selectively routes data to different processing pipelines based on declared input type (LC, GC, IMS, or MS Imaging). Apply this skill when the codebase uses conditional dispatch logic (if/switch statements or factory patterns) that is distributed across multiple files or methods and no existing architecture documentation exists.

## When NOT to use

- The codebase already has published architecture documentation, design patterns document, or UML diagrams that explicitly show module dispatch logic—extract from those instead.
- Dispatch logic is trivial (e.g., a single if-else for two data types)—a simple written summary may be more efficient than a full diagram.
- The input platform does not support multiple data types or does not use conditional dispatch—the skill is only applicable to systems with branching routing logic.

## Inputs

- Source code repository (GitHub/GitLab/local checkout)
- Main entry point or launcher file
- Data-type enum or interface definitions
- Module initialization and factory code
- Conditional dispatch logic (if/switch/strategy pattern implementations)

## Outputs

- Control-flow diagram (SVG, PNG, or text-based flowchart)
- Dispatch pseudocode or routing table
- Annotated source code excerpts showing dispatch paths
- Module-to-data-type mapping artifact (e.g., table, matrix, or JSON schema)

## How to apply

Retrieve the source repository and locate the main entry point and module initialization code. Identify the data-type declaration interface or enum that classifies input as LC, GC, IMS, or MS Imaging. Trace conditional branching (if/switch statements or factory patterns) that maps each data type to its corresponding processing module. Extract dispatch conditions, parameter checks, and fallback behavior by following the call chain. Synthesize the routing logic as a control-flow diagram (e.g., flowchart or state diagram) or pseudocode, documenting each pathway, the criteria that trigger it, and any parameter transformations or validation steps. Cross-reference with module documentation to confirm that each module is indeed designed to handle its assigned data type.

## Related tools

- **mzmine** (Target software platform whose module dispatch routing logic is reconstructed and synthesized into a control-flow diagram) — https://github.com/mzmine/mzmine
- **JDK 25** (Java compiler and runtime environment used to build, execute, and analyze mzmine source code) — http://jdk.java.net
- **JavaFX 24** (GUI framework used by mzmine for user-facing module dispatch interfaces; may contain dispatch event handlers and routing logic)

## Evaluation signals

- All declared data types (LC, GC, IMS, MS Imaging) appear as distinct pathways in the control-flow diagram with no missing branches.
- Each pathway is annotated with the specific condition (e.g., data-type enum value, parameter threshold) that triggers it.
- Each dispatch path terminates in a concrete module or module set, confirmed by cross-reference with module class definitions in the codebase.
- Fallback or error-handling behavior (e.g., unsupported data type, invalid parameters) is explicitly documented in the diagram or pseudocode.
- The synthesized diagram can be validated by tracing a sample data object through the codebase and confirming that the drawn path matches the actual code execution flow.

## Limitations

- If dispatch logic is obfuscated, uses reflection, or is scattered across multiple inheritance hierarchies, reconstruction may be incomplete or require manual code inspection.
- The diagram represents the current state of the master branch; if development is active, the diagram may become stale and require periodic refresh.
- No changelog is available for mzmine (per the article), so it may be difficult to track when dispatch logic changed or which versions support which data types.
- The skill does not validate whether the synthesized routes are correct or optimal—it only reconstructs what exists; a code review or functional test is recommended to confirm correctness.

## Evidence

- [other] Identify the data-type declaration interface or enum that classifies input as LC, GC, IMS, or MS Imaging: "Identify the data-type declaration interface or enum that classifies input as LC, GC, IMS, or MS Imaging."
- [other] Trace the conditional branching logic (if/switch statements or factory pattern) that maps each data type to its corresponding processing module: "Trace the conditional branching logic (if/switch statements or factory pattern) that maps each data type to its corresponding processing module."
- [intro] mzmine supports selective processing module dispatch across liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), and MS imaging: "mzmine supports selective processing module dispatch across liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), and MS imaging (e.g., MALDI) data types"
- [readme] mzmine is an open-source software for mass spectrometry data processing: "mzmine is an open-source software for mass spectrometry data processing"
- [other] Synthesize the routing logic as a control-flow diagram or pseudocode, documenting each pathway and the criteria that trigger it: "Synthesize the routing logic as a control-flow diagram or pseudocode, documenting each pathway and the criteria that trigger it."
