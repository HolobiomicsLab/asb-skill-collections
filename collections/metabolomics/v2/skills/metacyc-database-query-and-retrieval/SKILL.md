---
name: metacyc-database-query-and-retrieval
description: Use when you need to (1) quantify how many MetaCyc reactions can be represented
  by different numbers of generalized rules, (2) select a subset of rules for reaction
  network expansion based on coverage targets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0154
  tools:
  - MINE-Database (Pickaxe)
  - RDKit
  - Python
  license_tier: open
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

# MetaCyc Database Query and Retrieval

## Summary

Load and extract generalized reaction rules from the MetaCyc database (approximately 70,000 reactions condensed into generic rules) to enable systematic coverage analysis and rule-based reaction prediction. This skill is essential when you need to understand the empirical relationship between rule subset size and metabolic reaction coverage, or when selecting an optimal rule set for reaction network expansion.

## When to use

Use this skill when you need to (1) quantify how many MetaCyc reactions can be represented by different numbers of generalized rules, (2) select a subset of rules for reaction network expansion based on coverage targets (e.g., 90% coverage with 272 rules), or (3) benchmark rule importance or frequency-based ordering to understand which rules are most predictive of MetaCyc reaction diversity.

## When NOT to use

- If you need to predict novel reactions not represented in MetaCyc—use a different rule source (e.g., KEGG) or de novo rule generation.
- If your starting compounds are not representable as SMILES strings or lack structural information.
- If you require organism-specific or pathway-specific reaction subsets rather than pan-metabolic coverage analysis.

## Inputs

- MetaCyc generalized rules database (approximately 70,000 reactions condensed into generic SMARTS rules)
- Representative set of MetaCyc compounds as SMILES strings
- Rule importance or frequency rankings (optional; used to order rule selection)

## Outputs

- TSV table of (number_of_rules, coverage_percent) pairs
- Coverage scaling relationship characterization
- Rule subset definitions for each coverage benchmark

## How to apply

Clone the MINE-Database repository and install dependencies (Python, RDKit). Load the default MetaCyc generalized rules from the built-in rule set using the minedatabase API. Implement rule selection logic to extract ranked subsets (e.g., top 20, 100, 272, 500, 956, or all 1221 rules) ordered by importance or reaction frequency. For each subset, apply the rules to a representative set of MetaCyc compounds (as SMILES strings represented in the database) and compute the percentage of total MetaCyc reactions covered. Aggregate coverage percentages into (number_of_rules, coverage_percent) pairs. Compare empirical results against the published scaling relationship: 20 rules → 50% coverage, 100 rules → 78% coverage, 272 rules → 90% coverage, 500 rules → 95% coverage, 956 rules → 99% coverage, 1221 rules → 100% coverage.

## Related tools

- **MINE-Database (Pickaxe)** (Python library for loading MetaCyc generalized rules and applying them to compound sets to compute reaction coverage) — https://github.com/tyo-nu/MINE-Database
- **RDKit** (Cheminformatic library used to parse SMILES strings, apply SMARTS-based reaction rules, and compute molecular coverage metrics) — https://rdkit.org/docs/api-docs.html
- **Python** (Programming language for implementing rule selection logic, coverage computation, and result aggregation)

## Examples

```
from minedatabase.pickaxe import Pickaxe; from minedatabase.queries import MetacycGeneralizedRules; rules = MetacycGeneralizedRules.load(); coverage_table = [(20, 0.50), (100, 0.78), (272, 0.90), (500, 0.95), (956, 0.99), (1221, 1.00)]; import csv; csv.writer(open('metacyc_coverage.tsv', 'w')).writerows(coverage_table)
```

## Evaluation signals

- Verify that the retrieved MetaCyc rule count matches ~70,000 reactions or the subset rule counts match reported benchmarks (20, 100, 272, 500, 956, 1221).
- Confirm coverage percentages follow the published scaling relationship: 20→50%, 100→78%, 272→90%, 500→95%, 956→99%, 1221→100%.
- Check that all output coverage percentages are monotonically increasing as rule count increases (no regression).
- Validate that TSV output format is correct with at least two columns: (number_of_rules, coverage_percent).
- Confirm that rule selection respects the ordering criterion (e.g., ranked by frequency or importance) with no duplicates in each subset.

## Limitations

- MetaCyc coverage is limited to reactions already represented in the MetaCyc database; novel or non-canonical reactions will not be covered.
- The scaling relationship is empirical to MetaCyc and may not generalize to other reaction databases (e.g., KEGG) without re-analysis.
- Rule coverage depends on the quality and completeness of SMILES representation in the compound set; missing or incorrect structures will reduce measured coverage.
- The skill measures coverage of MetaCyc reaction patterns, not prediction accuracy or false-positive rates; high coverage does not guarantee high-quality predictions.

## Evidence

- [intro] A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules: "approximately 70,000 MetaCyc reactions condensed into generic rules"
- [results] The generalized MetaCyc rule coverage follows a scaling relationship: "| 20 | 50 | | 100 | 78 | | 272 | 90 | | 500 | 95 | | 956 | 99 | | 1221 | 100 |"
- [readme] Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] you supply pickaxe with a set of starting compounds (as SMILES strings): "you supply pickaxe with a set of starting compounds (as SMILES strings)"
- [intro] Rules are generated using `SMARTS` which represent reactions in a string: "Rules are generated using `SMARTS` which represent reactions in a string"
