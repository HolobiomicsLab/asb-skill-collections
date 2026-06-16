# Workflow Challenge: `coll_tximport_workflow`


> tximport is an R package that imports and summarizes transcript-level abundance estimates from multiple quantification tools (salmon, kallisto, RSEM, StringTie, alevin, oarfish, and others) into gene-level matrices for downstream differential expression analysis. The package provides mechanisms for gene-level analysis while correcting for changes in average transcript length across samples through offset matrices compatible with edgeR, DESeq2, and limma-voom.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

tximport imports transcript-level abundance, estimated counts, and transcript lengths from quantification tools and summarizes them into matrices suitable for statistical analysis packages such as edgeR, DESeq2, and limma-voom. The vignette demonstrates tximport's functionality across multiple quantification methods, including salmon, kallisto, RSEM, StringTie, alevin, and oarfish. Key workflows reproduced include: importing gene-level estimates from salmon quantification files using a tx2gene mapping to produce abundance, count, and length matrices; showing equivalence between obtaining gene-level counts via direct gene-level summarization (txOut=FALSE) versus transcript-level import followed by summarizeToGene function; and importing transcript-level estimates from oarfish long-read quantification. The vignette also describes mechanisms provided by tximport for downstream analysis, including how DESeq2::DESeqDataSetFromTximport automatically constructs an appropriate offset matrix from transcript-length estimates to correct for differential isoform usage, and how DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates for transcript-level differential expression analysis.

## Research questions

- Can tximport successfully import salmon transcript-level quantification files and produce gene-level counts, abundance, and length matrices using a pre-constructed tx2gene mapping?
- Do transcript-level estimates obtained via tximport with txOut=TRUE produce identical gene-level count matrices after summarization with summarizeToGene as compared to direct gene-level import using txOut=FALSE?
- When DESeq2::DESeqDataSetFromTximport is called with a tximport output object (txi) and a sample table, does the resulting DESeqDataSet correctly embed the transcript-length-derived offset matrix needed for gene-level differential expression analysis using the 'original counts and offset' method?
- How does edgeR::DGEListFromTximport with divide=TRUE process tximport inferential replicates to generate transcript-level divided counts for differential expression analysis?
- Can tximport successfully import transcript-level quantification data from oarfish-quantified long-read RNA-seq samples using the type='oarfish' parameter with txOut=TRUE to produce transcript-level matrices?

## Methods overview

Load the tx2gene.gencode.v27.csv file containing transcript-to-gene ID mappings. Read six salmon quant.sf.gz files and parse quantification estimates using tximport with type='salmon'. Aggregate transcript-level estimates to gene-level by summing abundance and counts across all transcripts per gene, weighted by effective length. Extract and export three gene-level matrices: counts (read assignments), abundance (TPM), and length (effective transcript length per sample). Validation: confirm that output matrices have correct dimensions (genes × samples), contain non-negative numeric values, and match expected gene IDs from tx2gene mapping. References: source article (DOI: 10.12688/f1000research.7563.1) Load salmon quantification files and tx2gene mapping, then import with tximport (type='salmon', txOut=TRUE) to obtain transcript-level matrices. Apply summarizeToGene to collapse transcript-level counts to gene level using the tx2gene mapping. Separately import the same salmon files with tximport (txOut=FALSE, default) to generate gene-level matrices directly. Compare gene-level count matrices from both routes using all-equal or matrix-equality check. Validation: Report success when both gene-level count matrices are bit-for-bit identical. References: source article (DOI: 10.12688/f1000research.7563.1) Load tximport list (txi) containing transcript abundance, counts, and length matrices from salmon quantification files. Prepare a sample metadata table (colData) with two-condition group assignments for each sample. Invoke DESeq2::DESeqDataSetFromTximport with the txi object and sample table to construct a DESeqDataSet; the function automatically computes and embeds an offset matrix from the length matrix to adjust for effective gene length variation across conditions. Validation: Confirm that the DESeqDataSet object contains a non-null, correctly dimensioned offset matrix (samples × genes) stored in the assays slot, and that matrix values reflect the log-normalized length ratios used to correct count-based abundance estimates. References: source article (DOI: 10.12688/f1000research.7563.1) Load transcript-level abundance and inferential replicates from salmon_gibbs files using tximport with txOut=TRUE. Convert tximport output to edgeR DGEList with library size normalization using DGEListFromTximport(divide=TRUE). Validate DGEList object structure, count matrix presence, and library size factors. Extract and verify presence of common and tagwise dispersion estimates for count overdispersion modeling. Validation: DGEList object contains non-empty count matrix, positive library size factors, and both common and tagwise dispersion estimates suitable for transcript-level differential expression analysis. References: source article (DOI: 10.12688/f1000research.7563.1) Load three oarfish quant.gz files from tximportData package. Call tximport() with type='oarfish' to parse quantification format and txOut=TRUE to preserve transcript-level output. Extract abundance, count, and length matrices from returned list object. Validation: verify that all three output matrices have dimensions of 3 samples (columns) × n_transcripts (rows) and contain numeric values ≥ 0 for counts and lengths, and ≥ 0 for abundance. References: source article (DOI: 10.12688/f1000research.7563.1)

