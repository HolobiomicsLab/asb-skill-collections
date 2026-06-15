---
name: rna-seq-abundance-matrix-handling
description: Use when you have transcript-level quantification output files (quant.sf, quant.gz) from salmon, kallisto, sailfish, or oarfish and need to produce gene-level count matrices, abundance matrices, and length-based offsets for differential expression analysis in DESeq2, edgeR, or limma-voom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0199
  tools:
  - tximport
  - readr
  - salmon
  - kallisto
  - sailfish
  - oarfish
  - DESeq2
  - edgeR
  - limma-voom
  - tximeta
  - summarizeToGene
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

# rna-seq-abundance-matrix-handling

## Summary

Import transcript-level quantification estimates from RNA-seq quantifiers (salmon, kallisto, sailfish, oarfish) and summarize them into gene-level or transcript-level abundance, count, and length matrices for use in downstream statistical analysis. This skill corrects for differential isoform usage by embedding transcript-length-derived offsets that adjust for changes in effective gene length across samples.

## When to use

You have transcript-level quantification output files (quant.sf, quant.gz) from salmon, kallisto, sailfish, or oarfish and need to produce gene-level count matrices, abundance matrices, and length-based offsets for differential expression analysis in DESeq2, edgeR, or limma-voom. Use this when you want to retain the benefits of alignment-free quantification while accounting for isoform-level variation that affects gene-level inference.

## When NOT to use

- Input is already aligned BAM files or bed-format feature counts; use alignment-based counting instead.
- You require exon-level or small exonic region-level analysis; tximport summarizes to transcript or gene level only.
- Your quantifier is not one of: salmon, kallisto, sailfish, or oarfish; tximport does not support other quantification methods.

## Inputs

- Quantification output files (quant.sf for salmon/sailfish, quant.sf for kallisto, quant.gz for oarfish)
- tx2gene data.frame mapping transcript IDs to gene IDs
- Sample metadata table (optional, for downstream DESeqDataSetFromTximport)

## Outputs

- tximport list object containing 'abundance' matrix (TPM or other normalized estimates)
- tximport list object containing 'counts' matrix (estimated read counts at gene or transcript level)
- tximport list object containing 'length' matrix (average transcript length, weighted by sample-specific abundance)
- DESeqDataSet (if using DESeq2::DESeqDataSetFromTximport) with embedded offset matrix

## How to apply

Load quantification files using tximport, specifying the appropriate quantifier type (salmon, kallisto, sailfish, or oarfish). Provide a tx2gene mapping data.frame (transcript-to-gene associations) to enable gene-level summarization. Set txOut=FALSE for direct gene-level matrices or txOut=TRUE to retain transcript-level output and apply summarizeToGene afterward—both approaches produce identical results. The tximport function returns a list containing 'abundance', 'counts', and 'length' matrices; the 'length' matrix (average transcript length weighted by sample-specific abundance) serves as the offset matrix to correct for differential isoform usage in downstream count-based analysis. Use the readr package for faster file reading if available.

## Related tools

- **tximport** (Core function that imports transcript-level abundance, estimated counts, and transcript lengths from quantification files and summarizes into matrices) — https://github.com/thelovelab/tximport
- **salmon** (Upstream quantifier whose output (quant.sf files) is imported by tximport)
- **kallisto** (Upstream quantifier whose output (quant.sf files) is imported by tximport)
- **sailfish** (Upstream quantifier whose output (quant.sf files) is imported by tximport)
- **oarfish** (Upstream long-read quantifier whose output (quant.gz files) is imported by tximport with type='oarfish')
- **readr** (Optional package that accelerates file reading in tximport)
- **DESeq2** (Downstream statistical analysis package; DESeqDataSetFromTximport constructs a DESeqDataSet with offset matrix from tximport output)
- **edgeR** (Alternative downstream statistical analysis package for differential expression using tximport matrices)
- **limma-voom** (Alternative downstream statistical analysis package for differential expression using tximport matrices)
- **tximeta** (Extended package that wraps tximport functionality and automatically adds annotation metadata)
- **summarizeToGene** (Function that collapses transcript-level tximport output (txOut=TRUE) to gene level using tx2gene mapping)

## Examples

```
txi <- tximport(files = c('sample1.quant.sf', 'sample2.quant.sf'), type = 'salmon', tx2gene = tx2gene); dds <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
```

## Evaluation signals

- Verify that the returned tximport list contains 'abundance', 'counts', and 'length' matrices with consistent row (gene/transcript) and column (sample) dimensions.
- Check that gene-level count matrices produced via txOut=TRUE followed by summarizeToGene are identical (confirmed by all.equal()) to those from txOut=FALSE direct import.
- Confirm that the 'length' matrix values are positive, finite, and vary across samples (indicating sample-specific transcript length weighting).
- Validate that offset matrix embedded in DESeqDataSet (via DESeqDataSetFromTximport) is non-zero and derived from the length matrix.
- Ensure that matrix dimensions match the number of genes/transcripts and number of samples; missing or malformed files should raise an error rather than producing incomplete matrices.

## Limitations

- tximport does not support quantifiers other than salmon, sailfish, kallisto, and oarfish; users must identify or convert output to a supported format.
- Gene-level summarization requires an accurate and comprehensive tx2gene mapping; missing or incorrect transcript-to-gene associations will produce incomplete or misaligned gene-level matrices.
- The length matrix assumes that differential isoform usage is the primary source of gene-length variation; other sources (e.g., differential exon inclusion not tied to isoform switching) may not be fully corrected.
- tximport is designed for gene- and transcript-level analysis; it does not produce exon- or small-region-level quantification.
- Inferential replicates (Gibbs or bootstrap samples) from salmon, sailfish, and kallisto require tximport version ≥ 1.3.9 and may increase memory and disk usage.

## Evidence

- [readme] Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom.: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [intro] this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto.: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto."
- [intro] A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] While tximport works without any dependencies, it is significantly faster to read in files using the readr package: "While tximport works without any dependencies, it is significantly faster to read in files using the readr package"
