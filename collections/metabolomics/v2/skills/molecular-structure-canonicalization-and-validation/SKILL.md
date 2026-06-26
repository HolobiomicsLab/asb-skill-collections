---
name: molecular-structure-canonicalization-and-validation
description: Use when immediately after generating candidate transformation products
  from biotransformation rules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3961
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - PROXIMAL2
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-structure-canonicalization-and-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Canonicalize SMILES strings and validate molecular structures for chemical correctness after transformation or generation. This ensures that duplicate candidates are detected, invalid molecules are filtered, and structures are represented in a standardized form suitable for downstream comparison and storage.

## When to use

Apply this skill immediately after generating candidate transformation products from biotransformation rules. Use it when you have a collection of molecular structures (in SMILES or MOL format) that need to be de-duplicated, checked for chemical validity (valence, aromaticity), and standardized for downstream storage or comparison in a metabolomics annotation workflow.

## When NOT to use

- Input metabolites are already manually curated and de-duplicated by a third party; re-validation may introduce false rejections.
- Only structural diversity (not chemical validity) matters for your downstream analysis; canonicalization overhead may not be justified.
- You are working with pre-validated, canonicalized reference databases (e.g., KEGG or PubChem) where duplicate checking has already been performed.

## Inputs

- SMILES strings (product molecules from biotransformation rule application)
- MOL format molecular structures
- Molecular objects parsed by RDKit

## Outputs

- Canonical SMILES strings (deduplicated)
- Validated molecule objects (passing valence and aromaticity checks)
- Candidate molecule set with parent–product links
- Rule metadata associated with each transformation

## How to apply

For each generated product molecule, use RDKit to parse the molecular structure into a canonical SMILES representation. Then validate the molecule by checking for chemical correctness: verify valence rules are satisfied, confirm aromaticity perception is consistent, and ensure the molecule is chemically plausible. Aggregate all products into a candidate set and remove duplicates by comparing canonical SMILES strings. Retain only valid structures and store them alongside parent–product links and applied rule metadata. This canonicalization step is critical for detecting when different transformation pathways produce the same product, preventing redundant downstream analysis.

## Related tools

- **RDKit** (Parses molecular structures into graph objects, canonicalizes SMILES, and validates molecular properties (valence, aromaticity))
- **PROXIMAL2** (Upstream tool for generating biotransformation rules; outputs are used as input to BAM and require canonicalization/validation) — https://github.com/HassounLab/PROXIMAL2

## Examples

```
from rdkit import Chem; products_smiles = [...]; canonical_products = [Chem.MolToSmiles(Chem.MolFromSmiles(s)) for s in products_smiles if Chem.MolFromSmiles(s) is not None]; unique_products = list(set(canonical_products))
```

## Evaluation signals

- All output SMILES are in canonical form: running RDKit canonicalization a second time produces identical strings.
- No duplicate canonical SMILES exist in the deduplicated product set; set size equals count of unique products.
- All retained molecules pass RDKit validity checks: Chem.SanitizeMol() succeeds for each structure.
- Parent–product links are preserved: each canonical product is traceable to its parent metabolite and applied rule.
- Invalid or implausible structures (e.g., violated valence rules) are logged and excluded; rejection count and reason are recorded for audit.

## Limitations

- Canonicalization depends on RDKit's valence model and aromaticity perception; edge cases (exotic coordination, hypervalent sulfur) may not canonicalize as expected.
- Canonical SMILES can differ across RDKit versions or when generated by different chemistry toolkits; ensure consistent RDKit version across the pipeline.
- Invalid molecules are silently rejected; users must manually inspect rejected products if chemical plausibility is disputed.
- Duplicate detection by canonical SMILES assumes that structural isomers should be treated as equivalent; stereoisomers may not be properly distinguished if not explicitly encoded in the SMILES.

## Evidence

- [other] For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity).: "execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity)"
- [other] Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata.: "Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata"
- [other] Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit.: "Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit"
