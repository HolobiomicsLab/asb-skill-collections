---
name: nmrbox-environment-management
description: Use when when you need to deploy SAND for 1D NMR spectrum deconvolution
  on a new machine or cluster, or when testing code changes before merging into production.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - NMRBox
  - SAND
  - NMRPipe
  - SAND (Spectral Automatic NMR Deconvolution)
  - GACRC
  techniques:
  - NMR
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.3c03078
  title: SAND
evidence_spans:
- latest interface to NMRBox (SAND_V7)
- Any user is welcome to make new modificaitons on the SAND code, particularly its
  version for NMRBox
- interface to NMRPipe (pipe_scripts/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sand_cq
    doi: 10.1021/acs.analchem.3c03078
    title: SAND
  dedup_kept_from: coll_sand_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03078
  all_source_dois:
  - 10.1021/acs.analchem.3c03078
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmrbox-environment-management

## Summary

Set up and configure the NMRBox computational environment to run SAND and related NMR processing tools. This skill ensures reproducible execution of automatic NMR deconvolution workflows across local, HPC, and cloud platforms.

## When to use

When you need to deploy SAND for 1D NMR spectrum deconvolution on a new machine or cluster, or when testing code changes before merging into production. Apply this skill if you are starting fresh with SAND_V7 on NMRBox, or if you need to validate updates against a test NMRBox server environment.

## When NOT to use

- If you only need to run SAND on already-configured shared HPC or NMRBox infrastructure — environment setup has already been performed.
- If your input is already a peak table or processed NMR output; this skill addresses environment provisioning, not peak generation itself.
- If you do not have shell access or administrative permissions to install software on your target machine.

## Inputs

- NMRBox installation script (install_SAND.sh)
- Updated SAND code repository (optional, for testing)
- System specifications and access credentials (local, HPC, or NMRBox cloud)

## Outputs

- Configured NMRBox environment with SAND_V7 installed and executable
- Test results confirming environment readiness
- Access path to SAND executables (/usr/software/sand or equivalent)

## How to apply

Follow the NMRBox installation script located at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh to set up the environment. Request a test NMRBox server if you are testing code updates. Copy your updated code into /usr/software/sand within the test environment and run the provided test examples to verify correct installation and functionality. For production deployments, SAND works on local machines, HPC systems (e.g., GACRC), or NMRBox cloud services; choose the deployment target based on data size and compute requirements. After successful test execution, merge changes into the main branch.

## Related tools

- **NMRBox** (Computational platform that hosts and runs SAND; provides virtualized NMR software environment accessible locally, on HPC, or via cloud service) — https://nmrbox.org
- **SAND (Spectral Automatic NMR Deconvolution)** (NMR processing tool installed and configured within the NMRBox environment to perform automatic 1D spectrum deconvolution) — https://github.com/edisonomics/SAND
- **NMRPipe** (NMR data processing utility interfaced by SAND via pipe_scripts/ for spectrum manipulation)
- **GACRC** (HPC cluster option for running SAND on larger datasets requiring distributed compute) — https://gacrc.uga.edu

## Evaluation signals

- SAND installation script completes without errors and outputs confirmation of successful installation.
- Running test examples (as specified in the installation documentation) produces valid NMR peak-table outputs in the expected format.
- Environment variable PATH or module system correctly resolves SAND and NMRPipe executables when invoked from shell.
- Deployment on local, HPC, and NMRBox cloud platforms all execute the same test workflow and produce identical peak-table outputs (reproducibility across platforms).
- After code update, test NMRBox server environment passes all test cases before merge authorization is granted.

## Limitations

- No changelog documentation is provided with SAND; version changes and updates are not formally documented.
- SAND has been tested only on urine and worm NMR datasets; applicability to other experimental datasets or NMR data types is planned but not yet validated.
- Environment management is specific to NMRBox, GACRC, and local installs; deployment on other HPC systems or cloud providers may require additional configuration not covered by the install script.

## Evidence

- [other] Set up the NMRBox environment and install SAND_V7 by following the installation script at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh.: "Set up the NMRBox environment and install SAND_V7 by following the installation script at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh."
- [intro] SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org).: "SAND works locally, on HPC ([GACRC](https://gacrc.uga.edu)), and on services like [NMRBox](https://nmrbox.org)."
- [methods] the user need to request test NMRBox sever, copy updated codes into /usr/software/sand, and run the test examples: "the user need to request test NMRBox sever, copy updated codes into /usr/software/sand, and run the test examples"
- [readme] We provide multiple [tutorials](https://github.com/edisonomics/SAND/tree/main/tutorial) on installation and running.: "We provide multiple [tutorials](https://github.com/edisonomics/SAND/tree/main/tutorial) on installation and running."
- [methods] latest interface to NMRBox (SAND_V7), and interface to NMRPipe: "latest interface to NMRBox (SAND_V7), and interface to NMRPipe"
