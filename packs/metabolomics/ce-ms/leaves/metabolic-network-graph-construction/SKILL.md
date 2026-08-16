---
name: metabolic-network-graph-construction
description: Use when when you have an untargeted metabolomics feature table (m/z values, retention times, intensities) and aim to predict functional pathway activity without explicit metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - mummichog
  - JMS
  techniques:
  - CE-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-network-graph-construction

## Summary

Construct or load a metabolic network representation that captures biochemical pathway organization and metabolite connectivity, enabling graph-based propagation of activity signals through network nodes. This is a foundational step in network-based functional prediction from untargeted metabolomics feature tables.

## When to use

When you have an untargeted metabolomics feature table (m/z values, retention times, intensities) and aim to predict functional pathway activity without explicit metabolite identification. Use this skill when you need to map observed features to biochemical pathways via network topology rather than individual metabolite identifiers.

## When NOT to use

- Input already contains fully identified metabolites with high-confidence MS/MS spectra; direct compound-level pathway lookup may be more efficient than network propagation.
- Metabolic model lacks chemical formulas or compound identifiers cannot be reliably resolved; mass-to-node mapping will fail or be unreliable.
- Analysis goal is single-metabolite biomarker discovery rather than pathway-level functional inference.

## Inputs

- Metabolic model definition (JSON format with list_of_pathways, list_of_reactions, list_of_compounds)
- Compound chemical formulas (neutral mass format)
- Compound identifier mappings (e.g., KEGG IDs, ChEBI)
- Pathway or subsystem definitions

## Outputs

- Metabolic network graph object (in-memory representation with nodes as metabolites/reactions, edges as pathway connections)
- Node-to-compound identifier mapping table
- Pathway-to-reaction mapping for downstream aggregation

## How to apply

Obtain or construct a metabolic network model in JSON format containing list_of_pathways, list_of_reactions, and list_of_compounds. Ensure compound entries include chemical formulas (neutral mass, not salt format) and identifiers aligned with your annotation sources; if formulas are missing, resolve them via compound identifiers. Load the model representation into your analysis environment (Python) as a graph structure capturing metabolite connectivity and pathway organization. Validate that the network includes pathway definitions or subsystem metadata to enable downstream aggregation of activity scores. The constructed graph serves as the topology through which feature intensities will be propagated to infer functional activities.

## Related tools

- **mummichog** (Python package that loads, constructs, and validates metabolic network models from JSON and performs mass-to-node mapping and graph-based pathway analysis) — https://github.com/metabolomics-cloud/mummichog
- **JMS** (Companion tool for metabolite annotation and model format conversion, used to prepare metabolic models with aligned compound identifiers) — https://github.com/shuzhao-li-lab/JMS

## Examples

```
```python
from mummichog import models
metabolic_network = models.load_model('default_model.json')
# or: metabolic_network = models.convert_gsmm('genome_scale_model.xml', resolve_formulas=True)
```
```

## Evaluation signals

- Network graph contains all compounds and reactions from input model; node count matches expected pathway complexity.
- Compound formulas are in neutral (non-salt) format; calculated monoisotopic masses are consistent with metabolomics adduct expectations (e.g., [M+H]+, [M-H]-).
- Edges correctly represent biochemical connectivity (reactants → products); pathway membership is preserved for each node.
- Compound identifiers can be resolved via lookup; no unmapped or ambiguous nodes remain.
- Downstream mass-to-node matching (at m/z ± tolerance) successfully anchors observed features to ≥1 network node per significant feature.

## Limitations

- Network construction quality depends on metabolic model completeness and accuracy; models may not capture all relevant organisms or growth conditions.
- Chemical formulas may be unavailable in some models; requires external lookup via compound ID, introducing potential mapping errors or delays.
- Salts in compound formats produce incorrect neutral masses, leading to m/z mismatches during feature mapping.
- Pathway definitions may be sparse or missing in some models; subsystem-level organization is used as fallback but may not reflect functional relevance.
- Network size and complexity can impact computational performance of downstream graph-based algorithms.

## Evidence

- [other] Construct or load a metabolic network representation capturing biochemical pathway organization and metabolite connectivity.: "Construct or load a metabolic network representation capturing biochemical pathway organization and metabolite connectivity."
- [readme] The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds.: "The format of a metabolic model contains list_of_pathways, list_of_reactions and list_of_compounds."
- [readme] We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [readme] If formulas are not provided in a model, we need to look them up via compound identifiers. The compound identifiers need to align with other data.: "If formulas are not provided in a model, we need to look them up via compound identifiers. The compound identifiers need to align with other data."
- [readme] Pathway definition may not be available in some models. 'Subsystem' could be a substitute.: "Pathway definition may not be available in some models. 'Subsystem' could be a substitute."
