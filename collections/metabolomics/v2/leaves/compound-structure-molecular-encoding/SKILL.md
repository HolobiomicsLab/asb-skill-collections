---
name: compound-structure-molecular-encoding
description: Use when when you have SMILES strings or molecular structures for compounds
  and need to predict their retention behavior in reversed-phase liquid chromatography
  (RPLC) systems at pH ~2.7, but lack pre-computed molecular fingerprints or descriptor-based
  feature representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0602
  tools:
  - ROASMI
  - chemprop
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-025-00968-8
  title: ROASMI
evidence_spans:
- ROASMI is a Retention Order model to Assist Small Molecule Identification
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_roasmi_cq
    doi: 10.1186/s13321-025-00968-8
    title: ROASMI
  dedup_kept_from: coll_roasmi_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-025-00968-8
  all_source_dois:
  - 10.1186/s13321-025-00968-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-structure-molecular-encoding

## Summary

Encode small molecule structures into learned chemical embeddings using a directed message-passing neural network (D-MPNN) to represent compounds in generic chemical spaces attuned to chromatographic retention properties. This enables retention order prediction across diverse chemical spaces without requiring hand-crafted molecular descriptors or fingerprints.

## When to use

When you have SMILES strings or molecular structures for compounds and need to predict their retention behavior in reversed-phase liquid chromatography (RPLC) systems at pH ~2.7, but lack pre-computed molecular fingerprints or descriptor-based feature representations. Use this skill as the prerequisite step before ranking or retention order prediction.

## When NOT to use

- Compounds are outside reversed-phase liquid chromatography context or pH conditions differ substantially from ~2.7; the embeddings are trained specifically for RPLC at this pH and may not generalize.
- Input data are already hand-curated molecular descriptors or RDKit fingerprints; D-MPNN learns its own representations and does not require or improve from pre-computed features.
- Computational resources are severely limited and GPU acceleration is unavailable; the README notes CPU-only operation is possible but slower, and retraining is not recommended without GPU.

## Inputs

- SMILES strings or molecular structure objects for compounds
- Pre-trained ROASMI molecular embedding module weights

## Outputs

- Learned molecular embeddings in chemical space attuned to retention properties
- Encoded feature vectors for downstream retention order prediction

## How to apply

Load a pre-trained ROASMI molecular embedding module (an extension of chemprop using D-MPNN architecture) and pass SMILES or molecular structure data through it. The D-MPNN learns directly from compound structure to generate embeddings in a chemical space specifically tuned to retention properties, rather than mapping to artificially designed fingerprint or descriptor spaces. The resulting embeddings preserve structural information relevant to chromatographic behavior and allow prediction across new chemical spaces. These embeddings are then fed into the retention prediction module (RankNet) for ranking-based retention order inference.

## Related tools

- **ROASMI** (Complete retention order prediction framework containing the molecular embedding module (D-MPNN) and retention prediction module (RankNet) for small molecule identification via chromatographic retention) — https://github.com/FangYuan717/ROASMI
- **chemprop** (Base directed message-passing neural network architecture extended by ROASMI for learning molecular representations directly from compound structure) — https://github.com/chemprop/chemprop

## Examples

```
python code/ROASMI_predict.py
```

## Evaluation signals

- Embeddings successfully pass through downstream RankNet module without dimension mismatch errors
- Compounds with similar chemical structures produce embeddings with small Euclidean or cosine distance in embedding space
- Ensemble variance across four ROASMI models (ROASMI_1–ROASMI_5) for retention order predictions is lower for compounds in well-represented chemical spaces than outliers
- Predicted retention orders from the ensemble match experimental elution order for a held-out validation set of RPLC compounds at pH ~2.7
- The embedding space clusters compounds by chemical family or functional group, indicating the model has learned interpretable structural patterns

## Limitations

- Embeddings are trained specifically for reversed-phase liquid chromatography at pH ~2.7; generalization to other chromatographic modes (HILIC, SEC, etc.) or different pH conditions is not supported by the provided models.
- D-MPNN requires valid SMILES or structure input; malformed or disconnected molecular graphs will fail or produce unreliable embeddings.
- The README notes that optional descriptastorus package for computed RDKit features does not improve model performance, confirming that D-MPNN learns sufficient chemical information from structure alone without hand-crafted descriptors.
- Model uncertainty quantification via ensemble variance assumes that all four ROASMI models (ROASMI_1–ROASMI_5) were trained independently; predictions from a single model provide no uncertainty estimate.

## Evidence

- [readme] Molecular embedding module as extension of chemprop: "The molecular embedding module. This module is an extension of chemprop described in the paper [Analyzing Learned Molecular Representations for Property Prediction] which is available in the"
- [readme] D-MPNN learns directly from compound structure: "A directed message transfer neural network (D-MPNN) is used to learn directly from the structure of compounds, allowing prediction of compounds in new chemical spaces: molecules can be mapped"
- [readme] Four ROASMI models for RPLC pH 2.7: "We provide four initial ROASMI models (ROASMI_1 - ROASMI_5) for predicting the retention behavior of compounds in the reversed-phase liquid chromatography (RPLC) system with an eluent pH of around"
- [readme] Ensemble approach quantifies uncertainty via variance: "The ensemble approach allowed quantifying model uncertainty using the variance of the retention order predictions across the trained models."
- [readme] Optional descriptastorus does not improve performance: "The optional descriptastorus package is only necessary if you plan to incorporate computed RDKit features into your model. The ROASMI models we provide do not include these features as they have not"