**Domain:** transcriptomics

**Techniques:** normalization, statistical-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** tximport imports transcript-level abundance, estimated counts, and transcript lengths, and summarizes them into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, and limma-voom. _[grounded: sys_tximport]_
- **(finding)** The tximport approach corrects for potential changes in gene length across samples from differential isoform usage. _[grounded: sys_tximport]_
- **(finding)** Upstream quantification methods such as salmon, sailfish, and kallisto are substantially faster and require less memory and disk usage compared to alignment-based methods that require creation and storage of BAM files. _[grounded: tool_salmon]_
- **(finding)** It is possible to avoid discarding fragments that can align to multiple genes with homologous sequence, thus increasing sensitivity.
- **(finding)** tximeta extends tximport, offering the same functionality plus automatic addition of annotation metadata for commonly used transcriptomes (GENCODE, Ensembl, RefSeq for human and mouse). _[grounded: sys_tximport]_
- **(finding)** tximport outputs a simple list of matrices, while tximeta outputs a SummarizedExperiment object with appropriate GRanges added. _[grounded: sys_tximport]_
- **(finding)** tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish, or kallisto. _[grounded: sys_tximport]_
- **(finding)** The tximport package has a single function for importing transcript-level estimates. _[grounded: sys_tximport]_
- **(finding)** The tximport type argument is used to specify what software was used for transcript abundance estimation. _[grounded: sys_tximport]_
- **(finding)** tximport returns a simple list with matrices for abundance, counts, and length, where transcript level information is summarized to the gene-level. _[grounded: sys_tximport]_
- **(finding)** Abundance is typically provided by quantification tools as TPM (transcripts-per-million).
- **(finding)** The length matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices.
- **(finding)** tximport is significantly faster to read in files using the readr package. _[grounded: sys_tximport]_
- **(finding)** tximport detects if readr is installed and will use readr::read_tsv function by default. _[grounded: sys_tximport]_
- **(finding)** From version 1.2 to 1.4 of tximport, the reader is not specified by the user anymore but is chosen automatically based on the availability of the readr package. _[grounded: sys_tximport]_
- **(finding)** tximport users can customize the import of files using the importer argument. _[grounded: sys_tximport]_
- **(finding)** Counts can be generated from abundances using the countsFromAbundance argument, scaled to library size as scaledTPM. _[grounded: cond_scaled_tpm]_
- **(finding)** Counts can be additionally scaled using the average transcript length, averaged over samples and to library size, as lengthScaledTPM. _[grounded: cond_length_scaled_tpm]_
- **(finding)** When using scaledTPM or lengthScaledTPM approaches, the counts are not correlated with length, and the length matrix should not be provided as an offset. _[grounded: cond_length_scaled_tpm]_
- **(finding)** As of tximport version 1.10, a new countsFromAbundance option dtuScaledTPM has been added, designed for use with txOut=TRUE for differential transcript usage analyses. _[grounded: sys_tximport]_
- **(finding)** Gene-level summarization can be avoided by setting txOut=TRUE, which gives the original transcript level estimates as a list of matrices. _[grounded: cond_txout_true]_
- **(finding)** Transcript-level matrices can be summarized afterwards using the summarizeToGene function. _[grounded: comp_summarize_to_gene]_
- **(finding)** salmon or sailfish quant.sf files can be imported by setting type to salmon or sailfish. _[grounded: tool_salmon]_
- **(finding)** If inferential replicates are present in expected locations relative to the quant.sf file, tximport will import these as well. _[grounded: sys_tximport]_
- **(finding)** kallisto abundance.h5 files can be imported by setting type to kallisto. _[grounded: tool_kallisto]_
- **(finding)** Importing kallisto abundance.h5 files requires that the Bioconductor package rhdf5 is installed. _[grounded: tool_kallisto]_
- **(finding)** kallisto abundance.tsv files can be imported with tximport, but this is typically slower than using abundance.h5 files. _[grounded: sys_tximport]_
- **(finding)** The ignoreAfterBar=TRUE argument is used to split incoming quantification matrix rownames at the first bar and only use the part before the bar as an identifier. _[grounded: comp_tx2gene]_
- **(finding)** RSEM sample.genes.results files can be imported by setting type to rsem with txIn and txOut set to FALSE. _[grounded: tool_rsem]_
- **(finding)** RSEM sample.isoforms.results files can be imported by setting type to rsem with txIn and txOut set to TRUE. _[grounded: tool_rsem]_
- **(finding)** StringTie t_data.ctab files can be imported by setting type to stringtie. _[grounded: tool_stringtie]_
- **(finding)** tximport will compute counts from StringTie coverage information by reversing the formula that StringTie uses to calculate coverage. _[grounded: sys_tximport]_
- **(finding)** The read length is used in the formula that tximport uses to compute counts from StringTie coverage, and can be provided with the readLength argument. _[grounded: sys_tximport]_
- **(finding)** scRNA-seq data quantified with alevin can be imported using tximport. _[grounded: sys_tximport]_
- **(finding)** A single file should be specified for alevin import, which will import a gene-by-cell matrix of data. _[grounded: tool_alevin]_
- **(finding)** Long read data quantified with oarfish can be imported using tximport. _[grounded: sys_tximport]_
- **(finding)** One suggested way of importing estimates for use with differential gene expression methods is to use gene-level estimated counts from the quantification tools and additionally use the transcript-level abundance estimates to calculate a gene-level offset. _[grounded: tool_deseq2]_
- **(finding)** The gene-level offset corrects for changes to the average transcript length across samples.
- **(finding)** The functions edgeR::DGEListFromTximport and DESeq2::DESeqDataSetFromTximport take care of creation of the offset. _[grounded: tool_deseq2]_
- **(finding)** A second method for importing estimates for differential gene expression is to use tximport argument countsFromAbundance=lengthScaledTPM or scaledTPM and then use the gene-level count matrix directly. _[grounded: sys_tximport]_
- **(finding)** One should not manually pass the original gene-level counts to downstream methods without an offset.
- **(finding)** The only case where passing original gene-level counts without an offset would make sense is if there is no length bias to the counts, as may happen in 3 prime tagged RNA-seq data.
- **(finding)** The original gene-level counts are in txi$counts when tximport is run with countsFromAbundance=no. _[grounded: sys_tximport]_
- **(finding)** Using only txi$counts is simply passing the summed estimated transcript counts, and does not correct for potential differential isoform usage.
- **(finding)** Passing uncorrected gene-level counts without an offset is not recommended by the tximport package authors. _[grounded: sys_tximport]_
- **(finding)** For 3 prime tagged RNA-seq data, correcting the counts for gene length will induce a bias in the analysis because the counts do not have length bias.
- **(finding)** For 3 prime tagged RNA-seq, the original counts from txi$counts should be used as a counts matrix without calculating an offset and without using countsFromAbundance. _[grounded: tool_edger]_
- **(finding)** The DGEListFromTximport function is available in edgeR as of version 4.10.0 (Bioconductor release 3.23, Spring 2026). _[grounded: tool_edger]_
- **(finding)** If tximport output contains inferential replicates, DGEListFromTximport will also estimate the count overdispersion that arises from probabilistic read assignment to transcripts. _[grounded: sys_tximport]_
- **(finding)** The DGEListFromTximport function can compute divided counts suitable for differential expression analysis at the transcript level when the divide parameter is set to TRUE. _[grounded: comp_dgelistfromtximport]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Generate counts from abundances using countsFromAbundance argument with scaledTPM or lengthScaledTPM options as alternative to using counts with offset
- Use txOut=TRUE to generate transcript-level matrices instead of gene-level summarization
- Use summarizeToGene function after tximport with txOut=TRUE to summarize transcript-level estimates to gene-level

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Do not manually pass original gene-level counts to downstream methods without an offset, as this would not correct for potential differential isoform usage
- For 3' tagged RNA-seq data, do not correct counts for gene length as counts do not have length bias

