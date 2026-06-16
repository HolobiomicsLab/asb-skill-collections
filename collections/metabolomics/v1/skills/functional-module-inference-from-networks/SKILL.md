---
name: functional-module-inference-from-networks
description: Use when you have an untargeted metabolomics feature table (m/z and retention time columns) and a statistical test result (p-value) per feature, but lack confident metabolite identifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - mass2chem
derived_from:
- doi: 10.1371/journal.pcbi.1003123
  title: mummichog
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mummichog
    doi: 10.1371/journal.pcbi.1003123
    title: mummichog
  dedup_kept_from: coll_mummichog
schema_version: 0.2.0
---

# functional-module-inference-from-networks

## Summary

Infer metabolic functional activity and pathway membership directly from untargeted metabolomics feature tables by mapping m/z values onto a metabolic network graph and propagating signals through connected nodes, without requiring explicit metabolite identification. This approach predicts which metabolic modules and pathways are active in a sample based on the spatial organization of detected features within the network.

## When to use

You have an untargeted metabolomics feature table (m/z and retention time columns) and a statistical test result (p-value) per feature, but lack confident metabolite identifications. Your analysis goal is to predict which metabolic pathways or functional modules are active, rather than identifying individual metabolites. You have access to a metabolic network model (in JSON format with pathways, reactions, and compounds including chemical formulas).

## When NOT to use

- Input is already a fully annotated metabolite table with identifications; use targeted pathway enrichment instead.
- Your metabolic network model lacks chemical formulas or compound identifier alignment; functional module inference requires accurate mass matching and formula-based adduct calculation.
- You require confidence in individual metabolite identifications; this skill outputs pathway-level predictions, not compound-level annotations.

## Inputs

- untargeted metabolomics feature table (CSV/TSV with m/z, retention time, p-value, optional feature ID)
- metabolic network model (JSON with list_of_pathways, list_of_reactions, list_of_compounds)
- optional: annotation table on features (e.g., from authentic standards or MS/MS)
- mass-to-charge tolerance threshold (ppm)

## Outputs

- pathway activity predictions (tables and JSON)
- network module analysis results (JSON)
- network mapping statistics (feature-to-node matches, pathway coverage)
- result.html with figures and aggregated activity scores

## How to apply

Load the feature table (TSV/CSV format with m/z, retention time, and p-value columns) and initialize a metabolic network model in JSON format, ensuring compound records contain correct neutral-mass chemical formulas (not salt formats, since both biological and mass-spec contexts produce salts and adducts). Map each feature's m/z value to network compound nodes using a mass-to-charge tolerance window (typically in ppm). Propagate the feature signal (weighted by p-value or intensity) through the metabolic network graph to neighboring compounds and their associated reactions and pathways. Aggregate network-level activity scores across connected modules to infer functional activity. Output includes pathway activity predictions, network module scores, and mapping statistics (e.g., fraction of features matched, network coverage). Rationale: signal propagation through metabolic connectivity allows weak or unmapped individual features to contribute to pathway inference when their m/z neighbors are well-connected.

## Related tools

- **Mummichog 3** (Core Python program that implements network-based feature table analysis, signal propagation, and functional module inference) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model framework for structuring metabolomics annotations and metabolic models used by Mummichog)
- **JMS** (Tool for performing annotation on metabolomics datasets; can supply optional annotation tables to Mummichog) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Utility library for interpreting mass spectrometry data, annotation, and chemical formula calculations (adducts, neutral mass))

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Verify that m/z tolerance matching aligns feature precision with expected mass accuracy; check fraction of input features mapped to network nodes (coverage %).
- Confirm metabolic model validity: all compounds have chemical formulas; compound identifiers are internally consistent; pathway and reaction definitions are non-empty.
- Check that pathway activity scores aggregate correctly (e.g., pathway score ≥ max feature p-value in that pathway); validate that signal propagation respects network topology (features only contribute through connected pathways).
- Compare output activity ranks against known biology (e.g., expected metabolic pathways should rank higher than unrelated ones in positive control samples).
- Ensure JSON output is parseable and contains non-null pathway and network module scores; HTML visualization should display network heatmaps and activity confidence intervals.

## Limitations

- Requires chemically accurate metabolic model with correct neutral-mass formulas and aligned compound identifiers; models lacking formulas require lookup via external databases, introducing potential identifier mismatch.
- Signal propagation depends critically on network connectivity; sparsely connected or isolated features contribute minimally to pathway inference even if biologically relevant.
- Pathway definitions may be unavailable in some metabolic models; 'Subsystem' fields may be used as substitutes, reducing interpretability.
- Does not perform explicit metabolite identification; functional predictions are network-level inferences and may conflate multiple isomeric or isobaric compounds mapping to the same m/z.
- Mummichog 3 is under active development; no changelog available, and backward compatibility with version 2 is not guaranteed beyond the mummichog-2.7 branch.

## Evidence

- [intro] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [other] Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signals through the metabolic network to infer functional modules and pathways.: "Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signals through the metabolic network to infer functional modules and pathways."
- [readme] User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID.: "User supplied features with m/z, rtime, p-value from a statistical test. If no unique feature ID is supplied, row_number will be used as ID."
- [readme] We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [other] Aggregate network-level activity scores and generate functional activity predictions without performing explicit metabolite identification.: "Aggregate network-level activity scores and generate functional activity predictions without performing explicit metabolite identification."
