---
name: metabolic-network-mapping
description: Use when you have an untargeted metabolomics feature table (with m/z,
  retention time, and statistical significance values) and want to predict which metabolic
  pathways and functional modules are active in your sample, but you lack confident
  metabolite identifications or wish to bypass the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0159
  - http://edamontology.org/topic_0602
  tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - mass2chem
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-network-mapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Map untargeted metabolomics feature table m/z values onto a metabolic network structure to predict functional activity and pathway involvement without requiring explicit metabolite identification. This approach leverages network organization to infer functional modules directly from feature-level data.

## When to use

You have an untargeted metabolomics feature table (with m/z, retention time, and statistical significance values) and want to predict which metabolic pathways and functional modules are active in your sample, but you lack confident metabolite identifications or wish to bypass the metabolite ID bottleneck entirely.

## When NOT to use

- Your input is already a validated metabolite list with confirmed identifications — use network mapping to augment, not replace, annotation.
- You require identification of specific metabolites rather than functional pathway inference — this skill predicts activity without naming individual compounds.
- Your metabolic model lacks chemical formulas for compounds — you must either supply formulas or use a model with complete compound definitions and correct neutral masses (not salt formats).

## Inputs

- Feature table (CSV/TSV): m/z, retention time, p-value, feature ID
- Metabolic network model (JSON): list_of_compounds (with chemical formulas and neutral masses), list_of_reactions, list_of_pathways
- Optional: annotation table on features from authentic standards or MS/MS

## Outputs

- Pathway activity predictions (JSON and HTML)
- Network module analysis results
- Result tables and figures (result.html)
- Network mapping statistics and feature-to-node assignments

## How to apply

Load the feature table in CSV/TSV format with m/z and retention time columns into Mummichog. Initialize a metabolic network database (provided or user-supplied in JSON format with list_of_compounds, list_of_reactions, and list_of_pathways) and retrieve its structure. Map each feature's m/z value to network compound nodes using a mass-to-charge tolerance threshold (exact tolerance not specified in docs but inferred from mass spectrometry practice). Propagate feature signals through the metabolic network graph to identify which reaction modules and pathways contain mapped features. Aggregate network-level activity scores across connected compounds and reactions to generate functional activity predictions. Verify that mapped features fall within plausible adduct patterns (neutral mass + salt forms) and that compound formulas in the model use neutral mass representation, not salt formats.

## Related tools

- **Mummichog 3** (Core Python package that performs metabolic network initialization, m/z-to-node mapping, signal propagation, and functional activity prediction) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model library for structuring metabolomics annotations and metabolic model definitions used by Mummichog)
- **JMS** (Utility for performing metabolite annotation on datasets before or alongside network mapping) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Common utilities for interpreting mass spectrometry data and adduct calculation for neutral-to-measured mass conversion)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- All feature m/z values successfully map to at least one network compound within the specified tolerance; check network mapping statistics output.
- Mapped features cluster on known metabolic pathways relevant to the biological context (e.g., lipid metabolism, amino acid synthesis).
- Network-level activity scores are reproducible across identical inputs and show expected biological patterns (e.g., higher activity in pathways known to be active in the sample condition).
- Compound formulas in the input metabolic model use neutral masses; verify no salt-format formulas are present that would cause adduct mismatch.
- Feature-to-pathway assignments are consistent with the topology of the metabolic network (features in the same pathway or connected reactions should show correlated activity).

## Limitations

- Requires a complete, accurate metabolic network model with compound formulas and correct neutral masses; incomplete or mislabeled models degrade accuracy.
- Does not provide explicit metabolite identification — only functional activity prediction; cannot name which specific compounds are present.
- Pathway definitions may not be available in all metabolic models; 'subsystem' fields may be used as a substitute but with less biological validation.
- Compound identifiers in the metabolic model must align with external databases; translation modules are needed for model format conversion.
- Performance depends critically on the choice of m/z-to-node matching tolerance; no guidance on tolerance selection is provided in the README.

## Evidence

- [intro] Mummichog leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [readme] Feature table input format and required columns for m/z and retention time.: "User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID."
- [readme] Metabolic model structure and requirement for chemical formulas.: "The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds. We need chemical formulas of the compounds, which may not be available in a GSMM."
- [readme] Critical requirement for neutral mass representation in compound formulas.: "If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format. Salts are formed in both biological systems and in mass spectrometry. We use neutral formula"
- [other] Workflow steps for network initialization and signal propagation.: "Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signals through the metabolic network to infer functional modules and pathways."
- [readme] Output format and result types produced by the analysis.: "Outpout are 1. Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use."
