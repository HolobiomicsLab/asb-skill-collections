---
name: numerical-reproducibility-testing
description: Use when you have instantiated a learned component (embedding layer,
  encoder, or transformer submodule) from a published codebase and need to verify
  that its forward pass produces outputs matching the original paper's implementation
  before integrating it into a downstream analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MIST
  - SCARF
  - MIST-CF
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numerical-reproducibility-testing

## Summary

Validate that neural network embedding layers produce consistent, numerically stable outputs by comparing forward-pass results against reference implementations using strict tolerance thresholds. This skill ensures that model components (e.g., sinusoidal formula embeddings) reproduce reliably across environments and commits.

## When to use

You have instantiated a learned component (embedding layer, encoder, or transformer submodule) from a published codebase and need to verify that its forward pass produces outputs matching the original paper's implementation before integrating it into a downstream analysis pipeline. Use this skill when publishing or reusing model code to detect silent numerical drift, initialization errors, or architectural divergence.

## When NOT to use

- You are validating a model's end-to-end task performance (e.g., formula ranking accuracy on held-out spectra) rather than component-level reproducibility. Use task-level evaluation metrics instead.
- You lack reference outputs from the original implementation or published codebase. Numerical reproducibility requires a ground-truth baseline.
- Your inputs are synthetic or toy data not representative of the domain the embedding was trained on (e.g., random token IDs instead of valid chemical formulas).

## Inputs

- Neural network embedding layer code (e.g., PyTorch module or TensorFlow/Keras layer)
- Representative domain inputs (chemical formulas, sequences, or structured objects)
- Reference output embeddings from published repository (CSV, HDF5, or NumPy format)
- Configuration parameters (embedding dimension, initialization seed, precision dtype)

## Outputs

- Embedding vectors (dense float arrays, shape [num_inputs, embedding_dim])
- Validation report (structured file: pass/fail flags, L2 distances, dimensionality checks, range checks)
- Reproducibility metrics (max L2 distance, mean L2 distance, percentage of inputs passing tolerance threshold)

## How to apply

First, instantiate the target embedding layer (e.g., sinusoidal formula embeddings from SCARF as incorporated in MIST-CF) with a defined dimensionality and forward-compatible configuration. Second, prepare a representative set of inputs (e.g., chemical formulas C6H12O6, C3H7NO2, C8H10N4O2) that span the domain the model was trained on. Third, invoke the forward pass on each input and collect the output embedding vectors. Fourth, verify that embedding dimensionality matches the configured parameter and that all values fall within the expected numerical range (typically [−1, 1] for sinusoidal embeddings). Fifth, compute pairwise L2 distances between your outputs and reference outputs from the published repository, using a strict tolerance threshold (e.g., L2 distance < 1e-6 for single-precision reproducibility). Sixth, document pass/fail status and numerical statistics (max distance, mean distance) in a structured output file for audit and publication.

## Related tools

- **MIST-CF** (Source repository containing sinusoidal formula embedding implementation adopted from SCARF; provides reference outputs and configuration for reproducibility testing) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Original work defining sinusoidal formula embeddings technique; establishes embedding design and expected numerical properties) — https://arxiv.org/abs/2303.06470

## Examples

```
from mist_cf.embeddings import SinusoidalFormulaEmbedding; import torch; emb = SinusoidalFormulaEmbedding(embedding_dim=128); formulas = ['C6H12O6', 'C3H7NO2', 'C8H10N4O2']; outputs = torch.stack([emb(f) for f in formulas]); assert outputs.shape == (3, 128) and torch.all(outputs >= -1.0) and torch.all(outputs <= 1.0)
```

## Evaluation signals

- Embedding vector dimensionality equals the configured embedding_dim parameter for all inputs.
- All embedding values fall within the expected range (typically [−1, 1] for sinusoidal embeddings); check min/max across all outputs.
- L2 distance between reproduced embeddings and reference outputs is below the tolerance threshold (e.g., < 1e-6); compute pairwise distances for each formula.
- Validation report indicates 100% of test inputs passed numerical tolerance checks; no inputs have anomalously large distances.
- Embedding statistics (mean, std, quantiles) are consistent with reference outputs, indicating no systematic bias or scale drift.

## Limitations

- Reproducibility depends critically on matching the original implementation's precision (float32 vs. float64), initialization seed, and library versions (PyTorch, NumPy). Minor numerical differences may arise from platform-specific floating-point behavior.
- The tolerance threshold (e.g., L2 < 1e-6) must be chosen in advance based on the precision and scale of the embeddings; too strict a threshold may fail due to acceptable floating-point rounding, while too loose a threshold may miss real divergence.
- This skill validates component reproducibility only; it does not ensure that downstream model predictions (e.g., formula ranking or scoring) remain accurate after integration or parameter updates.
- Representative inputs must be carefully selected to cover the domain space. If test inputs are unrepresentative (e.g., formulae outside the training distribution), the validation may not detect subtle errors.

## Evidence

- [other] Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors.: "Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors."
- [other] Verify embedding vector dimensionality matches the configured embedding dimension parameter and all embedding values fall within the expected numerical range.: "Verify embedding vector dimensionality matches the configured embedding dimension parameter. 5. Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal"
- [other] Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (L2 distance < 1e-6) to confirm reproducibility.: "Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility."
- [other] MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture.: "MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture for improved representation of chemical"
- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]"
