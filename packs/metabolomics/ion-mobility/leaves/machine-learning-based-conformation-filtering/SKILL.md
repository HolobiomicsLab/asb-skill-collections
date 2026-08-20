---
name: machine-learning-based-conformation-filtering
description: Use when when you have generated multiple 3D conformations for a molecule or set of ionized adducts (e.g., via RDKit) and need to retain only the most energetically favorable structures before expensive quantum calculations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - Snakemake
  - Dimorphite-DL
  - ASE-ANI
  - QUICK
  - RDKit
  techniques:
  - ion-mobility-MS
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
- 'Dimorphite-DL: For ionization state determination'
- 'ASE-ANI: For conformation filtering'
- 'QUICK: For quantum calculations'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# machine-learning-based-conformation-filtering

## Summary

Filter low-energy molecular conformations from an ensemble using neural network potentials (ANI) trained on quantum chemical data. This reduces the computational burden of subsequent quantum mechanical calculations for predicting molecular properties like collision cross sections.

## When to use

When you have generated multiple 3D conformations for a molecule or set of ionized adducts (e.g., via RDKit) and need to retain only the most energetically favorable structures before expensive quantum calculations. Use this skill when the ensemble size is large enough that filtering will reduce downstream compute cost significantly, and when your molecules contain only C, H, N, O elements (or the subset supported by your ANI model).

## When NOT to use

- Molecules containing elements outside the ANI model's training set (ANI-1x/1ccx support C, H, N, O only; do not use for S, F, Cl, or other heteroatoms without ANI-2x or later variants).
- When quantum mechanical accuracy is required for the filtering step itself; ANI is a fast approximation and may misorder conformations compared to DFT.
- If your conformation ensemble is already small (<5–10 per molecule) or you have computational resources for direct QM calculations on all; filtering overhead may not justify the speedup.

## Inputs

- SMILES strings (ionized, e.g., protonated or deprotonated adducts)
- 3D molecular conformations (XYZ or ASE-compatible format)
- Conformation ensemble (multiple structures per molecule)

## Outputs

- Filtered conformation ensemble (subset of input; lowest-energy structures)
- Energy rankings for all conformations
- Conformation coordinates (ASE atoms objects or XYZ files)

## How to apply

Load the ensemble of conformations into ASE (Atomic Simulation Environment) and evaluate each using the pre-trained ANI neural network potential (ANI-1x or ANI-1ccx recommended). Compute the energy for each conformation; retain those ranked in the lowest-energy percentile (the README examples and the workflow do not specify a hard cutoff, but typical practice retains the lowest ~10–20% of conformations by energy). The rationale is that ANI potentials, trained on millions of off-equilibrium DFT conformations, provide fast and reasonably accurate energy ordering at a fraction of the cost of full quantum mechanical geometry optimization, enabling high-throughput filtering before expensive QUICK or similar QM calculations.

## Related tools

- **ASE-ANI** (Neural network potential for fast conformation energy evaluation and filtering within the Snakemake CCS pipeline) — https://github.com/isayev/ASE_ANI
- **RDKit** (Upstream tool for conformation generation; output fed to ASE-ANI for filtering) — https://www.rdkit.org
- **QUICK** (Downstream quantum mechanical calculator applied only to filtered conformations) — https://github.com/merzlab/QUICK
- **Snakemake** (Workflow orchestration framework that automates and parallelizes conformation filtering across multiple adducts and molecules) — https://github.com/DasSusanta/snakemake_ccs

## Evaluation signals

- Filtered ensemble size is smaller than input ensemble, and energy values are monotonically ordered or span a realistic range for the molecular system.
- All retained conformations have ANI energies within the lowest-energy percentile (typically bottom 10–20%) of the original distribution.
- Downstream QUICK QM calculations converge successfully and complete in less wall-clock time than they would have on the unfiltered ensemble, validating that the filter removed high-energy outliers.
- Energy ordering from ANI filtering is consistent across multiple runs and stable with respect to small perturbations in input coordinates.
- Predicted CCS values computed from the filtered conformations agree with experimental measurements within acceptable tolerance (article does not specify, but metabolomics CCS prediction typically targets <5–10% error).

## Limitations

- ASE-ANI repository is deprecated; the README recommends migration to TorchANI for ongoing support and better compatibility with modern Python/CUDA versions.
- ANI-1x and ANI-1ccx potentials are limited to C, H, N, O elements; molecules with S, F, Cl, or metals require ANI-2x or alternative ML potentials.
- Filtering is heuristic based on energy alone; does not account for kinetic accessibility, solvent effects, or other physical factors that may favor higher-energy but dynamically accessible conformations.
- The README specifies strict requirements (Python 3.6, CUDA 9.2, Ubuntu/NVIDIA GPU only), which may be outdated or unavailable on modern HPC systems; TorchANI recommended instead.
- No hard threshold cutoff is documented for which conformations to retain; practitioners must choose percentile or energy window empirically for their use case.

## Evidence

- [intro] ASE-ANI: For conformation filtering.: "ASE-ANI: For conformation filtering."
- [other] The workflow integrates four sequential computational steps... ASE-ANI for conformation filtering, and QUICK for quantum calculations.: "The workflow integrates four sequential computational steps... ASE-ANI for conformation filtering, and QUICK for quantum calculations."
- [other] Filter conformations using ASE-ANI machine learning model to retain low-energy structures.: "Filter conformations using ASE-ANI machine learning model to retain low-energy structures."
- [readme] This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials for The Atomic Simulation Environment (ASE). Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials for The Atomic Simulation Environment (ASE). Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
- [readme] For best performance the ANI-1x and ANI-1ccx ensembles in this branch should be used in any application.: "For best performance the ANI-1x and ANI-1ccx ensembles in this branch should be used in any application."
