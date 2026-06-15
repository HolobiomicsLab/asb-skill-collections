---
name: transcript-to-gene-mapping
description: Use when you have transcript-level quantification files (salmon quant.sf.gz, kallisto, or Sailfish output) and need to perform gene-level differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - salmon
  - kallisto
  - Sailfish
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

# transcript-to-gene-mapping

## Summary

Construction and application of a transcript-to-gene mapping table (tx2gene) to aggregate transcript-level quantification estimates into gene-level matrices for downstream differential expression analysis. This skill enables correction for gene-length variation across samples caused by differential isoform usage.

## When to use

You have transcript-level quantification files (salmon quant.sf.gz, kallisto, or Sailfish output) and need to perform gene-level differential expression analysis. A tx2gene mapping is required when your quantification tool reports transcript-level abundances, counts, and lengths, but your experimental design and statistical framework call for gene-level summaries.

## When NOT to use

- Input quantification is already at gene level (e.g., featureCounts output): tx2gene mapping is unnecessary and tximport summarization will be redundant.
- Analysis objective is transcript-level differential expression: use txOut=TRUE or skip aggregation to preserve isoform-level signal.
- Your reference annotation and transcript IDs in quantification files do not match (e.g., different Gencode versions or mismatched biotype filtering): mapping will fail silently or produce incomplete aggregation.

## Inputs

- transcript-to-gene mapping file (tx2gene data.frame with transcript IDs and gene IDs)
- transcript-level quantification files (quant.sf.gz from salmon, or equivalent from kallisto/Sailfish)
- reference annotation (e.g., Gencode GTF or GFF) to construct tx2gene if not pre-built

## Outputs

- gene-level abundance matrix (TPM)
- gene-level estimated counts matrix
- gene-level effective transcript length matrix
- offset matrix for use in downstream statistical models

## How to apply

First, construct a two-column data frame associating each transcript ID with its parent gene ID, typically extracted from a reference annotation (e.g., Gencode v27). Load this tx2gene table and the set of transcript-level quantification files into tximport, specifying the appropriate type argument (e.g., type='salmon'). tximport will aggregate transcript-level abundance, counts, and effective transcript lengths to the gene level by summing counts and computing length-weighted averages. The returned list contains three matrices (abundance in TPM, estimated counts, and effective length) ready for use in statistical packages such as DESeq2, edgeR, or limma-voom. The length matrix can be converted to an offset to account for sample-specific transcript composition differences in downstream models.

## Related tools

- **tximport** (Reads transcript-level quantification files and summarizes them to gene-level matrices using the tx2gene mapping) — https://github.com/thelovelab/tximport
- **readr** (Accelerates file I/O for reading large quantification and tx2gene files into R)
- **salmon** (Upstream quantification tool that produces transcript-level estimates (quant.sf.gz) to be summarized with tx2gene)
- **kallisto** (Alternative upstream quantification tool producing transcript-level estimates compatible with tx2gene mapping)
- **Sailfish** (Alternative upstream quantification tool producing transcript-level estimates compatible with tx2gene mapping)
- **DESeq2** (Downstream statistical package that accepts tximport gene-level count matrices and length offsets for differential expression)
- **edgeR** (Downstream statistical package that accepts tximport gene-level count matrices and length offsets for differential expression)
- **limma-voom** (Downstream statistical package that accepts tximport gene-level count matrices and length offsets for differential expression)

## Examples

```
tx2gene <- read.csv('tx2gene.gencode.v27.csv'); txi <- tximport(files=salmon_files, type='salmon', tx2gene=tx2gene); counts <- txi$counts; length_offset <- txi$length
```

## Evaluation signals

- The returned list contains exactly three matrices: 'abundance' (TPM), 'counts' (estimated counts), and 'length' (effective transcript length), each with gene IDs as row names and sample IDs as column names.
- All transcript IDs in the quantification files are successfully mapped to gene IDs; no transcript-level rows remain in the output, confirming complete aggregation.
- Gene-level counts are consistent with the sum of all transcripts assigned to each gene; spot-check a few genes by manual summation of their constituent transcript counts.
- The length matrix contains sample-specific weighted averages that reflect transcript composition within genes; samples with different isoform usage patterns will show different length values for the same gene.
- Downstream statistical models (DESeq2/edgeR) accept the count and length matrices without error, and the offset derived from length corrects gene-level bias caused by differential isoform usage.

## Limitations

- tx2gene mapping quality depends entirely on the accuracy and completeness of the reference annotation; mismatched Gencode versions or transcript ID formats will cause silent loss of mappings.
- The mapping approach discards transcript-level variance; if differential isoform usage or transcript-level effects are central to the biological question, gene-level summarization will obscure them.
- Quantification files must use the same transcript nomenclature as the tx2gene table; aliases or alternative transcript ID formats (e.g., ENST vs. NM identifiers) will fail to map.
- The effective length offset assumes that transcript-level abundance estimates are unbiased; biases in upstream quantification (salmon, kallisto) will propagate to the gene-level offset.

## Evidence

- [intro] Create a tx2gene mapping from reference annotation: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [intro] tximport performs the summarization with specified quantification type: "The tximport package has a single function for importing transcript-level estimates. The type argument is used to specify what software was used for estimation"
- [intro] Output is a list of three gene-level matrices: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] Length matrix is used to generate offset for differential analysis: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] tximport corrects for gene-length changes due to isoform usage: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [readme] tximport accepts multiple upstream quantification formats: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
