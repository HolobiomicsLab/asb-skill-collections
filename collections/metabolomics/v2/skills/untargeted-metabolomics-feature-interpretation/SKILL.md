---
name: untargeted-metabolomics-feature-interpretation
description: Use when you have an untargeted metabolomics feature table (m/z values, retention times, p-values from statistical testing) and need to infer which metabolic pathways are active without performing metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - mummichog
  - metDataModel
  - JMS
  - mass2chem
derived_from:
- doi: 10.1371/journal.pcbi.1003123
  title: mummichog
evidence_spans:
- Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mummichog_cq
    doi: 10.1371/journal.pcbi.1003123
    title: mummichog
  dedup_kept_from: coll_mummichog_cq
schema_version: 0.2.0
---

# Reconstruct metabolic-network-based functional activity prediction from a feature table

## Summary

This skill predicts functional pathway activity directly from untargeted metabolomics feature tables (m/z, retention time, intensity) by mapping features to a metabolic network and propagating activity signals through biochemical pathways, without requiring prior metabolite identification. It enables rapid functional interpretation of mass spectrometry data via network-based inference.

## When to use

Apply this skill when you have an untargeted metabolomics feature table (m/z values, retention times, p-values from statistical testing) and need to infer which metabolic pathways are active without performing metabolite identification. Use it especially when you have feature-level p-values from differential analysis but lack confident metabolite annotations, or when you want pathway-level functional interpretation that is robust to annotation uncertainty.

## When NOT to use

- Your metabolic model lacks chemical formulas for compounds and no identifier translation module is available to look them up
- You have already performed comprehensive metabolite identification and want to use those identities directly in quantitative pathway analysis rather than network-based inference
- Your feature table contains no statistical test results (p-values) or intensity values to propagate as activity signals through the network

## Inputs

- Untargeted metabolomics feature table (TSV/CSV with m/z, retention time, intensity, p-value columns)
- Optional: Feature annotation table (from authentic standards and MS/MS, structured in metDataModel format)
- Metabolic model in JSON format (list of pathways, reactions, compounds with chemical formulas; default models provided by mummichog or user-supplied)
- Optional: Compound identifier translation mapping

## Outputs

- Result tables and figures (HTML report as main deliverable)
- JSON strings of pathway analysis results (for programmatic use)
- JSON strings of network module analysis results
- Ranked list of predicted functional pathways with activity scores

## How to apply

Load the untargeted metabolomics feature table containing m/z, retention time, and intensity measurements into Python. Construct or load a metabolic network representation (provided by mummichog or user-supplied in JSON format) that captures biochemical pathway organization and metabolite connectivity, ensuring compound formulas are present or can be looked up via identifiers. Map feature m/z values to network nodes using mass-matching (without explicit metabolite identification), accounting for adducts and neutral masses. Propagate activity signals (derived from feature p-values or intensities) through the metabolic network using graph-based algorithms to infer which pathways show coordinated activation. Aggregate and rank pathway-level predictions by network evidence strength, outputting structured results (pathway activity scores, ranked functional predictions) in HTML and JSON formats for both visual inspection and programmatic downstream use.

## Related tools

- **mummichog** (Core Python package that implements network-based pathway prediction from untargeted metabolomics feature tables; performs mass-matching, network propagation, and pathway ranking) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model framework for structuring metabolomics annotations (used by mummichog to organize feature metadata))
- **JMS** (Performs MS/MS-based metabolite annotation (optional input to enrich feature annotations before network analysis)) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Utility library for mass spectrometry data interpretation and adduct calculations (underpins m/z-to-compound mapping))

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Output JSON contains non-empty lists of predicted pathways ranked by evidence strength (network connectivity and signal propagation depth)
- Predicted pathway scores correlate with expected biology (known differential metabolic activity in the experimental context should rank highly)
- Feature-to-network mappings respect chemical mass tolerance (adducts and neutral masses match observed m/z within instrument accuracy)
- HTML report contains both pathway rankings and network visualizations, confirming signal propagation through biochemically connected nodes
- Results remain stable across multiple runs with same inputs, indicating deterministic network propagation

## Limitations

- Accuracy depends critically on the completeness and correctness of the input metabolic model; incomplete or incorrect pathway definitions will produce misleading rankings
- Requires chemical formulas for compounds (either in model or via lookup); models missing this information cannot perform accurate mass-matching
- Pathway definition may be unavailable in some metabolic models; 'subsystem' annotation can be used as a substitute but may not represent true biological pathways
- Network-based inference cannot distinguish between direct pathway activation and indirect effects propagated through network connectivity
- Results do not identify individual metabolites; functional predictions operate at pathway level and should be validated with targeted metabolite analysis

## Evidence

- [intro] Feature-table-based pathway prediction without metabolite ID: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [other] Workflow steps for network mapping and signal propagation: "Map feature m/z values to network nodes via mass-matching without performing explicit metabolite identification. Propagate activity signals through the metabolic network using graph-based algorithms"
- [readme] Input format specification: "User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID."
- [readme] Metabolic model requirements and format: "The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds. We need chemical formulas of the compounds, which may not be available in a GSMM."
- [readme] Output format and deliverables: "Outpout are 1. Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use."
- [readme] Chemical formula and adduct handling: "If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format. Salts are formed in both biological systems and in mass spectrometry. We use neutral formula"
