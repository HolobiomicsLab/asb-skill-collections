---
name: ugt-sequence-curation-and-filtering
description: Use when curating and filtering UGT sequences in the metabolomics domain using Pfam domain scanning to retain functionally relevant single-domain candidates for downstream phylogenetic analysis.
when_to_use_negative:
- Input is already a curated multiple sequence alignment or a phylogenetic tree — filtering is only needed on raw Pfam scan outputs.
- You intend to characterize multidomain enzymes or study domain-fusion evolution — filtering out PF03033-containing sequences would discard the biology you want to study.
- The downstream goal is functional classification of all UGTs regardless of domain architecture — single-domain filtering may be overly restrictive.
edam_operation: http://edamontology.org/operation_0370
edam_topics:
- http://edamontology.org/topic_0078
- http://edamontology.org/topic_0080
tools:
- name: Pfam database
  role: Source of domain annotations (PF00201, PF03033) used to identify and filter candidate UGT sequences
- name: hmmscan
  role: Generates domain hit tables that are parsed and filtered by this skill to remove multi-domain sequences
- name: MAFFT
  role: 'Downstream tool: receives the filtered single-domain UGT sequences as input for multiple sequence alignment'
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_jeong_full/skills/ugt-sequence-curation-and-filtering/SKILL.md
    - outputs/audit_jeong_full/skills/ugt-sequence-curation-and-filtering/skill.md
    merged_at: '2026-05-25T07:33:56.382877+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/ugt-sequence-curation-and-filtering@sha256:912c230db7a2308608040c8a3e711215e030d62b72416c2468e255d904d59678
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# UGT sequence curation and filtering

## Summary

Filter and curate UDP-glycosyltransferase (UGT) sequences identified via Pfam domain scanning to retain functionally relevant single-domain candidates for downstream phylogenetic analysis. This skill removes multi-domain sequences that may conflate evolutionary relationships or functional assignments.

## When to use

After Pfam scanning of deduced amino acid sequences has identified candidate UGT sequences (PF00201 domain) across multiple fungal genomes, and you need to refine the candidate set before phylogenetic tree construction. Use this skill when the raw Pfam scan output contains sequences with multiple Pfam domains (e.g., both PF00201 and PF03033) that would confound downstream placement and functional interpretation.

## When NOT to use

- Input is already a curated multiple sequence alignment or a phylogenetic tree — filtering is only needed on raw Pfam scan outputs.
- You intend to characterize multidomain enzymes or study domain-fusion evolution — filtering out PF03033-containing sequences would discard the biology you want to study.
- The downstream goal is functional classification of all UGTs regardless of domain architecture — single-domain filtering may be overly restrictive.

## Inputs

- hmmscan output table (tab-separated or domain-hit table format) with columns: sequence_id, pfam_domain, e-value, domain_start, domain_end
- Deduced amino acid sequences in FASTA format (one file per species or concatenated across 19 species)

## Outputs

- Filtered FASTA file containing only single-domain UGT sequences (PF00201 present, PF03033 absent)
- Filtering report documenting: total candidate sequences, sequences removed (with reasons), final count, and species-wise breakdown

## How to apply

Parse the hmmscan output and filter out sequences containing both the PF00201 (UDP-glucoronosyl/glucosyl transferase domain) and PF03033 domains simultaneously, retaining only single-domain UGTs. The rationale is that sequences with multiple domains may represent multifunctional enzymes or domain-fusion artifacts that do not align clearly with experimentally characterized UGTs in phylogenetic space. Perform the filtering before multiple sequence alignment (MSA) to reduce noise in downstream tree construction. Document the number of sequences at each filtering stage (pre-filter total, sequences removed, final count) to track curation transparency.

## Related tools

- **Pfam database** (Source of domain annotations (PF00201, PF03033) used to identify and filter candidate UGT sequences)
- **hmmscan** (Generates domain hit tables that are parsed and filtered by this skill to remove multi-domain sequences)
- **MAFFT** (Downstream tool: receives the filtered single-domain UGT sequences as input for multiple sequence alignment)

## Evaluation signals

- Filtering preserves 100% of true single-domain UGTs (no false negatives): verify by spot-checking a subset of filtered sequences in the original hmmscan table.
- No sequences in the output file contain both PF00201 and PF03033 domains: parse output headers or re-scan filtered FASTA against Pfam to confirm.
- Filtering report shows reasonable species-wise counts (e.g., L. brumalis reduced from candidate pool to 8 putative UGTs) consistent with expected enzyme diversity.
- Filtered sequence count is lower than or equal to pre-filtered count, and e-value thresholds for retained domains meet Pfam default cutoffs (typically e < 0.01 for domain hit significance).
- Phylogenetic tree constructed from filtered alignment shows UGT66A1 clustering only with UGT62A1 (the expected biological signal) without spurious multi-domain taxa creating long branches or sister-group instability.

## Limitations

- Filtering is binary and does not accommodate partial domain overlap or domain boundaries close to sequence termini; borderline cases must be handled manually.
- E-value cutoff for Pfam domain detection relies on hmmscan default or user-specified thresholds — sequences with marginal e-values (e.g., 0.001–0.1) may be incorrectly included or excluded depending on stringency.
- Single-domain filtering assumes that PF03033-containing sequences are non-orthologous or represent a distinct functional class; if PF03033 co-occurs in experimentally characterized UGTs, this filter could remove true homologs.
- No mechanism to detect or handle frameshifts, sequencing errors, or incomplete ORF predictions in the deduced amino acid sequences; garbage-in-garbage-out applies to source Fasta quality.

## Evidence

- [other] Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only.: "Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only."
- [other] Scanning 19 wood-decaying fungal species against the Pfam database identified 138 total UGT sequences with the PF00201 domain, with eight putative UGTs found in L. brumalis.: "Scanning 19 wood-decaying fungal species against the Pfam database identified 138 total UGT sequences with the PF00201 domain, with eight putative UGTs found in L. brumalis."
- [other] Scan all sequences against Pfam database version 34 using hmmscan to identify those containing PF00201 (UDP-glucoronosyl/glucosyl transferase domain), yielding 138 candidate sequences.: "Scan all sequences against Pfam database version 34 using hmmscan to identify those containing PF00201 (UDP-glucoronosyl/glucosyl transferase domain), yielding 138 candidate sequences."
- [other] Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters.: "Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters."
