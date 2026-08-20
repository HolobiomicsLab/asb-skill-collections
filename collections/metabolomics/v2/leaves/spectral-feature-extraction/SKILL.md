---
name: spectral-feature-extraction
description: Use when you have raw mass-spectrometry data (precursor m/z, ionization
  mode, and fragment m/z–intensity pairs) and need to feed it into a CNN-based metabolite
  annotation pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_0602
  tools:
  - TensorFlow
  - PyTorch
  - scikit-learn
  - PyFingerprint
  - Open Babel 3.1.1
  - PubChemPy 1.0.4
  - Python 3.11.7
  - subformula_assign.py
  - data_preprocess.py
  - rdkit
  - PyTorch Geometric
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-020-01726-7
  title: MetFID
- doi: 10.1101/2025.11.12.688047v1
  title: ''
evidence_spans:
- No usage/docs found.
- 'python_version: 3.11.7'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metfid_cq
    doi: 10.1007/s11306-020-01726-7
    title: MetFID
  - build: coll_mvp_cq
    doi: 10.1101/2025.11.12.688047v1
    title: MVP
  dedup_kept_from: coll_metfid_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01726-7
  all_source_dois:
  - 10.1007/s11306-020-01726-7
  - 10.1101/2025.11.12.688047v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-feature-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and normalize mass-spectrometry spectral features (m/z and intensity pairs) into a tensor format suitable for CNN input in metabolite fingerprint prediction. This skill bridges raw MS data and deep learning by standardizing fragmentation patterns into feature vectors that preserve chemical information.

## When to use

Apply this skill when you have raw mass-spectrometry data (precursor m/z, ionization mode, and fragment m/z–intensity pairs) and need to feed it into a CNN-based metabolite annotation pipeline. Use it specifically when preparing MS spectra for compound fingerprint prediction via learned feature representations rather than template matching or library search.

## When NOT to use

- Input is already a pre-computed molecular fingerprint or structural descriptor (e.g., ECFP, RDKit hash) — skip to similarity scoring.
- Mass spectra lack intensity information or contain only nominal m/z values without quantitative fragmentation data — insufficient for CNN feature learning.
- Spectra are from gas chromatography–mass spectrometry (GC–MS) with extreme m/z ranges or highly non-standard ionization (not positive or negative ESI/EI) — may require domain-specific preprocessing not covered by this skill.

## Inputs

- mass-spectrometry spectrum file (e.g., testing_compound.txt format with precursor m/z, ionization mode, and m/z–intensity pairs)
- precursor mass (float, in Daltons)
- ionization mode (string: 'positive' or 'negative')
- fragment m/z values (array of floats)
- fragment intensities (array of floats, arbitrary units)

## Outputs

- normalized spectral feature matrix (2D array or 1D vector compatible with CNN input layer)
- intensity-normalized m/z–intensity pairs (0–100 or 0–1 scale)
- metadata tuple (precursor m/z, ionization mode, spectrum ID)

## How to apply

Parse MS input data into m/z and intensity arrays, recording precursor mass and ionization mode (positive or negative). Normalize intensity values (typically to 0–100 or 0–1 range) to ensure scale invariance across spectra of different dynamic ranges. Arrange normalized pairs into a 2D matrix or 1D concatenated vector format compatible with the CNN input layer shape (e.g., flattened or gridded by m/z bins). The MetFID implementation uses this spectral matrix to map local and global fragmentation patterns through convolutional layers to predict molecular fingerprint bits. Validate that feature extraction preserves rank-order intensity relationships and that no spectral information (especially high-intensity fragments) is lost in quantization.

## Related tools

- **PyFingerprint** (generates reference molecular fingerprints from InChIKey for comparison and loss computation during CNN training) — https://github.com/hcji/PyFingerprint
- **TensorFlow** (defines CNN architecture and processes batched spectral feature tensors through convolutional and dense layers) — https://www.tensorflow.org/
- **Open Babel 3.1.1** (converts chemical identifiers (InChIKey, SMILES) to and from molecular structures for fingerprint validation) — https://openbabel.org/wiki/Python
- **PubChemPy 1.0.4** (retrieves reference molecular fingerprints and compound metadata from PubChem for training ground truth) — https://pubchempy.readthedocs.io/en/latest/guide/install.html

## Examples

```
# Parse and normalize spectrum from testing_compound.txt; example command:
python3 -c "import numpy as np; spectrum = np.array([[58.0653, 0.1393717711334875], [70.0652, 0.5051454118468733], [201.0465, 100.0]]); normalized = spectrum.copy(); normalized[:, 1] /= normalized[:, 1].max() * 100; print(normalized)"
```

## Evaluation signals

- Normalized intensities fall within expected range (0–100 or 0–1); verify max intensity equals 100 or 1.0 per spectrum.
- Feature matrix shape matches CNN input layer specification (e.g., (n_spectra, height, width, 1) for 2D convolution); check tensor dimensions with model.input_shape.
- Precursor m/z and ionization mode are correctly paired with spectral features; spot-check first and last rows of input file against parsed metadata.
- Rank order of fragment intensities is preserved after normalization (highest intensity fragment remains highest); verify via argsort comparison.
- No NaN, Inf, or out-of-range values in feature matrix; apply numpy.isfinite() and value range checks before training.

## Limitations

- Spectral preprocessing assumes positive or negative ionization mode; other modes (e.g., MALDI, APCI variants) may require separate preprocessing or mode-agnostic normalization.
- Intensity normalization to 0–100 scale discards absolute quantitative information (e.g., total ion current); relative fragmentation patterns are preserved but absolute abundances are lost.
- No handling of isotope patterns or adduct features explicitly mentioned in the README; isotopic fine structure may be averaged or binned into m/z grid, reducing resolution.
- Input file format requires strict block structure (#digit separator); mismatched counters between testing_compound.txt and inchikey_list.txt cause runtime errors.
- CNN input shape is fixed after model training; spectra with very high (m/z > 1000) or very low (m/z < 50) fragment ions may require dataset-specific re-binning or interpolation.

## Evidence

- [other] Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer.: "Load or construct mass-spectrometry input data (m/z and intensity arrays or spectral matrices) in a format compatible with the CNN input layer."
- [readme] The first row represents the precursor mass and ionization mode, followed by intensity pairs.: "The first row represents the precursor mass and ionization mode, followed by intensity pairs."
- [other] MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation.: "MetFID implements a CNN-based approach for predicting compound fingerprints from mass-spectrometry data, serving as the core predictor component for metabolite annotation."
- [readme] The second column represents the Tanimoto similarity score. Each table will be ranked in a descending order by score.: "The second column represents the Tanimoto similarity score. Each table will be ranked in a descending order by score."
- [other] Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance.: "Train the CNN model using a suitable loss function (e.g., binary cross-entropy for fingerprint bits or Tanimoto-based loss) and optimizer, monitoring validation performance."
