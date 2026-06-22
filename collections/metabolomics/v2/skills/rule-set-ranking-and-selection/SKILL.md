---
name: rule-set-ranking-and-selection
description: Use when when you have a large set of generalized reaction rules (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0176
  tools:
  - RDKit
  - Python
  - MINE-Database / Pickaxe
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
---

# Rule-set ranking and selection

## Summary

Rank and select subsets of reaction transformation rules by importance or frequency to achieve target coverage of a reaction database while minimizing the number of rules needed. This skill trades off rule set size against coverage percentage to enable efficient reaction network expansion with reduced computational burden.

## When to use

When you have a large set of generalized reaction rules (e.g., ~1,221 MetaCyc rules) and need to balance computational efficiency against reaction coverage—for instance, when expanding 10,000 compounds with limited resources where selecting 272 rules yields 90% coverage but all 1,221 rules provide 100% coverage.

## When NOT to use

- Rule set is already small (<50 rules) or coverage is not a practical constraint.
- All rules are equally rare or specialized; ranking by frequency will not improve efficiency.
- Target database is poorly characterized or unavailable; coverage cannot be measured empirically.

## Inputs

- Generalized reaction rule set (SMARTS format, ~1,221 rules from MetaCyc or equivalent)
- Representative compound set (SMILES strings)
- Target reaction database for coverage evaluation (e.g., full MetaCyc reaction list)

## Outputs

- Ranked rule subset cardinalities with corresponding coverage percentages (TSV table: number_of_rules | coverage_percent)
- Rule importance or frequency scores used for ranking
- Selected rule subset(s) in SMARTS format for downstream network expansion

## How to apply

Load the full generalized rule set from a built-in repository (e.g., metacyc_generalized ruleset containing ~70,000 MetaCyc reactions condensed into generic rules). Rank rules by frequency of occurrence or estimated importance across known reactions. Extract rule subsets at predetermined cardinalities (e.g., 20, 100, 272, 500, 956, 1221 rules). For each subset, apply the rules to a representative compound set and measure the percentage of total reactions in the target database that can be represented. Tabulate (number_of_rules, coverage_percent) pairs to identify the optimal trade-off point for your analysis goals. The resulting coverage table follows a scaling relationship: 20 rules ≈ 50%, 100 rules ≈ 78%, 272 rules ≈ 90%, 500 rules ≈ 95%, 956 rules ≈ 99%, and all 1,221 rules ≈ 100%.

## Related tools

- **RDKit** (Parse and apply SMARTS reaction rules to compounds; compute molecular fingerprints for similarity metrics) — https://rdkit.org/
- **Python** (Implement rule ranking logic, subset extraction, and coverage computation workflows)
- **MINE-Database / Pickaxe** (Load built-in MetaCyc generalized rules and apply subsets iteratively to compound sets) — https://github.com/tyo-nu/MINE-Database

## Examples

```
# Load MINE-Database, extract ranked MetaCyc rules, and compute coverage for cardinality 272
from minedatabase.pickaxe import Pickaxe
rules = Pickaxe.load_rules('./data/metacyc_generalized_rules.tsv')
selected_rules = rules[:272]  # Top 272 by frequency
coverage = Pickaxe.compute_coverage(selected_rules, target_db='metacyc_reactions')
print(f'272 rules cover {coverage}% of MetaCyc')
```

## Evaluation signals

- Coverage percentages for each rule cardinality match published reference values (e.g., 272 rules → 90%, 500 rules → 95%).
- Coverage increases monotonically as rule set size increases; no cardinality should show lower coverage than a smaller preceding set.
- TSV output file contains all expected (number_of_rules, coverage_percent) pairs with no missing or malformed rows.
- Rule subset sizes correspond to ranked cardinalities (e.g., top 20 rules differ from top 100 only by the addition of 80 new rules in rank order).
- Compounds in output are subset of input; no novel compounds are generated during coverage evaluation (reaction network not expanded, only applicability tested).

## Limitations

- Coverage follows an empirical scaling relationship that is specific to MetaCyc; scaling may differ for other reaction databases or specialized rule sets.
- Rule ranking by frequency assumes that common reaction patterns are more useful than rare ones; domain-specific applications may benefit from alternative ranking criteria (e.g., thermodynamic feasibility, organism specificity).
- Coverage measurement requires a well-defined target database; incomplete or noisy reference databases will bias coverage estimates.
- Computational cost of coverage evaluation grows linearly with rule set size and representative compound count; very large databases may require sampling or approximation.

## Evidence

- [intro] 20 rules provide 50% coverage, 100 rules provide 78% coverage, 272 rules provide 90% coverage, 500 rules provide 95% coverage, 956 rules provide 99% coverage, and all 1221 rules provide 100% coverage of MetaCyc reactions: "The generalized MetaCyc rule coverage follows a scaling relationship: 20 rules provide 50% coverage, 100 rules provide 78% coverage, 272 rules provide 90% coverage, 500 rules provide 95% coverage,"
- [intro] Implement rule selection logic to extract subsets of 20, 84, 100, 272, 500, 956, and 1221 rules from the metacyc_generalized ruleset using ranked rule importance or frequency-based ordering: "Implement rule selection logic to extract subsets of 20, 84, 100, 272, 500, 956, and 1221 rules from the metacyc_generalized ruleset using ranked rule importance or frequency-based ordering."
- [intro] approximately 70,000 MetaCyc reactions condensed into generic rules: "A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules"
- [intro] For each rule subset, apply the rules to a representative set of MetaCyc compounds and compute the percentage of total MetaCyc reactions covered by the selected rules: "For each rule subset, apply the rules to a representative set of MetaCyc compounds and compute the percentage of total MetaCyc reactions covered by the selected rules."
- [intro] expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
