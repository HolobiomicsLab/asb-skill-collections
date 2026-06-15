---
name: transcript-to-gene-aggregation
description: Use when when you have transcript-level quantification files (e.g., Salmon quant.sf.gz, kallisto abundance.h5, or RSEM .results) and need to construct a gene-level count matrix for DESeq2 differential expression testing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
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

# transcript-to-gene-aggregation

## Summary

Aggregate transcript-level quantification estimates from tools like Salmon, kallisto, or RSEM to gene-level counts using a transcript-to-gene mapping table. This step produces un-normalized gene-level count matrices suitable for downstream differential expression analysis with DESeq2.

## When to use

When you have transcript-level quantification files (e.g., Salmon quant.sf.gz, kallisto abundance.h5, or RSEM .results) and need to construct a gene-level count matrix for DESeq2 differential expression testing. Apply this skill before constructing a DESeqDataSet, especially when your research question targets gene-level rather than transcript-level effects.

## When NOT to use

- Input is already a gene-level count matrix from htseq-count, featureCounts, or a prior aggregation step.
- Your research question specifically targets isoform-level or transcript-level differential usage (use transcript-level quantification directly instead).
- Quantification was performed with a tool not supported by tximport (e.g., proprietary formats without documented import methods).

## Inputs

- transcript-level quantification files (Salmon quant.sf.gz, kallisto abundance.h5, RSEM .results, or equivalents)
- tx2gene mapping table (two-column data frame: transcript ID → gene ID)
- sample metadata table with condition/group assignments

## Outputs

- tximport list object (containing $abundance, $counts, $length, $countsFromAbundance)
- gene-level count matrix (integer estimated counts)
- DESeqDataSet object (after DESeqDataSetFromTximport)

## How to apply

Load transcript abundance quantifications using tximport() with the appropriate quantifier type (e.g., type='salmon') and supply a transcript-to-gene mapping table (tx2gene) that links each transcript ID to its parent gene ID. The tx2gene table is typically a two-column data frame with transcript identifiers in the first column and corresponding gene identifiers in the second. tximport() will aggregate transcript-level estimated counts to the gene level and return a list object containing gene-level counts, effective lengths, and offsets. These un-normalized estimated counts are then passed directly to DESeqDataSetFromTximport() along with sample metadata and a design formula to construct the DESeqDataSet for statistical testing. Verify that the resulting count matrix contains integer-like estimated counts without library-size scaling or normalization applied.

## Related tools

- **tximport** (Core tool: ingests transcript-level quantification files and aggregates counts to gene level using tx2gene mapping) — https://bioconductor.org/packages/tximport
- **DESeq2** (Downstream consumer: accepts tximport output via DESeqDataSetFromTximport() to construct DESeqDataSet for differential expression analysis) — https://github.com/thelovelab/DESeq2
- **Salmon** (Upstream quantifier: produces transcript-level abundance estimates (quant.sf.gz files) that serve as input to tximport)
- **kallisto** (Upstream quantifier: produces transcript-level abundance estimates (abundance.h5) that serve as input to tximport)
- **RSEM** (Upstream quantifier: produces transcript-level abundance estimates (.results files) that serve as input to tximport)
- **tximportData** (Reference data package: provides example Salmon quantification files, sample metadata, and tx2gene mapping tables for learning and testing) — https://bioconductor.org/packages/tximportData
- **tximeta** (Alternative: imports quantification data and automatically retrieves transcript-to-gene mappings and metadata from remote databases)

## Examples

```
txi <- tximport(files, type="salmon", tx2gene=tx2gene); ddsTxi <- DESeqDataSetFromTximport(txi, colData=samples, design=~condition)
```

## Evaluation signals

- The resulting tximport list object contains integer-like estimated gene counts in the $counts element, without library-size normalization or log transformation applied.
- Spot-check the tx2gene mapping: verify that all transcript IDs in the quantification files are present in the mapping table and that gene IDs are valid and non-duplicated within the mapping.
- Compare gene-level totals: sum of aggregated transcript counts for each gene should be approximately equal to the transcript-level estimates for that gene (within rounding and abundance-weighting tolerances).
- DESeqDataSet construction succeeds and the assay slot contains un-normalized integer counts; row counts should match the number of unique genes in the tx2gene mapping.
- Pre-filtering or independent filtering on the DESeqDataSet (e.g., genes with rowSums < threshold) works as expected, confirming that counts are properly structured as a numeric matrix.

## Limitations

- tximport requires an exact, curated tx2gene mapping; missing or misnamed transcript IDs will result in silent loss of quantification data for those transcripts.
- Quantification uncertainty (e.g., from multi-mapping reads in Salmon) is already embedded in the estimated counts; tximport does not increase or decrease that uncertainty.
- Gene-level aggregation is irreversible; transcript-level isoform quantification information is lost after aggregation, making post-hoc transcript-level inference impossible.
- The tx2gene mapping is typically species-, genome-build-, and transcriptome-version-specific; using an incorrect or mismatched mapping will yield meaningless results.

## Evidence

- [other] tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level: "tximport ingests transcript-level quantification files and produces a list object that contains un-normalized counts aggregated to the gene level, which serves as input to DESeqDataSetFromTximport"
- [other] tximport processes transcript-level quantification files using type parameter and tx2gene mapping: "Import transcript abundance quantifications using tximport() with type="salmon" and the tx2gene mapping to aggregate to gene level, producing a list object containing estimated gene counts, lengths,"
- [other] Supported quantification tools for tximport: "If you have performed transcript quantification (with *Salmon*, *kallisto*, *RSEM*, etc.) you could import the data with *tximport*, which produces a list, and then you can use"
- [other] DESeqDataSetFromTximport constructor accepts tximport output: "Construct a DESeqDataSet from the tximport output using DESeqDataSetFromTximport(), specifying the sample metadata and design formula (~condition)"
- [other] Verification of un-normalized count values: "Verify that the resulting count matrix contains un-normalized estimated counts by examining the assay data and confirming values are integer counts without library-size scaling or normalization"
