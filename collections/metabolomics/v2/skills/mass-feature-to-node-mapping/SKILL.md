---
name: mass-feature-to-node-mapping
description: Use when you have an untargeted metabolomics feature table with m/z values, retention times, and intensity measurements, a metabolic network representation with compound nodes and chemical formulas, and you want to infer functional pathway activity directly from features without performing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - mummichog
  - metDataModel
  - JMS
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

# mass-feature-to-node-mapping

## Summary

Map untargeted metabolomics m/z features to metabolic network nodes via mass matching to enable functional activity prediction without explicit metabolite identification. This is the critical bridge step that connects raw mass spectrometry observations to biochemical pathway context.

## When to use

You have an untargeted metabolomics feature table with m/z values, retention times, and intensity measurements, a metabolic network representation with compound nodes and chemical formulas, and you want to infer functional pathway activity directly from features without performing metabolite identification or annotation.

## When NOT to use

- Targeted metabolomics where metabolite identities are already confirmed via standards or high-confidence tandem MS — use direct annotation instead.
- When chemical formulas are unavailable and cannot be looked up via compound identifiers — mapping requires neutral mass calculations from formulas.
- When the metabolic model contains incorrect or salt-format formulas rather than neutral formulas — this will produce incorrect adduct predictions and failed m/z matches.

## Inputs

- Untargeted metabolomics feature table (m/z values, retention times, intensity measurements, p-values from statistical test)
- Metabolic network model (JSON format containing list_of_pathways, list_of_reactions, list_of_compounds with neutral chemical formulas)
- Optional: annotation table on features from authentic standards or MS/MS

## Outputs

- Feature-to-network-node mapping (m/z-indexed associations linking each feature to one or more metabolic network compounds)
- Annotated feature table with network node IDs and mass-matching confidence scores
- Input data structure ready for graph-based signal propagation and pathway analysis

## How to apply

Load the untargeted metabolomics feature table containing m/z values and intensity measurements alongside a metabolic network representation that includes list_of_compounds with neutral chemical formulas (ensuring formulas are in neutral, not salt, format). For each feature m/z value, perform mass matching against network compound nodes by calculating adducts from their neutral formulas; mummichog performs this indexing and calculation on chemical formulas to test matches to metabolomic data patterns. Use the matched m/z-to-node associations as the foundation for downstream graph-based signal propagation and pathway activity inference. Ensure compound identifiers in the model align with your data and that formulas are available (either provided directly or looked up via compound identifiers); if formulas are missing from a model, they must be added before mapping.

## Related tools

- **mummichog** (Core Python package that performs mass-matching indexing and calculation on chemical formulas to map m/z features to metabolic network nodes; handles adduct calculation from neutral formulas) — https://github.com/metabolomics-cloud/mummichog
- **metDataModel** (Data model framework for structuring metabolomics annotation and metabolic model compound representation with chemical formula metadata)
- **JMS** (Tool for annotation of metabolomics datasets; can prepare annotation tables and metabolic model conversions upstream of mass-feature-to-node mapping) — https://github.com/shuzhao-li-lab/JMS

## Examples

```
python3 -m mummichog.main -i tests/ineurons_ttest_1127.tsv -j testneuron -a tests/empCpds_with_annotations.json -d .
```

## Evaluation signals

- Verify that every feature m/z value has at least one associated network node (or document features with no match and confirm these are expected, e.g., contaminants or instrumental artifacts).
- Check that matched m/z values fall within the expected mass tolerance of the model's chemical formulas when accounting for specified adducts (e.g., [M+H]+, [M-H]−, [M+Na]+).
- Confirm that network nodes with multiple mapped features show consistent adduct patterns (e.g., the same compound node should not be matched via both [M+H]+ and [M+2H]2+ if only singly charged ions are expected).
- Validate that mapped nodes are structurally connected in the metabolic network and that intensity patterns across co-localized features in a pathway are biologically plausible.
- Compare the number and distribution of matched features across pathways to expected metabolic coverage for the biological system (e.g., central carbon metabolism should be well-covered in primary metabolomics).

## Limitations

- Mass matching is ambiguous when multiple network compounds share similar or identical neutral masses, especially in high m/z regions or with limited mass spectrometry resolution; the method does not resolve these ambiguities without retention time or MS/MS data.
- Accuracy depends critically on correctness of compound chemical formulas in the metabolic model; if formulas are missing, incorrect, or in salt format rather than neutral format, m/z matching will fail or produce false associations.
- The method bypasses metabolite identification entirely, so mapped features may not correspond to actual metabolites if the network model is incomplete or if the biological system contains metabolites absent from the model.
- Compound identifiers must align across the metabolic model, chemical database, and any external annotation; translation or curation is needed if identifiers diverge, adding a potential source of error.
- Retention time information, if available, is not used in the mass-matching step itself; isomeric compounds with identical m/z values cannot be distinguished by this step alone.

## Evidence

- [other] Map feature m/z values to network nodes via mass-matching without performing explicit metabolite identification.: "Map feature m/z values to network nodes via mass-matching without performing explicit metabolite identification."
- [readme] We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format.: "We need chemical formulas of the compounds, which may not be available in a GSMM. If compound formulas are provided in a model, be sure to have correct neutral mass and not a salt format."
- [readme] Some indexing and calculation on chemical formulas are involved in testing the match to metabolomic data patterns.: "Some indexing and calculation on chemical formulas are involved in testing the match to metabolomic data patterns."
- [readme] If formulas are not provided in a model, we need to look them up via compound identifiers.: "If formulas are not provided in a model, we need to look them up via compound identifiers."
- [intro] It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification.: "It leverages the organization of metabolic networks to predict functional activity directly from feature tables, bypassing metabolite identification."
