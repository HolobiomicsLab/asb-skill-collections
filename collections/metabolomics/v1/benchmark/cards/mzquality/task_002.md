# SciTask Card: Reconstruct the doAnalysis quality-control and batch-correction step to produce the ratio_corrected assay

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T13:20:51.739319+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_mzquality/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `statistical-analysis`
- GitHub: `hankemeierlab/mzQuality`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, 6 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `untargeted-metabolomics`, `computational-metabolomics`
- Techniques: `quality-control`, `feature-detection`, `lc-ms`, `normalization`, `statistical-analysis`

## Research Question
How does the doAnalysis function process a SummarizedExperiment object to identify outliers and mis-injections, and what corrected assay does it produce?

## Connected Finding
doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio, tests Study Samples for mis-injections using Internal Standard areas, and produces a ratio_corrected assay in the output experiment.

## Task Description
Apply the doAnalysis function with default parameters (removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30) to a SummarizedExperiment object to perform quality control analysis, producing an experiment with ratio-corrected assays and outlier/mis-injection annotations.

## Inputs
- task_001.expected_outputs[0]: SummarizedExperiment object with rowData, colData, and assays including 'ratio'
- SummarizedExperiment object with raw compound area and internal standard area assays, sample metadata (type, batch, injection_time), and compound annotations

## Expected Outputs
- SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios
- Outlier annotations on QC samples flagged by Compound/Internal Standard ratio analysis
- Mis-injection annotations on study samples identified via Internal Standard area thresholds
- Optional: absolute concentration values calculated via linear regression for compounds in calibration samples with known spike concentrations

## Landmark Outputs

- `ratio_corrected_assay.tsv`
- `outlier_annotations.csv`
- `mis_injection_flags.csv`
- `concentrations.csv`

## Tools
- mzQuality
- R
- SummarizedExperiment

## Skills
- metabolite-ratio-batch-correction
- quality-control-sample-outlier-detection
- internal-standard-area-mis-injection-flagging
- compound-reliability-filtering-by-rsd-threshold
- linear-regression-concentration-calibration

## Workflow Description
1. Load the SummarizedExperiment object created by buildExperiment from the prior data preparation step. 2. Invoke doAnalysis with parameters removeOutliers=TRUE to flag QC sample outliers based on Compound/Internal Standard ratios, useWithinBatch=TRUE to apply batch correction using pooled study quality control samples, and removeBadCompounds=TRUE to filter compounds failing quality thresholds. 3. Apply qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 thresholds to define acceptable analyte reliability and measurement variability. 4. Generate output SummarizedExperiment containing the 'ratio_corrected' assay with batch-corrected compound/internal-standard ratios and metadata annotations marking detected outliers and mis-injected study samples (identified via internal standard areas). 5. Optionally calculate absolute concentrations via (weighted) linear regression if concentration column is present in the input data, restricted to a single sample type per analysis run.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/Rplot001.jpg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog documenting version history, bug fixes, or parameter changes to doAnalysis function

## Domain Knowledge
- Batch correction in metabolomics uses pooled study quality control (SQC) samples as a reference to normalize Compound/Internal Standard ratios across injection sequences, removing systematic drift and instrument variation.
- Outlier detection in QC samples flags aberrant Compound/Internal Standard ratios that exceed control limits, indicating failed injections or instrument malfunction; study samples flagged via abnormal Internal Standard areas indicate potential mis-injection or sample preparation failure.
- Compound reliability filtering removes analytes with Relative Standard Deviation (RSD) of QC sample ratios above a threshold (default nonReportableRSD=30%), ensuring only reproducible measurements are reported.
- The qcPercentage and backgroundPercentage parameters define the fraction of QC and background-only samples required to pass quality checks; withBatch=TRUE restricts corrections to within-batch samples to avoid artificial normalization across batch boundaries.
- mzQuality currently supports only one sample type (e.g., Academic Calibration or Plasma Calibration) for concentration calculations; multi-type concentration support is a known limitation for future releases.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: SummarizedExperiment, SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] How does the doAnalysis function process a SummarizedExperiment object to identify outliers and mis-injections, and what corrected assay does it produce?: 'The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio. Furthermore, Study Samples are tested for mis-injections'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] doAnalysis with parameters removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, and nonReportableRSD=30 tests QC samples for outliers using Compound/Internal Standard ratio, tests Study Samples for mis-injections using Internal Standard areas, and produces a ratio_corrected assay in the output experiment.: 'exp <- doAnalysis(
    exp = exp, 
    removeOutliers = TRUE, 
    useWithinBatch = TRUE, 
    removeBadCompounds = TRUE,
    qcPercentage = 80,
    backgroundPercentage = 40,
    nonReportableRSD ='
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] SummarizedExperiment object with raw compound area and internal standard area assays, sample metadata (type, batch, injection_time), and compound annotations: 'The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] SummarizedExperiment object with 'ratio_corrected' assay containing batch-corrected Compound/Internal Standard ratios: 'batch-correction using pooled study quality control samples (SQC)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Outlier annotations on QC samples flagged by Compound/Internal Standard ratio analysis: 'The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Mis-injection annotations on study samples identified via Internal Standard area thresholds: 'Furthermore, Study Samples are tested for mis-injections using their Internal Standard areas.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Optional: absolute concentration values calculated via linear regression for compounds in calibration samples with known spike concentrations: 'mzQuality can calculate absolute concentrations by using calibration line samples and known concentrations for spiked compounds.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] mzQuality: 'mzQuality requires a specific format for the input data.'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] R: 'library(mzQuality)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [intro] SummarizedExperiment: 'Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data.'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting version history, bug fixes, or parameter changes to doAnalysis function: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify that the input SummarizedExperiment object exists and is loadable from task_NNN.expected_outputs (from prior buildExperiment step)
- verify that doAnalysis function is callable from the mzQuality package (script_runs with documented default parameters: removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30)
- verify that the output SummarizedExperiment object contains an assay named 'ratio_corrected' (field_present)
- verify that the output SummarizedExperiment object contains column metadata with outlier annotations for QC samples (field_present)
- verify that the output SummarizedExperiment object contains column metadata with mis-injection annotations for study samples (field_present)
- verify that row count and column count of output assays are consistent with input (robust to parameter choices)

