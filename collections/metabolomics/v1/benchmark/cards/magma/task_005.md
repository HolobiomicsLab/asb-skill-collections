# SciTask Card: Extend MAGMa to produce a Docker Compose deployment manifest for all subproject components

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:32:39.548179+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_magma/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `NLeSC/MAGMa`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 7 grounding failures

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `in-silico-fragmentation`, `metabolite-identification`, `database-annotation`, `spectral-library-matching`

## Research Question
What are the distinct architectural components of the MAGMa system that need to be containerized and orchestrated as separate microservices?

## Connected Finding
The MAGMa project is organized into four distinct subprojects: emetabolomics_site (website), job (calculation engine), joblauncher (webservice), and pubchem (data processing), which can be deployed as separate containerized services.

## Task Description
Create a docker-compose.yml configuration file that orchestrates the MAGMa metabolomics platform as separately runnable Docker services (magmaweb, joblauncher, job, and pubchem components), enabling containerized deployment of the full annotation pipeline.

## Inputs
- NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa) containing Dockerfiles, service configurations, and deployment documentation
- MAGMa README with Docker-ready badge and subproject component list documenting magmaweb, joblauncher, job, and pubchem services

## Expected Outputs
- docker-compose.yml file defining four services (magmaweb, joblauncher, job, pubchem) with networks, volumes, environment variables, and service dependencies fully configured
- Service configuration documentation (README or inline comments in docker-compose.yml) describing port mappings, environment setup, and inter-service communication

## Expected Output File

- `docker-compose.yml`

## Landmark Outputs

- `Dockerfile.* (individual service Dockerfiles if not already present)`
- `docker-compose-dev.yml (development variant with volume mounts)`
- `.env.example (environment variable template)`
- `docker-compose.override.yml (local overrides)`

## Tools
- MAGMa

## Skills
- docker-compose-service-orchestration
- container-networking-configuration
- multi-service-dependency-management
- environment-variable-provisioning
- volume-mount-and-persistence-design
- service-health-check-definition

## Workflow Description
1. Parse the MAGMa GitHub repository structure and identify the four component services (magmaweb, joblauncher, job, pubchem) with their dependencies and environment requirements. 2. Extract or infer service configurations from existing Dockerfiles, build scripts, and documentation in the NLeSC/MAGMa repository. 3. Define service specifications in docker-compose.yml including image names, ports, environment variables, volume mounts, and inter-service networking. 4. Configure service interdependencies (e.g., joblauncher depends on job service, magmaweb depends on joblauncher) using depends_on and health checks. 5. Add PubChem data service with appropriate initialization and persistence configuration. 6. Validate docker-compose.yml syntax and test orchestration workflow by building and running the composed services.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ESCIENCE_logo_C_nl_small_cyanblack.png` | figure | False |
| `figures/nlesc.jpg` | figure | False |
| `figures/nmc.png` | figure | False |
| `figures/ui-bg_flat_0_aaaaaa_40x100.png` | figure | False |
| `figures/ui-bg_flat_0_eeeeee_40x100.png` | figure | False |
| `figures/ui-bg_flat_55_c0402a_40x100.png` | figure | False |
| `figures/ui-bg_flat_55_eeeeee_40x100.png` | figure | False |
| `figures/ui-bg_glass_100_f8f8f8_1x400.png` | figure | False |
| `figures/ui-bg_glass_35_dddddd_1x400.png` | figure | False |
| `figures/ui-bg_glass_60_eeeeee_1x400.png` | figure | False |
| `figures/ui-bg_inset-hard_75_999999_1x100.png` | figure | False |
| `figures/ui-bg_inset-soft_50_c9c9c9_1x100.png` | figure | False |
| `figures/ui-icons_3383bb_256x240.png` | figure | False |
| `figures/ui-icons_454545_256x240.png` | figure | False |
| `figures/ui-icons_70b2e1_256x240.png` | figure | False |
| `figures/ui-icons_999999_256x240.png` | figure | False |
| `figures/ui-icons_fbc856_256x240.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found
- README does not explicitly document the Docker-ready badge location, subproject list structure, or architectural relationships among magmaweb, joblauncher, job, and pubchem components

