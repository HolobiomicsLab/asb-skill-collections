---
name: tool-xml-wrapper-integration
description: Use when you have standalone metabolomics analysis tools (Python scripts, R packages, MATLAB compiled applications) that you want to expose through Galaxy's UI and make composable into reproducible workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - Python 2.7
  - R 3.0.1
  - MATLAB Compiler Runtime 8.3
  - Galaxy
  - R 3.0.1 (x86 64bit)
  - MATLAB Compiler Runtime (MCR) 8.3
  - MI-Pack (Metabolite Identification Package)
  - Galaxy-M
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
---

# tool-xml-wrapper-integration

## Summary

Integrate metabolomics analysis tools into Galaxy by mapping tool code and creating XML wrapper definitions that register tools with Galaxy's framework. This skill enables seamless execution of external command-line tools (Python, R, MATLAB) within Galaxy's web interface and workflow engine.

## When to use

You have standalone metabolomics analysis tools (Python scripts, R packages, MATLAB compiled applications) that you want to expose through Galaxy's UI and make composable into reproducible workflows. The tool folder structure must correspond to Galaxy's standard directory layout (tools/, configs/), and you need to target a specific Galaxy Master branch commit for reproducibility.

## When NOT to use

- Tool dependencies (Python 2.7, R 3.0.1, MATLAB Runtime 8.3) are not available or cannot be installed in the target environment.
- The target Galaxy version significantly differs from Master branch commit c429777c93680dcee449fe410f5360afbe673758 — version mismatches may cause XML parsing or configuration compatibility failures.
- Tool implementations are already natively integrated into Galaxy via Bioconda or the Galaxy Tool Shed, making manual XML wrapper creation redundant.

## Inputs

- Galaxy-M repository with tool implementations (GitHub release or commit)
- Target Galaxy installation directory (at Master branch commit c429777c93680dcee449fe410f5360afbe673758 or equivalent)
- Tool source code files (Python, R, or MATLAB compiled binaries)
- Tool XML wrapper definitions (.xml files defining inputs, parameters, outputs)

## Outputs

- Registered Galaxy tools accessible via Galaxy web interface
- Tool entries in Galaxy's tool registry and admin configuration
- Integrated metabolomics analysis workflow components
- Executable tool instances within Galaxy execution environment

## How to apply

First, obtain the Galaxy-M repository and identify the directory structure mapping to a standard Galaxy installation, including tool files, .xml wrapper definitions, and configuration files. Examine the .xml wrappers to understand how tool inputs, parameters, and outputs are declared in Galaxy's tool definition format. Copy tool implementation files and .xml wrappers into the corresponding Galaxy directories (e.g., tools/ for tool code, tools/*/static for auxiliary files). Copy Galaxy configuration files from Galaxy-M into the target Galaxy installation's config/ directory. Verify that all software dependencies (Python 2.7, R 3.0.1, MATLAB Compiler Runtime 8.3) are installed and accessible from the Galaxy execution environment. Restart the Galaxy service to reload tool definitions, then verify tool registration by checking Galaxy's admin interface or querying the tool registry to confirm metabolomics tools are listed and callable.

## Related tools

- **Galaxy** (Workflow platform and execution environment that reads XML tool definitions and coordinates tool execution; required installation at Master branch commit c429777c93680dcee449fe410f5360afbe673758) — https://github.com/galaxyproject/galaxy/
- **Python 2.7** (Runtime environment for tool wrapper scripts and Python-based metabolomics tool implementations) — https://www.python.org/download/releases/2.7/
- **R 3.0.1 (x86 64bit)** (Runtime environment for R-based metabolomics analysis tools and statistical computations) — http://cran.r-project.org/bin/windows/base/
- **MATLAB Compiler Runtime (MCR) 8.3** (Standalone library enabling execution of compiled MATLAB applications and metabolomics tools without MATLAB license) — http://uk.mathworks.com/supportfiles/downloads/R2014a/deployment_files/R2014a/installers/glnxa64/MCR_R2014a_glnxa64_installer.zip
- **MI-Pack (Metabolite Identification Package)** (Metabolomics-specific Python package providing metabolite identification functionality integrated into Galaxy-M tools) — https://github.com/Viant-Metabolomics/MI-Pack
- **Galaxy-M** (Reference implementation providing pre-built tool files, XML wrappers, and configuration files mapped to Galaxy directory structure) — https://github.com/Viant-Metabolomics/Galaxy-M

## Evaluation signals

- All metabolomics tools appear in Galaxy's admin interface under 'Manage Tools' and are marked as 'installed' or 'active'.
- Tools are selectable and executable from Galaxy's web UI without 404 or 'tool not found' errors.
- Tool XML definitions parse without validation errors (check Galaxy logs for XML schema violations).
- Workflow editor lists registered tools with correct input/output ports matching XML wrapper declarations.
- End-to-end test workflow execution succeeds: submit test data (e.g., mass spectrometry file) and verify output files are generated in expected format without runtime errors.

## Limitations

- Galaxy-M has been tested specifically on Master branch commit c429777c93680dcee449fe410f5360afbe673758; using significantly different Galaxy versions may introduce compatibility issues.
- MATLAB Compiler Runtime 8.3 installation can be problematic and version-sensitive; WINE (for running Windows MSFileReader on Linux) is notoriously difficult to configure correctly, particularly on 64-bit systems requiring 32-bit architecture enforcement.
- Tool installation and configuration is complex and involves multiple troubleshooting steps; the README recommends using the pre-installed virtual machine instead of manual recreation.
- No changelog is provided for Galaxy-M releases, making it difficult to track version-specific changes or debug integration issues across different releases.

## Evidence

- [intro] Required software dependencies and version specifications: "Galaxy-M deployment requires Python 2.7, R programming language 3.0.1 (x86 64bit), and MATLAB Compiler Runtime version 8.3, with tool files structured to correspond to folders in a standard Galaxy"
- [readme] Tool directory structure mapping to Galaxy installation: "The folders stored here corresond to folders found in a standard Galaxy installation. Included are the tool files (both original code and .xml wrappers) for Metabolomics analysis and the Galaxy"
- [readme] Specific Galaxy version requirement: "The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758."
- [other] Workflow for integrating tools: "Copy the Galaxy-M tool files and .xml wrapper definitions into the corresponding Galaxy tool directories (e.g., tools/, configs/). Copy Galaxy configuration files from Galaxy-M into the target Galaxy"
- [other] Verification procedure after integration: "Verify tool registration by checking Galaxy's admin interface or tool registry to confirm all metabolomics tools are listed and accessible."
- [readme] Complexity and recommendation for pre-built VM: "Installation instructions to recreate the virtual machine can be found below. They are quite complex and can involve a lot of troubleshooting, so it is advised to work direct from the virtual machine"
