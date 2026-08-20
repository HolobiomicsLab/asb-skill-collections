---
name: smarts-reaction-rule-encoding
description: Use when when you have a set of known chemical reactions (e.g., from
  MetaCyc or KEGG) that you want to generalize into reusable transformation rules
  for predicting novel reactions on new compound sets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  tools:
  - MongoDB
  - RDKit
  - Pickaxe
  - Python
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- The URI of the mongo database to connect to. Defaults to mongodb://localhost:27017
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-023-05149-8
  all_source_dois:
  - 10.1186/s12859-023-05149-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMARTS Reaction Rule Encoding

## Summary

Encode chemical reaction transformation patterns as SMARTS strings for use in iterative network expansion workflows. SMARTS rules capture generalized reaction templates that can be applied programmatically to predict reactions across compound libraries.

## When to use

When you have a set of known chemical reactions (e.g., from MetaCyc or KEGG) that you want to generalize into reusable transformation rules for predicting novel reactions on new compound sets. Use this skill if you need to convert reaction patterns into a machine-readable format suitable for RDKit-based cheminformatic tools.

## When NOT to use

- Input reactions are already encoded as SMARTS and only need to be loaded—skip to rule application.
- You need arbitrary reaction prediction without reference to a known reaction database—SMARTS rules require grounding in observed chemistry.
- Reaction data is in non-standard formats (e.g., reaction arrow notation without atom mappings) and cannot be reliably parsed into SMARTS.

## Inputs

- Reaction dataset (e.g., MetaCyc, KEGG reactions with SMILES or structure format)
- Reference reactants and products (SMILES strings or chemical structure notation)
- Reaction mechanism or transformation description

## Outputs

- SMARTS-encoded rule TSV file (columns: rule_id, SMARTS_string, optionally metadata)
- Validated rule set suitable for RDKit pattern matching
- Coverage metrics (percentage of reference reactions matched by rule set)

## How to apply

Analyze the reactants and products of reference reactions to identify conserved transformation patterns—atom mappings, bond changes, and functional group modifications. Encode these patterns as SMARTS strings, which represent the reaction in a format RDKit can parse and match. Organize encoded rules into a TSV file with rule identifiers and SMARTS strings. Test rule specificity and coverage by applying them to reference compounds; coverage benchmarks (e.g., 272 rules → 90% MetaCyc coverage) help calibrate rule set size. Load the SMARTS rules into Pickaxe alongside coreactant specifications for iterative application across generations.

## Related tools

- **RDKit** (Parses SMARTS strings and performs chemical pattern matching and reaction transformation computation) — https://rdkit.org
- **Pickaxe** (Loads and iteratively applies SMARTS-encoded rules to compound sets for network expansion) — https://github.com/tyo-nu/MINE-Database
- **Python** (Implementation language for rule encoding, curation, and testing workflows)

## Examples

```
# Load SMARTS rules from TSV and initialize Pickaxe with 272 rules (90% MetaCyc coverage)
pickaxe = Pickaxe(starting_compounds='iML1515_ecoli_GEM.csv', rules='metacyc_generalized_rules.tsv', coreactants='metacyc_coreactants.tsv', generations=1)
```

## Evaluation signals

- SMARTS strings are syntactically valid and parseable by RDKit without errors
- Rule set coverage matches or exceeds expected threshold (e.g., 272 rules achieve ≥90% coverage of MetaCyc reference reactions)
- When applied to test compound sets, encoded rules reproduce known reactions or generate chemically plausible products
- Rule-generated compounds can be validated against external databases (MetaCyc, KEGG) or experimental metabolomics peaks
- No duplicate or contradictory rules in the final TSV file; each rule ID is unique and deterministic

## Limitations

- SMARTS rule quality depends on quality of reference reaction data; errors or ambiguities in reactant/product annotation propagate into rules.
- Rule coverage plateaus: 100% coverage of MetaCyc requires all 1221 rules; smaller rule sets (e.g., 20 rules) achieve only ~50% coverage, forcing trade-offs between specificity and breadth.
- Reaction selectivity and regiochemistry cannot always be captured in SMARTS rules; rules may predict multiple products or fail to distinguish regioisomers.
- SMARTS encoding requires domain expertise in cheminformatics notation; subtle errors in atom mapping or bond specification can produce non-functional rules.

## Evidence

- [intro] Rules are generated using `SMARTS` which represent reactions in a string: "Rules are generated using `SMARTS` which represent reactions in a string"
- [intro] Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules: "A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules"
- [intro] Selecting 20 rules provides 50% coverage of MetaCyc reactions; 100 rules provide 78% coverage; 272 rules provide 90% coverage; 500 rules provide 95% coverage; 956 rules provide 99% coverage; 1221 rules provide 100% coverage: "Selecting 20 rules provides 50% coverage of MetaCyc reactions; 100 rules provide 78% coverage; 272 rules provide 90% coverage; 500 rules provide 95% coverage; 956 rules provide 99% coverage; 1221"
- [intro] which set of reaction rules you would like to use: "which set of reaction rules you would like to use"
- [other] Load coreactant list and reaction rules (SMARTS-encoded) from TSV files: "Load coreactant list and reaction rules (SMARTS-encoded) from TSV files"
