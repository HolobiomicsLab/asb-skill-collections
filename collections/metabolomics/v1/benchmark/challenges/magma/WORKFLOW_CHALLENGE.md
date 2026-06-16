# Workflow Challenge: `coll_magma_workflow`


> MAGMa is a chemo-informatics platform for metabolite identification and biochemical network reconstruction, comprising five named subproject components (emetabolomics_site, job, joblauncher, pubchem, and magmaweb) with embedded CI/CD status badges for Travis CI, Landscape.io, Coveralls, Docker Hub, and Zenodo.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

The eMetabolomics project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow. MAGMa (Ms Annotation based on in silico Generated Metabolites) is the project's core system, composed of five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and magmaweb (results interface). The MAGMa joblauncher subproject functions as a webservice to execute jobs, serving as the interface for triggering MAGMa calculations. The system employs in silico generation of metabolites as part of the integrative metabolomics data analysis workflow. The MAGMa GitHub repository embeds five badge endpoints linking to live project status pages: Travis CI (build status), Landscape.io (code health), Coveralls (test coverage), Docker Hub (container readiness), and Zenodo (DOI archival). The project subcomponents can be deployed as separate containerized services.

## Research questions

- What are the named subproject components that comprise the MAGMa system architecture, and what are their designated roles?
- What are the current build, code quality, test coverage, deployment, and archival status indicators reported by the badge endpoints referenced in the MAGMa project README?
- What are the HTTP endpoints, request/response schemas, and authentication mechanisms exposed by the joblauncher webservice component in the MAGMa project?
- What is the chemo-informatics workflow that MAGMa uses to generate candidate metabolites in silico?
- What are the distinct architectural components of the MAGMa system that need to be containerized and orchestrated as separate microservices?

## Methods overview

Access the NLeSC/MAGMa GitHub repository via provided URL. Enumerate and locate named subproject directories and configuration files (emetabolomics_site, job, joblauncher, pubchem, magmaweb). Extract functional role and source path for each component via documentation scanning and code inspection. Compile structured manifest cataloging component name, role, and path. Validation: manifest file exists, contains all five named components, each with a non-empty name, role description, and file path entry. Access the MAGMa GitHub repository and retrieve the README file. Parse the README to extract all badge endpoint URLs (Travis CI, Coveralls, Landscape.io, Docker Hub, Zenodo). Query each badge endpoint and extract the current status value or metric reported. Organize results into a structured table with badge name, endpoint URL, status value, and retrieval timestamp. Validation: Verify that the output table contains at least four badge entries with non-empty status values and valid endpoint URLs. Clone the NLeSC/MAGMa repository and locate joblauncher source files. Parse HTTP route definitions and endpoint handlers to extract paths, methods, and parameter names. Analyze function signatures and type hints to infer request and response payload schemas. Map extracted metadata into OpenAPI 3.0 format with complete endpoint documentation. Validation: OpenAPI specification is structurally valid JSON/YAML and all joblauncher endpoints are present and accurately documented. Retrieve the MAGMa source repository from GitHub and navigate to the job subproject directory. Perform static analysis of Python/source files to identify metabolite generation entry points and function signatures. Trace call chains and data flow through fragmentation, enumeration, and property-filtering modules. Extract transformation logic, parameter definitions, and decision points that govern metabolite candidate generation. Construct a directed acyclic graph representation as JSON, annotating nodes with function identifiers and algorithm names. Validation: Verify that the generated flowchart covers the complete path from input parent structure to output candidate metabolite set, with all major computational steps and data dependencies explicitly documented. Scan NLeSC/MAGMa repository for existing Dockerfiles, build configuration, and service architecture documentation. Identify the four service components (magmaweb, joblauncher, job, pubchem) and their runtime dependencies. Extract port bindings, environment variables, and data volume requirements from existing build artifacts and documentation. Author docker-compose.yml with service definitions, networks, volume bindings, and dependency ordering. Validate docker-compose syntax and test multi-service startup workflow. Validation: docker-compose config returns no errors, all four services can be started with docker-compose up, and inter-service networking is verified via service health checks.

**Domain:** metabolomics

**Techniques:** in-silico-fragmentation, metabolite-identification, database-annotation, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The eMetabolomics project is funded by the Netherlands eScience Center. _[grounded: eMetabolomics_Project]_
- **(finding)** The eMetabolomics project is carried out at Wageningen University and the Netherlands eScience Center. _[grounded: eMetabolomics_Project]_
- **(finding)** The eMetabolomics project collaborates with the Netherlands Metabolomics Centre. _[grounded: eMetabolomics_Project]_
- **(finding)** The project develops chemo-informatics based methods for metabolite identification.
- **(finding)** The project develops methods for biochemical network reconstruction in an integrative metabolomics data analysis workflow.
- **(finding)** MAGMa is an abbreviation for 'Ms Annotation based on in silico Generated Metabolites'. _[grounded: MAGMa_System]_
- **(finding)** emetabolomics_site is a subproject that provides the eMetabolomics website. _[grounded: eMetabolomics_Project]_
- **(finding)** The job subproject runs MAGMa calculation. _[grounded: MAGMa_System]_
- **(finding)** The joblauncher subproject is a webservice to execute jobs. _[grounded: MAGMa_JobLauncher_Component]_
- **(finding)** Contributions to the eMetabolomics project can be made via Github issue or pull request. _[grounded: MAGMa_System]_

## Steps

