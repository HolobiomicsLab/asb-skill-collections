# SciTask Card: Reconstruct the MS data analysis workflow module coverage across LC, GC, IMS, and MS Imaging input types

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:03:35.256902+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mzmine3/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `information-extraction`, `benchmark-evaluation`
- GitHub: `mzmine/mzmine`
- Quality: Score 2/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the software architecture?

## Connected Finding
mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.

## Task Description
Enumerate all mzmine processing modules and verify that each supported separation/ionisation type (LC, GC, IMS, MS Imaging) maps to at least one corresponding module, confirming complete coverage of the MS data analysis workflow architecture.

## Inputs
- mzmine repository at github.com/mzmine/mzmine

## Expected Outputs
- Module inventory and coverage matrix documenting all mzmine processing modules and their supported separation/ionisation types
- Verification report confirming each of LC, GC, IMS, and MS Imaging has at least one corresponding processing module

## Artifact References

### Inputs

- `mzmine repository at github.com/mzmine/mzmine` → **github** `mzmine/mzmine` (score 0.25)

## Expected Output File

- `mzmine_module_coverage_report.csv`

## Landmark Outputs

- `module_list.txt`
- `separation_type_module_mapping.csv`

## Tools
- mzmine

## Skills
- software-architecture-documentation-review
- ms-instrument-type-classification
- module-coverage-mapping
- ionisation-method-hardware-correspondence
- separation-technique-workflow-alignment

## Workflow Description
1. Access the mzmine repository (github.com/mzmine/mzmine) and retrieve the complete list of processing modules from the codebase structure or documentation. 2. Categorise each module by its primary function (e.g., import, preprocessing, alignment, identification, visualisation). 3. Cross-reference module documentation or source code to identify which separation/ionisation types each module supports (LC, GC, IMS, MS Imaging). 4. Build a coverage matrix mapping separation/ionisation types to modules. 5. Verify that every supported type (LC, GC, IMS, MS Imaging) is covered by at least one module in the workflow. 6. Document the module inventory and coverage verification in a structured report.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/CV.png` | figure | False |
| `figures/MZmine_IIMN_logo_RGB.png` | figure | False |
| `figures/anova_test.png` | figure | False |
| `figures/logo300_mzmine.png` | figure | False |
| `figures/logo300_mzmine_light.png` | figure | False |
| `figures/logo300_mzmine_white.png` | figure | False |
| `figures/logo300_mzwizard.png` | figure | False |
| `figures/logo300_mzwizard_light.png` | figure | False |
| `figures/logo300_mzwizard_white.png` | figure | False |
| `figures/logo_mzmine.svg` | figure | False |
| `figures/logo_mzmine_light.svg` | figure | False |
| `figures/logo_mzmine_white.svg` | figure | False |
| `figures/logo_mzwizard.svg` | figure | False |
| `figures/logo_mzwizard_light.svg` | figure | False |
| `figures/logo_mzwizard_white.svg` | figure | False |
| `figures/logratio.png` | figure | False |
| `figures/mac_installer_background.png` | figure | False |
| `figures/mac_installer_background@2x.png` | figure | False |
| `figures/mzmine-fbmn.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found
- The provided section text contains no detailed enumeration of mzmine modules, their names, or their specific mapping to LC, GC, IMS, and MS Imaging data types. The EnrichedIndex references a high-level claim that mzmine provides 'a complete set of modules covering the entire MS data analysis workflow' and 'support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging', but does not supply the actual module list or architecture specification required to verify this claim.

## Domain Knowledge
- LC (liquid chromatography), GC (gas chromatography), IMS (ion mobility spectrometry), and MALDI MS imaging are distinct separation and ionisation approaches each requiring dedicated data preprocessing and interpretation logic.
- A complete MS data analysis workflow spans raw data import, preprocessing (noise reduction, alignment), feature detection, metabolite identification, and statistical/visualisation output.
- Module architecture must support multiple instrument types because ionisation and separation hardware produce qualitatively different data formats and peak characteristics.
- Coverage verification requires mapping each data-acquisition modality to its corresponding processing pipeline rather than relying on generic module names.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the complete set of processing modules provided by mzmine, and does each supported separation/ionisation technique (LC, GC, IMS, MS imaging) have at least one corresponding module in the software architecture?: 'provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow. Support includes liquid chromatography (LC), gas'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] mzmine is designed with a complete set of modules covering the entire MS data analysis workflow and supports liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI), and most MS instruments.: 'provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow. Support includes liquid chromatography (LC), gas'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] mzmine repository at github.com/mzmine/mzmine: 'github.com/mzmine/mzmine'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] Module inventory and coverage matrix documenting all mzmine processing modules and their supported separation/ionisation types: 'complete set of modules covering the entire MS data analysis workflow'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Verification report confirming each of LC, GC, IMS, and MS Imaging has at least one corresponding processing module: 'Support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging (e.g., MALDI)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] mzmine: 'mzmine is an open-source software for mass spectrometry data processing'
- `ev_007` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] The provided section text contains no detailed enumeration of mzmine modules, their names, or their specific mapping to LC, GC, IMS, and MS Imaging data types. The EnrichedIndex references a high-level claim that mzmine provides 'a complete set of modules covering the entire MS data analysis workflow' and 'support includes liquid chromatography (LC), gas chromatography (GC), ion mobility spectrometry (IMS), MS imaging', but does not supply the actual module list or architecture specification required to verify this claim.: 'provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow; Support includes liquid chromatography (LC), gas'

