# SciTask Card: Reconstruct the derivatizing-matrix ion adduct enumeration module in Met-ID

- Task ID: `task_001`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:59:56.876471+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_metid/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `modeling`
- GitHub: `pbjarterot/Met-ID`
- Quality: Score 2/5 — Coherent: false, placeholder, 6 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `untargeted-metabolomics`
- Techniques: `metabolite-identification`, `database-annotation`, `in-silico-fragmentation`

## Research Question
How does Met-ID compute expected adduct ions for metabolites when using derivatizing matrices like FMP-10, beyond the standard [M+H]+ and [M-H]- ions?

## Connected Finding
Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode, and the software is extendable to use any derivatizing matrix.

## Task Description
Implement an adduct ion prediction module that, given a derivatizing matrix identifier (e.g., FMP-10) and a metabolite SMILES string, computes expected adduct masses beyond the common [M+H]+ and [M-H]- ions. Return predicted adduct m/z values and ion formulas as a structured output.

## Inputs
- Metabolite SMILES string and derivatizing matrix identifier (e.g., FMP-10)
- Reference FMP-10 adduct mass dataset from Nature Methods paper

## Expected Outputs
- Predicted adduct ions table with adduct formula, mass shift, m/z value, and ionization state
- Validation report comparing predicted adduct masses to reference FMP-10 values

## Expected Output File

- `predicted_adducts.csv`

## Landmark Outputs

- `matrix_ruleset_loaded.json`
- `molecules_parsed.tsv`
- `predicted_adducts.csv`

## Tools
- RDKit

## Skills
- adduct-mass-calculation-from-smiles
- derivatizing-matrix-ionization-rule-application
- molecular-weight-prediction-with-modifications
- mass-spectrometry-ion-formula-assignment
- reference-dataset-validation-for-metabolite-ions

## Workflow Description
1. Parse input metabolite SMILES and matrix identifier using RDKit to construct the molecular graph and validate structure. 2. Query or load the matrix-specific adduct ionization ruleset (e.g., FMP-10 adduct patterns from Nature Methods reference data). 3. For each adduct rule in the matrix profile, apply RDKit molecular weight calculation to compute the expected m/z accounting for the derivatizing matrix modification and ionization state. 4. Return a table of predicted adduct ions with their formulas, mass shifts, and expected m/z values, and compare against reference FMP-10 adduct masses from the published Nature Methods dataset.

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
- No changelog provided; cannot trace evolution of adduct computation component or verify stability of the implementation.
- The specific Nature Methods paper containing reference FMP-10 adduct masses is not cited or linked in the provided section text.
- No explicit description of the adduct computation algorithm, matrix-specific ionization rules, or expected output format is present in the provided section text.

## Domain Knowledge
- Derivatizing matrices like FMP-10 modify metabolite ionization patterns by forming covalent adducts, resulting in ions with m/z values that depend on both the matrix mass and the protonation/deprotonation state of the resulting complex.
- Common MS adducts in positive mode include [M+H]+, [M+Na]+, [M+K]+, and [M+NH4]+; in negative mode [M-H]-, [M+Cl]-, and [M+HCOO]-; derivatizing matrices introduce additional adduct patterns specific to their chemical structure.
- RDKit molecular weight calculation must account for exact isotope masses and ionization-state charge to produce accurate predicted m/z values for comparison against experimental high-resolution mass spectrometry data.
- The Nature Methods reference FMP-10 dataset likely reports observed adduct m/z values with measurement uncertainty (typically ≤5 ppm for high-resolution instruments); predicted values within this tolerance are considered correct matches.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Predicted adduct ions table with adduct formula, mass shift, m/z value, and ionization state, Validation report comparing predicted adduct masses to reference FMP-10 values.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does Met-ID compute expected adduct ions for metabolites when using derivatizing matrices like FMP-10, beyond the standard [M+H]+ and [M-H]- ions?: 'Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]- in negative mode.'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] Met-ID is designed to handle derivatizing matrices such as FMP-10, which produce ions other than the common [M+H]+ in positive mode and [M-H]- in negative mode, and the software is extendable to use any derivatizing matrix.: 'As [FMP-10](https://www.nature.com/articles/s41592-019-0551-3) was developed in house, it features heavily in the software, however, this is mostly to show the point at which to start as Met-ID is'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Metabolite SMILES string and derivatizing matrix identifier (e.g., FMP-10): 'given a derivatizing matrix (e.g. FMP-10) and a metabolite SMILES'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Reference FMP-10 adduct mass dataset from Nature Methods paper: 'Evaluation is against known FMP-10 adduct masses published in the referenced Nature Methods paper'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] Predicted adduct ions table with adduct formula, mass shift, m/z value, and ionization state: 'computes the expected adduct ions beyond [M+H]+ and [M-H]-'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Validation report comparing predicted adduct masses to reference FMP-10 values: 'Evaluation is against known FMP-10 adduct masses published in the referenced Nature Methods paper'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] RDKit: 'Powered by RDKit'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog provided; cannot trace evolution of adduct computation component or verify stability of the implementation.: '_No changelog found._'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] The specific Nature Methods paper containing reference FMP-10 adduct masses is not cited or linked in the provided section text.: 'References — Source: github:pbjarterot__Met-ID'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No explicit description of the adduct computation algorithm, matrix-specific ionization rules, or expected output format is present in the provided section text.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that the adduct computation module accepts a derivatizing matrix identifier (e.g., 'FMP-10') and a metabolite SMILES string as inputs
- verify that the module returns a structured list or table of predicted adduct ions with their m/z values
- verify that output includes adducts beyond [M+H]+ and [M-H]- (e.g., [M+Na]+, [M+K]+, or matrix-specific adducts)
- verify script runs without errors on a test case with FMP-10 and a standard metabolite SMILES
- output matches reference adduct masses for FMP-10 reported in Nature Methods paper — robust to minor mass tolerance (±0.01 Da or ±10 ppm, multiple defensible tolerances acceptable)

