# Workflow Challenge: `coll_champ_workflow`


> ChAMP is a comprehensive R package for DNA methylation array analysis on Illumina 450K and EPIC platforms, providing an integrated pipeline from raw data loading through quality control, normalization, and differential methylation detection to gene set enrichment analysis.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

ChAMP implements a complete methylation analysis workflow that accepts Illumina methylation data from .idat files or beta-value matrices. The package loads 485,512 probes for 450K arrays and 867,531 probes for EPIC arrays before quality filtering, then applies successive filtering to remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples. ChAMP provides multiple normalization methods (BMIQ, SWAN, PBC, Functional Normalization) to correct for type-I and type-II probe biases, implements SVD analysis capping at 20 components when Random Matrix Theory detects more than 20 latent variables, and supports ComBat batch effect correction. The package identifies differentially methylated positions and regions using limma, Bumphunter, ProbeLasso, and DMRcate algorithms, detects differentially methylated blocks, and performs gene set enrichment analysis with bias correction. Interactive web-based GUI functions enable visualization of results. When applied to the EPIC simulation dataset, champ.DMR() detects approximately 4700+ differentially methylated regions (fewer than the 5000 simulated due to single- or two-CpG regions not meeting DMR criteria), and champ.Block() detects no differentially methylated blocks in this dataset.

## Research questions

- Do champ.load() and champ.import() correctly load the expected numbers of probes before filtering for the HumanMethylation450 and EPIC array types?
- Does champ.filter() applied to the HumanMethylation450 test dataset remove probes with detection p-value > 0.01 and probes with fewer than 3 beads in at least 5% of samples?
- When champ.DMR() is applied to the EPIC simulation dataset using bumphunter-based detection, how many differentially methylated regions are identified?
- When champ.Block() is applied to the EPICSimData simulation dataset with arraytype='EPIC', are any differentially methylated blocks detected?
- Does champ.SVD() correctly limit the number of reported principal components to a maximum of 20 when Random Matrix Theory detects more than 20 latent components in the data?

## Methods overview

Load HumanMethylation450 test dataset (450K lung tumor data) into ChAMP environment using champ.load() function. Extract and record pre-filter probe count from loaded 450K object. Load EPICSimData test dataset using champ.load() or data() function into ChAMP environment. Extract and record pre-filter probe count from loaded EPIC object. Validation: Verify that 450K pre-filter probe count equals 485,512 and EPIC pre-filter probe count equals 867,531, confirming successful data import and correct array type detection. References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279) Load HumanMethylation450 test dataset (8 samples) into R environment using ChAMP data import functions Execute champ.filter() with default parameters on the raw methylation dataset Filter probes with detection p-value > 0.01 to remove low-confidence measurements Filter probes with fewer than 3 beads in ≥5% of samples to ensure sufficient bead replication Validate: Confirm that probe count decreases match expected filtering thresholds and that filtered matrix contains only high-quality probes References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279) Load EPICSimData from ChAMPdata using data() function in R environment Execute champ.DMR() on loaded EPIC simulation data with bumphunter algorithm selected Parse and tabulate detected DMR results with genomic coordinates and p-values Count total number of DMRs in output table Validation: Verify DMR count is within expected range of ~4700+, consistent with reported bumphunter simulation benchmark References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279) Load EPICSimData simulation dataset into R environment Execute champ.Block() with arraytype='EPIC' to detect differentially methylated blocks Launch Block.GUI() to visualize and inspect block detection results interactively Validation: Confirm that zero differentially methylated blocks are detected, matching expected behavior for this synthetic dataset References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279) Load normalized beta matrix (n × m: samples × probes) into R environment. Execute champ.SVD() function on the beta matrix to compute singular value decomposition and detect latent batch components using Random Matrix Theory. Retrieve the number of latent components detected; verify that output is capped at maximum 20 components even if RMT identifies more. Validation: Confirm that champ.SVD() component count ≤ 20 in all cases where Random Matrix Theory signals detection of components. References: GSE40279 (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279)

**Domain:** genomics

