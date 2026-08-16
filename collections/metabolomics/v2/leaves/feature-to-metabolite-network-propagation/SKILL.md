---
name: feature-to-metabolite-network-propagation
description: Use when you have an untargeted metabolomics feature table (m/z, retention
  time, p-value from statistical test) but lack comprehensive metabolite identifications
  or MS/MS annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_2275
  tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - mass2chem
  techniques:
  - LC-MS
  license_tier: restricted
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

# feature-to-metabolite-network-propagation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Map untargeted metabolomics feature m/z values onto a metabolic network and propagate signal through connected nodes to infer functional activity and pathway involvement without explicit metabolite identification. This skill bypasses the bottleneck of compound annotation by leveraging network topology to predict metabolic function directly from feature tables.

## When to use

You have an untargeted metabolomics feature table (m/z, retention time, p-value from statistical test) but lack comprehensive metabolite identifications or MS/MS annotations. You want to predict which metabolic pathways and functional modules are active in your samples despite feature-level ambiguity. Use this when sample size, cost, or chemical complexity makes full annotation infeasible but you need pathway-level biological inference.

## When NOT to use

- Input is already a fully annotated list of metabolite identities (skill assumes feature ambiguity is the starting point)
- Your metabolic model lacks chemical formulas for compounds; without neutral mass and adduct information, m/z matching becomes unreliable
- You require compound-level identifications; this skill predicts pathway activity, not individual metabolite identity

## Inputs

- Untargeted metabolomics feature table (TSV/CSV with m/z, retention time, p-value columns and optional unique feature ID)
- Metabolic model in JSON format (list_of_pathways, list_of_reactions, list_of_compounds with chemical formulas)
- Optional: annotation table on features from authentic standards or MS/MS
- Mass-to-charge tolerance threshold (ppm or Da)

## Outputs

- Pathway activity predictions with aggregated network-level scores
- Feature-to-network node mapping table with matched m/z and tolerance information
- Functional module assignments for active metabolic regions
- Result HTML report and JSON strings for programmatic downstream use

## How to apply

Load your feature table (CSV/TSV format with m/z and retention time columns) into Mummichog 3 alongside a metabolic model in JSON format (containing list_of_pathways, list_of_reactions, and list_of_compounds with chemical formulas). Match each feature m/z to metabolic network nodes using mass-to-charge tolerance matching (accounting for neutral mass, not salt format). Propagate feature signals through the connected metabolic network using the network's reaction topology to identify which functional modules and pathways are collectively active. Aggregate network-level activity scores across all matched features to generate pathway-activity predictions and module assignments. Verify that matched features cluster on biochemically coherent subnetworks rather than scattered randomly across the network.

## Related tools

- **Mummichog 3** (Core algorithm package that accepts feature tables and metabolic models, performs m/z-to-network matching and network-propagated functional prediction) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model for structuring metabolomics annotations and compound metadata for use by Mummichog)
- **JMS** (Companion tool for pre-processing and annotating feature datasets before input to Mummichog) — https://github.com/shuzhao-li-lab/JMS
- **mass2chem** (Utilities for interpreting mass spectrometry data, m/z-to-neutral-mass conversion, and adduct calculation)

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Matched features cluster on biochemically coherent metabolic subnetworks (e.g., connected pathways for fatty acid or amino acid metabolism) rather than scattered randomly across the network
- Pathway activity predictions show statistical significance or ranking consistent with the p-values supplied in the input feature table
- Network mapping statistics report reasonable m/z matching rates within the specified tolerance threshold (e.g., no unexpectedly high false-match rates)
- Generated pathway annotations align with known biology of the sample type or experimental treatment
- JSON output structures contain valid pathway, reaction, and compound node references traceable back to the input metabolic model

## Limitations

- Requires a high-quality metabolic model with accurate compound chemical formulas; missing or incorrect formulas (especially salt vs. neutral form) cause m/z mismatch errors
- Compound identifiers in the metabolic model must align with external databases if formula lookup is needed; inconsistent naming or versioning reduces match rate
- Pathway definitions may be absent in some metabolic models; 'Subsystem' tags can substitute but may not reflect functional biology
- Mass spectrometry salt formation in both biological systems and instrument can confound neutral mass calculation if not accounted for
- Network propagation assumes connectivity implies co-activity, which may not hold when pathways are independently regulated or when features represent parallel metabolic routes

## Evidence

- [readme] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
- [other] Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signals through the metabolic network to infer functional modules and pathways.: "Map feature m/z values to metabolic network nodes using mass-to-charge tolerance matching. Propagate feature signals through the metabolic network to infer functional modules and pathways."
- [readme] Input: 1. User supplied features with m/z, rtime, p-value from a statistical test. 2. [Optional] Annotation table on the features. 3. [Optional] Metabolic model to use.: "User supplied features with m/z, rtime, p-value from a statistical test. [Optional] Annotation table on the features. [Optional] Metabolic model to use."
- [readme] We use neutral formula to calculate adducts in mass spec, which includes salts. If formulas are not provided in a model, we need to look them up via compound identifiers.: "We use neutral formula to calculate adducts in mass spec, which includes salts. If formulas are not provided in a model, we need to look them up via compound identifiers."
- [readme] Outpout are 1. Result tables and figures, result.html as ver 2. 2. JSON strings from pathway analysis and network module analysis for programmatic use.: "Result tables and figures, result.html as ver 2. JSON strings from pathway analysis and network module analysis for programmatic use."
