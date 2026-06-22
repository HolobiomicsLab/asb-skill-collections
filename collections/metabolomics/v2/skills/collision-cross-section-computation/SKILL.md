---
name: collision-cross-section-computation
description: Use when you have a set of molecular structures in SMILES format that require CCS prediction for metabolite annotation in untargeted mass spectrometry workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - Snakemake
  - Dimorphite-DL
  - ASE-ANI
  - QUICK
  - RDKit
  - hpccs
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# collision-cross-section-computation

## Summary

End-to-end computational workflow for predicting collisional cross section (CCS) values from SMILES molecular structures via automated ionization state determination, conformer generation, energy-based filtering, and quantum mechanical calculations. CCS values aid in metabolite annotation by providing a third orthogonal dimension (mobility) for mass spectrometry-based compound identification.

## When to use

Apply this skill when you have a set of molecular structures in SMILES format that require CCS prediction for metabolite annotation in untargeted mass spectrometry workflows. Use it specifically when you need CCS values for multiple protonated or deprotonated adducts to improve compound identification confidence in liquid chromatography–mass spectrometry (LC–MS) or ion mobility spectrometry (IMS) experiments.

## When NOT to use

- Input molecules contain elements outside the CHNO or CHNOSFCl periodic set (ANI potentials only support these elements; QUICK may have broader support but verification is required).
- When only single-point CCS values without conformational ensemble averaging are needed (this workflow is over-engineered for such cases).
- When CCS values are already experimentally measured or available in reference databases; use direct lookup or targeted refinement instead.

## Inputs

- SMILES strings (simplified molecular-input line-entry system formatted molecular structures)
- pH specification (typically physiological pH ~7.4 for ionization state generation)

## Outputs

- CCS values (in Ų units) for each protonated/deprotonated adduct
- Boltzmann-weighted ensemble CCS values
- Quantum mechanical properties (energies, charges) for each conformer
- Metadata table mapping SMILES to predicted CCS across all models/adducts

## How to apply

Execute a four-stage sequential pipeline: (1) Pass each SMILES through Dimorphite-DL to generate ionization states (protonated and deprotonated adducts) at physiological pH; (2) Use RDKit to generate multiple three-dimensional conformations for each ionization state; (3) Filter conformations using the ASE-ANI machine learning potential to retain only low-energy structures, reducing computational cost; (4) Run quantum mechanical geometry optimization and property calculations on filtered conformations using QUICK; (5) Aggregate results and compute Boltzmann-weighted average CCS values across the ensemble of conformations. Parallelize steps 2–4 on high-performance computing (HPC) systems via Snakemake workflow orchestration to manage job dependencies and resource allocation.

## Related tools

- **Dimorphite-DL** (Ionization state determination: generates protonated and deprotonated adducts from SMILES input at specified pH) — https://durrantlab.pitt.edu/dimorphite-dl
- **RDKit** (Three-dimensional conformer generation: produces multiple low-energy 3D structures for each ionization state) — https://www.rdkit.org
- **ASE-ANI** (Conformer filtering and energy ranking: uses ANI-1x/ANI-1ccx neural network potentials to rank and retain low-energy conformations, reducing QUICK calculation time) — https://github.com/isayev/ASE_ANI
- **QUICK** (Quantum mechanical geometry optimization and property calculation: refines conformer geometries and computes molecular properties required for CCS calculation) — https://github.com/merzlab/QUICK
- **hpccs** (CCS calculation from optimized geometries: computes collision cross section values from quantum mechanical structures) — https://github.com/cepid-cces/hpccs
- **Snakemake** (Workflow orchestration and parallelization: manages job dependencies, resource allocation, and parallel execution on HPC systems) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
bash scheduler.sh # after configuring paths.json, cluster.yaml, and arguments.json with input SMILES, ionization pH, and HPC parameters
```

## Evaluation signals

- Output CCS values fall within expected ranges for the molecular class (e.g., peptides/metabolites typically 50–500 Ų); compare against experimental CCS databases when available.
- Boltzmann-averaged CCS values are closer to the lowest-energy conformer CCS than to the highest-energy conformer (indicating correct weighting).
- All input SMILES generate at least one ionization state and at least one conformer per adduct without errors or missing outputs.
- Quantum geometry optimization converges successfully for >95% of conformers; inspect QUICK output logs for SCF convergence failures.
- CCS predictions for chemically similar compounds (e.g., isomers, homologs) show plausible rank ordering consistent with molecular size and branching.

## Limitations

- ASE-ANI is deprecated and no longer maintained; the developers recommend migrating to TorchANI for production use. ASE-ANI requires Python 3.6, CUDA 9.2, and modern NVIDIA GPUs (compute capability ≥5.0) and only supports CHNO elements.
- ANI potentials are trained on small molecules; extrapolation to very large biomolecules (proteins >10 kDa) or inorganic clusters is not validated and may produce unreliable geometries.
- Ionization state generation at a fixed pH does not account for local microenvironments or conformer-dependent pKa shifts; manual specification of alternative adducts may be necessary for edge cases.
- Quantum calculations (QUICK) are computationally expensive and scale poorly beyond ~50 atoms; large metabolites may require approximations (e.g., reducing conformer ensemble size or using faster semiempirical methods).
- CCS predictions assume structures in the gas phase; interactions with drift gas or charge carriers in real IMS experiments are not modeled and may cause discrepancies with experimental values.

## Evidence

- [other] The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for quantum calculations.: "The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for"
- [intro] Workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on HPC systems.: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
- [readme] ANI-1x and ANI-1ccx potentials provide predictions for CHNO elements; ASE-ANI is a prototype interface for these potentials with ASE.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
- [readme] ASE-ANI is deprecated; developers recommend using TorchANI implementation.: "DEPRECATED and no longer supported, please use TorchANI implementation"
- [readme] Python 3.6, modern NVIDIA GPU with compute capability 5.0 or newer, CUDA 9.2, ASE, and optional MOPAC required.: "Python 3.6 (we recommend Anaconda distribution) * Modern NVIDIA GPU, compute capability 5.0 of newer. * CUDA 9.2"
- [readme] Workflow generates ccs.txt output file containing Boltzmann average CCS values from ensemble of conformations.: "the workflow will generate a `ccs.txt` file in the `ensemble` (or `ensemble_fast`) folder. The `ccs.txt` file contains the Boltzmann average CCS values computed using this workflow."
