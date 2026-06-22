---
name: galaxy-tool-registration-verification
description: Use when after deploying Galaxy-M tool files and XML wrappers into a Galaxy installation's tool directories and restarting the Galaxy service, use this skill to confirm all metabolomics tools appear in the Galaxy admin interface and are ready for end-user access.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3047
  tools:
  - Galaxy
  - Python 2.7
  - R 3.0.1
  - MATLAB Compiler Runtime 8.3
  - Galaxy-M
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# galaxy-tool-registration-verification

## Summary

Verify that metabolomics tools and their XML wrapper definitions have been correctly registered and are accessible within a Galaxy installation after deployment. This skill ensures tool discoverability and proper integration before beginning analysis workflows.

## When to use

After deploying Galaxy-M tool files and XML wrappers into a Galaxy installation's tool directories and restarting the Galaxy service, use this skill to confirm all metabolomics tools appear in the Galaxy admin interface and are ready for end-user access. This is the gate-keeping step between infrastructure setup and operational readiness.

## When NOT to use

- Before XML wrapper files and tool code have been copied into the Galaxy installation directories — verification will fail and generate false negatives.
- If the Galaxy service has not been restarted after tool files were deployed — the registry will not yet reflect the new tools.
- When auditing tool execution results or analyzing metabolomics data — this skill verifies registration only, not tool correctness or output validity.

## Inputs

- Galaxy installation at the tested commit c429777c93680dcee449fe410f5360afbe673758
- Deployed Galaxy-M tool files and .xml wrapper definitions in Galaxy tools/ directory
- Restarted Galaxy service

## Outputs

- Confirmation that all Galaxy-M metabolomics tools appear in Galaxy admin tool registry
- Tool availability status report (enabled/disabled, errors if any)
- Verification that tools are searchable and accessible via Galaxy UI

## How to apply

Log into the Galaxy admin interface and navigate to the tool registry or administrative tools section. Check that all expected metabolomics analysis tools (e.g., PCA, empirical formula search, XCMS integration tools) are listed with correct tool IDs, versions, and descriptions matching the Galaxy-M XML wrapper definitions. Verify that tool search and discovery functions can locate tools by name or keyword. If a tool does not appear, cross-check that its .xml file was copied to the correct Galaxy tools/ subdirectory, that the tool ID in the XML matches Galaxy's tool registry expectations, and that the Galaxy service was restarted after tool files were added. Tools should be marked as 'enabled' and show no validation errors in the admin interface.

## Related tools

- **Galaxy** (Platform hosting the tool registry and admin interface used to verify tool registration and accessibility) — https://github.com/galaxyproject/galaxy
- **Galaxy-M** (Source of metabolomics tool files, .xml wrapper definitions, and configuration that are registered and verified) — https://github.com/Viant-Metabolomics/Galaxy-M

## Evaluation signals

- All Galaxy-M tool names appear in the Galaxy admin tool registry with no errors or warnings
- Tool search functionality returns metabolomics tools when queried by name or keyword
- Each tool XML definition is valid and parses without schema errors in Galaxy's tool validation system
- Tools are marked as 'enabled' and accessible to regular Galaxy users (not hidden or disabled)
- No duplicate tool IDs or conflicting tool definitions are detected in the registry

## Limitations

- This skill verifies registration only; it does not check whether the underlying tool code, dependencies (Python 2.7, R 3.0.1, MATLAB Compiler Runtime 8.3), or data files are correctly installed or functional.
- Tool registration success depends on exact Galaxy commit c429777c93680dcee449fe410f5360afbe673758; tools may not register correctly on different Galaxy versions or commits due to API and schema changes.
- The skill assumes the Galaxy service has been properly restarted after tool deployment; if restart failed or was incomplete, registration verification will produce false negatives.

## Evidence

- [other] Copy the Galaxy-M tool files and .xml wrapper definitions into the corresponding Galaxy tool directories (e.g., tools/, configs/).: "Copy the Galaxy-M tool files and .xml wrapper definitions into the corresponding Galaxy tool directories (e.g., tools/, configs/)."
- [other] Restart the Galaxy service to reload tool definitions.: "Restart the Galaxy service to reload tool definitions."
- [other] Verify tool registration by checking Galaxy's admin interface or tool registry to confirm all metabolomics tools are listed and accessible.: "Verify tool registration by checking Galaxy's admin interface or tool registry to confirm all metabolomics tools are listed and accessible."
- [readme] Included are the tool files (both original code and .xml wrappers) for Metabolomics analysis and the Galaxy config files from a working installation of Galaxy.: "Included are the tool files (both original code and .xml wrappers) for Metabolomics analysis and the Galaxy config files from a working installation of Galaxy."
- [readme] The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758.: "The Galaxy version that these files have been tested on is from the Master branch on Github: commit c429777c93680dcee449fe410f5360afbe673758."
