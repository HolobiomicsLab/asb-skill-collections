---
name: phylogenetic-tree-construction-and-interpretation
description: Construct maximum-likelihood phylogenetic trees from aligned protein sequences to resolve evolutionary relationships and identify functional divergence among homologous enzymes. This skill disambiguates the placement of newly characterized sequences within established protein families and informs functional predictions through phylogenetic clustering.
when_to_use_negative:
- Input sequences have not been filtered for spurious domains or low-complexity regions; alignment quality is not assured, risking misleading topology.
- The set of reference sequences does not include experimentally characterized family members; phylogenetic position alone cannot then inform functional prediction.
- Sequence divergence is very high or the alignment has excessive gaps (>50% missing data per column); homology assumptions break down and tree topology becomes unreliable.
edam_operation: http://edamontology.org/operation_0323
edam_topics:
- http://edamontology.org/topic_3293
- http://edamontology.org/topic_0080
- http://edamontology.org/topic_0623
tools:
- name: MAFFT
  role: Multiple sequence alignment of candidate UGT sequences to establish positional homology; used with default parameters prior to tree inference
- name: TrimAl
  role: Automated gap-removal and low-information column trimming to reduce phylogenetic noise in the alignment before tree-building
- name: FastTree
  role: Fast maximum-likelihood tree construction from aligned sequences; suitable for moderate-scale phylogenies (>100 sequences)
- name: RAxML
  role: Rigorous maximum-likelihood tree construction with support estimation; more computationally intensive but higher accuracy than FastTree
- name: Pfam database
  role: Prior filtering step to identify sequences containing target domain (e.g., PF00201) before phylogenetic analysis
  repo: http://pfam.xfam.org
- name: UGT Nomenclature Committee
  role: Reference repository of experimentally characterized UGTs used as anchors for functional annotation of phylogenetic clusters
  repo: https://labs.wsu.edu/ugt/
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/phylogenetic-tree-construction-and-interpretation@sha256:2466bb295032a32f8a5f62544db662fe2eb4b7cec46ebb44f4ad46b336d412e9
---

# phylogenetic-tree-construction-and-interpretation

## Summary

Construct maximum-likelihood phylogenetic trees from aligned protein sequences to resolve evolutionary relationships and identify functional divergence among homologous enzymes. This skill disambiguates the placement of newly characterized sequences within established protein families and informs functional predictions through phylogenetic clustering.

## When to use

When you have identified a candidate protein sequence (e.g., via domain scanning) and need to determine its evolutionary origin and likely function by comparing it to experimentally characterized homologs. Specifically, use this skill when domain-based classification alone is ambiguous or when you need phylogenetic support to hypothesize substrate specificity, catalytic mechanism, or functional category (e.g., UGT66A vs. UGT62).

## When NOT to use

- Input sequences have not been filtered for spurious domains or low-complexity regions; alignment quality is not assured, risking misleading topology.
- The set of reference sequences does not include experimentally characterized family members; phylogenetic position alone cannot then inform functional prediction.
- Sequence divergence is very high or the alignment has excessive gaps (>50% missing data per column); homology assumptions break down and tree topology becomes unreliable.

## Inputs

- Multiple sequence alignment (FASTA format) of filtered protein sequences, pre-filtered to remove sequences with multiple Pfam domains (e.g., both PF00201 and PF03033)
- Unaligned protein sequences in FASTA format (deduced amino acids)

## Outputs

- Maximum-likelihood phylogenetic tree (Newick format) with branch support values
- Clade assignment and clustering interpretation for query sequence (e.g., 'UGT66A1 clusters only with UGT62A1')
- Functional prediction inferred from phylogenetic position relative to characterized sequences

## How to apply

Beginning with a curated set of protein sequences (e.g., 138 UDP-glycosyltransferases with PF00201 domain), perform multiple sequence alignment using MAFFT with default parameters to ensure consistent positional homology. Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns that introduce phylogenetic noise. Construct a maximum-likelihood tree using FastTree or RAxML, which produces a bifurcating topology with branch support values (bootstrap or SH-aLRT). Inspect the tree to identify which characterized UGT subfamily(ies) your query sequence clusters with (monophyly indicates functional constraint). The rationale is that proteins clustering together have recent common ancestry and thus likely share substrate specificity, cofactor usage, and subcellular localization; deviations from expected clusters signal functional innovation or misclassification.

