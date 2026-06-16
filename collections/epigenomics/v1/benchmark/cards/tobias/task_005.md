# SciTask Card: Extend TOBIAS footprinting to an ATAC-seq dataset deposited in GEO and report TF differential occupancy across two conditions

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:12:11.236771+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_tobias/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `data-analysis`, `statistical-analysis`
- DOI: `10.1038/s41467-020-18035-1`
- GitHub: `loosolab/TOBIAS`
- Input from: `task_003`

## Classification

- Task kind: `extension`
- Article type: `research-article`
- Primary domain: `transcriptomics`
- Subdomains: `gene-regulation`, `functional-genomics`
- Techniques: `enrichment-analysis`, `statistical-analysis`

## Research Question
Can the TOBIAS pipeline (bias correction, footprint scoring, and BINDetect) be applied to a two-condition ATAC-seq experiment to identify differential transcription factor occupancy between conditions?

## Connected Finding
ATAC-seq footprinting analysis can detect transcription factor binding through the visible depletion of Tn5 insertions around protein-bound sites, providing a basis for differential occupancy analysis across conditions.

## Task Description
Apply the complete TOBIAS pipeline (bias correction, footprint scoring, and BINDetect differential analysis) to a publicly available two-condition ATAC-seq dataset from GEO/SRA to identify differential transcription factor occupancy. Produce a differential TF occupancy results table (.tsv) and summary visualization (.pdf or .png).

## Inputs
- Raw ATAC-seq BAM alignments (condition 1) from GEO/SRA accession
- Raw ATAC-seq BAM alignments (condition 2) from GEO/SRA accession
- Peak annotations (BED or narrowPeak format) for both conditions
- Known TFBS motif library (PWM or MEME format)

## Expected Outputs
- Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, log2 fold-change, and p-values
- Summary visualization (.pdf or .png) showing top differential TFs and footprint patterns across conditions

## Expected Output File

- `differential_tf_occupancy.tsv`

## Landmark Outputs

- `bias_corrected_condition1.bam`
- `bias_corrected_condition2.bam`
- `footprint_scores_condition1.bw`
- `footprint_scores_condition2.bw`
- `bindetect_results.tsv`
- `summary_visualization.pdf`

## Tools
- TOBIAS

## Skills
- atac-seq-tn5-bias-correction
- transcription-factor-footprint-scoring
- differential-tf-occupancy-analysis
- motif-site-occupancy-comparison
- chromatin-accessibility-footprint-visualization

## Workflow Description
1. Retrieve raw ATAC-seq BAM files and peak annotations for two experimental conditions from GEO/SRA. 2. Run TOBIAS ATACorrect to perform Tn5 insertion bias correction on BAM files. 3. Execute TOBIAS FootprintScores to compute footprint enrichment signals genome-wide for each condition. 4. Apply TOBIAS BINDetect to perform differential transcription factor occupancy analysis between the two conditions, comparing footprint patterns at known TFBS motif sites. 5. Generate differential TF occupancy results table (.tsv) containing TF names, footprint scores, and statistical significance metrics. 6. Create summary visualization (.pdf or .png) showing top differential TFs, occupancy changes between conditions, and representative footprint patterns.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/BATF_footprint_comparison_all.png` | figure | False |
| `figures/BATF_footprint_comparison_subsets.png` | figure | False |
| `figures/BATF_heatmap.png` | figure | False |
| `figures/IRF1_footprint.png` | figure | False |
| `figures/atacorrect.png` | figure | False |
| `figures/bindetect.png` | figure | False |
| `figures/chr4-119628321-119629356.png` | figure | False |
| `figures/chr4-163701830-163702617.png` | figure | False |
| `figures/footprinting.png` | figure | False |
| `figures/network.png` | figure | False |
| `figures/tobias.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog or version history is documented for the TOBIAS repository

