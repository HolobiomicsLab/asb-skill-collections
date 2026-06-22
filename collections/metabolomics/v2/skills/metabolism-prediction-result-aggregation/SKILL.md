---
name: metabolism-prediction-result-aggregation
description: Use when when you have run CypReact predictions on a molecular dataset against multiple CYP isoforms (e.g., 1A2, 2A6, 2B6) and need to consolidate the per-isoform output files into a single combined result file for cross-isoform comparison, visualization, or downstream metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - CypReact
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  dedup_kept_from: coll_cypreact_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolism-prediction-result-aggregation

## Summary

Aggregate cytochrome P450 (CYP) metabolism predictions across multiple isoforms into a single consolidated result file. This skill enables comprehensive metabolic profiling by collecting per-isoform predictions and merging them for downstream pharmacokinetic or drug metabolism analysis.

## When to use

When you have run CypReact predictions on a molecular dataset against multiple CYP isoforms (e.g., 1A2, 2A6, 2B6) and need to consolidate the per-isoform output files into a single combined result file for cross-isoform comparison, visualization, or downstream metabolite identification.

## When NOT to use

- Predictions have only been generated for a single CYP isoform (aggregation is unnecessary).
- Output files from different molecular input datasets are being mixed (cross-contamination risk).
- Per-isoform predictions use incompatible or non-aligned molecular identifier schemes.

## Inputs

- Multiple per-isoform CypReact output files in .sdf format
- Multiple per-isoform CypReact output files in .csv format
- Metadata mapping molecule identifiers to isoforms tested

## Outputs

- Merged prediction file (.sdf or .csv) containing all isoform results
- Consolidated metabolite list with isoform attribution

## How to apply

After invoking CypReact with comma-separated isoform codes (e.g., '1A2,2A6,2B6'), the tool generates per-isoform predictions. Collect all output files (.sdf or .csv format) corresponding to each isoform, then merge them using a standard consolidation workflow: (1) ensure all per-isoform files share the same molecular identifier column and prediction schema; (2) concatenate records while preserving isoform source attribution (e.g., add an 'isoform' column); (3) deduplicate on molecule ID if necessary, retaining all isoform-specific metabolite predictions; (4) validate that the merged file contains predictions from all requested isoforms and that no records were lost during aggregation.

## Related tools

- **CypReact** (Generates per-isoform cytochrome P450 metabolism predictions that are aggregated into a consolidated result) — github:bitbucket.org__Leon_Ti__cypreact

## Examples

```
java -jar cypreact.jar /path/to/input.sdf /path/to/output_merged.sdf 1A2,2A6,2B6
```

## Evaluation signals

- Merged file contains records from all requested CYP isoforms (verify isoform column has no missing values for any molecule).
- Row count in merged file equals the sum of rows across all per-isoform input files (no records lost during aggregation).
- Molecular identifiers are consistent and non-duplicated across the merged file (one row per molecule per isoform).
- Prediction fields (e.g., metabolite structures, reaction types) are preserved and non-null for all isoforms.
- Metadata schema (column names, data types) matches the original CypReact output specification for .sdf or .csv format.

## Limitations

- CypReact must be invoked with the multi-isoform parameter format (comma-separated, no spaces) to generate all per-isoform predictions before aggregation can occur.
- No automated conflict resolution is specified if the same metabolite is predicted by multiple isoforms with different reaction mechanisms; manual review may be required.
- Aggregation workflow (file merging) is not automated within CypReact; external scripting or data-wrangling tools are required to execute the consolidation steps.

## Evidence

- [other] Consolidation step: "Collect and merge the per-isoform predictions into a single combined result file (.sdf or .csv) for downstream analysis."
- [other] Multi-isoform invocation format: "Multiple CYP isoforms are specified as a comma-separated list without spaces by replacing the single isoform parameter (e.g., replacing "1A2" with "1A2,2A6,2B6")."
- [intro] Output format options: "The user can output a .sdf file or a .csv file."
- [intro] Multi-isoform testing instruction: "if the user wants to test his/her molecules on CYP1A2,2A6 and 2B6, he/she can simply replace "1A2" with "1A2,2A6,2B6""
