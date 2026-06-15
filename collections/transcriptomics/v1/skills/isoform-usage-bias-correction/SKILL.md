---
name: isoform-usage-bias-correction
description: 'Use when when performing gene-level differential expression analysis on RNA-seq data where samples may express different isoforms of the same gene at different relative abundances. Specifically: (1) you have transcript-level quantification (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_3308
  tools:
  - tximport
  - DESeq2
  - edgeR
  - limma-voom
  - salmon
  - kallisto
  - Sailfish
  - tximeta
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

# isoform-usage-bias-correction

## Summary

Correct gene-level differential expression analysis for changes in effective gene length arising from differential isoform usage across samples by embedding a transcript-length-derived offset matrix in the count matrix. This prevents bias in downstream DE inference when isoform composition varies between conditions.

## When to use

When performing gene-level differential expression analysis on RNA-seq data where samples may express different isoforms of the same gene at different relative abundances. Specifically: (1) you have transcript-level quantification (e.g., from salmon, kallisto, or Sailfish) with estimated transcript abundances and lengths; (2) you are aggregating transcript-level counts to gene level; (3) you are NOT performing transcript-level analysis exclusively; and (4) your downstream tool is DESeq2, edgeR, or limma-voom. The offset correction is essential because differential isoform usage changes the average transcript length per gene in a sample-specific manner, which would otherwise inflate or deflate gene-level fold-change estimates.

## When NOT to use

- Input is already a pre-normalized or batch-corrected feature table (e.g., log2-CPM, variance-stabilized values, or posterior counts) — offsets must be embedded before normalization and modeling.
- You are performing transcript-level differential analysis only (use txOut=TRUE in tximport and analyze transcript counts directly without gene-level aggregation).
- Quantification was performed using alignment-based methods that already output gene-level counts (e.g., featureCounts, HTSeq) — the offset correction is specific to transcript-level estimates that must be summarized to gene level.

## Inputs

- tximport list object (containing 'counts', 'abundance', and 'length' matrices at gene level)
- sample metadata table (colData) with sample identifiers and condition/group assignments
- tx2gene mapping data.frame (transcript ID → gene ID)

## Outputs

- DESeqDataSet object with embedded offset matrix (or equivalent count-plus-offset object for edgeR/limma)
- offset matrix (sample × gene, log scale, ready for DE model)

## How to apply

Import transcript-level abundance, counts, and length estimates using tximport with the type argument set to match your quantification software (e.g., type='salmon'). Provide a tx2gene mapping table (transcript ID to gene ID associations) to aggregate transcript-level matrices into gene-level matrices: a 'counts' matrix (summed transcript counts per gene), an 'abundance' matrix (averaged transcript abundances per gene), and a 'length' matrix (weighted average transcript length per gene, weighted by sample-specific transcript abundance). The length matrix encodes the sample-specific transcript-length variation caused by differential isoform usage. Pass the tximport output list (txi) and sample metadata to DESeq2::DESeqDataSetFromTximport (or equivalent functions in edgeR/limma), which automatically constructs an offset matrix from the length matrix. The offset is calculated as the average log-length across all samples for each gene, then subtracted from each sample's log-length for that gene, producing a sample–gene-specific correction term that is embedded in the model and applied during dispersion estimation and statistical testing. This ensures that changes in effective gene length are accounted for in the likelihood ratio test, preventing spurious DE calls due to isoform switching rather than true abundance changes.

## Related tools

- **tximport** (Imports transcript-level abundance, counts, and length matrices from quantification software (salmon, kallisto, Sailfish); aggregates to gene level using tx2gene mapping; produces the length matrix that encodes isoform-usage-driven gene-length variation.) — https://github.com/thelovelab/tximport
- **DESeq2** (Accepts tximport output and automatically constructs the offset matrix from the length matrix; embeds offset in the negative binomial GLM used for gene-level differential expression inference.)
- **edgeR** (Alternative downstream tool for gene-level differential expression that can use a length-derived offset matrix to correct for differential isoform usage.)
- **limma-voom** (Alternative downstream tool for gene-level differential expression that can incorporate a length-derived offset.)
- **salmon** (Upstream transcript-level quantification software; produces transcript abundance and length estimates that tximport imports and summarizes.)
- **kallisto** (Upstream transcript-level quantification software; produces transcript abundance and length estimates that tximport imports and summarizes.)
- **Sailfish** (Upstream transcript-level quantification software; produces transcript abundance and length estimates that tximport imports and summarizes.)
- **tximeta** (Extension of tximport that provides the same transcript-level import and gene-level summarization functionality, plus automatic addition of annotation metadata.)

## Examples

```
txi <- tximport(salmon_quant_files, type='salmon', tx2gene=tx2gene); dds <- DESeqDataSetFromTximport(txi, colData=sample_table, design=~condition)
```

## Evaluation signals

- Verify that the DESeqDataSet object contains a non-null assay named 'offset' (or check normalizationFactors() in DESeq2) with dimensions matching the count matrix (samples × genes). The offset values should vary across samples for each gene, reflecting sample-specific differences in average transcript length.
- Confirm that the offset matrix is on the log scale and is centered approximately around zero (i.e., mean offset ≈ 0 per gene), indicating it represents deviations from the per-gene baseline length.
- Run DESeq2::DESeq() and inspect the fitted model: the offset should be passed to the likelihood ratio test. Compare DE results (log fold-changes, p-values, significant gene lists) against results computed without the offset; inclusion of the offset should stabilize log-fold-change estimates in genes with strong isoform-usage differences and reduce spurious DE calls caused by differential isoform composition rather than true abundance shifts.
- Check that the length matrix from tximport shows sample-specific variation (i.e., the same gene has different average lengths across samples), confirming that isoform-usage heterogeneity is present and the offset correction is meaningful.
- Validate that tx2gene mapping is complete and one-to-many (one gene per transcript, possibly many transcripts per gene) by confirming no transcript IDs are lost and no genes are duplicated in the aggregated count/length matrices.

## Limitations

- The offset correction assumes that the length matrix accurately represents average transcript length weighted by transcript abundance. Errors in transcript quantification or length estimates from the upstream quantifier (salmon, kallisto, Sailfish) will propagate into the offset.
- The method corrects for changes in average transcript length but does not directly model the underlying isoform-switching event; if isoform switching is itself of scientific interest, transcript-level analysis (txOut=TRUE) may be more appropriate and should complement gene-level analysis.
- The offset is most effective when isoform-usage variation is substantial and correlated with experimental conditions. If isoform composition is largely invariant across samples, the offset will have little practical impact, though it should not introduce bias.
- The README notes that gene-level differential expression analysis can be complemented with transcript- or exon-level analysis; relying on gene-level analysis alone may obscure condition-specific isoform switches and their biological meaning, especially in genes with multiple isoforms.

## Evidence

- [intro] tximport corrects for potential changes in gene length across samples from differential isoform usage: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
- [intro] tximport generates a length matrix for offset computation in downstream differential expression: "The 'length' matrix can be used to generate an offset matrix for downstream gene-level differential analysis of count matrices"
- [readme] tximport imports transcript-level estimates and summarizes to gene level for use with DESeq2, edgeR, and limma-voom: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom."
- [methods] DESeqDataSetFromTximport automatically embeds the offset matrix from tximport's length matrix: "DESeq2::DESeqDataSetFromTximport accepts a tximport list object (containing gene-level counts, abundance, and length matrices) and a sample table, and automatically constructs the appropriate offset"
- [readme] tximport supports transcript-level import from salmon, kallisto, and Sailfish with inferential replicates: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
