---
name: multiple-sequence-alignment-optimization
description: Use when optimizing multiple sequence alignment in metabolomics using LC-MS or GC-MS techniques by trimming low-information columns and removing gap-rich regions to enhance phylogenetic signal before tree construction.
when_to_use_negative:
- Input alignment is already curated, published, or hand-trimmed for a specific analysis—re-trimming may discard biologically informative positions.
- Sequences are too divergent or too short (< 50 amino acids) to tolerate aggressive gap removal without losing critical information.
- Analysis goal is to preserve gap patterns themselves (e.g., indel-based phylogenetics or structural alignment annotation).
edam_operation: http://edamontology.org/operation_0564
edam_topics:
- http://edamontology.org/topic_3293
- http://edamontology.org/topic_0084
tools:
- name: MAFFT
  role: Initial multiple sequence alignment of candidate domain-containing protein sequences using default parameters to generate unambiguous MSA
- name: TrimAl
  role: Automated gap-removal and column trimming to eliminate low-information sites and gap-rich regions that introduce phylogenetic noise
- name: FastTree
  role: Maximum-likelihood phylogenetic tree construction from the trimmed alignment to infer sequence placement and relationships
- name: RAxML
  role: Alternative maximum-likelihood tree-building engine from trimmed alignment when more rigorous branch support is required
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/multiple-sequence-alignment-optimization@sha256:fbba11419e22a121b51dfe90df01dfbdd17abc2db0b9190719fa3b2771c0f74b
---

# multiple-sequence-alignment-optimization

## Summary

Optimize a multiple sequence alignment by trimming low-information columns and removing gap-rich regions to improve phylogenetic signal before tree construction. This skill is essential when building phylogenetic trees from domain-filtered protein sequences to ensure that only informative sites contribute to evolutionary inference.

## When to use

After performing multiple sequence alignment (MSA) of filtered protein sequences (e.g., UGTs containing a single Pfam domain) and before constructing a maximum-likelihood phylogenetic tree. Use this skill when the alignment contains gap-rich regions or low-complexity columns that would introduce noise into tree topology inference, particularly when resolving placement of newly characterized sequences (like UGT66A1) among a large reference set (138+ sequences).

## When NOT to use

- Input alignment is already curated, published, or hand-trimmed for a specific analysis—re-trimming may discard biologically informative positions.
- Sequences are too divergent or too short (< 50 amino acids) to tolerate aggressive gap removal without losing critical information.
- Analysis goal is to preserve gap patterns themselves (e.g., indel-based phylogenetics or structural alignment annotation).

## Inputs

- Multiple sequence alignment in FASTA or aligned format (output of MAFFT)
- 138+ aligned protein sequences (e.g., UGT sequences containing PF00201 Pfam domain)

## Outputs

- Trimmed, gap-optimized multiple sequence alignment in FASTA or aligned format
- Column quality/masking information indicating which sites were retained
- Alignment statistics (number of sites before/after trimming, gaps removed)

## How to apply

Perform multiple sequence alignment of candidate sequences using MAFFT with default parameters to generate an unambiguous alignment. Then apply automated gap-removal using TrimAl with its automated settings to identify and remove columns with excessive gaps or low sequence information. The rationale is that gap-rich and low-complexity columns introduce phylogenetic noise; removing them preserves signal for resolving deep and shallow branches. The trimmed alignment is then used as input to maximum-likelihood tree construction (e.g., FastTree or RAxML) to infer the evolutionary relationships and placement of query sequences (e.g., determining that UGT66A1 clusters with UGT62A1 from H. erinaceum).

## Related tools

- **MAFFT** (Initial multiple sequence alignment of candidate domain-containing protein sequences using default parameters to generate unambiguous MSA)
- **TrimAl** (Automated gap-removal and column trimming to eliminate low-information sites and gap-rich regions that introduce phylogenetic noise)
- **FastTree** (Maximum-likelihood phylogenetic tree construction from the trimmed alignment to infer sequence placement and relationships)
- **RAxML** (Alternative maximum-likelihood tree-building engine from trimmed alignment when more rigorous branch support is required)

## Examples

```
mafft --auto ugt_candidates.fasta > ugt_aligned.fasta && trimal -in ugt_aligned.fasta -out ugt_trimmed.fasta -automated1 && raxmlHPC -T 4 -f a -x 12345 -p 12345 -m PROTGAMMAAUTO -N 100 -s ugt_trimmed.fasta -n ugt_tree
```

## Evaluation signals

- Trimmed alignment has fewer gaps and low-complexity regions than input; number of aligned sites reduced by 10–30% (typical for automated trimming)
- Phylogenetic tree from trimmed alignment shows improved branch resolution and clearer clustering of known functional orthologs (e.g., UGT66A1 with UGT62A1) compared to untrimmed MSA
- No unexpected loss of critical diagnostic positions; key Pfam domain features (e.g., active-site residues) remain present in trimmed alignment
- Tree topology is stable across different tree-building algorithms (FastTree vs. RAxML) when both are applied to the same trimmed MSA

## Limitations

- Automated gap-removal can be aggressive and may discard weak but real phylogenetic signal in sparse or highly variable regions; manual review recommended for publication-quality trees.
- TrimAl's automated settings assume sufficient sequence diversity; performance may degrade with very similar sequences or small alignment size (< 10 sequences).
- Trimming parameters are fixed; no adaptive tuning to sequence family-specific characteristics (e.g., transmembrane vs. soluble proteins may have different gap distributions).
- Does not address sequence compositional biases or heterogeneous evolutionary rates that can distort downstream tree inference.

## Evidence

- [methods] Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters.: "Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters."
- [methods] Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns.: "Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns."
- [methods] Construct a maximum-likelihood phylogenetic tree from the trimmed alignment using standard tree-building software (FastTree or RAxML) to resolve placement of UGT66A1 among the 138 UGTs.: "Construct a maximum-likelihood phylogenetic tree from the trimmed alignment using standard tree-building software (FastTree or RAxML) to resolve placement of UGT66A1 among the 138 UGTs."
- [results] phylogenetic analysis revealed that UGT66A1 clusters only with UGT62A1, a fungal UGT from Hericium erinaceum: "phylogenetic analysis revealed that UGT66A1 clusters only with UGT62A1, a fungal UGT from Hericium erinaceum"
