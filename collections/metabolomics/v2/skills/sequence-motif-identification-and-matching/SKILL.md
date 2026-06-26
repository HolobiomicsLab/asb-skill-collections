---
name: sequence-motif-identification-and-matching
description: Use when you have differentially expressed isoform or exon FASTA sequences
  and need to identify conserved regulatory or structural motifs as part of comprehensive
  functional annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0239
  edam_topics:
  - http://edamontology.org/topic_0157
  - http://edamontology.org/topic_0160
  tools:
  - CPAT
  - signalP
  - pfam
  - fimo
  - IsoformSwitchAnalyzer
  - Pfam
  license_tier: open
  provenance_tier: literature
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

# sequence-motif-identification-and-matching

## Summary

Scan biological sequences (DNA, RNA, or protein) against a database of known motifs to identify and annotate functional or structural features. This skill applies FIMO (Find Individual Motif Occurrences) to discover motif matches within differentially expressed isoform sequences as part of multi-level functional annotation.

## When to use

Apply this skill when you have differentially expressed isoform or exon FASTA sequences and need to identify conserved regulatory or structural motifs as part of comprehensive functional annotation. Use it after coding potential and signal peptide predictions have been completed, to add motif-based feature annotations to the unified functional annotation table.

## When NOT to use

- Input sequences lack clear functional context or are already fully annotated with motif information.
- Motif database is unavailable, outdated, or irrelevant to the biological system being studied.
- You are annotating sequences at the gene level rather than isoform/exon level, where motif variation is less likely to be informative.

## Inputs

- Differentially expressed isoform/exon FASTA sequences
- Known motif database (e.g., from MEME suite or curated collection)
- IsoformSwitchAnalyzer output

## Outputs

- FIMO motif match table (with E-values, positions, scores)
- Unified functional annotation table with motif annotations indexed by isoform/exon identifier
- Annotated sequence report with motif locations and confidence scores

## How to apply

Load differentially expressed isoform/exon FASTA sequences (e.g., from IsoformSwitchAnalyzer output). Run FIMO to scan sequences for known motifs from a curated motif database, which identifies positions and scores of motif matches. FIMO reports each match with E-value and position information. Merge FIMO results into the unified functional annotation table indexed by isoform/exon identifier, alongside CPAT coding scores, signalP signal peptide predictions, and Pfam domain hits. Include motif match coordinates and confidence scores in the summary report to enable downstream functional interpretation.

## Related tools

- **fimo** (Scans isoform/exon sequences for known motif occurrences; identifies match positions, scores, and E-values for functional feature assignment)
- **IsoformSwitchAnalyzer** (Source of differentially expressed isoform and exon FASTA sequences that serve as input to motif scanning)
- **CPAT** (Provides coding potential scores; motif matching complements coding annotation in the unified functional table)
- **signalP** (Provides signal peptide predictions; motif matching runs in parallel to build complete functional annotation)
- **Pfam** (Provides protein domain annotations; motif matches merge with domain hits into unified annotation table)

## Evaluation signals

- FIMO returns non-empty match table with E-values and genomic coordinates for at least a subset of input sequences.
- All motif matches are successfully merged into the unified functional annotation table with consistent isoform/exon indexing.
- Motif match coordinates are consistent with input sequence boundaries (no out-of-range positions).
- E-values and match scores are within expected ranges (e.g., E-value ≤ 0.05 for stringent threshold, ≤ 0.1 for exploratory).
- Annotated sequence report includes motif match summaries alongside CPAT, signalP, and Pfam results with no missing or misaligned records.

## Limitations

- FIMO performance depends on motif database quality and completeness; missing or poorly curated motifs will not be detected.
- False-positive motif matches may occur if E-value thresholds are too permissive; threshold selection requires balance between sensitivity and specificity.
- Motif matching identifies sequence similarity but does not confirm functional relevance; additional experimental validation may be needed.
- Overlapping motif matches in close proximity may obscure true functional sites if post-processing does not resolve conflicts.

## Evidence

- [methods] Run fimo to scan sequences for known motifs as part of functional feature identification: "Run fimo to scan sequences for known motifs as part of functional feature identification."
- [methods] Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon identifier: "Merge all annotation results (CPAT coding scores, signalP signal peptide predictions, Pfam domain hits, and motif matches) into a unified functional annotation table indexed by isoform/exon"
- [methods] Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output: "Load differentially expressed isoform/exon FASTA sequences from IsoformSwitchAnalyzer output."
- [other] The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP for signaling sequence identification: "The functional_annotation.nf subworkflow processes differentially expressed isoform sequences by applying CPAT for coding potential assessment, Pfam for protein domain homology detection, and signalP"
