---
name: chemical-structure-transformation-documentation
description: Use when when you have access to source code or algorithmic documentation of a metabolite generation pipeline (such as MAGMa's job subproject) and need to understand, validate, or reconstruct the transformations that convert a parent compound into enumerated metabolite candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0225
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-transformation-documentation

## Summary

Document the algorithmic rules, fragmentation logic, and transformation workflows that convert parent chemical structures into candidate metabolites in silico. This skill extracts and systematizes the chemo-informatics transformations embedded in metabolite generation pipelines so they can be audited, reproduced, and transferred across tools.

## When to use

When you have access to source code or algorithmic documentation of a metabolite generation pipeline (such as MAGMa's job subproject) and need to understand, validate, or reconstruct the transformations that convert a parent compound into enumerated metabolite candidates. Use this skill to reverse-engineer the decision logic, fragmentation rules, molecular property filters, and isomer enumeration that control metabolite candidate generation.

## When NOT to use

- Input is a pre-computed metabolite candidate table without access to the generation source code or algorithmic rules — use this skill only when you need to audit or document HOW candidates were generated, not just to interpret results.
- The metabolite generator is a black-box commercial tool with no source code or rule export capability — this skill requires transparency into fragmentation logic and parameter tuning.
- Your goal is only to match experimental MS/MS spectra to known metabolites without reconstructing the generation pipeline — use spectral matching or database lookup skills instead.

## Inputs

- Source code repository (e.g., NLeSC/MAGMa job subproject)
- Metabolite generation module files (Python, Java, or other language)
- Algorithm documentation or chemical transformation rule specifications
- Parent chemical structure(s) in SMILES or MOL format

## Outputs

- Directed acyclic graph (DAG) or flowchart in JSON format
- Annotated transformation rule document (function mappings, parameter definitions)
- Structured enumeration of fragmentation rules and property filters
- Candidate metabolite set(s) with provenance (which rule generated each)
- Validation report comparing generated metabolites against expected chemical transformations

## How to apply

Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations. Map chemical structure fragmentation logic, molecular property computation, and in silico metabolite enumeration steps by extracting parameter definitions, conditional branches, and transformation rules. Construct a directed acyclic graph (DAG) or flowchart JSON representation that documents inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property filters), and outputs (candidate metabolite sets). Annotate each node with function names, algorithm identifiers, and key computational steps sourced from the code. The rationale is that chemo-informatics workflows are rule-driven; externalizing these rules in structured form enables validation against published chemical theory, comparison across tools, and reuse in new pipelines.

## Related tools

- **MAGMa** (In silico metabolite generation and MS annotation tool; source code target for static analysis of fragmentation and enumeration logic) — https://github.com/NLeSC/MAGMa
- **PubChem** (Source database for initial parent compounds and reference structures used to validate generated metabolite candidates)

## Evaluation signals

- The DAG or flowchart JSON is acyclic and reflects all documented transformation steps without missing intermediate nodes or data flow edges.
- Each transformation rule is traceable to a specific function, code line number, or published algorithm in the source; spot-checking rule application on a test parent structure yields the expected candidate set.
- All conditional branches (e.g., property filters, isomer pruning thresholds) are explicitly documented and parameterized; changing a parameter in the DAG reproduces the code's behavior on a held-out test case.
- Generated metabolite candidates can be reproduced by following the DAG manually (or via code) without reference to the original pipeline; output structures are valid SMILES or MOL with consistent stereochemistry.
- The documented rules are consistent with published chemo-informatics literature (e.g., loss rules match known neutral losses in mass spectrometry, fragmentation patterns follow retrosynthetic logic).

## Limitations

- Static code analysis may not fully capture implicit rules encoded in data structures or machine-learned fragmentation models; dynamic tracing or instrumentation may be needed.
- The documentation reflects the state of the code at a snapshot in time; without changelog records (noted as missing in the project), it may diverge from prior or future versions.
- Rule extraction assumes the source code is well-commented and modular; obfuscated or legacy code may require manual chemical knowledge to infer intent.
- Enumeration of all metabolite candidates can be combinatorially explosive; property filters and heuristics (e.g., max isomers per structure, maximum metabolite depth) must be documented to avoid infinite or unrealistic candidate sets.

## Evidence

- [intro] The chemo-informatics workflow includes in silico generation of metabolites: "The eMetabolomics project develops chemo-informatics based methods for metabolite identification, which includes in silico generation of metabolites as part of an integrative metabolomics data"
- [other] Static code analysis targets fragmentation logic, property computation, and enumeration steps: "Perform static code analysis on the metabolite generation modules to identify algorithm entry points, function call chains, and data transformations. Map chemical structure fragmentation logic,"
- [other] Construct a DAG representation with annotated nodes for function names and algorithm steps: "Construct a directed acyclic graph or flowchart JSON representation showing inputs (parent structures, generation rules), intermediate computations (fragmentation, isomer enumeration, property"
- [readme] MAGMa is the primary tool for MS annotation based on in silico generated metabolites: "MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'."
- [readme] The job subproject runs MAGMa calculations and is the target for source analysis: "Subprojects: - emetabolomics_site - The http://www.emetabolomics.org website - job - Runs MAGMa calculation"
