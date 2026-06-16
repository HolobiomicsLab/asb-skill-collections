# Workflow Challenge: `coll_massql_workflow`


> MassQL is a domain-specific query language designed for mass spectrometry data, inspired by SQL but incorporating mass spectrometry-centric assumptions to enable natural and precise querying across spectra and repositories.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MassQL implements a query language for mass spectrometry following four core design principles: Expressiveness to capture complex mass spectrometry patterns, Precision to exactly prescribe data discovery without ambiguity, Scalability to query from individual spectra to entire repositories, and Relatively Natural readability and writeability for mass spectrometry users. The package includes automated testing infrastructure comprising a unit test suite and a periodic package-testing workflow, both of which execute successfully as indicated by their associated CI badges in the project repository.

## Research questions

- How does the Mass Spec Query Language parser convert MassQL query strings into structured representations while satisfying the design principles of expressiveness, precision, scalability, and natural language readability?
- Does the MassQL repository's unit test suite pass successfully when executed via the test-unit.yml CI workflow?
- Does the MassQL package pass its periodic integration test suite as indicated by the test-package.yml CI workflow?

## Methods overview

Define MassQL grammar extending SQL with MS-specific constructs aligned to four design principles (Expressiveness, Precision, Scalability, Natural Language). Implement lexer to tokenize MassQL query strings into recognized tokens (SQL keywords, MS operators, literals). Implement parser (recursive descent or LALR) to construct an Abstract Syntax Tree from token stream. Validate AST against design principles: confirm unambiguous MS pattern expression, support for single-spectrum to repository-scale queries, and human readability. Validation: Parser successfully parses conformant MassQL queries without ambiguity and rejects non-conformant input with diagnostic error messages; validation report confirms alignment with all four design principles. Clone the MassQL repository from GitHub Install all required dependencies and runtime environment Execute the unit test suite via test-unit.yml CI workflow Collect and structure test results (pass/fail counts, logs, error details) Validation: All tests pass and badge state matches the reported passing condition Retrieve the published MassQL source code from the mwang87/MassQueryLanguage GitHub repository. Parse the test-package.yml CI workflow file to identify integration test targets, commands, and acceptance criteria. Execute the integration test suite in a clean environment matching the CI specification. Capture structured test results (pass/fail status, execution time, error messages) for each test case. Validation: All tests specified in test-package.yml pass without error, and the structured report documents 100% completion of the test matrix.

**Domain:** bioinformatics

**Techniques:** natural-language-processing

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Mass Spec Query Language (MassQL) is a domain specific language designed to express queries in a mass spectrometry centric fashion. _[grounded: massql_system]_
- **(finding)** MassQL is inspired by SQL but bakes in assumptions of mass spectrometry to make querying more natural for mass spectrometry users. _[grounded: massql_system]_
- **(finding)** MassQL is designed according to the principle of Expressiveness to capture complex mass spectrometry patterns that the community would like to look for. _[grounded: massql_system]_
- **(finding)** MassQL is designed according to the principle of Precision to exactly prescribe how to find data without ambiguity. _[grounded: massql_system]_
- **(finding)** MassQL is designed to be scalable for querying from one spectrum to entire repositories of data. _[grounded: massql_system]_
- **(finding)** MassQL is designed to be relatively natural and easy to read and write for mass spectrometry users. _[grounded: massql_system]_

## Steps

### Step `task_001`
- Title: Implement MassQL query parser that encodes mass-spectrometry-centric assumptions from SQL inspiration
- Task kind: `component_reconstruction`
- Task: Implement a parser for the Mass Spec Query Language (MassQL) that converts a MassQL query string into a structured Abstract Syntax Tree (AST) or JSON representation, validating conformance to the four design principles: Expressiveness, Precision, Scalability, and Natural Language readability.
- Inputs:
  - MassQL query string to be parsed (e.g., a string representing a mass spectrometry search pattern)
- Expected outputs:
  - Structured Abstract Syntax Tree (AST) or JSON representation of the parsed MassQL query
  - Parser validation report confirming adherence to Expressiveness, Precision, Scalability, and Natural Language design principles
- Tools: MassQL
- Landmark output files: grammar_specification.txt, tokenized_query.json, parsed_ast.json, validation_report.txt
- Primary expected artifact: `parsed_query.json`

### Step `task_002`
- Title: Reproduce unit-test suite pass/fail results for the MassQL package
- Task kind: `reproduction`
- Task: Execute the unit-testing CI workflow (test-unit.yml) against the MassQL repository source code and produce a structured pass/fail report confirming the test suite status.
- Inputs:
  - MassQL repository source code at github:mwang87/MassQueryLanguage
- Expected outputs:
  - Structured test execution report with pass/fail status, test suite summary, and any failure details
- Tools: MassQL
- Landmark output files: test_log.txt, test_summary.json
- Primary expected artifact: `test_report.json`

### Step `task_003`
- Title: Reproduce periodic package-testing CI workflow pass/fail results for MassQL
- Task kind: `reproduction`
- Task: Execute the MassQL package-level integration test suite (test-package.yml CI workflow) against the published repository and produce a structured pass/fail report documenting test execution status, distinct from unit test results.
- Inputs:
  - mwang87/MassQueryLanguage GitHub repository (public source)
- Expected outputs:
  - Structured pass/fail report documenting package-level integration test execution status and per-test outcomes
- Tools: MassQL
- Landmark output files: test-package.yml, test_execution.log, test_report.json
- Primary expected artifact: `test_report.json`

## Final expected outputs

- `Structured Abstract Syntax Tree (AST) or JSON representation of the parsed MassQL query` (type: file, tolerance: hash)
- `Parser validation report confirming adherence to Expressiveness, Precision, Scalability, and Natural Language design principles` (type: file, tolerance: hash)
- `Structured test execution report with pass/fail status, test suite summary, and any failure details` (type: file, tolerance: hash)
- `Structured pass/fail report documenting package-level integration test execution status and per-test outcomes` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** abstract

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_massql_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Structured Abstract Syntax Tree (AST) or JSON representation of the parsed MassQL query": "<locator>",
    "Parser validation report confirming adherence to Expressiveness, Precision, Scalability, and Natural Language design principles": "<locator>",
    "Structured test execution report with pass/fail status, test suite summary, and any failure details": "<locator>",
    "Structured pass/fail report documenting package-level integration test execution status and per-test outcomes": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
