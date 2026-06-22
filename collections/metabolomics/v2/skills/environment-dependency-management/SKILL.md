---
name: environment-dependency-management
description: Use when when deploying Galaxy-M or similar multi-component metabolomics platforms that depend on heterogeneous runtime environments (Python, R, MATLAB, WINE) across multiple operating systems (Ubuntu 14.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python 2.7
  - R 3.0.1
  - MATLAB Compiler Runtime 8.3
  - Galaxy
  - Python
  - R
  - MATLAB Compiler Runtime (MCR)
  - WINE
  - MSFileReader
  - MI-Pack
  - winetricks
  techniques:
  - LC-MS
  - direct-infusion-MS
  - MS-imaging
derived_from:
- doi: 10.1186/s13742-016-0115-8
  title: Galaxy-M
evidence_spans:
- '[Python (version 2.7)](https://www.python.org/download/releases/2.7/)'
- '[R programming language (version 3.0.1, x86 64bit)](http://cran.r-project.org/bin/windows/base/)'
- '[MATLAB Compiler Runtime (MCR) (version 8.3)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_galaxy_m_cq
    doi: 10.1186/s13742-016-0115-8
    title: Galaxy-M
  dedup_kept_from: coll_galaxy_m_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13742-016-0115-8
  all_source_dois:
  - 10.1186/s13742-016-0115-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# environment-dependency-management

## Summary

Identify, document, and configure all software dependencies (language runtimes, compilers, third-party libraries, optional tools) required to deploy a complex bioinformatics platform into a target computing environment. This skill ensures reproducible installation by pinning versions, validating compatibility matrices, and automating environment reconstruction.

## When to use

When deploying Galaxy-M or similar multi-component metabolomics platforms that depend on heterogeneous runtime environments (Python, R, MATLAB, WINE) across multiple operating systems (Ubuntu 14.04 LTS 64-bit, Windows), especially when: (1) the original development environment differs from the target deployment environment; (2) tool functionality depends on specific compiled binaries or Windows-only libraries (MSFileReader); (3) reproducibility requires pinning to exact commits or versions; (4) 32-bit vs. 64-bit architecture choices affect library loading or system calls.

## When NOT to use

- When the target platform is already pre-configured with all dependencies (e.g., a pre-built Docker image or VM provided by the authors); this skill would be redundant.
- When deploying only pure-Python or single-language tools that have no compiled dependencies or architecture constraints; simpler dependency declaration suffices.
- When the project provides no documentation of tested versions or environment details; you would need to reverse-engineer or contact maintainers instead.

## Inputs

- Project README or installation documentation (plain text or Markdown)
- Git repository metadata (commit hashes, branch information)
- Target OS specification (e.g., Ubuntu 14.04 LTS 64-bit)
- Project source tree or release archive

## Outputs

- Validated dependency matrix (tool name, version, architecture, optional/required flag)
- Sequenced installation workflow with version-pinned commands
- Environment snapshot (virtual machine VMDK + metadata files, or container image)
- Verified tool registry showing all deployed tools are accessible

## How to apply

First, extract the explicit dependency matrix from the project README or documentation, recording each runtime, library, and its tested version (e.g., Python 2.7, R 3.0.1 x86 64-bit, MATLAB Compiler Runtime 8.3, WINE 1.7). Second, identify conditional or optional dependencies (e.g., MATLAB 2014a and PLS-Toolbox 8.0.2 for development only; Parallel Python for multi-core speedup but not required). Third, trace architecture constraints: Galaxy-M requires forcing WINE into 32-bit mode by removing the .wine folder and setting WINEARCH=win32, which is non-obvious and failure-prone if missed. Fourth, install dependencies in order of dependency graph (OS packages first via apt-get, then WINE and its Windows packages via msiexec, then Python packages via setup.py). Fifth, test each layer incrementally (e.g., verify MSFileReader registration in WINE using winetricks vcrun2008 before attempting tool execution). Finally, document the Git commit hash of the validated environment (e.g., Galaxy Master commit c429777c93680dcee449fe410f5360afbe673758) and package it as a virtual machine snapshot or container to enable deterministic re-deployment.

## Related tools

- **Galaxy** (Target bioinformatics platform into which metabolomics tools are deployed) — https://github.com/galaxyproject/galaxy
- **Python** (Runtime environment for tool scripts and setup.py installation)
- **R** (Runtime environment for statistical metabolomics analysis tools)
- **MATLAB Compiler Runtime (MCR)** (Standalone shared libraries enabling execution of compiled MATLAB tools without MATLAB license) — http://uk.mathworks.com/supportfiles/downloads/R2014a/deployment_files/R2014a/installers/glnxa64/MCR_R2014a_glnxa64_installer.zip
- **WINE** (Windows emulation layer enabling execution of Windows-only dependencies (MSFileReader, SimStitch) on Linux) — https://www.winehq.org/download/ubuntu
- **MSFileReader** (Thermo Scientific Windows package for reading DIMS mass spectrometry data; requires registration and 32-bit WINE installation) — https://thermo.flexnetoperations.com
- **MI-Pack** (Python package for metabolite identification; installed via setup.py after cloning from repository) — https://github.com/Viant-Metabolomics/MI-Pack
- **winetricks** (Utility to install Visual C runtime dependencies into WINE)

## Examples

```
git clone https://github.com/galaxyproject/galaxy/ && cd galaxy && git checkout -b master origin/master && git checkout c429777c93680dcee449fe410f5360afbe673758 && cd ~/MI-Pack && sudo python setup.py install && export WINEARCH=win32 && wine msiexec /i python-2.7.8.msi && winetricks vcrun2008
```

## Evaluation signals

- All declared dependencies (Python 2.7, R 3.0.1 x86 64-bit, MATLAB MCR 8.3, WINE 1.7) install without errors and are discoverable via system PATH or LD_LIBRARY_PATH.
- Galaxy admin interface or tool registry displays all Galaxy-M metabolomics tools as registered and accessible (not grayed out or showing dependency errors).
- WINE is confirmed to be running in 32-bit mode (WINEARCH=win32 is set and .wine folder is clean) and can execute MSFileReader.exe without 'Invalid file identifier' errors.
- Test data from ~/GalaxyM-TestData/LCMS_DATA and ~/GalaxyM-TestData/DIMS_DATA can be processed through deployed workflows without missing-library or version-mismatch errors.
- Git commit hash of the deployed Galaxy instance matches the tested commit c429777c93680dcee449fe410f5360afbe673758 (or documented compatibility matrix is verified).

## Limitations

- WINE+Python2.7 interaction is platform-dependent and 'notoriously difficult'; 32-bit vs. 64-bit architecture mismatches silently cause tool failures (e.g., SimStitch 'Invalid file identifier' errors) that are hard to diagnose without explicit WINEARCH configuration.
- MSFileReader requires manual registration with Thermo Scientific and download authorization; this introduces a human bottleneck and potential licensing compliance issues.
- Installation is complex, multi-step, and error-prone; authors explicitly recommend using the pre-built virtual machine snapshot rather than manual installation due to troubleshooting burden.
- Tested versions (Python 2.7, R 3.0.1, MCR 8.3) are aging; forward compatibility with modern OS distributions (Ubuntu 20.04+, Python 3.x) is not guaranteed.
- Optional dependencies (MATLAB 2014a, PLS-Toolbox 8.0.2) are proprietary and expensive; users without licenses cannot develop or modify certain tools.

## Evidence

- [readme] Dependency matrix extraction: "Programming languages (versions given were used for development, other versions may also be compatible): Python (version 2.7), R programming language (version 3.0.1, x86 64bit), MATLAB Compiler"
- [readme] Galaxy version pinning: "The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758."
- [readme] Architecture constraint and failure mode: "IMPORTANT: You must force wine to install everything in 32bit mode. In order to get WINE to run in 32bit, remove the .wine folder in your home directory (or move it to e.g. ~/.wine_backup) which will"
- [readme] Sequenced installation workflow: "Install packages: python2.7... Install packages: numpy... Install packages: scipy... Install packages: comtypes... Install software: MSFileReader 3.0 sp2... Install visual C using winetricks"
- [readme] VM-based environment snapshot rationale: "Installation instructions to recreate the virtual machine can be found below. They are quite complex and can involve a lot of troubleshooting, so it is advised to work direct from the virtual machine"
- [readme] Optional vs. required dependencies: "Matlab (version 2014a) (Optional: tool development and use of most recent source code), PLS-Toolbox for PCA tools (version 8.0.2) (Optional: tool development and use of most recent source code)"