## Domain Knowledge
- Docker Compose syntax requires explicit service definitions with image, ports, environment, volumes, and depends_on keys to orchestrate multi-container applications.
- Inter-service communication in Docker Compose uses the service name as hostname; joblauncher must resolve the job service and magmaweb must resolve joblauncher via container networking.
- PubChem data service requires persistent volume configuration to avoid re-downloading chemical structure database on every container restart.
- Health checks (healthcheck directive) should be defined for services that have startup delays to prevent dependent services from attempting connections too early.
- Environment variable inheritance and network isolation in docker-compose require explicit definition of external ports (host:container) and internal service networking (bridge or custom networks).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What are the distinct architectural components of the MAGMa system that need to be containerized and orchestrated as separate microservices?: 'Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processin'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The MAGMa project is organized into four distinct subprojects: emetabolomics_site (website), job (calculation engine), joblauncher (webservice), and pubchem (data processing), which can be deployed as separate containerized services.: 'Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processin'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa) containing Dockerfiles, service configurations, and deployment documentation: 'To contribute contact me via Github issue or pull request at https://github.com/NLeSC/MAGMa'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] MAGMa README with Docker-ready badge and subproject component list documenting magmaweb, joblauncher, job, and pubchem services: 'https://travis-ci.org/NLeSC/MAGMa'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] docker-compose.yml file defining four services (magmaweb, joblauncher, job, pubchem) with networks, volumes, environment variables, and service dependencies fully configured: 'To contribute contact me via Github issue or pull request at https://github.com/NLeSC/MAGMa'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Service configuration documentation (README or inline comments in docker-compose.yml) describing port mappings, environment setup, and inter-service communication: 'The project develops chemo-informatics based methods for metabolite identification'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] MAGMa: 'MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites''
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] README does not explicitly document the Docker-ready badge location, subproject list structure, or architectural relationships among magmaweb, joblauncher, job, and pubchem components: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file docker-compose.yml exists in expected_outputs[0]
- file_format_is docker-compose.yml text/yaml or application/x-yaml
- contains_substring 'magmaweb' in docker-compose.yml
- contains_substring 'joblauncher' in docker-compose.yml
- contains_substring 'job' in docker-compose.yml (as a service name distinct from joblauncher)
- contains_substring 'pubchem' in docker-compose.yml
- contains_substring 'services:' in docker-compose.yml
- script_runs docker-compose config -f docker-compose.yml without errors (validates YAML syntax and service definitions)

### Expert Review
- expert_review: verify that docker-compose.yml service definitions correctly reflect component responsibilities (magmaweb=web interface, joblauncher=job queue manager, job=compute worker, pubchem=data source) as implied by NLeSC/MAGMa architecture
- expert_review: assess whether inter-service networking (environment variables, ports, volumes) enables the expected data flow among four components; no canonical answer without MAGMa deployment documentation
- expert_review: assess whether the composition extends or decomposes the single deployable artifact mentioned in scope in a chemically/informatically sensible way

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Scan NLeSC/MAGMa repository for existing Dockerfiles, build configuration, and service architecture documentation.
2. Identify the four service components (magmaweb, joblauncher, job, pubchem) and their runtime dependencies.
3. Extract port bindings, environment variables, and data volume requirements from existing build artifacts and documentation.
4. Author docker-compose.yml with service definitions, networks, volume bindings, and dependency ordering.
5. Validate docker-compose syntax and test multi-service startup workflow.
6. Validation: docker-compose config returns no errors, all four services can be started with docker-compose up, and inter-service networking is verified via service health checks.

## Workflow Ports

**Inputs:**

- `magma_repo` — NLeSC/MAGMa GitHub repository with Dockerfiles and service configs ← `task_001/component_manifest`

**Outputs:**

- `docker_compose` — docker-compose.yml orchestration file
- `service_docs` — Service configuration documentation

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:NLeSC__MAGMa`
- **Synthesized at:** 2026-06-16T07:37:05+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (7):
  - research_question asks about 'distinct architectural components that need to be containerized' but evidence_span only lists subproject names without explaining containerization needs or architectural relationships
  - finding claims four components 'can be deployed as separate containerized services' but source text provides no evidence about containerization feasibility or design intent
  - finding infers architectural purpose ('website', 'calculation engine', 'webservice', 'data processing') from brief descriptions not present in evidence_span
  - evidence_span is truncated at 'pubchem - Processin' without completing the description; incomplete grounding
  - expected_outputs[1] evidence_span ('The project develops chemo-informatics based methods for metabolite identification') does not ground the claim about 'port mappings, environment setup, and inter-service communication' documentation
  - inputs[1] evidence_span points to Travis CI link, not to README content with 'Docker-ready badge and subproject component list'
  - missing_information entry contradicts card premise: states 'README does not explicitly document the Docker-ready badge location, subproject list structure, or architectural relationships' yet the task assumes these are knowable
- Notes: This card presents a significant coherence problem. The research_question and finding ask about containerization architecture, but the evidence only provides an incomplete list of subprojects with minimal descriptions. The task then assumes these four components should be orchestrated as docker-compose services, but this is an inference/decision, not a finding from the source text. Critical issues: (1) evidence_span is truncated, making grounding incomplete; (2) the mapping between subproject names (emetabolomics_site, job, joblauncher, pubchem) and service names in task (magmaweb, joblauncher, job, pubchem) is inconsistent and unexplained; (3) the missing_information section contradicts the task premise by noting architectural documentation is absent; (4) the task asks for a deterministic docker-compose.yml but expert_review admits no canonical answer exists without deployment docs; (5) skills and domain_knowledge are generic Docker patterns, not MAGMa-specific insights. The card conflates a task objective (create docker-compose.yml for MAGMa) with claimed findings about MAGMa's architecture. This should be restructured as a design/engineering task, not a research finding extraction task. Recommend: clarify whether this is (a) a finding extraction card from MAGMa documentation (requires complete, grounded evidence) or (b) an engineering design card (should not claim to be grounded in source text).

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
