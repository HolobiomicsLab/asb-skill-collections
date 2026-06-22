---
name: molecular-geometry-optimization
description: Use when you have generated multiple 3D conformers (e.g., from RDKit's distance-geometry algorithm) of ionized adducts and need to relax them toward local minima before filtering with machine-learning potentials or quantum methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2476
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3373
  tools:
  - Snakemake
  - RDKit
  - ASE-ANI
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  dedup_kept_from: coll_pomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.1c00315
  all_source_dois:
  - 10.1021/jasms.1c00315
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-geometry-optimization

## Summary

Optimize 3D molecular geometries toward local energy minima using force-field methods, preparing conformer ensembles for downstream quantum or machine-learning filtering. This skill bridges conformer generation and high-level validation by relaxing structures to physically plausible states.

## When to use

Apply this skill when you have generated multiple 3D conformers (e.g., from RDKit's distance-geometry algorithm) of ionized adducts and need to relax them toward local minima before filtering with machine-learning potentials or quantum methods. Use it to eliminate high-strain, unphysical geometries that would waste computational resources in expensive downstream steps.

## When NOT to use

- Input is a single rigid crystal structure or experimentally resolved conformation—optimization may introduce unnecessary perturbation.
- Computational budget does not permit even fast force-field minimization; consider skipping to machine-learning filtering if conformer count is very large (>10,000 per molecule).
- Conformers are already validated by a higher-accuracy method (e.g., already filtered by machine learning)—re-optimization is redundant.

## Inputs

- Ensemble of 3D conformers with hydrogens attached (SDF or MOL format)
- Ionized adduct structures from upstream ionization-state determination
- Conformer count specification (e.g., 50–500 samples per molecule)

## Outputs

- Relaxed 3D conformer ensemble with minimized geometries (SDF or pickle format)
- Conformer ensemble retained for downstream ASE-ANI filtering

## How to apply

For each conformer in the ensemble, apply a force-field geometry minimization using either MMFF94 or UFF. Run minimization until convergence (typically gradient-based optimization to a tolerance threshold). Retain all minimized conformers in an ensemble format (SDF or pickle) for export to downstream ASE-ANI filtering. The rationale is that force-field relaxation is fast (compared to quantum or neural-network evaluations), removes obvious strain, and ensures the conformer ensemble is physically initialized for more expensive filtering and quantum calculations.

## Related tools

- **RDKit** (Generate initial 3D coordinates and conformers; supply force-field minimization routines (MMFF94 or UFF)) — https://www.rdkit.org
- **ASE-ANI** (Downstream filtering of relaxed conformer ensemble using neural-network potential) — https://github.com/isayev/ASE_ANI
- **Snakemake** (Workflow orchestration for parallelized geometry optimization across multiple molecules) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; mol = Chem.AddHs(Chem.MolFromSmiles('[NH4+]')); AllChem.EmbedMolecule(mol); AllChem.UFFGetMoleculeForceField(mol).Minimize(); Chem.SDWriter('optimized.sdf').write(mol)
```

## Evaluation signals

- All conformers converge to a local minimum (energy gradient below convergence tolerance); check final RMS gradient reported by minimizer.
- No conformer remains in a high-energy state (outlier energies >3σ above median suggest incomplete optimization or strain).
- Geometry ensemble diversity is preserved: inter-conformer RMSD values remain consistent before and after minimization, confirming relaxation did not collapse distinct conformations.
- Downstream ASE-ANI filtering step accepts all conformers without crashing; no invalid molecular structures (e.g., overlapping atoms, broken bonds).
- Output ensemble file size and conformer count match input (SDF or pickle format is readable and complete).

## Limitations

- Force-field methods (MMFF94, UFF) may not accurately describe highly strained or unusual functional groups; ASE-ANI filtering is essential before quantum calculation.
- ASE-ANI README notes the tool is DEPRECATED and recommends migration to TorchANI; downstream filtering infrastructure may require updates.
- Local minima from force-field optimization may differ from those found by higher-accuracy quantum methods; this is acceptable as a rapid filter, but some conformers may be discarded that would survive quantum screening.
- Very large conformer ensembles (>1000 per molecule) incur cumulative computational cost even with fast force fields; practical limits depend on HPC walltime allocation.

## Evidence

- [other] Use RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima: "Minimize each conformer's geometry using RDKit's built-in force field (MMFF94 or UFF) to relax structures toward local minima."
- [other] Conformer ensemble exported in SDF/pickle for downstream filtering: "Export the conformer ensemble to SDF or pickle format with all conformers retained for downstream filtering."
- [readme] Force-field minimization is fast and prepares conformers for neural-network filtering: "ASE-ANI: For conformation filtering. Available at: [https://github.com/isayev/ASE_ANI]"
- [other] Workflow context: ionized structures → conformer generation → force-field optimization → ASE-ANI filtering: "RDKit is used in the workflow as the conformation generation tool that operates on ionized adduct structures produced by Dimorphite-DL, generating 3D conformers that are subsequently filtered by"
