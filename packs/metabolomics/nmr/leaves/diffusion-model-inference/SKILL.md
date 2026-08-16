---
name: diffusion-model-inference
description: Use when when you have multi-modal spectroscopic data (IR, Raman, UV-Vis, mass spectra, or NMR) and need to recover the underlying molecular structure without relying on finite spectral libraries or autoregressive SMILES generation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - DiffSpectra
  - DiffSpectra (DMT + SpecFormer)
  - Model Checkpoints
  techniques:
  - NMR
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

# diffusion-model-inference

## Summary

Run a pretrained diffusion model conditioned on spectroscopic input data to iteratively generate candidate molecular structures. This skill applies spectrum-conditioned diffusion modeling to de novo molecular structure elucidation, producing ranked 2D/3D structures with confidence scores.

## When to use

When you have multi-modal spectroscopic data (IR, Raman, UV-Vis, mass spectra, or NMR) and need to recover the underlying molecular structure without relying on finite spectral libraries or autoregressive SMILES generation. Use this skill when 3D geometry and 2D topology must be jointly modeled from spectra.

## When NOT to use

- When input is a finite spectral library with known reference spectra — use retrieval-based matching instead.
- When only 2D topology is needed and 3D geometry is not required — a SMILES-only autoregressive model may be more efficient.
- When spectroscopic data is missing preprocessing or normalization steps specific to DiffSpectra — the model expects preprocessed tensor inputs matching training distribution.

## Inputs

- multi-modal spectroscopic data (IR, Raman, UV-Vis spectra as numeric arrays or encoded tensors)
- pretrained model checkpoint (DMT with SpecFormer encoder)
- configuration file specifying spectra modality version and model hyperparameters
- number of samples and evaluation checkpoint epoch

## Outputs

- ranked list of candidate molecular structures (SMILES or molecular graphs)
- confidence scores or reconstruction likelihood per candidate
- top-1 and top-10 accuracy metrics (exact structure recovery)
- optional 3D structural metrics (RMSD for geometry evaluation)
- generated molecule files saved to exp/{exp_name}/eval/

## How to apply

Load spectroscopic data and preprocess according to the DiffSpectra pipeline normalization and tokenization requirements. Initialize a pretrained diffusion model (e.g., pretrained DMT with SpecFormer encoder) from the checkpoint repository. Run the diffusion-based generation process conditioned on input spectra, iteratively denoising latent molecular representations over a fixed number of diffusion steps. Decode the denoised representations into molecular structure format (SMILES, InChI, or molecular graph). Rank and filter candidate structures by model confidence scores or reconstruction likelihood. Return a ranked list of candidate structures with associated confidence metrics and optionally compute 3D structural metrics (RMSD).

## Related tools

- **DiffSpectra (DMT + SpecFormer)** (SE(3)-equivariant denoising network and multi-modal spectral encoder for spectrum-conditioned diffusion inference) — https://github.com/AzureLeon1/DiffSpectra
- **Model Checkpoints** (Pretrained diffusion model weights for molecular structure generation) — https://huggingface.co/AzureLeon1/DiffSpectra

## Examples

```
CUDA_VISIBLE_DEVICES=0,1 python main.py --config configs/diffspectra_qm9s.py --config_original_qm9 configs/base_qm9.py --mode eval --workdir exp/allspectra --config.eval.ckpts '40' --config.eval.num_samples 10000 --config.eval.save_mols true --config.data.spectra_version allspectra
```

## Evaluation signals

- Top-1 accuracy ≥ 40.76% (exact molecular structure recovery on first-ranked candidate)
- Top-10 accuracy ≥ 99.49% (ground-truth structure within top 10 candidates)
- Generated molecules decode without error into valid molecular representations (SMILES or InChI)
- 3D RMSD metric computed from generated coordinates matches expectation for valid chemically equivalent structures
- Model confidence scores rank correct structures higher than incorrect alternatives

## Limitations

- Performance depends on multi-modal spectral data; single-modality input (e.g., IR only) yields lower accuracy than all-spectra combined.
- Model trained on QM9 dataset; applicability to larger, out-of-distribution molecules not extensively validated.
- Requires GPU acceleration (tested on multi-GPU setup); inference on CPU is not documented.
- Preprocessing and tokenization of spectra must exactly match DiffSpectra pipeline; misconfigured input normalization degrades output.
- No changelog or version history provided; backward compatibility across checkpoints unclear.

## Evidence

- [readme] DiffSpectra formulates structure elucidation as a conditional diffusion process: "DiffSpectra formulates structure elucidation as a **conditional diffusion process**."
- [readme] SpecFormer captures intra- and inter-spectrum dependencies across diverse spectral modalities: "**SpecFormer:** A transformer-based spectral encoder that captures intra- and inter-spectrum dependencies across diverse spectral modalities (e.g., IR, Raman, UV-Vis)."
- [readme] DiffSpectra achieves 40.76% top-1 accuracy and 99.49% top-10 accuracy: "DiffSpectra achieves **40.76% top-1 accuracy** and **99.49% top-10 accuracy** in recovering exact molecular structures."
- [other] Run the diffusion-based generation process conditioned on input spectra to iteratively denoise and generate molecular structure candidates: "Run the diffusion-based generation process conditioned on the input spectra to iteratively denoise and generate molecular structure candidates."
- [other] Decode the generated latent representations into molecular structure format: "Decode the generated latent representations into molecular structure format (SMILES, InChI, or molecular graph)."
- [other] Rank and filter candidate structures by model confidence scores or reconstruction likelihood: "Rank and filter candidate structures by model confidence scores or reconstruction likelihood."
- [other] Preprocess spectra according to DiffSpectra pipeline normalization and tokenization requirements: "Preprocess spectra according to DiffSpectra pipeline normalization and tokenization requirements."
