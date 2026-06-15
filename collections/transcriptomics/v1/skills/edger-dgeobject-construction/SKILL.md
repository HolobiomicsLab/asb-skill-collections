---
name: edger-dgeobject-construction
description: Use when you have transcript-level abundance estimates and count matrices from tximport (derived from Salmon, Sailfish, or kallisto output) and need to prepare them for differential expression analysis in edgeR.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - edgeR
  - salmon
  - kallisto
  - Sailfish
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
- use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom
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

# edger-dgeobject-construction

## Summary

Construct a DGEList object from transcript-level quantification estimates using edgeR's DGEListFromTximport function, optionally with divided counts to account for inferential uncertainty from quantification tools. This enables downstream differential expression analysis while preserving transcript-level resolution and probabilistic assignment of reads to transcripts.

## When to use

You have transcript-level abundance estimates and count matrices from tximport (derived from Salmon, Sailfish, or kallisto output) and need to prepare them for differential expression analysis in edgeR. Use this skill particularly when working with Gibbs sample or bootstrap inferential replicates from your quantification method, which capture uncertainty in read-to-transcript assignment that should be reflected in overdispersion estimates.

## When NOT to use

- Input is already gene-level summarized (txOut=FALSE in tximport); construct DGEList from gene counts directly instead
- You are performing alignment-free quantification without inferential replicates and do not need divided counts; a standard DGEList constructor may suffice
- Your upstream quantification does not come from salmon, sailfish, or kallisto; verify the quantification tool is supported by tximport first

## Inputs

- tximport output object (transcript-level, txOut=TRUE)
- tximport object with Gibbs sample or bootstrap inferential replicates (optional but recommended)

## Outputs

- DGEList object with transcript-level count matrix
- Library size factors embedded in DGEList
- Common and tagwise dispersion estimates
- Offset-adjusted counts (if divide=TRUE)

## How to apply

Load tximport output (obtained from transcript-level quantification with txOut=TRUE) into edgeR::DGEListFromTximport, setting divide=TRUE if inferential replicates are available to estimate count overdispersion from the replicate samples. This produces a DGEList object with divided counts offset by library size and transcript-level abundance variability. The function automatically calculates common and tagwise dispersion estimates from the divided replicates, making the resulting object ready for negative binomial modeling. Inspect the DGEList structure to verify the count matrix, library size normalization factors, and dispersion estimates are present before proceeding to statistical testing.

## Related tools

- **tximport** (Import transcript-level abundance estimates, counts, and lengths from quantification output; supply input to DGEListFromTximport) — https://github.com/thelovelab/tximport
- **edgeR** (Perform negative binomial differential expression analysis on DGEList objects; DGEListFromTximport is a constructor within edgeR)
- **salmon** (Upstream quantification tool; generates transcript-level abundance and inferential replicates imported by tximport)
- **kallisto** (Upstream quantification tool; generates transcript-level abundance and bootstrap samples imported by tximport)
- **Sailfish** (Upstream quantification tool; generates transcript-level abundance and inferential replicates imported by tximport)

## Examples

```
txi <- tximport(files, type='salmon', txOut=TRUE); dge <- edgeR::DGEListFromTximport(txi, divide=TRUE)
```

## Evaluation signals

- DGEList object is successfully created with no errors or warnings from DGEListFromTximport
- Count matrix within DGEList has expected dimensions (transcripts × samples) and contains non-negative integer or divided counts
- Library size factors (or normalization offsets) are present and reasonable in magnitude (typically in range of sample sequencing depth)
- Common dispersion and tagwise dispersion estimates are computed and present in the DGEList object; check via $common.dispersion and $tagwise.dispersion slots
- If divide=TRUE was used, verify that counts reflect division by variance inflation from inferential replicates; raw counts should be smaller than if divide=FALSE

## Limitations

- DGEListFromTximport with divide=TRUE requires inferential replicates (Gibbs or bootstrap samples) from the quantification step; point estimates alone cannot estimate overdispersion
- Transcript-level analysis does not preclude but complements gene-level analysis; users should consider performing both transcript- and gene-level differential expression to capture isoform-specific effects
- Potential bias from differential isoform usage across samples is corrected at the transcript level, but downstream gene-level summarization may obscure transcript-specific signals

## Evidence

- [other] DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting for the probabilistic assignment of reads to transcripts.: "DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting"
- [readme] tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
- [readme] Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR, DESeq2, limma-voom: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages such as edgeR"
- [other] Extract and validate presence of common dispersion and tagwise dispersion estimates within the DGEList to confirm overdispersion modeling readiness.: "Extract and validate presence of common dispersion and tagwise dispersion estimates within the DGEList to confirm overdispersion modeling readiness"
- [intro] this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage): "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
