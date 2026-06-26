---
name: molecular-structure-decoding
description: Use when after running spectrum-conditioned diffusion generation that
  produces latent molecular representations, when you need to convert continuous or
  abstract model outputs into discrete chemical formats suitable for structure matching,
  library comparison, or chemical database lookup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0369
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2275
  tools:
  - DiffSpectra
  - Diffusion Molecule Transformer (DMT)
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.48550/arxiv.2507.06853
  title: DiffSpectra
evidence_spans:
- github.com/AzureLeon1/DiffSpectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_diffspectra_cq
    doi: 10.48550/arxiv.2507.06853
    title: DiffSpectra
  dedup_kept_from: coll_diffspectra_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.48550/arxiv.2507.06853
  all_source_dois:
  - 10.48550/arxiv.2507.06853
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-decoding

## Summary

Decoding latent representations from diffusion models into interpretable molecular structure formats (SMILES, InChI, or molecular graphs). This skill bridges generative model outputs to chemically valid, ranked candidate structures for downstream validation and analysis.

## When to use

Apply this skill after running spectrum-conditioned diffusion generation that produces latent molecular representations, when you need to convert continuous or abstract model outputs into discrete chemical formats suitable for structure matching, library comparison, or chemical database lookup. Specifically use when the diffusion model has completed iterative denoising and you have latent state tensors that encode both 2D topology and 3D geometry but are not yet in a queryable chemical format.

## When NOT to use

- Input is already in a queryable chemical format (SMILES, InChI, SDF, MOL2) — skip directly to structure matching.
- Latent representations have not completed the full diffusion denoising cycle — apply this skill only after generation is complete.
- You need to preserve probabilistic uncertainty across the full candidate ensemble rather than deterministic point estimates — consider sampling multiple trajectories before decoding instead.

## Inputs

- Latent molecular representations from diffusion model (tensors encoding 2D topology and 3D geometry)
- Diffusion model confidence scores or denoising log-likelihoods
- Trained Diffusion Molecule Transformer checkpoint

## Outputs

- Decoded molecular structures in SMILES format
- Decoded molecular structures in InChI format
- Molecular graphs with ranked confidence scores
- Ranked list of candidate structures with reconstruction likelihood metrics

## How to apply

After the diffusion-based generation process completes iterative denoising conditioned on input spectra, retrieve the final latent state from the Diffusion Molecule Transformer (DMT). Decode these latent representations into molecular structure format by inverting the SE(3)-equivariant encoding: extract 2D bond topology and atomic coordinates to construct a molecular graph, then serialize into SMILES or InChI strings. Rank candidate structures by the model's confidence scores (typically denoising log-likelihood or reconstruction error at the final timestep). Filter candidates by a threshold (e.g., top-10 by confidence) and optionally apply chemical validity checks (valence, aromaticity) to eliminate chemically infeasible structures. Output a ranked list paired with confidence metrics for retrieval against reference spectroscopic databases or known compound libraries.

## Related tools

- **Diffusion Molecule Transformer (DMT)** (SE(3)-equivariant denoising network that generates latent molecular representations encoding both 2D topology and 3D geometry; outputs are decoded by this skill) — https://github.com/AzureLeon1/DiffSpectra
- **DiffSpectra** (End-to-end framework housing the diffusion pipeline; this skill is invoked as the output decoding stage of the full DiffSpectra workflow) — https://github.com/AzureLeon1/DiffSpectra

## Examples

```
CUDA_VISIBLE_DEVICES=0,1 python main.py --config configs/diffspectra_qm9s.py --config_original_qm9 configs/base_qm9.py --mode eval --workdir exp/allspectra --config.eval.ckpts '40' --config.eval.num_samples 10000 --config.eval.save_mols true --config.data.spectra_version allspectra
```

## Evaluation signals

- Decoded SMILES/InChI strings pass chemical validity checks (valence, aromaticity, atom count > 0).
- Top-1 accuracy on held-out test spectra: recovered structure exactly matches ground-truth molecular identity (exact match to reference SMILES or InChI).
- Top-10 accuracy: ground-truth structure appears in ranked list of top-10 candidates by confidence score (expected ≥99% per README performance claim).
- Ranked confidence scores are monotonic or non-increasing from rank 1 to rank 10 — no rank inversions.
- Generated molecules can be successfully imported and validated by RDKit or OpenBabel without errors; 3D coordinates satisfy SE(3) equivariance constraints (e.g., invariance to rigid rotations and translations).

## Limitations

- Decoding accuracy depends critically on quality of latent representations from the DMT; poor denoising leads to invalid or chemically infeasible structures.
- Framework achieves 40.76% top-1 accuracy, meaning ~59% of single-best predictions are incorrect — rank-1 structures should not be trusted without additional confirmation.
- Decoding is deterministic given a latent state; stochasticity must be injected at the diffusion generation stage, not the decoding stage, to explore alternative candidate structures.
- Performance is benchmarked on QM9S dataset; generalization to out-of-domain spectra or larger molecular weight ranges (>900 Da) is not explicitly reported.
- SE(3)-equivariance assumes rigid 3D molecular geometry; highly flexible or disordered molecular ensembles may not decode correctly.

## Evidence

- [other] Decode the generated latent representations into molecular structure format (SMILES, InChI, or molecular graph).: "Decode the generated latent representations into molecular structure format (SMILES, InChI, or molecular graph)."
- [other] Rank and filter candidate structures by model confidence scores or reconstruction likelihood.: "Rank and filter candidate structures by model confidence scores or reconstruction likelihood."
- [readme] Diffusion Molecule Transformer (DMT): An SE(3)-equivariant denoising network that models both 2D topology and 3D geometry of molecules.: "Diffusion Molecule Transformer (DMT): An SE(3)-equivariant denoising network that models both 2D topology and 3D geometry of molecules."
- [readme] Through spectrum-conditioned diffusion modeling, DiffSpectra unifies multi-modal reasoning with 2D/3D generative modeling. Extensive experiments demonstrate that DiffSpectra achieves 40.76% top-1 accuracy and 99.49% top-10 accuracy in recovering exact molecular structures.: "DiffSpectra achieves 40.76% top-1 accuracy and 99.49% top-10 accuracy in recovering exact molecular structures."
- [other] Output ranked list of candidate structures with associated confidence metrics.: "Output ranked list of candidate structures with associated confidence metrics."
