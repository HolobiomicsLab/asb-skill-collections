---
name: least-squares-optimization-spectral-deconvolution
description: Use when after GCMSFormer has predicted the pure mass spectral matrix
  S from overlapped GC-MS peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Python 3
  - numpy.linalg.lstsq
  - GCMSFormer
  techniques:
  - GC-MS
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# least-squares-optimization-spectral-deconvolution

## Summary

Solves for the concentration distribution matrix C in GC-MS peak deconvolution by minimizing the reconstruction error between predicted mass spectra and observed overlapped peak intensities. This step follows Transformer-based pure spectrum prediction to obtain quantitative abundance estimates for each resolved component.

## When to use

Apply this skill after GCMSFormer has predicted the pure mass spectral matrix S from overlapped GC-MS peaks. Use it when you have resolved mass spectra and need to recover the concentration (abundance) distribution of each component across the chromatographic profile to reconstruct the original overlapped peak data.

## When NOT to use

- Mass spectral matrix S is not yet available or contains unresolved/overlapping peaks
- Input overlapped peak data is already deconvolved into pure component spectra (concentration matrix already solved)
- The least squares problem is underdetermined (fewer time points than components) without regularization

## Inputs

- Predicted mass spectral matrix S (m × n, where m = mass bins, n = number of components)
- Observed overlapped peak intensity data (m × t, where m = mass bins, t = time points)
- Pure mass spectra from GCMSFormer model output

## Outputs

- Concentration distribution matrix C (n × t, where n = components, t = time points)
- Reconstructed overlapped peak matrix (S·C)
- Residuals from reconstruction (||overlapped_peaks - S·C||²)

## How to apply

Formulate a least squares optimization problem: minimize ||overlapped_peaks - S·C||² where S is the m×n resolved mass spectral matrix (m mass bins, n components), C is the n×t unknown concentration matrix (n components, t time points), and overlapped_peaks is the m×t observed intensity matrix. Solve using numpy.linalg.lstsq or PyTorch optimization routines to obtain C. Validate by computing the reconstruction S·C and comparing against the input overlapped peak data using residual magnitude and spectral fidelity metrics; solutions should recover the overlapped data to high precision if the pure spectra are well-resolved.

## Related tools

- **PyTorch** (Solves least squares optimization to compute concentration matrix C using GPU-accelerated tensor operations) — https://pytorch.org/
- **numpy.linalg.lstsq** (CPU-based least squares solver for reconstructing concentration distribution)
- **GCMSFormer** (Produces the resolved mass spectral matrix S that serves as input to the least squares deconvolution) — https://github.com/zxguocsu/GCMSFormer

## Examples

```
import numpy as np; S = np.array([[...], [...]]);  overlapped_peaks = np.array([[...], [...]); C, residuals, rank, s = np.linalg.lstsq(S, overlapped_peaks, rcond=None); reconstructed = S @ C
```

## Evaluation signals

- Reconstruction error (||overlapped_peaks - S·C||²) is minimized and smaller than input noise level
- Reconstructed peaks S·C visually and numerically match the original overlapped peak data within measurement precision
- Concentration matrix C is non-negative (abundance constraints) and physically interpretable
- Residual distribution is white/random (not structured), indicating full spectrum capture
- Solution is stable across multiple runs or different initialization conditions

## Limitations

- Requires accurate pure mass spectra from GCMSFormer; errors in S directly propagate to C
- Least squares solution is sensitive to ill-conditioning when components have highly similar mass spectra
- No explicit regularization (L1/L2) is mentioned; may require Tikhonov or similar if the problem is underdetermined or noisy
- Assumes linear mixing model (overlapped_peaks = S·C); deviations from linearity are not modeled

## Evidence

- [other] minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution: "Formulate the least squares problem: minimize ||overlapped_peaks - S·C||² where C is the unknown concentration distribution."
- [other] Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization): "Solve for C using a least squares solver (e.g., numpy.linalg.lstsq or PyTorch optimization) to obtain the concentration matrix."
- [intro] GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [other] Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data: "Validate the solution by reconstructing the overlapped peaks as S·C and comparing with the input overlapped data."
- [readme] The automatic resolution of the overlapped peaks can be easily achieved.: "then use the least squares method to find the concentration distribution matrix C. The automatic resolution of the overlapped peaks can be easily achieved."
