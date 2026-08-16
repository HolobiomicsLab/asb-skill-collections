---
name: molecular-fragment-assembly-from-transformer-predictions
description: Use when when you have encoded spectral features (from a CNN featurizer applied to 1D 1H and/or 13C NMR spectra) and a set of candidate molecular fragments predicted for a molecule with ≤19 heavy atoms, and you need to determine the correct connectivity and assembly order to recover the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0081
  tools:
  - transformer architecture
  - convolutional neural network
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acscentsci.4c01132
  title: NMR2Struct
evidence_spans:
- a transformer architecture can be constructed to efficiently solve the task
- we show how a transformer architecture can be constructed to efficiently solve the task
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nmr2struct
    doi: 10.1021/acscentsci.4c01132
    title: NMR2Struct
  dedup_kept_from: coll_nmr2struct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.4c01132
  all_source_dois:
  - 10.1021/acscentsci.4c01132
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fragment-assembly-from-transformer-predictions

## Summary

This skill uses a transformer architecture to assemble large numbers of molecular fragments predicted from spectral features into complete molecular structures with connectivity information. It is applied as the decoding stage of an end-to-end NMR-to-structure pipeline to convert fragment embeddings into valid molecular graphs.

## When to use

When you have encoded spectral features (from a CNN featurizer applied to 1D 1H and/or 13C NMR spectra) and a set of candidate molecular fragments predicted for a molecule with ≤19 heavy atoms, and you need to determine the correct connectivity and assembly order to recover the ground-truth molecular structure rather than enumerating all combinatorially possible combinations.

## When NOT to use

- Input molecules contain >19 heavy atoms; the framework is demonstrated only on molecules with ≤19 non-hydrogen atoms and may not scale or remain accurate for larger structures.
- Input spectra are not preprocessed 1D 1H or 13C NMR; the model expects single-dimensional spectra, not 2D COSY, HSQC, or other multi-dimensional techniques.
- Fragment candidates are not available or cannot be reliably extracted from spectral features; the skill assumes fragments are already identified and only assembles them.

## Inputs

- encoded spectral features (CNN output tensor from preprocessed 1D NMR spectra)
- molecular formula constraints (optional; predicted or ground-truth element counts)
- candidate molecular fragments (set or embedding matrix)

## Outputs

- predicted molecular connectivity (adjacency matrix or bond table)
- molecular structure graph (nodes = atoms, edges = bonds)
- top-k candidate structures ranked by confidence or likelihood score

## How to apply

Feed the CNN-encoded spectral features into the transformer architecture, which treats molecular fragment assembly as a sequence-to-sequence decoding task. The transformer learns to order and connect fragments by attending to spectral evidence and previously assembled substructures. The model is trained via multitask learning to jointly predict molecular formula and connectivity, regularizing fragment choices toward chemically valid combinations. Perform inference by decoding the transformer output autoregressively or via beam search to produce candidate molecular graphs, then rank by confidence scores or exact structure recovery against known ground-truth. The transformer's attention mechanism allows it to implicitly learn which spectral peaks correspond to which molecular substructures, bridging the combinatorial explosion problem inherent in manual fragment assembly.

## Related tools

- **transformer architecture** (decoding stage for assembling molecular fragments into connectivity; learns attention-based mapping from spectral features to bond predictions and fragment ordering)
- **convolutional neural network** (encoder stage; extracts spectral features from raw 1D NMR spectra prior to transformer decoding)

## Evaluation signals

- Exact structure recovery rate: percentage of test molecules for which the top-1 predicted structure matches the ground-truth molecular structure (including all atoms and bonds).
- Top-k accuracy: fraction of test cases where the correct structure appears in the top-k candidate predictions ranked by confidence.
- Molecular formula correctness: verify that predicted formula (element counts) matches the ground-truth before or independently of connectivity accuracy.
- Invariant checks: all predicted bonds are chemically valid (e.g., valence constraints respected, no invalid bond multiplicities); connectivity forms a single connected component.
- Comparison to baseline: performance improvement over fragment-assembly heuristics or exhaustive enumeration on molecules with ≤19 heavy atoms.

## Limitations

- Evaluation is limited to molecules with ≤19 heavy atoms; scalability to larger structures is not demonstrated.
- Combinatorial explosion of possible molecular structures makes manual validation challenging; the paper relies on test set ground-truth comparison rather than independent chemical verification.
- Model performance depends on preprocessing quality and completeness of spectral input (1H and/or 13C); incomplete or noisy spectra may degrade assembly accuracy.
- The skill assumes fragments have been correctly identified from spectra; errors in fragment detection are not corrected during assembly.

## Evidence

- [intro] a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures: "a transformer architecture can be constructed to efficiently solve the task, traditionally performed by chemists, of assembling large numbers of molecular fragments into molecular structures"
- [intro] Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra: "Integrating this capability with a convolutional neural network, we build an end-to-end model for predicting structure from spectra"
- [intro] we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra: "we introduce a multitask machine learning framework that predicts the molecular structure (formula and connectivity) of an unknown compound solely based on its 1D 1H and/or 13C NMR spectra"
- [intro] We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms: "We demonstrate the effectiveness of this framework on molecules with up to 19 heavy (non-hydrogen) atoms"
- [intro] elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion: "elucidating structure using only one-dimensional (1D) NMR spectra, the most readily accessible data, remains an extremely challenging problem because of the combinatorial explosion"
