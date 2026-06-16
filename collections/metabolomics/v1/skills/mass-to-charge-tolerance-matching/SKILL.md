---
name: mass-to-charge-tolerance-matching
description: Use when you have an untargeted metabolomics feature table (with m/z and retention time columns) and a metabolic network database with compound chemical formulas, and you want to connect observed features to known metabolic reactions and pathways using mass matching rather than metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Mummichog 3
  - mass2chem
  - JMS
  - metDataModel
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

# mass-to-charge-tolerance-matching

## Summary

Map untargeted metabolomics feature m/z values to metabolic network nodes by matching observed mass-to-charge ratios against theoretical compound masses within a specified tolerance window. This enables feature-level functional inference without requiring explicit metabolite identification.

## When to use

You have an untargeted metabolomics feature table (with m/z and retention time columns) and a metabolic network database with compound chemical formulas, and you want to connect observed features to known metabolic reactions and pathways using mass matching rather than metabolite annotation.

## When NOT to use

- Features have already been identified and annotated to specific metabolites—use annotation tables directly instead
- Metabolic model lacks compound chemical formulas or neutral mass values—formulas must be available or resolvable via compound identifiers
- Mass spectrometry data have very poor mass accuracy (>>10 ppm for typical high-resolution instruments)—matching will be unreliable

## Inputs

- Untargeted metabolomics feature table (CSV/TSV with m/z, retention time, p-value columns)
- Metabolic network database in JSON format (containing list_of_compounds with chemical formulas and neutral masses, list_of_reactions, list_of_pathways)
- Optional: mass-to-charge tolerance parameter (ppm or Da)

## Outputs

- Feature-to-compound mapping table (feature ID → matched compound(s))
- Network-level pathway activity scores
- Network module analysis results (JSON format for programmatic use)
- Functional activity predictions without explicit metabolite identification

## How to apply

Load the feature table and metabolic network database, which contains lists of compounds with calculated neutral masses derived from their chemical formulas. For each feature m/z value, search the compound mass index using a mass-to-charge tolerance (typically a few ppm for high-resolution instruments) to identify candidate matches. Retain all matches within tolerance rather than enforcing a single best match, as multiple isomeric or isobaric compounds may share the same m/z. These matched features are then propagated through the metabolic network structure (reactions, pathways, subsystems) to aggregate network-level activity signals. The tolerance parameter should be chosen based on instrument resolution and mass accuracy; the README emphasizes that compound formulas must reflect neutral mass, not salt or adduct forms, since adducts are calculated separately during annotation.

## Related tools

- **Mummichog 3** (Core algorithm package that performs mass-to-charge tolerance matching and metabolic network propagation for untargeted metabolomics feature tables) — https://github.com/metabolomics-cloud/mummichog
- **mass2chem** (Common utilities for interpreting mass spectrometry data and managing compound mass calculations)
- **JMS** (Annotation tool that can be used to perform MS/MS-based annotation on datasets before or after mass matching) — https://github.com/shuzhao-li-lab/JMS
- **metDataModel** (Data model framework for structuring metabolomics annotation data and metabolic model information)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Feature-to-compound mapping statistics: number of matched features, distribution of matches per feature (singleton vs. multiple matches), and coverage of input feature table
- Mass accuracy check: verify that matched compound masses are within the specified tolerance window (e.g., all matches within ±5 ppm for high-resolution data)
- Network propagation invariant: confirm that matched features produce non-zero activity scores only for pathways and reactions that actually contain the matched compounds
- Consistency with optional annotations: if annotation table is provided, verify that mass-matched compounds are consistent with (or orthogonal to) annotated metabolites
- Downstream functional predictions: pathway and module activity scores should be computable and aggregatable from feature-level matches without errors

## Limitations

- Multiple compounds may have identical m/z values within tolerance, especially for isobaric or isomeric species; the method propagates all matches but does not resolve ambiguity
- Requires accurate neutral chemical formulas in the metabolic model; salt or adduct-form formulas will produce incorrect masses and failed matches
- Compound identifiers in the model must be traceable and resolvable if formulas are not directly provided; translation modules may be needed for different model sources
- Mass matching alone cannot distinguish between features arising from the same compound in different ionization states or as different adducts; such disambiguation requires additional metadata or annotation
- Pathway definitions may not be available in all metabolic models; subsystem fields may be used as a substitute, which may affect biological interpretation

## Evidence

- [other] Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching.: "Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching."
- [intro] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [readme] If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [readme] The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds.: "The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds."
- [other] Load the untargeted metabolomics feature table (CSV/TSV format with m/z and retention time columns).: "Load the untargeted metabolomics feature table (CSV/TSV format with m/z and retention time columns)."
