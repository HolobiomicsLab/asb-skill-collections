---
name: conformer-ensemble-processing
description: Use when you have a set of conformers that have already been filtered
  by ASE-ANI neural network potentials and need to extract quantum-mechanical electronic
  properties (polarizability tensor, dipole moment) required for collision cross section
  calculation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2476
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0625
  tools:
  - QUICK
  - Snakemake
  - ASE-ANI
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'QUICK: For quantum calculations'
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional
  cross sections (CCS)
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

# conformer-ensemble-processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load pre-filtered conformers (in xyz or molden format) from ASE-ANI filtering, prepare quantum calculation inputs for each conformer, and submit them in parallel to QUICK for quantum calculations. This skill bridges molecular geometry optimization and electronic property extraction in the CCS prediction workflow.

## When to use

You have a set of conformers that have already been filtered by ASE-ANI neural network potentials and need to extract quantum-mechanical electronic properties (polarizability tensor, dipole moment) required for collision cross section calculation. Use this skill when input conformers are in xyz or molden format and you have access to HPC resources for parallel quantum calculations.

## When NOT to use

- Input conformers have not been pre-filtered by ASE-ANI or another energy-based screening method; unfiltered ensembles will incur prohibitive quantum calculation costs.
- Conformer geometries are in formats other than xyz or molden; format conversion is required first.
- HPC resources with parallel quantum calculation capability are unavailable; QUICK requires GPU or multi-core support for reasonable runtime.

## Inputs

- Pre-filtered conformer geometry files (xyz or molden format from ASE-ANI filtering step)
- Conformer metadata (conformer IDs, molecular identities)
- QUICK configuration parameters (quantum method, basis set specification)

## Outputs

- QUICK quantum calculation output logs
- Structured electronic properties table (conformer ID → polarizability tensor components, dipole moment)
- Aggregated conformer properties for Boltzmann averaging in CCS ensemble calculation

## How to apply

Load each pre-filtered conformer geometry from xyz or molden files. For each conformer, generate a QUICK input file specifying the quantum method, basis set, and molecular geometry. Submit conformers in parallel across available HPC cores via QUICK, leveraging Snakemake's job orchestration. After execution, parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment). Aggregate results into a structured output table mapping conformer ID to computed properties. The rationale is that quantum calculations on only the most stable conformer ensemble (pre-filtered by ASE-ANI) reduces computational cost while maintaining accuracy for downstream CCS prediction.

## Related tools

- **QUICK** (Executes quantum calculations on each filtered conformer to extract polarizability tensor and dipole moment) — https://github.com/merzlab/QUICK
- **Snakemake** (Orchestrates parallel submission and job management for multiple conformers across HPC cores) — https://github.com/DasSusanta/snakemake_ccs
- **ASE-ANI** (Pre-filters conformers before this skill; provides input ensemble in xyz/molden format) — https://github.com/isayev/ASE_ANI

## Evaluation signals

- All input conformer files (xyz/molden) are successfully parsed and QUICK input files are generated with correct molecular geometries and method specifications.
- QUICK jobs complete without crashes; output logs contain valid electronic property data (polarizability tensor components as symmetric 3×3 matrices, dipole moments as real numbers).
- Output property table has one row per input conformer with no missing values; conformer IDs match input conformer identifiers.
- Polarizability tensor eigenvalues are physically reasonable (positive, typically 1–100 Å³ for organic metabolites); dipole moments are non-negative.
- Aggregated properties can be successfully used in downstream Boltzmann averaging step to compute ensemble-weighted CCS values.

## Limitations

- ASE-ANI is deprecated (README: 'DEPRECATED and no longer supported, please use TorchANI implementation'); users should migrate to TorchANI for conformer filtering to ensure ongoing support.
- QUICK quantum calculations scale linearly with conformer count and molecular size; very large ensembles (>10,000 conformers) or large molecules may exceed HPC walltime or memory limits.
- Electronic properties depend critically on choice of quantum method and basis set; basis set incompleteness and method choice (DFT functional, post-HF level) affect accuracy and must be validated against experimental data.
- Output quality requires proper QUICK installation and GPU/HPC configuration; missing dependencies or incorrect compute resource allocation will cause silent failures or timeout.

## Evidence

- [other] Load the set of pre-filtered conformers (in xyz or molden format) from the ASE-ANI filtering step.: "Load the set of pre-filtered conformers (in xyz or molden format) from the ASE-ANI filtering step."
- [other] Prepare QUICK input files for each conformer specifying the quantum method, basis set, and molecular geometry.: "Prepare QUICK input files for each conformer specifying the quantum method, basis set, and molecular geometry."
- [other] Submit each conformer for quantum calculation via QUICK, executing in parallel on available HPC cores.: "Submit each conformer for quantum calculation via QUICK, executing in parallel on available HPC cores."
- [other] Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment).: "Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment)."
- [other] Aggregate results into a structured output table mapping conformer ID to computed properties.: "Aggregate results into a structured output table mapping conformer ID to computed properties."
- [other] QUICK performs quantum calculations as the final computational step in the CCS prediction pipeline, operating on conformers that have been filtered by ASE-ANI.: "QUICK performs quantum calculations as the final computational step in the CCS prediction pipeline, operating on conformers that have been filtered by ASE-ANI."
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
- [intro] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
