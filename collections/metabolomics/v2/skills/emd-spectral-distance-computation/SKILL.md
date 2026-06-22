---
name: emd-spectral-distance-computation
description: Use when you have an NMR mixture spectrum and a library of single-compound reference spectra, and you need to identify which compounds are present in the mixture and their abundances.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - mcfNMR
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.4c01652
  title: mcfNMR
evidence_spans:
- mcfNMR is a tool for recovering constituent compounds from an NMR spectrum
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mcfnmr_cq
    doi: 10.1021/acs.analchem.4c01652
    title: mcfNMR
  dedup_kept_from: coll_mcfnmr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01652
  all_source_dois:
  - 10.1021/acs.analchem.4c01652
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# EMD-based Spectral Distance Computation

## Summary

Compute pairwise Earth Mover's Distance (Wasserstein metric) scores between an NMR mixture spectrum and a library of single-compound reference spectra to establish edge costs for network flow optimization. This metric quantifies the minimum cost to transform one spectrum into another by redistributing spectral mass.

## When to use

You have an NMR mixture spectrum and a library of single-compound reference spectra, and you need to identify which compounds are present in the mixture and their abundances. EMD is particularly useful when spectra exhibit peak shifts, overlaps, or distortions that make direct peak-by-peak matching unreliable.

## When NOT to use

- The input spectra are already aligned to a common reference frame and exhibit no peak shifts or overlaps; direct peak matching or simpler Euclidean distance would be more efficient.
- Computational budget is extremely tight and you need real-time performance; EMD computation is more expensive than L2 or cosine distance, especially for high-resolution spectra.
- You are analyzing 1D spectra without any 2D context and peaks are sufficiently resolved that mass redistribution is not a meaningful metric.

## Inputs

- NMR mixture spectrum (peak coordinates and intensities in chemical shift space)
- Library of single-compound reference spectra (each with name, 1H coordinate, 13C coordinate, and intensity weights)
- Spectral data in CSV or gzipped CSV format with columns: 1H, 13C, and optionally weights

## Outputs

- Pairwise Earth Mover's Distance matrix (compounds × 1, symmetric distance scores)
- Edge cost assignments for minimum-cost flow network
- Distance-ranked compound candidates for inclusion in mixture

## How to apply

Load the NMR mixture spectrum and all library spectra as distributions of spectral intensity across chemical shift bins. Compute the Earth Mover's Distance (Wasserstein metric) between the mixture spectrum and each library spectrum; this produces a symmetric distance matrix where each entry represents the minimum cost to morph one spectrum into another by moving spectral mass. These pairwise EMD scores become edge costs in a subsequent minimum-cost flow formulation, where lower EMD indicates better spectral similarity. The EMD computation is foundational to the graph construction step; the resulting cost matrix constrains which compounds can be selected and in what proportions to optimally reconstruct the mixture spectrum.

## Related tools

- **mcfNMR** (Implements EMD-based spectral distance computation as part of its minimum-cost flow pipeline for NMR mixture deconvolution; uses EMD scores as edge costs in the network flow optimization) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
python -m mcfnmr -c data/user_templates/config_basic.toml
# Where config_basic.toml specifies lib and target CSV/gzipped paths; EMD computation is executed internally during the MCF problem formulation step.
```

## Evaluation signals

- EMD distance matrix is symmetric: distance(spectrum_A, spectrum_B) == distance(spectrum_B, spectrum_A)
- All pairwise distances are non-negative and satisfy the triangle inequality (d(A,C) ≤ d(A,B) + d(B,C))
- Distance to self is zero or near-zero: distance(spectrum, spectrum) ≈ 0
- Spectra with visually similar peak patterns (position, intensity, shape) yield lower EMD scores than dissimilar spectra
- Reconstruction error (EMD or residual norm) of the final linear combination of selected library spectra meets the reported tolerance threshold specified in the workflow

## Limitations

- EMD computation is computationally expensive for high-resolution spectra or very large spectral libraries; runtime scales with spectral dimensionality and library size.
- EMD is sensitive to the choice of bin resolution and coordinate normalization; inconsistent binning or scale differences between mixture and library spectra can inflate or deflate distances spuriously.
- EMD alone does not account for spectral variability due to pH, concentration, or solvent effects; compounds with similar chemical shifts but different line widths or coupling patterns may be indistinguishable by EMD.
- The metric assumes that mass redistribution cost is uniform across all regions of the spectrum; it does not weight diagnostic peaks or biologically relevant regions more heavily unless explicitly incorporated into the cost function.

## Evidence

- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs.: "Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs."
- [other] nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD: "nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD"
- [other] mcfNMR constructs an optimal approximation of a mixture spectrum by combining single compound spectra from a library, with optimality measured in terms of the Earth Mover's Distance.: "mcfNMR constructs an optimal approximation of a mixture spectrum by combining single compound spectra from a library, with optimality measured in terms of the Earth Mover's Distance."
- [readme] an optimal approximation ([in terms of the Earth Mover's Distance](https://en.wikipedia.org/wiki/Wasserstein_metric)) of the mixture spectrum by combining single compound spectra from a library: "an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library"
