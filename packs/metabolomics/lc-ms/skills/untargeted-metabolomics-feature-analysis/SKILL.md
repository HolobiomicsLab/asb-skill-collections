---
name: untargeted-metabolomics-feature-analysis
description: Use when you have a feature table from untargeted metabolomics (with m/z, retention time, and p-values from differential abundance testing) but lack or wish to bypass metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - mass2chem
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1003123
  title: mummichog
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mummichog
    doi: 10.1371/journal.pcbi.1003123
    title: mummichog
  dedup_kept_from: coll_mummichog
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

# untargeted-metabolomics-feature-analysis

## Summary

Map untargeted metabolomics feature tables (m/z, retention time, statistical significance) onto metabolic networks to predict functional pathway activity without requiring explicit metabolite identification. This skill leverages network-level propagation of feature signals to infer active metabolic modules and pathways directly from feature-level data.

## When to use

You have a feature table from untargeted metabolomics (with m/z, retention time, and p-values from differential abundance testing) but lack or wish to bypass metabolite annotation. You want to predict which metabolic pathways and functional modules are active based on the spatial organization of features within known metabolic networks, rather than identifying individual compounds.

## When NOT to use

- Input features are already annotated to specific metabolites and you need high-resolution compound-level predictions rather than pathway-level summaries.
- Metabolic model lacks chemical formulas or reliable compound identifiers that align with your feature annotation data.
- Your research question requires unambiguous metabolite identification (e.g., to support biomarker validation or pharmacokinetic tracing).

## Inputs

- Feature table (TSV/CSV): columns for m/z, retention time, p-value, optional feature ID
- Metabolic network model (JSON): list_of_pathways, list_of_reactions, list_of_compounds with chemical formulas
- Optional: Annotation table on features (from authentic standards or MS/MS)

## Outputs

- Pathway-level activity scores and predictions
- Network module analysis results
- Result tables and figures (HTML report)
- JSON strings for programmatic integration

## How to apply

Load the untargeted metabolomics feature table (TSV/CSV format with required columns: m/z, retention time, p-value, and optional feature ID). Initialize a metabolic network database (JSON format containing list_of_pathways, list_of_reactions, list_of_compounds with chemical formulas). Match feature m/z values to metabolic network compound nodes using mass-to-charge tolerance matching (accounting for adducts and salt forms). Propagate feature signals (weighted by p-value or abundance) through the connected metabolic network structure to aggregate activity at the pathway and functional module level. Generate functional predictions without performing explicit metabolite identification. Validate that neutral mass formulas (not salt forms) were used in the model for accurate adduct calculation.

## Related tools

- **Mummichog 3** (Core Python program that accepts feature tables and metabolic models, performs network-based propagation, and outputs functional activity predictions without metabolite identification) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model framework for structuring metabolomics annotations and feature metadata compatible with Mummichog input)
- **JMS** (Tool for performing metabolite annotation on datasets; output can optionally feed Mummichog as annotation table) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Utilities for interpreting mass spectrometry data and calculating neutral mass / adduct forms used in feature-to-network matching)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Feature m/z values are successfully matched to metabolic network compound nodes within specified mass-to-charge tolerance; check matching statistics output.
- Pathway and module activity scores are generated for all connected network regions; verify that signal propagation produces non-zero activity in pathways containing matched features.
- Output JSON and HTML report are produced without errors; validate schema compliance of JSON pathway/module results.
- Functional predictions correspond to pathways containing features with low p-values (high statistical significance); verify that activity scores correlate with input feature significance.
- Neutral mass formulas (not salt forms) were correctly applied in compound–adduct mapping; inspect model.json compound entries for formula format and cross-check against literature neutral masses.

## Limitations

- Requires a validated metabolic model with accurate chemical formulas for all compounds; missing or incorrect formulas will cause failed or spurious feature-to-compound matches.
- Compound identifiers must align across the metabolic model and any external annotation tables; misalignment breaks linkage between pathway definitions and feature-level activity.
- Cannot handle metabolic models that lack pathway definitions; subsystems may be used as a substitute, but network propagation strength depends on pathway connectivity depth.
- Feature signal aggregation assumes that co-localized features in the network reflect coordinated pathway activity, which may not hold if features arise from independent or unrelated biochemical processes.
- Adduct and salt forms in mass spectrometry require careful handling: neutral formulas must be used for accurate m/z matching, and both biological and instrument-induced salts must be considered.

## Evidence

- [readme] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [other] Load the untargeted metabolomics feature table (CSV/TSV format with m/z and retention time columns). Initialize the metabolic network database and retrieve the network structure. Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching.: "Load the untargeted metabolomics feature table (CSV/TSV format with m/z and retention time columns). Initialize the metabolic network database and retrieve the network structure. Map feature m/z"
- [readme] We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [other] Propagate feature signals through the metabolic network to infer functional modules and pathways. Aggregate network-level activity scores and generate functional activity predictions without performing explicit metabolite identification.: "Propagate feature signals through the metabolic network to infer functional modules and pathways. Aggregate network-level activity scores and generate functional activity predictions without"
- [readme] User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID.: "User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID."
