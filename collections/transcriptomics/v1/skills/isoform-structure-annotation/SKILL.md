---
name: isoform-structure-annotation
description: Use when when you have a GTF genome annotation and need to catalog all transcript isoforms and local alternative splicing event variants (exon skipping, intron retention, alternative splice sites, mutually exclusive exons, alternative first/last exons) before quantifying their inclusion levels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0102
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

# isoform-structure-annotation

## Summary

Reconstruct transcript isoform structures and local alternative splicing events from a genome annotation GTF file using SUPPA2's generateEvents subcommand, producing three indexed artifact files (ioi, ioe, gtf) that map transcripts to events and define splicing coordinates for downstream quantification.

## When to use

When you have a GTF genome annotation and need to catalog all transcript isoforms and local alternative splicing event variants (exon skipping, intron retention, alternative splice sites, mutually exclusive exons, alternative first/last exons) before quantifying their inclusion levels (PSI) across samples or conditions.

## When NOT to use

- Input is not a GTF file or lacks gene_id and transcript_id attributes in exon features.
- You only have raw RNA-seq reads and need de novo isoform discovery (use StringTie or Cufflinks first).
- You are working at the gene expression level only and do not need isoform or event-level resolution.

## Inputs

- GTF genome annotation file (exon features with gene_id and transcript_id tags required)
- Gene annotation source (e.g. Ensembl, GENCODE)

## Outputs

- ioe (index of events) file: event identifier, genomic coordinates, and transcript IDs for inclusion/exclusion forms
- ioi (index of isoforms) file: transcript ID, gene ID, and all transcript IDs in gene for denominator
- gtf file: local alternative splicing event coordinates with UCSC track header

## How to apply

Load the GTF file into SUPPA2's generateEvents subcommand, which parses exon-level features to extract transcript structures grouped by gene_id. The tool generates three indexed outputs: (1) ioe (index of events) file mapping each local AS event to transcripts contributing to the numerator (inclusion form) and denominator (both forms) of PSI calculation; (2) ioi (index of isoforms) file listing all transcripts per gene and their inclusion in each event; (3) gtf file with local event coordinates and UCSC track headers. Use the -b V option if allowing variable boundary tolerance (default 10 nt) to capture RT-PCR-like event definitions. The ioe and ioi outputs then serve as lookup tables for the psiPerEvent and psiPerIsoform quantification steps.

## Related tools

- **SUPPA2** (Generates transcript isoform structures and local alternative splicing event definitions from GTF annotation via generateEvents subcommand) — https://github.com/comprna/SUPPA

## Examples

```
python3 suppa.py generateEvents -i annotation.gtf -o suppa_events -f ioi -f ioe -f gtf
```

## Evaluation signals

- ioe file contains one row per event with unique genomic coordinates and non-empty transcript sets for both inclusion and exclusion forms.
- ioi file lists all transcripts in each gene and correctly maps transcript IDs to their parent gene.
- gtf output coordinates match the original GTF exon boundaries and correctly label event types (SE, A5, A3, MX, RI, AF, AL).
- All transcript IDs in ioe and ioi files are present in the input GTF.
- PSI calculation in downstream psiPerEvent step succeeds without missing transcript lookups.

## Limitations

- SUPPA reads only exon-level features; other GTF features (CDS, start_codon, stop_codon) are ignored, so non-coding transcript regions are not captured.
- Events at gene boundaries with variable splice sites may be redundant if -b V option is used; redundant events are reported on separate lines but have identical transcript contributions.
- Complex splicing variations spanning multiple exons cannot be encapsulated in simple local event coordinates; use ioi (transcript-level) annotations for such cases.
- Variable boundary option (-b V) may over-aggregate events if tolerance is set too high, potentially conflating distinct biological variants.

## Evidence

- [other] The SUPPA2 generateEvents subcommand produces three named output artifacts: ioi (input-output index), ioe (input-output events), and gtf for local events, which are generated from parsing a genome annotation GTF file.: "The three named output artifacts: ioi (input-output index), ioe (input-output events), and gtf for local events, which are generated from parsing a genome annotation GTF file."
- [readme] The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the event) and the denominator (both forms of the event) of the PSI calculation.: "The ioe file provides for each AS event in a gene, the transcripts that describe either form of the event. Specifically, it provides the transcripts that contribute to the numerator (one form of the"
- [readme] The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated.: "The ioi file provides for each transcript in a gene, the set of all transcripts from that gene from which the transcript relative abundance is calculated."
- [readme] The method reads transcript and gene information solely from the 'exon' lines in the GTF. It then generates the events and outputs an ioe file, which contains the for each event the transcripts that describe either form of the event.: "The method reads transcript and gene information solely from the 'exon' lines in the GTF. It then generates the events and outputs an ioe file"
- [readme] For that purpose 'gene_id' and 'transcript_id' tags are required in the attributes field (column 9). For local AS events, this command also generates a GTF file with the calculated events and with a track header ready to be uploaded into the UCSC browser for visualization: "gene_id and transcript_id tags are required in the attributes field. For local AS events, this command also generates a GTF file with the calculated events and with a track header ready to be"
- [readme] Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3) (generated together with the option SS), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL) (generated together with the option FL).: "Different local event types generated by SUPPA: Skipping Exon (SE), Alternative 5'/3' Splice Sites (A5/A3), Mutually Exclusive Exons (MX), Retained Intron (RI), Alternative First/Last Exons (AF/AL)"
