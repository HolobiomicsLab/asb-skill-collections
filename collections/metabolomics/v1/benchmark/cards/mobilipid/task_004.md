# SciTask Card: Analyze the minimum lipids-per-class requirement for effective CCS bias calculation in MobiLipid

- Task ID: `task_004`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:36:27.945262+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mobilipid/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-analysis`, `benchmark-evaluation`
- GitHub: `FelinaHildebrand/MobiLipid`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 5 grounding failures

## Classification

- Task kind: `analysis`
- Article type: `software-tool`
- Primary domain: `lipidomics`
- Subdomains: `lipidomics`
- Techniques: `ion-mobility`, `quality-control`, `stable-isotope-labeling`, `high-resolution-ms`

## Research Question
What is the minimum number of lipids per lipid class required to achieve effective CCS bias estimation and correction using the MobiLipid workflow?

## Connected Finding
MobiLipid enables effective CCS bias calculation and correction while requiring only a low number of lipids detected per lipid class.

## Task Description
Computationally evaluate the relationship between the number of detected lipids per lipid class and CCS bias estimation quality using MobiLipid and the bundled DTCCSN2 library, reproducing the reported finding that effective CCS bias correction requires only a low number of lipids per class.

## Inputs
- MobiLipid codebase and DTCCSN2 library for U13C labeled lipids
- Ion mobility-mass spectrometry lipidomics experimental data

## Expected Outputs
- Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class
- Visualization (curve or heatmap) showing the relationship between number of detected lipids per class and CCS bias estimation quality

## Expected Output File

- `ccs_bias_quality_metrics.csv`

## Landmark Outputs

- `lipid_subsampling_levels.txt`
- `bias_estimates_per_class.csv`
- `residual_error_by_count.csv`
- `bias_quality_curve.png`

## Tools
- R

## Skills
- ccs-bias-calculation-and-correction
- lipid-class-stratified-analysis
- internal-standardization-with-isotope-labels
- ion-mobility-mass-spectrometry-data-processing
- quality-control-metric-evaluation

## Workflow Description
1. Load the DTCCSN2 library for U13C labeled lipids and experimental IM-MS lipidomics data into R. 2. Use MobiLipid to systematically vary the number of detected lipids per lipid class (e.g., 1, 2, 3, 5, 10 lipids). 3. For each subsampling level, calculate CCS bias using internal standardization with the available U13C labeled lipids without additional external calibration. 4. Assess bias estimation quality by computing residual error or deviation metrics between predicted and reference CCS values across lipid classes. 5. Quantify the trade-off between lipid count per class and bias correction accuracy, generating a summary table of performance metrics at each sampling level. 6. Visualize the relationship as a curve or heatmap showing how CCS bias estimation quality stabilizes with increasing lipid counts per class.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/MobiLipid_Logo_whiteBackground@300x.png` | figure | False |
| `figures/Output_CCS_bias_after_correction.jpg` | figure | False |
| `figures/Output_CCS_bias_after_correction_all_results.jpg` | figure | False |
| `figures/Output_CCS_bias_figure.jpg` | figure | False |
| `figures/Output_CCS_bias_table.jpg` | figure | False |
| `figures/Output_Correction_functions.jpg` | figure | False |
| `figures/Output_Number_Lipids.jpg` | figure | False |
| `figures/Output_Resampling.jpg` | figure | False |
| `figures/Output_Violin_plot_1.jpg` | figure | False |
| `figures/Output_Violin_plot_2.jpg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found
- specific minimum number of lipids per class required for effective CCS bias estimation not stated in section text
- quantitative results or tables demonstrating the relationship between detected lipid count per class and CCS bias quality not included in section text

## Domain Knowledge
- CCS (collision cross section) bias in IM-MS arises from systematic deviations between measured and theoretical CCS values; internal standardization with U13C labeled lipids can correct this without additional external calibration beyond vendor-specific requirements.
- Lipid class stratification is necessary because CCS bias may vary across lipid classes; MobiLipid groups lipids by class to enable class-specific bias assessment.
- The DTCCSN2 library contains reference CCS values for U13C labeled lipids; subsampling studies measure the minimum lipid count per class needed to achieve stable and accurate bias estimation.
- Quality metrics for CCS bias estimation typically include residual error (difference between predicted and reference CCS), coefficient of variation, or absolute error relative to reference values.
- Ion mobility-mass spectrometry instruments produce CCS measurements that require post-hoc correction; MobiLipid automates this via R Markdown workflows integrated into standard lipidomics pipelines.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What is the minimum number of lipids per lipid class required to achieve effective CCS bias estimation and correction using the MobiLipid workflow?: 'requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MobiLipid enables effective CCS bias calculation and correction while requiring only a low number of lipids detected per lipid class.: 'requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] MobiLipid codebase and DTCCSN2 library for U13C labeled lipids: 'Employing a newly established DT CCS N2 library for U13C labeled lipids, which is provided together with the code'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] Ion mobility-mass spectrometry lipidomics experimental data: 'MobiLipid aims to streamline lipidomics workflows by offering a fully automated solution for assessing and correcting collision cross section (CCS) bias in ion mobility-mass spectrometry (IM-MS)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Summary table of CCS bias estimation quality metrics (e.g., residual error, accuracy) as a function of lipid count per lipid class: 'requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Visualization (curve or heatmap) showing the relationship between number of detected lipids per class and CCS bias estimation quality: 'requiring a low number of lipids detected per lipid class for effective implementation of CCS bias calculation and correction'
- `ev_007` from `agent2_synthesis` (agent2_traced): [intro] R: 'Our tool enhances CCS quality control by providing a R Markdown that integrates into IM-MS lipidomics workflows'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: '_No changelog found._'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] specific minimum number of lipids per class required for effective CCS bias estimation not stated in section text: 'No explicit threshold value provided in the discussion section'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] quantitative results or tables demonstrating the relationship between detected lipid count per class and CCS bias quality not included in section text: 'No results, figures, or tables referenced in the discussion section'

## Evaluation Strategy
### Direct Checks
- verify file exists: github:FelinaHildebrand/MobiLipid repository is accessible and contains DTCCSN2 library artifact
- verify file_format_is: DTCCSN2 library is in a format compatible with R (e.g., .csv, .rds, or documented data structure)
- verify script_runs: R Markdown workflow in MobiLipid codebase executes without error when provided with lipid detection counts and CCS measurements as inputs
- verify output_matches_reference: computational workflow produces a quantitative metric (bias estimate, root mean square error, or correlation coefficient) that demonstrates relationship between lipid count per class and CCS bias quality
- verify field_present: output includes explicit statement or table row showing minimum lipid count per class threshold below which bias estimation remains effective

### Expert Review
- Assess whether the reported finding (low number of lipids per class suffices for effective CCS bias estimation) is scientifically defensible given the computational results and DTCCSN2 reference data
- Evaluate the statistical rigor of the relationship analysis (e.g., linearity, saturation behavior, confidence bounds) between lipid count per class and bias estimation quality
- Review whether the CCS bias estimation method is appropriate for ion mobility-mass spectrometry lipidomics and whether internal standardization with U13C labeled lipids is correctly implemented in the computational workflow

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load the DTCCSN2 reference library and experimental IM-MS lipidomics data into R.
2. Systematically subsample detected lipids per class across a range of counts (e.g., 1–10 lipids per class).
3. Apply MobiLipid internal standardization with U13C labeled lipids to calculate CCS bias at each subsampling level without external calibration.
4. Compute bias estimation quality metrics (residual error, accuracy, or deviation) for each lipid class and count level.
5. Generate a summary table and visualization showing how CCS bias estimation quality stabilizes with increasing lipid counts per class.
6. Validation: confirm that effective CCS bias correction is achieved with a low number of lipids per class, as indicated by convergence of bias metrics and acceptable residual error (acceptance criterion to be determined by reported thresholds in the paper).

## Workflow Ports

**Inputs:**

- `mobilipid_codebase` — MobiLipid codebase and DTCCSN2 library ← `task_001/validation_report`
- `imms_data` — Ion mobility-mass spectrometry lipidomics data

**Outputs:**

- `bias_metrics_table` — CCS bias estimation quality metrics by lipid count
- `bias_quality_plot` — Visualization of relationship between lipid count and bias quality

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:FelinaHildebrand__MobiLipid`
- **Synthesized at:** 2026-06-15T12:40:04+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (5):
  - inputs[0]: evidence_span not found in section 'intro' (value='MobiLipid codebase and DTCCSN2 library for U13C labeled lipi', span='Employing a newly established DT CCS N2 library for U13C lab')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='specific minimum number of lipids per class required for eff', span='No explicit threshold value provided in the discussion secti')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='quantitative results or tables demonstrating the relationshi', span='No results, figures, or tables referenced in the discussion ')
  - research_question asks for 'minimum number' (quantitative threshold) but finding only claims 'low number' (qualitative); semantic mismatch
  - expected_outputs both cite identical evidence_span that only asserts 'low number'—insufficient grounding for two distinct outputs
- Notes: The card exhibits low coherence between its research_question (quantitative threshold-seeking) and finding (qualitative claim of 'low number suffices'). The research_question presupposes an empirical minimum exists and asks to quantify it, while the finding only asserts qualitative benefit—these are semantically misaligned. Multiple groundedness failures stem from evidence_spans that either do not appear in the cited sections or are self-referential placeholders ('No explicit threshold provided'). Inputs lack concrete artifact specifications (URLs, file paths, accessions). The task is scientifically sound in design but the task card conflates the methodology (subsampling study to find the threshold) with an ungrounded claim (that 'low number' is sufficient). Recommend: (1) clarify whether the paper reports a specific minimum or only asserts qualitative benefit; (2) revise finding to match actual evidence; (3) provide concrete input artifact identifiers; (4) decouple the research_question from presupposed conclusions.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
