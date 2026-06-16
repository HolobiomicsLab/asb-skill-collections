# Workflow Challenge: `coll_methylkit_workflow`


> methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing data, designed to handle RRBS and target-capture methods. It provides functionality for reading methylation calls, comparative analysis, differential methylation detection, and annotation of methylated regions.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

methylKit implements a comprehensive workflow for analyzing DNA methylation from bisulfite sequencing experiments. The package reads methylation call files into methylRawList objects, performs quality filtering by coverage, and merges samples across common sites using the unite() function to produce methylBase objects. Differential methylation is calculated via calculateDiffMeth() using logistic regression or Fisher's exact test depending on sample size, with p-values adjusted to q-values by the SLIM method; getMethylDiff() then extracts hyper- and hypo-methylated bases using q-value and percent-methylation-difference cutoffs. Sample relationships are visualized through clusterSamples() producing dendrograms and PCASamples() generating scree plots and PC1/PC2 scatter plots. Annotation integrates with genomation to classify differentially methylated regions by overlap with gene features (promoters, exons, introns) and CpG islands using annotateWithGeneParts() and annotateWithFeatureFlank(). The package describes mechanisms for memory-efficient analysis via methylRawListDB objects that store methylation data in tabix-indexed bgzipped files on disk, and for correcting overdispersion in logistic regression models by calculating a scaling parameter φ = X²/(N-P) to adjust variance estimates.

## Research questions

- When differentially methylated bases are extracted from a methylDiff object using getMethylDiff() with q-value < 0.01 and 25% methylation difference thresholds, what are the counts of hyper-methylated versus hypo-methylated bases?
- Does the methylKit package support storing methylation data in tabix-indexed bgzipped files on disk, and if so, how are the database path and metadata header configured?
- How do the four samples (test1, test2, ctrl1, ctrl2) cluster based on methylation similarity, and what are their relationships in principal component space?
- Does overdispersion correction in calculateDiffMeth() with overdispersion='MN' produce more stringent statistical tests (higher q-values) compared to uncorrected differential methylation analysis?
- What is the distribution of differentially methylated bases across gene annotation features (promoters, exons, introns) and CpG island contexts (CpGi islands vs. shores)?

## Methods overview

Load methylation call files using methRead() to obtain methylRawList objects from CpG text files. Merge samples using unite() function to create methylBase object containing only universally covered bases. Calculate differential methylation using calculateDiffMeth(), which applies Fisher's exact test or logistic regression based on sample count. Extract differentially methylated bases using getMethylDiff() with q-value < 0.01 and ≥25% methylation difference thresholds. Validation: Confirm hyper-methylated and hypo-methylated base counts in output methylDiff object match published vignette values. Load example CpG methylation files into R using methylKit's methRead() function with dbtype='tabix' parameter to enable tabix-backed database storage mode. Inspect the resulting methylRawListDB object to confirm the dbpath slot contains file-system paths to bgzipped tabix files. Read and parse tabix file headers to extract and verify methylKit version metadata. Validation: Confirm dbpath slot is non-empty, all referenced tabix files exist on disk with valid .bgz and .tbi extensions, and header version field is ≥ 1.13.1. Load the united methylBase object containing merged methylation calls across all samples. Apply hierarchical clustering via clusterSamples() to compute pairwise sample distances and construct a dendrogram. Apply principal component analysis via PCASamples() to identify major axes of methylation variation. Generate scree plot showing cumulative and per-component variance explained by principal components. Generate PC1 vs. PC2 scatter plot to visualize sample grouping in the first two principal components. Validation: Dendrogram and PCA plots should visually match the vignette outputs and support expected sample stratification based on methylation profiles. Generate synthetic methylation data using dataSim() with 6 replicates and 1000 genomic sites to create a methylBase object. Run calculateDiffMeth() with overdispersion correction method set to MN and statistical test set to Chi-square. Run calculateDiffMeth() again without overdispersion correction (baseline) on the same methylBase object. Extract and tabulate q-value statistics from both runs and compare distributions. Validation: Confirm that average q-values from the MN-corrected run are higher than the uncorrected baseline, confirming more stringent multiple-testing control. Load the methylDiff object and gene annotation (BED format) into the R environment. Execute annotateWithGeneParts() to compute overlaps between differentially methylated bases and promoter/exon/intron regions. Execute annotateWithFeatureFlank() to classify bases relative to CpG islands and shore regions. Aggregate overlap counts for each genomic feature class and compute percentages relative to total differentially methylated bases. Validation: Output table percentages sum to 100% per category (gene parts and CpG island features are mutually exclusive within their respective groups), and counts match vignette reference statistics.

**Domain:** genomics

