---
name: metadata-extraction-from-source-code
description: Use when you need to reverse-engineer or document the architecture of a multi-component research software system where design information is embedded in repository structure, README declarations, setup files, or module docstrings rather than in a separate design document.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_0092
  tools:
  - MAGMa
  - GitHub
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

# metadata-extraction-from-source-code

## Summary

Extract architectural metadata (component names, roles, interdependencies, and functional descriptions) from source code repositories, README files, and configuration artifacts to reconstruct system design and workflow dependencies. This skill is essential when documentation is sparse or distributed across multiple files and you need to understand how discrete subproject components interact.

## When to use

Apply this skill when you need to reverse-engineer or document the architecture of a multi-component research software system where design information is embedded in repository structure, README declarations, setup files, or module docstrings rather than in a separate design document. Use it specifically when the input is a GitHub repository URL or local clone and the goal is to produce a structured inventory of named subcomponents and their roles in an analysis workflow.

## When NOT to use

- The input is a single-component, monolithic library or tool with no documented subproject structure; use generic code documentation extraction instead.
- Comprehensive API documentation or design documents already exist in a published manual or specification; extract from the authoritative source first.
- The repository is private or inaccessible; you cannot perform the scan without read access to the source tree and README files.

## Inputs

- GitHub repository URL (string)
- Repository root directory path or cloned local repository
- README.rst or README.md file content
- setup.py or pyproject.toml configuration file
- Directory listing and subdirectory structure

## Outputs

- Structured metadata manifest (JSON or CSV) with fields: component_name, role_description, directory_path, inferred_workflow_function
- Interdependency graph or text list showing data/execution flow between components
- Annotated system architecture diagram (optional, derived from the manifest)

## How to apply

Begin by cloning or accessing the target repository (e.g., https://github.com/NLeSC/MAGMa). Scan the repository root for README files, setup.py, configuration files (pyproject.toml, setup.cfg), and directory structure to identify top-level components. For each candidate component, extract its directory name, any inline functional description from the README (e.g., 'emetabolomics_site - The http://www.emetabolomics.org website'), and its inferred role in the larger workflow. Cross-reference component names with docstrings, comments, or interdependency sections that explain how components consume or produce data. Compile findings into a structured format (JSON, CSV, or YAML) listing component name, role, directory path, and documented dependencies. Validate by checking that declared interdependencies form a coherent workflow graph (e.g., 'web application starts job calculations via joblauncher webservice').

## Related tools

- **MAGMa** (Target software system being reverse-engineered; comprises five named subproject components for metabolite annotation and biochemical network reconstruction) — https://github.com/NLeSC/MAGMa
- **GitHub** (Repository hosting platform and source of README documentation and directory structure) — https://github.com/NLeSC/MAGMa

## Examples

```
git clone https://github.com/NLeSC/MAGMa && cd MAGMa && git submodule update --init && grep -A 20 '^Subprojects:' README.rst
```

## Evaluation signals

- All five declared subcomponents (emetabolomics_site, job, joblauncher, pubchem, web/magmaweb) are identified and assigned a functional role consistent with the README text.
- Interdependencies form a coherent DAG: emetabolomics_site → web, job requires pubchem database, web → joblauncher → job. No circular dependencies.
- Each component's role matches its name and inferred function (e.g., joblauncher described as 'Webservice to execute jobs').
- The structured output can be validated against the README interdependencies section without contradictions.
- Directory paths or file locations for each component can be verified in the actual repository structure.

## Limitations

- README documentation may be incomplete, outdated, or absent for some components; inline code documentation may be required to infer roles.
- Subproject interdependencies declared in the README may not reflect actual runtime dependencies or data flow; runtime or deployment testing may be needed to validate.
- If the repository uses git submodules (as MAGMa does for joblauncher), metadata extraction requires explicit submodule initialization (`git submodule update --init`) and may not work on shallow clones.
- No changelog or version history information is documented in the README, making it difficult to track architectural changes over time.

## Evidence

- [readme] Subprojects: emetabolomics_site - The http://www.emetabolomics.org website; job - Runs MAGMa calculation; joblauncher - Webservice to execute jobs; pubchem - Processing of PubChem database, used to find mass candidates; web - Web application to start jobs and view results: "Subprojects:

- emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processing of PubChem database,"
- [readme] The `emetabolomics_site` website can be used as starting pages for the `web` application. The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application. The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `emetabolomics_site` website can be used as starting pages for the `web` application.
- The `job` calculation requires a pubchem lookup database which can be made using the `pubchem`"
- [intro] The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
- [readme] Use following command to initialize and fetch the joblauncher submodule: git submodule update --init: "Use following command to initialize and fetch the joblauncher submodule:

.. code-block:: bash

    git submodule update --init"
