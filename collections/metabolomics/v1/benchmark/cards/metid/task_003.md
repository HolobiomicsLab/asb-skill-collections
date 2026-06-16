# SciTask Card: Extend Met-ID to register a novel derivatizing matrix beyond FMP-10

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:59:56.876471+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_metid/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `pbjarterot/Met-ID`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 8 grounding failures

## Classification

- Task kind: `extension`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `untargeted-metabolomics`
- Techniques: `metabolite-identification`, `database-annotation`, `in-silico-fragmentation`

## Research Question
Is Met-ID extensible to register and apply derivatizing matrices beyond FMP-10 to produce correct adduct annotations?

## Connected Finding
Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10 which was developed in-house.

## Task Description
Implement a configuration or plugin to register a second derivatizing matrix (e.g. TAHS) in Met-ID and verify that the system correctly recognizes and applies it to generate adduct annotations for test metabolites.

## Inputs
- Met-ID source code or installed package with extensibility interface
- Documentation or specifications for the second derivatizing matrix (e.g. TAHS reagent properties and ionization modes)
- Test metabolite dataset with known or reference adduct forms under derivatization

## Expected Outputs
- Configuration file or plugin code for the second derivatizing matrix (e.g. tahs_config.json or tahs_plugin.py)
- Adduct annotation table or report (CSV or JSON) produced by Met-ID using the newly registered matrix on test metabolites
- Verification report or summary table comparing predicted adducts to expected ground truth

## Expected Output File

- `verification_report.csv`

## Landmark Outputs

- `matrix_config.json`
- `adduct_predictions.csv`
- `verification_report.csv`

## Tools
- RDKit

## Skills
- mass-spectrometry-adduct-annotation
- derivatizing-matrix-configuration
- software-plugin-development
- metabolite-identification-validation

## Workflow Description
1. Review Met-ID's extensibility architecture and existing derivatizing matrix configuration (e.g. the documented matrix currently supported) to understand the plugin or configuration interface. 2. Create a configuration file or plugin module for the second derivatizing matrix (TAHS or similar publicly documented reagent), specifying the matrix composition, ionization behavior, and expected adduct forms. 3. Register the new matrix in Met-ID's system by integrating it into the tool's configuration loader or plugin registry. 4. Run Met-ID on a test set of metabolites (internal standards or reference compounds with known derivatization behavior) using the newly registered matrix. 5. Parse Met-ID's output and verify that adduct annotations match the expected ions produced by the second matrix (e.g. [M+matrix_adduct]+ or other characteristic forms). 6. Compare predicted adducts against ground truth or literature-reported adducts for the test metabolites to confirm correct recognition and application.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/128x128.png` | figure | False |
| `figures/128x128@2x.png` | figure | False |
| `figures/32x32.png` | figure | False |
| `figures/Square107x107Logo.png` | figure | False |
| `figures/Square142x142Logo.png` | figure | False |
| `figures/Square150x150Logo.png` | figure | False |
| `figures/Square284x284Logo.png` | figure | False |
| `figures/Square30x30Logo.png` | figure | False |
| `figures/Square310x310Logo.png` | figure | False |
| `figures/Square44x44Logo.png` | figure | False |
| `figures/Square71x71Logo.png` | figure | False |
| `figures/Square89x89Logo.png` | figure | False |
| `figures/StoreLogo.png` | figure | False |
| `figures/icon.png` | figure | False |
| `figures/metid_logo.png` | figure | False |
| `figures/tauri.svg` | figure | False |
| `figures/typescript.svg` | code | False |
| `figures/vite.svg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found
- The discussion section contains no description of Met-ID's configuration format, plugin architecture, extensibility mechanism, or documented steps for registering a new derivatizing matrix

## Domain Knowledge
- Derivatizing matrices alter the ionization pathway of metabolites, producing non-standard adducts ([M+matrix]+ or [M-H2O+matrix]+) that differ from common [M+H]+ in positive mode; proper configuration must specify the mass shift and ionization behavior associated with each matrix.
- Met-ID's extensibility design allows registration of new matrices beyond those currently implemented, enabling adaptation to custom or emerging derivatizing reagents used in mass spectrometry imaging.
- Verification of adduct annotation requires comparison against either literature-reported ion forms for known metabolites or experimentally determined masses from high-resolution MS data to confirm correct matrix recognition.
- Configuration of a new matrix typically requires specifying: matrix molecular weight, charge state, expected adduct formula (e.g. [M+matrix]+ or [M+Na+matrix]+), and ionization mode applicability (positive/negative).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Is Met-ID extensible to register and apply derivatizing matrices beyond FMP-10 to produce correct adduct annotations?: 'Met-ID is extendable to use any derivatizing ma'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10 which was developed in-house.: 'Met-ID is extendable to use any derivatizing matrix'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Met-ID source code or installed package with extensibility interface: 'github.com/pbjarterot/Met-ID'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Documentation or specifications for the second derivatizing matrix (e.g. TAHS reagent properties and ionization modes): 'any derivatizing matrix'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Test metabolite dataset with known or reference adduct forms under derivatization: 'derivatizing matrices leading to ions other than common [M+H]+ in positive mode and [M-H]- in negative mode'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Configuration file or plugin code for the second derivatizing matrix (e.g. tahs_config.json or tahs_plugin.py): 'any derivatizing matrix'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Adduct annotation table or report (CSV or JSON) produced by Met-ID using the newly registered matrix on test metabolites: 'derivatizing matrices leading to ions other than common [M+H]+'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Verification report or summary table comparing predicted adducts to expected ground truth: 'Met-ID has a particular focus on derivatizing matrices'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] RDKit: 'Powered by RDKit'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] The discussion section contains no description of Met-ID's configuration format, plugin architecture, extensibility mechanism, or documented steps for registering a new derivatizing matrix: '[Entire discussion section contains only metadata and no technical content]'

