# SciTask Card: Reproduce the detection p-value and beadcount filter thresholds applied by champ.filter()

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T19:16:49.189128+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_epigenomics/coll_champ/synthesized_package`
- Domain: `bioinformatics`
- Subtask categories: `data-processing`, `quality-control`
- GitHub: `YuanTian1991/ChAMP`
- Input from: `task_001`

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `genomics`
- Subdomains: `gene-regulation`, `biomarker-discovery`
- Techniques: `batch-correction`, `differential-abundance-analysis`, `normalization`, `quality-control`, `statistical-analysis`
- Keywords: `dna methylation` · `illumina beadarray` · `450k array` · `epic array` · `differentially methylated positions` · `differentially methylated regions` · `type-ii probe normalization` · `batch effect correction` · `gene set enrichment analysis` · `quality control` · `normalization methods` · `idat files` · `beta values`

## Research Question
Does champ.filter() applied to the HumanMethylation450 test dataset remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples?

## Connected Finding
champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.

## Task Description
Apply the champ.filter() function to the HumanMethylation450 test dataset using default parameters and verify that probes with detection p-value > 0.01 and probes with fewer than 3 beads in ≥5% of samples are removed.

## Inputs
- task_001.expected_outputs[0]: Loaded 450K dataset object with pre-filter probe count of 485,512 probes
- HumanMethylation450 test dataset (450k lung tumor data with 8 samples: 4 tumor, 4 control)

## Expected Outputs
- Filtered methylation matrix with low-quality probes removed
- Quality control report documenting probe filtering statistics (detection p-value and bead count thresholds applied)

## Expected Output File

- `filtered_methylation_matrix.csv`

## Landmark Outputs

- `raw_probe_counts.txt`
- `detection_pvalue_filtered_counts.txt`
- `bead_count_filtered_counts.txt`
- `champ_filter_summary.txt`

## Tools
- ChAMP

## Skills
- dna-methylation-quality-control
- probe-detection-pvalue-filtering
- bead-count-threshold-filtering
- illumina-methylation-array-preprocessing
- 450k-array-data-processing

## Workflow Description
1. Load the HumanMethylation450 test dataset (450k lung tumor data containing 8 samples: 4 tumor and 4 control) using ChAMP data import functions. 2. Apply champ.filter() with default parameters to remove low-quality probes. 3. Verify that probes with detection p-value > 0.01 have been filtered out by comparing pre- and post-filter probe counts. 4. Verify that probes with fewer than 3 beads in at least 5% of samples have been removed by examining bead count distributions before and after filtering. 5. Generate a filtered probe matrix and quality control report documenting the number of probes retained and removed.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/CNAimage.jpg` | figure | False |
| `figures/CNAtext.jpg` | figure | False |
| `figures/DMR.jpg` | figure | False |
| `figures/DMRdistributionplot.png` | figure | False |
| `figures/DMRoutput.jpg` | figure | False |
| `figures/MVP1.jpg` | figure | False |
| `figures/MVP2.jpg` | figure | False |
| `figures/MVP3.jpg` | figure | False |
| `figures/checkBMIQ.jpg` | figure | False |
| `figures/densityPlot.jpg` | figure | False |
| `figures/failedProbes.jpg` | figure | False |
| `figures/lasso.jpg` | figure | False |
| `figures/logo4.jpg` | figure | False |
| `figures/mdsPlot.jpg` | figure | False |
| `figures/probeFeatures.jpg` | figure | False |
| `figures/radius.jpg` | figure | False |
| `figures/rawSampleCluster.jpg` | figure | False |
| `figures/sampleSheetexample.jpg` | figure | False |
| `figures/studyInfo.jpg` | figure | False |
| `figures/studyInfo.png` | figure | False |
| `paper.md` | main_article | True |

## Data Deposits

