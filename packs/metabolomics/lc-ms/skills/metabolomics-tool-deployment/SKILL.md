---
name: metabolomics-tool-deployment
description: Use when you have a Galaxy installation (specifically Galaxy Master branch commit c429777c93680dcee449fe410f5360afbe673758 or compatible) and need to add metabolomics analysis capabilities including tools for XCMS integration, mass spectrometry file reading (via MSFileReader), and metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - Python 2.7
  - R 3.0.1
  - MATLAB Compiler Runtime 8.3
  - Galaxy
  - R 3.0.1 (x86 64bit)
  - MSFileReader 3.0 sp2
  - WineHQ 1.7
  - MI-Pack (Metabolite Identification Package)
  - XCMS
  techniques:
  - LC-MS
  - direct-infusion-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-tool-deployment

## Summary

Deploy Galaxy-M metabolomics analysis tools into a Galaxy installation by mapping tool files, XML wrappers, and configuration files from the Galaxy-M repository to the target Galaxy directory structure. This skill is essential when extending a Galaxy instance with pre-built metabolomics workflows for LC-MS, DIMS, and related mass spectrometry data processing.

## When to use

You have a Galaxy installation (specifically Galaxy Master branch commit c429777c93680dcee449fe410f5360afbe673758 or compatible) and need to add metabolomics analysis capabilities including tools for XCMS integration, mass spectrometry file reading (via MSFileReader), and metabolite identification. This is the right choice when you are setting up a shared Galaxy server or virtual machine for metabolomics data analysis and want to preserve reproducibility through a tested, versioned tool set.

## When NOT to use

- Your Galaxy installation is at a different commit or branch than c429777c93680dcee449fe410f5360afbe673758, and you have not validated compatibility—deployment may fail silently or produce runtime errors.
- You lack the required system dependencies (Python 2.7, R 3.0.1 x86 64bit, MATLAB Compiler Runtime 8.3, WineHQ 1.7 for MSFileReader on Linux) before attempting tool deployment—tools will register but fail at execution.
- You are deploying into Galaxy 19.x or later (Python 3 only), as Galaxy-M is explicitly built for Python 2.7 and will not function.

## Inputs

- Galaxy-M repository (GitHub release or clone from github.com/Viant-Metabolomics/Galaxy-M)
- Existing Galaxy installation at Master branch commit c429777c93680dcee449fe410f5360afbe673758
- Tool XML wrapper definitions from Galaxy-M
- Galaxy configuration files from Galaxy-M

## Outputs

- Deployed Galaxy tool directory (tools/) with metabolomics tool files and executables
- Registered Galaxy tool XML definitions accessible in Galaxy tool panel
- Updated Galaxy configuration files (config/) for metabolomics-specific settings
- Verified tool registry entries in Galaxy admin interface

## How to apply

