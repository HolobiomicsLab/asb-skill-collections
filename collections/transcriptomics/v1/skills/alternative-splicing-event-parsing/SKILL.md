---
name: alternative-splicing-event-parsing
description: Use when when you have a GTF genome annotation and need to identify all local alternative splicing events (SE, RI, A5/A3, MX, AF/AL) or transcript-level isoform events for a given gene set, prior to quantifying PSI values across samples or performing differential splicing analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0438
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0203
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

# alternative-splicing-event-parsing

## Summary

Parse a genome annotation GTF file to extract and define alternative splicing events (exon skipping, intron retention, alternative splice sites, etc.) and generate indexed event definition files (ioe, ioi, gtf) for downstream PSI quantification and differential splicing analysis.

## When to use

When you have a GTF genome annotation and need to identify all local alternative splicing events (SE, RI, A5/A3, MX, AF/AL) or transcript-level isoform events for a given gene set, prior to quantifying PSI values across samples or performing differential splicing analysis.

## When NOT to use

- Your GTF file lacks exon-level feature annotations or is missing gene_id/transcript_id attributes; the subcommand requires these fields.
- You already have pre-computed event definition files (ioe/ioi) from a prior analysis and only need to proceed to PSI quantification.
- Your analysis goal is transcript abundance quantification only, without interest in local splicing event definitions or PSI calculation.

## Inputs

- GTF genome annotation file (with exon feature lines containing gene_id and transcript_id attributes)

## Outputs

- ioe file (input-output events: event ID, transcript inclusion set, transcript exclusion set)
- ioi file (input-output isoforms: transcript ID, gene isoforms)
- gtf file (local alternative splicing event coordinates, UCSC-compatible)

## How to apply

Load the GTF annotation file into SUPPA2's generateEvents subcommand, which parses exon lines to extract transcript and gene structures. SUPPA2 then identifies all splicing event types: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3), Mutually Exclusive Exons (MX), Retained Intron (RI), and Alternative First/Last Exons (AF/AL). For each event, the algorithm records the transcripts contributing to the numerator (inclusion form) and denominator (both forms) of the PSI calculation. Output three indexed artifacts: ioe file (mapping events to constituent transcripts for PSI calculation), ioi file (mapping transcripts to their parent gene isoforms), and gtf file containing coordinates of local alternative splicing events. Optionally, apply variable boundary tolerances (e.g., ±10 nt) to capture transcript isoforms with minor splice-site variations that better mimic RT-PCR detection.

## Related tools

- **SUPPA2** (Parses GTF annotation and generates event definition files (ioe, ioi, gtf) via generateEvents subcommand) — https://github.com/comprna/SUPPA

## Examples

```
python3.4 suppa.py generateEvents -i genome.gtf -o events_output -f ioe,ioi,gtf
```

## Evaluation signals

- All ioe entries contain non-empty sets of inclusion and exclusion transcripts for each event; no event should have identical numerator and denominator sets unless marked as redundant.
- Event coordinates (start, end positions) fall within exonic boundaries defined in the input GTF and match the nomenclature rules (e.g., RI events have external coordinates, SE events have internal exon coordinates).
- ioi file contains every transcript from the input GTF paired with at least one other isoform from the same gene (denominator set is non-empty).
- Output gtf file contains only local alternative splicing event types (SE, RI, A5, A3, MX, AF, AL) with valid strand and coordinate information, and is loadable into UCSC genome browser.
- When re-run with identical parameters on the same GTF, outputs are deterministic (same event definitions, same transcript assignments).

## Limitations

- SUPPA2 reads only exon feature lines from the GTF; other feature types (CDS, start_codon, stop_codon) are ignored, which may miss some transcript-level details.
- Complex splicing variations that do not fit standard local event types (SE, RI, A5/A3, MX, AF, AL) may not be captured; such cases require the transcript-level (ioi) approach.
- Variable boundary tolerance (e.g., ±10 nt) may cause redundant events with identical numerator/denominator transcript sets, which are still reported separately but should be filtered by the user if needed.
- GTF files with non-standard gene_id or transcript_id formats, or with missing attributes, will cause parsing failures.

## Evidence

- [readme] The method reads transcript and gene information solely from the "exon" lines in the GTF. It then generates the events and outputs an ioe file, which contains the for each event the transcripts that describe either form of the event.: "The method reads transcript and gene information solely from the "exon" lines in the GTF. It then generates the events and outputs an ioe file"
- [readme] The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [readme] Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3) (generated together with the option SS), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL) (generated together with the option FL).: "Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3) (generated together with the option SS), Mutually Exclusive Exons (MX), Retained Intron"
- [readme] An annotation file in GTF format is required ... The generateEvents operation uses the lines where the feature (column 3) is "exon". It then reads the different transcripts and genes. For that purpose "gene_id" and "transcript_id" tags are required in the attributes field (column 9).: "The generateEvents operation uses the lines where the feature (column 3) is "exon". It then reads the different transcripts and genes. For that purpose "gene_id" and "transcript_id" tags are required"
- [readme] In case the option for variable boundaries is used -b V ... an user input variability (detault: 10nt) is allowed in some of the boundaries ... allow incorporating other transcripts contributing to the event, and therefore mimicking more closely the PSI calculate from RT-PCR primers.: "In case the option for variable boundaries is used -b V ... an user input variability (detault: 10nt) is allowed in some of the boundaries ... allow incorporating other transcripts contributing to"
