---
name: splicing-matrix-normalization
description: Use when you have transcript-level quantification (TPM or counts from Salmon/kallisto) and need to quantify the inclusion level of specific alternative splicing events (exon skipping, intron retention, alternative splice sites, etc.) in a form suitable for differential splicing analysis across.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0203
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

# splicing-matrix-normalization

## Summary

Compute PSI (Percent Spliced In) values from transcript quantification data and alternative splicing event definitions to produce a normalized inclusion-level matrix. This skill transforms raw transcript abundances into event-level splicing profiles that are comparable across samples and conditions.

## When to use

Apply this skill when you have transcript-level quantification (TPM or counts from Salmon/kallisto) and need to quantify the inclusion level of specific alternative splicing events (exon skipping, intron retention, alternative splice sites, etc.) in a form suitable for differential splicing analysis across multiple samples or conditions.

## When NOT to use

- If your input is already a pre-computed PSI or splicing matrix—this skill quantifies PSI from raw transcript abundances, not from existing PSI data.
- If you only have exon-level read counts (not transcript-level quantification)—SUPPA2 requires transcript-level (isoform) abundances to calculate proper PSI values.
- If you have no event definition file and cannot generate one from a GTF annotation—SUPPA2 requires explicit mapping of which transcripts define each event's inclusion/exclusion forms.

## Inputs

- Transcript quantification matrix (TPM or counts) from Salmon or kallisto
- SUPPA2 event definition file in ioe format (local AS events) or ioi format (transcript isoforms)
- GTF annotation file (used to generate event definitions if not pre-computed)

## Outputs

- PSI matrix: tab-separated file with alternative splicing events/isoforms as rows and samples as columns
- PSI values normalized to [0, 1] scale representing inclusion levels

## How to apply

Load transcript quantification data (TPM or counts) from RNA-seq quantifiers (Salmon/kallisto output). Obtain or generate a SUPPA2 event definition file (ioe format for local AS events, ioi format for transcript events) that specifies which transcripts contribute to the numerator (inclusion form) and denominator (both forms) of each event's PSI calculation. Execute SUPPA2's psiPerEvent (for local events) or psiPerIsoform (for transcript isoforms) subcommand, which aggregates transcript abundances according to event structure: PSI = (sum of transcript abundances in inclusion form) / (sum of all transcripts in event). The output is a tab-separated PSI matrix with events as rows and samples as columns, with values ranging from 0 (skipped) to 1 (included). This matrix serves as input for downstream differential splicing analysis or clustering.

## Related tools

- **SUPPA2** (Computes PSI values from transcript quantification and event definitions; provides psiPerEvent and psiPerIsoform subcommands for matrix calculation) — https://github.com/comprna/SUPPA
- **Salmon** (Upstream tool: generates transcript-level quantification (TPM/counts) used as input to PSI calculation)
- **kallisto** (Upstream tool: generates transcript-level quantification (TPM/counts) used as input to PSI calculation)

## Examples

```
python3 suppa.py psiPerEvent -i transcripts.ioe -e samples.tpm -o psi_output
```

## Evaluation signals

- PSI matrix shape is correct: number of rows = number of events/isoforms in the event definition file; number of columns = number of samples in the quantification input.
- All PSI values fall within [0, 1] range; no NaN or infinite values unless handling low-abundance events (verify against expected sparsity).
- Row totals (summed PSI for mutually exclusive event forms) equal 1.0 (or close, allowing for rounding); this validates the numerator/denominator structure.
- PSI patterns are biologically interpretable: similar samples show correlated PSI profiles; known tissue-specific or condition-specific splicing events show expected variation patterns.
- No unexpected missing values; events with zero transcript abundance across all samples should be marked consistently (0, NA, or filtered) and documented.

## Limitations

- PSI calculation is sensitive to transcript quantification accuracy; errors or bias in upstream Salmon/kallisto output propagate directly into the PSI matrix.
- Low-abundance events (few supporting transcripts or low TPM) may produce unstable or noisy PSI values; thresholding by expression level is recommended but not performed by SUPPA2 itself.
- SUPPA2 does not adjust for sequencing depth or library composition in the quantification input; quantification normalization (e.g., TPM) must be applied before or during quantification.
- Event definition quality is critical: if the ioe/ioi file incorrectly specifies which transcripts belong to inclusion vs. exclusion forms, calculated PSI values will be meaningless.

## Evidence

- [other] SUPPA2 leverages transcript quantification data for fast computation of alternative splicing profiles by calculating PSI values for transcript events and local alternative splicing events.: "SUPPA2 leverages transcript quantification data for fast computation of alternative splicing profiles by calculating PSI values"
- [other] Load transcript quantification data (TPM or counts) from Salmon/kallisto output and load the SUPPA2 event definition file in ioe or ioi format specifying alternative splicing events and their constituent transcripts.: "Load transcript quantification data (TPM or counts) from Salmon/kallisto output. Load the SUPPA2 event definition file in ioe or ioi format"
- [other] Execute SUPPA2 psi subcommand to calculate PSI values by aggregating transcript abundances according to event structure.: "Execute SUPPA2 psi subcommand to calculate PSI values by aggregating transcript abundances according to event structure"
- [readme] The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [readme] SUPPA generates the AS events or transcript events from an input annotation file (GTF format) and outputs an event file: .ioe format for local AS events, and .ioi format for transcripts.: "SUPPA generates the AS events or transcript events from an input annotation file (GTF format). It then generates the events and outputs an event file: .ioe format for local AS events, and .ioi format"
- [readme] SUPPA works with a command/subcommand structure where the subcommand can be psiPerEvent or psiPerIsoform to quantify event or isoform inclusion levels (PSIs) from multiple samples.: "psiPerEvent: Quantifies event inclusion levels (PSIs) from multiple samples. psiPerIsoform: Quantifies isoform inclusion levels (PSIs) from multiple samples."
