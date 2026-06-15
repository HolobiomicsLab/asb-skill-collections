---
name: quantification-output-parsing
description: Use when you have transcript-level quantification output files (e.g., quant.sf from salmon, abundance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  tools:
  - tximport
  - readr
  - tximeta
  - salmon
  - DESeq2
  - edgeR
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

# quantification-output-parsing

## Summary

Parse and import transcript-level abundance, count, and length estimates from RNA-seq quantification tools (salmon, sailfish, kallisto) into structured matrices suitable for downstream statistical analysis. This skill bridges pseudoalignment/quasi-mapping quantifiers and gene/transcript-level differential expression analysis.

## When to use

You have transcript-level quantification output files (e.g., quant.sf from salmon, abundance.tsv from kallisto) and need to convert them into abundance, count, and effective length matrices for gene-level or transcript-level differential expression analysis in R packages such as DESeq2, edgeR, or limma-voom.

## When NOT to use

- Input quantification files are from alignment-based methods (e.g., STAR, HISAT2, Bowtie2 BAM files); use a dedicated BAM-to-count tool instead.
- You already have pre-computed gene-level count matrices; tximport is unnecessary.
- Your downstream analysis requires exon-level or junction-level estimates; tximport aggregates to transcript or gene level only.

## Inputs

- quantification output files (quant.sf, abundance.tsv, or equivalent from salmon/sailfish/kallisto)
- tx2gene data.frame (transcript ID to gene ID mapping)
- sample metadata or file paths linking samples to quantification outputs

## Outputs

- abundance matrix (transcript or gene level, depending on txOut parameter)
- counts matrix (transcript or gene level)
- length matrix (average transcript length, weighted by sample-specific abundance)

## How to apply

Use tximport with the type argument set to the quantifier name (salmon, sailfish, or kallisto) and specify txOut parameter based on your analysis goal: set txOut=TRUE to retain transcript-level matrices, or txOut=FALSE for direct gene-level summarization. Provide a tx2gene data.frame mapping transcript IDs to gene IDs; tximport will then read all quantification files and return a list containing 'abundance', 'counts', and 'length' matrices. The length matrix represents average transcript length weighted by sample-specific transcript abundance estimates and should be used as an offset in downstream count-based analysis. For faster file reading, enable the readr package dependency. If performing transcript-level analysis, verify downstream tools can accept the txOut=TRUE output structure; if performing gene-level analysis, confirm that tx2gene mapping is complete and unambiguous.

## Related tools

- **tximport** (Core function to read quantification files, parse transcript-level estimates, and summarize to gene or transcript level) — https://github.com/thelovelab/tximport
- **readr** (Optional dependency to accelerate file reading in tximport)
- **tximeta** (Extended package wrapping tximport, adds automatic annotation metadata)
- **salmon** (Upstream quantifier producing transcript-level abundance and count estimates compatible with tximport)
- **DESeq2** (Downstream package for gene-level differential expression analysis using tximport count matrices and length offsets)
- **edgeR** (Downstream package for gene-level differential expression analysis using tximport count matrices)

## Examples

```
txi <- tximport(files=c('sample1/quant.sf', 'sample2/quant.sf'), type='salmon', tx2gene=tx2gene, txOut=FALSE)
```

## Evaluation signals

- Verify that the returned abundance, counts, and length matrices have dimensions (transcripts/genes) × (samples) with no missing values for expected features.
- Confirm gene-level matrices from txOut=TRUE followed by summarizeToGene are identical (via all.equal() in R) to those produced by txOut=FALSE on the same input files.
- Check that the length matrix is numeric, strictly positive, and reflects weighted average transcript lengths (should vary across samples if differential isoform usage is present).
- Validate that tx2gene mapping covers all transcripts in the quantification files and produces no unexpected many-to-many relationships.
- Ensure downstream offset calculation (e.g., log(length)) produces finite values and does not introduce systematic bias in downstream differential analysis.

## Limitations

- tximport requires a complete and accurate tx2gene mapping; incomplete or misaligned mappings will silently drop transcripts or produce incorrect gene-level summaries.
- The length matrix corrects for changes in gene length due to differential isoform usage, but does not account for other sources of length bias (e.g., gc content, sequence composition); users should consider additional offset matrices or methods for those confounders.
- Transcript-level analysis requires downstream tools that accept txOut=TRUE output structure (list of matrices); standard DESeq2 / edgeR workflows assume gene-level input and may require adaptation.
- tximport does not validate quantification file integrity or detect corrupted / incomplete quant.sf files; upstream quantifier errors will propagate into downstream analysis.

## Evidence

- [readme] Imports and core functionality: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [readme] Length matrix as offset: "Average transcript length, weighted by sample-specific transcript abundance estimates, is provided as a matrix which can be used as an offset for different expression of gene-level counts."
- [intro] Correction for differential isoform usage: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [readme] Supported quantifiers: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto."
- [intro] Gene-level summarization workflow: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [readme] Transcript-level output option: "The argument `txOut=TRUE` can be used to generate transcript-level matrices."
- [intro] readr performance benefit: "While tximport works without any dependencies, it is significantly faster to read in files using the readr package"