**Techniques:** batch-correction, differential-abundance-analysis, normalization, quality-control, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** ChAMP package is designed for DNA methylation array analysis, providing service from data loading to final gene set enrichment analysis. _[grounded: champ_system]_
- **(finding)** The current latest version of ChAMP is 2.29.1, which supports EPICv2. _[grounded: champ_system]_
- **(finding)** ChAMP version 2.29.1 must be used along with ChAMPdata version 2.23.1 or later. _[grounded: champ_system]_
- **(finding)** ChAMP provides Type-2 probe correction methods including SWAN, Peak Based Correction (PBC), and BMIQ. _[grounded: champ_system]_
- **(finding)** BMIQ is the default choice for Type-2 probe correction in ChAMP. _[grounded: champ_system]_
- **(finding)** ChAMP includes the Functional Normalization function offered by the minfi package. _[grounded: champ_system]_
- **(finding)** ChAMP implements the singular value decomposition (SVD) method for assessing batch effects. _[grounded: champ_system]_
- **(finding)** ChAMP has implemented the ComBat method for correction of multiple batch effects. _[grounded: champ_system]_
- **(finding)** ChAMP provides cell-type heterogeneity adjustment via RefbaseEWAS. _[grounded: champ_system]_
- **(finding)** ChAMP includes a function for inferring copy-number alterations from 450k or EPIC data. _[grounded: champ_system]_
- **(finding)** ChAMP offers three DMR detection methods: Probe Lasso, Bumphunter, and DMRcate. _[grounded: champ_system]_
- **(finding)** ChAMP includes a function to detect Differentially Methylated Blocks. _[grounded: champ_system]_
- **(finding)** ChAMP incorporates methods that correct for bias caused by unequal representation of probes among genes in Gene Set Enrichment Analysis. _[grounded: champ_system]_
- **(finding)** ChAMP incorporates the FEM package for inferring gene modules in user-specified gene networks that exhibit differential methylation between phenotypes. _[grounded: champ_system]_
- **(finding)** ChAMP provides a more comprehensive and complete analysis pipeline from reading original data files to final tertiary analysis results compared to other available packages. _[grounded: champ_system]_
- **(finding)** ChAMP provides Shiny and Plotly-based WebBrowser interactive analysis functions. _[grounded: champ_system]_
- **(finding)** R version 3.3 or above is required to install ChAMP. _[grounded: champ_system]_
- **(finding)** Bioconductor version 3.5 is the newest version recommended for ChAMP installation. _[grounded: champ_system]_
- **(finding)** Users must install the latest ChAMPdata package (version 2.8.1) to make ChAMP version above 2.8.3 work. _[grounded: champ_system]_
- **(finding)** The 450K test dataset contains 4 lung tumor samples (T) and 4 control samples (C). _[grounded: cond_array_450k]_
- **(finding)** The EPIC Simulation Data Set contains 16 samples.
- **(finding)** In the EPIC Simulation Data Set, 8 samples are simulated as control and 8 samples as case.
- **(finding)** In the EPIC Simulation Data Set, approximately 5000 regions were randomly chosen from the bumphunter clusterMaker() function. _[grounded: tool_bumphunter]_
- **(finding)** The EPIC Simulation Data Set contains less than 5000 DMRs (4700+) because some simulated DMRs contain only 1-2 CpGs. _[grounded: champ_system]_
- **(finding)** For 450K bead array data, before filtering for low quality probes, the dataset will include 485,512 probes. _[grounded: cond_array_450k]_
- **(finding)** For EPIC bead array data, before filtering probes the dataset will include 867,531 probes.
- **(finding)** The default loading method in ChAMP is 'ChAMP'. _[grounded: champ_system]_
- **(finding)** The 'ChAMP' method in champ.load() is a combination of champ.import() and champ.filter(). _[grounded: champ_system]_
- **(finding)** ChAMP filters probes with detection p-value greater than 0.01 by default. _[grounded: champ_system]_
- **(finding)** The default sample cutoff threshold for filtering is 0.1.
- **(finding)** ChAMP will filter out probes with less than 3 beads in at least 5% of samples per probe by default. _[grounded: champ_system]_
- **(finding)** ChAMP will by default filter out all non-CpG probes contained in the dataset. _[grounded: champ_system]_
- **(finding)** ChAMP will by default filter all SNP-related probes. _[grounded: champ_system]_
- **(finding)** ChAMP will by default filter all multi-hit probes. _[grounded: champ_system]_
- **(finding)** ChAMP will by default filter out all probes located in chromosome X and Y. _[grounded: champ_system]_
- **(finding)** champ.load() cannot perform filtering on beta matrix alone. _[grounded: champ_system]_
- **(finding)** ChAMP generates three main plots in quality control: mdsPlot, densityPlot, and dendrogram. _[grounded: champ_system]_
- **(finding)** QC.GUI() provides five interactive plots for quality control. _[grounded: comp_qc_gui]_
- **(finding)** ChAMP provides four methods for Type-2 probe normalization: BMIQ, SWAN, PBC, and Functional Normalization. _[grounded: champ_system]_
- **(finding)** BMIQ has been updated to version 1.6. _[grounded: tool_bmiq]_
- **(finding)** BMIQ version 1.6 provides better normalization for EPIC array data. _[grounded: tool_bmiq]_
- **(finding)** ChAMP uses Random Matrix Theory from the isva package to detect numbers of latent variables in SVD analysis. _[grounded: champ_system]_
- **(finding)** If more than 20 components are detected in SVD analysis, only the top 20 are selected.
- **(finding)** ComBat logit transforms beta values before adjustment and then computes the reverse logit transformation following adjustment. _[grounded: champ_system]_
- **(finding)** champ.DMP() implements the limma package to calculate p-values for differential methylation using a linear model. _[grounded: champ_system]_
- **(finding)** champ.DMP() supports numeric variables like age. _[grounded: champ_system]_
- **(finding)** champ.DMP() supports categorical variables which contain more than two phenotypes. _[grounded: champ_system]_
- **(finding)** For numeric variables, champ.DMP() conducts linear regression on each CpG site. _[grounded: champ_system]_
- **(finding)** For categorical variables, champ.DMP() performs contrast comparison between each two phenotypes. _[grounded: champ_system]_
- **(finding)** Three DMR algorithms are implemented in ChAMP: Bumphunter, ProbeLasso, and DMRcate. _[grounded: champ_system]_
- **(finding)** Bumphunter groups all probes into small clusters, then applies random permutation method to estimate candidate DMRs. _[grounded: tool_bumphunter]_
- **(finding)** DMRcate is a data-driven approach that is agnostic to all annotations except for chromosomal coordinates. _[grounded: champ_system]_
- **(finding)** champ.DMR() only takes categorical covariates with exactly two phenotypes. _[grounded: champ_system]_
- **(finding)** The ChAMP pipeline can run 200 samples successfully on a computer with 8GB of memory. _[grounded: champ_system]_
- **(finding)** The champ.load() function uses the most memory in the ChAMP pipeline. _[grounded: champ_system]_
- **(finding)** Users can conduct nearly all ChAMP analysis even if they are not starting from raw .idat files, as long as they have a methylation beta matrix and corresponding phenotypes file. _[grounded: champ_system]_