**Techniques:** differential-abundance-analysis, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. _[grounded: methylKit_system]_
- **(finding)** methylKit is designed to deal with sequencing data from RRBS and its variants. _[grounded: methylKit_system]_
- **(finding)** DNA methylation in vertebrates typically occurs at CpG dinucleotides.
- **(finding)** Non-CpG cytosines are methylated in certain tissues such as embryonic stem cells.
- **(finding)** DNA methylation can act as an epigenetic control mechanism for gene regulation.
- **(finding)** Methylation can hinder binding of transcription factors.
- **(finding)** Methylated bases can be bound by methyl-binding-domain proteins which recruit chromatin remodeling factors.
- **(finding)** Aberrant DNA methylation patterns have been associated with many human malignancies.
- **(finding)** DNA methylation patterns can be used in a predictive manner for disease.
- **(finding)** In malignant tissues, DNA is either hypo-methylated or hyper-methylated compared to normal tissue.
- **(finding)** Hypo-methylation is traditionally associated with gene transcription on regulatory regions.
- **(finding)** Hyper-methylation is traditionally associated with gene repression.
- **(finding)** In bisulfite sequencing, bisulfite converts cytosine residues to uracil but leaves 5-methylcytosine residues unaffected.
- **(finding)** The methylation status of a base determined by high-throughput bisulfite sequencing is a percentage rather than a binary score.
- **(finding)** The percentage of methylation determines how many of the bases aligning to a given cytosine location have actual C bases in the reads.
- **(finding)** Sequencing errors contribute to non-binary methylation responses in high-throughput sequencing experiments.
- **(finding)** Incomplete bisulfite conversion contributes to non-binary methylation responses.
- **(finding)** Heterogeneity of samples and heterogeneity of paired chromosomes from the same sample contribute to non-binary methylation responses.
- **(finding)** The methRead function returns a methylRawList object which stores methylation information per sample for each covered base. _[grounded: comp_methylRawList]_
- **(finding)** By default methRead requires a minimum coverage of 10 reads per base. _[grounded: tool_methRead]_
- **(finding)** methylKit offers methylDB classes that store methylation information in an external bgzipped file indexed by tabix. _[grounded: methylKit_system]_
- **(finding)** methylDB objects include methylRawListDB, methylRawDB, methylBaseDB and methylDiffDB classes. _[grounded: comp_methylRawListDB]_
- **(finding)** Most functions in methylKit work with methylDB objects the same way as with normal methylKit objects. _[grounded: methylKit_system]_
- **(finding)** Bismark is a popular aligner for bisulfite sequencing reads. _[grounded: tool_Bismark]_
- **(finding)** The processBismarkAln function reads Bismark SAM/BAM files as methylRaw or methylRawList objects. _[grounded: comp_methylRawList]_
- **(finding)** SAM files must be sorted by chromosome and read position columns for processBismarkAln. _[grounded: tool_processBismarkAln]_
- **(finding)** BAM files should be sorted and indexed for use with processBismarkAln. _[grounded: tool_processBismarkAln]_
- **(finding)** Typical percent methylation histograms should have two peaks on both ends.
- **(finding)** In any given cell, any given base is either methylated or not.
- **(finding)** Experiments suffering from PCR duplication bias will have a secondary peak towards the right hand side of the coverage histogram.
- **(finding)** The unite function merges all samples for base-pair locations covered in all samples. _[grounded: tool_unite]_
- **(finding)** Setting destrand=TRUE in unite will merge reads on both strands of a CpG dinucleotide. _[grounded: tool_unite]_
- **(finding)** The default value of destrand in unite is FALSE. _[grounded: tool_unite]_
- **(finding)** Setting destrand=TRUE in unite is only advised when looking at CpG methylation. _[grounded: tool_unite]_
- **(finding)** The unite function returns a methylBase object for comparative analysis. _[grounded: comp_methylBase]_
- **(finding)** By default, unite produces bases/regions covered in all samples. _[grounded: tool_unite]_
- **(finding)** The min.per.group option in unite can relax the requirement for coverage in all samples. _[grounded: tool_unite]_
- **(finding)** The getCorrelation function can plot scatter plot and correlation coefficients or print a correlation matrix. _[grounded: tool_getCorrelation]_
- **(finding)** The clusterSamples function clusters samples and draws a dendrogram. _[grounded: tool_clusterSamples]_
- **(finding)** Setting plot=FALSE in clusterSamples returns a dendrogram object for manipulation. _[grounded: tool_clusterSamples]_
- **(finding)** The PCASamples function can plot a scree plot for importance of components. _[grounded: tool_PCASamples]_
- **(finding)** The assocComp function checks which principal components are statistically associated with potential batch effects. _[grounded: tool_assocComp]_
- **(finding)** The assocComp function uses Kruskal-Wallis test or Wilcoxon test for categorical attributes. _[grounded: tool_assocComp]_
- **(finding)** The assocComp function uses correlation test for numerical attributes. _[grounded: tool_assocComp]_
- **(finding)** The removeComp function removes principal components from methylation data. _[grounded: tool_removeComp]_
- **(finding)** The reconstruct function reconstructs a corrected methylBase object from a corrected percent methylation matrix. _[grounded: comp_methylBase]_
- **(finding)** The tileMethylCounts function tiles the genome with windows and summarizes methylation information. _[grounded: tool_tileMethylCounts]_
- **(finding)** The calculateDiffMeth function is the main function to calculate differential methylation. _[grounded: tool_calculateDiffMeth]_
- **(finding)** calculateDiffMeth uses Fisher's exact test or logistic regression depending on sample size per each set. _[grounded: tool_calculateDiffMeth]_
- **(finding)** P-values in calculateDiffMeth are adjusted to Q-values using SLIM method. _[grounded: tool_calculateDiffMeth]_
- **(finding)** calculateDiffMeth automatically uses logistic regression when there are replicates. _[grounded: tool_calculateDiffMeth]_
- **(finding)** The pool function can be used to pool replicates for Fisher's exact test. _[grounded: tool_calculateDiffMeth]_
- **(finding)** The getMethylDiff function selects differentially methylated regions based on q-value and percent methylation difference cutoffs. _[grounded: tool_getMethylDiff]_
- **(finding)** The overdispersion parameter in logistic regression accounts for variance greater than expected by the binomial distribution.
- **(finding)** Overdispersion correction is not applied by default in calculateDiffMeth. _[grounded: tool_calculateDiffMeth]_
- **(finding)** Setting overdispersion="MN" applies overdispersion correction in calculateDiffMeth. _[grounded: tool_calculateDiffMeth]_
- **(finding)** The F-test is automatically used when overdispersion correction is applied in calculateDiffMeth. _[grounded: tool_calculateDiffMeth]_
- **(finding)** Covariates can be included in calculateDiffMeth analysis to separate their influence from treatment effect. _[grounded: tool_calculateDiffMeth]_
- **(finding)** methylKit objects can be coerced to GRanges objects from GenomicRanges package. _[grounded: methylKit_system]_
- **(finding)** The genomation package can be used to annotate differentially methylated regions with gene annotation. _[grounded: tool_genomation]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Fisher's exact test can be forced by pooling replicates using pool() function when you have multiple samples per group
- Multiple-cores can be utilized for differential methylation calculation using mc.cores option
- Bismark methylation extractor or methylDackel can be used to extract methylation calls instead of processBismarkAln()

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- methylKit is designed for bisulfite sequencing data (WGBS or RRBS) and not suitable for affinity-based methods like MIRA-seq or methylation arrays

