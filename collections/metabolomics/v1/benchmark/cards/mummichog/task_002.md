# SciTask Card: Extend Mummichog 3 to incorporate the metabolomics-cloud GitHub organization project structure

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-16T06:18:21.859677+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mummichog/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `metabolomics-cloud/mummichog`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 6 grounding failures

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `pathway-analysis`, `database-annotation`, `metabolite-identification`

## Research Question
Has the Mummichog 3 codebase been successfully relocated to the metabolomics-cloud GitHub organization and verified to install and function correctly in its new location?

## Connected Finding
The Mummichog project has been moved to the new metabolomics-cloud GitHub organization, but the provided documentation does not contain verification that the relocated package installs and runs correctly from its new home.

## Task Description
Migrate the Mummichog 3 codebase to the metabolomics-cloud GitHub organization, ensure compliance with organization conventions, and verify that the relocated package installs and executes correctly from its new repository location.

## Inputs
- Current Mummichog 3 repository source code and configuration files (setup.py, pyproject.toml, requirements.txt, CI/CD workflows, README, documentation)
- metabolomics-cloud organization repository standards and contribution guidelines
- Representative metabolomics feature table(s) for functional prediction testing

## Expected Outputs
- Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards
- Installation verification log confirming successful pip install from the new repository location in a clean Python environment
- Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly
- Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced

## Artifact References

### Inputs

- `metabolomics-cloud organization repository standards and contribution guidelines` → **github** `metabolomics-cloud/mummichog` (score 0.25)

## Expected Output File

- `migration_report.md`

## Landmark Outputs

- `conformance_checklist.txt`
- `setup.py`
- `install.log`
- `functional_test_output.json`

## Tools
- Python

## Skills
- python-package-migration-and-refactoring
- repository-structure-standardization
- ci-cd-workflow-adaptation-to-organization-standards
- package-installation-verification-and-testing
- metabolomics-functional-prediction-workflow-validation
- documentation-and-metadata-modernization

## Workflow Description
1. Clone the current Mummichog 3 repository and audit its structure, dependencies, and configuration files (setup.py, pyproject.toml, requirements.txt, .github workflows) against metabolomics-cloud organization standards. 2. Adapt package metadata, module naming, documentation structure, and CI/CD workflows to conform to metabolomics-cloud conventions. 3. Create a new repository under metabolomics-cloud/mummichog with the migrated codebase and updated configuration. 4. Run installation tests in a clean environment using pip install to verify the package builds without errors. 5. Execute core Mummichog functionality (e.g., loading feature tables and running functional prediction workflows) to confirm runtime correctness on representative metabolomics data. 6. Validate that all tests pass and generate a migration report documenting conformance changes and verification results.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting the migration, version bumps, or breaking changes introduced by moving Mummichog to the metabolomics-cloud organization
- No reference to specific metabolomics-cloud conventions, style guides, or integration requirements that the migrated package must satisfy

## Domain Knowledge
- Mummichog predicts functional activity from feature tables by leveraging metabolic network organization without requiring metabolite identification, so migration must preserve this core capability and its API contract.
- The metabolomics-cloud organization has specific repository conventions (naming, dependency management, CI/CD patterns, documentation structure) that the migrated codebase must adopt to be considered conformant.
- Python package installation verification requires testing in a clean environment isolated from the developer's local dependencies to catch missing or incorrectly specified dependencies in setup.py or requirements.txt.
- Functional testing of metabolomics software must use realistic feature table inputs and verify that output predictions (functional modules, activities) remain consistent with the original implementation.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Python, Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards, Installation verification log confirming successful pip install from the new repository location in a clean Python environment, Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly, Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Has the Mummichog 3 codebase been successfully relocated to the metabolomics-cloud GitHub organization and verified to install and function correctly in its new location?: 'Project is moved to new organization https://github.com/metabolomics-cloud'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The Mummichog project has been moved to the new metabolomics-cloud GitHub organization, but the provided documentation does not contain verification that the relocated package installs and runs correctly from its new home.: 'Project is moved to new organization https://github.com/metabolomics-cloud, to follow examples of https://scverse.org/'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Current Mummichog 3 repository source code and configuration files (setup.py, pyproject.toml, requirements.txt, CI/CD workflows, README, documentation): 'metabolomics-cloud/mummichog'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] metabolomics-cloud organization repository standards and contribution guidelines: 'Project is moved to new organization https://github.com/metabolomics-cloud'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Representative metabolomics feature table(s) for functional prediction testing: 'Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Migrated Mummichog 3 repository at metabolomics-cloud/mummichog with updated package metadata, configuration, and documentation conforming to organization standards: 'Project is moved to new organization https://github.com/metabolomics-cloud'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Installation verification log confirming successful pip install from the new repository location in a clean Python environment: 'metabolomics-cloud/mummichog'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Functional test results demonstrating that core Mummichog workflows (feature table loading, functional activity prediction) execute correctly: 'leverages the organization of metabolic networks to predict functional activity directly from feature tables'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Migration report documenting conformance changes applied, verification test outcomes, and any breaking changes or deprecations introduced: 'metabolomics-cloud/mummichog'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting the migration, version bumps, or breaking changes introduced by moving Mummichog to the metabolomics-cloud organization: '_No changelog found._'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] No reference to specific metabolomics-cloud conventions, style guides, or integration requirements that the migrated package must satisfy: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- Verify file exists: metabolomics-cloud/mummichog repository is accessible at https://github.com/metabolomics-cloud/mummichog
- Verify file_format_is: package structure conforms to Python setuptools conventions (setup.py or pyproject.toml present)
- Script runs: execute 'pip install -e .' from repository root without errors
- Script runs: execute package's primary entry point or test suite (e.g., 'python -m mummichog --help' or equivalent) and confirm exit code 0
- File exists: verify presence of metabolomics-cloud organization conventions documentation or style guide in the repository
- Contains_substring: check that relocated package __init__.py or main module docstring identifies correct GitHub origin (metabolomics-cloud/mummichog)