**Speculative claims (excluded from scoring):**
- **(finding)** BMIQ may not converge and provide output for certain samples if the methylation distribution deviates markedly from a 3-state beta-mixture distribution. _[grounded: tool_bmiq]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- SWAN, PBC, or FunctionalNormalization as alternatives to BMIQ for type-II probe correction
- Multiple DMR detection algorithms: Bumphunter, ProbeLasso, or DMRcate

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- ChAMP version 2.8.3 and above requires ChAMPdata package version 2.8.1 or later

## Steps

### Step `task_001`
- Title: Reproduce the pre-filter probe counts for 450K and EPIC arrays in champ.load()
- Task kind: `reproduction`
- Task: Load HumanMethylation450 and EPICSimData test datasets using champ.load() and verify that pre-filter probe counts match expected values: 485,512 probes for 450K and 867,531 probes for EPIC.
- Inputs:
  - HumanMethylation450 test dataset (450K lung tumor data: 8 samples, 4 tumor + 4 control)
  - EPICSimData test dataset
- Expected outputs:
  - Loaded 450K dataset object with pre-filter probe count of 485,512 probes
  - Loaded EPIC dataset object with pre-filter probe count of 867,531 probes
- Tools: ChAMP
- Landmark output files: 450k_loaded_object.rds, epic_loaded_object.rds

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the detection p-value and beadcount filter thresholds applied by champ.filter()
- Task kind: `reproduction`
- Task: Apply the champ.filter() function to the HumanMethylation450 test dataset using default parameters and verify that probes with detection p-value > 0.01 and probes with fewer than 3 beads in ≥5% of samples are removed.
- Inputs:
  - task_001.expected_outputs[0]: Loaded 450K dataset object with pre-filter probe count of 485,512 probes
  - HumanMethylation450 test dataset (450k lung tumor data with 8 samples: 4 tumor, 4 control)
