---
name: biotransformation-rule-application-to-metabolites
description: Use when you have untargeted metabolomics data with unknown or ambiguous molecular identities, anchor metabolites (known structures in SMILES or MOL format), and a curated database of biotransformation rules (e.g., from KEGG, RetroRules, or domain-specific repositories).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3658
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - PROXIMAL2
  - GNN-SOM
  techniques:
  - LC-MS
  - NMR
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

# biotransformation-rule-application-to-metabolites

## Summary

Apply biotransformation rules (encoded as SMARTS reactant/product patterns) to seed metabolite structures to generate candidate transformation products with parent–product traceability. This skill enables annotation of unknown metabolites in untargeted metabolomics by systematically exploring chemically plausible transformations from known metabolite seeds.

## When to use

You have untargeted metabolomics data with unknown or ambiguous molecular identities, anchor metabolites (known structures in SMILES or MOL format), and a curated database of biotransformation rules (e.g., from KEGG, RetroRules, or domain-specific repositories). Apply this skill when you need to predict plausible metabolite candidates that could arise from enzymatic or chemical transformations of the anchor seed compounds, and you want to rank or validate those candidates against observed mass or spectroscopic features.

## When NOT to use

- Input metabolites are already fully characterized and validated by orthogonal methods (e.g., NMR, MS/MS)—the skill generates candidates and requires downstream validation.
- Biotransformation rules are unavailable or not relevant to your biological or chemical system (e.g., studying abiotic environmental transformations with no enzymatic data).
- Seed metabolite structures are not available or are ambiguous (e.g., only mass or formula known, no SMILES or MOL structure).

## Inputs

- Seed metabolite structures (SMILES or MOL format)
- Biotransformation rules database (CSV with columns: id, EC, formula; each rule specifies reactant SMARTS, product SMARTS, transformation type)
- Reaction dataset (e.g., KEGG, RetroRules)

## Outputs

- Candidate product molecules (canonicalized SMILES)
- Parent–product relationship links and applied rule metadata
- Deduplicated candidate molecule set with validity annotations

## How to apply

Load seed metabolite structures and parse them into molecular graph objects using RDKit. Load biotransformation rules from a curated source (each rule specifies reactant SMARTS pattern, product SMARTS pattern, and transformation type). For each seed metabolite, iterate over all biotransformation rules and perform SMARTS substructure matching to identify applicable transformations. For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES representations, and validate chemical correctness (e.g., valence, aromaticity). Aggregate all products into a candidate set, remove duplicates by canonical SMILES, and retain parent–product links and applied rule metadata for traceability and ranking.

## Related tools

- **RDKit** (Parse seed metabolite structures into molecular graph objects; apply SMARTS substructure matching; execute biotransformation rules; canonicalize SMILES; validate chemical correctness)
- **PROXIMAL2** (Upstream tool for generating biotransformation operators from reaction datasets) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Downstream tool for site-of-metabolism prediction and ranking of enzymatic products) — https://github.com/HassounLab/GNN-SOM

## Examples

```
sh runBAM.sh
```

## Evaluation signals

- All output product SMILES are valid (valence and aromaticity checks pass); no chemically invalid molecules in candidate set.
- Parent–product links are traceable: each candidate is associated with the seed metabolite and the specific biotransformation rule that generated it.
- Duplicate products (identical canonical SMILES) have been removed; candidate set size is deterministic and reproducible.
- Product candidates rank or cluster correctly when compared to downstream validation (e.g., observed m/z in metabolomics data, known metabolite standards, or MS/MS fragmentation patterns).
- Rule coverage: biotransformation rules are exhaustively tested against all seed metabolites; no applicable rules are skipped (i.e., all SMARTS matches are captured).

## Limitations

- Biotransformation rule applicability depends on rule database quality and completeness; rules derived from KEGG or RetroRules may not cover organism-specific or rare enzymatic reactions.
- SMARTS substructure matching is deterministic but does not account for stereochemistry or regiochemical selectivity; multiple regioisomers may be generated when the rule does not specify selective atom mapping.
- No built-in scoring or ranking of products by biological plausibility; downstream tools (e.g., GNN-SOM) or experimental validation are required to discriminate among candidates.
- Computational cost scales with the number of seed metabolites and rule database size; large datasets or highly permissive rule sets may generate enormous candidate pools requiring post-hoc filtering.

## Evidence

- [other] For each seed metabolite, iterate over all biotransformation rules and apply rule matching (SMARTS substructure search) to identify applicable transformations.: "For each seed metabolite, iterate over all biotransformation rules and apply rule matching (SMARTS substructure search) to identify applicable transformations."
- [other] For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity).: "For each matched rule, execute the transformation to generate product molecule(s), canonicalize SMILES, and check for validity (e.g., valence, aromaticity)."
- [other] Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata.: "Aggregate all products into a candidate molecule set, remove duplicates (by canonical SMILES), and store with parent–product links and applied rule metadata."
- [intro] BAM implements a biotransformation-based annotation method that applies biotransformation rules to generate molecular candidates from metabolomics data.: "BAM implements a biotransformation-based annotation method that applies biotransformation rules to generate molecular candidates from metabolomics data."
- [readme] The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples.: "The desired reaction dataset of interest needs to be specified. We have used KEGG and RetroRules as examples."
- [other] Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit.: "Load seed metabolite structures (SMILES or MOL format) and parse into molecular graph objects using RDKit."
