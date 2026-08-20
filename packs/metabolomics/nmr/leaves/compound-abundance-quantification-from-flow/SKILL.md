---
name: compound-abundance-quantification-from-flow
description: Use when you have an NMR mixture spectrum (1D or 2D) and a library of reference spectra for pure compounds, and you need to identify which compounds are present and in what proportions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - mcfNMR
  - spec2csv
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compound-Abundance Quantification from Flow

## Summary

Extract compound identities and their fractional abundances from an NMR mixture spectrum by solving a minimum-cost flow optimization problem that reconstructs the mixture as a linear combination of single-compound library spectra. The method optimizes flow assignments to minimize the Earth Mover's Distance between reconstructed and observed spectra.

## When to use

You have an NMR mixture spectrum (1D or 2D) and a library of reference spectra for pure compounds, and you need to identify which compounds are present and in what proportions. Use this skill when you want to avoid peak-by-peak assignment and instead solve for the compound composition that best reconstructs the observed mixture spectrum as a weighted linear combination of library members.

## When NOT to use

- The mixture spectrum contains peaks from compounds not present in your reference library; the MCF formulation requires library coverage to reconstruct the mixture accurately.
- You already have reliable manual peak assignments or independent quantification data; MCF is an assignment-free approach and adds complexity where direct measurement suffices.
- Your input spectra are not properly normalized or aligned (e.g., different calibration references); MCF depends on consistent coordinate systems and intensity scales across library and target.

## Inputs

- NMR mixture spectrum (CSV or gzipped CSV with columns: peak coordinates in 1H/13C dimensions, optional intensity weights)
- Single-compound reference spectral library (CSV or gzipped CSV with columns: compound name, peak coordinates, peak weights)
- Configuration file (TOML) specifying: library path, target path, assignment_radius, detection_threshold, and optional fit parameters

## Outputs

- List of identified compounds with their fractional abundances (CSV format)
- Reconstructed mixture spectrum (peak list with predicted intensities)
- Reconstruction error metric (Earth Mover's Distance or residual norm)
- Optional visualization: matched compounds plotted on top of target spectrum (SVG/PNG/EPS/JPG)

## How to apply

Load the NMR mixture spectrum and single-compound reference spectral library (both as CSV files with peak coordinates and intensities). Compute pairwise Earth Mover's Distance scores between the mixture and each library spectrum to establish edge costs. Formulate a minimum-cost flow (MCF) problem where nodes represent spectral bins, edges represent possible compound contributions, and arc costs derive from EMD; set flow conservation constraints at each bin and supply/demand constraints at source/sink nodes. Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow that reconstructs the mixture. Extract compound identities and fractional abundances from the optimal flow solution. Reconstruct the approximated mixture spectrum by computing the linear combination of selected library spectra weighted by their identified abundances. Validate by computing reconstruction error (EMD or residual norm) and confirming it meets the specified tolerance threshold.

## Related tools

- **mcfNMR** (Primary tool that implements the minimum-cost flow optimization, solves the MCF problem, and outputs compound identities and abundances from mixture spectra) — https://github.com/GeoMetabolomics-ICBM/mcfNMR
- **spec2csv** (Utility within mcfNMR package to convert raw spectral data formats (USCF, Bruker matrices, peak lists) into CSV-compatible input files for MCF pipeline) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
python -m mcfnmr -c config.toml
or
mcfNMR -c config.toml
```

## Evaluation signals

- Reconstruction error (EMD or residual norm) falls below the specified detection_threshold, confirming the linear combination of identified compounds accurately approximates the observed mixture.
- All identified compounds have fractional abundances in the interval [0, 1] and sum to ≤ 1.0 (accounting for noise or unidentified components).
- The MCF solution respects flow conservation: total flow into each spectral bin matches total flow out, with no accumulation or loss at intermediate nodes.
- Visual inspection (if plot=true): the reconstructed spectrum aligns visibly with the target spectrum across all major peaks; systematic deviations suggest missing library members or spectral misalignment.
- Reproducibility check: re-running with the same configuration and cached results (load=true) yields identical compound assignments and abundances.

## Limitations

- Requires complete or near-complete coverage of compounds present in the mixture by the reference library; compounds absent from the library cannot be identified and may inflate reconstruction error or absorb their signal into partial identifications of similar library members.
- Assumes linear additivity of spectra (no nonlinear peak interactions, matrix effects, or solvent shifts between pure compounds and mixture); significant deviations invalidate the reconstruction assumption.
- Performance scales with library size and spectral resolution; very large libraries or high-resolution 2D grids may increase computational cost of EMD and MCF solving.
- Earth Mover's Distance calculation is sensitive to peak alignment; misalignment of coordinate systems between library and target spectra (e.g., different chemical shift references) can degrade reconstruction quality.
- Isolated_fit=true (independent fitting) may overestimate abundances if compound spectra overlap significantly; joint_fit (default) is more conservative but slower.

## Evidence

- [intro] mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample.: "mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample."
- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Extract the compound identities and their fractional abundances from the optimal flow solution.: "Extract the compound identities and their fractional abundances from the optimal flow solution."
- [other] nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and sink nodes: "nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and"
- [other] Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold.: "Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold."
- [readme] Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'.: "Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'."
- [readme] Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value).: "Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value)."
