# Workflow Challenge: `coll_pairedomicsdatapla_workflow`


> A web application platform for storing and sharing paired omics data that links mass spectrometry spectra with genomic information and experimental metadata through a JSON schema-based format.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 2 reported results: A JSON schema file located at app/public/schema.json defines the required format for paired omics data projects in the platform. A JSON schema (app/public/schema.json) has been published to formally describe the required format of paired omics data projects stored in the platform. Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): The platform links MS/MS mass spectra with genome identifiers and other metadata, enabling integration of genomic information with mass spectrometry data within stored project JSON documents. The platform stores paired omics data projects using a JSON schema format (app/public/schema.json) that defines project structure, which serves as the basis for implementing field-level validation rules including URL format constraints.

## Research questions

- What is the formal specification for the structure and constraints that uploaded JSON project documents must satisfy in the Pairing Omics Data Platform?
- How does the paired-data-form platform enrich a project JSON document by linking a genome identifier to organism name information from an external registry?
- Do all project JSON documents currently deposited in the Paired Omics Data Platform conform to the published JSON Schema specification?
- How should the validation system detect and flag URL fields in project JSON documents that contain whitespace characters, which are invalid in URLs?

## Methods overview

Load the candidate JSON project document from the upload endpoint. Load the JSON Schema definition from app/public/schema.json. Apply JSON Schema validation using a conformant validator library. Collect and report validation status (pass/fail) and enumerate any schema constraint violations. Validation: the task is successful when the validation report correctly identifies all schema violations or confirms full conformance against the published schema. Load the input project JSON document and extract the genome identifier field. Query an external organism/genome registry using the extracted identifier to retrieve the standardized organism name. Merge the retrieved organism name into the project JSON document as a new or updated field. Serialize and validate the enriched JSON document for well-formedness and required field presence. Validation: Verify that the enriched JSON is well-formed, contains the original genome identifier, and has a non-empty organism name field populated from the registry. Retrieve the complete set of published project JSON documents from the Paired Omics Data Platform. Load the canonical JSON Schema from app/public/schema.json in the iomega/paired-data-form repository. Validate each project JSON document against the schema, recording conformance status and any violations. Generate a structured validation report listing project identifiers and validation outcomes. Validation: All retrieved project documents must conform to the published schema with zero schema validation errors. Load and parse the project JSON document. Identify all fields with URL type designation in the document schema. Scan each URL field for the presence of whitespace characters (spaces, tabs, newlines, etc.). Record and report all URLs containing whitespace with their field locations. Validation: accept output if all URL fields in the document have been scanned and all whitespace-containing URLs are flagged.

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The platform links MS/MS mass spectra with genome, sample preparation, extraction method and instrumentation method.
- **(finding)** The platform links biosynthetic gene clusters with MS/MS mass spectra.
- **(finding)** The Pairing Omics Data Platform is a web application for storing paired omics data projects. _[grounded: sys-paired-omics-platform]_
- **(finding)** A JSON schema file located at app/public/schema.json describes the format of a project. _[grounded: comp-json-schema]_
- **(finding)** Users can contribute projects to the platform by submitting them at https://pairedomicsdata.bioinformatics.nl/add.
- **(finding)** After project submission, the project will be reviewed and if approved will appear in the list of projects.
- **(finding)** Each project page on the platform has a download button that provides the JSON document of the project.
- **(finding)** A developer manual is available at manuals/developers.md for programmatic access to the platform.
- **(finding)** Contributors should announce their plan to the community before starting to work on code changes.
- **(finding)** Contributors should wait until consensus is reached about their idea before proceeding with implementation.
- **(finding)** Development environment setup requires following instructions in api/README.md and app/README.md.
- **(finding)** Contributors must run npm test in the api/ and/or app/ directory to ensure existing tests still work.
- **(finding)** Version 0.2.0 was released on 2019-07-05.
- **(finding)** Version 0.1.0 was released on 2019-05-01 as the initial release.
- **(finding)** Version 0.2.0 added an intro page.
- **(finding)** Version 0.2.0 added a password protected review section to review pending projects.
- **(finding)** Version 0.2.0 added a page with a list of projects.
- **(finding)** Version 0.2.0 added a page to show single projects.
- **(finding)** Version 0.2.0 added a web service to store projects on disk as JSON documents. _[grounded: comp-api]_
- **(finding)** Version 0.2.0 added a task queue to enrich projects. _[grounded: comp-task-queue]_
- **(finding)** Version 0.2.0 added functionality to enrich projects by fetching organism name based on genome identifier.
- **(finding)** In version 0.2.0, the original form became for adding a project for review.
- **(finding)** Version 0.2.0 added metabolights study id to genome.
- **(finding)** Version 0.2.0 made which fields are required more clear.
- **(finding)** Version 0.2.0 replaced the run command from yarn to docker-compose. _[grounded: tool-docker-compose]_
- **(finding)** The platform validates labels when selected in links sections.
- **(finding)** The platform validates uploaded JSON documents.
- **(finding)** A GNPS task id link was broken and fixed. _[grounded: tool-gnps]_

