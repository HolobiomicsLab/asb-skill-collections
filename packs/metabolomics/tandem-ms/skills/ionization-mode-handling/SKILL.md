---
name: ionization-mode-handling
description: Use when your MZmine MGF and CSV input files contain mixed or ambiguous ionization modes, or when your experimental design specifies separate negative (NEG) and positive (POS) ionization mode acquisitions that must be processed independently before merging.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MolNotator
  - PyYAML
  - Python
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ionization-mode-handling

## Summary

Separates and processes LC-MS/MS data by ionization mode (negative/positive) to ensure mode-specific filtering, annotation, and adduct assignment before downstream dereplication and molecular network construction. This skill is essential because different ionization modes produce distinct ion species and require distinct adduct tables and parameters.

## When to use

Apply this skill when your MZmine MGF and CSV input files contain mixed or ambiguous ionization modes, or when your experimental design specifies separate negative (NEG) and positive (POS) ionization mode acquisitions that must be processed independently before merging. The skill becomes mandatory before invoking duplicate_filter, fragnotator, or adnotator, as each of these functions requires an explicit ion_mode argument and mode-specific parameter tables.

## When NOT to use

- Input is already a single-mode dataset (e.g., only NEG data available); in this case, apply only the NEG branch of the workflow and skip mode_merger.
- Data have already been merged or deduplicated across modes; reapplying mode-specific filters may discard valid cross-mode ions.
- Ionization modes are not clearly separable in the input files (e.g., demultiplexing is incomplete); resolve demultiplexing first.

## Inputs

- MZmine MGF file (negative ionization mode)
- MZmine CSV metadata file (negative ionization mode)
- MZmine MGF file (positive ionization mode)
- MZmine CSV metadata file (positive ionization mode)
- params.yaml configuration file with mode-specific adduct tables and parameters

## Outputs

- Deduplicated MGF file (negative mode)
- Deduplicated CSV file (negative mode)
- Deduplicated MGF file (positive mode)
- Deduplicated CSV file (positive mode)
- Sample-sliced MGF files (one per sample, per mode)
- Annotated node and edge tables (negative mode)
- Annotated node and edge tables (positive mode)
- Merged molecular network (global, all modes combined)

## How to apply

Load the YAML parameter file to confirm the presence of mode-specific configuration (primary and secondary adduct tables for both NEG and POS, fragnotator parameters, and database settings). For each ionization mode (NEG first, then POS), invoke duplicate_filter(params=params, ion_mode="NEG") and duplicate_filter(params=params, ion_mode="POS") sequentially to remove duplicate features within each mode's MGF and CSV outputs. Follow with mode-specific sample_slicer, fragnotator, and adnotator calls, each passing the appropriate ion_mode argument. After all mode-specific processing is complete, use mode_merger(params=params) to consolidate the deduplicated, annotated NEG and POS networks into a single global network. The rationale is that adduct complexity, in-source fragment patterns, and neutral mass inference differ significantly between ionization modes, so triangulation and annotation must be performed separately to avoid cross-mode artifacts.

## Related tools

- **MolNotator** (Framework providing duplicate_filter, sample_slicer, fragnotator, adnotator, mode_merger, and dereplicator functions; orchestrates ionization-mode-aware processing.) — https://github.com/ZzakB/MolNotator
- **PyYAML** (Parses params.yaml and mode-specific parameter files to retrieve ion_mode settings, adduct tables, and output paths.)
- **Python** (Runtime environment for invoking MolNotator functions and file I/O operations.)

## Examples

```
import yaml
from MolNotator.duplicate_filter import duplicate_filter
from MolNotator.mode_merger import mode_merger

with open("./params/params.yaml") as f:
    params = yaml.load(f, Loader=yaml.FullLoader)

duplicate_filter(params=params, ion_mode="NEG")
duplicate_filter(params=params, ion_mode="POS")
mode_merger(params=params)
```

## Evaluation signals

- Output files are correctly partitioned into NEG and POS directories with consistent naming and no cross-contamination of ionization modes.
- Deduplicated MGF and CSV files for each mode contain fewer features than input (indicating successful duplicate removal) and match row counts in paired CSV/MGF outputs.
- Mode-specific adduct annotations are semantically correct (e.g., NEG mode contains only negative adducts like [M-H]-, [M+Cl]-; POS mode contains only positive adducts like [M+H]+).
- Node and edge tables generated after mode_merger reflect combined but distinct neutrals and ions from both modes, with no duplicate neutral nodes across modes.
- Final molecular network visualized in Cytoscape shows connected components stratified by mode-specific adduct groups without spurious inter-mode edges.

## Limitations

- MolNotator currently supports only single-charge ions; multiple-charge adducts and ions are not processed and should be removed or transferred to secondary adduct tables before workflow execution.
- Mode merging assumes that neutral molecules inferred in NEG and POS modes are the same; if isotope labeling or differential adduction creates genuine mode-specific neutrals, merging may conflate unrelated species.
- Requires user to manually maintain separate, consistent adduct tables for each mode in the params folder; mismatched or missing tables will cause function failures or incomplete annotation.
- No changelog documented; version compatibility between MolNotator releases and specific MZmine output formats is not tracked, risking silent failures on format changes.

## Evidence

- [other] The duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes.: "duplicate_filter function accepts parameters and an ion_mode argument to filter duplicate features from MZmine's MGF and CSV files for either negative (NEG) or positive (POS) ionization modes"
- [readme] duplicate_filter(params = params, ion_mode = "NEG") and duplicate_filter(params = params, ion_mode = "POS") are invoked sequentially with explicit ionization mode strings.: "duplicate_filter(params = params,
                 ion_mode = "NEG")

# Duplicate filtering on MZmine's MGF and CSV files (POS):
duplicate_filter(params = params,
                 ion_mode = "POS")"
- [readme] mode_merger consolidates negative and positive mode data after all mode-specific annotation is complete.: "Use Moder Merger to merge negative and positive mode data :
mode_merger(params = params)"
- [readme] The adduct tables are formed for each ionization mode, with primary tables used for triangulation and secondary tables only for annotation after neutral node creation.: "The adduct tables are all formed the same, the primary being used for triangulation and the secondary only being used to annotate the remaining ions once the neutral node is created."
- [readme] Multiple charge adduct processing is not implemented; only single-charge ions should be used, with less abundant ion species prioritized if transferring from primary to secondary tables.: "Multiple charge adduct processing is not implemented as of yet, we would suggest only using single charge ions."
