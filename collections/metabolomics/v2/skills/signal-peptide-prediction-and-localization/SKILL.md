---
name: signal-peptide-prediction-and-localization
description: Use when you have differentially expressed isoform or exon FASTA sequences
  from transcript assembly (e.g., IsoformSwitchAnalyzer output) and need to identify
  which predicted coding isoforms encode signal peptides for secretion or membrane
  targeting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0418
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3407
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Pfam
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-peptide-prediction-and-localization

## Summary

Signal peptide prediction identifies and annotates N-terminal signaling sequences in predicted coding isoforms, enabling functional characterization of secreted and membrane-targeted proteins. This skill applies signalP to differentially expressed isoform sequences to classify subcellular localization and secretion pathways.

## When to use

Apply this skill when you have differentially expressed isoform or exon FASTA sequences from transcript assembly (e.g., IsoformSwitchAnalyzer output) and need to identify which predicted coding isoforms encode signal peptides for secretion or membrane targeting. Use when functional annotation of isoforms includes characterization of signal transduction or protein localization.

## When NOT to use

- Input sequences are already mature proteins or have signal peptides experimentally removed
- Analysis is limited to non-coding isoforms (lncRNAs); signalP requires translated open reading frames
- No interest in protein localization or secretion pathway; focus is only on transcript expression changes

## Inputs

- Differentially expressed isoform/exon FASTA sequences (from IsoformSwitchAnalyzer output)
- Prior CPAT coding potential predictions (to filter for coding isoforms)

## Outputs

- signalP signal peptide predictions per isoform (probability scores, cleavage site position)
- Annotated isoform table with signal peptide presence/absence and predicted localization
- Unified functional annotation table merging signalP, CPAT, Pfam, and motif results indexed by isoform identifier

## How to apply

Load differentially expressed isoform FASTA sequences that have been classified as coding by prior CPAT analysis. Run signalP to scan the N-terminal region of each predicted protein sequence for the presence of signal peptide cleavage sites and export signal peptide predictions (e.g., probability scores, cleavage position predictions, localization annotations). Merge signalP results with other functional annotations (CPAT coding scores, Pfam domain hits, motif matches) indexed by isoform identifier. Rationale: signal peptides are N-terminal targeting sequences cleaved post-translationally; their presence indicates proteins destined for secretion, ER translocation, or specific organellar pathways, which is critical for interpreting isoform-level functional switching events.

## Related tools

- **signalP** (Identifies and annotates signal peptide sequences at the N-terminus of predicted coding isoforms)
- **CPAT** (Predicts coding potential to classify isoform sequences as coding or non-coding prior to signalP analysis)
- **IsoformSwitchAnalyzer** (Generates differentially expressed isoform/exon FASTA sequences used as input to signalP)
- **Pfam** (Assigns protein domain annotations to merge with signalP results for unified functional annotation)
- **fimo** (Scans sequences for known motifs as part of functional feature identification alongside signalP)

## Evaluation signals

- signalP output contains probability scores and predicted cleavage site positions for ≥1 isoform
- Signal peptide predictions are present only for CPAT-classified coding isoforms, not non-coding sequences
- Merged annotation table successfully indexes signalP results by isoform/exon identifier with no missing or duplicated entries
- Summary statistics document the count and proportion of isoforms with detected signal peptides
- Predicted localization annotations (e.g., secreted, membrane-bound, ER-targeted) are consistent with isoform functional roles where known

## Limitations

- signalP accuracy depends on sequence quality and correctness of the upstream ORF prediction; errors in CPAT coding classification propagate
- Signal peptide prediction is most reliable for eukaryotic proteins; performance on non-model organisms or highly divergent isoforms may be reduced
- Cleavage site prediction may be ambiguous for short or atypical signal peptides, requiring manual inspection for critical isoforms
- The workflow assumes isoforms have been properly assembled and aligned; chimeric or misassembled transcripts may yield spurious signal peptide predictions

## Evidence

- [methods] Run signalP to identify and annotate signal peptide sequences at the N-terminus: "Run signalP to identify and annotate signal peptide sequences at the N-terminus."
- [methods] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [other] The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP for signaling sequence identification.: "The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP"
- [methods] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output.: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output."
