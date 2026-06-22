---
name: qm-output-parsing-and-aggregation
description: Use when you have completed parallel QUICK quantum calculations on multiple conformers filtered by ASE-ANI and need to extract electronic properties from the output logs and consolidate them into a single structured table for use in CCS calculations or metabolite annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3292
  tools:
  - QUICK
  - Snakemake
  - ASE-ANI
derived_from:
- doi: 10.1021/jasms.1c00315
  title: POMICS
evidence_spans:
- 'QUICK: For quantum calculations'
- Snakemake workflow manager for predicting collisional cross sections
- This repository contains a Snakemake workflow manager for predicting collisional cross sections (CCS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pomics_cq
    doi: 10.1021/jasms.1c00315
    title: POMICS
  dedup_kept_from: coll_pomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.1c00315
  all_source_dois:
  - 10.1021/jasms.1c00315
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QM Output Parsing and Aggregation

## Summary

Parse quantum mechanical (QM) output logs from QUICK to extract electronic properties (polarizability tensor components, dipole moment) and aggregate results into a structured table mapping conformer IDs to computed properties. This skill bridges the gap between raw QM calculations and downstream CCS prediction by collecting and organizing molecular descriptors needed for collision cross-section modeling.

## When to use

You have completed parallel QUICK quantum calculations on multiple conformers filtered by ASE-ANI and need to extract electronic properties from the output logs and consolidate them into a single structured table for use in CCS calculations or metabolite annotation workflows.

## When NOT to use

- QUICK calculations have not yet completed or output logs are unavailable.
- You require post-processing of CCS values rather than extraction of intermediate QM properties.
- Input conformers have not been filtered by ASE-ANI and you are working with raw, unoptimized geometries.

## Inputs

- QUICK output logs from parallel quantum calculations
- Mapping of conformer IDs to QUICK output file paths
- Set of filtered conformers (xyz or molden format) used as input to QUICK

## Outputs

- Structured output table (text/CSV) mapping conformer ID to electronic properties
- Aggregated polarizability tensor components per conformer
- Aggregated dipole moment values per conformer

## How to apply

After QUICK has completed quantum calculations on filtered conformers in xyz or molden format: (1) iterate over all QUICK output logs from the parallel computation; (2) parse each log to identify and extract polarizability tensor components and dipole moment values; (3) link each extracted property set to its corresponding conformer ID; (4) validate that all expected conformers have been parsed and no duplicate entries exist; (5) write results to a structured output table (typically a delimited text file or structured format) with columns for conformer ID and computed electronic properties; (6) verify row counts match the number of input conformers and that no property values are missing or malformed. The parsing must be robust to QUICK's log formatting to ensure all properties are captured accurately.

## Related tools

- **QUICK** (Performs quantum mechanical calculations on conformers; generates output logs containing polarizability and dipole moment data) — https://github.com/merzlab/QUICK
- **Snakemake** (Orchestrates parallel QUICK job submission and manages file dependencies for output log aggregation) — https://github.com/DasSusanta/snakemake_ccs
- **ASE-ANI** (Provides pre-filtered conformers as input to QUICK; output logs from QUICK are parsed for properties computed on ASE-ANI-optimized geometries) — https://github.com/isayev/ASE_ANI

## Examples

```
# After QUICK jobs complete, parse and aggregate outputs (pseudo-code within Snakemake rule):
# for log in QUICK_output_logs:
#   properties = parse_quick_log(log)
#   output_table.append({conformer_id: conf_id, polarizability: props['alpha'], dipole: props['mu']})
# output_table.to_csv('electronic_properties.txt', sep='\t')
```

## Evaluation signals

- All input conformers from the filtered set have a corresponding entry in the output table (row count matches conformer count).
- No missing or null values appear in polarizability or dipole moment columns.
- Conformer ID values in the output table are unique and match the conformer IDs from the input geometry files.
- Polarizability tensor components (6 independent values for symmetric 3×3 tensor) and dipole moment (3 components) are present and within physically plausible ranges.
- Output table format is consistent with downstream CCS calculation tool expectations (e.g., column order, delimiter, precision).

## Limitations

- ASE-ANI README is marked deprecated and no longer supported; users should prefer the TorchANI implementation instead. QUICK output log format may vary by version; parser must be adapted if QUICK version differs from the original workflow.
- Parsing assumes standard QUICK output formatting; non-standard or corrupted logs may cause extraction failures or silently incorrect values.
- Electronic properties are computed only for CHNO elements (ASE-ANI limitation); molecules containing other elements will not be processed through the full pipeline.
- Parallel QUICK jobs may fail silently or partially; no built-in validation ensures all conformers completed successfully before aggregation begins.

## Evidence

- [other] Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment). Aggregate results into a structured output table mapping conformer ID to computed properties.: "Parse QUICK output logs to extract electronic properties (polarizability tensor components, dipole moment). Aggregate results into a structured output table mapping conformer ID to computed"
- [other] QUICK performs quantum calculations as the final computational step in the CCS prediction pipeline, operating on conformers that have been filtered by ASE-ANI.: "QUICK performs quantum calculations as the final computational step in the CCS prediction pipeline, operating on conformers that have been filtered by ASE-ANI."
- [other] Load the set of pre-filtered conformers (in xyz or molden format) from the ASE-ANI filtering step. Prepare QUICK input files for each conformer specifying the quantum method, basis set, and molecular geometry. Submit each conformer for quantum calculation via QUICK, executing in parallel on available HPC cores.: "Load the set of pre-filtered conformers (in xyz or molden format) from the ASE-ANI filtering step. Prepare QUICK input files for each conformer specifying the quantum method, basis set, and molecular"
- [readme] QUICK: For quantum calculations. Available at: [https://github.com/merzlab/QUICK]: "QUICK: For quantum calculations. Available at: [https://github.com/merzlab/QUICK]"
- [readme] DEPRECATED and no longer supported, please use TorchANI implementation: "DEPRECATED and no longer supported, please use TorchANI implementation"
