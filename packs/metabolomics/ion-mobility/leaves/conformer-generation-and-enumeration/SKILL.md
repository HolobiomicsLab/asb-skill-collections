---
name: conformer-generation-and-enumeration
description: Use when you have SMILES strings of molecules at specific ionization states (e.g., protonated or deprotonated adducts) and need to predict collision cross section values for mass spectrometry-based metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0488
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3292
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

# conformer-generation-and-enumeration

## Summary

Generate and enumerate three-dimensional conformations for ionized molecular species to prepare for quantum mechanical property prediction. This skill creates multiple low-energy structural variants needed for accurate collisional cross section (CCS) calculations in metabolite annotation workflows.

## When to use

Apply this skill when you have SMILES strings of molecules at specific ionization states (e.g., protonated or deprotonated adducts) and need to predict collision cross section values for mass spectrometry-based metabolite annotation. You must perform conformer generation after ionization state determination but before filtering and quantum calculations.

## When NOT to use

- Input molecules are already fully optimized 3D structures (PDB or MOL format); skip directly to filtering or quantum calculation steps.
- The target molecules contain elements outside CHNO (RDKit handles these, but ASE-ANI filtering is limited to CHNO; you must substitute an alternative filter model).
- You are predicting properties that do not depend on conformational ensemble variation (e.g., exact mass or molecular formula); a single representative structure suffices.

## Inputs

- SMILES strings with assigned ionization states (protonated/deprotonated adducts)

## Outputs

- Conformer ensembles (3D structural variants per adduct)
- Filtered low-energy conformations ready for quantum mechanical calculations

## How to apply

Use RDKit to generate multiple three-dimensional conformations for each ionized SMILES input. The workflow generates a conformational ensemble per adduct, then retains low-energy structures using the ASE-ANI machine learning model before passing filtered conformations to quantum mechanical calculations (QUICK). The rationale is that CCS values depend on molecular geometry; multiple conformations account for thermal population and structural flexibility at physiological conditions. Filtering with ASE-ANI reduces computational burden by eliminating high-energy, unlikely structures before expensive quantum steps.

## Related tools

- **RDKit** (Conformation generation from SMILES; produces 3D coordinate sets for each ionization state) — https://www.rdkit.org
- **ASE-ANI** (Machine learning–based conformation filtering to retain low-energy structures; removes unlikely high-energy conformers before quantum calculations) — https://github.com/isayev/ASE_ANI
- **Dimorphite-DL** (Upstream step: ionization state determination that precedes conformer generation) — https://durrantlab.pitt.edu/dimorphite-dl
- **Snakemake** (Workflow orchestration and parallelization of conformer generation and filtering across multiple adducts and HPC systems) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
bash scheduler.sh  # After configuring paths.json (RDKit, ASE-ANI paths), cluster.yaml (HPC walltime/memory), and arguments.json (input SMILES file) in the snakemake_ccs workflow directory, execute the scheduler to generate and filter conformations.
```

## Evaluation signals

- Conformer ensemble size per adduct is > 1 and consistent across similar molecules (verify non-empty structure sets generated for each ionized SMILES).
- Filtered conformations exhibit lower energies than the full ensemble (ASE-ANI scores or energies should show monotonic reduction after filtering step).
- Filtered conformations pass element composition validation (all atoms remain within CHNO when using ASE-ANI; no structural corruption).
- Downstream quantum calculations (QUICK) converge on filtered conformations without geometry errors or unrealistic bond lengths.
- Final CCS predictions cluster around expected literature or experimental ranges for known metabolites (indicates biologically plausible conformations were retained).

## Limitations

- ASE-ANI filtering is limited to organic molecules containing C, H, N, O elements only; extension to S, F, Cl, or other heavy atoms requires alternative ML potentials (e.g., TorchANI or custom retrained ASE-ANI).
- RDKit conformation generation is stochastic; running the same SMILES twice may yield different ensemble compositions due to random seed variation. Reproducibility requires explicit seed control.
- The workflow assumes adequate computational resources for parallelized conformer generation and filtering on HPC systems; single-node execution may be prohibitively slow for large SMILES batches.
- ASE-ANI is deprecated as of the README notice; the authors recommend migrating to the TorchANI implementation for ongoing maintenance and GPU compatibility beyond CUDA 9.2.

## Evidence

- [intro] RDKit for conformation generation and ASE-ANI for filtering: "Generate conformations for each ionization state using RDKit. Filter conformations using ASE-ANI machine learning model to retain low-energy structures."
- [other] Multi-step workflow integrating ionization, generation, filtering, and quantum steps: "Determine ionization states (protonated/deprotonated adducts) using Dimorphite-DL for each SMILES. Generate conformations for each ionization state using RDKit. Filter conformations using ASE-ANI"
- [intro] Purpose: CCS prediction for metabolite annotation: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation"
- [readme] ASE-ANI element limitations: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
- [readme] ASE-ANI deprecation notice: "DEPRECATED and no longer supported, please use TorchANI implementation"
