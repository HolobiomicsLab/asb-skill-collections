---
name: transcript-level-abundance-import
description: Use when you have transcript-level quantification files (quant.sf.gz or quant.gz) from salmon, sailfish, kallisto, or oarfish and need to aggregate them into gene-level or transcript-level count, abundance, and length matrices for input to DESeq2, edgeR, or limma-voom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0197
  tools:
  - tximport
  - readr
  - salmon
  - sailfish
  - kallisto
  - oarfish
  - tximeta
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

# transcript-level-abundance-import

## Summary

Import transcript-level quantification estimates (abundance, counts, and effective lengths) from RNA-seq quantification tools (salmon, sailfish, kallisto) and summarize them into gene-level or transcript-level matrices for downstream differential expression analysis. This skill bridges fast quantification methods and statistical packages by providing length-corrected matrices that account for differential isoform usage across samples.

## When to use

You have transcript-level quantification files (quant.sf.gz or quant.gz) from salmon, sailfish, kallisto, or oarfish and need to aggregate them into gene-level or transcript-level count, abundance, and length matrices for input to DESeq2, edgeR, or limma-voom. Use this skill when you want to leverage transcript-level abundance estimates and inferred read counts while correcting for sample-specific changes in effective gene length caused by differential isoform usage.

## When NOT to use

- Your input is already a gene-level or transcript-level count matrix or DESeqDataSet/DGEList object—tximport is for raw quantification files only.
- You are working with alignment-based count data (BAM files) rather than quasi-alignment or pseudo-alignment quantification—use featureCounts, HTSeq, or similar instead.
- You need to perform alignment yourself; tximport assumes quantification is already complete and you have .sf or .gz output files.

## Inputs

- Quantification files (quant.sf.gz from salmon/sailfish/kallisto or quant.gz from oarfish)
- tx2gene data.frame (transcript IDs and corresponding gene IDs) or embedded gene IDs in quantification files
- Sample metadata (optional, for downstream tools but not required for tximport itself)

## Outputs

- tximport list object containing: abundance matrix (TPM), counts matrix (estimated read counts), length matrix (average transcript length weighted by abundance)
- Optionally: transcript-level matrices if txOut=TRUE
- Optionally: inferential replicate matrices if imported from Gibbs/bootstrap samples

## How to apply

First, construct a tx2gene mapping table (transcript ID → gene ID) from your reference annotation (e.g., Gencode) unless your quantification files already embed gene IDs. Then load the quantification files using tximport with the appropriate type argument ('salmon', 'sailfish', 'kallisto', or 'oarfish') and specify txOut=FALSE for gene-level summarization or txOut=TRUE to retain transcript-level matrices. The function imports three matrices: abundance (TPM), estimated counts, and average transcript length (weighted by sample-specific abundance). The length matrix is critical—it captures the average transcript length per gene per sample and serves as the basis for constructing an offset matrix in downstream tools (DESeq2, edgeR), which corrects for bias from differential isoform usage. If your quantifier supports inferential replicates (Gibbs samples or bootstrap samples), tximport can import these alongside point estimates to enable overdispersion modeling in edgeR. Verify that output matrix dimensions match your sample count and that length values are reasonable (typically 100–10,000 bp for protein-coding genes).

## Related tools

- **salmon** (Upstream quasi-alignment quantification tool producing transcript-level abundance and count estimates in quant.sf.gz files)
- **sailfish** (Upstream quasi-alignment quantification tool (predecessor to salmon) producing transcript-level estimates)
- **kallisto** (Upstream pseudo-alignment quantification tool producing transcript-level abundance and count estimates)
- **oarfish** (Long-read RNA-seq quantification tool producing transcript-level estimates in quant.gz format)
- **tximeta** (Extends tximport with automatic annotation metadata retrieval and addition to output objects)
- **readr** (Optional dependency that significantly accelerates file reading in tximport)
- **DESeq2** (Downstream differential expression package that accepts tximport output and uses embedded length matrix to construct offset for count-based analysis)
- **edgeR** (Downstream differential expression package that accepts tximport output; with divide=TRUE, accounts for inferential uncertainty via divided counts)
- **limma-voom** (Downstream differential expression package that accepts tximport output for gene-level analysis)

## Examples

```
library(tximport); txi <- tximport(files=quant_files, type='salmon', tx2gene=tx2gene, txOut=FALSE); abundance_matrix <- txi$abundance; offset_matrix <- log(txi$length)
```

## Evaluation signals

- Output list contains exactly three named matrices (abundance, counts, length) with dimensions matching the number of genes (or transcripts if txOut=TRUE) by number of samples.
- All values in the abundance matrix are non-negative and expressed in TPM units (typically summing to ~1e6 per sample).
- All values in the counts matrix are non-negative integers or fractional estimates; counts and abundance matrices should show expected correlation (higher abundance → higher counts).
- Length matrix contains positive values in the expected range for your organism (e.g., 100–10,000 bp for human protein-coding genes); length values vary across samples reflecting differential isoform usage.
- Successful downstream integration: the length matrix can be used to construct an offset matrix (via DESeq2::DESeqDataSetFromTximport or edgeR::DGEListFromTximport) without errors or dimension mismatches; overdispersion estimates (in edgeR or DESeq2) are reasonable and positive.

## Limitations

- tximport assumes quantification files are complete and correctly formatted; mismatched file lists or corrupted quant.sf/quant.gz files will cause import failure.
- The tx2gene mapping must be accurate and complete; transcripts not present in tx2gene will be discarded, potentially losing sensitivity.
- Aggregation to gene-level causes loss of transcript-level resolution; if transcript-level differential expression analysis is the primary goal, set txOut=TRUE and analyze transcript matrices directly.
- The length matrix reflects average transcript length weighted by sample-specific abundance; extreme outlier isoforms or annotation errors can inflate or deflate length estimates unpredictably.
- tximport does not handle multi-mapping reads differently from the upstream quantifier; if your quantifier assigns multi-mapping reads to a single transcript stochastically, that uncertainty is captured only via inferential replicates (if imported), not in point estimates.

## Evidence

- [readme] Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom.: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [readme] tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto.: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto."
- [intro] The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [intro] this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
