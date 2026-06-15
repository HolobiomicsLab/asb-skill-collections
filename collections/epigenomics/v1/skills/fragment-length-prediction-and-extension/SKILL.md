---
name: fragment-length-prediction-and-extension
description: Use when after filtering duplicate reads from ChIP-Seq data but before generating pileup coverage tracks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3218
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_3674
  tools:
  - macs3 predictd
  - macs3 pileup
derived_from:
- doi: 10.1186/gb-2008-9-9-r137
  title: macs
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_macs
    doi: 10.1186/gb-2008-9-9-r137
    title: macs
  dedup_kept_from: coll_macs
schema_version: 0.2.0
---

# fragment-length-prediction-and-extension

## Summary

Estimate the DNA fragment length (d) from ChIP-Seq data using cross-correlation analysis, then extend aligned reads to this length to generate accurate ChIP coverage tracks. This step is critical for converting point-wise read alignments into fragment-level signal representation.

## When to use

After filtering duplicate reads from ChIP-Seq data but before generating pileup coverage tracks. Apply this skill when you have aligned ChIP reads in BED format and need to construct coverage BEDGRAPH files that reflect the actual DNA fragment distribution rather than single-end read positions.

## When NOT to use

- Input reads are already paired-end (BEDPE format) — use the observed fragment length distribution from BEDPE instead of re-predicting.
- Fragment length is known a priori from sequencing metadata — skip prediction and use the known value directly with --extsize.
- Control sample is being processed — predictd should only be applied to ChIP data, not input/control data.

## Inputs

- Filtered ChIP-Seq reads in BED format (e.g., CTCF_ChIP_200K.bed.gz)
- Genome size specification (e.g., 'hs' for human, or explicit bp count)

## Outputs

- Predicted fragment length scalar d (integer, in base pairs)
- ChIP coverage BEDGRAPH track (genomic coordinates × extended fragment count)

## How to apply

First, run macs3 predictd on the filtered ChIP sample using parameters -g hs (human genome size) and -m 5 50 (search fragment length range 5–50 bp) to estimate the dominant fragment length d from cross-correlation peaks. The tool analyzes the distribution of reads across the genome and returns a single scalar d value. Next, use macs3 pileup with the --extsize parameter set to d to extend each filtered ChIP read bidirectionally (or in a strand-aware manner) to the predicted fragment length. This produces a BEDGRAPH file where each genomic position reflects the number of extended fragments covering it, not raw reads. The predicted fragment length d should typically fall within the sequencing protocol's expected range (e.g., 150–200 bp for typical ChIP-Seq); anomalous values (< 50 bp or > 500 bp) warrant re-examination of sequencing quality and read filtering.

## Related tools

- **macs3 predictd** (Estimates fragment length d from ChIP read cross-correlation) — https://github.com/macs3-project/MACS
- **macs3 pileup** (Extends filtered reads to fragment length d and generates coverage BEDGRAPH) — https://github.com/macs3-project/MACS

## Examples

```
macs3 predictd -i CTCF_ChIP_200K.bed.gz -g hs -m 5 50 && macs3 pileup -i CTCF_ChIP_200K.bed.gz -o CTCF_ChIP_pileup.bdg --extsize 147
```

## Evaluation signals

- Predicted fragment length d is within the expected range for the sequencing protocol and sample type (typically 100–300 bp for ChIP-Seq).
- macs3 predictd completes without error and outputs a single numeric d value to stdout or log.
- Generated BEDGRAPH has non-zero coverage at genomic regions expected to harbor the target protein (e.g., known binding sites for CTCF).
- BEDGRAPH coverage values are integers ≥ 1 and reflect the number of fragments, not raw reads; coverage should be lower than a raw (non-extended) pileup at the same loci.
- Fragment length d is consistent across replicate ChIP samples of the same protein/cell type.

## Limitations

- predictd assumes a single dominant fragment length; heterogeneous fragment size distributions (e.g., from degraded chromatin or mixed library sizes) may yield biased or multimodal estimates.
- Prediction quality depends on sequencing depth and the strength of ChIP enrichment; low-coverage or weak-signal ChIP samples may produce unreliable d estimates.
- predictd is designed for single-end ChIP-Seq; paired-end data should use empirical fragment length from BEDPE files instead.
- Extension by a single scalar d does not account for fragment-length heterogeneity or strand-specific biases; more sophisticated approaches (e.g., fragment-length-aware probabilistic models) may be needed for high-resolution analyses.

## Evidence

- [methods] This is a crucial step for analyzing ChIP-Seq with MACS3, as well as other types of data: "This is a crucial step for analyzing ChIP-Seq with MACS3"
- [methods] Predict fragment length d from the filtered ChIP sample using macs3 predictd with -g hs and -m 5 50 parameters: "Predict fragment length d from the filtered ChIP sample using macs3 predictd with -g hs and -m 5 50 parameters"
- [methods] Generate ChIP pileup BEDGRAPH by extending filtered ChIP reads to the predicted fragment length d using macs3 pileup with --extsize parameter: "Generate ChIP pileup BEDGRAPH by extending filtered ChIP reads to the predicted fragment length d using macs3 pileup with --extsize parameter"
- [methods] This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data: "This can also be accomplished using the `predictd` subcommand, which we need to apply only to ChIP data"
- [methods] generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand: "generate a pileup track for the ChIP sample using the MACS3 `pileup` subcommand"