First, verify your Galaxy installation matches the tested commit c429777c93680dcee449fe410f5360afbe673758, or document any divergence. Clone or download the Galaxy-M repository at the appropriate release from github.com/Viant-Metabolomics/Galaxy-M. Inspect the Galaxy-M directory structure to identify tool files (both source code and .xml wrapper definitions) and configuration files. Map each Galaxy-M subdirectory to the corresponding directory in your Galaxy installation (e.g., Galaxy-M/tools/* → Galaxy/tools/*, Galaxy-M/config/* → Galaxy/config/*). Copy all tool files and XML wrapper definitions into Galaxy's tool directories, then copy Galaxy configuration files into Galaxy's config/ directory. Restart the Galaxy service to reload and register the tool definitions. Verify successful deployment by navigating to Galaxy's admin interface and confirming that all metabolomics tools appear in the tool registry and are accessible in the workflow editor.

## Related tools

- **Galaxy** (Container platform for tool registration, execution, and workflow management) — http://galaxyproject.org/
- **Python 2.7** (Runtime for Galaxy-M tool scripts and wrappers) — https://www.python.org/download/releases/2.7/
- **R 3.0.1 (x86 64bit)** (Statistical computing runtime for metabolomics analysis tools within Galaxy-M) — http://cran.r-project.org/bin/windows/base/
- **MATLAB Compiler Runtime 8.3** (Runtime for compiled MATLAB executables bundled in Galaxy-M releases) — http://uk.mathworks.com/supportfiles/downloads/R2014a/deployment_files/R2014a/installers/glnxa64/MCR_R2014a_glnxa64_installer.zip
- **MSFileReader 3.0 sp2** (Thermo Scientific tool for reading proprietary mass spectrometry data files in DIMS workflows) — https://thermo.flexnetoperations.com
- **WineHQ 1.7** (Windows compatibility layer on Linux for executing MSFileReader and related Windows-only components) — winehq.org
- **MI-Pack (Metabolite Identification Package)** (Metabolite identification library integrated into Galaxy-M tools for empirical formula search and compound lookup) — https://github.com/Viant-Metabolomics/MI-Pack
- **XCMS** (Chromatography and mass spectrometry data processing referenced by Galaxy-M LC-MS workflows) — https://metlin.scripps.edu/xcms/

## Examples

```
git clone https://github.com/Viant-Metabolomics/Galaxy-M.git && cd Galaxy-M && cp -r tools/* ~/galaxy/tools/ && cp -r config/* ~/galaxy/config/ && ~/galaxy/run.sh
```

## Evaluation signals

- All Galaxy-M tool XML wrappers appear in Galaxy's tool panel and workflow editor without registration errors.
- Galaxy admin interface (Admin > Manage installed tools) lists all metabolomics tools with status 'installed' and no error messages.
- Tool icons, descriptions, and input/output ports render correctly in the Galaxy workflow canvas.
- A test workflow using LC-MS or DIMS data completes without 'tool not found' or 'command not recognized' errors.
- Galaxy service restart completes without errors in Galaxy logs (logs/galaxy.log); no warnings about malformed tool XML or missing dependencies.

## Limitations

- Galaxy-M has been tested only on Galaxy Master branch commit c429777c93680dcee449fe410f5360afbe673758; newer or older Galaxy versions may have incompatible tool XML schemas or deprecated APIs.
- Python 2.7, R 3.0.1, and MATLAB Compiler Runtime 8.3 are now end-of-life and may have security vulnerabilities; deployment into production systems should be evaluated for risk.
- MSFileReader and related Windows-only components require WineHQ 1.7 on Linux and must be explicitly forced to 32-bit mode (WINEARCH=win32) to function correctly; 64-bit installations will fail with 'Invalid file identifier' errors.
- The virtual machine snapshot is tied to the GigaScience publication and uses a specific MI-Pack commit (06ce0ace643ee1cf1d27550769a5272b7ea50825); updating MI-Pack or Galaxy independently may break published workflows.
- Installation involves significant manual steps (WINE configuration, MSFileReader registration, Python package setup) and is described as 'quite complex' with 'a lot of troubleshooting' needed; scripted or containerized deployment is not provided.

## Evidence

- [intro] Galaxy-M deployment requires Python 2.7, R programming language 3.0.1 (x86 64bit), and MATLAB Compiler Runtime version 8.3: "Python (version 2.7), R programming language (version 3.0.1, x86 64bit), MATLAB Compiler Runtime (MCR) (version 8.3)"
- [readme] Tool files are structured to correspond to folders in a standard Galaxy installation: "The folders stored here corresond to folders found in a standard Galaxy installation. Included are the tool files (both original code and .xml wrappers)"
- [readme] Tools have been tested on a specific Galaxy Master branch commit: "The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758."
- [other] Deployment workflow involves copying tool files and restarting the Galaxy service: "Copy the Galaxy-M tool files and .xml wrapper definitions into the corresponding Galaxy tool directories; Restart the Galaxy service to reload tool definitions"
- [readme] WINE must be forced into 32-bit mode to avoid errors with SimStitch tools: "You must force wine to install everything in 32bit mode... if you do not do this, you will likely get errors from the SimStitch tools along the lines of 'Invalid file identifier'"
- [readme] Installation is complex and requires troubleshooting: "They are quite complex and can involve a lot of troubleshooting, so it is advised to work direct from the virtual machine where possible."