### Expert Review
- assess whether batch-correction using pooled SQC samples has been correctly applied in the 'ratio_corrected' assay by inspecting a subset of QC sample ratios before and after correction
- assess whether outlier detection thresholds (including qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30) have been appropriately applied to flag QC sample outliers
- assess whether compound filtering (removeBadCompounds=TRUE) has removed only truly unreliable compounds based on the quality metrics applied

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load SummarizedExperiment object containing raw compound areas, internal standard areas, and sample metadata.
2. Apply outlier detection on QC samples by evaluating Compound/Internal Standard ratios against control thresholds (qcPercentage=80).
3. Test study samples for mis-injections using internal standard area thresholds (backgroundPercentage=40).
4. Perform batch correction of Compound/Internal Standard ratios using pooled SQC samples within batch strata (useWithinBatch=TRUE).
5. Filter out compounds with batch-corrected ratio RSD exceeding nonReportableRSD=30 threshold (removeBadCompounds=TRUE).
6. Optionally calculate absolute concentrations via linear regression from calibration samples (single sample type only).
7. Validation: output SummarizedExperiment contains 'ratio_corrected' assay with numeric batch-corrected ratio values, and metadata annotations identify all flagged outliers and mis-injections; concentration column (if input provided) contains numeric or NA values matching calibration line sample counts.

## Workflow Ports

**Inputs:**

- `summarized_experiment` — SummarizedExperiment with raw assays and metadata

**Outputs:**

- `analyzed_experiment` — SummarizedExperiment with ratio_corrected assay and quality annotations
- `outlier_flags` — QC sample outlier and study sample mis-injection annotations
- `concentrations` — Calculated absolute concentrations (if concentration column provided)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:hankemeierlab__mzQuality`
- **Synthesized at:** 2026-06-15T13:26:59+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: false
- Groundedness failures (6):
  - research_question: evidence_span not found in section 'results' (value='How does the doAnalysis function process a SummarizedExperim', span='The package tests samples for outliers, specifically for (Po')
  - finding: evidence_span not found in section 'results' (value='doAnalysis with parameters removeOutliers=TRUE, useWithinBat', span='exp <- doAnalysis(
    exp = exp, 
    removeOutliers = TRUE') — span truncated and evidence appears to be code snippet rather than explanatory text
  - expected_outputs[0]: evidence_span incomplete — 'batch-correction using pooled study quality control samples' does not support the claim of a 'ratio_corrected assay' output specifically
  - expected_outputs[1]: evidence_span mismatch — generic statement about outlier testing does not confirm annotation format or storage mechanism
  - expected_outputs[2]: evidence_span mismatch — generic statement about mis-injection testing does not confirm annotation format or storage mechanism
  - expected_outputs[3]: evidence_span mismatch — statement about concentration calculation capability does not specifically support 'linear regression' method or output format claims
- Notes: This card exhibits systemic grounding failures across research_question, finding, and all expected_outputs. The core issue is a mismatch between detailed, specific technical claims (parameter names, output assay names, annotation storage mechanisms) and generic, capability-focused evidence spans that do not substantiate the specifics. The research_question semantically aligns with the task objective and workflow, but the evidence provided does not support the detailed claims about how the function operates or what it produces. The finding's evidence_span is a truncated code snippet that appears to be example usage rather than documentation explaining the function's behavior. To resolve: (1) provide complete, untruncated evidence spans that explicitly document doAnalysis output structure and assay names; (2) cite results-section data showing the actual 'ratio_corrected' assay in output; (3) confirm metadata column names/formats for outlier and mis-injection flags; (4) clarify the distinction between capability (what the package CAN do) and execution (what this specific task produces).

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
