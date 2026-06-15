---
name: psi-calculation-from-isoform-abundance
description: Use when you have transcript-level abundance estimates (from Salmon, kallisto, or similar) and a set of defined alternative splicing events (in ioe or ioi format), and you need to compute event-level or isoform-level inclusion ratios (PSI) to quantify splicing patterns across multiple samples or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0654
  tools:
  - SUPPA2
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

# PSI calculation from isoform abundance

## Summary

Calculate Percent Spliced In (PSI) values for alternative splicing events by aggregating transcript abundance quantifications (TPM or counts) according to event-specific transcript definitions. This enables fast, genome-wide profiling of splicing inclusion levels across samples.

## When to use

You have transcript-level abundance estimates (from Salmon, kallisto, or similar) and a set of defined alternative splicing events (in ioe or ioi format), and you need to compute event-level or isoform-level inclusion ratios (PSI) to quantify splicing patterns across multiple samples or conditions.

## When NOT to use

- Transcript quantification data is not available or does not include isoform-level resolution (e.g., only gene-level counts).
- Event definitions are not pre-computed or the annotation GTF does not support the alternative splicing patterns you wish to study.
- Your goal is differential splicing analysis without intermediate PSI matrix generation — use diffSplice subcommand directly instead.

## Inputs

- Transcript quantification file (TSV/CSV with transcript IDs and TPM or count values per sample; output from Salmon or kallisto)
- Event definition file in ioe format (local alternative splicing events with transcript inclusions/exclusions)
- Event definition file in ioi format (transcript isoform events with constituent transcripts per gene)

## Outputs

- PSI matrix (tab-separated file with events/transcripts as rows, samples as columns, PSI values 0–1)
- Per-transcript isoform PSI file (when using psiPerIsoform subcommand)
- Per-event PSI file (when using psiPerEvent subcommand)

## How to apply

Load transcript quantification data (TPM or raw counts) and the corresponding event definition file (ioe format for local events or ioi format for transcript isoforms). Execute SUPPA's psi subcommand, which aggregates transcript abundances according to the event structure: the PSI for each event is computed as the sum of transcript abundances in the numerator (one splicing form) divided by the sum of abundances in the denominator (all forms of that event). The output is a matrix with events as rows and samples as columns, with PSI values ranging from 0 to 1 representing the fraction of transcripts that include the alternative region. Ensure transcript IDs in the quantification file match those in the event definition file to avoid missing data.

## Related tools

- **SUPPA2** (Computes PSI values by aggregating transcript abundances according to event structure; executes psiPerEvent and psiPerIsoform subcommands) — https://github.com/comprna/SUPPA

## Examples

```
python3 suppa.py psiPerEvent -e events.ioe -i transcript_quants.tsv -o psi_matrix
```

## Evaluation signals

- PSI matrix has no NaN or infinite values; all PSI entries are in the valid range [0, 1].
- Number of rows (events or transcripts) matches the number of events in the input ioe/ioi file.
- Number of columns equals the number of samples in the input quantification file.
- Transcript IDs in quantification file are successfully matched to those in the event definition (verify by checking for missing events or low coverage patterns).
- PSI values for simple events (e.g., exon skipping) are interpretable: PSI ≈ 1 when inclusion-form transcripts dominate abundance; PSI ≈ 0 when skipping-form transcripts dominate.

## Limitations

- Requires pre-existing event definitions (ioe or ioi files); cannot infer splicing events de novo from quantification data alone.
- PSI values are sensitive to transcript quantification accuracy; biases or errors in RNA-seq mapping and abundance estimation propagate directly to PSI.
- Complex overlapping or nested events may not be fully captured in the ioe format; transcript-level (ioi) events handle some but not all complex splicing variations.
- Low-abundance transcripts or events may produce unstable PSI estimates with high variance across replicates.
- SUPPA assumes transcript IDs are consistent between quantification and annotation files; mismatches result in missing or zero PSI values.

## Evidence

- [intro] Transcript quantification data leveraged for PSI computation: "Load transcript quantification data (TPM or counts) from Salmon/kallisto output. Load the SUPPA2 event definition file in ioe or ioi format specifying alternative splicing events and their"
- [readme] PSI aggregation logic and output format: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [intro] SUPPA2 speed and accuracy advantage: "SUPPA2: fast, accurate, and uncertainty-aware differential splicing analysis across multiple conditions"
- [readme] Transcript and event-level PSI computation: "SUPPA can work with local alternative splicing events or with transcripts "events" per gene. The local alternative splicing events are standard local splicing variations, whereas a transcript event"
- [readme] Subcommand execution for PSI calculation: "psiPerEvent: Quantifies event inclusion levels (PSIs) from multiple samples. psiPerIsoform: Quantifies isoform inclusion levels (PSIs) from multiple samples."