## Steps

### Step `task_001`
- Title: Reproduce differential methylation analysis using calculateDiffMeth on example CpG files
- Task kind: `reproduction`
- Task: Merge methylKit CpG samples using unite(), calculate differential methylation with calculateDiffMeth(), and extract differentially methylated bases meeting q-value < 0.01 and ≥25% methylation difference thresholds using getMethylDiff(). Output a methylDiff object with hyper- and hypo-methylated base counts.
- Inputs:
  - methylKit example CpG text files (methylation call format from bisulfite sequencing)
- Expected outputs:
  - methylDiff object containing differentially methylated bases with hyper- and hypo-methylated base counts
- Tools: methylKit, R
- Landmark output files: methylRawList.rds, methylBase_united.rds, methylDiff_raw.rds

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the methylRawListDB tabix-backed storage pipeline for memory-efficient sample loading
- Task kind: `component_reconstruction`
- Task: Call methRead() with dbtype='tabix' on CpG methylation files to produce a methylRawListDB object persisted as bgzipped tabix files, and verify that the dbpath slot is correctly populated with tabix file headers containing methylKit metadata (version ≥ 1.13.1).
- Inputs:
  - Example CpG methylation call files in methylKit-compatible format (e.g., from bisulfite sequencing via Bismark)
- Expected outputs:
  - methylRawListDB object with dbpath slot populated and pointing to bgzipped tabix files on disk
  - Tabix file header containing methylKit metadata and version information (≥ 1.13.1)
