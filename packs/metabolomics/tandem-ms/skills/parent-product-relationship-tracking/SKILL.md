---
name: parent-product-relationship-tracking
description: Use when when you have applied biotransformation rules to generate candidate product structures from a set of input molecules (represented as SMILES strings) and need to document which product structures were derived from which parent structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3375
  tools:
  - RDKit
  - HassounLab/BAM
  - HassounLab/GNN-SOM
  - KEGG or RetroRules
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- standard library for parsing and manipulating SMILES and chemical structures
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# parent-product-relationship-tracking

## Summary

Maintain and serialize parent–product relationships when applying biotransformation rules to input molecular structures, enabling traceability of how candidate molecules are derived from anchor compounds. This is essential for validating structure predictions and reconstructing the chemical transformation pathway in untargeted metabolomics annotation.

## When to use

When you have applied biotransformation rules to generate candidate product structures from a set of input molecules (represented as SMILES strings) and need to document which product structures were derived from which parent structures. Critical in metabolomics workflows where you must rank or evaluate candidates by their transformation distance from the anchor compound, or when you need to report the applied rule for each transformation.

## When NOT to use

- Input molecules are already annotated with known identities and you only need to confirm their structures, not discover new candidates.
- Biotransformation rules are not available or not applicable to your molecule class (e.g., inorganic compounds, non-metabolic transformations).
- You are filtering an existing suspect library rather than generating de novo candidates from input anchors.

## Inputs

- SMILES strings for input molecules (parsed and validated by RDKit)
- Biotransformation rules encoded in BAM codebase or loaded from reaction datasets (e.g., KEGG, RetroRules)
- Parent–product pairs from rule application engine

## Outputs

- Structured output file (JSON or CSV) with columns: original SMILES, applied rule identifier, product SMILES, transformation metadata
- Deduplicated set of candidate product structures with parent–product relationship graph

## How to apply

After applying each biotransformation rule to every input structure using RDKit and the BAM rule engine, collect the transformed structures and maintain an explicit mapping of parent SMILES → applied rule identifier → product SMILES. Deduplicate product structures while preserving all parent–product edges; if multiple rules or parents generate the same product, record each path. Serialize the complete parent–product graph (with rule metadata) to a structured output file (JSON or CSV), ensuring each record contains original SMILES, applied rule identifier, product SMILES, and transformation metadata. This traceability allows downstream ranking algorithms (e.g., GNN-SOM site-of-metabolism prediction) to score candidates by transformation specificity and chemical plausibility.

## Related tools

- **RDKit** (Parse, validate, and manipulate SMILES strings; execute biotransformation rule application on molecular structures)
- **HassounLab/BAM** (Implement biotransformation rule engine and orchestrate parent–product relationship tracking within the annotation method) — https://github.com/HassounLab/BAM
- **HassounLab/GNN-SOM** (Predict site-of-metabolism and rank candidate products by their parent–product relationships and transformation plausibility) — https://github.com/HassounLab/GNN-SOM
- **KEGG or RetroRules** (Provide the biotransformation rules (reaction definitions) applied to generate products from parent structures)

## Examples

```
sh runBAM.sh
```

## Evaluation signals

- Every product SMILES can be traced back to at least one parent SMILES and one applied rule identifier; no orphaned products.
- Deduplicated product set contains no duplicate SMILES entries, but the parent–product mapping records multiple derivation paths when applicable.
- Output file schema conforms to specified columns (original SMILES, rule ID, product SMILES, metadata); all rows are valid and parseable.
- Product SMILES are chemically valid and consistent with the biotransformation rule definitions (spot-check by comparing rule mechanism to product structure).
- Parent–product graph has no cycles (transformations are acyclic, flowing from input anchors outward to products).

## Limitations

- Biotransformation rule coverage is limited to the reaction dataset specified (KEGG, RetroRules, or custom); rules absent from the dataset will not generate corresponding products, potentially missing true metabolites.
- SMILES parsing and validation depend on RDKit's chemical inference; invalid or ambiguous SMILES may be silently dropped or misinterpreted, introducing false negatives.
- Parent–product relationships do not themselves rank or prioritize candidates; ranking requires downstream integration with site-of-metabolism prediction (e.g., GNN-SOM) or spectral matching.
- Deduplication of product SMILES is exact-match only; tautomers, stereoisomers, or alternative SMILES representations of the same molecule are treated as distinct, potentially inflating the candidate pool.

## Evidence

- [other] Collect and deduplicate the transformed structures, maintaining parent–product relationships.: "Collect and deduplicate the transformed structures, maintaining parent–product relationships."
- [other] Serialize the results as a structured output file (JSON or CSV) containing original SMILES, applied rule identifier, product SMILES, and transformation metadata.: "Serialize the results as a structured output file (JSON or CSV) containing original SMILES, applied rule identifier, product SMILES, and transformation metadata."
- [other] BAM is implemented as a method that uses biotransformation rules and global molecular networking for molecular structure discovery from untargeted metabolomics data.: "BAM is implemented as a method that uses biotransformation rules and global molecular networking for molecular structure discovery from untargeted metabolomics data."
- [readme] To change to using RetroRules reaction data, simply comment the "KEGG biotransformations" block and uncomment the "RetroRules biotransformations" box, and then run the runBAM.sh file.: "To change to using RetroRules reaction data, simply comment the "KEGG biotransformations" block and uncomment the "RetroRules biotransformations" box, and then run the runBAM.sh file."
