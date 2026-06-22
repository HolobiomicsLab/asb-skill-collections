---
name: chemo-informatics-workflow-reconstruction
description: Use when when you have access to the source code of a chemo-informatics tool (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3375
  tools:
  - MAGMa
  - PubChem
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

# chemo-informatics-workflow-reconstruction

## Summary

Reconstructs the algorithmic pipeline and computational logic of a chemo-informatics tool (MAGMa) by performing static code analysis on source modules to extract fragmentation rules, molecular property filters, and in silico metabolite enumeration steps. This skill is essential when you need to understand, document, or reproduce the internal chemical transformation logic of a closed or insufficiently documented metabolite generation system.

## When to use

When you have access to the source code of a chemo-informatics tool (e.g., MAGMa) and need to understand the in silico generation workflow—including fragmentation logic, isomer enumeration, and candidate filtering—in order to validate metabolite annotations, extend the pipeline, or integrate it into a larger metabolomics analysis workflow. Use this skill specifically when the original documentation is sparse or does not detail the intermediate chemical transformations and parameter thresholds.

## When NOT to use

- Input is a high-level tool documentation or user manual without access to underlying source code—use the tool's published API documentation instead.
- The goal is to apply an existing metabolite generation tool to a dataset, not to understand or reconstruct its internal logic—directly invoke the tool via its CLI or API.
- You lack programming expertise to perform static code analysis on the target language—seek domain expert assistance or rely on published algorithm papers.

## Inputs

- Source code repository (GitHub or equivalent) containing chemo-informatics calculation modules
- Parent chemical structures (molecular SMILES or InChI)
- Generation rules and parameter definitions from source code
- Fragmentation rules and molecular property computation logic

## Outputs

- Directed acyclic graph (DAG) or flowchart JSON representation of the metabolite generation pipeline
- Annotated function call chains and algorithm entry points
- Extracted parameter thresholds and conditional branching rules
- Candidate metabolite sets with computed molecular properties
- Documentation of intermediate transformations and data flow

## How to apply

Clone the source repository (e.g., NLeSC/MAGMa from GitHub) and locate the metabolite generation subproject modules. Perform static code analysis on the relevant source files to identify algorithm entry points, function call chains, and data structure transformations. Map the chemical structure fragmentation logic, molecular property computation routines, and in silico metabolite enumeration steps by tracing parameter definitions, conditional branches, and transformation rules. Construct a directed acyclic graph (DAG) or flowchart JSON representation that explicitly documents inputs (parent chemical structures, generation rules, filters), intermediate computations (fragmentation, isomer enumeration, property thresholding), and outputs (ranked candidate metabolite sets). Annotate each node with function names, algorithm identifiers (e.g., fragmentation type, property metric), and key computational steps extracted directly from the source code to ensure fidelity to the implementation.

## Related tools

- **MAGMa** (Target chemo-informatics system providing in silico metabolite generation, fragmentation, and annotation capabilities; source code subject of workflow reconstruction) — https://github.com/NLeSC/MAGMa
- **PubChem** (Chemical structure and property database used by MAGMa for mass candidate lookup and reference metabolite data)

## Evaluation signals

- The reconstructed DAG/flowchart matches the actual code execution path when traced through with a representative parent structure and generation rules.
- All parameter thresholds (e.g., fragmentation weights, isomer enumeration limits, property filters) extracted from source code are validated against their usage sites and produce identical candidate sets.
- Intermediate computational outputs (fragmentation products, enumerated isomers, filtered candidates) match reference runs of the original tool on the same input.
- All documented function names, algorithm identifiers, and conditional branches can be located and verified in the source code with line references.
- The pipeline documentation enables independent implementation or modification of the workflow without requiring the original tool's execution.

## Limitations

- Static code analysis alone cannot capture dynamic runtime behavior, optimization passes, or external library side effects that may influence metabolite enumeration.
- Reconstruction fidelity depends on code clarity, presence of comments, and absence of obfuscation; highly complex or legacy code may require iterative validation against tool execution.
- Changes to dependency libraries or language runtime versions may alter the computational behavior of extracted rules, requiring re-validation.
- No changelog documentation was found for the MAGMa repository, making it difficult to track algorithm changes across versions.

## Evidence

- [readme] The eMetabolomics project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [readme] MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.: "MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'."
- [other] Map chemical structure fragmentation logic, molecular property computation, and in silico metabolite enumeration steps.: "Map chemical structure fragmentation logic, molecular property computation, and in silico metabolite enumeration steps."
- [other] Construct a directed acyclic graph or flowchart JSON representation showing inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property filters), and outputs (candidate metabolite sets).: "Construct a directed acyclic graph or flowchart JSON representation showing inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property"
- [other] Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations.: "Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations."
