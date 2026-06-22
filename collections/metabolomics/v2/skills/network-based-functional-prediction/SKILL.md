---
name: network-based-functional-prediction
description: Use when you have an untargeted metabolomics feature table with m/z values, retention times, intensity measurements, and p-values from statistical testing, but lack or wish to bypass metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
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

# network-based-functional-prediction

## Summary

Predict metabolic functional activity and pathway activation directly from untargeted metabolomics feature tables by propagating activity signals through a metabolic network graph, without requiring explicit metabolite identification. This approach leverages mass-to-network node mapping and graph-based algorithms to infer biochemical pathway engagement from feature intensities and statistical significance.

## When to use

You have an untargeted metabolomics feature table with m/z values, retention times, intensity measurements, and p-values from statistical testing, but lack or wish to bypass metabolite identification. You want to know which metabolic pathways or functional modules are active in your samples despite having many unidentified features. Use this skill when your goal is pathway-level or functional inference rather than compound-level annotation.

## When NOT to use

- Your primary goal is to identify the chemical identity of individual metabolites — use targeted MS/MS annotation or database matching instead.
- Your feature table is already annotated to specific metabolites and you only need compound-level summary statistics.
- You lack or cannot construct a metabolic network model with compound chemical formulas for your organism or biological context.

## Inputs

- untargeted metabolomics feature table (TSV/CSV with columns: feature_ID, m/z, retention_time, intensity, p-value)
- metabolic network model (JSON format with list_of_pathways, list_of_reactions, list_of_compounds including chemical formulas)
- optional: annotation table mapping features to known metabolites (from authentic standards or MS/MS)

## Outputs

- pathway activity predictions ranked by network evidence strength
- result tables and figures in HTML format
- JSON strings containing pathway analysis and network module analysis results for programmatic use

## How to apply

Load the feature table (m/z, retention time, intensity, p-value) and a metabolic model containing lists of pathways, reactions, and compounds with chemical formulas. Map feature m/z values to metabolic network nodes via mass-matching tolerance (neutral mass calculation accounting for adducts and salts formed in mass spectrometry). Propagate activity signals (feature intensities and statistical significance) through the network using graph-based algorithms to infer which pathways or subsystems are activated. Aggregate evidence across connected features and reactions to rank functional pathways by network support strength. Output pathway activity scores, ranked predictions, and network evidence in both human-readable tables/figures (HTML) and machine-readable JSON for downstream analysis.

## Related tools

- **mummichog** (Core Python package that implements network-based functional prediction from feature tables via mass-to-network mapping and graph propagation) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model framework for structuring metabolomics annotations compatible with mummichog)
- **JMS** (Annotation tool for assigning metabolite identities to features, optionally feeding annotation table into mummichog) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Utilities for interpreting mass spectrometry data and mass-to-formula calculations including adduct and salt handling)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Ranked pathways should show biochemically coherent clusters (e.g., related lipid or amino acid metabolism pathways ranked together) rather than scattered, unrelated pathways.
- Network evidence strength scores should correlate with the number of significant features mapping to pathway reactions and the connectivity of those features through the network.
- Output JSON should contain explicit pathway names, reaction lists, and feature-to-node mapping for reproducibility and downstream filtering.
- HTML result should show network visualizations where node and edge weights correspond to feature intensity and pathway connectivity.
- Re-running with the same feature table and model should produce identical ranked pathway predictions (deterministic output).

## Limitations

- Requires accurate chemical formulas in the metabolic model; incorrect or missing formulas will cause mass-matching failures and reduce pathway coverage.
- Mass-to-node mapping relies on mass tolerance and adduct specification; incorrect adduct models or tolerance settings will misalign features to the network.
- Pathway definition and subsystem organization vary across metabolic models; results depend heavily on model choice and completeness.
- Cannot distinguish between multiple isomeric features with identical m/z; network propagation may conflate activity signals from co-eluting compounds.
- Assumes that feature intensity or p-value correlates with metabolite abundance and pathway activity; highly variable or noisy features may produce spurious pathway predictions.

## Evidence

- [intro] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [readme] Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics.: "Mummichog is a Python program for analyzing data from high throughput, untargeted metabolomics."
- [readme] User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID.: "User supplied features with m/z, rtime, p-value from a statistical test."
- [readme] The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds.: "The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds."
- [readme] We use neutral formula to calculate adducts in mass spec, which includes salts.: "We use neutral formula to calculate adducts in mass spec, which includes salts."
- [readme] Outpout are 1. Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use.: "Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use."
