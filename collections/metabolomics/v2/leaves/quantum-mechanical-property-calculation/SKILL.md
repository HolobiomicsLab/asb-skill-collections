---
name: quantum-mechanical-property-calculation
description: Use when when you have interpolated or optimized molecular geometries
  (from geodesic_interpolate or CREST conformer ensembles) and need to compute ab
  initio electronic energies, orbital properties, or transition state characteristics
  to populate a fragmentation reaction network or validate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0321
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_3314
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
  - CREST
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.5c00234
  title: QCxMS2
evidence_spans:
- Program package for the quantum mechanical calculation of EI mass spectra using
  automated reaction network exploration
- '**xtb** (version > 6.7.1 - bleeding edge version)'
- '**orca** (version >= 6.0.0)'
- '**molbar** (version >= 1.1.3)'
- '**geodesic_interpolate** (version'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  - build: coll_qcxms2_cq
    doi: 10.1021/jasms.5c00234
    title: QCxMS2
  dedup_kept_from: coll_qcxms2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00234
  all_source_dois:
  - 10.1021/jasms.5c00234
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quantum-mechanical-property-calculation

## Summary

Execute high-level quantum mechanical single-point energy and molecular property calculations on interpolated reaction pathway geometries using ORCA. This skill enables calculation of fragmentation energetics and structural properties required for constructing reaction networks and EI mass spectra.

## When to use

When you have interpolated or optimized molecular geometries (from geodesic_interpolate or CREST conformer ensembles) and need to compute ab initio electronic energies, orbital properties, or transition state characteristics to populate a fragmentation reaction network or validate energetic ordering of reaction intermediates.

## When NOT to use

- Input geometries are unoptimized or contain unphysical bond lengths — use CREST or xtb geometry optimization first
- Target molecules are too large (>~200 heavy atoms) for practical ORCA computation with hybrid functionals — consider semiempirical methods (xtb) instead
- Electronic properties (e.g., excited state energies, transition dipoles) are needed but only ground-state single-point calculation is requested

## Inputs

- molecular geometry files (XYZ or ORCA input format) representing optimized structures, conformers, or interpolated reaction pathway snapshots
- ORCA input template or configuration specifying functional, basis set, and calculation parameters
- electronic structure method specification (functional, basis set, convergence criteria)

## Outputs

- ORCA output files containing converged single-point energies and molecular properties
- parsed electronic energies (Hartree or eV)
- molecular orbital energies and occupation numbers
- fragmentation reaction channel energetics data

## How to apply

Submit interpolated geometries to ORCA (version >= 6.0.0) as single-point calculations with appropriate functional and basis set. ORCA processes the electron density and molecular orbital information to compute electronic energies and molecular properties. Parse ORCA output files to extract converged energies and structural properties, then aggregate these values into a fragmentation database or reaction channel list. Verify convergence flags in ORCA output and check that computed energies follow expected thermochemical ordering (e.g., intermediates lower in energy than transition states on the same pathway). Properties feed directly into subsequent molbar processing for fragmentation pathway construction.

## Related tools

- **ORCA** (high-level quantum mechanical single-point energy and property calculator for fragmentation pathway characterization) — https://orcaforum.kofo.mpg.de
- **geodesic_interpolate** (upstream tool generating interpolated reaction pathway geometries for ORCA input) — https://github.com/virtualzx-nad/geodesic-interpolate
- **molbar** (downstream tool processing ORCA-computed energies and properties to construct fragmentation database) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **CREST** (upstream conformer generation and ensemble sampling tool producing initial geometries for ORCA calculation) — https://github.com/crest-lab/crest

## Evaluation signals

- ORCA SCF convergence flag is present in output (e.g., 'THE OPTIMIZATION HAS CONVERGED' or final energy printed)
- Computed energies are consistent with chemical intuition: intermediates lower than separated fragments, barriers positive relative to reactants
- Parsed energy values successfully aggregate into molbar reaction channel database without parsing errors
- Energy differences between conformers or reaction path points fall within expected range (typically 0–100 kcal/mol for fragmentation pathways)
- ORCA geometry structures match input XYZ/interpolated geometries within expected numerical precision

## Limitations

- ORCA single-point calculations are computationally expensive for large molecular ensembles; QCxMS2 workflow typically uses hybrid functionals (B3LYP, PBE0) which scale as O(N⁴); for molecules >150 atoms, runtime may exceed practical limits on standard compute clusters
- ORCA version >= 6.0.0 required; older versions may not produce compatible output format for automatic parsing by molbar
- Fragmentation pathways depend critically on correct geometry interpolation from geodesic_interpolate; poor interpolation (e.g., over long distances or through steric clashes) can yield spurious energetic ordering
- Electronic correlation effects beyond single-point DFT are not captured; post-HF methods (MP2, CCSD) are not integrated into the QCxMS2 pipeline and would require custom molbar modifications

## Evidence

- [intro] Submit interpolated geometries to ORCA for high-level QM calculation: "Submit interpolated geometries to ORCA (version >= 6.0.0) for high-level quantum mechanical single-point energy and property calculations."
- [intro] Parse ORCA output to extract energies and properties: "Process ORCA output energies and molecular properties via molbar (version >= 1.1.3) to construct fragmentation database and reaction channels."
- [readme] ORCA is required dependency for QCxMS2: "**orca** (version >= 6.0.0) [`orca`](https://orcaforum.kofo.mpg.de)"
- [readme] Installation prerequisite for QCxMS2 calculations: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [intro] ORCA output feeds into molbar for reaction network construction: "Aggregate reaction network fragment data and apply EI mass spectrum simulation algorithm to produce final mass spectrum."
