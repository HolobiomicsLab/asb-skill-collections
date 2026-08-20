---
name: spectra-to-structure-elucidation
description: Use when you have one or more spectroscopic datasets (IR, Raman, UV-Vis,
  mass spectra, NMR) from an unknown compound and need to generate candidate molecular
  structures ranked by likelihood. Use this when retrieval-based approaches are infeasible
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - DiffSpectra
  - DiffSpectra (Diffusion Molecule Transformer + SpecFormer)
  - SpecFormer
  - Diffusion Molecule Transformer (DMT)
  techniques:
  - NMR
  license_tier: open
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

# spectra-to-structure-elucidation

## Summary

Apply spectrum-conditioned diffusion modeling to generate candidate molecular structures from multi-modal spectroscopic input (IR, Raman, UV-Vis, mass spectra, NMR). This skill unifies multi-modal spectral reasoning with joint 2D topology and 3D geometry generative modeling to perform de novo molecular structure elucidation.

## When to use

You have one or more spectroscopic datasets (IR, Raman, UV-Vis, mass spectra, NMR) from an unknown compound and need to generate candidate molecular structures ranked by likelihood. Use this when retrieval-based approaches are infeasible (e.g., compound is not in a library) and you require both 2D connectivity and 3D geometry in the output.

## When NOT to use

- Spectroscopic input has not been preprocessed or normalized according to DiffSpectra pipeline requirements — preprocessing is mandatory.
- The unknown compound is known to be in an existing chemical library; use retrieval-based methods instead.
- Only 2D topology is needed and 3D geometry is not relevant to the application.

## Inputs

- Multi-modal spectroscopic data (IR, Raman, UV-Vis, mass spectra, or combinations)
- Preprocessed and tokenized spectra following DiffSpectra normalization requirements
- Pretrained model checkpoint (DMT + SpecFormer weights)
- Configuration file specifying spectra_version, model.name, eval.num_samples, eval.ckpts

## Outputs

- Ranked list of candidate molecular structures in SMILES, InChI, or molecular graph format
- Confidence scores or reconstruction likelihood metrics for each candidate
- Top-k accuracy metrics (e.g., top-1 and top-10 exact match rates)
- 3D structural metrics (e.g., RMSD) if evaluated against reference structures

## How to apply

Load preprocessed spectroscopic input data and initialize a pretrained diffusion model (DMT + SpecFormer) conditioned on the spectra. The SpecFormer encoder captures intra- and inter-spectrum dependencies across modalities; the SE(3)-equivariant DMT denoises iteratively to generate 2D/3D molecular candidates. Run the diffusion process (typically 40 checkpoint steps) to generate a sample pool (e.g., 10,000 molecules). Decode latent representations into SMILES, InChI, or molecular graph format. Rank candidates by model confidence or reconstruction likelihood and filter by chemical validity. Evaluate top-k accuracy (e.g., top-1 and top-10 exact match rates) against ground truth if available.

## Related tools

- **DiffSpectra (Diffusion Molecule Transformer + SpecFormer)** (Pretrained generative model that performs spectrum-conditioned diffusion to jointly model 2D topology and 3D geometry; SE(3)-equivariant denoising network with multi-modal spectral encoder) — https://github.com/AzureLeon1/DiffSpectra
- **SpecFormer** (Transformer-based spectral encoder within DiffSpectra that captures intra- and inter-spectrum dependencies across IR, Raman, UV-Vis, and other modalities) — https://github.com/AzureLeon1/DiffSpectra
- **Diffusion Molecule Transformer (DMT)** (SE(3)-equivariant denoising network that models both 2D topology and 3D geometry of molecules during iterative generation) — https://github.com/AzureLeon1/DiffSpectra

## Examples

```
CUDA_VISIBLE_DEVICES=0,1 python main.py --config configs/diffspectra_qm9s.py --config_original_qm9 configs/base_qm9.py --mode eval --workdir exp/allspectra --config.eval.ckpts '40' --config.eval.num_samples 10000 --config.eval.save_mols true --config.data.spectra_version allspectra
```

## Evaluation signals

- Top-1 and top-10 exact match accuracy: percentage of test cases where ground-truth structure ranks in top-k predictions (expected: ≥40.76% top-1, ≥99.49% top-10 based on paper results)
- Chemical validity: all generated molecules pass RDKit validity checks and have correct valence/aromaticity
- Reconstruction likelihood: confidence scores for top-ranked predictions are higher than those for lower-ranked candidates
- 3D geometry fidelity: RMSD between predicted 3D coordinates and reference structures falls within acceptable range for the application domain
- Spectra consistency: generated structures, when re-embedded and spectrum-predicted, should reconstruct input spectra with low reconstruction error

## Limitations

- Performance is spectrum-dependent: single-modality predictions (IR or Raman only) show lower accuracy than multi-modal fusion; UV-Vis alone is less informative than combined modalities
- Requires substantial training data and pretrained model checkpoints; performance degrades on out-of-distribution spectroscopic inputs or rare molecular scaffolds not well-represented in training set
- Computational cost scales with number of diffusion steps (40 steps per model) and sample pool size; generating 10,000 candidates requires multi-GPU resources
- Does not recover stereochemistry information that is not encoded in spectroscopic modalities; 2D exact match may not imply correct stereoisomer assignment

## Evidence

- [readme] multi-modal spectral data: "generative framework for molecular structure elucidation from multi-modal spectral data"
- [readme] SE(3)-equivariant denoising network: "Diffusion Molecule Transformer (DMT): An SE(3)-equivariant denoising network that models both 2D topology and 3D geometry of molecules"
- [readme] SpecFormer transformer encoder: "SpecFormer: A transformer-based spectral encoder that captures intra- and inter-spectrum dependencies across diverse spectral modalities (e.g., IR, Raman, UV-Vis)"
- [readme] 40.76% top-1 accuracy and 99.49% top-10 accuracy: "Extensive experiments demonstrate that DiffSpectra achieves 40.76% top-1 accuracy and 99.49% top-10 accuracy in recovering exact molecular structures"
- [readme] conditional diffusion process: "DiffSpectra formulates structure elucidation as a conditional diffusion process"
- [readme] spectrum-conditioned diffusion modeling: "Through spectrum-conditioned diffusion modeling, DiffSpectra unifies multi-modal reasoning with 2D/3D generative modeling"
- [readme] first framework unifying multi-modal spectral reasoning: "DiffSpectra is the first framework that unifies multi-modal spectral reasoning and joint 2D/3D generative modeling for de novo molecular structure elucidation"
- [other] Preprocess spectra and initialize diffusion model: "Preprocess spectra according to DiffSpectra pipeline normalization and tokenization requirements. 3. Initialize the pretrained diffusion model"
- [other] Decode into SMILES, InChI, or molecular graph: "Decode the generated latent representations into molecular structure format (SMILES, InChI, or molecular graph)"
