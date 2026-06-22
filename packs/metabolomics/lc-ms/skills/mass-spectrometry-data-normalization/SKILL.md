---
name: mass-spectrometry-data-normalization
description: Use when when raw MS/MS spectra from GNPS or similar databases contain variable-scale peak intensities, missing metadata, or inconsistent m/z calibration, and you intend to feed peak information into a transformer-based spectral embedding model that expects normalized, fixed-length tensor inputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - pandas
  - scikit-learn
  - numpy
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c00260
  title: CLERMS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_clerms_cq
    doi: 10.1021/acs.analchem.3c00260
    title: CLERMS
  dedup_kept_from: coll_clerms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00260
  all_source_dois:
  - 10.1021/acs.analchem.3c00260
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-data-normalization

## Summary

Normalization of MS/MS peak intensity and m/z information to prepare raw spectra for transformer-based embedding and contrastive learning. This step removes inaccurate or incomplete records and scales peak data into a fixed numerical range suitable for sinusoidal encoding and downstream model input.

## When to use

When raw MS/MS spectra from GNPS or similar databases contain variable-scale peak intensities, missing metadata, or inconsistent m/z calibration, and you intend to feed peak information into a transformer-based spectral embedding model that expects normalized, fixed-length tensor inputs.

## When NOT to use

- Input spectra are already preprocessed by the instrument vendor or a prior pipeline and documented as normalized.
- Your analysis goal does not involve transformer or contrastive learning; classical spectral matching or database search may not require uniform normalization.
- Peak data is already encoded as fixed-length feature vectors or embeddings; re-normalization risks losing learned structure.

## Inputs

- raw MS/MS spectra dataset (GNPS or equivalent format)
- m/z array per spectrum (variable length)
- intensity array per spectrum (variable length)
- spectrum metadata (compound ID, source annotation)

## Outputs

- cleaned and filtered spectra dataset
- normalized m/z arrays (fixed range, e.g. [0, 1])
- normalized intensity arrays (fixed range, e.g. [0, 1])
- data quality report (number of records removed, statistics on retained spectra)

## How to apply

Load raw spectra data (m/z arrays and intensity values per spectrum). Filter records with inaccurate or missing peak information to remove noise and ensure data quality. Normalize m/z and intensity values to a consistent numerical range (typically [0, 1] or standardized z-score) so that sinusoidal basis functions encode them uniformly across frequency scales. Apply this normalization uniformly across all spectra in the dataset before passing peaks to the embedder module. Validation involves confirming that normalized intensities fall within the expected range and that all spectra retain at least a minimum number of valid peaks.

## Related tools

- **matchms** (Spectrum I/O and metadata extraction for GNPS and other MS/MS data formats)
- **pandas** (Tabular data manipulation and filtering of spectra records)
- **scikit-learn** (StandardScaler or MinMaxScaler for m/z and intensity normalization)
- **numpy** (Efficient numerical operations on peak arrays during normalization)

## Examples

```
# Run dataset_preprocessing.ipynb as instructed in the README to normalize peak information for model input; the notebook handles record filtering and normalization before downstream embedding and training steps.
```

## Evaluation signals

- All normalized m/z and intensity values fall within the expected range (e.g., [0, 1] or [-1, 1]).
- Spectra with missing or null peak information are correctly identified and removed; record count before and after filtering is logged.
- Normalized peaks preserve relative intensity order and m/z separation (no rank inversions after scaling).
- Variable-length peak lists are handled consistently; no crashes or silent truncation occur during batch processing.
- Deterministic output: running normalization twice on the same input produces identical normalized arrays (no randomness in scaling).

## Limitations

- Records with inaccurate or incomplete peak data are removed entirely; this may reduce dataset size significantly if data quality is poor.
- Normalization range and method (min-max, z-score, etc.) must be chosen a priori and applied uniformly; mismatched choices between training and inference degrade model performance.
- Very low-intensity peaks may be lost or collapsed to near-zero after normalization, reducing information content for rare or weak spectral features.
- The README does not specify handling of isotope peaks, neutral loss patterns, or other MS/MS-specific structure; generic normalization may not preserve biochemically meaningful relationships.

## Evidence

- [readme] Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for the model input.: "Some of the records in the spectra data contain inaccurate data or some of the information is missing. So, we remove them from the input data. Also, the peak information needs to be normalized for"
- [intro] Extract embeddings from peak information and metadata: "Extract embeddings from peak information and metadata"
- [readme] Model architecture equipped with a sinusoidal embedder and a novel loss function composed of InfoNCE loss and MSE loss has been proposed for the obtaining of good embedding from the peak information and the metadata.: "obtaining of good embedding from the peak information and the metadata"
- [readme] The GNPS data set can be obtained from https://zenodo.org/record/5186176, and should be put to the directory `data`.: "The GNPS data set can be obtained from https://zenodo.org/record/5186176"
