---
name: protein-sequence-domain-scanning
description: Use when metabolomics involves systematic scanning of deduced protein sequences against curated domain databases using techniques like LC-MS and GC-MS to identify and quantify conserved functional domains across a species set.
when_to_use_negative:
- Input sequences are already functionally annotated or experimentally characterized; domain scanning is redundant.
- Your target protein family has no curated domain signature in your chosen database; use sequence homology search instead.
- You need to resolve isoform-specific or splice-variant differences; domain scanning operates on deduced consensus sequences and will not distinguish them.
edam_operation: http://edamontology.org/operation_0361
edam_topics:
- http://edamontology.org/topic_0078
- http://edamontology.org/topic_0080
- http://edamontology.org/topic_3393
tools:
- name: hmmscan
  role: HMM-based domain scanner; queries sequences against Pfam using profile hidden Markov models to assign domains and compute E-values
- name: Pfam
  role: Curated database of protein family domains; provides versioned domain profiles (e.g., v34) and functional annotation
- name: JGI MycoCosm
  role: Genome portal for fungal sequences; source of deduced amino acid sequences for wood-decaying fungi and other species
- name: MAFFT
  role: Multiple sequence alignment of domain-filtered candidate sequences to prepare for phylogenetic analysis
- name: TrimAl
  role: Alignment trimming and gap removal to remove low-information columns before tree construction
- name: FastTree / RAxML
  role: Phylogenetic tree construction from trimmed alignments to resolve placement of candidates among characterized references
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
    - outputs/audit_jeong_full/skills/protein-sequence-domain-scanning/SKILL.md
    - outputs/audit_jeong_full/skills/protein-sequence-domain-scanning/skill.md
    merged_at: '2026-05-25T07:04:57.525128+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/protein-sequence-domain-scanning@sha256:fc1aa2db66537753c9bd1087c37416ded80364264b684713e886e19183c67e85
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# protein-sequence-domain-scanning

## Summary

Systematic scanning of deduced protein sequences against curated domain databases (e.g., Pfam) to identify and quantify conserved functional domains across a species set, enabling candidate prioritization and phylogenetic placement. Essential for high-throughput annotation of enzyme families when experimental characterization is infeasible.

## When to use

You have deduced amino acid sequences from multiple fungal or microbial genomes and need to identify which sequences encode a specific conserved domain (e.g., UDP-glycosyltransferase, PF00201) to narrow a large set to functionally relevant candidates before phylogenetic or transcriptomic analysis. Use this when domain presence/absence is your primary filter for candidate prioritization.

## When NOT to use

- Input sequences are already functionally annotated or experimentally characterized; domain scanning is redundant.
- Your target protein family has no curated domain signature in your chosen database; use sequence homology search instead.
- You need to resolve isoform-specific or splice-variant differences; domain scanning operates on deduced consensus sequences and will not distinguish them.

## Inputs

- Deduced amino acid sequences (FASTA format) from multiple fungal or microbial genomes
- Versioned Pfam database or equivalent (e.g., Pfam v34)
- Domain identifier(s) of interest (e.g., 'PF00201' for UDP-glycosyltransferase)

## Outputs

- Candidate protein sequences containing the target domain
- Domain annotation table (sequence ID, domain name, boundaries, E-value)
- Per-species count of domain-containing sequences
- Filtered MSA-ready sequence set for downstream phylogenetic or structural analysis

## How to apply

Download deduced amino acid sequences from a genome database (e.g., JGI MycoCosm) for your species of interest. Run hmmscan (or comparable HMM-based scanner) against a versioned domain database (e.g., Pfam 34) to identify all sequences containing your target domain (e.g., PF00201). Apply domain-based filters (e.g., retain only single-domain hits by excluding sequences that also contain PF03033) to enrich for likely monofunctional candidates. Record the domain boundaries and E-values for each hit. Tabulate the count and distribution of domain-containing sequences per species to assess prevalence and guide downstream functional prioritization (e.g., via transcriptomics or phylogenetic clustering).

## Related tools

- **hmmscan** (HMM-based domain scanner; queries sequences against Pfam using profile hidden Markov models to assign domains and compute E-values)
- **Pfam** (Curated database of protein family domains; provides versioned domain profiles (e.g., v34) and functional annotation)
- **JGI MycoCosm** (Genome portal for fungal sequences; source of deduced amino acid sequences for wood-decaying fungi and other species)
- **MAFFT** (Multiple sequence alignment of domain-filtered candidate sequences to prepare for phylogenetic analysis)
- **TrimAl** (Alignment trimming and gap removal to remove low-information columns before tree construction)
- **FastTree / RAxML** (Phylogenetic tree construction from trimmed alignments to resolve placement of candidates among characterized references)

## Examples

```
hmmscan --domtblout results.domtbl Pfam-A.hmm fungal_sequences.fasta | grep 'PF00201' > ugt_candidates.txt
```

## Evaluation signals

- Total candidate count and per-species distribution matches expected prevalence of the domain in literature (e.g., 138 UGT sequences across 19 wood-decaying fungi is reasonable).
- Domain E-values fall below your chosen threshold (typically < 0.01 or database default) indicating confident matches.
- Filtered single-domain sequences represent coherent phylogenetic groups in downstream tree analysis (e.g., new UGT66A1 clusters only with close homolog UGT62A1).
- No false positives detected by spot-checking a few high-E-value hits against literature or reverse searches.
- Downstream transcriptional profiling or kinetic analysis correlates with domain predictions (e.g., LbUGT3 expression increases when baicalin is present, consistent with it being a UGT).

## Limitations

- Domain scanning does not confirm enzymatic activity; homozygous domain presence may be necessary but not sufficient for substrate specificity or catalytic efficiency.
- Domains may be incomplete, fragmented, or co-occur with additional domains (requiring explicit filtering, e.g., excluding PF00201+PF03033 double-domain hits).
- Candidate prioritization based on domain presence alone cannot distinguish subcellular localization (transmembrane vs. intracellular) or expression level; supplementary experiments (DeepTMHMM, transcriptomics) are needed.
- Large gene families will still require manual or computational prioritization (e.g., RNAseq fold-change) to identify the most functionally relevant member.
- Pfam databases are versioned and may change between studies, affecting reproducibility and cross-study comparability.

## Evidence

- [results] Scanning 19 wood-decaying fungal species against the Pfam database identified 138 total UGT sequences with the PF00201 domain, with eight putative UGTs found in L. brumalis: "Scanning of deduced amino acid sequences of the 19 species against the Pfam database found a total of 138 sequences containing a Pfam domain for UDP-glucoronosyl and UDP-glucosyl transferase"
- [methods] Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only: "Filter out sequences containing both PF00201 and PF03033 domains to retain single-domain UGTs only"
- [methods] Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters: "Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters"
- [results] phylogenetic analysis revealed that UGT66A1 clusters only with UGT62A1, a fungal UGT from Hericium erinaceum: "Protein sequence–based phylogenetic analysis with the other experimentally characterized UGTs revealed that UGT66A1 clusters only with UGT62A1"
- [methods] Deduced amino acid sequences of 19 wood-decaying fungi were downloaded from the JGI MycoCosm database and scanned using Pfam version 34: "Deduced amino acid sequences of 19 wood-decaying fungi were downloaded from the JGI MycoCosm database"
