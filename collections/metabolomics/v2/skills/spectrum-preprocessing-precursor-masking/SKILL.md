---
name: spectrum-preprocessing-precursor-masking
description: Use when when training a formula-prediction model with a frozen pretrained TCN spectrum encoder and unfrozen FormulaEncoder and RescoreHead components, or when you suspect the model may use precursor intensity as a spurious feature rather than fragment-pattern information for molecular formula.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - FIDDLE
  - msfiddle
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-preprocessing-precursor-masking

## Summary

Zero the precursor m/z channel in tandem MS/MS spectra before passing them to a frozen neural encoder to prevent the model from over-relying on the precursor ion intensity as a trivial prediction signal. This preprocessing step is critical in transfer-learning scenarios where the encoder is frozen and only downstream formula-prediction heads are trained.

## When to use

When training a formula-prediction model with a frozen pretrained TCN spectrum encoder and unfrozen FormulaEncoder and RescoreHead components, or when you suspect the model may use precursor intensity as a spurious feature rather than fragment-pattern information for molecular formula inference.

## When NOT to use

- When the TCN encoder is not frozen (i.e., all model parameters are jointly trainable); in this case, the encoder can learn to ignore precursor information on its own.
- When using a model architecture where precursor m/z is not represented as a separate input channel or is already ablated upstream.
- When the goal is to predict properties that legitimately depend on absolute precursor mass (e.g., molecular weight range filtering), rather than formula identity from fragmentation patterns alone.

## Inputs

- spectrum array (env) with shape [batch_size, num_channels] where channel 0 is the precursor m/z intensity
- pretrained TCN spectrum encoder (frozen, not trainable)
- FormulaEncoder module (trainable)
- RescoreHead module (trainable)
- binary cross-entropy loss function

## Outputs

- zeroed spectrum array with env[:,0] set to 0
- formula predictions from FormulaEncoder
- rescore confidence scores from RescoreHead
- formula_encoder_state_dict (saved checkpoint)
- rescore_head_state_dict (saved checkpoint)

## How to apply

Before passing the spectrum array (env) to the frozen TCN encoder during training, explicitly zero the precursor m/z channel at index 0 (env[:,0] = 0). This prevents information leakage from the known precursor mass into the encoder's learned representations. The zeroing step is applied uniformly to all training batches without exception. The frozen encoder then processes only fragment peaks, forcing the FormulaEncoder and RescoreHead to learn formula predictions from fragmentation patterns alone. Verify that the precursor channel remains zero throughout the forward pass and that no preprocessing step inadvertently restores or uses the original precursor intensity.

## Related tools

- **FIDDLE** (Deep learning method for molecular formula prediction from MS/MS spectra; the precursor masking step is part of its rescore model training pipeline) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package providing CLI and Python API for FIDDLE inference; uses frozen TCN encoder with precursor masking during internal training) — https://github.com/josiehong/msfiddle

## Examples

```
# In train_rescore.py: zero precursor m/z before frozen encoder
env[:, 0] = 0  # env is spectrum array [batch_size, num_channels]
encoder_output = frozen_tcn_encoder(env)  # frozen encoder processes masked spectra
formula_pred = formula_encoder(encoder_output)
rescore_score = rescore_head(formula_pred)
loss = binary_cross_entropy(rescore_score, target_labels)
loss.backward()  # backprop updates only FormulaEncoder and RescoreHead
```

## Evaluation signals

- Verify that env[:,0] is exactly 0.0 for all batch samples after the masking operation, before encoder forward pass
- Check that the frozen TCN encoder's parameters are not updated during backpropagation (no gradient flow into encoder)
- Confirm that formula_encoder_state_dict and rescore_head_state_dict are distinct keys in the saved checkpoint, indicating separate trainable components
- Monitor that binary cross-entropy loss converges on the training set despite precursor channel ablation, confirming the model learns from fragment peaks alone
- Compare model performance (Top-1/Top-5 formula accuracy) with and without precursor masking to demonstrate that masking prevents trivial precursor-intensity reliance

## Limitations

- Precursor masking assumes the precursor m/z is represented as a separate input channel at index 0; if the spectrum representation differs (e.g., precursor info encoded differently), this approach must be adapted.
- Masking the precursor channel may reduce model performance if fragmentation patterns alone are insufficient to disambiguate formulas; the trade-off between robustness and accuracy must be evaluated empirically.
- The zeroing step is applied statically (env[:,0] = 0) and does not account for variable precursor intensity distributions; if spectra have heterogeneous precursor SNR, a more adaptive masking strategy may be needed.
- This preprocessing step is specific to Siamese rescore architectures with frozen encoders; other model designs (e.g., end-to-end training) may not require or benefit from precursor masking.

## Evidence

- [other] Zero the precursor m/z channel (env[:,0]) before the encoder: "Zero the precursor m/z channel (env[:,0]) from the input spectrum array before passing to the frozen encoder."
- [other] Freeze TCN spectrum encoder while training FormulaEncoder and RescoreHead: "The training mechanism operates by freezing the TCN spectrum encoder, training FormulaEncoder and RescoreHead with BCE loss, zeroing the precursor m/z channel (env[:,0]) before the encoder"
- [other] Save formula_encoder_state_dict and rescore_head_state_dict separately: "Save formula_encoder_state_dict and rescore_head_state_dict as separate keys in the checkpoint dictionary."
- [readme] Rescore model redesigned with Siamese architecture in v2.0.0: "The rescore model has been redesigned (Siamese architecture)"
