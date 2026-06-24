---
name: smiles-structure-annotation
description: Use when you have LC–QTOF mass spectra from real environmental or biological
  samples (e.g., wastewater, complex mixtures) and need to assign molecular structures
  to spectra where traditional library matching fails or reference compounds are unavailable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python 3.7
  - Torch
  - Python
  - MSGO
  - cfmid
  - PyTorch 1.7.1
  techniques:
  - LC-MS
  - NMR
  license_tier: open
derived_from:
- doi: 10.1038/s42256-025-01140-5
  title: MSGo
evidence_spans:
- 'Python: 3.7'
- 'Torch: 1.7.1'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msgo_cq
    doi: 10.1038/s42256-025-01140-5
    title: MSGo
  dedup_kept_from: coll_msgo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-025-01140-5
  all_source_dois:
  - 10.1038/s42256-025-01140-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES Structure Annotation

## Summary

Annotate mass spectra with predicted molecular structures as SMILES strings using a neural model trained on pseudo SMILES-spectrum pairs. This skill enables elucidation of unknown chemical structures in real LC–QTOF datasets, particularly for challenging compound classes like PFAS and lipids where reference libraries are incomplete.

## When to use

You have LC–QTOF mass spectra from real environmental or biological samples (e.g., wastewater, complex mixtures) and need to assign molecular structures to spectra where traditional library matching fails or reference compounds are unavailable. Use this skill when you want rapid, ranked predictions of plausible SMILES structures with confidence scores for downstream validation or hypothesis generation.

## When NOT to use

- Input spectra are already matched to reference compounds in a spectral library with high confidence; library lookup is faster and more reliable.
- Sample is known to contain only a narrowly defined chemical class (e.g., pharmaceuticals with existing in-silico prediction tools); class-specific methods may outperform the general MSGO model.
- Spectra are low quality, have poor signal-to-noise, or lack clear precursor ion signals; preprocessing or filtering should occur first.

## Inputs

- LC–QTOF mass spectra (CSV format with m/z, intensity, precursor m/z, ionization polarity)
- Pre-trained MSGO model weights (checkpoint directory containing pfas or lipid model)
- Beam size parameter (integer; 300–500 typical)

## Outputs

- CSV file with top-ranked SMILES predictions per spectrum
- Confidence scores or model probabilities for each SMILES candidate
- Ranked list of plausible molecular structures (typically top 10)

## How to apply

Load the pre-trained MSGO model checkpoint (pfas or lipid variant) and preprocess experimental spectra to match the model's expected input format (CSV with mass-to-charge, intensity, precursor m/z, and polarity). Run inference using eval_standard.py with a specified beam size (500 for PFAS, 300 for lipid) to generate top-ranked SMILES predictions and confidence scores for each spectrum. The model outputs a ranked list of predicted molecular structures; validate top predictions against reference compounds or literature annotations where available. Predictions flagged as low-confidence or novel should be prioritized for independent verification (e.g., synthesis, NMR, or targeted MS/MS).

## Related tools

- **MSGO** (Pre-trained neural model for predicting SMILES structures from mass spectra; loads checkpoint and performs inference to generate ranked molecular structure candidates.) — https://github.com/aaronma2020/MSGO
- **cfmid** (Generates pseudo SMILES-spectrum pairs used for training the MSGO model; supports in silico fragmentation for synthetic training data generation.)
- **Python 3.7** (Runtime environment for executing MSGO inference scripts (eval_standard.py).)
- **PyTorch 1.7.1** (Deep learning framework underlying the MSGO model; required for loading and running checkpoint inference.)

## Examples

```
python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg
```

## Evaluation signals

- Output CSV contains exactly as many rows as input spectra, with no missing or duplicate entries.
- Each spectrum prediction includes at least one valid SMILES string (must pass chemical syntax validation).
- Confidence scores are bounded and monotonically decreasing across ranked candidates (top prediction has highest score).
- For spectra with reference annotations available, top-ranked SMILES matches reference structure or a plausible structural isomer (manual verification or fingerprint similarity > 0.7).
- Runtime is consistent with beam size and model complexity; significant slowdowns may indicate memory or convergence issues in inference.

## Limitations

- Model performance is dependent on training set composition; PFAS and lipid models must be selected appropriately for the sample class. Predictions for out-of-domain compound classes (e.g., natural products if trained only on synthetic PFAS) may be unreliable.
- Predictions are ranked by model confidence, not chemical plausibility or biological relevance; high-scoring SMILES may still be incorrect or represent structural artifacts of the training data.
- Real spectra may contain adducts, fragments, or noise not well-represented in training data; manual inspection and orthogonal validation (e.g., NMR, exact mass tolerance checks) are essential for confident structure assignment.
- Model generates SMILES strings only; it does not provide fragmentation pathways, mechanism details, or explain how predictions were derived.

## Evidence

- [other] Can the MSGO model trained on pseudo SMILES-spectrum pairs successfully elucidate molecular structures in real wastewater samples from an LC–QTOF dataset?: "Can the MSGO model trained on pseudo SMILES-spectrum pairs successfully elucidate molecular structures in real wastewater samples from an LC–QTOF dataset?"
- [other] Preprocess the experimental spectra to match the input format expected by the model. 3. Perform inference using MSGO to generate predicted SMILES structures and corresponding confidence scores: "Preprocess the experimental spectra to match the input format expected by the model. 3. Perform inference using MSGO to generate predicted SMILES structures and corresponding confidence scores"
- [other] Collect and rank the predicted molecular structures by model confidence. 5. Validate predictions against reference compounds or literature annotations: "Collect and rank the predicted molecular structures by model confidence. 5. Validate predictions against reference compounds or literature annotations"
- [readme] For pfas, run : python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg: "python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg"
- [readme] Pseudodata-based molecular structure generator to reveal unknown chemicals: "Pseudodata-based molecular structure generator to reveal unknown chemicals"
- [readme] we use one LC–QTOF dataset for wastewater samples to verify our model: "we use one LC–QTOF dataset for wastewater samples to verify our model"
