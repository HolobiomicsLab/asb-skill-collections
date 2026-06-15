---
name: rna-seq-count-matrix-generation
description: Use when you have transcript-level abundance estimates from salmon, sailfish, or kallisto quantification and need gene-level count matrices for differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - tximeta
  - salmon
  - DESeq2
  - edgeR
  - limma-voom
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
- While tximport works without any dependencies, it is significantly faster to read in files using the readr package
- significantly faster to read in files using the readr package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tximport
    doi: 10.12688/f1000research.7563.1
    title: tximport
  dedup_kept_from: coll_tximport
schema_version: 0.2.0
---

# rna-seq-count-matrix-generation

## Summary

Generate gene-level count, abundance (TPM), and length matrices from transcript-level quantification files (salmon, sailfish, or kallisto) using transcript-to-gene mapping. This approach corrects for differential isoform usage effects on gene length and enables downstream statistical analysis with edgeR, DESeq2, or limma-voom.

## When to use

You have transcript-level abundance estimates from salmon, sailfish, or kallisto quantification and need gene-level count matrices for differential expression analysis. Apply this skill when you require summarization of transcript estimates to genes, correction for differential isoform usage across samples, and generation of length offsets for statistical modeling.

## When NOT to use

- Input quantification files are already aligned BAM files rather than transcript-level estimates; use alignment-based counting (e.g., featureCounts, htseq-count) instead.
- Transcript-level differential analysis is the primary goal; use txOut=TRUE parameter or retain transcript-level matrices instead of aggregating to genes.
- Gene length is already normalized or accounted for in your downstream analysis; the length matrix offset may be redundant.

## Inputs

- transcript-to-gene mapping file (tx2gene.csv or data.frame with transcript_id and gene_id columns)
- salmon/sailfish/kallisto quantification files (quant.sf.gz format, one per sample)
- annotation reference (e.g., Gencode GTF or equivalent)

## Outputs

- gene-level abundance matrix (TPM, rows=genes, columns=samples)
- gene-level count matrix (estimated counts, rows=genes, columns=samples)
- gene-level length matrix (average transcript length, rows=genes, columns=samples)

## How to apply

First, construct or load a tx2gene mapping file (data.frame) associating transcript IDs with gene IDs from your annotation source (e.g., Gencode v27). Use the tximport function with type argument matching your quantifier (type='salmon', type='sailfish', or type='kallisto') to import transcript-level quantification files (quant.sf.gz format). tximport will automatically summarize transcript-level abundance, counts, and effective transcript lengths to the gene level by aggregating across transcripts mapped to each gene. The returned list contains three matrices: 'abundance' (TPM-normalized), 'counts' (estimated counts), and 'length' (average transcript length weighted by sample-specific abundance). Use the length matrix as an offset matrix in downstream count-based differential analysis to account for gene length variation induced by isoform switching.

## Related tools

- **tximport** (primary tool for importing transcript-level quantification and summarizing to gene-level matrices; handles salmon, sailfish, and kallisto formats) — https://github.com/thelovelab/tximport
- **readr** (faster file I/O for reading tx2gene mapping and quantification files; optional but recommended for performance)
- **tximeta** (extends tximport with automatic annotation metadata addition; alternative to manual tx2gene construction)
- **salmon** (upstream quantification tool producing transcript-level estimates compatible with tximport input)
- **DESeq2** (downstream statistical analysis tool for differential expression using gene-level count matrices and length offsets)
- **edgeR** (downstream statistical analysis tool for differential expression using gene-level count matrices and length offsets)
- **limma-voom** (downstream statistical analysis tool for differential expression using gene-level count matrices and length offsets)

## Examples

```
txi <- tximport(files = c('sample1.quant.sf.gz', 'sample2.quant.sf.gz', 'sample3.quant.sf.gz'), type = 'salmon', tx2gene = tx2gene)
```

## Evaluation signals

- Returned list contains exactly three matrices: 'abundance', 'counts', and 'length', each with dimensions (n_genes × n_samples).
- Gene IDs in output matrices match the gene_id column of the input tx2gene mapping; transcript IDs are no longer present.
- Count and abundance values are non-negative; length values reflect average transcript length weighted by sample-specific isoform abundance.
- All input samples are represented as columns in output matrices; no samples are dropped or reordered unexpectedly.
- Length matrix shows variation across genes and (typically) across samples due to differential isoform usage; constant lengths per gene suggest possible tx2gene mapping errors.

## Limitations

- Requires a complete and accurate tx2gene mapping file; missing or incorrect gene annotations will produce incorrect or missing gene-level summaries.
- Cannot distinguish between genes with overlapping or ambiguous transcript boundaries; fragments mapping to multiple genes may be discarded depending on upstream quantifier settings.
- Length correction assumes that differential isoform usage is the primary driver of gene length variation; other sources of length bias are not accounted for.
- tximport does not validate biological consistency of aggregated estimates; downstream quality control (e.g., PCA, library size checks) is essential.

## Evidence

- [readme] Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom.: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom"
- [intro] The type argument is used to specify what software was used for estimation: "The type argument is used to specify what software was used for estimation"
- [intro] this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two: "Transcripts need to be associated with gene IDs for gene-level summarization"
- [readme] tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto: "tximport as of version 1.3.9 will import inferential replicates from Salmon, Sailfish or kallisto"
