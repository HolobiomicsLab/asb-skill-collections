---
name: transcript-event-extraction
description: Use when you have a genome annotation GTF file and need to identify all transcript-level alternative splicing events (exon skipping, intron retention, alternative splice sites, mutually exclusive exons, alternative first/last exons) before quantifying their inclusion levels (PSI) across samples or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
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

# transcript-event-extraction

## Summary

Extract alternative splicing events and transcript isoforms from genome annotation GTF files to produce indexed event definitions (ioe, ioi) and local event coordinates (gtf). This step is essential for downstream PSI calculation and differential splicing analysis across multiple conditions.

## When to use

You have a genome annotation GTF file and need to identify all transcript-level alternative splicing events (exon skipping, intron retention, alternative splice sites, mutually exclusive exons, alternative first/last exons) before quantifying their inclusion levels (PSI) across samples or conditions.

## When NOT to use

- Input file is not GTF format or lacks required gene_id and transcript_id fields in column 9 attributes.
- You have only a single transcript per gene with no alternative isoforms (no splicing events to extract).
- You are working with pre-computed event files and need only to quantify PSI values—use psiPerEvent or psiPerIsoform directly instead.

## Inputs

- genome annotation GTF file (exon features with gene_id and transcript_id attributes)

## Outputs

- ioe file (index of events with transcript-to-event mappings)
- ioi file (index of isoforms with transcript event definitions)
- gtf file (local alternative splicing event coordinates, UCSC-ready)

## How to apply

Load the GTF annotation file into SUPPA2's generateEvents subcommand, which parses exon-level features and gene/transcript identifiers to extract transcript structures. The tool generates three distinct output files: (1) ioe (index of events) mapping each local alternative splicing event to the transcripts that define its inclusion and skipping forms, (2) ioi (index of isoforms) describing each transcript isoform in a gene as a 'transcript event' for isoform-centric analysis, and (3) gtf containing the genomic coordinates of all local events formatted for visualization. Optionally use the -b V flag to allow variable boundary tolerance (default 10 nt) when incorporating splice sites with minor coordinate variations, or specify event types (SE, A5, A3, MX, RI, AF, AL) to filter output. The ioe file is critical downstream—it provides the numerator (transcripts with the event form included) and denominator (all transcripts with either form) required for PSI calculation.

## Related tools

- **SUPPA2** (parses GTF annotation and generates ioe, ioi, and gtf artifacts for transcript and local alternative splicing event definitions) — https://github.com/comprna/SUPPA

## Examples

```
python3.4 suppa.py generateEvents -i annotation.gtf -o events_output -f ioe,ioi,gtf
```

## Evaluation signals

- ioe file contains all expected alternative splicing event types (SE, A5, A3, MX, RI, AF, AL) with non-empty inclusion and skipping transcript lists for each event.
- ioi file lists each transcript isoform with the complete set of gene-level transcripts for normalization.
- gtf output file is non-empty and contains valid genomic coordinates (start < end) with UCSC track header for browser upload.
- Number of events generated is consistent with known complexity of the input annotation (e.g., genes with multiple isoforms produce events; single-isoform genes do not).
- All transcript identifiers in ioe/ioi files match the input GTF transcript_id values.

## Limitations

- The tool reads only exon-level features; GTF files lacking exon lines or with malformed gene_id/transcript_id attributes will fail or produce incomplete output.
- Variable boundary tolerance (-b V) can produce redundant event lines with identical inclusion/skipping transcripts; downstream filtering may be needed.
- Complex splicing variations involving more than simple local events are better captured by ioi (transcript events) rather than local AS event types.
- GTF files from different sources (Ensembl, RefSeq, GENCODE) may produce different event counts due to annotation differences; reproducibility requires consistent input sources.

## Evidence

- [readme] SUPPA generates the alternative splicing events from an input annotation file (GTF format). The method reads transcript and gene information solely from the 'exon' lines in the GTF. It then generates the events and outputs an ioe file.: "SUPPA generates the alternative splicing events from an input annotation file (GTF format). The method reads transcript and gene information solely from the "exon" lines in the GTF. It then generates"
- [readme] The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated.: "The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated."
- [readme] For local AS events, this command also generates a GTF file with the calculated events and with a track header ready to be uploaded into the UCSC browser for visualization.: "For local AS events, this command also generates a GTF file with the calculated events and with a track header ready to be uploaded into the UCSC browser for visualization"
- [readme] The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [readme] Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL): "Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL)"
