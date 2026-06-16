# SciTask Card: Extend PCPFM batch correction step to validate pycombat output retains sample count and reduces batch variance

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T12:44:57.617706+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_pcpfm/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `statistical-analysis`
- DOI: `10.1371/journal.pcbi.1011912`
- GitHub: `shuzhao-li-lab/PythonCentricPipelineForMetabolomics`
- Input from: `task_002`

## Classification

- Task kind: `extension`
- Article type: `research-article`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`
- Techniques: `lc-ms`, `tandem-ms`, `feature-detection`, `database-annotation`, `spectral-library-matching`, `metabolite-identification`

## Research Question
Does batch correction via pycombat preserve the structural integrity (sample and feature count) of multi-batch metabolomics feature tables while reducing inter-batch variance?

## Connected Finding
Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while systematically reducing inter-batch intensity variance for shared features.

## Task Description
Apply batch correction to a multi-batch interpolated feature table using pycombat, then verify that the corrected table preserves sample and feature counts while reducing inter-batch variance for selected metabolite features.

## Inputs
- task_002.expected_outputs[0]: Blank-masked feature table in TSV format with low-intensity background features removed, indexed by feature identifier and sample
- Interpolated feature table (.tsv) with missing values imputed to 0.5× minimum feature intensity
- Sample metadata CSV with batch field indicating experimental batch or acquisition group for each sample

## Expected Outputs
- Batch-corrected feature table (.tsv) with identical dimensions to input, feature intensities adjusted to remove systematic batch biases
- Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for ≥5 representative features

## Expected Output File

- `batch_corrected_feature_table.tsv`

## Landmark Outputs

- `interpolated_input_table.tsv`
- `pre_correction_batch_variance_summary.json`
- `batch_corrected_feature_table.tsv`
- `post_correction_batch_variance_summary.json`
- `batch_correction_validation_report.txt`

## Tools
- ThermoRawFileParser
- pycombat
- Python

## Skills
- batch-effect-variance-quantification
- metabolomic-feature-table-processing
- batch-correction-quality-assessment
- multi-batch-experimental-design-understanding
- inter-sample-variance-calculation

## Workflow Description
1. Load the interpolated feature table (post-imputation) and sample metadata containing batch labels. 2. Apply pycombat-based batch correction via the pcpfm batch_correct command with the --by_batch parameter specifying the batch metadata field. 3. Verify that the output table has identical dimensions (sample count and feature count) to the input table. 4. Calculate median inter-batch variance for a subset of high-intensity features in both uncorrected and corrected tables using sample grouping by the batch field. 5. Confirm that corrected table median inter-batch variance is lower than uncorrected median inter-batch variance, demonstrating successful batch effect attenuation.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version information found

## Domain Knowledge
- Batch effects in LC-MS metabolomics arise from systematic shifts in feature intensities across acquisition runs or experimental groups, independent of biological variation; pycombat uses an empirical Bayesian approach to identify and adjust these systematic biases.
- Batch correction cannot reliably handle tables with extensive missing values (zeros), so imputation must precede batch correction to avoid distorted covariate estimation and parameter shrinkage.
- Inter-batch variance is typically quantified as the ratio or difference in median feature intensity between batch pairs; reduction in this metric (relative to pre-correction) is the primary success criterion for batch correction efficacy.
- The --by_batch metadata field must exactly match sample-level batch labels in the input metadata CSV; mismatched or misspelled batch designations will cause the correction to fail or produce spurious results.
- Batch correction trades inter-batch variance reduction against potential inflation of within-batch variance or removal of genuine biological signals that correlate with batch; validation requires domain expert review of corrected feature distributions, not only variance metrics.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for ≥5 representative features.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [results] Does batch correction via pycombat preserve the structural integrity (sample and feature count) of multi-batch metabolomics feature tables while reducing inter-batch variance?: 'Batch correction is performed using pycombat'
- `ev_002` from `agent2_synthesis` (agent2_traced): [results] Batch correction using pycombat is applied to multi-batch interpolated feature tables via the by_batch flag, and the corrected table should retain identical sample and feature dimensions while systematically reducing inter-batch intensity variance for shared features.: 'Batch correction is difficult and may require non-default options for removing rare features or other params to achieve the desired result. Batch correction cannot handle missing values well either,'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Interpolated feature table (.tsv) with missing values imputed to 0.5× minimum feature intensity: 'Missing features can complicate statistical testing since zeros will skew analyses towards significant results. It is often proper to impute values to 'fill in' these missing values. Currently, the'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Sample metadata CSV with batch field indicating experimental batch or acquisition group for each sample: 'Batch correction is performed using pycombat.'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Batch-corrected feature table (.tsv) with identical dimensions to input, feature intensities adjusted to remove systematic batch biases: 'This command will use the batches, determed by the `--by_batch` flag to batch correct the feature table. Batch correction is performed using pycombat.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Quantitative validation report containing: sample count, feature count, pre- and post-correction inter-batch variance estimates for ≥5 representative features: 'Batch correction is difficult and may require non-default options for removing rare features or other params to achieve the desired result.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] pycombat: 'Batch correction is performed using pycombat.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [intro] Python: 'Python-Centric Pipeline for Metabolomics'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] No changelog or version information found: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists: input multi-batch interpolated feature table (e.g., CSV, TSV, or HDF5 format)
- verify file_format_is: input feature table conforms to expected shape (rows=samples, columns=features)
- script_runs: pycombat batch_correct function executes without errors on input table using by_batch parameter
- verify file_exists: output corrected feature table (same format as input)
- row_count_equals: corrected table row count matches input table row count (samples preserved)
- row_count_equals: corrected table column count matches input table column count (features preserved)
- verify output_matches_reference: inter-batch variance (e.g., sum-of-squares or Silhouette distance) for selected features is lower in corrected table than uncorrected table; solution_space: multiple defensible variance metrics (PCA-based, PERMANOVA, homogeneity index) are valid
- value_in_range: variance reduction magnitude is quantitatively reported as a numeric score or percentage; parameter-sensitive: depends on feature and batch selection

### Expert Review
- inspect corrected feature table for biological plausibility: verify that batch correction does not artificially inflate or eliminate true biological signal (e.g., case-control or treatment effects should remain detectable post-correction)
- assess choice of selected features for variance reduction analysis: confirm that features are representative (e.g., not cherry-picked) and that the selection strategy is justified
- evaluate appropriateness of inter-batch variance metric: confirm that the chosen metric (e.g., between-batch dispersion, homogeneity index) is statistically sound for the experimental design

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load interpolated feature table and metadata containing batch labels for each sample.
2. Invoke pycombat-based batch correction via pcpfm batch_correct with --by_batch parameter set to the batch metadata field.
3. Confirm output table preserves input sample and feature dimensions.
4. Calculate median inter-batch variance for representative high-intensity features before and after correction, grouped by batch field.
5. Validation: confirm corrected-table inter-batch variance is lower than uncorrected baseline, indicating successful batch effect attenuation without dimension loss.
6. References: source article (DOI: 10.1371/journal.pcbi.1011912)

## Workflow Ports

**Inputs:**

- `interpolated_feature_table` — Interpolated feature table (.tsv) with imputed missing values
- `sample_metadata_with_batches` — Sample metadata CSV with batch field

**Outputs:**

- `batch_corrected_feature_table` — Batch-corrected feature table (.tsv)
- `batch_correction_validation_report` — Quantitative validation report (JSON or text)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:shuzhao-li-lab__PythonCentricPipelineForMetabolomics`
- **Synthesized at:** 2026-06-15T12:53:24+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