| Kind | Accession | URL | Evidence |
|---|---|---|---|
| geo_series | `GSE40279` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279 | lot looks not complicated. Below we used another plot from [GSE40279](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE4027 |

## Missing Information
- No changelog documenting filter() function behavior or parameter defaults
- No methods section provided describing the champ.filter() function implementation or default parameter values

## Domain Knowledge
- Detection p-value > 0.01 is the standard threshold for marking low-confidence probes in Illumina methylation arrays and must be filtered prior to downstream analysis.
- Bead count thresholds protect against unreliable intensity measurements; fewer than 3 beads per probe in ≥5% of samples indicates insufficient technical replication and probe removal.
- ChAMP.filter() integrates these two quality filters as default parameters for HumanMethylation450 (450k) arrays, removing problematic probes before normalization.
- The 450k assay interrogates ~480,000 probes across the human genome using two probe types (Type I and Type II) that require different correction methods.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [other] Does champ.filter() applied to the HumanMethylation450 test dataset remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples?: 'First filter is for probes with detection p-value (default > 0.01). This utilises detection p-value stored in .idat file. Second, ChAMP will filter out probes with <3 beads in at least 5% of samples'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] champ.filter() applies two successive filtering steps by default: (1) removal of probes with detection p-value > 0.01, and (2) removal of probes with fewer than 3 beads in at least 5% of samples per probe.: 'First filter is for probes with detection p-value (default > 0.01). This utilises detection p-value stored in .idat file. Second, ChAMP will filter out probes with <3 beads in at least 5% of samples'
- `ev_003` from `agent2_synthesis` (agent2_traced): [intro] HumanMethylation450 test dataset (450k lung tumor data with 8 samples: 4 tumor, 4 control): 'The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [intro] Filtered methylation matrix with low-quality probes removed: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading'
- `ev_005` from `agent2_synthesis` (agent2_traced): [intro] Quality control report documenting probe filtering statistics (detection p-value and bead count thresholds applied): 'provides a pipeline that integrates currently available 450k and EPIC analysis methods'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] ChAMP: 'ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis'
- `ev_007` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting filter() function behavior or parameter defaults: 'No changelog found.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] No methods section provided describing the champ.filter() function implementation or default parameter values: 'Document contains only title metadata and introduction; no methods section present'

## Evaluation Strategy
### Direct Checks
- verify that champ.filter() function exists in the ChAMP package source code at github:YuanTian1991__ChAMP
- verify that HumanMethylation450 test dataset is loadable from ChAMPdata package (version >= 2.23.1)
- script_runs: execute champ.filter() on HumanMethylation450 test dataset with default parameters and confirm no errors occur
- verify that output is a filtered methylation matrix or object with reduced probe count compared to input
- expert_review required: confirm that probes with detection p-value > 0.01 were removed by comparing probe counts pre- and post-filtering (requires validation against filtering source code or documentation)

### Expert Review
- inspect ChAMP package source code or documentation to confirm that champ.filter() removes probes with detection p-value > 0.01 by default
- inspect ChAMP package source code or documentation to confirm that champ.filter() removes probes with fewer than 3 beads in at least 5% of samples by default
- validate that the reported filtering thresholds (detection p-value > 0.01, bead count < 3 in ≥5% samples) match the actual implementation in default parameters

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load HumanMethylation450 test dataset (8 samples) into R environment using ChAMP data import functions
2. Execute champ.filter() with default parameters on the raw methylation dataset
3. Filter probes with detection p-value > 0.01 to remove low-confidence measurements
4. Filter probes with fewer than 3 beads in ≥5% of samples to ensure sufficient bead replication
5. Validate: Confirm that probe count decreases match expected filtering thresholds and that filtered matrix contains only high-quality probes
6. References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279)

## Workflow Ports

**Inputs:**

- `raw_methylation_data` — HumanMethylation450 test dataset

**Outputs:**

- `filtered_methylation_matrix` — Filtered probe matrix after quality control
- `filter_qc_report` — Filtering statistics and quality control report

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:YuanTian1991__ChAMP`
- **Synthesized at:** 2026-06-15T19:25:01+00:00

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
