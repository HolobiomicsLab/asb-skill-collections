---
name: automated-reaction-network-exploration
description: Use when when you have a molecular geometry (XYZ format) and need to predict electron ionization (EI) mass spectrum fragmentation patterns by exhaustively sampling conformational space and reaction intermediates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2426
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_3372
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
  - CREST
  techniques:
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.5c00234
  title: QCxMS2
evidence_spans:
- Program package for the quantum mechanical calculation of EI mass spectra using automated reaction network exploration
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# automated-reaction-network-exploration

## Summary

Automated exploration of low-energy molecular reaction pathways and fragmentation channels using chained semiempirical and quantum mechanical calculations. This skill enables discovery of energetically accessible reaction networks for mass spectrum simulation without manual pathway specification.

## When to use

When you have a molecular geometry (XYZ format) and need to predict electron ionization (EI) mass spectrum fragmentation patterns by exhaustively sampling conformational space and reaction intermediates. Apply this skill when manual pathway specification is infeasible or when you need to discover unexpected fragmentation routes that contribute significantly to the mass spectrum.

## When NOT to use

- Input molecular structure contains metal centers or organometallic coordination; QCxMS2 and xtb are optimized for organic molecules
- You require classical (non-quantum mechanical) fragmentation rules or empirical mass spectrum libraries rather than first-principles reaction network exploration
- The molecule is too large (>~100 heavy atoms) for exhaustive conformational sampling to complete in reasonable wall-clock time on available hardware

## Inputs

- Molecular geometry file in XYZ or equivalent format
- Reaction network parameters (conformer search settings, energy thresholds)
- Electronic structure level specifications for ORCA calculations

## Outputs

- Calculated EI mass spectrum as text or structured format with m/z and intensity values
- Fragmentation database mapping molecular fragments to reaction channels
- Ensemble of low-energy conformers and reaction intermediates
- Reaction pathway interpolations and transition state geometries

## How to apply

Parse and validate the input molecular geometry file (XYZ or equivalent format), then initialize the QCxMS2 driver with molecular structure and reaction network parameters. Execute xtb (version > 6.7.1) for fast geometry optimization and conformer generation, followed by CREST (version >= 3.0.2) to exhaustively explore conformational space and generate an ensemble of low-energy structures. Use geodesic_interpolate to generate smooth reaction pathway interpolations between identified minima and transition states. Submit interpolated geometries to ORCA (version >= 6.0.0) for high-level quantum mechanical single-point energy and property calculations. Process ORCA output energies and molecular properties via molbar (version >= 1.1.3) to construct a fragmentation database and identify viable reaction channels. Finally, aggregate the reaction network fragment data and apply the EI mass spectrum simulation algorithm to produce the final mass spectrum with m/z and intensity values.

## Related tools

- **QCxMS2** (Main orchestrator that dispatches the entire automated reaction network exploration and mass spectrum calculation pipeline) — https://github.com/grimme-lab/QCxMS2
- **xtb** (Performs fast semiempirical geometry optimization and conformer generation (version > 6.7.1 required)) — https://github.com/grimme-lab/xtb
- **CREST** (Explores conformational space and generates ensemble of low-energy molecular structures (version >= 3.0.2 required)) — https://github.com/crest-lab/crest
- **ORCA** (Executes high-level quantum mechanical single-point energy and property calculations on interpolated geometries (version >= 6.0.0 required))
- **molbar** (Processes quantum mechanical output to construct fragmentation database and identify reaction channels (version >= 1.1.3 required)) — https://git.rwth-aachen.de/bannwarthlab/molbar
- **geodesic_interpolate** (Generates smooth reaction pathway interpolations between identified minima and transition states) — https://github.com/virtualzx-nad/geodesic-interpolate

## Evaluation signals

- Output mass spectrum contains m/z values within expected range (1–molecular_mass) with non-zero intensities for observed ions
- Fragmentation database identifies chemically reasonable fragments (neutral losses, rearrangement products) consistent with known EI chemistry
- CREST conformer ensemble contains at least 2–3 geometrically distinct low-energy structures with energy spacing < 10 kcal/mol
- ORCA single-point calculations converge successfully for all interpolated geometries with reasonable orbital energies and electronic properties
- Reaction network contains sequential (stepwise) fragmentation pathways connecting parent ion to observed fragments, demonstrating network connectivity

## Limitations

- QCxMS2 and its dependencies (xtb, CREST, ORCA, molbar) must be independently installed and correctly sourced in PATH; no integrated packaging in the binary distribution
- Conformational sampling and ORCA calculations scale poorly for molecules larger than ~100 heavy atoms; computational wall-time can exceed hours or days on modest hardware
- No support for metal-containing molecules, highly strained ring systems, or exotic bonding scenarios where semiempirical (xtb) or DFT (ORCA) assumptions break down
- Fragmentation pathways depend critically on ORCA functional and basis set choice; choice not specified in README and may require user tuning for non-standard molecules
- No changelog available; version compatibility and bug-fix history cannot be retrospectively audited

## Evidence

- [other] QCxMS2 requires five external programs to be installed and sourced: xtb (version > 6.7.1), CREST (version >= 3.0.2), molbar (version >= 1.1.3), orca (version >= 6.0.0), and geodesic_interpolate: "For any installation make sure that you have correctly installed and sourced the following external programs before attempting any calculations with QCxMS2"
- [other] Workflow proceeds from geometry validation through conformer generation, pathway interpolation, quantum mechanical calculations, and final fragmentation database aggregation: "Parse and validate the input molecular geometry file (XYZ or equivalent format). 2. Initialize QCxMS2 driver with molecular structure and reaction network parameters. 3. Execute xtb (version > 6.7.1)"
- [other] Purpose and output format of the mass spectrum calculation: "Output calculated mass spectrum as text or structured format with m/z and intensity values"
- [readme] CREST is used for conformational space exploration as part of the automated workflow: "CREST (abbreviated from Conformer-Rotamer Ensemble Sampling Tool) is a program for the automated exploration of the low-energy molecular chemical space."
- [readme] xtb version requirement grounded in bleeding-edge capability: "xtb (version > 6.7.1 - bleeding edge version)"
