---
name: concentration-matrix-estimation-gc-ms
description: Use when after GCMSFormer (or similar Transformer model) has predicted pure mass spectra (matrix S) for all components in overlapped GC-MS peaks, apply this skill to quantify the relative abundance of each component.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0630
  tools:
  - PyTorch
  - Python 3
  - NumPy
  - GCMSFormer
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c05772
  title: GCMSFormer
evidence_spans:
- '[pytorch](https://pytorch.org/)'
- '[python3](https://www.python.org/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcmsformer_cq
    doi: 10.1021/acs.analchem.3c05772
    title: GCMSFormer
  dedup_kept_from: coll_gcmsformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05772
  all_source_dois:
  - 10.1021/acs.analchem.3c05772
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Least-Squares Concentration Distribution Matrix Estimation for GC-MS

## Summary

Solves for the concentration distribution matrix C in gas chromatography–mass spectrometry (GC-MS) data by applying least-squares optimization to overlapped peak intensities and predicted pure mass spectra. This post-processing step completes the GCMSFormer workflow after Transformer-based spectral deconvolution.

## When to use

After GCMSFormer (or similar Transformer model) has predicted pure mass spectra (matrix S) for all components in overlapped GC-MS peaks, apply this skill to quantify the relative abundance of each component. Specifically, when you have resolved mass spectral matrix S and measured overlapped peak intensities, and need to recover the concentration distribution matrix C that explains how pure spectra mix to reconstruct the observed data.

## When NOT to use

- The predicted mass spectral matrix S is not available or has rank < number of components (underdetermined system; least squares cannot recover unique C).
- Overlapped peak intensities contain systematic noise or outliers not accounted for in the model; use robust regression or iterative outlier removal first.
- The goal is peak detection or identification only; concentration estimation is not needed.

## Inputs

- Predicted mass spectral matrix S (components × m/z dimensions)
- Overlapped peak intensity matrix (m/z × time or samples)
- Resolved mass spectral predictions from GCMSFormer or similar model

## Outputs

- Concentration distribution matrix C (components × time/samples)
- Reconstructed overlapped peaks S·C (for validation)
- Residuals from least-squares fit

## How to apply

Formulate the least-squares minimization problem: minimize ||overlapped_peaks - S·C||², where S is the predicted mass spectral matrix (rows = mass-to-charge ratios, columns = components), C is the unknown concentration distribution (rows = components, columns = time points or samples), and overlapped_peaks is the measured intensity matrix. Solve using a standard least-squares solver such as numpy.linalg.lstsq or PyTorch optimization. The solver yields C, the concentration distribution of each component over time or across samples. Validate the solution by reconstructing the overlapped peaks as S·C and comparing element-wise with the input overlapped_peaks data; residuals should be small and randomly distributed if the decomposition is adequate.

## Related tools

- **PyTorch** (Provides optimization backend and tensor operations for solving the least-squares problem and reconstructing predicted peaks.) — https://pytorch.org/
- **NumPy** (Provides numpy.linalg.lstsq solver for direct least-squares solution of the system.)
- **GCMSFormer** (Upstream Transformer model that predicts the pure mass spectral matrix S; output from GCMSFormer is the primary input to this skill.) — https://github.com/zxguocsu/GCMSFormer

## Examples

```
import numpy as np
C = np.linalg.lstsq(S, overlapped_peaks, rcond=None)[0]
reconstructed = S @ C
residuals = overlapped_peaks - reconstructed
```

## Evaluation signals

- Reconstruction error ||overlapped_peaks - S·C||² is minimized; check that residuals are small relative to peak intensities (e.g., relative error < 5%).
- All elements of C are non-negative (physical constraint: concentrations cannot be negative).
- Residuals are randomly distributed around zero with no systematic bias; plot residuals vs. predicted values to confirm.
- Cross-validation or hold-out test: fit C on training peaks, predict held-out peaks, and compare reconstruction error.
- Concentration profile C is smooth or interpretable (e.g., no spurious negative or oscillating values that indicate overfitting or ill-conditioning).

## Limitations

- Assumes the mass spectral matrix S is accurate and complete; errors in S propagate directly to C.
- Least-squares is sensitive to outliers in overlapped_peaks; robust regression variants may be needed for noisy or contaminated data.
- If S is ill-conditioned or components are highly similar, the solution may be unstable; regularization (ridge regression, Lasso) may help.
- Requires the number of components to be known or correctly predicted beforehand; rank mismatches lead to underdetermined or overdetermined systems.

## Evidence

- [other] Formulate the least squares problem: minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution.: "Formulate the least squares problem: minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution."
- [other] Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization) to obtain the concentration matrix.: "Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization) to obtain the concentration matrix."
- [other] Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data.: "Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data."
- [readme] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [other] The workflow applies the least squares method as a computational step following GCMSFormer's prediction of the pure mass spectra (mass spectral matrix S) to solve for the concentration distribution matrix C.: "The workflow applies the least squares method as a computational step following GCMSFormer's prediction of the pure mass spectra (mass spectral matrix S) to solve for the concentration distribution"
