---
name: software-component-identification
description: Use when when you need to understand the modular structure of a multi-component
  research software project—particularly when integrating, documenting, or extending
  a system whose architecture is not immediately obvious from high-level descriptions.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - MAGMa
  license_tier: open
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
evidence_spans:
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'.
- MAGMa is a abbreviation for 'Ms Annotation based on in silico Generated Metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_magma
    doi: 10.5702/massspectrometry.S0033
    title: magma
  dedup_kept_from: coll_magma
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-component-identification

## Summary

Systematically identify and document named subproject components within a complex research software system by scanning repository structure, configuration files, and documentation. This skill extracts component names, directory paths, functional roles, and interdependencies to produce a structured manifest of the system architecture.

## When to use

When you need to understand the modular structure of a multi-component research software project—particularly when integrating, documenting, or extending a system whose architecture is not immediately obvious from high-level descriptions. Use this skill when you have access to a source repository (GitHub, GitLab, Zenodo) and need to map logical subprojects to their implementation locations and roles within a larger workflow.

## When NOT to use

- Repository is a monolithic single-purpose application with no subproject structure.
- Documentation or README explicitly states that the project is not modular or does not use named subproject components.
- You only need to identify external dependencies (pip, conda, npm packages); this skill is for internal component discovery only.

## Inputs

- GitHub repository URL or cloned repository directory
- README.md or similar documentation files
- setup.py, setup.cfg, or pyproject.toml configuration files
- Directory tree structure and subdirectory names

## Outputs

- Structured manifest (JSON or CSV) of component names, paths, roles, and interdependencies
- Component registry with entries for each named subproject
- Documented subproject interdependency graph

## How to apply

Begin by cloning or accessing the target repository (e.g., https://github.com/NLeSC/MAGMa). Scan the repository root for README files, setup.py, configuration files (setup.cfg, pyproject.toml, docker-compose.yml), and directory structure to identify candidate subproject directories. For each candidate, extract its name (e.g., 'job', 'joblauncher', 'pubchem') and infer its functional role by reading inline documentation, module docstrings, and dependency declarations. Document interdependencies by tracing how subprojects reference or invoke one another (e.g., 'web application starts job calculations via joblauncher webservice'). Compile findings into a structured manifest (JSON or CSV) with columns for component name, directory path, inferred role, and documented dependencies. Cross-reference your findings against the README and any architecture diagrams to validate assignments.

## Related tools

- **MAGMa** (The target system being decomposed into components; acronym for 'Ms Annotation based on in silico Generated Metabolites'.) — https://github.com/NLeSC/MAGMa

## Examples

```
git clone https://github.com/NLeSC/MAGMa && cd MAGMa && git submodule update --init && grep -A 20 '^Subprojects:' README.rst | head -10
```

## Evaluation signals

- All named subproject components mentioned in the README are present in the manifest with assigned directory paths.
- Each component entry includes a role description that aligns with the README's documented purpose (e.g., 'job' → 'Runs MAGMa calculation').
- Interdependencies in the manifest match the documented dependency statements (e.g., 'web application starts job calculations via joblauncher webservice').
- Directory paths in the manifest correspond to actual subdirectories in the cloned repository.
- The manifest is serializable to valid JSON or CSV with consistent schema across all component entries.

## Limitations

- Component roles may be inferred rather than explicitly stated; validation against inline code or external documentation may be necessary.
- Submodules (e.g., joblauncher in MAGMa) require explicit initialization (git submodule update --init) and may not be discoverable from the README alone.
- The skill relies on documentation accuracy; if the README is out of sync with the actual codebase, the manifest may be incomplete or incorrect.
- Complex transitive dependencies between components may not be fully resolvable from static analysis of configuration files alone.

## Evidence

- [readme] Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processing of PubChem database, used to find mass candidates
- web - Web application to start jobs and view results: "Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processing of PubChem database,"
- [readme] Subproject interdependencies
----------------------------

- The `emetabolomics_site` website can be used as starting pages for the `web` application.
- The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.
- The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `web` application starts `job` calculations via the `joblauncher` webservice."
- [other] The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and magmaweb (results interface).: "The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and"
- [readme] Use following command to initialize and fetch the joblauncher submodule:

.. code-block:: bash

    git submodule update --init: "Use following command to initialize and fetch the joblauncher submodule"