## Related tools

- **MAFFT** (Multiple sequence alignment of candidate UGT sequences to establish positional homology; used with default parameters prior to tree inference)
- **TrimAl** (Automated gap-removal and low-information column trimming to reduce phylogenetic noise in the alignment before tree-building)
- **FastTree** (Fast maximum-likelihood tree construction from aligned sequences; suitable for moderate-scale phylogenies (>100 sequences))
- **RAxML** (Rigorous maximum-likelihood tree construction with support estimation; more computationally intensive but higher accuracy than FastTree)
- **Pfam database** (Prior filtering step to identify sequences containing target domain (e.g., PF00201) before phylogenetic analysis) — http://pfam.xfam.org
- **UGT Nomenclature Committee** (Reference repository of experimentally characterized UGTs used as anchors for functional annotation of phylogenetic clusters) — https://labs.wsu.edu/ugt/

## Examples

```
mafft --auto filtered_UGTs.fasta > aligned_UGTs.fasta && trimal -in aligned_UGTs.fasta -out trimmed_UGTs.fasta -automated1 && fasttree -quote aligned_UGTs.fasta > UGT_tree.nwk
```

## Evaluation signals

- Sequence alignment exhibits no obvious misalignments in secondary-structure regions (e.g., active-site motifs are aligned across all sequences); spot-check conserved residue columns visually or via entropy scoring.
- Trimmed alignment retains >30% of original positions; excessive trimming indicates low sequence conservation and unreliable tree inference.
- Branch support values (bootstrap or SH-aLRT) for internal nodes are >70 (well-supported clades) or >50 (weakly supported); low support on the branch containing the query sequence suggests its functional assignment is ambiguous.
- Query sequence clusters with at least one experimentally characterized family member with support >50; if it branches alone or with only uncharacterized sequences, functional prediction is not grounded.
- Tree topology is consistent with known evolutionary relationships (e.g., fungi and plants cluster in separate clades if both are present); major topological inversions may indicate misalignment or extreme sequence divergence.

## Limitations

- Phylogenetic clustering does not prove functional equivalence; LbUGT3 clusters with UGT66A1 but may have substrate promiscuity not seen in the reference protein (e.g., can use both UDP-xylose and UDP-glucose while reference may use only one).
- Multiple uncharacterized or poorly annotated sequences in the alignment can mislead tree topology; the quality of reference data directly affects confidence in functional prediction.
- Gene duplication and horizontal transfer can produce trees that do not reflect true organismal phylogeny; substrate specificity and enzymatic activity may diverge rapidly even between closely related sequences.
- Transmembrane topology and subcellular localization (predicted, e.g., by DeepTMHMM) are not resolved by phylogenetic analysis alone and must be integrated separately to complete functional annotation.

## Evidence

- [results] Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters.: "Perform multiple sequence alignment of the filtered UGT sequences using MAFFT with default parameters."
- [results] Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns.: "Trim the alignment using TrimAl with automated gap-removal settings to remove low-information columns."
- [results] Construct a maximum-likelihood phylogenetic tree from the trimmed alignment using standard tree-building software (FastTree or RAxML) to resolve placement of UGT66A1 among the 138 UGTs.: "Construct a maximum-likelihood phylogenetic tree from the trimmed alignment using standard tree-building software (FastTree or RAxML)"
- [results] Protein sequence–based phylogenetic analysis with the other experimentally characterized UGTs revealed that UGT66A1 clusters only with UGT62A1: "Protein sequence–based phylogenetic analysis with the other experimentally characterized UGTs revealed that UGT66A1 clusters only with UGT62A1"
- [other] Eight putative UGTs were found in L. brumalis; phylogenetic analysis revealed that UGT66A1 clusters only with UGT62A1, a fungal UGT from Hericium erinaceus.: "phylogenetic analysis revealed that UGT66A1 clusters only with UGT62A1, a fungal UGT from Hericium erinaceus"
