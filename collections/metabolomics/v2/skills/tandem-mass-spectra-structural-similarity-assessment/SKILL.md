---
name: tandem-mass-spectra-structural-similarity-assessment
description: Use when you have pairs of cleaned tandem mass spectra with known chemical structure annotations (InChIKey, SMILES, or InChI), and you need to predict Tanimoto structural similarity scores directly from spectral data without pre-computing molecular fingerprints.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3676
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - matchms
  - PyTorch
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Using the t-SNE [28] implementation from scikit-learn [29] we computed two-dimensional coordinates
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tandem-mass-spectra structural similarity assessment

## Summary

Quantify structural similarity between pairs of MS/MS spectra using deep learning (MS2DeepScore) with optional uncertainty quantification via Monte-Carlo Dropout ensemble sampling and interquartile range (IQR) filtering to achieve calibrated RMSE predictions against reference Tanimoto scores.

## When to use

You have pairs of cleaned tandem mass spectra with known chemical structure annotations (InChIKey, SMILES, or InChI), and you need to predict Tanimoto structural similarity scores directly from spectral data without pre-computing molecular fingerprints. This is particularly useful when you seek RMSE ≤ 0.15 on large spectral datasets, or when you need to trade retrieval rate for higher accuracy by filtering on prediction uncertainty.

## When NOT to use

- Input spectra lack chemical structure annotations (InChIKey/SMILES/InChI); the reference Tanimoto labels cannot be computed.
- Input spectra have not undergone standard cleaning (peak filtering, intensity transformation, metadata harmonization); baseline RMSE will degrade.
- You require predictions on spectra from ionization modes or chemical families not well-represented in the pre-trained model's training data; retraining or domain adaptation may be necessary.
- Your goal is to rank spectral library matches by similarity without needing absolute Tanimoto scores; classical spectral similarity measures (e.g., cosine, neutral loss) may be faster and sufficient.

## Inputs

- Pairs of cleaned MS/MS spectra (matchms Spectrum objects or MGF/MSP/JSON files)
- Chemical structure annotations: InChIKey, SMILES, or InChI for both spectra in each pair
- Pre-trained MS2DeepScore Siamese neural network model (PyTorch .pt file)
- Test or validation dataset of spectrum pairs (3,000–3,600+ spectra recommended for stable RMSE estimates)

## Outputs

- Predicted structural similarity scores (0–1 range, median across ensemble or single forward pass)
- Prediction uncertainty estimates (IQR of ensemble predictions per pair)
- Filtered prediction set (subset of pairs meeting IQR threshold)
- RMSE against reference Tanimoto scores (overall and per-threshold)
- Retrieval rate curve (fraction of predictions retained vs. IQR threshold)
- Spectral embeddings (200-dimensional vectors for visualization or downstream clustering)

## How to apply

Load a pre-trained MS2DeepScore Siamese network (base network trained on 109,734+ annotated MS/MS spectra). For each spectrum pair, bin peaks into 10,000 equally-sized bins (10–1000 m/z range), square-root transform intensities, and remove peaks < 0.1% of maximum intensity. To obtain Tanimoto reference labels, compute RDKit Daylight fingerprints (2048 bits) for both spectra's InChI and calculate Tanimoto similarity. For uncertainty-aware predictions, enable dropout during inference and perform N=10 forward passes with dropout rate 0.2, computing cosine similarity of 200-dimensional embeddings for each pass. Calculate the median and interquartile range (IQR) across the 10 predictions per pair. Filter predictions by incrementally raising the IQR threshold (e.g., retaining only predictions with IQR ≤ 0.05, 0.10, 0.15) and compute RMSE against reference Tanimoto scores. Plot RMSE and retrieval rate versus IQR threshold to identify the threshold achieving target accuracy (e.g., RMSE ≈ 0.10 typically requires discarding ~75% of highest-uncertainty predictions).

## Related tools

