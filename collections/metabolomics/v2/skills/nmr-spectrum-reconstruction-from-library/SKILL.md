---
name: nmr-spectrum-reconstruction-from-library
description: Use when you have an NMR spectrum of a mixture sample and a library of reference spectra for individual compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mcfNMR
  - spec2csv
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
---

# NMR Spectrum Reconstruction from Library

## Summary

Reconstruct an NMR mixture spectrum by solving a minimum-cost flow (MCF) problem that optimally combines single-compound reference spectra from a library, measured by Earth Mover's Distance. This skill identifies constituent compounds and their fractional abundances in a mixture sample.

## When to use

You have an NMR spectrum of a mixture sample and a library of reference spectra for individual compounds. Use this skill when you need to determine which compounds are present in the mixture and in what proportions, measured against an Earth Mover's Distance optimality criterion rather than simple peak matching.

## When NOT to use

- Input is a pure single-compound spectrum (no mixture present); use direct spectral matching instead.
- Library does not contain reference spectra for the compounds present in the mixture; mcfNMR can only reconstruct from available library entries.
- Mixture spectrum lacks sufficient spectral resolution or signal-to-noise ratio to resolve individual compound peaks from library spectra.

## Inputs

- NMR mixture spectrum (CSV or gzipped CSV with columns: 1H, 13C, optionally weights)
- Library of single-compound reference spectra (CSV or gzipped CSV with columns: name, 1H, 13C, optionally weights)
- Configuration file (TOML) specifying assignment_radius, detection_threshold, and other MCF parameters

## Outputs

- List of identified compounds and their fractional abundances
- Reconstructed approximated mixture spectrum
- Reconstruction error metric (Earth Mover's Distance or residual norm)
- Visualization of matched compounds overlaid on target spectrum (optional)

## How to apply

Load the NMR mixture spectrum and the library of single-compound reference spectra (both as CSV files with columns for 1H, 13C coordinates and peak weights). Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs in a flow network. Formulate the MCF problem where nodes represent spectral bins, edges represent compound contributions, and arc costs derive from EMD; enforce flow conservation constraints at each bin and supply/demand constraints for source and sink nodes. Solve using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow. Extract compound identities and their fractional abundances from the optimal flow solution, then reconstruct the approximated mixture spectrum by linear combination of selected library spectra weighted by their identified abundances. Validate by computing reconstruction error (EMD or residual norm) and confirming it meets the reported tolerance threshold.

## Related tools

- **mcfNMR** (Primary tool that implements minimum-cost flow network optimization for NMR spectrum reconstruction and compound identification) — https://github.com/GeoMetabolomics-ICBM/mcfNMR
- **spec2csv** (Utility within mcfNMR package to convert various spectral data formats (USCF, Bruker matrices, peak lists) into standardized CSV input for mcfNMR) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
mcfNMR -c config.toml
```

## Evaluation signals

- Reconstruction error (EMD or residual norm) is below the detection_threshold specified in the configuration file.
- Identified compounds have assignment scores (derived from MCF flow values) that exceed the detection_threshold, indicating reliable containment.
- Linear combination of selected library spectra weighted by identified abundances visually matches the target mixture spectrum when plotted.
- Flow conservation constraints are satisfied at all nodes in the MCF solution, and all arc flows are non-negative.
- Compound abundances sum to a physically meaningful total (e.g., between 0 and 1 in normalized representation) without negative values.

## Limitations

- mcfNMR can only identify compounds present in the reference library; unknown compounds or library gaps lead to incomplete or incorrect reconstruction.
- Reconstruction quality depends on the quality and diversity of the reference spectral library; incomplete or poorly curated libraries reduce reliability.
- Overlapping spectral peaks from different compounds can lead to ambiguous assignments; the MCF algorithm resolves this globally but may not reflect true individual concentrations in highly congested regions.
- Works with 1D and 2D spectra; 1D spectra require the second coordinate to be set to zero or a fixed identical value across all spectra.
- Performance and solution quality can be sensitive to the choice of assignment_radius and detection_threshold parameters; incremental_fit mode with multiple radii can improve robustness but increases computational cost.

## Evidence

- [readme] mcfNMR constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [readme] mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample.: "mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample."
- [readme] Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding peaks belong to.: "Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding"
- [readme] Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value).: "Although developed with the goal of processing 2D spectra, it is possible to analyze 1D spectra. To represent a 1D-spectrum, simply set the second coordinate to zero (or any fixed, identical value)."
- [other] Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs. Formulate the MCF problem: nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and sink nodes. Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm.: "Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs. Formulate the MCF problem: nodes represent spectral bins, edges"
- [other] Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold.: "Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold."
