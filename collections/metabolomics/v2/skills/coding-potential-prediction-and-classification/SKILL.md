---
name: coding-potential-prediction-and-classification
description: Use when you have differentially expressed isoform or exon FASTA sequences from transcript assembly or isoform-level analysis (e.g., IsoformSwitchAnalyzer output) and need to distinguish functional protein-coding transcripts from non-coding RNA.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3320
  - http://edamontology.org/topic_0654
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Pfam
  - Nextflow
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# coding-potential-prediction-and-classification

## Summary

Predicts and classifies RNA sequences as coding or non-coding using computational assessment of protein-coding capacity. This skill is essential for functional annotation of differentially expressed isoforms and long non-coding RNAs in multi-omics pipelines.

## When to use

Apply this skill when you have differentially expressed isoform or exon FASTA sequences from transcript assembly or isoform-level analysis (e.g., IsoformSwitchAnalyzer output) and need to distinguish functional protein-coding transcripts from non-coding RNA. Use it as a first step before downstream protein domain or signal peptide annotation.

## When NOT to use

- Input sequences are already pre-filtered to known protein-coding genes; redundant classification
- Analyzing short reads or fragments < 200 bp; CPAT reliability decreases on very short sequences
- Non-FASTA input format or sequences without proper isoform/exon identifiers

## Inputs

- Differentially expressed isoform FASTA sequences
- Differentially expressed exon FASTA sequences
- IsoformSwitchAnalyzer output FASTA file

## Outputs

- CPAT coding potential scores (probability/numeric)
- Binary coding/non-coding classification per isoform
- Unified functional annotation table with isoform identifiers and coding status

## How to apply

Load differentially expressed isoform/exon sequences in FASTA format from IsoformSwitchAnalyzer or similar transcript-level output. Run CPAT (Coding Potential Assessment Tool) on these sequences to generate coding potential scores and classify each sequence as coding or non-coding. CPAT uses a machine learning model trained on known coding and non-coding sequences to assign a probability score; sequences are typically classified using a threshold (exact threshold should be specified in pipeline configuration). Merge CPAT coding scores into a unified annotation table indexed by isoform/exon identifier for downstream integration with protein domain (Pfam) and signal peptide (signalP) predictions.

## Related tools

- **CPAT** (Predicts coding potential and classifies sequences as coding or non-coding using machine learning)
- **IsoformSwitchAnalyzer** (Upstream tool providing differentially expressed isoform/exon FASTA sequences as input to CPAT)
- **signalP** (Complementary tool for downstream annotation of signal peptides in sequences classified as coding by CPAT)
- **Pfam** (Complementary tool for protein domain homology detection in CPAT-classified coding sequences)
- **Nextflow** (Workflow orchestration framework for executing CPAT within multi-omics pipeline) — https://www.nextflow.io

## Evaluation signals

- CPAT output file contains valid numeric coding potential scores (0–1 range) for all input isoforms
- Binary classification (coding/non-coding) assigned to every isoform with no missing values
- Unified annotation table row count matches input FASTA sequence count; no sequences dropped
- Isoform identifiers correctly preserved from input FASTA headers through to final annotation table
- CPAT scoring is consistent with downstream Pfam and signalP annotations (e.g., coding isoforms with detected Pfam domains; non-coding sequences lack significant domain hits)

## Limitations

- CPAT accuracy depends on machine learning model training; performance may vary for evolutionarily distant or atypical transcript sequences
- Classification threshold is user-configurable but no universal consensus threshold; requires pipeline-specific tuning
- Short sequences (< 200 bp) have reduced CPAT reliability and may yield ambiguous scores near decision boundary
- CPAT does not account for isoform-specific features such as alternative splicing patterns that may affect coding potential assessment

## Evidence

- [other] The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment: "The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP"
- [other] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output and run CPAT to predict coding potential: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output. 2. Run CPAT to predict coding potential and classify sequences as coding or non-coding."
- [other] Merge all annotation results into a unified functional annotation table indexed by isoform/exon identifier: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [intro] Pipeline performs functional annotation of transcripts as part of RNAseq analysis: "2. Functional annotation of transcripts"
