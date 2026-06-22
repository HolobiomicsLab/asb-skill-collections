---
name: structured-inventory-compilation
description: Use when when you need to understand the modular composition of a multi-component research software project, particularly before onboarding, refactoring, or deploying it.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0081
  tools:
  - MAGMa
  - GitHub API / git
  - jq or pandas
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

# structured-inventory-compilation

## Summary

Compile named software components and their functional roles from project repository documentation into a machine-readable manifest (JSON/CSV). This skill systematically extracts architecture metadata to enable downstream dependency analysis, deployment orchestration, and integration testing.

## When to use

When you need to understand the modular composition of a multi-component research software project, particularly before onboarding, refactoring, or deploying it. Use this skill when the project README or root-level documentation lists subproject names but lacks a formal architecture registry or when you must derive component interdependencies from prose descriptions.

## When NOT to use

- Input is a single-module or monolithic application with no named subproject structure.
- Documentation is severely outdated or contradicts the actual directory layout; in this case, perform a code-based inventory instead.
- The goal is source-code-level dependency analysis (AST parsing, import graphs); use static analysis tools instead.

## Inputs

- GitHub repository URL or local repository clone
- Project README or architecture documentation file
- Optional: setup.py, pyproject.toml, or docker-compose.yml for dependency hints

## Outputs

- Structured manifest (JSON array of objects with keys: name, role, path, dependencies)
- CSV table with columns: component_name, functional_role, directory_path, upstream_dependencies
- Interdependency diagram (edge list or adjacency matrix)

## How to apply

Clone or access the target repository (e.g., GitHub) and locate the primary README or architecture documentation. Scan for sections explicitly listing named subproject components (e.g., 'Subprojects:' heading in the MAGMa README). For each named component, extract: (1) the declared name (e.g., 'emetabolomics_site'), (2) the functional description provided in-line or in a cross-referenced section, and (3) the inferred directory path or module reference. Cross-reference component interdependencies by reading any 'Subproject interdependencies' or similar section that documents which components call or depend on others. Compile findings into a structured format (JSON object array or CSV with columns: component_name, role, directory_path, dependencies) with consistent naming and no duplicate entries. Validate by checking that each named component either has a corresponding directory in the repository or is a documented external service.

## Related tools

- **MAGMa** (Subject research software system from which named subproject components are extracted and inventoried) — https://github.com/NLeSC/MAGMa
- **GitHub API / git** (Repository access and README retrieval) — https://github.com
- **jq or pandas** (JSON/CSV schema validation and manifest formatting)

## Examples

```
# Extract and compile MAGMa subproject inventory from README
git clone https://github.com/NLeSC/MAGMa && cd MAGMa && python -c "import json; components = [{'name': 'emetabolomics_site', 'role': 'website'}, {'name': 'job', 'role': 'calculation engine'}, {'name': 'joblauncher', 'role': 'webservice'}, {'name': 'pubchem', 'role': 'data processing'}, {'name': 'magmaweb', 'role': 'results interface'}]; print(json.dumps(components, indent=2))" > magma_inventory.json
```

## Evaluation signals

- All named components listed in the README appear in the manifest with no omissions.
- Each component has a non-empty, distinct role description extracted or inferred from documentation.
- Interdependencies are bidirectional-consistent: if component A depends on B, the manifest edge A→B exists; no circular dependencies unless documented as intentional.
- Directory paths in the manifest correspond to actual subdirectories or modules in the repository (checked via file listing or git ls-tree).
- Manifest is valid JSON/CSV and passes schema validation (e.g., all required fields populated, no duplicate keys).

## Limitations

- If documentation is prose-only without explicit 'Subprojects' section, component discovery relies on inference from directory names or import statements, which may be incomplete or ambiguous.
- README may describe aspirational or legacy components no longer present in the codebase; cross-check against the actual repository structure to confirm currency.
- Interdependency descriptions in README may use informal language ('used by', 'requires') that needs normalization into a consistent dependency model.
- External dependencies (databases, web services) may be listed but their integration points not fully documented in the README alone; supplementary configuration files may be needed.

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
- pubchem - Processing of PubChem database
-"
- [readme] Subproject interdependencies
----------------------------

- The `emetabolomics_site` website can be used as starting pages for the `web` application.
- The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.
- The `web` application starts `job` calculations via the `joblauncher` webservice.: "The `job` calculation requires a pubchem lookup database which can be made using the `pubchem` application.
- The `web` application starts `job` calculations via the `joblauncher` webservice."
- [other] The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and magmaweb (results interface).: "The MAGMa system comprises five named subproject components: emetabolomics_site (website), job (calculation engine), joblauncher (webservice for job execution), pubchem (data processing), and"
