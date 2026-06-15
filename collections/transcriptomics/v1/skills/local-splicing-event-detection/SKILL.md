---
name: local-splicing-event-detection
description: Use when you have a GTF annotation file and need to systematically extract all local alternative splicing event coordinates (not transcript isoforms) for downstream PSI calculation or when you require a searchable index mapping events to contributing transcripts for inclusion and skipping forms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3320
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

# local-splicing-event-detection

## Summary

Detect and catalog local alternative splicing (AS) events from genome annotation GTF files, generating indexed event definitions and isoform mappings that serve as inputs for PSI quantification and differential splicing analysis. This skill identifies standard splicing variations (exon skipping, intron retention, alternative splice sites, mutually exclusive exons, and alternative first/last exons) at single-event resolution.

## When to use

Apply this skill when you have a GTF annotation file and need to systematically extract all local alternative splicing event coordinates (not transcript isoforms) for downstream PSI calculation or when you require a searchable index mapping events to contributing transcripts for inclusion and skipping forms.

## When NOT to use

- Input annotation is not in GTF format or lacks mandatory gene_id and transcript_id attributes in exon lines.
- Your goal is transcript-level quantification only without per-event PSI calculation; use psiPerIsoform subcommand instead.
- You need to detect novel splice junctions or non-canonical splicing from RNA-seq reads rather than from existing annotation; this skill requires pre-annotated exon structures.

## Inputs

- GTF annotation file (exon feature lines with gene_id and transcript_id attributes)

## Outputs

- ioe file (input-output events: event ID, transcripts in inclusion form, transcripts in exclusion form)
- ioi file (input-output isoforms: transcript-centric event definitions)
- gtf file (local AS event coordinates in UCSC track format)

## How to apply

Load the GTF annotation file into SUPPA2's generateEvents subcommand, which parses exon-level features and gene_id/transcript_id attributes to extract transcript structures. The tool identifies all local AS event types (SE, A5/A3, MX, RI, AF/AL) by examining exon boundaries and splice junctions within each gene. For each event detected, SUPPA2 generates three indexed outputs: (1) ioe (input-output events) file listing transcripts contributing to the numerator—the form for which PSI is calculated—and denominator of each event; (2) ioi (input-output isoforms) file for transcript-level events; and (3) gtf output containing event coordinates in UCSC browser–compatible format. Use variable boundary options (–b V) with default 10 nt tolerance if incorporating isoforms with slightly divergent exon boundaries, mimicking RT-PCR primer specificity.

## Related tools

- **SUPPA2** (Parses GTF exon features, detects local AS event types (SE, A5/A3, MX, RI, AF/AL), and generates indexed ioe/ioi/gtf outputs) — https://github.com/comprna/SUPPA

## Examples

```
python3.4 suppa.py generateEvents -i annotation.gtf -o output_prefix -f ioe
```

## Evaluation signals

- ioe file contains one line per detected event with non-empty transcript lists for both inclusion and exclusion forms; no event should have identical transcripts in both forms.
- All five AS event types (SE, A5/A3, MX, RI, AF/AL) are represented in output if present in annotation; check event nomenclature matches documented coordinate scheme (forward/reverse strand conventions).
- gtf output file is valid GTF format with track header and can be uploaded to UCSC browser for visualization.
- Event coordinates in ioe and gtf outputs are consistent and reflect correct exon boundary positions from input GTF.
- ioi file (if generated) includes all transcripts per gene with complete set of gene-level transcripts for relative abundance calculation.

## Limitations

- Event detection depends entirely on exon-level annotation quality; missing or incorrectly annotated exons will produce incomplete or spurious events.
- Variable boundary tolerance (–b V) may generate redundant events with identical transcript sets but different reported coordinates; these are still reported as separate lines.
- Complex splicing patterns that cannot be encapsulated in standard local event definitions require use of transcript-event (ioi) approach rather than local event (ioe) approach.
- The tool reads only 'exon' feature lines; other GTF feature types (start_codon, stop_codon, etc.) are ignored.

## Evidence

- [readme] The method reads transcript and gene information solely from the 'exon' lines in the GTF.: "The method reads transcript and gene information solely from the "exon" lines in the GTF."
- [readme] It then generates the events and outputs an ioe file, which contains the for each event the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "It then generates the events and outputs an ioe file, which contains the for each event the transcripts that describe either form of the event. Specifically, it provides the transcripts that"
- [readme] Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL): "Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3) (generated together with the option SS), Mutually Exclusive Exons (MX), Retained Intron"
- [readme] The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated.: "The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated."
- [readme] In case the option for variable boundaries is used –b V, an user input variability (default: 10nt) is allowed in some of the boundaries: "In case the option for variable boundaries is used **-b V** (see below), an user input variability (detault: 10nt) is allowed in some of the boundaries"
