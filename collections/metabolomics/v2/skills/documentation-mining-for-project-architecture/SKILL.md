---
name: documentation-mining-for-project-architecture
description: Use when you have access to a multi-component research software repository (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3071
  tools:
  - MAGMa
  - job
  - joblauncher
  - pubchem
  - web (magmaweb)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# documentation-mining-for-project-architecture

## Summary

Extract and map the named subproject components, their functional roles, and interdependencies from a multi-module research software project by systematically scanning repository READMEs, configuration files, and module docstrings. This skill reconstructs the logical architecture of complex systems like MAGMa to enable downstream dependency analysis, integration testing, and workflow optimization.

## When to use

You have access to a multi-component research software repository (e.g., via GitHub or Zenodo) and need to understand its internal architecture—which subprojects exist, what each does, and how they depend on each other—in order to design integration workflows, trace data flow, or plan maintenance or extension work.

## When NOT to use

- Repository documentation is absent, minimal, or severely outdated (e.g., lists components no longer in the codebase or omits recently added ones); extract from source code instead.
- Project is a monolithic single-module application with no named subprojects; use simpler module-level inspection instead.
- You only need to run or use the software, not understand or modify its internal architecture; user-facing documentation suffices.

## Inputs

- GitHub repository URL or local clone of a multi-module research software project
- README.md or similar root-level documentation file
- setup.py, setup.cfg, or pyproject.toml configuration files
- Module __init__.py and docstrings for functional role confirmation

## Outputs

- Structured manifest (JSON or CSV) containing component name, inferred functional role, source directory path, and dependencies
- Dependency graph or adjacency list showing inter-subproject relationships
- Validated component registry with inferred role and confirmation source

## How to apply

Clone or access the target repository (e.g., https://github.com/NLeSC/MAGMa) and begin with the root README, which typically lists named subprojects and their roles. For each named component, locate its directory and scan for setup.py, __init__.py, or inline module docstrings to confirm or infer its functional role. Document the dependency graph by cross-referencing sections in the README that explicitly state interdependencies (e.g., 'job calculation requires a pubchem lookup database'). Extract component name, inferred role, source path, and dependency relationships into a structured manifest (JSON or CSV). Validate by checking that all named subprojects are locatable in the filesystem and that stated interdependencies align with import statements or configuration.

## Related tools

- **MAGMa** (Subject system being reverse-engineered; comprises five named subproject components (emetabolomics_site, job, joblauncher, pubchem, web) for metabolite annotation workflow) — https://github.com/NLeSC/MAGMa
- **job** (Calculation engine subproject that executes MAGMa metabolite annotation; depends on pubchem lookup database) — https://github.com/NLeSC/MAGMa
- **joblauncher** (Webservice subproject that mediates job submission and execution; bridges web application to job calculation engine) — https://github.com/NLeSC/MAGMa
- **pubchem** (Data processing subproject that builds and maintains PubChem lookup database used by job calculation) — https://github.com/NLeSC/MAGMa
- **web (magmaweb)** (Results interface and job submission frontend; initiates job calculations via joblauncher webservice) — https://github.com/NLeSC/MAGMa

## Examples

```
git clone https://github.com/NLeSC/MAGMa && cd MAGMa && git submodule update --init && grep -r 'def \|class ' job/ joblauncher/ pubchem/ web/ | head -20
```

## Evaluation signals

- All named subprojects listed in README are locatable as directories in the repository filesystem
- Each subproject's inferred role can be confirmed by at least one source (README section, module docstring, or setup.py description)
- Stated interdependencies in README align with import statements or configuration references in source code (e.g., job imports pubchem; web imports joblauncher)
- Manifest is complete and unambiguous: each component has a name, directory path, functional role, and list of direct dependencies
- No named components exist in the repository that are absent from the manifest; and no manifest entries correspond to missing or deleted directories

## Limitations

- README documentation may be outdated, inconsistent, or incomplete; always cross-reference with actual source code and directory structure.
- Functional roles inferred from documentation are necessarily informal and may not capture all responsibilities or edge cases visible only in code.
- Submodule dependencies (e.g., git submodule joblauncher) may be listed but not present in a shallow clone; use 'git submodule update --init' to fetch them.
- Interdependencies stated in README may be incomplete or aspirational; missing dependencies are best discovered via import analysis or static code inspection.

## Evidence

- [readme] The MAGMa system comprises five named subproject components with stated roles: "Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processing of PubChem database,"
- [readme] Interdependencies are explicitly documented and traceable: "Subproject interdependencies
----------------------------

- The `emetabolomics_site` website can be used as starting pages for the `web` application.
- The `job` calculation requires a pubchem"
- [intro] Project context: metabolomics chemo-informatics and metabolite identification: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [readme] Submodule initialization is required for full repository: "Use following command to initialize and fetch the joblauncher submodule:

.. code-block:: bash

    git submodule update --init"
