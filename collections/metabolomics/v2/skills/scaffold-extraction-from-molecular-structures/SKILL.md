---
name: scaffold-extraction-from-molecular-structures
description: 'Use when when pre-training or fine-tuning a molecular representation
  model on natural products and you need to encode scaffold-derived evolutionary patterns
  as a distinct learning signal. Trigger: input is SMILES strings or molecular graphs
  from natural product databases (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3369
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0121
  tools:
  - Git
  - PyTorch or equivalent deep learning framework (inferred from GNN/contrastive learning
    context)
  - RDKit
  - PyTorch Geometric (PyG)
  - NaFM pre-training framework
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans:
- Fork the repository
- Our method integrates contrastive learning with masked graph modeling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_nafm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# scaffold-extraction-from-molecular-structures

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract chemical scaffolds from natural product molecular structures to isolate conserved core frameworks that encode evolutionary lineage and biosynthetic ancestry. This isolates scaffold-derived patterns for contrastive learning in pre-training natural product foundation models.

## When to use

When pre-training or fine-tuning a molecular representation model on natural products and you need to encode scaffold-derived evolutionary patterns as a distinct learning signal. Trigger: input is SMILES strings or molecular graphs from natural product databases (e.g., LOTUS, custom biosynthetic collections) and your downstream task includes taxonomy classification, gene-level or microbial-level evolutionary inference, or virtual screening where scaffold conservation reflects biosynthetic ancestry.

## When NOT to use

- Input molecules are purely synthetic (non-natural products); conventional scaffolding lacks discriminative power for evolutionary lineage.
- Downstream task is chemical property prediction (logP, solubility) rather than evolutionary or biosynthetic inference; scaffold features are not optimized for these targets.
- Molecular graph already includes explicit side-chain encoding and you are bypassing explicit scaffold extraction; dual objectives may over-regularize the model.

## Inputs

- SMILES strings (CSV or pickle format, as in pretrain_smiles.pkl)
- Molecular graphs (PyG Data objects or rdkit mol objects)
- Natural product molecular structure database (e.g., LOTUS, ONTOLOGY, custom BGC-derived collections)

## Outputs

- Scaffold representations (Murcko scaffolds as SMILES or graph embeddings)
- Side-chain information (atomic/bond features isolated from scaffold)
- Scaffold-annotated molecular graph dataset (input to contrastive learning objective)
- Scaffold similarity matrix or contrastive pairs for pre-training

## How to apply

Parse input SMILES strings into molecular graphs, compute Murcko scaffolds (core ring systems and linkers with all side chains removed) to isolate evolutionary-conserved backbones. Extract side-chain information separately to preserve biosynthetic diversity. Integrate scaffold representations into the contrastive learning objective alongside full-molecule representations, such that molecules sharing scaffolds are pulled into proximity in embedding space. The rationale is that natural products exhibit strong scaffold clustering by organism and biosynthetic pathway; explicitly encoding scaffold similarity improves the model's capacity to learn evolutionary information at both gene and microbial levels (as validated in NaFM's taxonomy classification benchmarks). Scaffold and side-chain information are complementary: contrastive learning on scaffolds captures evolutionary commonality while masked graph modeling on full structures preserves biosynthetic diversity.

## Related tools

- **RDKit** (Compute Murcko scaffolds from SMILES and convert molecules to graph representations)
- **PyTorch Geometric (PyG)** (Represent scaffold and side-chain information as graph nodes/edges; construct batches for contrastive learning)
- **NaFM pre-training framework** (Integrate scaffold extraction and side-chain encoding into dual contrastive + masked modeling pipeline) — https://github.com/TomAIDD/NaFM-Official

## Examples

```
python scripts/setup_data.py; python train.py --conf examples/Pretrain.yml
```

## Evaluation signals

- Scaffold extraction preserves ring systems and linkers while removing all side chains; verify by comparing Murcko scaffold SMILES to original SMILES (scaffold should be a substructure).
- Contrastive pairs: molecules with identical scaffolds but different side chains should have high cosine similarity in scaffold embedding space; validate via k-nearest neighbor analysis on scaffold embeddings.
- Downstream taxonomy classification accuracy on held-out natural products improves when NaFM-pretrained scaffold representations are used vs. models pre-trained on synthetic molecules (as reported in paper benchmarks).
- Scaffold clustering in learned embedding space correlates with known biosynthetic pathways or organism taxonomy (gene/microbial-level analysis signal).
- Ablation: remove scaffold extraction and re-train; contrastive loss should be higher and downstream taxonomy accuracy should drop, confirming scaffold information is a material learning signal.

## Limitations

- Murcko scaffold extraction assumes ring systems encode evolutionary lineage; linear natural products (no rings) yield trivial or empty scaffolds and may not benefit from this approach.
- Scaffold conservation is organism/pathway-dependent; scaffolds extracted from unrelated natural product families may not cluster meaningfully.
- Scaffold extraction is computationally expensive for large pre-training datasets; preprocessing (SMILES standardization, scaffold generation) must be run once and cached (as in NaFM's filter.py step).
- Side-chain diversity is lost in scaffold representation; models must use both scaffold and full-molecule objectives to retain biosynthetic details.

## Evidence

- [intro] Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information: "Our method integrates contrastive learning with masked graph modeling, effectively encoding scaffold-derived evolutionary patterns alongside diverse side-chain information"
- [other] Identify and document the scaffold extraction and side-chain encoding mechanisms used to represent evolutionary and structural diversity.: "Identify and document the scaffold extraction and side-chain encoding mechanisms used to represent evolutionary and structural diversity."
- [intro] Through detailed analysis at both gene and microbial levels, NaFM reveals a strong capacity for learning evolutionary information: "Through detailed analysis at both gene and microbial levels, NaFM reveals a strong capacity for learning evolutionary information"
- [intro] conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products: "conventional molecular representation techniques are not well-suited to the unique structural and evolutionary features of natural products"
