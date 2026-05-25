---
name: fungal-genome-sequence-retrieval-and-processing
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to retrieve and preprocess deduced amino acid sequences from fungal genome databases, applying domain-based filtering and alignment for comparative genomics and phylogenetic analysis.
when_to_use_negative:
- Input sequences are already functionally characterized or experimentally validated; use this skill for hypothesis generation and target prioritization, not confirmation.
- Target domain is not well-represented in Pfam or you have custom domain definitions; consider ab initio domain discovery (InterProScan, HMMER3 custom models) instead.
- You require nucleotide-level sequence information (e.g., codon usage, splice sites); this skill operates on translated protein sequences only.
edam_operation: http://edamontology.org/operation_0346
edam_topics:
- http://edamontology.org/topic_0080
- http://edamontology.org/topic_0637
- http://edamontology.org/topic_3293
tools:
- name: JGI MycoCosm database
  role: primary source for download of deduced amino acid sequences from wood-decaying fungal genomes
- name: Pfam database
  role: domain annotation reference (v34); used with hmmscan to identify PF00201-containing sequences
- name: hmmscan
  role: profile-HMM scanning tool to query amino acid sequences against Pfam domains; identifies candidate sequences and returns E-values and bitscores
- name: MAFFT
  role: multiple sequence alignment of filtered protein candidates using default parameters to preserve structural alignment quality
- name: TrimAl
  role: automated trimming of multiple sequence alignment to remove low-information (high-gap) columns prior to phylogenetic analysis
- name: FastTree / RAxML
  role: tree-building software to construct maximum-likelihood phylogenetic tree from trimmed alignment for resolving placement of novel candidate sequences (e.g., UGT66A1)
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
    - outputs/audit_jeong_full/skills/fungal-genome-sequence-retrieval-and-processing/SKILL.md
    - outputs/audit_jeong_full/skills/fungal-genome-sequence-retrieval-and-processing/skill.md
    merged_at: '2026-05-25T07:33:56.376387+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/fungal-genome-sequence-retrieval-and-processing@sha256:90f44da076ae58dc8acb5b08e0f2a78ad4ea035c934bd47fef11fdd84c30e895
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# fungal-genome-sequence-retrieval-and-processing

## Summary

Retrieval and preprocessing of deduced amino acid sequences from fungal genome databases, followed by domain-based filtering and alignment to prepare protein sequences for comparative genomics and phylogenetic analysis. This skill enables systematic identification of gene families (e.g., UDP-glycosyltransferases) across multiple fungal species.

## When to use

You have identified a target protein domain (e.g., Pfam PF00201 for UDP-glycosyltransferases) and need to systematically mine it across multiple fungal species to compare sequence homology, abundance, and phylogenetic placement. Specifically: when you need to identify and filter candidate sequences from 5+ species, resolve their evolutionary relationships, or prioritize targets for experimental characterization based on taxonomic distribution.

## When NOT to use

- Input sequences are already functionally characterized or experimentally validated; use this skill for hypothesis generation and target prioritization, not confirmation.
- Target domain is not well-represented in Pfam or you have custom domain definitions; consider ab initio domain discovery (InterProScan, HMMER3 custom models) instead.
- You require nucleotide-level sequence information (e.g., codon usage, splice sites); this skill operates on translated protein sequences only.

## Inputs

- deduced amino acid sequences from 5+ fungal species (FASTA format)
- Pfam database version 34 or later
- target protein domain identifier (e.g., PF00201)

## Outputs

- filtered candidate protein sequences (FASTA, single-domain only)
- multiple sequence alignment (MAFFT MSA format or Nexus/Stockholm)
- trimmed alignment with low-information columns removed
- domain annotation metadata (Pfam accession, bitscore, E-value per sequence)

## How to apply

Download deduced amino acid sequences for all target fungal species from a curated database (e.g., JGI MycoCosm). Scan all sequences against a domain database (Pfam v34 or later) using profile-HMM tools (hmmscan) to identify sequences containing your target domain(s)—in this case, PF00201. Filter the resulting candidate set by applying secondary constraints: remove sequences containing multiple domains (e.g., both PF00201 and PF03033) if single-domain specificity is required, or apply custom thresholds (e.g., E-value cutoff, bitscore minimum). Perform multiple sequence alignment on the filtered set using MAFFT with default parameters, then trim low-information columns using TrimAl with automated gap-removal settings. The output is a curated, aligned protein sequence set ready for phylogenetic tree construction or motif analysis.