## Steps

### Step `task_001`
- Title: Reproduce the JSON schema validation of uploaded project documents
- Task kind: `reproduction`
- Task: Validate an uploaded JSON project document against the published JSON Schema (app/public/schema.json) and report validation pass/fail status with any schema violation errors.
- Inputs:
  - Candidate JSON project document from user upload
  - JSON Schema definition file (app/public/schema.json)
- Expected outputs:
  - Validation report (JSON) containing pass/fail status and list of schema violation errors (if any)
- Tools: npm
- Landmark output files: schema_definition_loaded.json, validation_report.json
- Primary expected artifact: `validation_report.json`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the task-queue project enrichment step that fetches organism names from genome identifiers
- Task kind: `component_reconstruction`
- Task: Given a project JSON document containing a genome identifier, enrich it by fetching the corresponding organism name from an external genome registry and return the augmented project JSON with the organism name field populated.
- Inputs:
  - Project JSON document with genome identifier field
- Expected outputs:
  - Enriched project JSON document with organism name populated from external registry
- Tools: npm
- Landmark output files: parsed_genome_id.txt, registry_query_result.json, enriched_project.json
- Primary expected artifact: `enriched_project.json`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the published project listing from the live Paired Omics Data platform
- Task kind: `reproduction`
- Task: Retrieve all current project JSON documents from the Paired Omics Data Platform (https://pairedomicsdata.bioinformatics.nl/projects) and validate each document against the published JSON Schema (app/public/schema.json) to ensure structural conformance.
- Inputs:
  - Published project JSON documents from Paired Omics Data Platform (https://pairedomicsdata.bioinformatics.nl/projects)
  - JSON Schema definition file (app/public/schema.json)
- Expected outputs:
  - Validation report (CSV or JSON) listing each project identifier, validation status (pass/fail), and any schema violations
- Tools: npm
- Landmark output files: project_ids.txt, validation_report.csv, failed_validations.json
- Primary expected artifact: `validation_report.csv`

### Step `task_004`
- Depends on: `task_002`
- Title: Implement URL-space validation for project JSON fields to detect embedded spaces
- Task kind: `component_reconstruction`
- Task: Implement a validation rule that scans all URL-typed fields in a project JSON document and flags any value containing whitespace characters, enforcing the constraint that URLs must not include spaces.
- Inputs:
  - Project JSON document with URL-typed fields
- Expected outputs:
  - Validation report listing all URL fields containing whitespace, with field names and flagged values
- Tools: npm
- Landmark output files: url_fields_schema.json, flagged_urls.csv
- Primary expected artifact: `url_validation_report.json`

## Final expected outputs

- `Validation report (CSV or JSON) listing each project identifier, validation status (pass/fail), and any schema violations` (type: file, tolerance: hash)
- `Validation report listing all URL fields containing whitespace, with field names and flagged values` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** event_driven

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
  "workflow_id": "coll_pairedomicsdatapla_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    },
    "task_004": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Validation report (CSV or JSON) listing each project identifier, validation status (pass/fail), and any schema violations": "<locator>",
    "Validation report listing all URL fields containing whitespace, with field names and flagged values": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