### Expert Review
- verify that predicted adduct ions are chemically plausible for the given derivatizing matrix FMP-10
- verify that fragmentation or ionization logic follows established mass spectrometry principles for the matrix type
- assess whether adduct coverage is complete relative to known FMP-10 ionization pathways in the referenced Nature Methods study

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** trivial

## Methodology Summary
1. Load and validate metabolite SMILES string; parse matrix identifier to retrieve or initialize adduct ionization ruleset.
2. Construct molecular graph using RDKit; calculate exact molecular weight of the unmodified metabolite.
3. For each matrix-specific adduct rule, compute the expected m/z by adding matrix mass and applying charge state (proton gain/loss).
4. Compile predicted adduct table with ion formula, mass shift, m/z, and charge state.
5. Validation: Compare predicted adduct m/z values against reference FMP-10 dataset; accept predictions with mass error ≤5 ppm (or as specified in Nature Methods reference).

## Workflow Ports

**Inputs:**

- `metabolite_smiles` — Metabolite SMILES string
- `matrix_id` — Derivatizing matrix identifier
- `reference_adducts` — Reference FMP-10 adduct masses from Nature Methods

**Outputs:**

- `predicted_adducts` — Predicted adduct ions table with formula, mass, and m/z
- `validation_report` — Comparison of predicted vs. reference FMP-10 adduct masses

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:pbjarterot__Met-ID`
- **Synthesized at:** 2026-06-15T14:02:41+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (6):
  - inputs[0]: evidence_span not found in section 'other' (value='Metabolite SMILES string and derivatizing matrix identifier ', span='given a derivatizing matrix (e.g. FMP-10) and a metabolite S')
  - inputs[1]: evidence_span not found in section 'other' (value='Reference FMP-10 adduct mass dataset from Nature Methods pap', span='Evaluation is against known FMP-10 adduct masses published i')
  - expected_outputs[0]: evidence_span not found in section 'other' (value='Predicted adduct ions table with adduct formula, mass shift,', span='computes the expected adduct ions beyond [M+H]+ and [M-H]-')
  - expected_outputs[1]: evidence_span not found in section 'other' (value='Validation report comparing predicted adduct masses to refer', span='Evaluation is against known FMP-10 adduct masses published i')
  - finding: evidence_span is incomplete — truncates mid-sentence ('As [FMP-10]... however, this is mostly to show the point at which to start as Met-ID is') and does not substantiate the claim that the software is 'extendable to use any derivatizing matrix'
  - research_question vs. finding mismatch: RQ asks 'HOW does Met-ID compute...' (algorithmic mechanism), but finding only states THAT it handles derivatizing matrices (capability statement); no algorithm/method is described
- Notes: This task card demonstrates a critical disconnect between its research question (mechanism-focused) and its finding (capability-focused). The RQ asks 'HOW does Met-ID compute expected adduct ions' but the finding only states 'Met-ID is designed to handle derivatizing matrices'—these are orthogonal claims. The card is heavily over-specified in workflow and methodology (suggesting synthesis from domain knowledge rather than article extraction) while simultaneously under-grounded in actual source evidence. Four of four inputs/expected_outputs fail groundedness checks due to section location errors. The evidence span for the finding is incomplete and truncated. The extensibility claim ('extendable to use any derivatizing matrix') is unsupported by the quoted evidence. The Nature Methods reference dataset is cited but not linked or validated. Recommend: (1) Clarify whether the task is to extract HOW Met-ID works or merely WHAT it does; (2) Locate complete, untruncated evidence spans in the actual source sections; (3) Ground all inputs, outputs, and workflow steps to article text; (4) Remove speculative workflow language and replace with either documented behavior or explicit inferences; (5) Provide concrete FMP-10 reference dataset link and expected adduct m/z values.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
