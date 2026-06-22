---
name: molecular-structure-generation-evaluation
description: Use when you have access to pre-trained MSGO model weights (PFAS or lipid variants) and a set of 300+ real mass spectra (LC–QTOF or similar), and need to verify whether the model can generate correct molecular structures for unknown chemicals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Python 3.7
  - Torch 1.7.1
  - Python
  - Torch
  - MSGO (aaronma2020/MSGO)
  - cfmid
  techniques:
  - GC-MS
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

# Molecular Structure Generation Evaluation

## Summary

Evaluate a pre-trained molecular structure generation model (MSGO) on a real spectrum evaluation set to quantify its ability to predict unknown chemical structures from mass spectrometry data. This skill validates whether model weights trained on pseudo SMILES-spectrum pairs reproduce reported structure-generation performance on authentic experimental spectra.

## When to use

You have access to pre-trained MSGO model weights (PFAS or lipid variants) and a set of 300+ real mass spectra (LC–QTOF or similar), and need to verify whether the model can generate correct molecular structures for unknown chemicals. This is the standard evaluation pathway after training on pseudo data or when reproducing published results.

## When NOT to use

- Model has not been trained on pseudo SMILES-spectrum pairs using cfmid-generated data; use training workflow first.
- Input spectra are from a fundamentally different instrument or ionization mode (e.g., EI-MS, MALDI) than the model was trained on; MSGO is optimized for LC–QTOF data.
- You are evaluating a novel model variant or architecture; use the training workflow with custom parameters instead.

## Inputs

- Pre-trained MSGO model checkpoint (PyTorch .pt or directory)
- Real mass spectra dataset (CSV with columns: spectrum ID, m/z array, intensity array, precursor m/z, polarity)
- 300+ real spectrum evaluation set (LC–QTOF or equivalent)

## Outputs

- Results CSV file with predicted molecular structures (SMILES)
- Top-k predictions per spectrum with confidence/ranking
- Performance metrics (accuracy, structure-prediction statistics)
- Optional: matched or unmatched structure assignments for known chemical standards

## How to apply

Load the pre-trained MSGO model weights using Python 3.7 and Torch 1.7.1. Prepare the real spectrum evaluation dataset in the required CSV format (with m/z values, intensities, and metadata). Execute batch inference on each spectrum using the model's inference API (e.g., `eval_standard.py` for real data or `eval.py` for the 300+ benchmark set) with appropriate beam size (300–500 depending on analyte class: PFAS typically 500, lipids 300) and polarity setting. Collect predicted molecular structures (top-k predictions per spectrum) and compute performance metrics (e.g., top-1 accuracy, rank of correct structure if known). Validate that output CSV contains predicted SMILES, confidence scores, and rank positions for each query spectrum.

## Related tools

- **Python** (Runtime environment for loading model and executing inference)
- **Torch** (Deep learning framework (version 1.7.1) for model weight loading and GPU-accelerated inference)
- **MSGO (aaronma2020/MSGO)** (Repository hosting pre-trained model weights, evaluation scripts (eval.py, eval_standard.py), and example datasets) — github.com/aaronma2020/MSGO
- **cfmid** (Tool used to generate the 30k+ pseudo SMILES-spectrum pairs used during model training; underpins the pseudo data that evaluation reproduces against)

## Examples

```
python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg
```

## Evaluation signals

- Output CSV is well-formed with one row per spectrum, columns for spectrum ID, top-1 predicted SMILES, confidence scores, and rank of ground-truth structure (if available).
- Inference completes without runtime errors on all 300+ spectra using the specified Python 3.7 and Torch 1.7.1 environment.
- Top-1 and top-10 accuracy on the 300+ real spectrum benchmark match or exceed the reported values in the paper (exact thresholds vary by analyte class: PFAS vs. lipid).
- Predicted structures are valid SMILES strings and can be round-tripped through a cheminformatics library (e.g., RDKit) to recover valid molecular graphs.
- When ground-truth structures are known (e.g., wastewater LC–QTOF dataset), rank-1 or rank-k accuracy for known chemicals is above baseline random assignment.

## Limitations

- Model is specialized for LC–QTOF metabolomics data; performance on other instrument types or ionization modes (EI-MS, MALDI, GC-MS) is not guaranteed and may be substantially lower.
- Evaluation set size (300+ spectra) is modest; confidence intervals and per-class performance breakdowns may have high variance.
- No ground-truth molecular identities are provided for the 300+ benchmark set in the public release; absolute accuracy cannot be computed without manual curation or external databases.
- Pseudo SMILES-spectrum pairs used in training may not fully capture the chemical diversity or noise characteristics of real environmental or biological samples, limiting generalization.
- Beam search size (300–500) trades inference speed for completeness of the top-k predictions; smaller beam sizes may miss correct structures.

## Evidence

- [other] Can the released MSGO model weights reproduce the reported structure-generation performance when evaluated on the 300+ real spectrum evaluation set?: "Can the released MSGO model weights reproduce the reported structure-generation performance when evaluated on the 300+ real spectrum evaluation set?"
- [other] The MSGO model weights (PFAS and lipid variants) were trained using pseudo SMILES-spectrum pairs with the methods described in the paper and are provided for download to enable reproduction of evaluation results.: "The MSGO model weights (PFAS and lipid variants) were trained using pseudo SMILES-spectrum pairs with the methods described in the paper and are provided for download"
- [other] Load the pre-trained MSGO model weights from the released github.com/aaronma2020/MSGO repository using Python 3.7 and Torch 1.7.1.: "Load the pre-trained MSGO model weights from the released github.com/aaronma2020/MSGO repository using Python 3.7 and Torch 1.7.1"
- [other] Execute inference on each spectrum using the MSGO model to generate predicted molecular structures.: "Execute inference on each spectrum using the MSGO model to generate predicted molecular structures"
- [readme] For evaluation, we use 300+ real specturm to verify our method: "For evaluation, we use 300+ real specturm to verify our method"
- [readme] Download the model weights in ckpts/pfas or ckpts/lipid, run python tools/eval.py --log_path [ckpts/pfas or ckpts/lipid]: "Download the model weights in ckpts/pfas or ckpts/lipid, run python tools/eval.py --log_path [ckpts/pfas or ckpts/lipid]"
- [readme] For pfas, run: python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg: "python tools/eval_standard.py --log_path ckpts/pfas --real_csv ./data/example/pfas.csv --out_csv ./pfas_results.csv --beam_size 500 --polar neg"
- [readme] For evaluation in real samples，we use one LC–QTOF dataset for wastewater samples to verify our model: "For evaluation in real samples，we use one LC–QTOF dataset for wastewater samples to verify our model"
- [other] Collect and format the structure-generation predictions and performance metrics into a results file.: "Collect and format the structure-generation predictions and performance metrics into a results file"
