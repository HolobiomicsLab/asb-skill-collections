---
name: wmy-network-prediction-confidence-scoring
description: Use when after initial lipid candidate annotation via spectral library
  matching (e.g., from XCMS/CAMERA peak alignment and LipidIN EQ module querying),
  when you need to improve coverage and annotation confidence on unannotated or low-confidence
  lipid signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - LipidIN EQ (Expeditious Querying) Module
  - WMY network (PyTorch)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Wide-spectrum Modeling Yield (WMY) Network Prediction with Confidence Scoring

## Summary

Apply the WMY neural network to regenerate lipid fingerprints from MS/MS spectra and assign confidence scores to enhanced lipid predictions, improving annotation recall by ~20% over baseline spectral library matching. This skill bridges initial spectral matching outputs into higher-confidence predictions by leveraging a deep learning model trained on fragmentation patterns.

## When to use

After initial lipid candidate annotation via spectral library matching (e.g., from XCMS/CAMERA peak alignment and LipidIN EQ module querying), when you need to improve coverage and annotation confidence on unannotated or low-confidence lipid signals. Specifically apply when baseline spectral matching yields incomplete or uncertain lipid identifications and you have access to MS/MS spectra and pre-trained WMY weights.

## When NOT to use

- Input spectra are already high-confidence, manually validated lipid identifications (WMY adds complexity without benefit).
- Pre-trained WMY weights are unavailable and training data (annotated fingerprints) cannot be assembled for your lipid class or ionization mode.
- Computational resources are severely constrained; WMY network inference is more costly than spectral matching alone.

## Inputs

- MS/MS spectra (m/z and intensity pairs from mzML format after preprocessing into .rda)
- Initial lipid annotations from spectral library matching (e.g., LipidIN EQ module output)
- Pre-trained WMY network weights (or training data: annotated lipid matrix and ground-truth fingerprint vector in CSV format)

## Outputs

- Regenerated lipid fingerprint predictions with per-prediction confidence scores
- Recall, precision, and coverage metrics comparing WMY vs. baseline annotations
- Quantified recall boost (%) relative to spectral-matching-only baseline

## How to apply

Load processed MS/MS spectra with initial annotations from spectral library matching. Input the annotated lipid candidates into the WMY network along with their MS/MS fragmentation patterns. Execute the WMY network (inspired by KAN and multi-head attention architectures) to regenerate lipid fingerprints, which produces enhanced predictions paired with confidence scores. The model operates independently of sample matrix and instrument type. Compare regenerated fingerprints against baseline spectral-matching-only annotations by computing recall, precision, and coverage metrics. Verify achievement of the ~20% recall boost threshold using the formula: (recall_WMY − recall_baseline) / recall_baseline × 100%.

## Related tools

- **XCMS** (Preprocesses raw MS data (mzML files) into peak-aligned, matched spectra ready for annotation)
- **CAMERA** (Performs initial compound spectral extraction and annotation upstream of WMY input)
- **LipidIN EQ (Expeditious Querying) Module** (Performs secondary matching with the 168.6 million lipid fragmentation hierarchical library to generate baseline candidate annotations input to WMY) — https://github.com/LinShuhaiLAB/LipidIN
- **WMY network (PyTorch)** (Core deep learning model that regenerates lipid fingerprints and assigns confidence scores) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
python predict.py --data_path <annotated_lipid_spectra.csv> --project_folder <pretrained_weights_dir> --mode pos
```

## Evaluation signals

- Recall improvement ≥ ~20% over baseline spectral-matching-only annotations, calculated as (recall_WMY − recall_baseline) / recall_baseline × 100%.
- Confidence scores are properly normalized and calibrated (e.g., 0–1 range, or empirically validated to correlate with prediction correctness).
- Regenerated fingerprints show improved precision and coverage metrics (increased number of correctly identified lipids, reduced false positives).
- Output CSV predictions include both regenerated fingerprint signatures and per-lipid confidence scores, allowing downstream filtering by confidence threshold.
- Performance is reproducible across multiple replicates and ionization modes (pos/neg, [M+H]+, [M+CH₃COO]−, [M+COOH]−) when applicable weights are used.

## Limitations

- WMY network performance is dependent on availability of pre-trained weights; if no pre-trained weights exist for a specific lipid class or ionization mode, training data (annotated fingerprint matrices and ground-truth vectors) must be assembled, which is labor-intensive.
- The ~20% recall boost is a reported estimate and may vary across different sample types, lipid classes, and MS instrument platforms; empirical validation on user data is required.
- WMY network operates on MS/MS fragmentation patterns independently of matrix and instrument, but performance has not been exhaustively validated across all lipid species or instrument types.
- Computational cost of WMY inference is higher than simple spectral matching; real-time or high-throughput analysis on very large datasets may require GPU acceleration (PyTorch with torch 1.13.1+cu116 recommended).
- No changelog or discussion section provided in repository to document known failure modes or edge cases (e.g., behavior on lipids with rare fragmentation patterns).

## Evidence

- [other] Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost in lipid annotation coverage and accuracy?: "Does applying the Wide-spectrum Modeling Yield (WMY) network to regenerate lipid fingerprints produce the reported ~20% estimated recall boost in lipid annotation coverage and accuracy?"
- [other] Execute the WMY network to regenerate lipid fingerprints, producing enhanced predictions with confidence scores. Compare regenerated fingerprints against baseline spectral-matching-only annotations to calculate recall, precision, and coverage metrics.: "Execute the WMY network to regenerate lipid fingerprints, producing enhanced predictions with confidence scores. Compare regenerated fingerprints against baseline spectral-matching-only annotations"
- [readme] Wide-spectrum Modeling Yield network for regenerating lipid fingerprints to further improve coverage and accuracy with a 20% estimated recall boosting: "Wide-spectrum Modeling Yield network for regenerating lipid fingerprints to further improve coverage and accuracy with a 20% estimated recall boosting"
- [readme] Reverse Lipid Fingerprint Spectrogram Module: WMYn predict lipid fingerprint spectrogram using the model we designed inspired by KAN and Muit-head attention.: "WMYn predict lipid fingerprint spectrogram using the model we designed inspired by KAN and Muit-head attention"
- [readme] Using the model to generate reverse lipid fingerprint spectrograms, independent of sample matrices, instruments.: "generate reverse lipid fingerprint spectrograms, independent of sample matrices, instruments"
- [readme] The input data include a matrix and a vector for training at least. For example AAA.csv(matrix) and AAA_GT.csv(vector).: "The input data include a matrix and a vector for training at least. For example AAA.csv(matrix) and AAA_GT.csv(vector)"
