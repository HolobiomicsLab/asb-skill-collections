---
name: structure-matching-via-smarts-patterns
description: Use when when you need to identify compounds matching specific structural motifs or apply reaction transformation rules to a set of molecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - RDKit
  - Pickaxe (MINE-Database)
  - Python
  - MongoDB or TSV output
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans: []
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

# structure-matching-via-smarts-patterns

## Summary

Use SMARTS (Simplified Molecular Input Line Entry System) strings to encode and match chemical reaction transformation patterns against compound structures within reaction networks. This skill enables systematic structure-based filtering and rule application in generative cheminformatics workflows.

## When to use

When you need to identify compounds matching specific structural motifs or apply reaction transformation rules to a set of molecules. Use this skill when working with MetaCyc or KEGG reaction databases and want to select only compounds that undergo particular transformations, or when building predictive reaction networks where rule specificity matters.

## When NOT to use

- Input compounds are already curated to a specific structural family; rule matching may over-filter or miss relevant structures.
- You need graph isomorphism matching beyond SMARTS substructure matching (SMARTS is greedy and pattern-order-dependent).
- The rule set is not semantically aligned with your domain (e.g., applying MetaCyc rules to non-biological synthetic chemistry may give spurious matches).

## Inputs

- SMARTS pattern strings encoding chemical structures or reaction transformations
- Compound set as SMILES strings (e.g., from KEGG or MetaCyc)
- Reaction rule file in TSV format (rules and cofactors from metacyc_generalized ruleset)
- Optional: ranked rule subset specification (number of top rules to apply)

## Outputs

- Set of compounds matching the SMARTS pattern (subset of input compounds)
- Predicted reaction products after rule application
- Coverage metrics (percentage of total reactions represented by selected rule subsets)
- TSV file with matched compounds and their generated descendants

## How to apply

Encode the desired structural or reaction pattern as a SMARTS string, which represents the transformation in a compact notation understood by RDKit. Load the SMARTS-encoded rules (e.g., from the built-in metacyc_generalized ruleset containing ~70,000 MetaCyc reactions condensed into generic rules) and apply them iteratively to your input compound set using RDKit's matching algorithm. The matching determines which compounds undergo each transformation. For coverage optimization, rank rules by importance or frequency and apply successive subsets (e.g., 20 rules for 50% coverage, 272 rules for 90% coverage) to balance specificity and computational cost. Inspect the matched compound outputs and verify that the expected structural transformations occurred.

## Related tools

- **RDKit** (Provides cheminformatic API for SMARTS pattern matching and molecular structure manipulation; applies generalized reaction rules to compounds.) — https://rdkit.org/docs/api-docs.html
- **Pickaxe (MINE-Database)** (Orchestrates iterative application of SMARTS-encoded reaction rules to compound sets across multiple generations; handles rule selection and network expansion.) — https://github.com/tyo-nu/MINE-Database
- **Python** (Programming environment for scripting rule loading, SMARTS pattern manipulation, and result aggregation.)
- **MongoDB or TSV output** (Storage and retrieval of matched compounds and coverage results.)

## Examples

```
from minedatabase.pickaxe import Pickaxe; pk = Pickaxe(compound_list=['CC(C)O'], rules='./data/metacyc_generalized_rules.tsv', generations=2); pk.run_pickaxe()
```

## Evaluation signals

- Matched compound set contains only molecules whose structures satisfy the SMARTS substructure criteria (validate by visual inspection or re-matching).
- Coverage metrics match reported scaling relationship: 20 rules → 50% coverage, 100 rules → 78%, 272 rules → 90%, 500 rules → 95%, 956 rules → 99%, 1221 rules → 100% of MetaCyc reactions.
- Number of generated compounds and reactions after rule application scales predictably with input compound size and rule subset (e.g., 10,000 KEGG compounds + 272 rules → ~5 million compounds).
- Output TSV/database entries contain non-empty SMILES strings and reaction product identifiers for all matched compounds.
- Rule subset selection (e.g., top-272 rules) reproducibly achieves stated coverage when applied to a held-out MetaCyc compound set.

## Limitations

- SMARTS pattern matching is order-dependent and greedy; equivalent molecules represented differently in SMILES may match inconsistently.
- MetaCyc generalized rules provide biological reaction coverage but may not capture synthetic or non-standard chemistry.
- Coverage scaling is empirical and specific to MetaCyc; scaling relationships do not necessarily transfer to other reaction databases.
- No changelog is maintained; version-to-version changes in rule sets or RDKit behavior are not explicitly documented, risking reproducibility issues.

## Evidence

- [intro] Rules are generated using `SMARTS` which represent reactions in a string: "Rules are generated using `SMARTS` which represent reactions in a string"
- [intro] approximately 70,000 MetaCyc reactions condensed into generic rules: "A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules"
- [intro] Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] 100 rules provide 78% coverage; 272 rules provide 90% coverage; 500 rules provide 95% coverage; 956 rules provide 99% coverage; 1221 rules provide 100% coverage: "| 20 | 50 | | 100 | 78 | | 272 | 90 | | 500 | 95 | | 956 | 99 | | 1221 | 100 |"
- [other] Default filters are created using RDKit, a python library providing a collection of cheminformatic tools: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools."
- [intro] expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
