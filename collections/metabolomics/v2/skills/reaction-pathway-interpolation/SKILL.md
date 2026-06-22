---
name: reaction-pathway-interpolation
description: Use when after CREST (version >= 3.0.2) has identified an ensemble of low-energy conformers and stationary points (minima and transition states), and before submitting interpolated geometries to ORCA (version >= 6.0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0321
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_2275
  tools:
  - QCxMS2
  - xtb
  - ORCA
  - molbar
  - geodesic_interpolate
  - CREST
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

# reaction-pathway-interpolation

## Summary

Generate smooth geometric pathways between identified molecular minima and transition states using geodesic interpolation, preparing them for high-level quantum mechanical evaluation. This technique bridges low-cost conformational sampling with expensive single-point calculations by systematically connecting stationary points.

## When to use

After CREST (version >= 3.0.2) has identified an ensemble of low-energy conformers and stationary points (minima and transition states), and before submitting interpolated geometries to ORCA (version >= 6.0.0) for quantum mechanical single-point energy and property calculations in an automated EI mass spectrum fragmentation pipeline.

## When NOT to use

- When endpoint structures are not stationary points (minima or transition states) — linear interpolation may not preserve chemical validity.
- For single isolated molecules or when no meaningful reaction pathways exist between sampled conformers.
- When ORCA single-point calculations are not intended as the next step — geodesic interpolation is specifically designed to prepare geometries for high-level QM evaluation.

## Inputs

- XYZ geometry files representing identified minima from conformational ensemble
- XYZ geometry files representing identified transition states
- Pairs of endpoint geometries to interpolate between

## Outputs

- Interpolated molecular geometries along geodesic paths
- Geometry ensemble ready for ORCA single-point calculations
- Reaction pathway coordinates for fragmentation network

## How to apply

Execute geodesic_interpolate on pairs of molecular geometries identified as minima or transition states from the conformational ensemble. The tool generates a series of intermediate geometries along the geodesic path connecting the two endpoints, preserving molecular connectivity and minimizing geometric distortion. Feed the resulting interpolated geometry set to ORCA for high-level quantum mechanical evaluation. Validate interpolation success by confirming that intermediate structures maintain chemical connectivity and that energy profiles along the path are physically reasonable (no artificial discontinuities or severe strain). The interpolated structures populate the reaction network database used by the EI mass spectrum fragmentation algorithm.

## Related tools

- **geodesic_interpolate** (Generates smooth geometric pathways between molecular conformations, essential for connecting stationary points identified by CREST into a continuous reaction coordinate representation.) — https://github.com/virtualzx-nad/geodesic-interpolate
- **CREST** (Identifies the minima and transition states that serve as interpolation endpoints; must be run (version >= 3.0.2) before geodesic interpolation to generate the conformational ensemble.) — https://github.com/crest-lab/crest
- **ORCA** (Receives interpolated geometries for high-level quantum mechanical single-point energy and property calculations; energies from ORCA are aggregated into the fragmentation database (version >= 6.0.0).) — https://orcaforum.kofo.mpg.de
- **QCxMS2** (Master orchestration tool that dispatches geodesic_interpolate as part of the automated reaction network exploration pipeline for EI mass spectrum calculation.) — https://github.com/grimme-lab/QCxMS2
- **molbar** (Processes ORCA output energies and molecular properties from interpolated geometries to construct fragmentation database and reaction channels (version >= 1.1.3).) — https://git.rwth-aachen.de/bannwarthlab/molbar

## Evaluation signals

- Interpolated geometry files are valid XYZ format with conserved atom counts and connectivity matching endpoints.
- Energy profile along interpolated pathway is smooth and monotonic (or exhibits expected barrier structure if true TS present); no artificial discontinuities or sudden jumps between adjacent frames.
- Intermediate structures maintain chemical feasibility: bond lengths remain within standard ranges, no steric clashes, RMSD between adjacent frames is consistently small.
- ORCA single-point calculations on all interpolated geometries complete successfully without geometry errors or convergence failures.
- Fragmentation database constructed by molbar from interpolated + ORCA energies yields EI mass spectrum peak intensities and m/z values consistent with experimental reference spectra.

## Limitations

- Geodesic interpolation accuracy depends on the quality and similarity of endpoint geometries; poorly converged or chemically dissimilar minima may yield unphysical intermediates.
- The method is computationally expensive for large molecular systems due to repeated geometry optimizations along the path in ORCA.
- No built-in validation of whether the interpolated pathway represents a chemically relevant reaction channel; users must verify that endpoints and intermediates are chemically sensible.
- Interpolation assumes continuous deformation; it cannot model bond-breaking/forming events that require discrete topology changes without additional molecular fragmentation logic.
- Convergence and quality depend critically on CREST conformer sampling completeness; if important minima or TS are missed, interpolation will not represent the full reaction network.

## Evidence

- [other] Execute geodesic_interpolate to generate reaction pathway interpolations between identified minima and transition states.: "Execute geodesic_interpolate to generate reaction pathway interpolations between identified minima and transition states."
- [other] Interpolated geometries submitted to ORCA for high-level QM calculations.: "Submit interpolated geometries to ORCA (version >= 6.0.0) for high-level quantum mechanical single-point energy and property calculations."
- [readme] Reaction pathway interpolations enable connection of stationary points in automated network.: "automated exploration of the low-energy molecular chemical space"
- [other] CREST generates the conformational ensemble prior to interpolation.: "Run CREST (version >= 3.0.2) to explore conformational space and generate ensemble of low-energy structures."
- [other] Molbar processes interpolated geometry energies into fragmentation database.: "Process ORCA output energies and molecular properties via molbar (version >= 1.1.3) to construct fragmentation database and reaction channels."
