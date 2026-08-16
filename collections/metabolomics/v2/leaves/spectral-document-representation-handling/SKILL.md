---
name: spectral-document-representation-handling
description: Use when you have per-sample MS2 spectra (in matchms-compatible formats
  like mzML, mzXML, MGF, or msp) and need to compare metabolomic samples across different
  LC methods, mass spectrometers, or retention-time regimes—especially when samples
  are chemodiverse with poor feature overlap or strong RT.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - spec2vec
  - numpy
  - Python
  - MEMO
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra and converting them into documents.
- pip install numpy
- conda create --name memo python=3.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-document-representation-handling

## Summary

Convert MS2 spectra into machine-learning-ready vector representations (document embeddings) that capture fragment and neutral loss relationships, enabling downstream cross-sample comparison and alignment without explicit feature engineering. This skill bridges raw spectral data and matrix-based sample-level analysis by treating spectra as semantic documents.

## When to use

You have per-sample MS2 spectra (in matchms-compatible formats like mzML, mzXML, MGF, or msp) and need to compare metabolomic samples across different LC methods, mass spectrometers, or retention-time regimes—especially when samples are chemodiverse with poor feature overlap or strong RT drift. Use this skill when you want to create a single comparable matrix of samples rather than aligning individual feature peaks.

## When NOT to use

- Input spectra are already aligned at the feature level (e.g., a pre-built peak intensity matrix)—use this skill only when starting from raw MS2 spectra.
- Your goal is to identify individual compound metabolites with high mass accuracy; this skill is retention-time agnostic and loses temporal information, making it unsuitable for targeted metabolite detection.
- Samples have minimal MS2 fragmentation or very few spectra per sample; the fingerprint counting approach requires sufficient spectral diversity within each sample to generate meaningful vectors.

## Inputs

- Per-sample MS2 spectra (mzML, mzXML, MGF, msp, or JSON format)
- Matched spectra objects (matchms Spectrum class instances)
- Sample identifiers or metadata associating spectra to samples

## Outputs

- Per-sample MS2 fingerprints (counted occurrence vectors of peaks and neutral losses)
- MemoMatrix: unified numpy array with samples as rows and MS2 features (peaks + losses) as aligned columns
- Feature alignment metadata (list of MS2 m/z and loss values in consistent column order)

## How to apply

Load per-sample MS2 spectra using matchms (supporting mzML, mzXML, MGF, msp, JSON formats). Apply spec2vec document representation to convert each spectrum into a fixed-dimensional embedding that encodes the learned relationships between MS2 peaks and neutral losses. For each sample, aggregate (count occurrences of) all MS2 peaks and neutral losses across its constituent spectra to generate a fingerprint vector. Stack these per-sample fingerprint vectors into a unified numpy array, ensuring consistent feature alignment and dimensionality across all samples. Validate that the resulting matrix has identical feature columns across all samples (e.g., same set of m/z and loss features), confirming readiness for downstream sample-level filtering and visualization (MDS/PCoA, TMAP, heatmap).

## Related tools

- **matchms** (Load, parse, and preprocess MS2 spectra from standard mass spectrometry file formats into Spectrum objects; clean and normalize spectral metadata.) — https://github.com/matchms/matchms
- **spec2vec** (Learn spectral embeddings from MS2 peak and neutral loss relationships; convert individual spectra into fixed-dimensional document representations.) — https://github.com/iomega/spec2vec
- **numpy** (Aggregate fingerprint vectors and construct the unified MemoMatrix with consistent feature alignment across samples.)
- **MEMO** (High-level framework integrating matchms and spec2vec for retention-time-agnostic sample-level comparison via MS2 fingerprint matrices.) — https://github.com/mandelbrot-project/memo

## Examples

```
from matchms.importing import load_from_json
from spec2vec import Spec2Vec
import numpy as np

spectra = load_from_json('samples.json')
model = Spec2Vec.load_pretrained()
vectors = [model.pair_to_vector(s, s) for s in spectra]
matrix = np.array(vectors)
print(matrix.shape)
```

## Evaluation signals

- Matrix dimensions are (n_samples, n_features) where all samples have identical feature column sets and no NaN or inconsistent alignment across rows.
- Each sample's fingerprint vector is non-zero and contains only non-negative integer counts or valid occurrence frequencies (no negative or extreme outlier values).
- Spot-check a subset of samples: verify that high-abundance m/z or neutral loss values in the fingerprint correspond to peaks actually present in the underlying per-sample MS2 spectra.
- Cross-sample feature consistency: confirm that the same m/z or loss feature appears in the same column index for all samples (no feature-reordering between samples).
- Downstream visualization (MDS/PCoA or TMAP) reveals expected sample clustering or separation—e.g., biological replicates cluster together, or known treatment groups separate—indicating the fingerprints captured meaningful sample-level variation.

## Limitations

- Retention time information is discarded; samples acquired on different LC timescales or instruments cannot be aligned by chromatographic order alone.
- Low-abundance or rare MS2 features may be underrepresented or noise-dominated, especially in samples with few spectra; results depend on depth and quality of MS2 data per sample.
- Poor feature overlap between chemodiverse samples is a motivation for the method, but extreme chemical divergence may still result in sparse matrices with limited cross-sample comparability.
- The method is agnostic to instrument calibration and mass accuracy; incorrect or uncalibrated m/z values will produce inconsistent feature alignment across samples.
- TMAP visualization (one of the recommended downstream steps) is only available on MacOS and Linux, not Windows (without WSL).

## Evidence

- [other] MS2 fingerprints are generated by counting occurrences of MS2 peaks and neutral losses in each sample, and these fingerprints are then aligned in a second stage to compare different samples.: "MS2 fingerprints are generated by counting occurrences of MS2 peaks and neutral losses in each sample, and these fingerprints are then aligned in a second stage to compare different samples."
- [other] Load per-sample MS2 fingerprints from matchms-processed spectra using spec2vec document representations, then aggregate into a unified matrix using numpy array operations.: "Load per-sample MS2 fingerprints (each generated by counting occurrences of MS2 peaks and neutral losses to the precursor) from matchms-processed spectra using spec2vec document representations."
- [readme] Spec2vec learns relationships between mass fragments and neutral losses in MS/MS spectra, enabling semantic document embeddings.: "spec2vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships"
- [readme] Matchms supports multiple spectral data formats and enables reproducible MS/MS analysis pipelines.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON."
- [readme] MEMO is retention-time agnostic and suits comparison of chemodiverse samples with poor feature overlap or strong RT shift.: "is a method allowing a Retention Time (RT) agnostic alignment of metabolomics samples using the fragmentation spectra (MS2)"
- [other] Validate matrix dimensions and feature consistency to confirm preparedness for downstream alignment and filtering steps.: "Validate matrix dimensions and feature consistency across samples to confirm preparedness for downstream alignment and filtering steps."
