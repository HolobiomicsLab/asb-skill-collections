# SciTask Card: Reconstruct the MAGMa subproject component registry from the repository README

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:32:39.548179+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_magma/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `information-extraction`, `data-processing`
- GitHub: `NLeSC/MAGMa`
- Quality: Score 2/5 — Coherent: false, placeholder, 3 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `in-silico-fragmentation`, `metabolite-identification`, `database-annotation`, `spectral-library-matching`

## Research Question
What are the named subproject components that comprise the MAGMa system architecture, and what are their designated roles?

## Connected Finding
The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and magmaweb (results interface).

## Task Description
Parse the MAGMa GitHub repository to extract and catalog the named subproject components (emetabolomics_site, job, joblauncher, pubchem, magmaweb), producing a structured manifest that lists each component's name, functional role, and source file path.

## Inputs
- NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa)

## Expected Outputs
- Structured manifest file (JSON or CSV) listing component name, functional role, and source path for each identified subproject

## Artifact References

### Inputs

- `NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa)` → **github** `NLeSC/MAGMa` (score 0.3333)

## Expected Output File

- `magma_components_manifest.json`

## Landmark Outputs

- `repository_tree.txt`
- `component_readme_excerpts.txt`
- `magma_components_manifest.json`

## Tools
- MAGMa

## Skills
- repository-structure-parsing
- software-component-identification
- metadata-extraction-from-source-code
- documentation-mining-for-project-architecture
- structured-inventory-compilation

## Workflow Description
1. Clone or access the NLeSC/MAGMa GitHub repository at https://github.com/NLeSC/MAGMa. 2. Scan the repository root and subdirectories for README, setup.py, or configuration files that document subproject structure. 3. Identify named components (emetabolomics_site, job, joblauncher, pubchem, magmaweb) and extract their directory paths and functional descriptions. 4. Cross-reference component names with inline documentation or module docstrings to infer or confirm each component's role in the metabolite annotation workflow. 5. Compile findings into a structured manifest (JSON or CSV) containing component name, inferred role, and source path.

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
- No changelog documentation found in the discussion section; README parsing will not uncover version history or component evolution timeline
- The provided section text contains only metadata (source reference and synthesis timestamp) with no actual README content; the full README.md from github:NLeSC__MAGMa must be retrieved to perform component extraction

## Domain Knowledge
- MAGMa is a chemo-informatics framework for metabolite identification and biochemical network reconstruction in metabolomics workflows, composed of multiple modular subprojects.
- Component emetabolomics_site likely serves as the web interface or frontend; job and joblauncher handle workflow task submission and execution; pubchem interfaces with the PubChem chemical database; magmaweb integrates the web platform.
- GitHub repository structure conventions: subprojects are typically organized as directories with their own setup.py, __init__.py, or README files that document their function and dependencies.
- Source path extraction requires inspection of directory hierarchy and import statements to distinguish between top-level packages, submodules, and external dependencies.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What are the named subproject components that comprise the MAGMa system architecture, and what are their designated roles?: 'Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processin'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and magmaweb (results interface).: 'Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processin'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] NLeSC/MAGMa GitHub repository (https://github.com/NLeSC/MAGMa): 'To contribute contact me via Github issue or pull request at https://github.com/NLeSC/MAGMa'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Structured manifest file (JSON or CSV) listing component name, functional role, and source path for each identified subproject: 'To contribute contact me via Github issue or pull request at https://github.com/NLeSC/MAGMa'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] MAGMa: 'MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documentation found in the discussion section; README parsing will not uncover version history or component evolution timeline: '_No changelog found._'
- `ev_007` from `agent2_synthesis` (agent2_traced): [discussion] The provided section text contains only metadata (source reference and synthesis timestamp) with no actual README content; the full README.md from github:NLeSC__MAGMa must be retrieved to perform component extraction: 'Source: github:NLeSC__MAGMa'

## Evaluation Strategy
### Direct Checks
- file_exists: README.md or equivalent documentation in github:NLeSC__MAGMa repository root
- contains_substring: README text includes at least one of the named components ('emetabolomics_site', 'job', 'joblauncher', 'pubchem', 'magmaweb')
- format_is: output manifest is a valid JSON or YAML structured record with fields 'name', 'role', and 'source_path' for each component entry
- row_count_equals: output manifest lists exactly 5 components (or documents if fewer are actually present in README with explicit naming)

### Expert Review
- Verify that extracted component roles and source paths accurately reflect the documented responsibilities and locations stated in the README (requires domain knowledge of MAGMa architecture)
- Assess whether any components are missing from the manifest despite being named and described in the README (completeness check)

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Access the NLeSC/MAGMa GitHub repository via provided URL.
2. Enumerate and locate named subproject directories and configuration files (emetabolomics_site, job, joblauncher, pubchem, magmaweb).
3. Extract functional role and source path for each component via documentation scanning and code inspection.
4. Compile structured manifest cataloging component name, role, and path.
5. Validation: manifest file exists, contains all five named components, each with a non-empty name, role description, and file path entry.

## Workflow Ports

**Inputs:**

- `magma_repo_url` — NLeSC/MAGMa GitHub repository

**Outputs:**

- `component_manifest` — Structured manifest of MAGMa subproject components

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:NLeSC__MAGMa`
- **Synthesized at:** 2026-06-16T07:36:47+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (3):
  - Finding claims 'magmaweb (results interface)' but evidence_span is truncated at 'pubchem - Processin' and does not contain magmaweb description
  - Evidence span is incomplete/truncated—cuts off mid-word at 'Processin', suggesting the actual source text was not fully captured
  - Finding asserts five components but evidence only explicitly documents four (emetabolomics_site, job, joblauncher, pubchem); magmaweb is inferred/added without grounding evidence
- Notes: The card exhibits significant quality issues. (1) The evidence_span is truncated mid-word ('Processin'), preventing verification of the complete subproject list. (2) The finding includes 'magmaweb' without corresponding evidence in the truncated span, violating groundedness. (3) The task explicitly requires extraction of source file paths for each component (per task_description: 'source file path' and expected_outputs: 'source path'), but neither the research_question nor finding address paths—creating a semantic gap between task intent and card execution. (4) The card presents findings as a prose statement rather than the expected structured manifest artifact (magma_components_manifest.json). (5) The task workflow is detailed and well-scoped, but the card's research_question and finding do not fully operationalize it. Recommend: (a) re-capture complete evidence_span without truncation, (b) verify magmaweb presence in source or remove from finding, (c) extend finding to include source paths, (d) restructure output as JSON manifest matching expected_artifact_name and evaluation criteria.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
