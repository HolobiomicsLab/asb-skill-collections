---
name: transcript-abundance-quantification-import
description: Use when you have transcript abundance files (e.g., Salmon quant.sf.gz, kallisto abundance.h5, RSEM .isoforms.results) from a quantification tool and need to construct a gene-level count matrix for DESeq2 analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0080
  tools:
  - tximport
  - DESeq2
  - Salmon
  - tximportData
  - readr
  - kallisto
  - RSEM
  - tximeta
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

# transcript-abundance-quantification-import

## Summary

Import transcript-level abundance quantifications from tools like Salmon, kallisto, or RSEM and aggregate them to gene-level counts using tximport, producing a list object suitable for downstream differential expression analysis with DESeq2.

## When to use

You have transcript abundance files (e.g., Salmon quant.sf.gz, kallisto abundance.h5, RSEM .isoforms.results) from a quantification tool and need to construct a gene-level count matrix for DESeq2 analysis. Use this skill when you want to leverage transcript-to-gene mapping to aggregate transcript-level estimates rather than re-aligning to gene annotations.

## When NOT to use

- Your quantification files are already aggregated to gene level (e.g., HTSeq-count output) — use DESeqDataSetFromHTSeq() or DESeqDataSetFromMatrix() instead.
- You have already imported quantifications via tximeta and obtained a SummarizedExperiment with automatic metadata — construct DESeqDataSet directly from the SummarizedExperiment rather than calling tximport again.
- Your input is a raw count matrix in tabular format — use DESeqDataSetFromMatrix() directly.

## Inputs

- transcript quantification files (Salmon quant.sf.gz, kallisto abundance.h5, RSEM .isoforms.results, or equivalent)
- sample metadata table (data frame with condition, batch, or other covariates; row names as run IDs)
- tx2gene mapping table (two-column data frame: transcript ID → gene ID)

## Outputs

- tximport list object (containing $abundance, $counts, $length, $countsFromAbundance)
- DESeqDataSet object (SummarizedExperiment subclass with un-normalized count assay)

## How to apply

First, assemble sample metadata (condition labels, run IDs) and construct file paths to transcript quantification outputs. Load the tx2gene mapping table (a two-column data frame linking transcript IDs to gene IDs), which defines the aggregation target. Call tximport() with the quantification file paths, type parameter matching your quantification tool (e.g., type='salmon'), and the tx2gene mapping to produce a list object containing un-normalized estimated gene counts, transcript lengths, and offsets. Pass this list directly to DESeqDataSetFromTximport() along with sample metadata (colData) and a design formula to construct a DESeqDataSet. The resulting counts remain un-normalized (not scaled by library size), allowing DESeq2 to apply its own normalization internally.

## Related tools

- **tximport** (Primary function to import transcript-level quantifications and aggregate to gene level using tx2gene mapping) — http://bioconductor.org/packages/tximport
- **DESeq2** (Accepts tximport output via DESeqDataSetFromTximport() to construct DESeqDataSet for differential expression analysis) — https://github.com/thelovelab/DESeq2
- **Salmon** (Quantification tool producing quant.sf.gz files imported with type='salmon' in tximport)
- **kallisto** (Quantification tool producing abundance.h5 files imported with type='kallisto' in tximport)
- **RSEM** (Quantification tool producing .isoforms.results files imported with type='rsem' in tximport)
- **tximportData** (R package providing example transcript quantification files and tx2gene mapping for testing and vignettes) — http://bioconductor.org/packages/tximportData
- **tximeta** (Alternative import function that produces SummarizedExperiment with automatic metadata, bypassing need for manual tx2gene specification in some cases)

## Examples

```
txi <- tximport(files, type="salmon", tx2gene=tx2gene); ddsTxi <- DESeqDataSetFromTximport(txi, colData=samples, design=~condition)
```

## Evaluation signals

- The tximport list object contains keys $abundance, $counts, and $length with numeric values; $counts contains integer-like estimated counts (not scaled by library size).
- The DESeqDataSet assay(dds) contains un-normalized count values consistent with the tximport $counts matrix, verifiable by comparing ranges and sums across samples.
- Gene counts in the DESeqDataSet match the union of genes represented in the tx2gene mapping; no transcript-level IDs remain in row names.
- DESeq() can be executed on the resulting DESeqDataSet without errors regarding missing or malformed count data; the design formula matches the sample metadata structure.
- Independent filtering and variance stabilization downstream proceed normally, indicating the count matrix is properly formatted and free of structural defects.

## Limitations

- tximport depends on a correctly formatted tx2gene mapping table; misaligned or incomplete mappings will result in missing or incorrect gene aggregations.
- The method requires that transcript IDs in the quantification files exactly match those in the tx2gene table; ID format mismatches (e.g., ENST vs transcript_id) will cause silent loss of data.
- tximport produces un-normalized counts; further preprocessing (filtering, normalization) is the responsibility of downstream methods like DESeq2 and should not be assumed automatic.
- For organisms or transcriptomes without pre-built tx2gene resources, manual construction is error-prone; tximeta with automatic metadata retrieval (when available) can mitigate this risk.
- Aggregation from transcript to gene level loses fine-grained transcript-level analysis potential; if differential transcript usage or isoform switching is the research goal, preserve transcript-level counts separately.

## Evidence

- [other] tximport produces transcript-to-gene aggregation: "you could import the data with *tximport*, which produces a list, and then you can use `DESeqDataSetFromTximport()`"
- [other] tximport ingests quantification files and aggregates by tx2gene: "txi <- tximport(files, type="salmon", tx2gene=tx2gene)"
- [other] tximport output contains un-normalized gene-level counts: "tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level"
- [other] DESeqDataSet construction from tximport: "ddsTxi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)"
- [other] Supported quantification tools: "If you have performed transcript quantification (with *Salmon*, *kallisto*, *RSEM*, etc.) you could import the data with *tximport*"
