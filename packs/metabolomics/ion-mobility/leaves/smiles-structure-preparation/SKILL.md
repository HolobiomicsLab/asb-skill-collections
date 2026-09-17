---
name: smiles-structure-preparation
description: Use when you have a SMILES input file of small organic molecules and
  need to predict their collision cross sections or other molecular properties via
  quantum mechanics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0361
  edam_topics:
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_0154
  tools:
  - Snakemake
  - Dimorphite-DL
  - ASE-ANI
  - QUICK
  - RDKit
  techniques:
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional
  cross sections (CCS)
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

# SMILES Structure Preparation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Prepare and standardize molecular structures from SMILES notation by determining ionization states and generating conformations for subsequent computational chemistry workflows. This skill is essential when beginning an in silico collision cross section (CCS) prediction pipeline where molecular input must be chemically contextualized before quantum mechanical calculations.

## When to use

Apply this skill when you have a SMILES input file of small organic molecules and need to predict their collision cross sections or other molecular properties via quantum mechanics. The skill is triggered by the requirement to handle multiple ionization states (protonated/deprotonated adducts) and generate low-energy 3D conformations prior to quantum calculations, especially in metabolomics annotation workflows where accurate CCS values depend on correct chemical state representation.

## When NOT to use

- Input molecules contain elements outside the scope of your chosen ASE-ANI model (e.g., metals, halogens beyond Cl for ANI-1x/ANI-1ccx)
- You already have 3D structures with pre-computed ionization states; this skill is redundant for already-prepared conformational ensembles
- The target molecules are large polymers or proteins; SMILES preparation and RDKit conformation generation are designed for small organic molecules

## Inputs

- SMILES string or SMILES input file (plain text, one structure per line or in tabular format)
- pH or ionization state specification (default: physiological pH ~7.4)
- Atom composition specification for ASE-ANI model selection (CHNO, CHNOSFCl, etc.)

## Outputs

- List of ionization state variants (protonated/deprotonated adducts) with corresponding SMILES
- 3D conformation files (typically .xyz, .mol, or ASE-compatible formats) for each adduct
- Filtered conformation ensemble with computed energies from ASE-ANI
- Metadata table mapping SMILES → adduct → conformation → energy

## How to apply

First, prepare a plain-text SMILES input file containing one or more molecular structures. Use Dimorphite-DL to automatically determine all relevant ionization states (protonated and deprotonated adducts) for each SMILES at physiological pH, producing a standardized list of chemical variants. Next, use RDKit to generate multiple conformations for each ionization state using distance geometry and force-field-based optimization. Filter the generated conformations using the ASE-ANI machine learning potential (ANI-1x or ANI-1ccx for CHNO elements) to retain only low-energy structures, discarding high-energy outliers. This filtering step reduces computational cost for the downstream quantum mechanical phase while preserving structural diversity. The output is a curated set of conformations per adduct ready for QUICK quantum calculations.

## Related tools

- **Dimorphite-DL** (Determine ionization states (protonated/deprotonated adducts) for each SMILES at specified pH) — https://durrantlab.pitt.edu/dimorphite-dl
- **RDKit** (Generate 3D conformations for each ionization state using distance geometry and force-field optimization) — https://www.rdkit.org
- **ASE-ANI** (Filter and rank conformations using neural network potential energy prediction (ANI-1x or ANI-1ccx) to retain low-energy structures) — https://github.com/isayev/ASE_ANI
- **Snakemake** (Orchestrate the full workflow pipeline from SMILES input through ionization, conformation generation, and filtering with HPC parallelization) — https://github.com/DasSusanta/snakemake_ccs

## Examples

```
bash scheduler.sh  # After configuring paths.json, cluster.yaml, and arguments.json with SMILES input file path and ionization/conformation parameters
```

## Evaluation signals

- All input SMILES are successfully parsed and produce at least one valid ionization state variant (check Dimorphite-DL output for non-null adducts)
- Conformations are generated for every ionization state, with 3D coordinates properly embedded in output files (verify .xyz or .mol file validity and atom count consistency with SMILES)
- ASE-ANI filtering reduces the conformation pool by ≥50% while preserving structural diversity (compare count before/after; check that energy range is physically plausible, typically −10 to −100 eV for organic CHNO molecules)
- No SMILES or conformation is lost during the preparation pipeline; final ensemble size matches expected cardinality (n_input_smiles × n_adducts_per_smiles × n_retained_conformations_per_adduct)
- Energy ordering is consistent: lowest-energy conformers of a given adduct appear first in ranked output; no inverted or NaN energies

## Limitations

- ASE-ANI models are restricted to CHNO elements in ANI-1x/ANI-1ccx; molecules containing S, F, Cl, or other heteroatoms require ANI-2x or alternative filtering methods
- NVIDIA GPU with compute capability ≥5.0 and CUDA 9.2+ is required for ASE-ANI; CPU-only runs are not supported by the original ASE-ANI repository
- ASE-ANI is deprecated and no longer officially supported; the maintainers recommend migrating to TorchANI for long-term compatibility
- RDKit conformation generation is stochastic; different random seeds may yield different conformational ensembles, introducing variability in downstream quantum results
- Ionization state determination assumes physiological pH (or user-specified pH); non-standard pH values or explicit specification of unusual protonation states require manual override

## Evidence

- [other] The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for quantum calculations.: "The workflow integrates four sequential computational steps: Dimorphite-DL for ionization state determination, RDKit for conformation generation, ASE-ANI for conformation filtering, and QUICK for"
- [other] Determine ionization states (protonated/deprotonated adducts) using Dimorphite-DL for each SMILES.: "Determine ionization states (protonated/deprotonated adducts) using Dimorphite-DL for each SMILES."
- [other] Generate conformations for each ionization state using RDKit.: "Generate conformations for each ionization state using RDKit."
- [other] Filter conformations using ASE-ANI machine learning model to retain low-energy structures.: "Filter conformations using ASE-ANI machine learning model to retain low-energy structures."
- [readme] This is a prototype interface for ANI-1x and ANI-1ccx neural network potentials for The Atomic Simulation Environment (ASE). Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements.: "Current ANI-1x and ANI-1ccx potentials provide predictions for the CHNO elements."
- [readme] workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems: "workflow allows users to predict CCS values for multiple protonated/deprotonated adducts and models with high automation and parallelized computation on high-performance computing (HPC) systems"
- [readme] Dimorphite-DL: For ionization state determination: "Dimorphite-DL: For ionization state determination. Available at: [https://durrantlab.pitt.edu/dimorphite-dl]"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use [TorchANI](https://github.com/aiqm/torchani) implementation"
