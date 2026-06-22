---
name: linear-algebra-peak-reconstruction
description: Use when after a Transformer model (e.g. GCMSFormer) has predicted the pure mass spectral matrix S for all components in overlapped peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Python 3
  - numpy.linalg.lstsq
  - GCMSFormer
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
---

# linear-algebra-peak-reconstruction

## Summary

Reconstruct overlapped GC-MS peak intensities by solving a least-squares problem that decomposes the observed overlapped spectrum into a linear combination of pure mass spectra (matrix S) and unknown concentration coefficients (matrix C). This skill recovers the concentration distribution of co-eluting compounds after pure spectra have been predicted.

## When to use

Apply this skill after a Transformer model (e.g. GCMSFormer) has predicted the pure mass spectral matrix S for all components in overlapped peaks. You have observed overlapped peak intensity data and need to estimate the concentration distribution matrix C by inverting the linear relationship overlapped_peaks ≈ S·C. Use when the number of pure spectra is known and the peak data are quantitative.

## When NOT to use

- Pure mass spectra (S) have not yet been predicted or resolved; use GCMSFormer or OPR first.
- Overlapped peak data are qualitative (presence/absence only) rather than quantitative intensities.
- The number of components n is unknown or varies across samples; this linear approach assumes fixed n.

## Inputs

- mass spectral matrix S (predicted pure mass spectra; m×n array)
- overlapped peak intensity data (m×t array of observed intensities)
- resolved component count n (from prior prediction step)

## Outputs

- concentration distribution matrix C (n×t array of concentration coefficients)
- reconstructed peak intensities (S·C; m×t array for validation)

## How to apply

Formulate the least-squares optimization problem: minimize ||overlapped_peaks - S·C||² where S is the m×n matrix of predicted pure mass spectra (m mass-to-charge ratios, n components), C is the n×t unknown concentration matrix (n components, t time points or samples), and overlapped_peaks is the m×t observed intensity matrix. Solve for C using a least-squares solver such as numpy.linalg.lstsq (normal equations) or PyTorch-based optimization. Validate the solution by reconstructing the overlapped peaks as S·C and comparing element-wise with the input overlapped_peaks to check residual magnitude and ensure the reconstruction is faithful.

## Related tools

- **numpy.linalg.lstsq** (Least-squares solver for the linear system S·C ≈ overlapped_peaks) — https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
- **PyTorch** (Optional optimization framework for solving the least-squares problem via gradient descent) — https://pytorch.org/
- **GCMSFormer** (Upstream Transformer model that predicts the pure mass spectral matrix S) — https://github.com/zxguocsu/GCMSFormer

## Examples

```
import numpy as np; C = np.linalg.lstsq(S, overlapped_peaks, rcond=None)[0]; reconstructed = S @ C
```

## Evaluation signals

- Reconstruction error: ||overlapped_peaks - S·C||² is minimized and residuals are small relative to peak magnitudes.
- Schema validation: C has shape (n_components, n_samples); all entries are non-negative (concentrations cannot be negative).
- Peak intensity fidelity: reconstructed peaks S·C match observed overlapped_peaks element-wise within measurement noise; visual overlay or Pearson correlation > 0.99.
- Least-squares solver convergence: solver reports successful solution (rank = n or convergence flag = 0); condition number of S is not pathologically large (κ < 10³).
- Component separation: concentration profiles in C are distinct and interpretable; spurious solutions (e.g. negative or near-zero concentrations for all components) are absent.

## Limitations

- Linear model assumes additive mixing (Beer–Lambert law); nonlinear effects (saturation, matrix suppression) are not accounted for.
- Sensitivity to errors in S: if the predicted pure spectra S are inaccurate, the recovered C will be biased or unstable; condition number of S increases with spectral correlation.
- Assumes the number of components n is known and constant; if n is misspecified or variable, the least-squares solution may be underdetermined or overdetermined.
- No regularization by default; ill-conditioned S may yield C with large or oscillating entries; Tikhonov regularization (ridge regression) may be needed for stability.

## Evidence

- [other] Formulate the least squares problem: minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution.: "Formulate the least squares problem: minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution."
- [other] Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization) to obtain the concentration matrix.: "Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization) to obtain the concentration matrix."
- [intro] use the least squares method to find the concentration distribution matrix C: "use the least squares method to find the concentration distribution matrix C"
- [other] Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data.: "Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data."
- [intro] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
