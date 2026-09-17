---
name: ei-mass-spectrum-simulation
description: Use when when you have a molecular structure (XYZ or equivalent format)
  and need to predict its EI mass spectrum including major fragment ions and their
  relative intensities, particularly for validation against experimental data or when
  experimental spectra are unavailable;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3314
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
  - CREST
  techniques:
  - GC-MS
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

# ei-mass-spectrum-simulation

## Summary

Quantum mechanical calculation of electron ionization (EI) mass spectra through automated reaction network exploration, integrating semiempirical geometry optimization, conformational ensemble sampling, high-level quantum mechanical single-point calculations, and fragmentation pathway simulation to produce predicted m/z and intensity values.

## When to use

When you have a molecular structure (XYZ or equivalent format) and need to predict its EI mass spectrum including major fragment ions and their relative intensities, particularly for validation against experimental data or when experimental spectra are unavailable; applicable to organic molecules where automated fragmentation pathways are chemically interpretable.

## When NOT to use

- Input molecular structure is already a fragmentation tree or derived fragment list rather than a complete intact molecule geometry
- Target molecule contains metal centers or non-standard bonding not adequately described by the xTB/ORCA computational methods
- Experimental mass spectrum is already available and high-throughput screening is the primary goal (use simpler library matching instead)

## Inputs

- molecular geometry file (XYZ or equivalent format)
- reaction network parameters (conformation search settings, energy thresholds)
- quantum mechanical calculation specifications (functional, basis set for ORCA)

## Outputs

- calculated EI mass spectrum (text or structured format with m/z and intensity values)
- fragmentation database (reaction channels and pathways)
- ensemble of low-energy molecular structures with energies and properties

## How to apply

Begin by parsing the input molecular geometry file (XYZ format) and initializing QCxMS2 with reaction network parameters. Execute xtb (version > 6.7.1) for rapid geometry optimization and conformer generation, then apply CREST (version >= 3.0.2) to exhaustively sample the conformational space and identify low-energy structural ensembles. Use geodesic_interpolate to generate interpolated geometries along reaction pathways connecting minima and transition states. Submit the ensemble to ORCA (version >= 6.0.0) for high-level single-point energy and property calculations at each geometry. Process ORCA outputs through molbar (version >= 1.1.3) to construct a fragmentation database and identify reaction channels. Finally, aggregate the reaction network data and apply the EI mass spectrum simulation algorithm to yield m/z and intensity values. Success is indicated by chemically reasonable fragment masses, intensity ratios consistent with known fragmentation rules, and convergence of spectral features across the conformational ensemble.

## Related tools

- **QCxMS2** (primary orchestrator for automated reaction network exploration and EI mass spectrum calculation) — https://github.com/grimme-lab/QCxMS2
- **xtb** (fast semiempirical geometry optimization and conformer generation (version > 6.7.1 required)) — https://github.com/grimme-lab/xtb
- **CREST** (conformational space exploration and low-energy ensemble generation (version >= 3.0.2 required)) — https://github.com/crest-lab/crest
- **ORCA** (high-level quantum mechanical single-point energy and property calculations (version >= 6.0.0 required))
- **molbar** (post-processing of ORCA outputs to construct fragmentation database and reaction channels (version >= 1.1.3 required)) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **geodesic_interpolate** (generation of interpolated reaction pathways between identified minima and transition states) — https://github.com/virtualzx-nad/geodesic-interpolate

## Evaluation signals

- All external programs (xtb, CREST, ORCA, molbar, geodesic_interpolate) execute without errors and produce expected intermediate output files
- CREST conformational ensemble contains multiple low-energy structures spanning energetically distinct regions of configuration space, indicating successful sampling
- ORCA single-point calculations converge for all interpolated geometries without SCF or geometry errors
- Predicted m/z values align with known stable fragment ions for the molecular class (e.g., loss of common neutral fragments such as CO, H₂O, or alkyl groups)
- Relative intensities of major peaks follow expected fragmentation patterns and McLafferty rearrangement rules where applicable; base peak corresponds to chemically reasonable fragment

## Limitations

- Computational cost scales steeply with molecular size (> 50 heavy atoms may become prohibitive) and complexity of conformational landscape
- Requires correct installation and sourcing of five external dependencies; missing or incompatible versions will cause pipeline failure
- Quality of predictions depends on adequacy of xTB semiempirical method for initial conformer sampling and ORCA functional/basis choice for final energetics; no guarantee of chemical accuracy
- Fragmentation pathways are derived from energetic minima and interpolated structures; kinetic barriers, tunneling effects, and non-equilibrium processes may not be accurately captured
- Method assumes EI ionization mechanism (direct electron impact); inapplicable to soft ionization techniques (ESI, APCI) or molecules prone to rearrangement in the mass spectrometer

## Evidence

- [methods] QCxMS2 requires five external programs for EI mass spectrum calculation: "QCxMS2 requires five external programs to be installed and sourced: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), and geodesic_interpolate"
- [other] Workflow sequence from geometry parsing through mass spectrum output: "Parse and validate the input molecular geometry file (XYZ or equivalent format). Initialize QCxMS2 driver with molecular structure and reaction network parameters. Execute xtb for fast geometry"
- [readme] External program sourcing requirement stated in README: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [readme] CREST role in conformational ensemble generation: "CREST (abbreviated from Conformer-Rotamer Ensemble Sampling Tool) is a program for the automated exploration of the low-energy molecular chemical space. It functions as an OMP scheduler for"
- [readme] xtb version requirement specificity: "xtb (version > 6.7.1 - bleeding edge version)"
