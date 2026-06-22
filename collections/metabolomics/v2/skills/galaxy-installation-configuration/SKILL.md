---
name: galaxy-installation-configuration
description: Use when you have a Galaxy Master branch installation (or specific commit c429777c93680dcee449fe410f5360afbe673758) and need to add metabolomics tools from Galaxy-M.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Galaxy
  - Python 2.7
  - R 3.0.1
  - MATLAB Compiler Runtime 8.3
  - Galaxy-M
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1186/s13742-016-0115-8
  title: Galaxy-M
evidence_spans:
- Metabolomics Tools for [Galaxy](http://galaxyproject.org/)
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

# galaxy-installation-configuration

## Summary

Deploy Galaxy with integrated metabolomics analysis tools by mapping Galaxy-M repository structure to a target Galaxy installation, installing required language runtimes and dependencies, and registering tool definitions. This skill is essential when setting up a Galaxy server to support specialized metabolomics workflows.

## When to use

You have a Galaxy Master branch installation (or specific commit c429777c93680dcee449fe410f5360afbe673758) and need to add metabolomics tools from Galaxy-M. Use this skill when you possess the Galaxy-M repository and need to integrate its tool files, XML wrappers, and configuration into an existing or new Galaxy instance to enable metabolite identification and mass spectrometry analysis pipelines.

## When NOT to use

- Your Galaxy installation is on a different or incompatible branch/commit; version mismatch may cause tool registration failures or runtime errors.
- Required runtime dependencies (Python 2.7, R 3.0.1 x86 64bit, MATLAB Compiler Runtime 8.3) are not available or cannot be installed on your system.
- You do not have write access to Galaxy's tool and config directories, or lack permissions to restart the Galaxy service.

## Inputs

- Galaxy-M repository (from github.com/Viant-Metabolomics/Galaxy-M)
- Galaxy installation at Master branch commit c429777c93680dcee449fe410f5360afbe673758
- Galaxy tool and config directory paths

## Outputs

- Integrated Galaxy installation with metabolomics tools registered and accessible
- Tool definitions loaded in Galaxy admin interface
- Metabolomics analysis workflows available in Galaxy UI

## How to apply

First, verify your Galaxy installation matches the tested version (Master branch commit c429777c93680dcee449fe410f5360afbe673758) and that Python 2.7, R 3.0.1 (x86 64bit), and MATLAB Compiler Runtime 8.3 are installed on the system. Clone or obtain the Galaxy-M repository from github.com/Viant-Metabolomics/Galaxy-M at the desired release. Examine the repository directory structure, which mirrors a standard Galaxy installation layout (tool files, .xml wrappers, configuration files). Copy Galaxy-M tool files and XML wrapper definitions into your Galaxy installation's tool directories (e.g., tools/, configs/). Copy all Galaxy configuration files from Galaxy-M into the target installation's config/ directory. Restart the Galaxy service to reload tool definitions. Verify tool registration by checking the Galaxy admin interface or querying the tool registry to confirm all metabolomics tools are listed and accessible.

## Related tools

- **Galaxy** (Server framework that hosts and orchestrates metabolomics tool execution and UI) — http://galaxyproject.org/
- **Galaxy-M** (Metabolomics tool package containing tool files, XML wrappers, and configuration files to integrate into Galaxy) — https://github.com/Viant-Metabolomics/Galaxy-M
- **Python 2.7** (Runtime required by Galaxy and metabolomics tool scripts) — https://www.python.org/download/releases/2.7/
- **R 3.0.1** (Statistical computing language required by R-based metabolomics analysis tools) — http://cran.r-project.org/bin/windows/base/
- **MATLAB Compiler Runtime 8.3** (Enables execution of compiled MATLAB applications used in metabolomics tools) — http://uk.mathworks.com/supportfiles/downloads/R2014a/deployment_files/R2014a/installers/glnxa64/MCR_R2014a_glnxa64_installer.zip

## Examples

```
cd ~ && git clone https://github.com/galaxyproject/galaxy/ && cd galaxy && git checkout -b master origin/master && git checkout c429777c93680dcee449fe410f5360afbe673758 && cp -r ~/Galaxy-M/tools/* ./tools/ && cp -r ~/Galaxy-M/config/* ./config/ && ./scripts/galaxy.py
```

## Evaluation signals

- Galaxy admin interface displays all metabolomics tools as registered and enabled, with no error flags or missing dependencies.
- Tool registry query returns complete list of Galaxy-M tools with correct XML wrapper definitions and parameter sets.
- Galaxy service restarts without errors and does not log any tool loading or registration failures.
- Metabolomics workflows can be created in Galaxy UI and tools appear in the tool search and sidebar panels.
- Test execution of a metabolomics tool (e.g., a simple metabolite identification workflow) completes without runtime errors.

## Limitations

- Installation is tightly coupled to a specific Galaxy commit (c429777c93680dcee449fe410f5360afbe673758); newer Galaxy versions may introduce incompatibilities with XML wrapper syntax or configuration file format.
- Python 2.7, R 3.0.1, and MATLAB Compiler Runtime 8.3 are legacy software versions and may not run on modern operating systems or architectures without compatibility layers.
- The README notes that installation instructions are 'quite complex and can involve a lot of troubleshooting', particularly around WINE configuration for Windows package deployment in a Linux environment.
- MSFileReader package requires registration and download from Thermo Scientific; licensing restrictions may apply for non-academic use despite the stated 'no restrictions' license.

## Evidence

- [other] Galaxy-M deployment requires Python 2.7, R programming language 3.0.1 (x86 64bit), and MATLAB Compiler Runtime version 8.3: "Galaxy-M deployment requires Python 2.7, R programming language 3.0.1 (x86 64bit), and MATLAB Compiler Runtime version 8.3"
- [readme] The folders stored here correspond to folders found in a standard Galaxy installation. Included are the tool files (both original code and .xml wrappers) for Metabolomics analysis and the Galaxy config files from a working installation of Galaxy.: "The folders stored here corresond to folders found in a standard Galaxy installation. Included are the tool files (both original code and .xml wrappers) for Metabolomics analysis and the Galaxy"
- [readme] The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758: "The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758"
- [other] Verify tool registration by checking Galaxy's admin interface or tool registry to confirm all metabolomics tools are listed and accessible.: "Verify tool registration by checking Galaxy's admin interface or tool registry to confirm all metabolomics tools are listed and accessible"
- [readme] These are quite complex and can involve a lot of troubleshooting, so it is advised to work direct from the virtual machine where possible.: "These are quite complex and can involve a lot of troubleshooting, so it is advised to work direct from the virtual machine where possible"
