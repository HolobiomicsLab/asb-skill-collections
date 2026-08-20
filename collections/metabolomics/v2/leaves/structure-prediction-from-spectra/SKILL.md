---
name: structure-prediction-from-spectra
description: Use when you have experimental mass spectrometry spectra (LC–QTOF or
  similar format) from unknown compounds and need to predict their molecular structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - Python 3.7
  - Torch
  - Python
  - Torch 1.7.1
  - MSGO
  - PyTorch
  - cfmid
  techniques:
  - LC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
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

# structure-prediction-from-spectra

## Summary

Use a pre-trained deep learning model (MSGO) to predict molecular structures from mass spectrometry spectra by performing inference on preprocessed experimental spectra and ranking predicted SMILES structures by model confidence. This skill enables elucidation of unknown chemical structures in real-world samples, including wastewater, without relying on spectral libraries.

## When to use

You have experimental mass spectrometry spectra (LC–QTOF or similar format) from unknown compounds and need to predict their molecular structures. This is particularly useful when reference library matches are unavailable, when dealing with novel or modified compounds, or when validating structure assignments in complex environmental or biological samples. The MSGO model is specialized for PFAS and lipid compound classes.

## When NOT to use

- Input spectra are from compound classes not covered by the model training (MSGO is specialized for PFAS and lipids; other chemical classes may have poor predictive performance)
- Experimental spectra have not been preprocessed or normalized to match the model's expected input format (e.g., incorrect mass calibration or intensity normalization)
- The goal is to identify known compounds using spectral library matching rather than predict structures of unknown compounds

## Inputs

- Pre-trained MSGO model weights (checkpoint files for PFAS or lipid variants)
- LC–QTOF mass spectrometry spectra in CSV format with precursor m/z and fragmentation data
- Experimental spectrum dataset (real samples from wastewater or other matrices)
- Polarity setting (positive or negative ion mode)

## Outputs

- CSV file containing ranked predicted molecular structures (top 10 SMILES per spectrum)
- Model confidence scores for each prediction
- Validated structure assignments or flagged novel structure predictions for experimental confirmation

## How to apply

Load the pre-trained MSGO model weights (PFAS or lipid variant) using PyTorch 1.7.1 and Python 3.7. Preprocess experimental spectra to match the input format expected by the model (polar mode and beam_size parameters should match the compound class: beam_size 500 for PFAS, 300 for lipids). Execute inference on each spectrum using the model to generate predicted SMILES structures and confidence scores. Collect and rank predictions by model confidence, typically retaining the top 10 predictions. Validate predictions against reference compounds or literature annotations where available; flag novel structure predictions for further verification through orthogonal methods.

## Related tools

- **MSGO** (Pre-trained deep learning model for molecular structure generation from mass spectra; provides model weights and inference engine for PFAS and lipid variants) — https://github.com/aaronma2020/MSGO
- **PyTorch** (Deep learning framework used to load and run inference with the pre-trained MSGO model weights)
- **Python 3.7** (Scripting language environment for executing model inference, data preprocessing, and result collection)
- **cfmid** (Used during model training to generate the 30k+ pseudo SMILES-spectrum pairs; not directly used during inference but understanding its role clarifies training data provenance)

## Examples

```
python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg
```

## Evaluation signals

- Predicted SMILES strings are valid chemical structures (parseable by chemistry libraries and chemically sensible)
- Model confidence scores are within expected range (0–1) and rank predictions consistently across the dataset
- Top-ranked predictions can be validated against reference compound annotations or literature when available; match rate or rank-1 accuracy reported
- Predictions for real wastewater samples align with expected chemical properties (e.g., PFAS predictions contain fluorine; lipid predictions contain fatty acid chains)
- Output CSV file contains exactly 10 predictions per spectrum with corresponding confidence scores; no missing or null entries for processed spectra

## Limitations

- Model performance is specialized to PFAS and lipid compound classes; generalization to other chemical classes is not demonstrated
- Predictions are based on pseudo SMILES-spectrum pairs generated by cfmid during training; model may inherit biases or artifacts from synthetic training data
- Predictions must be validated against reference compounds or experimental confirmation (NMR, MS/MS fragmentation patterns) because the model confidence score reflects only in-distribution certainty, not chemical plausibility
- Real-sample evaluation was conducted on one LC–QTOF wastewater dataset; generalization to other LC–QTOF instruments, ionization methods, or sample matrices is not explicitly validated
- The model requires precise preprocessing of input spectra (polarity, mass calibration, format); mismatches between input and training data format may degrade prediction quality

## Evidence

- [other] Can the MSGO model trained on pseudo SMILES-spectrum pairs successfully elucidate molecular structures in real wastewater samples from an LC–QTOF dataset?: "Can the MSGO model trained on pseudo SMILES-spectrum pairs successfully elucidate molecular structures in real wastewater samples from an LC–QTOF dataset?"
- [other] Preprocess the experimental spectra to match the input format expected by the model. 3. Perform inference using MSGO to generate predicted SMILES structures and corresponding confidence scores for each spectrum. 4. Collect and rank the predicted molecular structures by model confidence.: "Preprocess the experimental spectra to match the input format expected by the model. 3. Perform inference using MSGO to generate predicted SMILES structures and corresponding confidence scores for"
- [readme] For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid: "For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid"
- [readme] For evaluation in real samples，we use one LC–QTOF dataset for wastewater samples to verify our model: "For evaluation in real samples，we use one LC–QTOF dataset for wastewater samples to verify our model"
- [readme] For pfas, run : python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg: "python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg"
- [other] The MSGO model weights (PFAS and lipid variants) were trained using pseudo SMILES-spectrum pairs with the methods described in the paper: "The MSGO model weights (PFAS and lipid variants) were trained using pseudo SMILES-spectrum pairs with the methods described in the paper"
