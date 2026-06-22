---
name: model-weight-loading-and-deployment
description: Use when you have a pre-trained MSGO model checkpoint (PFAS or lipid variant) and need to evaluate it against a real mass spectrometry dataset (300+ real spectra, LC–QTOF, or custom CSV) to generate predicted molecular structures and compare against ground truth or baseline results.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - Python 3.7
  - Torch 1.7.1
  - Python
  - Torch
  - MSGO repository
  techniques:
  - mass-spectrometry
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

# model-weight-loading-and-deployment

## Summary

Load pre-trained deep learning model weights from a repository and deploy them for inference on new spectral data to generate molecular structure predictions. This skill enables reproducibility of published structure-generation performance without retraining.

## When to use

You have a pre-trained MSGO model checkpoint (PFAS or lipid variant) and need to evaluate it against a real mass spectrometry dataset (300+ real spectra, LC–QTOF, or custom CSV) to generate predicted molecular structures and compare against ground truth or baseline results.

## When NOT to use

- Model weights have not been downloaded or checkpoint path is invalid—training must be performed first using tools/train.py
- Input spectra are in non-standard formats (not CSV or incompatible with eval_standard.py schema)
- Evaluating on pseudo SMILES-spectrum pairs used for training—use the 300+ real spectrum validation set instead to assess generalization

## Inputs

- Pre-trained model checkpoint directory (ckpts/pfas or ckpts/lipid)
- Real mass spectrometry spectrum dataset (CSV format with spectrum features)
- Polarization mode specification (pos or neg)
- Beam search size parameter (integer, 300–500)

## Outputs

- Results CSV file with predicted SMILES structures
- Top-10 ranked predictions per spectrum with scores
- Inference time and structure-generation performance metrics

## How to apply

Load the released MSGO model weights from github.com/aaronma2020/MSGO using Python 3.7 and Torch 1.7.1 by specifying the checkpoint path (ckpts/pfas or ckpts/lipid). Prepare your input spectrum dataset as a CSV file compatible with the eval_standard.py evaluation script, specifying polarization mode (pos or neg) and beam search size (300–500 depending on model variant). Execute inference by calling tools/eval.py or tools/eval_standard.py with the model path and input CSV, collecting predicted SMILES structures ranked by beam search score. Verify correctness by confirming the output CSV includes top-10 predictions with associated confidence scores for each spectrum.

## Related tools

- **Python** (Runtime environment for model loading and inference)
- **Torch** (Deep learning framework for checkpoint deserialization and GPU-accelerated inference)
- **MSGO repository** (Source of pre-trained model weights and evaluation scripts (eval.py, eval_standard.py)) — github.com/aaronma2020/MSGO

## Examples

```
python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg
```

## Evaluation signals

- Model checkpoint successfully loads without Torch deserialization errors
- Output CSV contains exactly 10 ranked predictions per spectrum with monotonically decreasing beam search scores
- Predicted SMILES are valid and canonicalizable (no malformed SMILES strings)
- Structure-generation metrics (e.g., exact match rate on 300+ real spectra) match or closely reproduce the reported paper results
- Inference completes without CUDA out-of-memory or framework compatibility errors for the specified Python 3.7 and Torch 1.7.1 versions

## Limitations

- Model weights are specialized to PFAS or lipid chemical classes—deployment on spectra from other compound classes may yield poor predictions
- Evaluation requires exact Python 3.7 and Torch 1.7.1 versions; newer PyTorch releases may break checkpoint compatibility
- Pseudo SMILES-spectrum pairs used during training may introduce systematic bias in predicted structures; real-world validation datasets are recommended
- Beam search size (300–500) trades inference speed against coverage of candidate structures—smaller beam sizes may miss correct predictions

## Evidence

- [other] Load the pre-trained MSGO model weights from the released github.com/aaronma2020/MSGO repository using Python 3.7 and Torch 1.7.1.: "Load the pre-trained MSGO model weights from the released github.com/aaronma2020/MSGO repository using Python 3.7 and Torch 1.7.1."
- [readme] Download the model weights in ckpts/pfas or ckpts/lipid, run python tools/eval.py --log_path [ckpts/pfas or ckpts/lipid]: "Download the model weights in ckpts/pfas or ckpts/lipid, run
```
python tools/eval.py --log_path [ckpts/pfas or ckpts/lipid]
```"
- [other] Execute inference on each spectrum using the MSGO model to generate predicted molecular structures. Collect and format the structure-generation predictions and performance metrics into a results file.: "Execute inference on each spectrum using the MSGO model to generate predicted molecular structures. Collect and format the structure-generation predictions and performance metrics into a results file."
- [readme] Then you can obatin a results csv file inluding top 10 predicts.: "Then you can obatin a results csv file inluding top 10 predicts."
- [readme] For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid. For evaluation, we use 300+ real specturm to verify our method: "For Training, we use 30k+ pseudo smiles-specturm pairs generated by cfmid. For evaluation, we use 300+ real specturm to verify our method"
