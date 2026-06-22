---
name: smarts-pattern-matching-for-chemical-transformation
description: Use when when you have seed metabolite structures (SMILES or MOL format) from metabolomics data and a curated biotransformation rule database (each rule specifying reactant SMARTS, product SMARTS, and transformation type), and you need to systematically enumerate plausible biotransformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0370
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - PROXIMAL2
  - GNN-SOM
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- No usage/docs found.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam_cq
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam_cq
schema_version: 0.2.0
---

# SMARTS pattern matching for chemical transformation

## Summary

Apply SMARTS-based substructure matching to identify which biotransformation rules are applicable to a seed metabolite, then execute matched transformations to generate candidate molecular products. This is the core operation that links reaction knowledge bases (KEGG, RetroRules) to untargeted metabolomics data.

## When to use

When you have seed metabolite structures (SMILES or MOL format) from metabolomics data and a curated biotransformation rule database (each rule specifying reactant SMARTS, product SMARTS, and transformation type), and you need to systematically enumerate plausible biotransformation products to expand the chemical search space for annotation.

## When NOT to use

- Input metabolite structures are already validated products (e.g., from targeted MS/MS libraries); use this skill only to expand candidates from unknowns.
- Biotransformation rules are not available or poorly curated; rule quality directly affects product validity.
- Chemical space is already sufficiently constrained by prior annotation (e.g., a complete MS/MS spectral library is available); this skill is most valuable when annotation is incomplete.

## Inputs

- seed metabolite structures (SMILES or MOL format)
- biotransformation rule repository (CSV with columns: id, reactant SMARTS, product SMARTS, transformation type, EC number)
- reaction dataset (KEGG or RetroRules format with metabolites_list and reaction_list CSV files)

## Outputs

- candidate molecule set (deduplicated by canonical SMILES)
- parent–product links (mapping seed to generated products)
- applied rule metadata (rule ID, transformation type, EC annotation for each product)

## How to apply

Load seed metabolite structures into RDKit as molecular graph objects and parse the biotransformation rule repository. For each seed metabolite, iterate over all biotransformation rules and perform SMARTS substructure matching to identify applicable transformations. Execute each matched rule by applying the reactant-to-product transformation pattern, canonicalize the resulting SMILES strings, and validate the products (checking valence, aromaticity, and chemical feasibility). Aggregate all valid products into a candidate set, deduplicate by canonical SMILES, and retain parent–product links and rule metadata for downstream ranking and validation.

## Related tools

- **RDKit** (Molecular graph parsing, SMARTS substructure matching, SMILES canonicalization, and valence/aromaticity validation)
- **PROXIMAL2** (Upstream tool for operator generation from reaction datasets) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Downstream graph neural network tool for site-of-metabolism prediction and product ranking) — https://github.com/HassounLab/GNN-SOM

## Evaluation signals

- All returned products have valid canonical SMILES with correct valence and aromaticity (no failed RDKit parse or sanitization errors).
- Parent–product links are traceable: every product can be mapped back to its seed metabolite and the applied rule ID.
- Deduplication is complete: no two products in the candidate set share the same canonical SMILES.
- Rule coverage: compare the number of matched rules per seed metabolite against the total rule repository size; document which seeds have zero matches (potential false negatives).
- Cross-database consistency: when the same biotransformation rule exists in both KEGG and RetroRules, products generated from the same seed should be identical or minimal-diff (e.g., differing only in metadata).

## Limitations

- SMARTS matching sensitivity is rule-dependent; overly specific SMARTS patterns may miss valid transformations, while overly general patterns may over-generate spurious products.
- The skill depends on curated biotransformation rules; KEGG and RetroRules contain incomplete or inconsistent EC annotations, which may propagate into product metadata.
- Chemical validity checks (valence, aromaticity) use RDKit's rules and may not capture all biochemically implausible structures; final validation requires MS/MS confirmation or biological context.
- The method does not rank or prioritize products; all matched products are returned with equal weight. Downstream ranking (e.g., via GNN-SOM or spectral similarity) is required for annotation.

## Evidence

- [other] For each seed metabolite, iterate over all biotransformation rules and apply rule matching (SMARTS substructure search) to identify applicable transformations.: "For each seed metabolite, iterate over all biotransformation rules and apply rule matching (SMARTS substructure search) to identify applicable transformations."
- [other] For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity).: "For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity)."
- [other] Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit.: "Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit."
- [other] Load biotransformation rules from the BAM repository or curated database (each rule specifies a chemical transformation pattern: reactant SMARTS, product SMARTS, and transformation type).: "Load biotransformation rules from the BAM repository or curated database (each rule specifies a chemical transformation pattern: reactant SMARTS, product SMARTS, and transformation type)."
- [other] Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata.: "Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata."
- [readme] The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples.: "The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples."
