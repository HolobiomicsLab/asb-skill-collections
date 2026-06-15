---
name: transcript-level-count-aggregation
description: Use when you have transcript-level abundance and count estimates from salmon, sailfish, kallisto, or oarfish and need gene-level matrices for downstream differential analysis with edgeR, DESeq2, or limma-voom.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - summarizeToGene
  - salmon
  - kallisto
  - sailfish
  - oarfish
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

# transcript-level-count-aggregation

## Summary

Aggregate transcript-level quantification estimates (abundance, counts, and length) from RNA-seq quantification tools into gene-level matrices suitable for differential expression analysis. This approach corrects for differential isoform usage across samples by incorporating sample-specific weighted average transcript lengths as offsets.

## When to use

You have transcript-level abundance and count estimates from salmon, sailfish, kallisto, or oarfish and need gene-level matrices for downstream differential analysis with edgeR, DESeq2, or limma-voom. Use this skill when your research goal is gene-level inference but you want to leverage transcript-level quantification to account for length bias from isoform switching.

## When NOT to use

- Input quantification is already summarized to gene level (not transcript-level estimates).
- Your analysis goal is transcript-level differential expression, not gene-level; use txOut=TRUE instead.
- You are using alignment-based quantification (e.g., featureCounts, HTSeq) rather than pseudo-alignment tools.

## Inputs

- transcript-level quantification files (quant.sf for salmon/sailfish, abundance.h5 for kallisto, quant.gz for oarfish)
- tx2gene data.frame (two columns: transcript ID and corresponding gene ID)

## Outputs

- gene-level abundance matrix
- gene-level count matrix (estimated counts)
- gene-level length matrix (weighted average transcript length per sample)

## How to apply

Load transcript quantification files using tximport with the type argument matching your upstream quantification tool (salmon, sailfish, kallisto, or oarfish). Provide a tx2gene data.frame mapping transcript IDs to gene IDs. Set txOut=FALSE (or omit it) to directly generate gene-level matrices in a single pass, or use txOut=TRUE followed by summarizeToGene for transparency. The tximport function returns a list containing abundance, counts, and length matrices, where each value is aggregated to gene level via transcript abundance weighting. Use the length matrix as an offset in downstream statistical models to adjust for sample-specific changes in gene length due to differential isoform usage.

## Related tools

- **tximport** (Core function to import transcript-level estimates and aggregate to gene level; handles type-specific file parsing and summarization.) — github:thelovelab__tximport
- **summarizeToGene** (Post-hoc aggregation function to collapse tximport transcript-level output (txOut=TRUE) to gene level using tx2gene mapping.) — github:thelovelab__tximport
- **salmon** (Upstream quantification tool producing transcript-level estimates in quant.sf format consumed by tximport.)
- **kallisto** (Upstream quantification tool producing transcript-level estimates in abundance.h5 or abundance.tsv format consumed by tximport.)
- **sailfish** (Upstream quantification tool producing transcript-level estimates in quant.sf format consumed by tximport.)
- **oarfish** (Upstream long-read RNA-seq quantification tool producing transcript-level estimates in quant.gz format consumed by tximport with type='oarfish'.)
- **DESeq2** (Downstream differential expression analysis package that receives gene-level count matrices and length offset matrices from tximport.)
- **edgeR** (Downstream differential expression analysis package that receives gene-level count matrices and length offset matrices from tximport.)
- **limma-voom** (Downstream differential expression analysis package that receives gene-level count matrices and length offset matrices from tximport.)
- **readr** (Optional dependency for faster file I/O; tximport can use readr::read_delim for significantly faster loading of quantification files.)

## Examples

```
library(tximport); files <- c('sample1_quant.sf', 'sample2_quant.sf'); names(files) <- c('sample1', 'sample2'); txi <- tximport(files, type='salmon', tx2gene=tx2gene, txOut=FALSE); head(txi$counts)
```

## Evaluation signals

- Gene-level count matrices produced directly via txOut=FALSE are identical (all.equal) to those produced by txOut=TRUE followed by summarizeToGene, confirming correct aggregation logic.
- Matrix dimensions match expected number of genes (rows) and samples (columns); no rows or columns are duplicated or lost.
- Length matrix contains positive numeric values reflecting weighted average transcript length; values change across samples when isoform usage varies.
- Abundance matrix sums to 1.0 per sample, reflecting normalized TPM-like estimates; count matrix contains non-negative integers.
- No NA or NaN values in output matrices unless input files genuinely contained missing estimates; matrix structure is consistent across replicates.

## Limitations

- Requires a valid tx2gene mapping; if transcript IDs in quantification files do not match the mapping, aggregation will fail or produce empty genes.
- Transcript-level estimates from salmon, sailfish, or kallisto are bootstrap/Gibbs samples that reflect quantification uncertainty; this uncertainty is averaged away during aggregation, so downstream offset-based adjustment assumes point estimates are reliable.
- The length offset assumes that average transcript length differences across samples are informative and not driven by technical artifacts; misspecified isoform quantification can propagate bias.
- tximport does not validate that tx2gene is complete or non-redundant; duplicate or missing mappings may produce unexpected results.
- Gene-level aggregation loses all transcript-level information; if transcript-level or exon-level effects are of interest, use txOut=TRUE and analyze transcripts separately.

## Evidence

- [readme] Imports and aggregation rationale: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [intro] Length correction mechanism: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] Workflow step: import with type argument: "The tximport package has a single function for importing transcript-level estimates. The type argument is used to specify what software was used for estimation"
- [intro] Workflow step: create tx2gene mapping: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [intro] Output matrix types and aggregation: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] Length matrix as offset: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] txOut parameter for aggregation control: "The argument `txOut=TRUE` can be used to generate transcript-level matrices."
- [other] Task validation: equivalence of direct vs post-hoc aggregation: "Gene-level count matrices derived from transcript-level tximport output (txOut=TRUE) followed by summarizeToGene are identical to those produced by direct gene-level tximport (txOut=FALSE)"