- Tools: methylKit, R
- Landmark output files: methylRawListDB_object.rds, *.bgz, *.bgz.tbi

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce sample clustering and PCA outputs from the methylBase object
- Task kind: `reproduction`
- Task: From a united methylBase object, perform unsupervised clustering and dimensionality reduction to obtain a dendrogram and principal component analysis plots (scree plot and PC1/PC2 scatter) visualizing sample relationships.
- Inputs:
  - task_001.expected_outputs[0]: methylDiff object containing differentially methylated bases with hyper- and hypo-methylated base counts
  - methylBase object from unite() on example CpG files
- Expected outputs:
  - Dendrogram object showing hierarchical clustering of samples
  - Scree plot showing variance explained by each principal component (PNG or PDF)
  - PC1/PC2 scatter plot visualization (PNG or PDF)
- Tools: methylKit, R, knitr
- Landmark output files: dendrogram.rda, scree_plot.pdf, pca_scatter_pc1_pc2.pdf

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct overdispersion-corrected differential methylation using dataSim and calculateDiffMeth with overdispersion='MN'
- Task kind: `component_reconstruction`
- Task: Simulate a methylBase object using dataSim() with 6 replicates and 1000 methylation sites, then run calculateDiffMeth() with overdispersion correction (MN method) and Chi-square test. Verify that the function returns a methylDiff object and that the q-value distribution is more stringent (higher average q-values) compared to an uncorrected baseline run.
- Inputs:
  - methylKit package with dataSim() and calculateDiffMeth() functions available in R environment
- Expected outputs:
  - methylDiff object containing differential methylation test statistics, p-values, and q-values from the overdispersion-corrected run
  - Comparison report or figure showing q-value distributions (corrected vs. uncorrected) demonstrating that MN-corrected q-values are higher on average
- Tools: methylKit, R
- Landmark output files: simulated_methylbase.rds, methyldiff_corrected.rds, methyldiff_uncorrected.rds, qvalue_stats_comparison.csv
- Primary expected artifact: `qvalue_distribution_comparison.csv`

### Step `task_005`
- Depends on: `task_001`
- Title: Reproduce genomation-based annotation of differentially methylated bases with refseq and CpG island BED files
- Task kind: `reproduction`
- Task: Annotate a methylDiff object from calculateDiffMeth() with gene parts (promoter/exon/intron) and CpG island features using annotateWithGeneParts() and annotateWithFeatureFlank(), then generate and report a percentage overlap summary table matching the vignette reference statistics.
- Inputs:
  - task_001.expected_outputs[0]: methylDiff object containing differentially methylated bases with hyper- and hypo-methylated base counts
  - methylDiff object from calculateDiffMeth() containing differentially methylated bases with q-value and methylation difference annotations
  - refseq.hg18.bed.txt gene annotation file (BED format) bundled with methylKit package
  - cpgi.hg18.bed.txt CpG island annotation file (BED format) bundled with methylKit package
- Expected outputs:
  - Percentage overlap summary table showing the proportion of differentially methylated bases overlapping promoter, exon, and intron regions, and CpG island and shore categories
- Tools: methylKit, genomation, GenomicFeatures, R
- Landmark output files: gene_parts_annotation.bed, cpgi_annotation.bed, annotation_overlap_summary.csv
- Primary expected artifact: `annotation_overlap_summary.csv`

## Final expected outputs

- `Dendrogram object showing hierarchical clustering of samples` (type: file, tolerance: hash)
- `Scree plot showing variance explained by each principal component (PNG or PDF)` (type: file, tolerance: hash)
- `PC1/PC2 scatter plot visualization (PNG or PDF)` (type: file, tolerance: hash)
- `methylDiff object containing differential methylation test statistics, p-values, and q-values from the overdispersion-corrected run` (type: file, tolerance: hash)
- `Comparison report or figure showing q-value distributions (corrected vs. uncorrected) demonstrating that MN-corrected q-values are higher on average` (type: file, tolerance: hash)
- `Percentage overlap summary table showing the proportion of differentially methylated bases overlapping promoter, exon, and intron regions, and CpG island and shore categories` (type: file, tolerance: hash)

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

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_methylkit_workflow",
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
    "Dendrogram object showing hierarchical clustering of samples": "<locator>",
    "Scree plot showing variance explained by each principal component (PNG or PDF)": "<locator>",
    "PC1/PC2 scatter plot visualization (PNG or PDF)": "<locator>",
    "methylDiff object containing differential methylation test statistics, p-values, and q-values from the overdispersion-corrected run": "<locator>",
    "Comparison report or figure showing q-value distributions (corrected vs. uncorrected) demonstrating that MN-corrected q-values are higher on average": "<locator>",
    "Percentage overlap summary table showing the proportion of differentially methylated bases overlapping promoter, exon, and intron regions, and CpG island and shore categories": "<locator>"
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