## Domain Knowledge
- ATAC-seq detects chromatin accessibility via Tn5 transposase insertion, with transcription factor binding visible as localized depletion of insertions (footprints) around bound protein sites.
- Tn5 insertion bias (sequence-dependent cleavage preference) must be corrected before footprint scoring to prevent confounding signal from intrinsic transposase preferences.
- BINDetect performs differential analysis by comparing footprint enrichment scores at known TFBS motif locations between conditions, identifying TFs with altered occupancy.
- Footprint depth and sharpness are key quality indicators; weak or diffuse footprints may indicate low TF occupancy or experimental noise, affecting statistical power.
- TOBIAS requires pre-aligned BAM files and called peaks; peak quality and sequencing depth directly influence footprint detection sensitivity.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Can the TOBIAS pipeline (bias correction, footprint scoring, and BINDetect) be applied to a two-condition ATAC-seq experiment to identify differential transcription factor occupancy between conditions?: 'TOBIAS is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] ATAC-seq footprinting analysis can detect transcription factor binding through the visible depletion of Tn5 insertions around protein-bound sites, providing a basis for differential occupancy analysis across conditions.: 'the local distribution of Tn5 insertions contains information about transcription factor binding due to the visible depletion of insertions around sites bound by protein - known as _footprints_'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] Raw ATAC-seq BAM alignments (condition 1) from GEO/SRA accession: 'publicly available two-condition ATAC-seq dataset from GEO/SRA'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Raw ATAC-seq BAM alignments (condition 2) from GEO/SRA accession: 'publicly available two-condition ATAC-seq dataset from GEO/SRA'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Peak annotations (BED or narrowPeak format) for both conditions: 'ATAC-seq footprinting analysis'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Known TFBS motif library (PWM or MEME format): 'transcription factor binding'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Differential TF occupancy results table (.tsv) with TF names, footprint scores per condition, log2 fold-change, and p-values: 'differential TF occupancy results table'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Summary visualization (.pdf or .png) showing top differential TFs and footprint patterns across conditions: 'summary plot'
- `ev_009` from `agent2_synthesis` (agent2_traced): [intro] TOBIAS: '**TOBIAS** is a collection of command-line bioinformatics tools for performing footprinting analysis on ATAC-seq data'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No changelog or version history is documented for the TOBIAS repository: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify that inputs include a two-condition ATAC-seq dataset from GEO/SRA with accession number and sample metadata
- verify file_exists for output differential TF occupancy results table (.tsv format)
- verify file_exists for output summary plot (.pdf or .png format)
- verify that .tsv output contains at least the following fields: TF name, condition 1 occupancy score, condition 2 occupancy score, differential occupancy metric, and statistical significance (p-value or adjusted p-value)
- verify row_count_equals for .tsv output is greater than 0 (at least one TF detected)
- verify that all numeric fields in .tsv (occupancy scores, p-values) are in valid ranges: occupancy scores between 0–1 or normalized scale, p-values between 0–1
- verify script_runs: TOBIAS pipeline commands execute without error on the input dataset (bias correction, footprint scoring, BINDetect modules complete successfully)
- verify that plot (.pdf/.png) displays at least one visualization comparing differential TF occupancy between the two conditions (e.g., scatter plot, bar chart, or heatmap), parameter-sensitive to visualization design choices and no canonical answer for plot layout

### Expert Review
- assess whether the selection of the two-condition ATAC-seq dataset and experimental design are appropriate for testing differential TF occupancy
- assess whether the TOBIAS pipeline parameters (bias correction thresholds, footprint scoring windows, BINDetect statistical model) are reasonable and justified for the chosen dataset
- assess whether the differential TF occupancy results are biologically plausible and consistent with known TF biology and the experimental conditions
- assess whether the summary plot effectively communicates the main findings and is suitable for publication or presentation

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** heavy

## Methodology Summary
1. Retrieve two-condition ATAC-seq BAM alignments and peak annotations from public repository (GEO/SRA).
2. Correct Tn5 transposase insertion bias in both conditions using TOBIAS ATACorrect.
3. Compute footprint enrichment signals genome-wide for each condition using TOBIAS FootprintScores.
4. Perform differential TF occupancy analysis between conditions at known TFBS motif sites using TOBIAS BINDetect.
5. Validation: Differential TF occupancy table and summary plot successfully generated with statistically significant TFs identified (p < 0.05) and footprint patterns visually distinct between conditions.
6. References: source article (DOI: 10.1038/s41467-020-18035-1)

## Workflow Ports

**Inputs:**

- `bam_condition1` — Raw ATAC-seq BAM alignments (condition 1) ← `task_003/tf_occupancy_table`
- `bam_condition2` — Raw ATAC-seq BAM alignments (condition 2)
- `peaks_bed` — Peak annotations in BED or narrowPeak format
- `motif_pwm` — Known TFBS motif library (PWM/MEME format)

**Outputs:**

- `diff_tf_table` — Differential TF occupancy results (.tsv)
- `summary_plot` — Summary visualization of differential TFs (.pdf or .png)

**Used:** `urn:asb:port:task_003/tf_occupancy_table`

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:loosolab__TOBIAS`
- **Synthesized at:** 2026-06-15T19:17:04+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
