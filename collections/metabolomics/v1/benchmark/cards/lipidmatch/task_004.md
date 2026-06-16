# SciTask Card: Reconstruct the user-generated library integration module by ingesting a custom .csv lipid library into LipidMatch

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-16T06:03:34.399740+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_lipidmatch/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `GarrettLab-UF/LipidMatch`
- Input from: `task_001`
- Quality: Score 4/5 — clean

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `lipidomics`
- Subdomains: `lipidomics`
- Techniques: `database-annotation`, `high-resolution-ms`, `lc-ms`, `metabolite-identification`, `spectral-library-matching`, `tandem-ms`

## Research Question
Does LipidMatch successfully load and integrate user-authored .csv lipid libraries such that custom lipid entries become available as matching candidates in subsequent analyses?

## Connected Finding
LipidMatch provides functionality to integrate user-generated lipid libraries in .csv format, enabling custom lipid entries to be incorporated into the matching workflow for specialized applications.

## Task Description
Load a user-authored lipid library (.csv) into LipidMatch following the documented format specification, then execute a test matching run to verify that custom library entries appear as candidates in the results.

## Inputs
- LipidMatch software from GitHub repository (GarrettLab-UF/LipidMatch)
- User-authored .csv lipid library file conforming to LipidMatch format
- Test MS/MS dataset or fragment m/z list for matching validation

## Expected Outputs
- Custom library integration log or status report confirming successful loading of user entries
- Matching results file (e.g. .csv or .txt) listing candidate lipids from the integrated library for the test dataset

## Artifact References

### Inputs

- `LipidMatch software from GitHub repository (GarrettLab-UF/LipidMatch)` → **github** `GarrettLab-UF/LipidMatch` (score 0.5)

## Expected Output File

- `matching_candidates.csv`

## Landmark Outputs

- `custom_library_formatted.csv`
- `library_integration_log.txt`
- `test_matching_output.csv`

## Tools
- LipidMatch

## Skills
- lipid-library-format-specification
- library-integration-workflow
- fragmentation-pattern-annotation
- lipid-candidate-matching
- file-format-validation

## Workflow Description
1. Obtain the LipidMatch software and documentation from GitHub (GarrettLab-UF/LipidMatch repository). 2. Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns. 3. Place the .csv library file in the designated library directory within the LipidMatch installation. 4. Run LipidMatch library integration/loading step (as documented in the manual) to register the custom entries into the active library index. 5. Execute a test matching workflow on a sample MS/MS dataset (or synthetic fragment m/z list) with the integrated library active. 6. Parse and inspect the output candidate list to confirm that at least one custom library entry appears ranked among the matching candidates.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/LipidMatch_Icon2.png` | figure | False |
| `figures/LipidMatch_Icon3.png` | figure | False |
| `figures/LipidMatch_Icon4.png` | figure | False |
| `figures/LipidPioneer_Icon.png` | figure | False |
| `figures/LipidPioneer_Icon2.png` | figure | False |
| `figures/adwaita.png` | figure | False |
| `figures/ambiance.png` | figure | False |
| `figures/aqua.png` | figure | False |
| `figures/arrowStyles.png` | figure | False |
| `figures/baghira.png` | figure | False |
| `figures/browse.png` | figure | False |
| `figures/browseTree.png` | figure | False |
| `figures/bwidget.png` | figure | False |
| `figures/config.png` | figure | False |
| `figures/dirViewer.png` | figure | False |
| `figures/dust.png` | figure | False |
| `figures/dustSand.png` | figure | False |
| `figures/embeddedWindows.png` | figure | False |
| `figures/embeddedWindows_tile.png` | figure | False |
| `figures/scatterplot3d.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, breaking changes, or library format compatibility across LipidMatch releases

## Domain Knowledge
- LipidMatch library format requires annotation of lipid names, molecular weights, and in-silico fragmentation m/z patterns in a delimited .csv structure.
- Custom library entries must be placed in the designated library directory and registered through the LipidMatch loading step before they become available as matching candidates.
- Library integration success is verified by observing custom entries appear in the candidate output list when matching is performed on test data with matching fragment m/z values.
- LipidMatch supports over 500,000 lipid species across 60+ lipid types in its built-in library; user libraries extend or specialize this resource for unique applications.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Custom library integration log or status report confirming successful loading of user entries.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does LipidMatch successfully load and integrate user-authored .csv lipid libraries such that custom lipid entries become available as matching candidates in subsequent analyses?: 'LipidMatch allows for facile integration of user generated libraries for unique applications'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch provides functionality to integrate user-generated lipid libraries in .csv format, enabling custom lipid entries to be incorporated into the matching workflow for specialized applications.: 'LipidMatch allows for facile integration of user generated libraries for unique applications'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch software from GitHub repository (GarrettLab-UF/LipidMatch): 'the GitHub page for LipidMatch is: https://github.com/GarrettLab-UF/LipidMatch'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] User-authored .csv lipid library file conforming to LipidMatch format: 'LipidMatch allows for facile integration of user generated libraries for unique applications'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Test MS/MS dataset or fragment m/z list for matching validation: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Custom library integration log or status report confirming successful loading of user entries: 'LipidMatch allows for facile integration of user generated libraries for unique applications'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Matching results file (e.g. .csv or .txt) listing candidate lipids from the integrated library for the test dataset: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, breaking changes, or library format compatibility across LipidMatch releases: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists: LipidMatch repository cloned from github:GarrettLab-UF__LipidMatch contains executable scripts for library integration
- verify file_format_is: user-authored .csv lipid library conforms to format specification documented in LipidMatch manual (exact column names and order required)
- verify script_runs: library integration script executes without errors when passed valid .csv file as input
- verify file_exists: integrated library file is generated in expected output location after script execution
- verify contains_substring: output matching run results file contains at least one custom lipid entry from the integrated .csv library among candidate matches (requires exact lipid identifier match)

### Expert Review
- Confirm that the custom lipid entries correctly appear as valid candidates in the matching output (chemical accuracy of integration and ranking)
- Validate that library integration did not corrupt or duplicate entries from the original in-silico library

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Retrieve LipidMatch software from GitHub repository and install according to documentation.
2. Author a test lipid library in .csv format with custom entries including lipid identifiers, m/z values, and fragmentation patterns.
3. Load the custom library into LipidMatch by placing the .csv file in the library directory and executing the library integration step.
4. Run a test matching workflow on sample MS/MS data (or synthetic fragment list) with the integrated library active.
5. Validate: inspect the output candidate list to confirm custom library entries appear ranked among the matching results (at least one custom entry must be present and retrievable).

## Workflow Ports

**Inputs:**

- `lipidmatch_software` — LipidMatch software from GitHub repository ← `task_001/library_validation_report`
- `custom_library_csv` — User-authored lipid library in .csv format
- `test_msms_data` — Test MS/MS dataset or fragment m/z list

**Outputs:**

- `library_integration_log` — Library loading/integration status report
- `matching_candidates` — Matching results showing custom library candidates

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:GarrettLab-UF__LipidMatch`
- **Synthesized at:** 2026-06-16T06:08:45+00:00

## Extraction Quality
- Score: 4/5 — coherent, no placeholders, no flags.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
