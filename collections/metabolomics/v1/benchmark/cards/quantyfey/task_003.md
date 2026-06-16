# SciTask Card: Extend QuantyFey's Shiny interface to support Linux/macOS deployment

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:58:43.515508+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_quantyfey/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `information-extraction`
- GitHub: `CDLMarkus/QuantyFey`
- Quality: Score 2/5 — Coherent: false, placeholder, 9 grounding failures

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
What platform-specific dependencies currently prevent QuantyFey from running on Linux or macOS?

## Connected Finding
QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved to enable cross-platform compatibility.

## Task Description
Identify and resolve platform-specific dependencies in the QuantyFey Shiny application to enable cross-platform execution on Linux or macOS. Produce a modified app configuration and dependency resolution report documenting required changes.

## Inputs
- QuantyFey source code repository (CDLMarkus/QuantyFey)

## Expected Outputs
- Modified Shiny application configuration files with platform-agnostic code
- Platform dependency resolution and compatibility report
- Test log confirming successful application launch on Linux or macOS

## Artifact References

### Inputs

- `QuantyFey source code repository (CDLMarkus/QuantyFey)` → **github** `CDLMarkus/QuantyFey` (score 0.4)

## Expected Output File

- `compatibility_report.md`

## Landmark Outputs

- `dependency_audit.txt`
- `platform_incompatibilities.csv`
- `modified_app.R`
- `test_log_linux.txt`

## Tools
- Shiny

## Skills
- shiny-application-cross-platform-adaptation
- r-dependency-package-compatibility-auditing
- platform-specific-code-refactoring
- file-path-abstraction-and-normalization
- system-library-dependency-mapping

## Workflow Description
1. Audit the QuantyFey Shiny application codebase (from CDLMarkus/QuantyFey repository) to identify Windows-only dependencies, file path conventions, and system calls. 2. Scan for platform-specific R package requirements, system libraries, and conditional code branches using static analysis. 3. Document all identified platform incompatibilities with severity and suggested alternatives (e.g., replace Windows path separators with platform-agnostic file.path() calls, identify unavailable packages). 4. Modify configuration files (app.R, global.R, or environment specifications) to abstract platform detection and implement cross-platform fallbacks. 5. Test the modified application launch on a Linux or macOS environment to verify successful initialization and basic functionality. 6. Generate a platform compatibility report listing all changes, conditional imports, and any remaining OS-specific constraints.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/compound_quantification_IS.png` | figure | False |
| `figures/compound_quantification_accuracy.png` | figure | False |
| `figures/compound_quantification_bracketing_table.png` | figure | False |
| `figures/compound_quantification_drift_correction.png` | figure | False |
| `figures/compound_quantification_model_diagnostics.png` | figure | False |
| `figures/compound_quantification_parameters.png` | figure | False |
| `figures/compound_quantification_quantification_parameters.png` | figure | False |
| `figures/compound_quantification_quantification_plot.png` | figure | False |
| `figures/compound_quantification_visualization.png` | figure | False |
| `figures/concentration_template.png` | figure | False |
| `figures/configure_settings_output.png` | figure | False |
| `figures/data_upload_parameters.png` | figure | False |
| `figures/example1_RT.png` | figure | False |
| `figures/example1_areas.png` | figure | False |
| `figures/flowchart.png` | figure | False |
| `figures/graphical_abstract.png` | figure | False |
| `figures/icon.png` | figure | False |
| `figures/model_diagnostics_HisRes.png` | figure | False |
| `figures/model_diagnostics_QQ.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- QuantyFey is a Windows-only Shiny application designed to address intensity drifts in mass spectrometry datasets using multiple correction strategies.
- Cross-platform R/Shiny development requires abstracting OS-specific file paths (backslash vs. forward slash), conditionally loading system libraries, and testing package availability across distributions.
- Linux and macOS differ in library installation paths, system package managers (apt, brew), and availability of Windows-specific R packages; conditional logic must handle all three platforms.
- Shiny applications depend on system-level dependencies for data I/O, rendering, and external tool invocation; missing system libraries cause silent failures at runtime rather than installation time.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Shiny, Modified Shiny application configuration files with platform-agnostic code, Platform dependency resolution and compatibility report, Test log confirming successful application launch on Linux or macOS.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What platform-specific dependencies currently prevent QuantyFey from running on Linux or macOS?: 'QuantyFey is compatible with Windows operating systems only.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] QuantyFey is currently restricted to Windows operating systems, indicating the presence of unidentified platform-specific dependencies that must be resolved to enable cross-platform compatibility.: 'QuantyFey is compatible with Windows operating systems only.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] QuantyFey source code repository (CDLMarkus/QuantyFey): 'CDLMarkus/QuantyFey'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Modified Shiny application configuration files with platform-agnostic code: 'producing a modified app configuration that launches successfully on a non-Windows OS'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Platform dependency resolution and compatibility report: 'identifying and resolving platform-specific dependencies'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Test log confirming successful application launch on Linux or macOS: 'launches successfully on a non-Windows OS'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Shiny: 'QuantyFey is a Shiny application for the visualization, analysis, and quantification of mass spectrometry (MS) data'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: modified app configuration file (e.g., app.R, ui.R, server.R, or shiny.yaml) in the output artifact
- verify file_format_is: configuration file is valid R syntax or YAML, script_runs without parse errors
- verify script_runs: modified Shiny application launches successfully on Linux or macOS without dependency resolution errors
- verify contains_substring: documentation or configuration identifies at least one platform-specific dependency that was modified or resolved
- verify output_matches_reference: launched application displays the same core UI and data visualization components as the Windows baseline (robust to minor rendering differences across platforms)