- Expected outputs:
  - Filtered methylation matrix with low-quality probes removed
  - Quality control report documenting probe filtering statistics (detection p-value and bead count thresholds applied)
- Tools: ChAMP
- Landmark output files: raw_probe_counts.txt, detection_pvalue_filtered_counts.txt, bead_count_filtered_counts.txt, champ_filter_summary.txt
- Primary expected artifact: `filtered_methylation_matrix.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the EPICSimData DMR count result using champ.DMR()
- Task kind: `reproduction`
- Task: Load the EPICSimData simulation dataset and run champ.DMR() to detect differentially methylated regions (DMRs), verifying that the detected DMR count falls within the expected range (~4700+) as reported for bumphunter-based simulation.
- Inputs:
  - EPICSimData (EPIC simulation dataset)
- Expected outputs:
  - DMR detection results table with genomic coordinates and statistical metrics
  - DMR count (integer, expected ~4700+)
- Tools: ChAMP, Bumphunter
- Landmark output files: epic_sim_data_loaded.rda, dmr_detection.log, dmr_results.csv
- Primary expected artifact: `dmr_results.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reproduce the absence of differential methylation blocks in EPICSimData using champ.Block()
- Task kind: `reproduction`
- Task: Execute champ.Block() on the EPICSimData dataset with arraytype='EPIC' parameter and validate via Block.GUI() that the analysis correctly identifies zero differentially methylated blocks, confirming the expected behavior for this simulation dataset.
- Inputs:
  - EPICSimData (built-in simulation dataset)
- Expected outputs:
  - Block detection result object with zero differentially methylated blocks
  - Interactive Block.GUI() visualization confirming no blocks detected
- Tools: ChAMP

### Step `task_005`
- Depends on: `task_002`
- Title: Reproduce the SVD maximum components cap of 20 reported by champ.SVD()
- Task kind: `reproduction`
- Task: Execute champ.SVD() on a normalized beta matrix and verify that the function caps reported latent components at 20 when Random Matrix Theory detects more than 20 components.
- Inputs:
  - task_002.expected_outputs[0]: Filtered methylation matrix with low-quality probes removed
  - Normalized beta matrix from HumanMethylation450 test dataset or GSE40279
- Expected outputs:
  - SVD analysis report with latent component count capped at 20
- Tools: ChAMP
- Primary expected artifact: `svd_report.txt`

## Final expected outputs

- `DMR detection results table with genomic coordinates and statistical metrics` (type: file, tolerance: hash)
- `DMR count (integer, expected ~4700+)` (type: file, tolerance: hash)
- `Block detection result object with zero differentially methylated blocks` (type: file, tolerance: hash)
- `Interactive Block.GUI() visualization confirming no blocks detected` (type: file, tolerance: hash)
- `SVD analysis report with latent component count capped at 20` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_champ_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "DMR detection results table with genomic coordinates and statistical metrics": "<locator>",
    "DMR count (integer, expected ~4700+)": "<locator>",
    "Block detection result object with zero differentially methylated blocks": "<locator>",
    "Interactive Block.GUI() visualization confirming no blocks detected": "<locator>",
    "SVD analysis report with latent component count capped at 20": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
