---
name: call-graph-construction-and-visualization
description: Use when when you need to understand the computational structure of a modular scientific application (especially one with multiple subprojects or plug-in architectures) and static code inspection alone does not reveal algorithm entry points, parameter propagation, or intermediate data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_3047
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MAGMa
  - Static code analysis tools (e.g., ast module in Python, or javac for Java)
  - Graphviz or NetworkX (Python)
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
---

# call-graph-construction-and-visualization

## Summary

Extract and represent function call chains, control flow, and data transformations from scientific software source code as directed acyclic graphs or flowcharts to expose algorithm structure and identify computational entry points. This skill is essential for reverse-engineering complex chemo-informatics pipelines where static inspection of source alone is insufficient to understand metabolite generation workflows.

## When to use

When you need to understand the computational structure of a modular scientific application (especially one with multiple subprojects or plug-in architectures) and static code inspection alone does not reveal algorithm entry points, parameter propagation, or intermediate data transformations. Typical triggers: (1) you have cloned a research software repository but lack architectural documentation; (2) you need to trace how input chemical structures or generation rules flow through fragmentation, enumeration, and property-filtering stages; (3) you want to identify which functions control metabolite candidate set production and which parameters gate each stage.

## When NOT to use

- When the software has comprehensive API documentation or a published algorithmic description—consult the documentation first rather than reverse-engineering from source.
- When your goal is only to run the software on test data; if you do not need to understand algorithm internals, focus on execution and validation instead.
- When source code is obfuscated, heavily compiled, or dynamically generated at runtime; static analysis will yield incomplete or misleading graphs.

## Inputs

- GitHub repository source tree (Python, Java, or compiled modules)
- Subproject module files containing metabolite generation logic
- Function definitions, call chains, and control flow statements
- Parameter definitions and conditional branch rules
- Parent chemical structure inputs (SMILES, InChI, or molecular property sets)
- Generation rules or transformation templates (e.g., fragmentation rules, isomer enumeration bounds)

## Outputs

- Directed acyclic graph (DAG) representation (JSON, YAML, or GraphML format)
- Flowchart or call-graph visualization (PNG, SVG, or interactive HTML)
- Annotated node list mapping function names to algorithm roles and source locations
- Edge list with data types and parameter propagation paths
- Intermediate computation inventory (fragmentation steps, property filters, enumeration rules)
- Input–output type signatures for each computational stage

## How to apply

Begin by performing static code analysis on the modular source files (e.g., the `job` subproject in MAGMa) to identify all function definitions, call sites, and parameter assignments. Trace function call chains from entry points (e.g., job launcher or CLI handlers) through to outputs (e.g., metabolite candidate sets). For each step, extract the function name, algorithm identifier (if named), input types, output types, and any conditional branches or transformation rules that control behavior. Map chemical structure fragmentation logic, molecular property computation (e.g., mass, charge, polarity filters), and in silico metabolite enumeration steps explicitly. Represent the result as a directed acyclic graph (DAG) or flowchart in JSON, YAML, or GraphML format, with nodes labeled by function name and edges annotated with data type and parameter values. Annotate each node with source file location, function signature, and key computational roles. This representation becomes the executable reference for algorithm understanding and enables subsequent tasks (e.g., parameter sensitivity analysis, validation of intermediate outputs against expected chemical property distributions).

## Related tools

- **MAGMa** (Target software system whose in silico metabolite generation pipeline is reverse-engineered via call-graph construction) — https://github.com/NLeSC/MAGMa
- **Static code analysis tools (e.g., ast module in Python, or javac for Java)** (Parse and extract function definitions, call sites, and control flow from source modules)
- **Graphviz or NetworkX (Python)** (Render directed acyclic graphs and flowcharts from edge lists and node annotations)

## Evaluation signals

- Call graph is acyclic: no cycles detected in function call paths (except for intentional recursive base cases with explicit termination conditions).
- All function calls at each node resolve to defined functions in the source tree; unresolved external calls are flagged and annotated as library or API boundary crossings.
- Intermediate data types match across adjacent nodes: output type of function A equals input type of function B at every edge.
- Parameter flow is complete: all parameters required by downstream functions are supplied by upstream functions or explicitly documented as defaults.
- Chemical logic is preserved: nodes labeled as 'fragmentation' have inputs matching parent structure representations and outputs matching fragment structure sets; 'enumeration' nodes produce metabolite candidate counts consistent with input generation rules and filters.
- Call graph correctly identifies entry points (job launchers, CLI handlers) and terminal nodes (candidate set output, result serialization).

## Limitations

- Static analysis cannot resolve dynamically dispatched function calls (e.g., via reflection or plugin loaders) without runtime tracing; call graphs will be incomplete for systems with dynamic loading.
- Parameter dependencies not explicit in code (e.g., hardcoded constants in .cfg files or databases) may not appear in the call graph; cross-reference configuration files separately.
- Version-dependent behavior (e.g., different algorithms in branches) requires separate graphs per version or explicit version annotation on nodes.
- The MAGMa repository README notes no changelog documentation; historical algorithm changes are not recorded, so graphs represent only the current HEAD state.

## Evidence

- [other] Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations.: "Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations."
- [other] Construct a directed acyclic graph or flowchart JSON representation showing inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property filters), and outputs (candidate metabolite sets).: "Construct a directed acyclic graph or flowchart JSON representation showing inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property"
- [readme] The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [readme] MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.: "MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'."
- [other] Clone the NLeSC/MAGMa GitHub repository and locate the job subproject source files.: "Clone the NLeSC/MAGMa GitHub repository and locate the job subproject source files."
