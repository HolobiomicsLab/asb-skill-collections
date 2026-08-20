---
name: embedding-vector-validation
description: Use when after instantiating and invoking a sinusoidal formula embedding
  layer (such as SCARF embeddings in MIST-CF) on chemical formula inputs, validate
  that the output embeddings meet dimensionality and value constraints before using
  them for downstream transformer or ranking tasks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0080
  tools:
  - MIST
  - SCARF
  - MIST-CF
  license_tier: open
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

# embedding-vector-validation

## Summary

Validate sinusoidal formula embedding vectors produced by a neural network layer by checking dimensionality, numerical range, and reproducibility against reference outputs. This skill ensures embeddings are correctly instantiated and can be reliably compared across runs or implementations.

## When to use

After instantiating and invoking a sinusoidal formula embedding layer (such as SCARF embeddings in MIST-CF) on chemical formula inputs, validate that the output embeddings meet dimensionality and value constraints before using them for downstream transformer or ranking tasks. Apply this skill when you need to verify that a newly trained or loaded embedding model produces mathematically sound and reproducible outputs.

## When NOT to use

- Input embeddings are not sinusoidal or do not come from a learned transformation layer (e.g., one-hot encoded or pre-normalized embeddings that already satisfy known constraints).
- You are validating a final ranking or scoring output from MIST-CF rather than intermediate embedding representations — use model-level evaluation metrics (e.g., top-k accuracy on test spectra) instead.
- The chemical formula input set is empty or contains only formulas already known to produce edge-case embeddings (e.g., empty string, single atom).

## Inputs

- Chemical formula strings (e.g., 'C6H12O6', 'C3H7NO2')
- Sinusoidal embedding layer (instantiated model)
- Configured embedding dimensionality parameter
- Reference embedding outputs or checkpoint (optional, for reproducibility check)

## Outputs

- Embedding vectors (numerical arrays, shape [num_formulas, embedding_dim])
- Dimensionality validation report (boolean: pass/fail)
- Numerical range validation report (min, max values observed)
- Reproducibility comparison metrics (L2 distances to reference)
- Structured output file (e.g., JSON, CSV) with embedding vectors and validation results

## How to apply

Load or instantiate a representative set of chemical formula inputs (e.g., common organic molecules like glucose C6H12O6, alanine C3H7NO2, caffeine C8H10N4O2). Invoke the forward pass on the sinusoidal embedding layer to generate embedding vectors. Perform four sequential checks: (1) verify embedding vector dimensionality matches the configured embedding_dim parameter; (2) verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings); (3) confirm reproducibility by comparing produced embeddings against reference outputs using numerical tolerance (e.g., L2 distance < 1e-6); (4) output embedding vectors and validation results to a structured file for inspection. The L2 distance threshold of 1e-6 is chosen to account for floating-point precision variations across hardware and implementations.

## Related tools

- **MIST-CF** (Source neural network architecture containing the sinusoidal formula embedding layer to be validated) — https://github.com/samgoldman97/mist-cf
- **SCARF** (Prior work that developed the sinusoidal formula embeddings technique adopted in MIST-CF) — https://arxiv.org/abs/2303.06470

## Examples

```
from mist_cf.embedding import SinusoidalFormulaEmbedding; emb = SinusoidalFormulaEmbedding(embedding_dim=256); formulas = ['C6H12O6', 'C3H7NO2', 'C8H10N4O2']; vectors = [emb.forward(f) for f in formulas]; import json; json.dump({'embeddings': [v.tolist() for v in vectors], 'dim': 256, 'min': min(v.min().item() for v in vectors), 'max': max(v.max().item() for v in vectors)}, open('embedding_validation.json', 'w'))
```

## Evaluation signals

- Embedding vector dimensionality equals the configured embedding_dim parameter for all inputs
- All embedding values fall within [-1, 1] range (or the specified numerical bounds for sinusoidal functions)
- L2 distance between produced and reference embeddings is < 1e-6, indicating reproducibility across runs or implementations
- No NaN or Inf values appear in the output embedding matrices
- Output file is well-formed and contains vectors for all input formulas with no missing entries

## Limitations

- Validation threshold (L2 distance < 1e-6) may be too strict for embeddings computed on hardware with lower floating-point precision (e.g., GPUs with different numerical libraries); adjust tolerance if cross-platform testing is required.
- Sinusoidal embeddings typically constrain output to [-1, 1], but this may not hold if the layer is modified or incorrectly configured; always verify the mathematical definition used in the implementation.
- Reproducibility check requires access to reference outputs, which may not be available for newly trained models or custom modifications; baseline comparison may fall back to sanity checks (dimensionality and range only).
- The skill validates embedding vectors in isolation; it does not confirm that embeddings are semantically meaningful or effective for downstream ranking tasks (e.g., formula-spectrum scoring in MIST-CF).

## Evidence

- [other] Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula: "Instantiate the sinusoidal embedding layer with its configured dimensionality and invoke the forward pass on each formula to produce embedding vectors."
- [other] Verify embedding vector dimensionality matches the configured embedding dimension parameter: "Verify embedding vector dimensionality matches the configured embedding dimension parameter."
- [other] Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings): "Verify all embedding values fall within the expected numerical range (typically [-1, 1] for sinusoidal embeddings)."
- [other] Compare produced embeddings against reference outputs using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility: "Compare produced embeddings against reference outputs from the MIST-CF repository using numerical tolerance (e.g., L2 distance < 1e-6) to confirm reproducibility."
- [other] Utilizing sinusoidal formula embeddings as developed in prior work (SCARF), as an advance to the chemical formula transformer architecture: "MIST-CF incorporates sinusoidal formula embeddings, a technique developed in prior work (SCARF), as an advance to the chemical formula transformer architecture for improved representation of chemical"