## Steps

### Step `task_001`
- Title: Reproduce tx2gene table construction from Gencode v27 and tximport gene-level count matrix
- Task kind: `reproduction`
- Task: Import transcript-level abundance estimates from six salmon quant.sf.gz samples using tximport with the pre-built tx2gene.gencode.v27.csv mapping, and generate gene-level counts, abundance, and length matrices.
- Inputs:
  - Six salmon quant.sf.gz quantification files from tximportData package
  - tx2gene.gencode.v27.csv file mapping transcript IDs to gene IDs
- Expected outputs:
  - Gene-level counts matrix (rows: genes, columns: samples)
  - Gene-level abundance matrix in TPM (rows: genes, columns: samples)
  - Gene-level length matrix of effective transcript lengths (rows: genes, columns: samples)
- Tools: tximport, readr
- Landmark output files: tx2gene_loaded.csv, salmon_files_list.txt, tximport_output_list.rds, gene_counts.csv, gene_abundance.csv, gene_length.csv

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce equivalence of txOut=TRUE followed by summarizeToGene versus txOut=FALSE in tximport
- Task kind: `reproduction`
- Task: Run tximport on salmon transcript-abundance files with txOut=TRUE to obtain transcript-level counts, then apply summarizeToGene with a tx2gene mapping to collapse to gene level, and verify the resulting gene-level count matrix is identical to direct import with txOut=FALSE.
- Inputs:
  - Salmon quantification output files (quant.sf) from tximportData package
  - Transcript-to-gene mapping data.frame (tx2gene) with transcript IDs and corresponding gene IDs