## Evaluation Strategy
### Direct Checks
- verify that Met-ID repository (github:pbjarterot/Met-ID) contains configuration or plugin code (file or directory) that defines or registers derivatizing matrices
- verify file_exists for a second derivatizing matrix configuration file (e.g. TAHS.json, tahs_config.py, or equivalent) in the repository
- verify script_runs: execute Met-ID's matrix registration or initialization code with the new matrix configuration without errors
- verify file_format_is: the new matrix configuration adheres to the documented schema used by the first (existing) derivatizing matrix in the codebase
- verify output_matches_reference: run Met-ID with the second matrix on a test metabolite and confirm the output contains adduct annotations (e.g. [M+matrix_adduct]+) distinct from the baseline matrix
- verify contains_substring: adduct annotation strings in Met-ID output include the expected ion form for the second matrix (e.g. presence of TAHS-related ion notation if TAHS is chosen)

### Expert Review
- assess whether the second derivatizing matrix is a real, publicly documented reagent with known derivatization chemistry
- evaluate whether the adduct annotations produced by Met-ID for the second matrix are chemically correct and consistent with the reagent's known reaction mechanism
- judge whether the implementation is genuinely extensible (i.e. a new user could add a third matrix following the same pattern without modifying core code)
- assess the clarity and completeness of any documentation or comments in the configuration/plugin code that enable future matrix additions

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Review Met-ID's extensibility architecture and existing derivatizing matrix configuration interface
2. Define and implement configuration for a second derivatizing matrix using specifications or documentation
3. Register the new matrix in Met-ID's configuration loader or plugin system
4. Execute Met-ID on test metabolites using the newly registered matrix
5. Validate predicted adducts against expected ground truth or literature values
6. Validation: adduct annotations produced by Met-ID with the new matrix match expected ions for ≥90% of test metabolites

## Workflow Ports

**Inputs:**

- `metid_codebase` — Met-ID source code or package ← `task_001/predicted_adducts`
- `matrix_specs` — Derivatizing matrix specifications and ionization properties
- `test_metabolites` — Test metabolite dataset with reference adduct forms

**Outputs:**

- `matrix_config` — Configuration or plugin for second derivatizing matrix
- `adduct_predictions` — Adduct annotations produced by Met-ID with new matrix
- `verification_report` — Comparison of predicted vs. expected adducts

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:pbjarterot__Met-ID`
- **Synthesized at:** 2026-06-15T14:03:13+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (8):
  - inputs[0]: evidence_span 'github.com/pbjarterot/Met-ID' not found in section 'methods'
  - inputs[1]: evidence_span 'any derivatizing matrix' is generic placeholder, not article-specific evidence in 'methods'
  - inputs[2]: evidence_span 'derivatizing matrices leading to ions...' is generic concept, not grounded in 'methods' section
  - expected_outputs[0]: evidence_span 'any derivatizing matrix' is generic placeholder, not grounded in 'methods'
  - expected_outputs[1]: evidence_span 'derivatizing matrices leading to ions...' is generic concept, not grounded in 'methods'
  - expected_outputs[2]: evidence_span 'Met-ID has a particular focus on derivatizing matrices' not verified in 'methods' section
  - missing_information[1]: evidence_span '[Entire discussion section...]' is meta-commentary, not actual evidence from article text
  - Semantic gap: research_question asks about 'correct adduct annotations' but finding only asserts 'extensibility design' — no evidence of actual validation
- Notes: This task card has **poor groundedness and weak coherence**. The research_question is testable and well-formed, but the finding does not directly answer it—finding asserts design extensibility while question asks about actual correctness of adduct annotations. All input and output claims cite evidence_spans that are either absent from the article, too generic ('any derivatizing matrix'), or incomplete (truncated span in research_question). The missing_information field explicitly states the article lacks technical documentation on configuration, plugin architecture, and registration steps, yet the task_description and workflow assume this documentation exists. The card reads as a **template applied to an article that does not contain the necessary implementation details**, rather than a task derived from the article's actual content. Recommend: (1) verify the source article actually describes Met-ID's plugin/configuration architecture; (2) ground all inputs/outputs in specific claims or methods sections; (3) reconcile the research_question (about correctness) with the finding (about extensibility design intent); (4) either source specific matrix file formats from the article or acknowledge they are assumed/generic.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
