# SciTask Card: Reproduce the instrument-compatibility matrix reported for LipidMatch across acquisition modes and vendors

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-16T06:03:34.399740+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_lipidmatch/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `information-extraction`, `data-processing`
- GitHub: `GarrettLab-UF/LipidMatch`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 4 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `lipidomics`
- Subdomains: `lipidomics`
- Techniques: `database-annotation`, `high-resolution-ms`, `lc-ms`, `metabolite-identification`, `spectral-library-matching`, `tandem-ms`

## Research Question
What is the complete matrix of instrument/vendor and acquisition mode combinations for which LipidMatch has been validated, and what instrument platforms are explicitly unsupported?

## Connected Finding
LipidMatch validation spans Q-Exactive orbitrap with targeted, ddMS2-topN, and AIF modes; Agilent, Bruker, and SCIEX Q-TOF instruments with direct infusion and imaging; Waters instruments are explicitly unsupported.

## Task Description
Extract and tabulate all instrument/vendor and acquisition mode combinations supported by LipidMatch from the official repository and documentation, identifying validated platforms (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) with their tested modes (targeted, ddMS2-topN, AIF, direct infusion, imaging) and documenting the single unsupported platform (Waters). Output as a structured CSV table.

## Inputs
- LipidMatch GitHub repository (https://github.com/GarrettLab-UF/LipidMatch)
- LipidMatch official documentation and README files

## Expected Outputs
- Structured CSV table enumerating instrument/vendor and acquisition mode combinations with validation status

## Artifact References

### Inputs

- `LipidMatch GitHub repository (https://github.com/GarrettLab-UF/LipidMatch)` → **github** `GarrettLab-UF/LipidMatch` (score 0.4286)

## Expected Output File

- `lipidmatch_instrument_mode_support_matrix.csv`

## Landmark Outputs

- `validated_platforms_list.txt`
- `acquisition_modes_by_vendor.txt`
- `lipidmatch_instrument_mode_support_matrix.csv`

## Tools
- LipidMatch
- Q-Exactive orbitrap
- Agilent Q-TOF UHPLC-HRMS/MS
- Bruker Q-TOF UHPLC-HRMS/MS
- SCIEX Q-TOF UHPLC-HRMS/MS

## Skills
- instrument-platform-compatibility-mapping
- acquisition-mode-enumeration-and-validation
- ms-vendor-documentation-extraction
- technical-specification-tabulation
- software-support-matrix-construction

## Workflow Description
1. Clone or download the LipidMatch GitHub repository (GarrettLab-UF/LipidMatch). 2. Scan the repository README, documentation, and any supplementary materials for explicit statements of validated instrument platforms and acquisition modes. 3. Extract from EnrichedIndex findings the confirmed supported combinations: Q-Exactive orbitrap with targeted, ddMS2-topN, and AIF modes; Agilent, Bruker, and SCIEX Q-TOF platforms with direct infusion and imaging modes. 4. Document the unsupported platform (Waters) as a negative case. 5. Construct a tabular CSV file with columns for instrument vendor, instrument model, acquisition mode, validation status, and supporting reference (evidence location). 6. Validate completeness against the EnrichedIndex by cross-checking all named platforms and modes.

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
- No explicit matrix of validated instrument/vendor and acquisition mode combinations is provided; EnrichedIndex lists four instruments (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) and multiple modes (targeted, ddMS2-topN, AIF, direct infusion, imaging) but does not specify which modes have been validated for which instruments.
- The documentation provided does not clarify whether Agilent, Bruker, and SCIEX Q-TOF instruments have been tested with all five acquisition modes or only a subset; the direct infusion and imaging mode support may apply to all vendors or only specific ones.

## Domain Knowledge
- Q-Exactive orbitrap instruments support three validated acquisition modes with LipidMatch: targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF).
- Agilent, Bruker, and SCIEX Q-TOF platforms are validated for LipidMatch annotation in direct infusion and imaging mass spectrometry experiments.
- Waters mass spectrometry platforms are explicitly unsupported by LipidMatch and cannot be used with the software.
- LipidMatch is modular and platform-agnostic at the peak-picking stage, allowing integration with MZmine, XCMS, MS-DIAL, and Compound Discoverer outputs before lipid annotation.
- The distinction between UHPLC-coupled HRMS/MS (Q-Exactive, Q-TOF instruments) and direct infusion/imaging modes reflects different sample introduction and ionization strategies that affect fragmentation library applicability.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Bruker Q-TOF UHPLC-HRMS/MS, SCIEX Q-TOF UHPLC-HRMS/MS, Structured CSV table enumerating instrument/vendor and acquisition mode combinations with validation status.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the complete matrix of instrument/vendor and acquisition mode combinations for which LipidMatch has been validated, and what instrument platforms are explicitly unsupported?: 'LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch validation spans Q-Exactive orbitrap with targeted, ddMS2-topN, and AIF modes; Agilent, Bruker, and SCIEX Q-TOF instruments with direct infusion and imaging; Waters instruments are explicitly unsupported.: 'LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch GitHub repository (https://github.com/GarrettLab-UF/LipidMatch): 'the GitHub page for LipidMatch is: https://github.com/GarrettLab-UF/LipidMatch'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch official documentation and README files: 'LipidMatch is modular, allowing it to fit in various workflows'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Structured CSV table enumerating instrument/vendor and acquisition mode combinations with validation status: 'construct a structured table enumerating every validated instrument/vendor (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) and acquisition mode (targeted, ddMS2-topN, AIF, direct infusion,'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] LipidMatch: 'LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] Q-Exactive orbitrap: 'tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Agilent Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] Bruker Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] SCIEX Q-TOF UHPLC-HRMS/MS: 'Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No explicit matrix of validated instrument/vendor and acquisition mode combinations is provided; EnrichedIndex lists four instruments (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) and multiple modes (targeted, ddMS2-topN, AIF, direct infusion, imaging) but does not specify which modes have been validated for which instruments.: 'No changelog found.'
- `ev_012` from `agent2_synthesis` (agent2_traced): [discussion] The documentation provided does not clarify whether Agilent, Bruker, and SCIEX Q-TOF instruments have been tested with all five acquisition modes or only a subset; the direct infusion and imaging mode support may apply to all vendors or only specific ones.: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- file_exists: verify that the GitHub repository github:GarrettLab-UF__LipidMatch is accessible and contains documentation or source code listing instrument/vendor and acquisition mode support
- contains_substring: in repository documentation or README, verify presence of explicit mentions of each of the four validated instrument/vendor types (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF)
- contains_substring: in repository documentation, verify presence of explicit mention of at least three acquisition mode types from the set {targeted, ddMS2-topN, AIF, direct infusion, imaging}
- contains_substring: in repository documentation, verify presence of explicit statement that Waters is unsupported or not currently supported
- output_matches_reference: constructed table row count equals number of valid instrument/vendor and acquisition mode combinations documented in source material (no canonical answer — dependent on what combinations are explicitly documented as tested/validated vs. inferred)

### Expert Review
- assess whether the source documentation provides sufficient detail to distinguish between 'tested and validated,' 'applied,' and 'potentially supported but not documented' for each instrument/vendor × acquisition mode pair
- determine whether direct infusion and imaging modes should be attributed to specific instrument/vendor combinations or listed as general capabilities across vendors
- verify that the single documented unsupported case (Waters) is correctly identified and that no other vendor/instrument combinations are negated in the source material

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Access the LipidMatch GitHub repository and official documentation
2. Identify and list all instrument vendors and models explicitly named as supported (Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF)
3. Extract all acquisition modes documented as validated (targeted, ddMS2-topN, AIF, direct infusion, imaging)
4. Map each vendor–mode combination found in the documentation
5. Record the single documented unsupported platform (Waters) with status annotation
6. Validation: Completeness verified by confirmation that all four supported vendors and all five acquisition modes from the EnrichedIndex findings are represented in the table, and Waters is marked as unsupported

## Workflow Ports

**Inputs:**

- `lipidmatch_repo` — LipidMatch GitHub repository and documentation ← `task_001/library_validation_report`

**Outputs:**

- `instrument_mode_table` — Validated instrument/vendor and acquisition mode combinations table

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:GarrettLab-UF__LipidMatch`
- **Synthesized at:** 2026-06-16T06:08:32+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (4):
  - expected_outputs[0]: evidence_span not found in section 'other' (value='Structured CSV table enumerating instrument/vendor and acqui', span='construct a structured table enumerating every validated ins')
  - finding: claims Agilent, Bruker, SCIEX Q-TOF support 'direct infusion and imaging' modes, but evidence_span only mentions 'Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation' — no mention of Agilent, Bruker, SCIEX, direct infusion, or imaging in the provided evidence
  - finding: claims 'Waters instruments are explicitly unsupported' but this statement does not appear in the evidence_span
  - missing_information entries cite 'No changelog found' as evidence_span for discussion of validation matrix gaps — this is not meaningful grounding
- Notes: This card exhibits a critical disconnect between its narrow evidence base (single evidence_span about Q-Exactive only) and its broad finding (complete multi-vendor matrix with unsupported platforms). The finding appears to be constructed from the 'domain_knowledge' section and task descriptions rather than derived from actual grounded sources. The card conflates 'what the task asks to extract' with 'what has been extracted.' The missing_information section correctly identifies that no validated instrument/mode matrix is provided in the source, yet the finding asserts exactly such a matrix. Recommend: (1) Reground all finding statements against actual evidence_spans from the GitHub repository, (2) Remove unverified domain knowledge assertions, (3) Decompose the finding into separate TracedClaims for each vendor and mode combination with individual evidence, (4) Clarify whether this is an extraction task (in progress) or a verification task (post-extraction).

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