- Expected outputs:
  - Gene-level count matrix from two-step workflow (transcript import + summarizeToGene)
  - Gene-level count matrix from direct single-step import (txOut=FALSE)
  - Boolean confirmation that both matrices are identical
- Tools: tximport, readr
- Landmark output files: transcript_level_counts_txout_true.csv, gene_level_counts_summarized.csv, gene_level_counts_direct.csv
- Primary expected artifact: `equivalence_report.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Reconstruct DESeqDataSetFromTximport offset creation for DESeq2 downstream analysis
- Task kind: `component_reconstruction`
- Task: Construct a DESeqDataSet from a tximport object using DESeq2::DESeqDataSetFromTximport with a two-condition sample table, and verify that the offset matrix derived from transcript length estimates is correctly embedded in the resulting object.
- Inputs:
  - tximport list object (txi) containing transcript-level abundance, estimated counts, and transcript length matrices from salmon quantification
  - Sample metadata table with two condition groups for DESeqDataSet construction
- Expected outputs:
  - DESeqDataSet object with embedded offset matrix derived from transcript length estimates
- Tools: tximport, DESeq2, salmon
- Landmark output files: txi_list_object.RData, colData_sample_table.csv, dds_object_with_offset.RData

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct DGEListFromTximport with divided counts for edgeR transcript-level DGE
- Task kind: `component_reconstruction`
- Task: Import transcript-level abundance data with inferential replicates from salmon_gibbs files using tximport with txOut=TRUE, then call edgeR::DGEListFromTximport with divide=TRUE to produce a DGEList object with divided counts suitable for transcript-level differential expression analysis. Verify DGEList structure and presence of count overdispersion estimates.
- Inputs:
  - tximportData salmon_gibbs files with Gibbs sample replicates and transcript-level abundance estimates
- Expected outputs:
  - DGEList object with divided transcript-level counts, library size normalization factors, and overdispersion estimates
  - Verification report confirming DGEList structure integrity and presence of count overdispersion estimates
- Tools: tximport, edgeR, salmon
- Landmark output files: tximport_output.rds, dgelist_object.rds, dgelis_structure_summary.txt

### Step `task_005`
- Depends on: `task_001`
- Title: Reproduce tximport import of oarfish long-read SG-Nex samples at transcript level
- Task kind: `reproduction`
- Task: Import transcript-level abundance, count, and length matrices from three SG-Nex oarfish replicates using tximport with type='oarfish' and txOut=TRUE, producing quantification matrices ready for downstream statistical analysis.
- Inputs:
  - Three SG-Nex oarfish quant.gz files from tximportData package
- Expected outputs:
  - Transcript-level abundance matrix (3 samples × transcripts)
  - Transcript-level count matrix (3 samples × transcripts)
  - Transcript-level length matrix (3 samples × transcripts)
- Tools: tximport
- Landmark output files: abundance_matrix.csv, count_matrix.csv, length_matrix.csv

## Final expected outputs

- `Gene-level count matrix from two-step workflow (transcript import + summarizeToGene)` (type: file, tolerance: hash)
- `Gene-level count matrix from direct single-step import (txOut=FALSE)` (type: file, tolerance: hash)
- `Boolean confirmation that both matrices are identical` (type: file, tolerance: hash)
- `DESeqDataSet object with embedded offset matrix derived from transcript length estimates` (type: file, tolerance: hash)
- `DGEList object with divided transcript-level counts, library size normalization factors, and overdispersion estimates` (type: file, tolerance: hash)
- `Verification report confirming DGEList structure integrity and presence of count overdispersion estimates` (type: file, tolerance: hash)
- `Transcript-level abundance matrix (3 samples × transcripts)` (type: file, tolerance: hash)
- `Transcript-level count matrix (3 samples × transcripts)` (type: file, tolerance: hash)
- `Transcript-level length matrix (3 samples × transcripts)` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

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
  "workflow_id": "coll_tximport_workflow",
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
    "Gene-level count matrix from two-step workflow (transcript import + summarizeToGene)": "<locator>",
    "Gene-level count matrix from direct single-step import (txOut=FALSE)": "<locator>",
    "Boolean confirmation that both matrices are identical": "<locator>",
    "DESeqDataSet object with embedded offset matrix derived from transcript length estimates": "<locator>",
    "DGEList object with divided transcript-level counts, library size normalization factors, and overdispersion estimates": "<locator>",
    "Verification report confirming DGEList structure integrity and presence of count overdispersion estimates": "<locator>",
    "Transcript-level abundance matrix (3 samples \u00d7 transcripts)": "<locator>",
    "Transcript-level count matrix (3 samples \u00d7 transcripts)": "<locator>",
    "Transcript-level length matrix (3 samples \u00d7 transcripts)": "<locator>"
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
