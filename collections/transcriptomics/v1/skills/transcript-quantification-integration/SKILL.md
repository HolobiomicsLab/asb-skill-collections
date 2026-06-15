---
name: transcript-quantification-integration
description: Use when you have transcript quantification output (TPM or raw counts) from a pseudo-aligner (Salmon or kallisto) and an ioe/ioi event definition file from SUPPA2's generateEvents step, and you need to calculate PSI values—the relative inclusion level of alternative splicing events—across multiple.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0654
  tools:
  - SUPPA2
  - Salmon
  - kallisto
derived_from:
- doi: 10.1186/s13059-018-1417-1
  title: suppa2
evidence_spans:
- 'SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_suppa2
    doi: 10.1186/s13059-018-1417-1
    title: suppa2
  dedup_kept_from: coll_suppa2
schema_version: 0.2.0
---

# transcript-quantification-integration

## Summary

Integrate transcript abundance quantification (TPM or counts from Salmon/kallisto) with SUPPA2 event definitions to compute PSI (Percent Spliced In) values across samples. This skill bridges isoform-level expression data to alternative splicing event-level analysis by aggregating transcript abundances according to event structure.

## When to use

You have transcript quantification output (TPM or raw counts) from a pseudo-aligner (Salmon or kallisto) and an ioe/ioi event definition file from SUPPA2's generateEvents step, and you need to calculate PSI values—the relative inclusion level of alternative splicing events—across multiple samples for downstream differential splicing or clustering analysis.

## When NOT to use

- Input transcript quantification is not in TPM or count format (e.g. is already normalized or log-transformed in a non-standard way).
- No event definition file (ioe/ioi) is available; PSI calculation requires explicit specification of which transcripts form the numerator and denominator.
- Transcript-level abundance data are missing or incomplete (e.g. only gene-level counts are available).

## Inputs

- Transcript quantification matrix (TPM or count values; e.g. from Salmon or kallisto output)
- SUPPA2 ioe file (local alternative splicing event definitions with transcript assignments)
- SUPPA2 ioi file (transcript/isoform event definitions with gene-level transcript sets)

## Outputs

- PSI matrix (tab-separated file with events/isoforms as rows, samples as columns)
- PSI values per event or per isoform (0–1 scale representing relative inclusion level)

## How to apply

Load the transcript quantification matrix (TPM or counts, one transcript per row, one sample per column) and the ioe or ioi event definition file specifying which transcripts contribute to the numerator (inclusion form) and denominator (both forms) of each event's PSI calculation. Execute SUPPA2's psiPerEvent or psiPerIsoform subcommand, which aggregates transcript abundances by event structure: PSI = (sum of transcripts in numerator) / (sum of transcripts in denominator). The tool outputs a PSI matrix with events/isoforms as rows and samples as columns. Choose ioe for local alternative splicing events (SE, A5/A3, MX, RI, AF/AL) or ioi for transcript-level (isoform-centric) analysis when splicing patterns are too complex for simple event models.

## Related tools

- **SUPPA2** (Executes psiPerEvent and psiPerIsoform subcommands to aggregate transcript abundances into PSI values for alternative splicing events and transcripts) — https://github.com/comprna/SUPPA
- **Salmon** (Produces transcript-level quantification output (TPM) used as input to PSI calculation)
- **kallisto** (Produces transcript-level quantification output (TPM or counts) used as input to PSI calculation)

## Examples

```
python3 suppa.py psiPerEvent --ioe-file events.ioe --expression-file transcript_quantification.tsv -o psi_matrix
```

## Evaluation signals

- PSI values are bounded to [0, 1] for all events/isoforms and samples; values outside this range indicate calculation error.
- PSI matrix dimensions match the number of events (or transcripts) in the ioe/ioi file × number of samples in the quantification matrix.
- Events with zero denominator (no transcript abundance for either form) are either handled gracefully (reported as NaN or excluded) or flagged as low-confidence.
- PSI values remain stable when input quantification matrix is reordered by column (sample permutation test); row (event) order may change based on ioe/ioi specification.
- Comparison of PSI output against manual calculation for a small subset of events confirms correct aggregation of numerator and denominator transcripts.

## Limitations

- PSI calculation assumes that transcript quantification is accurate; errors or biases in upstream pseudo-alignment propagate into PSI estimates.
- Events with very low transcript abundance in both forms may produce noisy PSI estimates; filtering by minimum abundance is often necessary before downstream analysis.
- PSI is undefined (or reported as NaN) for events where the denominator sum is zero across all samples; such events must be excluded or flagged in differential splicing analysis.
- Complex splicing patterns not captured by the standard event types (SE, A5/A3, MX, RI, AF/AL) require use of the ioi (transcript event) format rather than ioe, which may be less intuitive to interpret.
- The ioe/ioi event definition is fixed at the time of generateEvents; novel or sample-specific transcripts absent from the annotation GTF are not represented in the event model.

## Evidence

- [other] Load transcript quantification data (TPM or counts) from Salmon/kallisto output.: "Load transcript quantification data (TPM or counts) from Salmon/kallisto output"
- [other] Load the SUPPA2 event definition file in ioe or ioi format specifying alternative splicing events and their constituent transcripts.: "Load the SUPPA2 event definition file in ioe or ioi format specifying alternative splicing events and their constituent transcripts"
- [other] Execute SUPPA2 psi subcommand to calculate PSI values by aggregating transcript abundances according to event structure.: "Execute SUPPA2 psi subcommand to calculate PSI values by aggregating transcript abundances according to event structure"
- [readme] The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [intro] Leveraging transcript quantification for fast computation of alternative splicing profiles: "Leveraging transcript quantification for fast computation of alternative splicing profiles"
