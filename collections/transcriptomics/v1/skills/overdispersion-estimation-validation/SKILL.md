---
name: overdispersion-estimation-validation
description: Use when after using edgeR::DGEListFromTximport with divide=TRUE on tximport output containing Gibbs sample or bootstrap replicates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - edgeR
  - Salmon
  - Sailfish
  - kallisto
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

# overdispersion-estimation-validation

## Summary

Validate that count overdispersion has been correctly estimated from inferential replicates (Gibbs samples or bootstrap samples) when using divided counts for transcript-level differential expression. This skill ensures that the DGEList object contains appropriate dispersion estimates—common and tagwise—necessary for reliable statistical inference in edgeR.

## When to use

Apply this skill after using edgeR::DGEListFromTximport with divide=TRUE on tximport output containing Gibbs sample or bootstrap replicates. Validation is essential before proceeding to dispersion estimation or statistical testing, to confirm that the division of counts by inferential replicates has produced a DGEList object with populated dispersion estimates suitable for modeling count overdispersion.

## When NOT to use

- Input does not contain inferential replicates (Gibbs samples or bootstrap samples); DGEListFromTximport with divide=TRUE requires these to estimate overdispersion.
- Analysis goal is gene-level (not transcript-level) differential expression; use txOut=FALSE in tximport and gene-level counts instead.
- DGEList has already been processed through estimateDisp() or other edgeR dispersion-fitting functions; validation is redundant after formal dispersion estimation.

## Inputs

- tximport output object (list with 'abundance', 'counts', 'length' matrices and Gibbs/bootstrap sample replicates) generated with txOut=TRUE and type='salmon'/'sailfish'/'kallisto'

## Outputs

- DGEList object with divided counts matrix
- common.dispersion estimate (numeric scalar)
- tagwise.dispersion vector (numeric, one per transcript)

## How to apply

After calling edgeR::DGEListFromTximport with divide=TRUE on tximport output (generated with txOut=TRUE for transcript-level and containing inferential replicates from Salmon, Sailfish, or kallisto), inspect the resulting DGEList object structure to verify: (1) presence of a count matrix with divided counts adjusted for library size; (2) presence of common dispersion estimate (accessible via dge$common.dispersion); (3) presence of tagwise dispersion estimates (accessible via dge$tagwise.dispersion or dge$genes column). The divide=TRUE parameter estimates overdispersion from the inferential replicates by accounting for the probabilistic assignment of reads to transcripts. Confirm these estimates are numeric and non-null before proceeding to differential expression testing.

## Related tools

- **tximport** (imports transcript-level abundance, estimated counts, transcript lengths, and inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish, or kallisto for downstream analysis) — https://github.com/thelovelab/tximport
- **edgeR** (provides DGEListFromTximport function to convert tximport output into a DGEList with divided counts and overdispersion estimates)
- **Salmon** (upstream quantification tool that generates transcript-level abundance estimates and Gibbs samples for use with tximport)
- **Sailfish** (upstream quantification tool that generates transcript-level abundance estimates and bootstrap samples for use with tximport)
- **kallisto** (upstream quantification tool that generates transcript-level abundance estimates and bootstrap samples for use with tximport)

## Examples

```
txi <- tximport(files, type='salmon', tx2gene=tx2gene, txOut=TRUE, importer=readr::read_delim); dge <- edgeR::DGEListFromTximport(txi, divide=TRUE); stopifnot(!is.null(dge$common.dispersion) && !is.null(dge$tagwise.dispersion))
```

## Evaluation signals

- DGEList object structure contains non-null 'counts' matrix with numeric, divided count values and library size factors
- common.dispersion slot is populated with a single positive numeric scalar representing gene-level overdispersion
- tagwise.dispersion slot (or equivalent in $genes data frame) contains a numeric vector with one dispersion estimate per transcript; all values are positive and finite
- Dispersion estimates are smaller than or comparable to those from alignment-based methods, reflecting improved precision from inferential replicate information
- DGEList$samples contains correct library size (lib.size) and normalization factors reflecting the divide operation

## Limitations

- divide=TRUE parameter requires inferential replicates (Gibbs or bootstrap samples) in the tximport input; standard point-estimate quantification (without replicates) will not produce meaningful overdispersion estimates via this method.
- The quality of overdispersion estimates depends on the number and coverage of inferential replicates provided by the upstream quantification method; sparse or low-coverage replicates may lead to unreliable estimates.
- Validation of dispersion estimates is structural and numerical; biological validity requires downstream evaluation of differential expression results (e.g., concordance with known biology, reproducibility across independent samples).

## Evidence

- [other] DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting for the probabilistic assignment of reads to transcripts.: "DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting"
- [readme] tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
- [other] Extract and validate presence of common dispersion and tagwise dispersion estimates within the DGEList to confirm overdispersion modeling readiness.: "Extract and validate presence of common dispersion and tagwise dispersion estimates within the DGEList to confirm overdispersion modeling readiness"
- [readme] Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom.: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom"
- [intro] this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