## Related tools

- **JGI MycoCosm database** (primary source for download of deduced amino acid sequences from wood-decaying fungal genomes)
- **Pfam database** (domain annotation reference (v34); used with hmmscan to identify PF00201-containing sequences)
- **hmmscan** (profile-HMM scanning tool to query amino acid sequences against Pfam domains; identifies candidate sequences and returns E-values and bitscores)
- **MAFFT** (multiple sequence alignment of filtered protein candidates using default parameters to preserve structural alignment quality)
- **TrimAl** (automated trimming of multiple sequence alignment to remove low-information (high-gap) columns prior to phylogenetic analysis)
- **FastTree / RAxML** (tree-building software to construct maximum-likelihood phylogenetic tree from trimmed alignment for resolving placement of novel candidate sequences (e.g., UGT66A1))

## Examples

```
hmmscan --domtblout ugt_results.txt Pfam-A.hmm fungal_sequences.fasta | grep 'PF00201' > candidates.txt; mafft --auto candidates.fasta > alignment.fasta; trimal -in alignment.fasta -out alignment_trimmed.fasta -automated1
```

## Evaluation signals

- Total number of candidate sequences identified matches expected domain prevalence in literature (138 UGTs across 19 species = ~7.3 per species; verify against published surveys).
- Post-filtering sequence count is consistent with domain-specificity criteria applied (e.g., single-domain PF00201 count should be ≤ pre-filter count).
- Multiple sequence alignment contains no gaps at conserved Pfam motif positions; alignment length is within expected range for the domain (e.g., UDP-glycosyltransferase ~50–120 aa core).
- Phylogenetic tree shows meaningful taxonomic clustering (e.g., fungal UGTs group separately from bacterial; closely related species cluster together) and novel sequences (e.g., UGT66A1) place near known orthologs (e.g., UGT62A1) with reasonable bootstrap support.
- Trimmed alignment removes >10% of alignment positions (low-information columns), indicating effective noise reduction without loss of core domain structure.

## Limitations

- Pfam database relies on previously characterized domains; novel or rapidly evolving domains may be missed, requiring supplementary ab initio prediction (InterProScan, HMMER custom models).
- Single-domain filtering (removal of multi-domain proteins) may exclude multifunctional candidates or regulatory isoforms; rationale for domain filter should be documented and tested empirically.
- Phylogenetic placement confidence depends on alignment depth and sequence divergence; species with <5 candidate sequences may have unstable phylogenetic positions; consider species-level sampling bias.
- JGI MycoCosm and Pfam database versions must be documented; version differences in genome annotation or domain definitions can affect reproducibility across analyses.
- Computational prediction (Pfam scanning, phylogenetic inference) does not confirm biochemical activity; experimental validation (heterologous expression, substrate assay) is required to assign function to novel candidates.

## Evidence

- [results] Download deduced amino acid sequences of 19 wood-decaying fungal species from JGI MycoCosm database: "Download deduced amino acid sequences of 19 wood-decaying fungal species from JGI MycoCosm database"
- [results] Scan all sequences against Pfam database version 34 using hmmscan to identify those containing PF00201: "Scan all sequences against Pfam database version 34 using hmmscan to identify those containing PF00201 (UDP-glucoronosyl/glucosyl transferase domain), yielding 138 candidate sequences"
- [results] Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only: "Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only"
- [results] Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters: "Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters"
- [results] Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns: "Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns"
- [results] Scanning of deduced amino acid sequences of the 19 species against the Pfam database found a total of 138 sequences containing a Pfam domain for UDP-glucoronosyl and UDP-glucosyl transferase: "Scanning of deduced amino acid sequences of the 19 species against the Pfam database found a total of 138 sequences containing a Pfam domain for UDP-glucoronosyl and UDP-glucosyl transferase"
- [results] Protein sequence–based phylogenetic analysis with the other experimentally characterized UGTs revealed that UGT66A1 clusters only with UGT62A1: "Protein sequence–based phylogenetic analysis with the other experimentally characterized UGTs revealed that UGT66A1 clusters only with UGT62A1"