## Evaluation Strategy
### Direct Checks
- verify file_exists: mzmine repository root at github:mzmine__mzmine contains a modules/ or src/ directory listing all module implementations
- verify file_format_is: module inventory (generated or extracted from source tree) is a structured table or JSON file mapping module name to supported data types (LC, GC, IMS, MS Imaging)
- verify contains_substring: module inventory explicitly lists at least one module for each of LC, GC, IMS, and MS Imaging (e.g., 'LC' or 'liquid chromatography', 'GC' or 'gas chromatography', 'IMS' or 'ion mobility', 'imaging' or 'MALDI')
- verify script_runs: automated audit script (e.g., Java reflection, AST parser, or build manifest parser) executes without error on mzmine source tree and produces complete module enumeration
- verify output_matches_reference: enumerated module set is byte-for-byte consistent with official mzmine documentation (README, manual, or API docs) module inventory, if published

### Expert Review
- confirm that each of the four separation/ionisation types (LC, GC, IMS, MS Imaging) is genuinely supported by at least one distinct processing module (not merely claimed in prose; module must have active implementation)
- assess whether the enumerated modules collectively cover the 'entire MS data analysis workflow' (data import, preprocessing, feature detection, alignment, annotation, export) or if critical stages are missing
- determine whether any separation/ionisation type is covered only by a single module (architectural fragility) or has redundant/complementary implementations

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Clone or access the mzmine GitHub repository to retrieve the complete source code and documentation structure.
2. Identify and enumerate all processing modules within the codebase by scanning the module directory structure and build configuration.
3. Extract module metadata (name, purpose, supported data types) from source code documentation and README files.
4. Map each module to one or more of the four supported separation/ionisation types: LC, GC, IMS, MS Imaging.
5. Construct a coverage matrix showing which modules support each type.
6. Validation: confirm that each of the four separation/ionisation types (LC, GC, IMS, MS Imaging) is assigned to at least one module, as stated in the article's core finding that mzmine provides 'a complete set of modules covering the entire MS data analysis workflow' with support for all four modalities.

## Workflow Ports

**Inputs:**

- `mzmine_repo` — mzmine repository

**Outputs:**

- `module_inventory` — Module inventory and coverage matrix
- `coverage_verification` — Verification report of separation/ionisation type coverage

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:mzmine__mzmine`
- **Synthesized at:** 2026-06-16T07:05:13+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - Evidence span truncated: 'provide a user-friendly, flexible and easily extendable software with a complete set of modules covering the entire MS data analysis workflow. Support includes liquid chromatography (LC), gas' — ends mid-sentence at 'gas', missing GC, IMS, and MS Imaging completeness claims
  - Semantic gap: research_question asks for 'complete set of processing modules' with enumeration, but finding claims support for four modalities without enumerating any actual module names
  - Semantic gap: finding claims support for 'most MS instruments' which is vague and not grounded in the evidence_span
  - Semantic gap: finding adds detail about MALDI MS imaging example not present in evidence_span
- Notes: This card conflates a research question (what needs to be verified) with a finding (what was allegedly found) without providing the intermediate evidence. The research_question is well-formed and specific, but the finding asserts four modality-support claims without listing a single module name. The evidence_span is truncated mid-sentence ('gas') and does not include the complete claim about GC, IMS, and MS Imaging support. The missing_information field explicitly acknowledges that no module enumeration exists in the source text. The card is structured as a task prescription (do this analysis) rather than a completed verification (here is what we found). Quality is further degraded by the vague claim of 'most MS instruments' in the finding, which is non-specific and potentially contradicts the 'complete set' claim. To improve: (1) either ground the finding in actual module enumeration from the source, or (2) reframe this as a task card (not a verified finding card) and move findings to expected_outputs. The coherence_ok flag is false because the research_question asks for enumeration + verification, but the finding provides only unsupported assertions.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
