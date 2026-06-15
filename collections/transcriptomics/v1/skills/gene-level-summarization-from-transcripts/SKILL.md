---
name: gene-level-summarization-from-transcripts
description: Use when you have transcript-level quantification files (salmon quant.sf.gz, kallisto h5, or Sailfish output) and need to perform gene-level differential expression analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - tximeta
  - salmon
  - kallisto
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

# gene-level-summarization-from-transcripts

## Summary

Aggregate transcript-level abundance, counts, and length estimates into gene-level matrices using a transcript-to-gene mapping. This approach corrects for differential isoform usage across samples and enables gene-level differential expression analysis with improved statistical power.

## When to use

You have transcript-level quantification files (salmon quant.sf.gz, kallisto h5, or Sailfish output) and need to perform gene-level differential expression analysis. Use this skill when downstream analysis packages (DESeq2, edgeR, limma-voom) require gene-level count and abundance matrices, or when you need to account for sample-specific changes in transcript length due to isoform switching.

## When NOT to use

- Input data are already gene-level counts or abundance matrices (no transcript disaggregation needed).
- You intend to perform transcript-level or exon-level differential analysis exclusively (use txOut=TRUE argument or analyse transcript matrices instead).
- Transcript-to-gene mapping is unavailable or ambiguous (e.g., multi-gene loci or novel transcripts without annotation).

## Inputs

- transcript-level quantification files (quant.sf.gz from salmon, h5 from kallisto, or equivalent from Sailfish)
- tx2gene mapping file or data.frame (two columns: transcript ID, gene ID) – e.g., derived from Gencode GTF

## Outputs

- gene-level abundance matrix (TPM)
- gene-level estimated counts matrix
- gene-level average transcript length matrix (weighted by sample-specific abundance)

## How to apply

First, construct or load a tx2gene mapping data.frame associating each transcript ID with its gene ID (e.g., from Gencode annotation). Next, use tximport with the type argument matching your quantification tool ('salmon', 'kallisto', or 'sailfish') to read all transcript-level quantification files and summarize them to gene level via the tx2gene mapping. The function returns a list containing three matrices: gene-level abundance (TPM), estimated counts, and average transcript length weighted by sample-specific abundance. The length matrix can then be used to generate an offset for downstream gene-level differential analysis, accounting for potential length bias from differential isoform usage. Use readr package for faster file I/O if needed.

## Related tools

- **tximport** (Core function for importing transcript-level estimates and summarizing to gene-level matrices via tx2gene mapping) — https://github.com/thelovelab/tximport
- **tximeta** (Extension of tximport offering automatic addition of annotation metadata alongside summarization)
- **readr** (Optional dependency for significantly faster file reading when importing quantification files)
- **salmon** (Upstream quantification tool producing transcript-level estimates consumed by tximport)
- **kallisto** (Upstream quantification tool producing transcript-level estimates consumed by tximport)
- **DESeq2** (Downstream package for gene-level differential expression analysis using tximport-generated count matrix and length offset)
- **edgeR** (Downstream package for gene-level differential expression analysis using tximport-generated count matrix and length offset)
- **limma-voom** (Downstream package for gene-level differential expression analysis using tximport-generated count matrix and length offset)

## Examples

```
txi <- tximport(files = c('sample1.quant.sf.gz', 'sample2.quant.sf.gz'), type = 'salmon', tx2gene = tx2gene)
```

## Evaluation signals

- The returned list contains exactly three named matrices: 'abundance', 'counts', and 'length', with dimensions matching the number of genes × number of samples.
- All gene-level abundance values are numeric, non-negative, and reasonable in magnitude (typically TPM range 0–1000+ depending on sequencing depth).
- Gene-level counts are non-negative integers summed from transcript-level estimates.
- Length matrix values reflect transcript length (typically 100–10,000 bp) weighted by sample-specific transcript proportions, with variation across samples indicating differential isoform usage.
- No missing values (NA) appear in the matrices for genes with non-zero transcript abundance in the input.

## Limitations

- Requires a pre-constructed or annotation-derived tx2gene mapping; ambiguous transcript-to-gene relationships (e.g., overlapping or multi-mapping transcripts) may introduce bias.
- Changes in transcript length across samples are inferred from abundance-weighted isoform proportions; direct isoform composition information is not retained in the output.
- The approach does not discard multi-mapping fragments, which may increase sensitivity but also introduce ambiguity in gene assignment for highly homologous sequences.
- Gene-level analysis cannot capture transcript-specific effects; the authors note that gene-level differential expression should be complemented with transcript- or exon-level analysis for comprehensive inference.

## Evidence

- [other] tximport successfully produces gene-level matrices from transcript quantification: "tximport with type='salmon' and a tx2gene mapping produces a list containing gene-level abundance, counts, and length matrices from salmon quant.sf.gz files."
- [intro] Length matrix corrects for isoform-driven length variation: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] Create tx2gene mapping for summarization: "Transcripts need to be associated with gene IDs for gene-level summarization. If that information is present in the files, we can skip this step... We first make a data.frame called tx2gene with two"
- [intro] Import transcript estimates with type argument: "The tximport package has a single function for importing transcript-level estimates. The type argument is used to specify what software was used for estimation"
- [intro] Generate three gene-level matrices: "A simple list with matrices, 'abundance', 'counts', and 'length', is returned, where the transcript level information is summarized to the gene-level"
- [intro] Use length matrix as offset for DEA: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] tximport imports multiple quantification formats: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
- [readme] Downstream packages require gene-level matrices: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom"
