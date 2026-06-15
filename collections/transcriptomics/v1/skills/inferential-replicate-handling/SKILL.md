---
name: inferential-replicate-handling
description: Use when when performing transcript- or gene-level differential expression analysis and your quantification tool (Salmon, Sailfish, or kallisto) has produced Gibbs sample or bootstrap sample replicates, and you want edgeR to account for inferential uncertainty rather than treating point estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0099
  - http://edamontology.org/topic_3308
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

# inferential-replicate-handling

## Summary

Import and propagate inferential replicates (Gibbs samples or bootstrap samples) from quantification tools (Salmon, Sailfish, kallisto) through tximport to enable edgeR to estimate count overdispersion and generate divided counts that account for quantification uncertainty in differential expression analysis.

## When to use

When performing transcript- or gene-level differential expression analysis and your quantification tool (Salmon, Sailfish, or kallisto) has produced Gibbs sample or bootstrap sample replicates, and you want edgeR to account for inferential uncertainty rather than treating point estimates as fixed counts.

## When NOT to use

- Input quantification files do not contain Gibbs samples or bootstrap replicates (use standard tximport import instead)
- You require only point estimates of abundance without uncertainty propagation
- Performing analysis with tools other than edgeR that do not support inferential replicate integration

## Inputs

- tximport object with inferential replicates (Gibbs samples or bootstrap samples from Salmon/Sailfish/kallisto quantification)
- salmon_gibbs files or equivalent bootstrap sample files from upstream quantification tool
- Sample metadata and experimental design information

## Outputs

- DGEList object with divided counts and offset-adjusted library size factors
- Common dispersion and tagwise dispersion estimates derived from inferential replicate variance
- Offset matrix for quasi-likelihood differential expression inference

## How to apply

Load transcript-level quantification files containing Gibbs samples or bootstrap replicates using tximport with type='salmon' (or equivalent for Sailfish/kallisto) and txOut=TRUE to retain transcript-level output. Pass the tximport object to edgeR::DGEListFromTximport with divide=TRUE; this function automatically extracts the inferential replicates embedded in the tximport output and uses them to estimate count overdispersion, producing a DGEList with offset-adjusted counts that account for the probabilistic assignment of reads to transcripts. The divide=TRUE parameter divides counts by library size and generates offset matrices suitable for quasi-likelihood (QL) dispersion estimation in edgeR's quasi-likelihood pipeline. Verify the resulting DGEList contains both common dispersion and tagwise dispersion estimates, confirming overdispersion modeling is ready for downstream statistical testing.

## Related tools

- **tximport** (Imports transcript-level abundance, counts, and transcript lengths; extracts and retains Gibbs sample or bootstrap replicate information for downstream uncertainty quantification) — https://github.com/thelovelab/tximport
- **edgeR** (Uses inferential replicates via DGEListFromTximport with divide=TRUE to estimate count overdispersion and produce divided counts suitable for quasi-likelihood differential expression inference)
- **Salmon** (Upstream quantification tool that generates Gibbs sample replicates of transcript-level abundance and counts, imported by tximport)
- **Sailfish** (Upstream quantification tool that generates Gibbs sample replicates of transcript-level abundance and counts, imported by tximport)
- **kallisto** (Upstream quantification tool that generates bootstrap sample replicates of transcript-level abundance and counts, imported by tximport)

## Examples

```
txi <- tximport(files, type='salmon', txOut=TRUE); dge <- edgeR::DGEListFromTximport(txi, divide=TRUE); dge <- edgeR::estimateDisp(dge, design)
```

## Evaluation signals

- DGEList object contains a non-empty counts matrix with divided counts (scaled by library size) and an offset matrix
- Common dispersion estimate is present and positive (typically 0.01–0.5 for RNA-seq)
- Tagwise dispersion estimates exist and are greater than or equal to common dispersion
- Comparison of dispersion estimates with and without divide=TRUE shows reduced variance inflation when inferential replicates are used
- Downstream quasi-likelihood F-test results are stable and produce credible false-discovery rates

## Limitations

- Requires that upstream quantification tool explicitly output Gibbs samples or bootstrap replicates; point estimates alone cannot be used
- divide=TRUE is designed for quasi-likelihood (QL) pipeline; traditional edgeR likelihood-ratio test may benefit differently from variance estimation
- Computational overhead increases with the number of inferential replicates (typically 20–100 Gibbs samples); balance between accuracy and runtime required
- Offset-based correction assumes that length bias is captured by the average transcript length weighted by sample-specific abundance, which may not hold for extreme differential isoform usage

## Evidence

- [readme] tximport version capability: "tximport as of version 1.3.9 will import inferential replicates (Gibbs samples or bootstrap samples) from Salmon, Sailfish or kallisto"
- [other] DGEListFromTximport with divide parameter: "DGEListFromTximport with divide=TRUE estimates count overdispersion from inferential replicates and produces divided counts suitable for transcript-level differential expression analysis, accounting"
- [other] Workflow for applying the skill: "Load tximportData salmon_gibbs files containing transcript-level abundance estimates and Gibbs sample replicates using tximport function with type='salmon' and txOut=TRUE to retain transcript-level"
- [other] Verification of correct application: "Extract and validate presence of common dispersion and tagwise dispersion estimates within the DGEList to confirm overdispersion modeling readiness"
- [intro] Core benefit and rationale: "this approach corrects for potential changes in gene length across samples (e.g. from differential isoform usage)"
