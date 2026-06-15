---
name: bioconductor-package-operation
description: Use when you have transcript-level quantification files (quant.gz, h5, or similar) from a known upstream quantifier (salmon, kallisto, sailfish, oarfish) and need to import them into R as matrices for differential expression analysis with edgeR, DESeq2, or limma-voom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3308
  tools:
  - tximport
  - salmon
  - kallisto
  - oarfish
  - DESeq2
  - edgeR
  - limma-voom
  - tximeta
  - readr
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
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

# bioconductor-package-operation

## Summary

Execute a Bioconductor R package function with specified parameters to transform RNA-seq quantification outputs into analysis-ready matrices. This skill applies a package's documented API to convert upstream quantifier results (salmon, kallisto, sailfish, oarfish) into transcript- or gene-level abundance, count, and length matrices suitable for downstream statistical testing.

## When to use

You have transcript-level quantification files (quant.gz, h5, or similar) from a known upstream quantifier (salmon, kallisto, sailfish, oarfish) and need to import them into R as matrices for differential expression analysis with edgeR, DESeq2, or limma-voom. The quantifier type and output format must be documented and supported by the Bioconductor package's `type` parameter.

## When NOT to use

- Input files are already in gene-level matrix format (e.g., from a prior tximport run or a count matrix from alignment-based methods).
- Upstream quantifier type is unknown or not supported by the package's `type` parameter.
- Input files are corrupt, incomplete, or do not match the expected schema for the declared quantifier type.

## Inputs

- quantification files (quant.gz, h5, or equivalent) from upstream quantifier (salmon, kallisto, sailfish, oarfish)
- named vector of file paths
- tx2gene data.frame (transcript ID to gene ID mapping) for gene-level summarization

## Outputs

- abundance matrix (transcript or gene level)
- counts matrix (estimated or observed counts, transcript or gene level)
- length matrix (transcript or gene level, average length weighted by sample-specific abundance)
- list object containing all three matrices

## How to apply

Load the Bioconductor package and prepare a named vector of file paths pointing to the quantification outputs. If performing gene-level analysis, construct a tx2gene data.frame mapping transcript IDs to gene IDs. Call the package's main import function (e.g., tximport) with the `type` argument set to match the upstream quantifier, `files` argument pointing to the quantification files, and optional parameters like `txOut=TRUE` to retain transcript-level output or `txOut=FALSE` (default) to summarize to gene level. Extract the returned list containing 'abundance', 'counts', and 'length' matrices. Verify matrix dimensions match the number of samples and features, and spot-check row and column names for consistency with the input files.

## Related tools

- **tximport** (Main import function that reads transcript-level quantification files and produces matrices for gene-level or transcript-level analysis) — https://github.com/thelovelab/tximport
- **salmon** (Upstream quantifier whose output (quant.sf files) is consumed by tximport with type='salmon')
- **kallisto** (Upstream quantifier whose output is consumed by tximport with type='kallisto')
- **oarfish** (Upstream quantifier for long-read RNA-seq whose output (quant.gz files) is consumed by tximport with type='oarfish')
- **DESeq2** (Downstream statistical analysis package that accepts tximport-derived count matrices and length offsets for gene-level differential expression)
- **edgeR** (Downstream statistical analysis package that accepts tximport-derived count matrices for gene-level differential expression)
- **limma-voom** (Downstream statistical analysis package that accepts tximport-derived count matrices for gene-level differential expression)
- **tximeta** (Extended Bioconductor package that wraps tximport and automatically adds annotation metadata)
- **readr** (Optional dependency that significantly improves file-reading speed in tximport)

## Examples

```
txi <- tximport(files = c('sample1_quant.sf', 'sample2_quant.sf', 'sample3_quant.sf'), type = 'salmon', tx2gene = tx2gene, txOut = FALSE)
```

## Evaluation signals

- Returned list contains exactly three named elements: 'abundance', 'counts', and 'length'.
- All three matrices have matching dimensions: rows equal the number of features (transcripts or genes), columns equal the number of samples.
- Row names match expected transcript or gene IDs from the input quantification files; column names match sample identifiers.
- Abundance and count values are numeric, non-negative, and within expected ranges (no NaN, Inf, or negative values).
- Length matrix values are positive and represent weighted average transcript lengths; gene-level lengths should reflect isoform composition in each sample.

## Limitations

- tximport requires prior knowledge of the upstream quantifier type; misspecifying `type` will cause incorrect parsing or parsing failure.
- The tx2gene mapping must be accurate and complete; missing or mismatched transcript IDs will result in failed summarization to gene level.
- Gene-level summarization may mask important transcript-level effects (differential isoform usage); use `txOut=TRUE` to retain transcript-level resolution when isoform-level questions are present.
- The length matrix represents average length weighted by sample-specific abundance; it does not capture actual, single-molecule transcript lengths from long-read data.
- tximport does not validate that input files belong to the same annotation version or reference genome; the user is responsible for consistency.

## Evidence

- [readme] Core functionality of tximport for importing and matrix generation: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [other] Type parameter and type='oarfish' support for long-read quantification: "The type argument is used to specify what software was used for estimation"
- [readme] Transcript-level output control via txOut parameter: "The argument `txOut=TRUE` can be used to generate transcript-level matrices."
- [intro] Gene-level summarization workflow using tx2gene: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [intro] Length matrix offset for downstream analysis: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] Correction for differential isoform usage effects: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [readme] Support for inferential replicates from multiple quantifiers: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto."
- [other] Transcript-level import demonstration with oarfish and SG-Nex samples: "tximport with type='oarfish' and txOut=TRUE successfully imports transcript-level abundance, count, and length matrices from oarfish quant.gz files for SG-Nex replicates"