### Expert Review
- Verify that migration preserves core algorithmic behavior: package still leverages metabolic network organization to predict functional activity from feature tables without requiring metabolite identification
- Confirm that code style, naming conventions, and module organization align with metabolomics-cloud organizational standards (review against any published guidelines or sister repositories)
- Assess whether any dependencies, Python version constraints, or platform-specific code required adjustment during migration and whether such changes are documented

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Audit current Mummichog 3 structure and dependencies against metabolomics-cloud standards.
2. Adapt package metadata, module structure, documentation, and CI/CD workflows to conform to organization conventions.
3. Create and populate migrated repository at metabolomics-cloud/mummichog with updated codebase.
4. Verify installation from clean environment using pip install.
5. Execute functional prediction workflows on test metabolomics data to confirm runtime correctness.
6. Validation: Installation completes without errors, all unit and integration tests pass, and functional prediction output on test data matches expected metabolic network-based predictions.

## Workflow Ports

**Inputs:**

- `source_repository` — Current Mummichog 3 codebase and configuration ← `task_001/activity_predictions`
- `org_standards` — metabolomics-cloud organization repository standards
- `test_data` — Representative metabolomics feature table for functional testing

**Outputs:**

- `migrated_repository` — Migrated Mummichog 3 repository at metabolomics-cloud/mummichog
- `install_log` — Installation verification log
- `test_results` — Functional test results
- `migration_report` — Migration report with conformance changes and verification outcomes

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li__mummichog`
- **Synthesized at:** 2026-06-16T06:20:43+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (6):
  - inputs[0]: evidence_span not found in section 'other' (value='Current Mummichog 3 repository source code and configuration', span='metabolomics-cloud/mummichog')
  - expected_outputs[1]: evidence_span not found in section 'other' (value='Installation verification log confirming successful pip inst', span='metabolomics-cloud/mummichog')
  - expected_outputs[3]: evidence_span not found in section 'other' (value='Migration report documenting conformance changes applied, ve', span='metabolomics-cloud/mummichog')
  - research_question asks about verification of installation and function ('verified to install and function correctly'), but finding explicitly states this verification is NOT in the documentation ('does not contain verification that the relocated package installs and runs correctly'). This is a semantic mismatch—the RQ asserts something as fact, while the finding negates it.
  - inputs[2]: evidence_span references 'Mummichog is a Python program...' but this describes what Mummichog does generally, not metabolomics feature table test data specifically. The span does not ground the claim that representative test data exists.
  - expected_outputs[2]: evidence_span about 'functional activity prediction' describes capability, not verification that test results will be generated or available.
- Notes: This card conflates the task objective (migrate and verify) with claimed findings (migration done, verification absent). The research_question asks 'Has [this] been successfully relocated... and verified...' but the finding states verification is NOT in the documentation. This is self-contradictory. Additionally, the groundedness failures reveal that critical inputs (source repository, test data, organization standards) and outputs (install log, migration report) lack proper evidence anchoring—they point to URL fragments or generic descriptions rather than actual source text. The task is premature for a draft card: it describes work to be done, but the finding section suggests work has been partially done (relocation confirmed) while verification remains incomplete. The card needs either (1) to be reframed as prospective/planning (research_question should ask 'How should...' not 'Has...'), or (2) to provide actual completed artifacts with proper evidence grounding. The absence of specific metabolomics-cloud conventions and changelog makes objective verification impossible.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
