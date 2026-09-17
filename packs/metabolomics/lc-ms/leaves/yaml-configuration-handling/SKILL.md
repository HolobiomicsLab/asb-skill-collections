---
name: yaml-configuration-handling
description: Use when when initializing a MolNotator project with user-defined parameters
  for ionization modes, adduct tables, database selections, output directories, and
  tool-specific thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MolNotator
  - PyYAML
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2021.12.21.473622v1
  title: MolNotator
evidence_spans:
- from MolNotator.duplicate_filter import duplicate_filter
- from MolNotator.sample_slicer import sample_slicer
- import yaml
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_molnotator_cq
    doi: 10.1101/2021.12.21.473622v1
    title: MolNotator
  dedup_kept_from: coll_molnotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.12.21.473622v1
  all_source_dois:
  - 10.1101/2021.12.21.473622v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# YAML Configuration Handling

## Summary

Load and parse YAML parameter files to configure MolNotator's modular processing pipeline (duplicate filtering, sample slicing, annotation, dereplication). This skill ensures reproducible, parameterized execution of LC-MS/MS metabolomics workflows where all tunable settings are externalized to human-readable YAML files.

## When to use

When initializing a MolNotator project with user-defined parameters for ionization modes, adduct tables, database selections, output directories, and tool-specific thresholds. Use this skill at the start of any reproducible workflow and before each module invocation that requires parameter configuration (duplicate_filter, sample_slicer, fragnotator, adnotator, dereplicator).

## When NOT to use

- Parameters are already hard-coded in the Python script or environment variables; YAML handling adds no value and introduces file I/O overhead.
- Input is a single, one-off analysis with no intention to reuse or batch-process parameter sets; inline configuration may be simpler.
- YAML files are corrupted, malformed, or reference non-existent database or table files; the workflow will fail at module invocation.

## Inputs

- params.yaml file (main configuration with global parameters, folder paths, ionization modes, database file references)
- Secondary params YAML files (e.g., params_colotus.yaml, params_ldb_ions.yaml for dereplication-specific settings)
- Adduct table TSV files referenced in params (NEG_adduct_table_primary.tsv, POS_adduct_table_primary.tsv, etc.)
- Fragnotator loss table TSV file referenced in params

## Outputs

- params dictionary (Python dict object ready for passing to MolNotator module functions)
- db_params dictionary (database-specific parameter dict for dereplicator module)

## How to apply

Load the main params.yaml file using PyYAML's FullLoader to instantiate a params dictionary containing global settings and paths (input/output directories, ionization modes, database file names). For dereplication, iterate over the 'db_params' list in params and load each referenced YAML file separately to retrieve database-specific configuration. Pass the parsed params (and db_params for dereplication) to each MolNotator module function. The params dictionary centralizes adduct tables, fragnotator loss lists, sample export flags, and dereplication database selections, avoiding hardcoded values and enabling batch processing of multiple experiments with parameter variation.

## Related tools

- **PyYAML** (Parse YAML configuration files into Python dicts; supports FullLoader for safe deserialization)
- **MolNotator** (Modular LC-MS/MS metabolomics pipeline; consumes parsed params dict to configure duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, dereplicator, cosiner, and molnet modules) — https://github.com/ZzakB/MolNotator

## Examples

```
with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)
duplicate_filter(params=params, ion_mode="NEG")
```

## Evaluation signals

- params dictionary is non-empty, contains all required top-level keys (e.g., input_files, output_dirs, ionization modes, db_params list)
- No YAML parsing exceptions or file-not-found errors when loading params.yaml and referenced secondary YAML files
- Each module function (duplicate_filter, sample_slicer, etc.) receives the params dict and ion_mode argument without type errors or missing keys
- Output folders and database files specified in params exist or are created; no silent failures due to missing paths
- Dereplicator loop successfully iterates over all db_params entries without KeyError or undefined references

## Limitations

- YAML files must be manually maintained and kept in sync with the input file directory structure; no automatic schema validation is enforced.
- Multiple charge adduct processing is not implemented; YAML adduct tables should contain only single-charge species to avoid triangulation failures.
- PyYAML FullLoader is vulnerable to unsafe deserialization if YAML files are untrusted; use UnsafeLoader only if the source is verified.
- Adduct and fragnotator tables are manually edited TSV files; incorrect mass values or missing required columns will propagate silently through downstream modules.

## Evidence

- [other] Load the params dictionary from the YAML configuration file using PyYAML: "Load the params dictionary from the YAML configuration file using PyYAML."
- [other] Parse the YAML parameter file to retrieve duplicate-filter configuration using PyYAML: "Parse the YAML parameter file to retrieve duplicate-filter configuration using PyYAML."
- [readme] with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader): "with open("./params/params.yaml") as info:
    params = yaml.load(info, Loader=yaml.FullLoader)"
- [readme] The params folder contains all parameter files for annotation, dereplication and also the folder names to be used in the project: "The params folder contains all parameter files for annotation, dereplication and also the folder names to be used in the project"
- [readme] The params yaml file contains all parameters to be used in the project. Each parameter has a short description as a comment: "The params yaml file contains all parameters to be used in the project. Each parameter has a short description as a comment"
- [readme] for db_params in params['db_params']:
    print("Dereplicating using the " + db_params + " file...")
    with open("./params/" + db_params) as info:
        db_params = yaml.load(info, Loader=yaml.FullLoader): "for db_params in params['db_params']:
    print("Dereplicating using the " + db_params + " file...")
    with open("./params/" + db_params) as info:
        db_params = yaml.load(info,"