### Expert Review
- assess whether all identified platform-specific dependencies (e.g., file paths, system calls, graphics libraries, R package binaries) have been correctly diagnosed and addressed for Linux/macOS compatibility
- evaluate whether the modified configuration preserves the original application's intended functionality for intensity drift correction and mass spectrometry quantification workflows
- review whether the cross-platform solution is maintainable and whether configuration changes are properly documented for future deployment

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Retrieve and parse the QuantyFey source code from the CDLMarkus/QuantyFey repository.
2. Perform static code analysis to identify Windows-only dependencies, hard-coded file paths, and platform-conditional logic.
3. Document all identified incompatibilities with OS context and severity level.
4. Refactor configuration and application code to use platform-agnostic patterns (file.path, Sys.info(), conditional package loading).
5. Validation: Modified application launches without errors on a Linux or macOS test environment and produces a compatibility report with zero unresolved critical dependencies.

## Workflow Ports

**Inputs:**

- `source_repo` — QuantyFey source code repository

**Outputs:**

- `modified_config` — Modified Shiny application configuration
- `compatibility_report` — Platform dependency and compatibility report
- `test_log` — Application launch test log

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:CDLMarkus__QuantyFey`
- **Synthesized at:** 2026-06-15T14:01:28+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (9):
  - research_question: evidence_span not found in section 'intro' (value='What platform-specific dependencies currently prevent Quanty', span='QuantyFey is compatible with Windows operating systems only.')
  - finding: evidence_span not found in section 'intro' (value='QuantyFey is currently restricted to Windows operating syste', span='QuantyFey is compatible with Windows operating systems only.')
  - inputs[0]: evidence_span not found in section 'other' (value='QuantyFey source code repository (CDLMarkus/QuantyFey)', span='CDLMarkus/QuantyFey')
  - expected_outputs[0]: evidence_span not found in section 'other' (value='Modified Shiny application configuration files with platform', span='producing a modified app configuration that launches success')
  - expected_outputs[1]: evidence_span not found in section 'other' (value='Platform dependency resolution and compatibility report', span='identifying and resolving platform-specific dependencies')
  - expected_outputs[2]: evidence_span not found in section 'other' (value='Test log confirming successful application launch on Linux o', span='launches successfully on a non-Windows OS')
  - tools[0]: evidence_span not found in section 'intro' (value='Shiny', span='QuantyFey is a Shiny application for the visualization, anal')
  - Semantic gap: research_question asks 'what [dependencies]', but evidence_span only states Windows-only compatibility without identifying specific dependencies. The question presupposes knowledge of dependencies not provided by the evidence.
  - Semantic gap: finding claims 'unidentified platform-specific dependencies,' which is logically inconsistent with the research_question's ask to identify them. This suggests the finding is speculative rather than grounded.
- Notes: This card conflates three distinct tasks: (1) identifying Windows-specific dependencies, (2) resolving them, and (3) validating cross-platform execution. The research_question implies the dependencies are unknown, but the task_objective assumes they are identifiable through code audit. The finding pre-declares dependencies as 'unidentified,' making it unfalsifiable. All groundedness failures stem from truncated or absent evidence_spans and lack of source document context. The card would benefit from: (a) a concrete evidence section documenting at least one known Windows-specific dependency (e.g., 'uses hardcoded C:\ paths'), (b) separation of discovery from remediation phases, (c) explicit input artifact references (e.g., GitHub URL, commit hash), and (d) objective test success criteria (e.g., 'app launches and loads sample data in <5s on Ubuntu 22.04').

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
