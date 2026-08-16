---
name: polarizability-tensor-extraction
description: Use when after ASE-ANI has filtered conformers to remove high-energy
  geometries, and you need to compute electronic properties required for CCS prediction.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2423
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3314
  tools:
  - QUICK
  - Snakemake
  - ASE-ANI
  techniques:
  - ion-mobility-MS
  license_tier: restricted
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

# polarizability-tensor-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract electronic polarizability tensor components and dipole moments from quantum calculation output logs (QUICK) applied to filtered molecular conformers. These properties are essential inputs for computing collision cross sections (CCS) via trajectory methods in metabolite annotation workflows.

## When to use

After ASE-ANI has filtered conformers to remove high-energy geometries, and you need to compute electronic properties required for CCS prediction. Use this skill when your input is a set of low-energy conformers in xyz or molden format and your goal is to obtain polarizability tensors and dipole moments for each conformer prior to CCS calculation.

## When NOT to use

- Input conformers have not been pre-filtered by ASE-ANI or an equivalent energy-ranking method; unfiltered high-energy geometries will produce unrepresentative polarizability values.
- Target molecules contain elements outside QUICK's supported set (e.g., transition metals, lanthanides); QUICK is optimized for organic small molecules (C, H, N, O, S, halogens).
- Polarizability is already available from prior calculations or experimental measurements; re-computing via QUICK introduces redundancy and computational cost.

## Inputs

- Filtered conformer geometries in xyz or molden format (output from ASE-ANI filtering step)
- Quantum method specification (e.g., B3LYP, HF, DFT hybrid functional name)
- Basis set specification (e.g., 6-31G*, aug-cc-pVDZ)

## Outputs

- Structured table mapping conformer ID to polarizability tensor components (αxx, αyy, αzz, αxy, αxz, αyz)
- Molecular dipole moment vector (μx, μy, μz) for each conformer
- Parsed QUICK output logs confirming successful quantum calculations

## How to apply

Submit each pre-filtered conformer to QUICK, a quantum chemistry package, specifying the desired quantum method and basis set in the input file. Execute QUICK calculations in parallel across available HPC cores to leverage computational resources. Parse the resulting QUICK output logs to systematically extract the 3×3 polarizability tensor components (αxx, αyy, αzz, αxy, αxz, αyz) and the molecular dipole moment vector. Aggregate the extracted properties into a structured output table with conformer IDs as row keys, enabling downstream mapping to CCS values. Verify extraction accuracy by checking that tensor elements are physically plausible (e.g., positive diagonal components, symmetric off-diagonal pairs) and that dipole magnitudes are within expected ranges for the molecular species.

## Related tools

- **QUICK** (Executes quantum mechanical calculations on conformers to compute electronic properties (polarizability tensor, dipole moment)) — https://github.com/merzlab/QUICK
- **ASE-ANI** (Filters and ranks conformers by energy before QUICK calculations; provides input conformer geometries) — https://github.com/isayev/ASE_ANI
- **Snakemake** (Workflow manager orchestrating parallel QUICK job submission, output collection, and log parsing across HPC nodes) — https://github.com/DasSusanta/snakemake_ccs

## Evaluation signals

- All conformer IDs in output table match input conformer set; no missing or duplicate entries.
- Polarizability tensor is symmetric: αxy = αyx, αxz = αzx, αyz = αzy (within floating-point tolerance).
- Diagonal polarizability components (αxx, αyy, αzz) are all positive and sum to a physically plausible isotropic polarizability value for the molecular composition.
- Dipole moment magnitudes are within expected ranges for the molecular species (e.g., < 10 Debye for small organic molecules).
- QUICK output logs show successful convergence (zero exit codes) and do not report basis set errors or geometry failures.

## Limitations

- QUICK's polarizability calculations are restricted to elements in C, H, N, O, S, and halogens; molecules outside this set require alternative quantum codes.
- Accuracy and computational cost depend strongly on choice of quantum method and basis set; higher levels of theory (e.g., wB97X-D, aug-cc-pVTZ) produce better accuracy but scale poorly to large conformer ensembles on HPC.
- The workflow assumes all conformers are chemically valid and already optimized to local minima by ASE-ANI; distorted or incomplete geometries will produce unreliable polarizability estimates or QUICK convergence failures.
- Polarizability is computed in vacuo (gas phase); solvent effects are not included, which may affect applicability to liquid-phase mass spectrometry conditions.

## Evidence

- [other] Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment): "Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment)."
- [other] Quantum calculations operating on conformers filtered by ASE-ANI: "QUICK performs quantum calculations as the final computational step in the CCS prediction pipeline, operating on conformers that have been filtered by ASE-ANI."
- [other] Load pre-filtered conformers and prepare QUICK input files: "Load the set of pre-filtered conformers (in xyz or molden format) from the ASE-ANI filtering step. 2. Prepare QUICK input files for each conformer specifying the quantum method, basis set, and"
- [other] Aggregate results into structured output mapping conformer ID to properties: "Aggregate results into a structured output table mapping conformer ID to computed properties."
- [readme] QUICK is listed as a prerequisite for CCS calculation workflow: "QUICK: For quantum calculations. Available at: [https://github.com/merzlab/QUICK]"