### Step `task_001`
- Title: Reconstruct the MAGMa subproject component registry from the repository README
- Task kind: `component_reconstruction`
- Task: Parse the MAGMa GitHub repository to extract and catalog the named subproject components (emetabolomics_site, job, joblauncher, pubchem, magmaweb), producing a structured manifest that lists each component's name, functional role, and source file path.
- Inputs:
  - NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa)
- Expected outputs:
  - Structured manifest file (JSON or CSV) listing component name, functional role, and source path for each identified subproject
- Tools: MAGMa
- Landmark output files: repository_tree.txt, component_readme_excerpts.txt, magma_components_manifest.json
- Primary expected artifact: `magma_components_manifest.json`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the CI/CD badge status for the MAGMa GitHub repository
- Task kind: `reproduction`
- Task: Retrieve the current status values from live badge endpoints (Travis CI, Coveralls, Landscape.io, Docker Hub, Zenodo) referenced in the MAGMa GitHub repository and record them in a structured table.
- Inputs:
  - MAGMa GitHub repository URL: https://github.com/NLeSC/MAGMa
- Expected outputs:
  - Structured table (CSV or JSON) recording badge status values with columns: badge_name, endpoint_url, status_value, retrieval_timestamp
- Tools: MAGMa
- Landmark output files: readme_raw.txt, badge_urls_extracted.txt
- Primary expected artifact: `badge_status_table.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement the joblauncher webservice component interface for MAGMa job submission
- Task kind: `component_reconstruction`
- Task: Inspect the MAGMa joblauncher component source files in the NLeSC/MAGMa repository and reconstruct its HTTP API contract by extracting endpoint definitions, request/response schemas, and parameters. Produce a machine-readable OpenAPI 3.0 specification document.
- Inputs:
  - NLeSC/MAGMa repository (GitHub)
- Expected outputs:
  - OpenAPI 3.0 specification document (JSON or YAML) describing joblauncher HTTP API contract
- Tools: MAGMa
- Landmark output files: joblauncher_endpoints.txt, joblauncher_schemas.json, joblauncher_openapi.json
- Primary expected artifact: `joblauncher_openapi.json`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the in silico metabolite generation pipeline stage within MAGMa
- Task kind: `component_reconstruction`
- Task: Analyze the MAGMa repository source code to extract and document the chemo-informatics workflow that generates candidate metabolites in silico. Produce a structured flowchart or annotated call-graph JSON file describing the metabolite generation logic and data flow.
- Inputs:
  - NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa), specifically the job subproject source code
- Expected outputs:
  - Structured flowchart or annotated call-graph JSON file documenting the in silico metabolite generation workflow, including function names, transformation logic, and data flow edges
- Tools: MAGMa
- Landmark output files: function_inventory.txt, call_graph.dot, algorithm_nodes.json
- Primary expected artifact: `metabolite_generation_workflow.json`

### Step `task_005`
- Depends on: `task_001`
- Title: Extend MAGMa to produce a Docker Compose deployment manifest for all subproject components
- Task kind: `extension`
- Task: Create a docker-compose.yml configuration file that orchestrates the MAGMa metabolomics platform as separately runnable Docker services (magmaweb, joblauncher, job, and pubchem components), enabling containerized deployment of the full annotation pipeline.
- Inputs:
  - NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa) containing Dockerfiles, service configurations, and deployment documentation
  - MAGMa README with Docker-ready badge and subproject component list documenting magmaweb, joblauncher, job, and pubchem services
- Expected outputs:
  - docker-compose.yml file defining four services (magmaweb, joblauncher, job, pubchem) with networks, volumes, environment variables, and service dependencies fully configured
  - Service configuration documentation (README or inline comments in docker-compose.yml) describing port mappings, environment setup, and inter-service communication
- Tools: MAGMa
- Landmark output files: Dockerfile.* (individual service Dockerfiles if not already present), docker-compose-dev.yml (development variant with volume mounts), .env.example (environment variable template), docker-compose.override.yml (local overrides)
- Primary expected artifact: `docker-compose.yml`

## Final expected outputs

- `Structured table (CSV or JSON) recording badge status values with columns: badge_name, endpoint_url, status_value, retrieval_timestamp` (type: file, tolerance: hash)
- `OpenAPI 3.0 specification document (JSON or YAML) describing joblauncher HTTP API contract` (type: file, tolerance: hash)
- `Structured flowchart or annotated call-graph JSON file documenting the in silico metabolite generation workflow, including function names, transformation logic, and data flow edges` (type: file, tolerance: hash)
- `docker-compose.yml file defining four services (magmaweb, joblauncher, job, pubchem) with networks, volumes, environment variables, and service dependencies fully configured` (type: file, tolerance: hash)
- `Service configuration documentation (README or inline comments in docker-compose.yml) describing port mappings, environment setup, and inter-service communication` (type: file, tolerance: hash)

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
  "workflow_id": "coll_magma_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
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
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Structured table (CSV or JSON) recording badge status values with columns: badge_name, endpoint_url, status_value, retrieval_timestamp": "<locator>",
    "OpenAPI 3.0 specification document (JSON or YAML) describing joblauncher HTTP API contract": "<locator>",
    "Structured flowchart or annotated call-graph JSON file documenting the in silico metabolite generation workflow, including function names, transformation logic, and data flow edges": "<locator>",
    "docker-compose.yml file defining four services (magmaweb, joblauncher, job, pubchem) with networks, volumes, environment variables, and service dependencies fully configured": "<locator>",
    "Service configuration documentation (README or inline comments in docker-compose.yml) describing port mappings, environment setup, and inter-service communication": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
