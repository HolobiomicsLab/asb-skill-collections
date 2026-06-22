---
name: pathway-activity-propagation-inference
description: Use when when you have an untargeted metabolomics feature table (m/z values, retention times, intensity measurements, and p-values from statistical testing) and want to predict which metabolic pathways are active, but metabolite identification is incomplete, unreliable, or computationally expensive.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  tools:
  - Python
  - mummichog (v3)
  - JMS
  - metDataModel
  - mass2chem
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1003123
  all_source_dois:
  - 10.1371/journal.pcbi.1003123
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-activity-propagation-inference

## Summary

Infer functional pathway activation from untargeted metabolomics feature tables by propagating intensity signals through a metabolic network graph, without requiring explicit metabolite identification. This network-based approach ranks pathways by the strength of biochemical evidence in the feature data.

## When to use

When you have an untargeted metabolomics feature table (m/z values, retention times, intensity measurements, and p-values from statistical testing) and want to predict which metabolic pathways are active, but metabolite identification is incomplete, unreliable, or computationally expensive. Use this when the primary goal is functional interpretation at the pathway level rather than individual compound annotation.

## When NOT to use

- Input is already a comprehensive metabolite identification table; direct pathway enrichment or ORA is more straightforward.
- Metabolic network model does not have chemical formulas or identifiable compound annotations; mass-matching will fail without formula-based neutral mass calculation.
- Analysis goal requires individual metabolite identity confirmation; this skill is explicitly designed to bypass identification and may mask ambiguities.

## Inputs

- untargeted metabolomics feature table (TSV/CSV with m/z, retention time, p-value, optional feature ID)
- metabolic network model (JSON format with list_of_pathways, list_of_reactions, list_of_compounds)
- optional: annotation table on features (e.g., from MS/MS standards or JMS)
- optional: custom metabolic model with compound formulas and identifiers

## Outputs

- ranked pathway predictions with activity scores
- network-based functional activity inferences
- result tables and HTML summary (result.html)
- JSON strings from pathway analysis for programmatic use

## How to apply

Load the feature table and a metabolic network model (containing list_of_pathways, list_of_reactions, list_of_compounds with chemical formulas or resolvable identifiers). Map feature m/z values to network nodes via mass-matching without explicit metabolite identification. Use graph-based algorithms to propagate activity signals (derived from feature intensities and p-values) through the metabolic network along biochemical pathways. Aggregate the propagated signals at the pathway level and rank functional activities by network evidence strength—pathways with more and stronger connected features receive higher scores. Output ranked pathway predictions with activity scores and supporting network topology.

## Related tools

- **mummichog (v3)** (core Python package that implements network-based functional activity prediction from feature tables via graph-based signal propagation) — https://github.com/metabolomics-cloud/mummichog
- **JMS** (annotation tool for metabolomics datasets; optional pre-processing step to supply or enrich feature annotation before pathway inference) — https://github.com/shuzhao-li-lab/JMS
- **metDataModel** (data model framework for structuring metabolomics annotations and metabolic models used by mummichog)
- **mass2chem** (utility library for mass spectrometry data interpretation and formula-based mass calculations)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Output pathway rankings are non-empty and ranked by activity score; no pathway has undefined or NaN scores.
- Each ranked pathway has support from ≥1 mapped features in the input table; evidence_span shows network connectivity.
- Predicted pathways are biochemically plausible given the input p-values and feature intensities; high-confidence features (low p-value) contribute to top-ranked pathways.
- Result.html or JSON output includes pathway composition, mapped feature counts per pathway, and network topology (edges between compounds and reactions).
- Pathway predictions remain stable when input features are permuted (reproducibility); signal propagation is deterministic given a fixed network and feature set.

## Limitations

- Accuracy depends critically on the quality and completeness of the metabolic network model; missing compounds or reactions reduce coverage and signal propagation.
- If compound formulas are not provided in the metabolic model, mummichog must look them up via compound identifiers; misalignment of identifiers across data sources causes mass-matching failures.
- Neutral formula (not salt format) is required for adduct calculation in mass spectrometry; incorrect formula representation can lead to false negatives in feature-to-compound matching.
- Pathway definition may not be available in all metabolic models; subsystem or other pathway surrogates may be used, reducing biological interpretability.
- Signal propagation assumes that feature intensity or p-value correlates with metabolite concentration and pathway flux; this assumption may not hold under non-physiological or experimental conditions.

## Evidence

- [other] Mummichog predicts functional activity by leveraging the organization of metabolic networks to analyze feature tables directly, thereby bypassing the need for metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [other] Map feature m/z values to network nodes via mass-matching without performing explicit metabolite identification. Propagate activity signals through the metabolic network using graph-based algorithms to infer functional pathway activation from feature intensities.: "Map feature m/z values to network nodes via mass-matching without performing explicit metabolite identification. 4. Propagate activity signals through the metabolic network using graph-based"
- [readme] We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [other] Aggregate pathway-level predictions and rank functional activities by network evidence strength.: "Aggregate pathway-level predictions and rank functional activities by network evidence strength."
- [other] Output predicted functional pathways and activity scores in a structured format.: "Output predicted functional pathways and activity scores in a structured format."