- **MS2DeepScore** (Siamese neural network that predicts structural similarity scores (Tanimoto) directly from MS/MS spectrum pairs; trained end-to-end without intermediate fingerprint computation.) — https://github.com/matchms/ms2deepscore
- **matchms** (Handles spectrum data preparation, metadata cleaning, peak binning, and intensity transformation; provides Spectrum objects compatible with MS2DeepScore.) — https://github.com/matchms/matchms
- **RDKit** (Computes reference Tanimoto scores using Daylight fingerprints (2048 bits) from InChI/SMILES annotations for validation and ground-truth labels.)
- **PyTorch** (Deep learning framework underlying MS2DeepScore; enables Monte-Carlo Dropout ensemble inference by toggling dropout layers during prediction.)
- **scikit-learn** (Provides t-SNE dimensionality reduction for visualization of spectral embeddings in 2D space; used for exploratory analysis of learned chemical similarity landscape.)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(spectrum_pairs)
similarities = ms2ds.pair_predict(spectrum_pairs)
```

## Evaluation signals

- Achieved RMSE on test set matches reported range (~0.15 without uncertainty filtering; ~0.10–0.11 with IQR threshold filtering); systematic deviation suggests model degradation or data incompatibility.
- IQR values across the 10 ensemble members are non-zero (indicating genuine uncertainty) and show positive correlation with prediction error magnitude; constant IQR may indicate dropout not functioning correctly.
- Retrieval rate (fraction of predictions retained) decreases monotonically as IQR threshold tightens; non-monotonic behavior suggests ensemble computation or filtering logic error.
- Tanimoto reference scores computed from RDKit fingerprints fall within [0, 1] with reasonable distribution (not all near 0 or 1); pathological distributions indicate fingerprint or InChI parsing failures.
- Predicted median similarity scores lie within [0, 1] and correlate positively with reference Tanimoto (Pearson r or Spearman ρ > 0.6 typical); negative or near-zero correlation indicates model failure or label inversion.

## Limitations

- Baseline RMSE of ~0.15 means that without aggressive uncertainty filtering, ~15% standard deviation in predictions persists; high-precision applications may require additional post-hoc methods.
- Achieving RMSE ≈ 0.10 requires discarding ~75% of predictions, dramatically reducing throughput; the speed–accuracy trade-off is steep and dataset-dependent.
- Model was trained on spectra binned to 10,000 equally-sized m/z bins (10–1000 m/z); spectra outside this range or with anomalous mass calibration may yield unreliable predictions.
- Spectrum metadata (parent mass, elemental formula) were not used during training; prediction accuracy for spectra with unusual or ambiguous fragmentation patterns (e.g., highly complex natural products) is not characterized.
- Pre-trained model was trained on GNPS, METLIN, and MassBank spectra; chemical families or ionization modes underrepresented in these libraries may exhibit degraded performance.
- Monte-Carlo Dropout assumes dropout is applied to all but the first layer; if model architecture changes or dropout is disabled, uncertainty estimates become invalid.
- IQR-based filtering is heuristic; optimal threshold is data- and application-dependent and must be determined empirically for each new dataset.

## Evidence

- [other] Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty: "Monte-Carlo Dropout ensemble predictions with IQR-based filtering reduce average RMSE from ~0.17 to ~0.11 by discarding ~75% of predictions with highest uncertainty, demonstrating that strong"
- [other] For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings.: "For each spectrum pair, enable dropout during inference and generate N=10 forward passes through the network with dropout rate 0.2 to create an ensemble of 200-dimensional spectral embeddings."
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [intro] MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "MS2DeepScore achieves a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network"
- [results] The validation set (3597 spectra of 500 unique InChIKeys): "The validation set (3597 spectra of 500 unique InChIKeys)"
- [methods] Metadata was cleaned and checked using matchms version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields"
- [methods] by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks: "by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks"
- [readme] ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra.: "ms2deepscore provides a Siamese neural network that is trained to predict molecular structural similarities (Tanimoto scores) from pairs of mass spectrometry spectra."
- [readme] In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum.: "In addition to the prediction of a structural similarity, MS2DeepScore can also make use of an embedding evaluator predict the models accuracy for each spectrum."
