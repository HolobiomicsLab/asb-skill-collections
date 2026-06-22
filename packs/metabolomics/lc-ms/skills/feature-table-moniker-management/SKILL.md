---
name: feature-table-moniker-management
description: Use when when processing a metabolomics feature table through multiple sequential transformations (e.g., imputation, normalization, batch correction, annotation) and you need to track which version of the table is being used at each step.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - ThermoRawFileParser
  - Python
  - PCPFM (PythonCentricPipelineForMetabolomics)
  - metDataModel
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Feature Table Moniker Management

## Summary

A systematic approach to naming and tracking feature tables throughout metabolomics preprocessing, enabling reproducible reference to intermediate and final tables in the pipeline. Feature tables are identified by monikers (symbolic names) stored in experiment metadata, allowing downstream steps to retrieve, transform, and save results without hardcoding file paths.

## When to use

When processing a metabolomics feature table through multiple sequential transformations (e.g., imputation, normalization, batch correction, annotation) and you need to track which version of the table is being used at each step. Use this skill whenever a workflow step reads a feature table by a symbolic name rather than a full file path, or when a transformation creates a new table variant that must be retrievable by downstream steps.

## When NOT to use

- When working with a single, final feature table that will not be referenced by downstream steps—use direct file paths instead.
- When the pipeline does not maintain an experiment.json metadata file or centralized registry of table variants.
- When tables are ephemeral or used only within a single function call and do not need to be persisted across workflow steps.

## Inputs

- experiment.json metadata file with table_moniker key
- Feature table TSV/CSV file referenced by moniker
- table_moniker parameter (string identifier)

## Outputs

- Feature table with new moniker registered in experiment.json
- Updated experiment.json with new_moniker entry
- Feature table file saved in experiment/feature_tables/ subdirectory

## How to apply

Assign a human-readable moniker (e.g., 'raw_table', 'imputed_table', 'normalized_table') to each feature table variant and store the moniker-to-filename mapping in the experiment.json metadata file. When a workflow step needs to load a feature table, retrieve the filename from the experiment metadata using the table_moniker parameter. After transformation (e.g., imputation with a specified interpolation_ratio), save the modified table with a new moniker (new_moniker) in the experiment's feature_tables subdirectory and update experiment.json. This allows subsequent steps to reference tables by logical name rather than path, supports pipeline reproducibility, and enables users to maintain multiple preprocessed versions for comparison or sensitivity analysis.

## Related tools

- **Python** (Language for implementing moniker lookup, file I/O, and experiment metadata management) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **PCPFM (PythonCentricPipelineForMetabolomics)** (Pipeline framework that orchestrates feature table creation, transformation, and moniker registration across workflow steps) — https://github.com/shuzhao-li-lab/PythonCentricPipelineForMetabolomics
- **metDataModel** (Data model library that defines experiment.json schema and table metadata structure)

## Evaluation signals

- experiment.json contains an entry for the new_moniker that points to a valid .tsv file in experiment/feature_tables/
- The feature table file exists at the path specified by the moniker lookup and contains expected dimensions (rows ≥ features, columns ≥ samples)
- Subsequent workflow steps successfully retrieve the table using the new_moniker without path resolution errors
- All rows and columns from the input table are present in the output table (no unintended row/column loss during save)
- Moniker names follow a consistent naming convention and do not collide with reserved keywords or existing monikers

## Limitations

- Moniker system depends on careful experiment.json maintenance; manual or external modifications to the metadata file can break downstream references.
- No built-in versioning or branching strategy; overwriting a moniker with a new table variant destroys the reference to the old version unless explicitly renamed.
- Monikers are local to a single experiment directory; sharing or comparing tables across experiments requires manual moniker synchronization.
- The README does not explicitly document the moniker naming convention or validation rules, which may lead to inconsistent naming practices across users.
- Large feature tables saved to feature_tables/ subdirectory can consume significant disk space if many intermediate variants are retained.

## Evidence

- [other] 1. Load the input feature table (identified by table_moniker) from the experiment directory. 2. Identify the minimum non-zero value for each feature across all samples. 3. For each feature, calculate the imputation value as interpolation_ratio × minimum non-zero value. 4. Replace all zero and missing values in the feature table with the corresponding imputation values. 5. Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables subdirectory.: "Load the input feature table (identified by table_moniker) from the experiment directory... Save the imputed feature table to a new moniker (new_moniker) in the experiment's feature_tables"
- [readme] Outputs are intended to be immediately usable for downstream analysis (e.g. MetaboAnalyst or common tools in R, Python etc.). This includes feature tables that are optionally blank masked, normalized, batch corrected, annotated or otherwise curated by PCPFM and empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards. The organization of the outputs is as such: Experiment Directory/ ... feature_tables/ user_created_table_1.tsv user_created_table_2.tsv ...: "feature_tables/ user_created_table_1.tsv user_created_table_2.tsv ... Outputs are intended to be immediately usable for downstream analysis"
- [readme] See the workflows under `examples/workflows/bash_workflows` for examples of processing pipelines to get started. You will need an appropriately formattted sequence file / sample metadata file along with mzML files.: "You will need an appropriately formattted sequence file / sample metadata file along with mzML files."
- [readme] The Python-Centric Pipeline for Metabolomics is designed to take raw LC-MS metabolomics data and ready them for downstream statistical analysis. The pipeline can ... perform quality control ... data normalization and batch correction ... output data in standardized formats (.txt, JSON), ready for downstream analysis: "pipeline can ... perform quality control ... data normalization and batch correction ... output data in standardized formats (.txt, JSON)"
