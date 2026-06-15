---
name: count-matrix-format-validation
description: Use when after constructing a count matrix from transcript quantification files (via tximport, HTSeq, featureCounts, or direct alignment) and before running DESeq() differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0092
  tools:
  - tximport
  - DESeq2
  - Salmon
  - tximportData
  - readr
  - tximeta
  - HTSeq
  - featureCounts
derived_from:
- doi: 10.1186/s13059-014-0550-8
  title: deseq2
evidence_spans:
- txi <- tximport(files, type="salmon", tx2gene=tx2gene)
- The package DESeq2 provides methods to test for differential expression by use of negative binomial generalized linear models
- library("DESeq2") ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
- files <- file.path(dir,"salmon", samples$run, "quant.sf.gz")
- library("tximportData") dir <- system.file("extdata", package="tximportData")
- library("readr") tx2gene <- read_csv(file.path(dir, "tx2gene.gencode.v27.csv"))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deseq2
    doi: 10.1186/s13059-014-0550-8
    title: deseq2
  dedup_kept_from: coll_deseq2
schema_version: 0.2.0
---

# count-matrix-format-validation

## Summary

Verify that a count matrix destined for DESeq2 differential expression analysis contains un-normalized integer counts aggregated to the gene level, with proper sample metadata and design specification. This ensures compatibility with DESeq2's negative binomial model and prevents silent failures downstream.

## When to use

After constructing a count matrix from transcript quantification files (via tximport, HTSeq, featureCounts, or direct alignment) and before running DESeq() differential expression analysis. Validation is critical when ingesting data from tximport(), DESeqDataSetFromHTSeq(), or DESeqDataSetFromMatrix() to confirm the count matrix has not been pre-normalized (e.g., by library-size scaling or log transformation) and that gene-level aggregation is complete.

## When NOT to use

- Input is already a normalized expression matrix (e.g., TPM, RPKM, log2-transformed, or library-size scaled) — validation will fail or give misleading results
- Data has been pre-filtered to remove low-count genes prior to DESeq2 construction — validation timing is incorrect; filtering should occur post-construction via independent filtering in results()
- Count matrix is at transcript level rather than gene level — tximport aggregation or manual gene-level aggregation must be performed first

## Inputs

- DESeqDataSet object (post-construction from tximport, HTSeq, featureCounts, or count matrix)
- sample metadata table (colData) with design variables
- tximport list object (if applicable) containing estimated counts, lengths, and offsets

## Outputs

- Validation report confirming integer counts, gene-level aggregation, proper metadata alignment, and absence of normalization
- Flagged issues (if any) indicating pre-normalization, transcript-level data, or metadata inconsistencies

## How to apply

Examine the assay data of the constructed DESeqDataSet using counts() to confirm: (1) values are integer counts without decimal places or scaling factors; (2) values are un-normalized (not divided by library size or scaled by other global factors); (3) row names correspond to genes (not transcripts); (4) column names correspond to sample identifiers in the colData metadata table; (5) colData includes all design variables (e.g., 'condition') with correct factor levels set. If constructed from tximport, verify that the list object returned by tximport() with type='salmon' and a tx2gene mapping was passed directly to DESeqDataSetFromTximport() without manual modification. Check that estimated gene counts in the tximport list are present and structured correctly for aggregation.

## Related tools

- **DESeq2** (Constructs DESeqDataSet and defines the differential expression framework requiring validated count matrices as input) — https://github.com/thelovelab/DESeq2
- **tximport** (Produces the list object containing un-normalized gene-level estimated counts from transcript quantification files; output must be validated before DESeqDataSetFromTximport() is called)
- **tximeta** (Alternative to tximport that produces a SummarizedExperiment with automatic metadata; count matrix from this object should also be validated for normalization status before DESeq2 use)
- **Salmon** (Upstream quantification tool that produces transcript-level abundance files (quant.sf.gz) ingested by tximport; validation occurs on aggregated output, not raw Salmon files)
- **HTSeq** (Alternative count matrix source; raw output used with DESeqDataSetFromHTSeq() must be validated to confirm integer counts)
- **featureCounts** (Alternative rapid count matrix generation from alignments; output must be validated for integer un-normalized counts before DESeq2 analysis)

## Examples

```
# Validate count matrix post-construction from tximport
all(counts(ddsTxi) == as.integer(counts(ddsTxi))); all(colnames(ddsTxi) %in% rownames(colData(ddsTxi)))
```

## Evaluation signals

- counts(dds) returns a numeric matrix with all integer values (no decimal places), confirming un-normalized input
- Row sums of the count matrix vary across genes (not constant), indicating biological signal and proper gene-level aggregation
- All design variables in dds$condition (or other design columns) are present in colData and match sample order in the count matrix
- assay(dds) structure matches the design formula specified during DESeqDataSet construction (e.g., ~condition captures all intended comparisons)
- No genes have all-zero counts across samples (if observed, pre-filtering has occurred incorrectly pre-construction)

## Limitations

- Validation cannot detect upstream errors in the tx2gene mapping table passed to tximport — validation assumes the mapping is biologically correct
- This skill does not validate the quality or accuracy of the quantification source (e.g., Salmon alignment quality); it only checks DESeq2 input format compatibility
- Pre-filtering of low-count genes should occur after DESeqDataSet construction via independent filtering in results(), not before; validation cannot distinguish intended upstream filtering from erroneous pre-normalization
- If sample metadata (colData) contains NA or mismatched factor levels, validation may not catch subtle design specification errors that only manifest during hypothesis testing

## Evidence

- [other] tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level: "tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level, which serves as input to DESeqDataSetFromTximport"
- [other] Integer counts without library-size scaling should be in the assay: "Verify that the resulting count matrix contains un-normalized estimated counts by examining the assay data and confirming values are integer counts without library-size scaling or normalization"
- [other] DESeqDataSetFromTximport requires tximport output as input: "ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
- [other] Design formula and metadata alignment are essential: "dds <- DESeqDataSetFromMatrix(countData = cts, colData = coldata, design= ~ batch + condition)"
- [other] Pre-filtering occurs post-construction: "by removing rows in which there are very few reads, we reduce the memory size of the `dds` data object, and we increase the speed"
