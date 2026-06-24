---
name: repository-structure-parsing
description: Use when when you encounter a multi-module scientific software project
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0769
  tools:
  - MAGMa
  - git submodule
  - PubChem
  - MetumpX
  - MetumpX_setup_enUS
  license_tier: open
derived_from:
- doi: 10.5702/massspectrometry.S0033
  title: magma
- doi: 10.1093/bioinformatics/btz765
  title: ''
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
  - build: coll_metumpx_untargeted_ms_support_package_cq
    doi: 10.1093/bioinformatics/btz765
    title: MetumpX untargeted MS support package
  dedup_kept_from: coll_magma
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5702/massspectrometry.S0033
  all_source_dois:
  - 10.5702/massspectrometry.S0033
  - 10.1093/bioinformatics/btz765
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Repository Structure Parsing

## Summary

Systematically extract and document named subproject components, their functional roles, and interdependencies from a multi-component research software repository by analyzing README files, configuration files, and inline documentation. This skill enables reconstruction of system architecture and dependency graphs needed to understand integration points and deployment strategies.

## When to use

When you encounter a multi-module scientific software project (e.g., MAGMa with five named subproject components) and need to understand the system architecture, component roles, and how subprojects depend on each other for metabolite annotation workflows, data processing pipelines, or web-based result interfaces.

## When NOT to use

- Input is a monolithic single-module project with no documented subproject structure—use simpler module/function inventory instead.
- Repository documentation is absent or severely incomplete (no README, setup.py, or docstrings); requires reverse-engineering via code inspection alone.
- The goal is to extract only a single component's internal API or function signatures, not the multi-component system architecture.

## Inputs

- GitHub repository URL or local repository clone (NLeSC/MAGMa or similar multi-component project)
- README.md or README.rst file(s) from repository root
- setup.py, setup.cfg, or pyproject.toml files listing subproject metadata
- Configuration files (.travis.yml, docker-compose.yml, or similar) that reveal component deployment structure

## Outputs

- Structured manifest of named subproject components (JSON or CSV format) with fields: component_name, role, directory_path, functional_description
- Subproject interdependency graph or adjacency list (e.g., job → joblauncher, joblauncher → pubchem)
- Architecture diagram or text summary documenting how components integrate in the metabolomics data analysis workflow

## How to apply

Begin by accessing the repository root (GitHub URL or local clone) and scan for documentation files: README, setup.py, requirements.txt, and configuration files that declare or describe subproject structure. Extract named components (e.g., emetabolomics_site, job, joblauncher, pubchem, magmaweb) by matching directory paths to functional descriptions in the README or docstrings. For each component, infer its role in the larger workflow—e.g., whether it serves as a calculation engine, webservice, data processor, or results interface. Trace explicit interdependencies documented in the README (e.g., 'web application starts job calculations via joblauncher webservice'; 'job calculation requires pubchem lookup database'). Compile findings into a structured manifest (JSON or CSV) with columns for component name, inferred role, directory path, and dependency relationships. Validate the manifest by cross-referencing component names against submodule declarations (e.g., git submodule commands) and license declarations to confirm scope.

## Related tools

- **MAGMa** (Multi-component chemo-informatics system for metabolite annotation; the subject repository being parsed for its subproject structure) — https://github.com/NLeSC/MAGMa
- **git submodule** (Used to initialize and manage the joblauncher submodule dependency within the repository)
- **PubChem** (External data resource; processed by the pubchem subproject component to create mass candidate lookup databases)

## Examples

```
git clone https://github.com/NLeSC/MAGMa && cd MAGMa && git submodule update --init && grep -E '^- [a-z_]+' README.rst | awk '{print $2}' | while read comp; do echo "$comp: $(grep -A1 "^- $comp" README.rst | tail -1)"; done
```

## Evaluation signals

- All five named subproject components (emetabolomics_site, job, joblauncher, pubchem, magmaweb) are identified and listed in the output manifest.
- Each component has a documented role that can be traced to a verbatim description in the README or configuration files (e.g., 'Runs MAGMa calculation' for job component).
- Interdependency relationships match the documented README statements (e.g., 'web application starts job calculations via joblauncher webservice'; 'job calculation requires pubchem lookup database').
- Directory paths for each component are present and verified against the actual repository structure (e.g., web/ subdirectory contains magmaweb).
- The manifest is valid JSON or CSV with no missing or malformed records; can be parsed and reused by downstream analysis or deployment tooling.

## Limitations

- Changelog documentation was not found in the MAGMa repository, limiting ability to trace evolution of subproject structure across versions.
- Subproject interdependencies are documented at a high level in the README but may not capture all internal communication patterns or data flow details visible only through code inspection.
- Web application component is documented as 'web' in the README but referred to as 'magmaweb' in the manifest, suggesting potential inconsistency in naming conventions across documentation and code.

## Evidence

- [readme] The five named components of the MAGMa system and their roles in the metabolomics workflow.: "emetabolomics_site - The http://www.emetabolomics.org website
- job - Runs MAGMa calculation
- joblauncher - Webservice to execute jobs
- pubchem - Processing of PubChem database, used to find mass"
- [readme] Documented interdependencies between subproject components.: "The `emetabolomics_site` website can be used as starting pages for the `web` application.
- The `job` calculation requires a pubchem lookup database which can be made using the `pubchem`"
- [readme] Integration of submodule management within the repository structure.: "Use following command to initialize and fetch the joblauncher submodule:

.. code-block:: bash

    git submodule update --init"
- [readme] The overarching project goal and context for the multi-component architecture.: "The project develops chemo-informatics based methods for metabolite identification and biochemical network reconstruction in an integrative metabolomics data analysis workflow."
