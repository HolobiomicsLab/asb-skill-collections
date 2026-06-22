---
name: minimum-cost-flow-formulation
description: Use when you have an NMR mixture spectrum and a library of single-compound reference spectra, and you need to identify which compounds are present and their relative abundances.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - mcfNMR
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

# minimum-cost-flow-formulation

## Summary

Formulate and solve a minimum-cost flow (MCF) network problem to reconstruct an NMR mixture spectrum as an optimal linear combination of single-compound reference spectra. This skill maps spectral matching to a flow conservation and cost-minimization problem, where nodes represent spectral bins, edges represent compound contributions, and arc costs derive from Earth Mover's Distance.

## When to use

You have an NMR mixture spectrum and a library of single-compound reference spectra, and you need to identify which compounds are present and their relative abundances. Use this skill when you want to find the optimal subset of library compounds and their weights such that their linear combination best approximates the observed mixture spectrum, measured by Earth Mover's Distance.

## When NOT to use

- The mixture spectrum is already a deconvolved peak table or pre-identified compound list; MCF formulation is unnecessary if ground truth identities are already known.
- The library is empty or does not contain the true constituents; MCF will reconstruct a suboptimal approximation from available compounds only.
- Real-time or near-real-time processing is required; MCF solving (especially cost-scaling) can be computationally expensive for large libraries or high-resolution spectra.

## Inputs

- NMR mixture spectrum (2D peak coordinates and intensities, or 1D with fixed second coordinate)
- Library of single-compound reference spectra (CSV with columns '1H', '13C', 'weights', and 'name')
- Assignment radius (single float for single-pass fit, or sequence for incremental multipass)
- Detection threshold (numeric; assignment > threshold indicates compound containment)

## Outputs

- Optimal MCF solution (minimum-cost flow assignment)
- Identified compound identities and fractional abundances
- Reconstructed mixture spectrum (linear combination of weighted library spectra)
- Reconstruction error metric (EMD or residual norm)
- Validation report confirming error meets tolerance threshold

## How to apply

Begin by computing pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs. Formulate the MCF network with nodes representing spectral bins and edges representing potential compound contributions, with arc costs derived from EMD. Set flow conservation constraints at each bin (what flows in must flow out) and supply/demand constraints for source and sink nodes, typically balancing the total spectrum intensity. Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow. Extract compound identities and their fractional abundances from the optimal flow solution, then reconstruct the approximated mixture spectrum by taking the weighted linear combination of selected library spectra using the identified abundances. Finally, validate by computing reconstruction error (EMD or residual norm) and confirming it meets the reported tolerance threshold.

## Related tools

- **mcfNMR** (Reference implementation that formulates, solves, and validates the MCF problem for NMR mixture reconstruction; computes Earth Mover's Distance, manages graph construction, and extracts compound abundances from the optimal flow.) — https://github.com/GeoMetabolomics-ICBM/mcfNMR

## Examples

```
python -m mcfnmr -c config.toml
```

## Evaluation signals

- Flow conservation is satisfied at every bin node: inflow equals outflow.
- Supply and demand constraints are met at source and sink nodes.
- The cost of the optimal flow is minimal (no alternative flow with lower total cost exists).
- Reconstruction error (EMD or residual norm) is ≤ the pre-specified tolerance threshold.
- The set of identified compounds and their abundances, when weighted and summed, produce a mixture spectrum visually and quantitatively consistent with the observed spectrum.

## Limitations

- The reconstruction is only as good as the library; if true constituents are absent, the MCF will approximate with available compounds, potentially masking unknowns.
- Computational complexity scales with library size and spectral resolution; large-scale or very-high-resolution 2D spectra may incur significant solver runtime.
- The Earth Mover's Distance metric assumes a sensible transport cost structure; misalignment or systematic bias in peak coordinates or intensities will propagate into the MCF formulation.
- Binary presence/absence decisions (detection_threshold) are sensitive to the chosen threshold value; suboptimal thresholds may misclassify minor or overlapping constituents.
- The successive shortest-paths and cost-scaling algorithms have known failure modes if the network is disconnected or if numerical precision issues arise in the cost matrix.

## Evidence

- [other] Formulate the MCF problem: nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand constraints for source and sink nodes.: "Formulate the MCF problem: nodes represent spectral bins, edges represent compound contributions, and arc costs are derived from EMD; set flow conservation constraints at each bin and supply/demand"
- [intro] It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library.: "It constructs an optimal approximation (in terms of the Earth Mover's Distance) of the mixture spectrum by combining single compound spectra from a library."
- [other] Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow that reconstructs the mixture.: "Solve the MCF problem using a successive shortest-paths or cost-scaling algorithm to identify the minimum-cost flow that reconstructs the mixture."
- [other] Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs.: "Compute pairwise Earth Mover's Distance scores between the mixture spectrum and each library spectrum to establish edge costs."
- [other] Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold.: "Validate: compute reconstruction error (EMD or residual norm) and confirm it meets the reported tolerance threshold."
- [readme] Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding peaks belong to.: "Library- and target files must be csv-files, with columns '1H', '13C', and optionally 'weights'. A library file must additionally have a column 'name' to indicate the compound id the corresponding"
