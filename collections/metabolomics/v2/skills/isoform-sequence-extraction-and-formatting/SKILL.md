---
name: isoform-sequence-extraction-and-formatting
description: Use when after completing differential isoform expression analysis using IsoformSwitchAnalyzer or equivalent isoform quantification, when you have identified sets of differentially expressed isoforms and need to perform functional characterization through sequence-based homology and structural.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0564
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0099
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Nextflow DSL2
  - nf-core/modules
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Functional annotation | CPAT, signalP, pfam
- Find motif | fimo
- Isoforms | Genome wide isoform analysis | IsoformSwitchAnalyzer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
---

# isoform-sequence-extraction-and-formatting

## Summary

Extract and format differentially expressed isoform sequences from RNA-seq assembly outputs into FASTA files for downstream functional annotation. This skill enables preparation of isoform/exon sequences in standardized format required by domain prediction, coding potential, and signal peptide detection tools.

## When to use

After completing differential isoform expression analysis using IsoformSwitchAnalyzer or equivalent isoform quantification, when you have identified sets of differentially expressed isoforms and need to perform functional characterization through sequence-based homology and structural prediction tools (CPAT, Pfam, signalP).

## When NOT to use

- Input sequences are already pre-formatted in FASTA and validated—skip directly to functional annotation tool invocation.
- Analysis focuses only on gene-level differential expression without isoform-level switching or alternative splicing characterization.
- Sequences have already been processed through the full annotation pipeline (CPAT, Pfam, signalP)—use only merged annotation table instead.

## Inputs

- Differentially expressed isoform identifiers (from IsoformSwitchAnalyzer or equivalent)
- Isoform/exon nucleotide or protein sequences (FASTA or tabular format)
- IsoformSwitchAnalyzer output table or equivalent isoform quantification results

## Outputs

- Isoform FASTA file with indexed headers (isoform_id | exon_id format)
- Exon FASTA file with indexed headers (optional, if exon-level annotation required)
- FASTA validation report (sequence count, length distribution)

## How to apply

Load differentially expressed isoform or exon identifiers and their corresponding nucleotide/protein sequences from IsoformSwitchAnalyzer output tables. Format sequences into FASTA format with properly indexed headers linking each sequence to its isoform/exon identifier for traceability. Validate FASTA syntax and sequence composition (nucleotides or amino acids as appropriate) before passing to downstream annotation tools. The standardized FASTA indexing ensures that annotation results (CPAT coding scores, signalP predictions, Pfam domain hits) can be merged back into a unified functional annotation table indexed by the same isoform/exon identifier.

## Related tools

- **IsoformSwitchAnalyzer** (Source tool for extracting differentially expressed isoform sequences and metadata)
- **Nextflow DSL2** (Workflow orchestration for parallelizing FASTA extraction and validation across isoform sets) — https://www.nextflow.io/docs/latest/dsl2.html
- **nf-core/modules** (Repository containing standardized Nextflow modules for sequence processing tasks) — https://github.com/nf-core/modules

## Evaluation signals

- All differentially expressed isoforms from input table appear exactly once in output FASTA (completeness check).
- FASTA headers conform to expected format (isoform_id | exon_id) with no whitespace corruption and can be parsed by downstream tools.
- Sequence composition is valid (no ambiguous characters outside of standard IUPAC nucleotide/amino acid codes for the molecule type).
- FASTA file passes validation by a standard parser (e.g., BioPython SeqIO, seqtk) without warnings or errors.
- Merged annotation table after downstream tools (CPAT, Pfam, signalP) contains results for all sequences in the FASTA file, indexed by isoform_id with no missing mappings.

## Limitations

- Sequence extraction accuracy depends on correct IsoformSwitchAnalyzer output format and absence of malformed or truncated entries in source data.
- FASTA formatting does not validate biological correctness (e.g., start/stop codons in coding sequences); annotation tools will flag issues downstream.
- Large isoform sets (>100k sequences) may require staged processing or memory-efficient streaming to avoid resource exhaustion during FASTA generation.
- If isoform identifiers contain special characters (whitespace, pipes, carriage returns), FASTA headers may be corrupted and cause parsing failures in downstream tools.

## Evidence

- [methods] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output.: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output."
- [methods] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon identifier.: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [intro] Pipeline performs RNAseq analysis on the level of : mRNAs, miRNAs, isoforms including lncRNAs: "Pipeline performs RNAseq analysis on the level of : mRNAs, miRNAs, isoforms including lncRNAs"
- [readme] The Nextflow DSL2 implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies.: "The Nextflow DSL2 implementation of this pipeline uses one container per process which makes it much easier to maintain and update software dependencies."
