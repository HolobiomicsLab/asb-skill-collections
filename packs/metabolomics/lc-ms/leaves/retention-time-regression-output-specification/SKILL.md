---
name: retention-time-regression-output-specification
description: Use when after initializing and executing a forward pass through a dual-branch
  RT-Transformer model (combining fingerprint and molecular graph inputs) on a batch
  of molecular samples, to verify that the output tensor conforms to the expected
  shape, data type, and numeric range for retention time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - torch
  - torch-scatter
  - torch-sparse
  - torch-cluster
  - torch_geometric
  - rdkit-pypi
  - RT-Transformer reference implementation
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btae084
  title: RT-Transformer
- doi: 10.1038/s41467-019-13680-7
  title: ''
evidence_spans:
- Python 3.9
- torch
- torch-scatter
- torch-sparse
- torch-cluster
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rt_transformer_cq
    doi: 10.1093/bioinformatics/btae084
    title: RT-Transformer
  dedup_kept_from: coll_rt_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btae084
  all_source_dois:
  - 10.1093/bioinformatics/btae084
  - 10.1038/s41467-019-13680-7
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-regression-output-specification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Specification of the scalar regression output tensor produced by the RT-Transformer dual-branch architecture when predicting liquid chromatography retention times for metabolites. This skill ensures the model's forward pass produces valid, correctly-shaped retention time predictions suitable for downstream validation and transfer learning workflows.

## When to use

After initializing and executing a forward pass through a dual-branch RT-Transformer model (combining fingerprint and molecular graph inputs) on a batch of molecular samples, to verify that the output tensor conforms to the expected shape, data type, and numeric range for retention time predictions before proceeding to loss computation, validation, or model deployment.

## When NOT to use

- Input fingerprint or graph data have not been normalized or validated (spec does not handle upstream data quality; verify inputs first)
- Model has not been instantiated with both fingerprint processing and graph neural network branches fully connected (incomplete architecture)
- Output predictions are already aggregated, averaged, or post-processed into a different shape (spec defines immediate raw model output only)

## Inputs

- Molecular fingerprint tensor (typically 2D array of shape [batch_size, fingerprint_dim] from RDKit)
- torch_geometric Batch object containing molecular graph representations (node features, edge indices, batch indices)
- Initialized RT-Transformer PyTorch model in forward-evaluation mode

## Outputs

- Output tensor of shape [batch_size, 1] with dtype float32 containing scalar retention time predictions
- Validation status (pass/fail) confirming output conforms to expected schema and numeric validity

## How to apply

Execute the RT-Transformer forward pass on a batch containing fingerprint tensors (from RDKit feature extraction) and torch_geometric Graph objects. Verify the output tensor has shape [batch_size, 1] and dtype float32 or compatible numeric type. Confirm all output values are scalar numeric predictions (not NaN or infinite). The output should represent predicted retention times in the same units as the training target (typically minutes or seconds depending on the chromatographic protocol used in the SMRT or PredRet datasets). Check that predictions fall within a plausible range relative to the training data distribution (e.g., positive values for retention time in standard LC–MS workflows). This validation step must complete without shape errors or type mismatches before feeding outputs to loss functions or evaluation metrics.

## Related tools

- **torch** (PyTorch tensor framework used to instantiate the RT-Transformer model, execute forward pass, and validate output tensor shape and dtype)
- **torch_geometric** (Library for molecular graph construction (Graph objects with node/edge features) and graph neural network branch that processes graph inputs and fuses with fingerprint embeddings)
- **rdkit-pypi** (Generates molecular fingerprints (input to fingerprint processing branch) from SMILES or InChI molecular representations)
- **RT-Transformer reference implementation** (Reference architecture and training scripts defining the dual-branch model topology, fusion layer, and regression head that produces the specified output tensor) — https://github.com/01dadada/RT-Transformer

## Examples

```
import torch; from model import RTTransformer; model = RTTransformer(); fingerprints = torch.randn(32, 2048); graphs = construct_batch(smiles_list); output = model(fingerprints, graphs); assert output.shape == (32, 1) and output.dtype == torch.float32
```

## Evaluation signals

- Output tensor shape must exactly equal [batch_size, 1] with no extraneous dimensions or flattening artifacts
- All output values must be numeric (float32 or compatible) with no NaN, infinity, or null values
- Output predictions must be non-negative and fall within a plausible retention time range (e.g., 0–120 minutes for typical LC–MS protocols using SMRT/PredRet datasets)
- Forward pass must complete without shape mismatch errors, dtype casting warnings, or gradient computation issues when model is in evaluation mode
- Output must be independent of batch size (i.e., changing batch_size should produce output shape [new_batch_size, 1] without error)

## Limitations

- Output specification assumes both fingerprint and graph inputs are correctly formatted and present; mismatched or missing modalities will cause shape errors upstream of the regression head
- Retention time predictions reflect the chromatographic conditions and chemical space of the training dataset (SMRT or PredRet); transfer to substantially different LC methods may require fine-tuning and output range adjustment
- Scalar predictions provide point estimates only; no uncertainty quantification (e.g., confidence intervals) is produced by this output specification
- Output tensor dtype depends on model initialization precision (float32 vs. float64); consistency with loss function and downstream metrics must be verified separately

## Evidence

- [other] The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch, with both inputs processed to produce a retention time prediction as output.: "The RT-Transformer model uses a dual-branch architecture that accepts fingerprint data from one branch and molecular graph data from another branch, with both inputs processed to produce a retention"
- [other] Validation: confirm model runs forward pass without errors and produces output tensor of shape [batch_size, 1] with numeric predictions.: "Validation: confirm model runs forward pass without errors and produces output tensor of shape [batch_size, 1] with numeric predictions."
- [other] Implement the regression head that outputs scalar retention time predictions.: "Implement the regression head that outputs scalar retention time predictions."
- [readme] The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output.: "The RT-Tranformer combine the fingerprint and the molecular graph data and predict retention time as the output."
- [other] Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects.: "Load molecular fingerprints (from RDKit feature extraction) and construct molecular graph representations using torch_geometric Graph objects."
