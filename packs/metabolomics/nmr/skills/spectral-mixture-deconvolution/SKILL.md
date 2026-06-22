---
name: spectral-mixture-deconvolution
description: Use when you have an NMR spectrum of a mixture sample and a library of reference spectra for individual compounds, and you need to determine which compounds are present and in what proportions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# spectral-mixture-deconvolution

## Summary

Reconstruct an NMR mixture spectrum and identify constituent compounds by solving a minimum-cost flow problem that optimally combines single-compound reference spectra from a library, minimizing Earth Mover's Distance. This skill recovers both compound identities and their fractional abundances from complex mixture samples.

## When to use

You have an NMR spectrum of a mixture sample and a library of reference spectra for individual compounds, and you need to determine which compounds are present and in what proportions. Use this skill when the mixture spectrum can be approximated as a linear combination of library spectra, and you want an optimal reconstruction measured by Earth Mover's Distance rather than simple least-squares fitting.

## When NOT to use

- Input mixture spectrum contains compounds not represented in the reference library; MCF will force a suboptimal fit rather than flag missing compounds.
- Spectrum is from a single pure compound; use for mixture deconvolution only, not for compound verification.
- Target spectrum has been pre-processed into a feature table or already-assigned peak list; this skill requires raw or minimally processed spectral coordinates and intensities.

## Inputs

- NMR mixture spectrum (CSV/CSV.GZ with columns: 1H, 13C, optional weights)
- Library of single-compound reference spectra (CSV/CSV.GZ with columns: name, 1H, 13C, optional weights)
- Configuration file (TOML) specifying library path, target path, assignment_radius, detection_threshold, and optional fit mode (isolated_fit, incremental_fit)

## Outputs

- Identified compound names and their fractional abundances
- Reconstructed approximated mixture spectrum (as weighted linear combination of library spectra)
- Reconstruction error metric (EMD or residual norm)
- Minimum-cost flow solution (pickle format)
- Results CSV with compound assignments and weights
- Optional visualization plot (SVG, PNG, EPS, JPG, etc.)

## How to apply

Load the mixture spectrum and library of single-compound reference spectra as CSV or gzipped CSV files with columns '1H' and '13C' (and optionally 'weights'); the library must include a 'name' column identifying each compound. Compute pairwise Earth Mover's Distance scores between the mixture and each library spectrum to establish arc costs. Formulate a minimum-cost flow (MCF) network where nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and sink nodes. Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow. Extract compound identities and fractional abundances from the optimal flow solution, then reconstruct an approximated mixture spectrum by linearly combining selected library spectra weighted by their identified abundances. Validate the reconstruction by computing residual error (EMD or residual norm) and confirming it meets your tolerance threshold; the assignment_radius and detection_threshold parameters control how strictly compounds must match.

## Related tools

- **mcfNMR** (Primary tool that implements the minimum-cost flow algorithm for spectral reconstruction and compound identification; executes the MCF solver, EMD computation, and result extraction) — https://github.com/GeoMetabolomics-ICBM/mcfNMR
- **spec2csv** (Utility within mcfNMR package to convert various spectral data formats (USCF files, Bruker matrices, peak lists) into the CSV format required by mcfNMR) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
mcfNMR -c config_basic.toml
# where config_basic.toml contains:
# lib = "lib.csv"
# target = "target.csv"
# assignment_radius = 0.5
# detection_threshold = 0.1
```

## Evaluation signals

- Reconstruction error (EMD or residual norm) is below the specified detection_threshold and tolerance, indicating the linear combination of selected compounds adequately approximates the mixture spectrum.
- All identified compounds have fractional abundances ≥ 0 and sum to ≤ 1.0 (or exactly 1.0 if flow conservation is strictly enforced), confirming valid flow solution.
- The set of identified compounds does not change when the assignment_radius is increased slightly, demonstrating robustness of the identification.
- Manual visual inspection: overlay of reconstructed spectrum and original mixture spectrum shows close alignment at major peaks and bins with large intensities; residual spectrum is flat or shows only noise-level deviations.
- For incremental_fit mode with multiple assignment radii, later passes should identify fewer new compounds and improve existing fits, confirming convergence of the refinement.

## Limitations

- Performance degrades if the reference library is very large or if the mixture contains many compounds; MCF solver scales with graph size (number of nodes and edges).
- MCF solution is optimal only for the chosen cost metric (EMD); other distance metrics or weighting schemes may yield different compound assignments.
- The linear mixture model assumes additive spectral contributions and does not account for non-linear peak shifts, multiplet splitting changes, or concentration-dependent effects that may alter peak positions or intensities in mixtures.
- Compounds absent from the library cannot be detected; the algorithm will instead over-fit contributions from partial library matches, yielding inflated abundances for similar library members.
- Grid spectra (2D NMR) can be represented, but the tool also accepts 1D spectra by setting the second coordinate to a fixed value—this may reduce discriminatory power for compound identification.

## Evidence

- [intro] mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample.: "mcfNMR is a tool for recovering constituent compounds from an NMR spectrum of a mixture sample."
- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Formulate the MCF problem: nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and sink nodes.: "Formulate the MCF problem: nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand"
- [readme] Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding peaks belong to.: "Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding"
- [readme] Obligatory fields: 'lib': Path to a library-file containing the names, peak-weights, and -coords of the spectra a set of compounds. 'target': Path to a target-file containing the name, peak-weights, and -coords of the target-(i.e., mixture-)spectrum. 'assignment_radius': Assignment radius. 'detection_threshold': Detection threshold (assignment > th indicates containment).: "Obligatory fields: 'lib': Path to a library-file. 'target': Path to a target-file. 'assignment_radius': Assignment radius. 'detection_threshold': Detection threshold (assignment > th indicates"
- [other] Extract the compound identities and their fractional abundances from the optimal flow solution. Reconstruct the approximated mixture spectrum by linear combination of selected library spectra weighted by their identified abundances.: "Extract the compound identities and their fractional abundances from the optimal flow solution. Reconstruct the approximated mixture spectrum by linear combination of selected library spectra"
