---
name: reaction-rule-coverage-analysis
description: Use when when you need to decide how many reaction rules to include in a Pickaxe expansion run and want to quantify the coverage penalty of using a smaller subset; when benchmarking rule importance or frequency rankings;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0196
  tools:
  - MINE-Database (Pickaxe)
  - RDKit
  - Python
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

# reaction-rule-coverage-analysis

## Summary

Empirically determine the scaling relationship between the number of generalized reaction rules applied and the percentage coverage of a reference reaction database (e.g., MetaCyc). This skill quantifies the trade-off between rule set size and reaction prediction coverage, enabling practitioners to select optimal rule subsets for their computational resources.

## When to use

When you need to decide how many reaction rules to include in a Pickaxe expansion run and want to quantify the coverage penalty of using a smaller subset; when benchmarking rule importance or frequency rankings; or when optimizing rule selection for a constrained computational budget while maintaining acceptable reaction coverage.

## When NOT to use

- You are working with reaction rules that are already curated or filtered to a specific biological context (e.g., organism-specific pathways); coverage analysis assumes a large, unbiased reference rule set.
- Your goal is to validate the correctness of individual reaction predictions, not to characterize aggregate coverage; this skill measures coverage breadth, not prediction accuracy.
- You have already selected a fixed rule subset based on prior knowledge or experimental evidence; coverage analysis is a planning/benchmarking tool, not a prediction validation step.

## Inputs

- Full generalized reaction rule set (TSV format, ~1221 MetaCyc rules with SMARTS representations)
- Representative compound set (SMILES strings) from the reference database
- Reference reaction database (e.g., MetaCyc reactions in TSV or equivalent format)
- Rule ranking or frequency scores for subset selection

## Outputs

- Coverage table (TSV format): rows of (number_of_rules, coverage_percent) pairs
- Scaling curve plot (optional): visualization of coverage vs. rule cardinality
- Validation report: empirical coverage values compared to expected benchmarks

## How to apply

Load the full generalized rule set (e.g., ~1221 MetaCyc generalized rules from MINE-Database) and create ranked subsets at strategic cardinalities (e.g., 20, 100, 272, 500, 956, 1221 rules) ordered by rule importance or frequency. For each subset, apply the rules to a representative compound set from the reference database and compute the fraction of total reference reactions that can be represented by the selected rules. Aggregate coverage percentages as (number_of_rules, coverage_percent) pairs and tabulate results. Compare empirical scaling curve against reported benchmarks to validate that selecting N rules achieves the expected coverage; use these curves to identify the rule cardinality that meets your application's coverage threshold.

## Related tools

- **MINE-Database (Pickaxe)** (Applies generalized reaction rules to compounds; provides the default MetaCyc generalized rule set and framework for iterative rule application) — https://github.com/tyo-nu/MINE-Database
- **RDKit** (Parses SMILES and SMARTS representations; enables rule-based molecular transformation and similarity calculations)
- **Python** (Orchestrates rule subset selection, iterative rule application, coverage computation, and tabulation)

## Examples

```
# Load MINE-Database, select rule subsets [20, 100, 272, 500, 956, 1221], apply to MetaCyc compounds, and tabulate coverage:
from minedatabase.pickaxe import Pickaxe
rule_counts = [20, 100, 272, 500, 956, 1221]
coverage_table = []
for n_rules in rule_counts:
    rules_subset = load_rules_ranked('./data/metacyc_generalized_rules.tsv', n_top=n_rules)
    pickaxe = Pickaxe(rules=rules_subset, coreactants='./data/metacyc_coreactants.tsv')
    coverage_pct = compute_coverage(pickaxe, reference_db='MetaCyc')
    coverage_table.append((n_rules, coverage_pct))
with open('coverage_table.tsv', 'w') as f:
    f.write('num_rules\tcoverage_percent\n')
    for n, cov in coverage_table:
        f.write(f'{n}\t{cov}\n')
```

## Evaluation signals

- Tabulated coverage values match or fall within expected ranges from published benchmarks (e.g., 20 rules → ~50% coverage, 272 rules → ~90% coverage, 1221 rules → 100% coverage for MetaCyc).
- Coverage percentages form a monotonically increasing curve with respect to rule cardinality; no rule subset should produce lower coverage than a larger subset.
- Sum of reactions covered by rule subset N ≥ sum covered by subset N−1; cumulative coverage is non-decreasing.
- Rule subsets are properly ranked by importance or frequency; top-ranked rules should dominate coverage gains at small cardinalities.
- All reference reactions are reachable by the full rule set (1221 rules achieve 100% coverage); this validates reference database completeness and rule-application logic.

## Limitations

- Coverage scaling is specific to the reference reaction database (MetaCyc); coverage curves may differ for KEGG or other reaction sources.
- Rule ranking method (importance vs. frequency) affects the coverage curve; different ranking strategies will produce different cardinality-vs-coverage relationships.
- Coverage is measured on the reference database compounds only; coverage may not transfer to novel or user-supplied compound sets, which may trigger different reaction pathways.
- Computational cost scales with rule cardinality and compound set size; expansion of 10,000 KEGG compounds with 272 rules can yield 5 million compounds, limiting feasibility for large subsets.

## Evidence

- [intro] Coverage relationship: "20 rules provide 50% coverage of MetaCyc reactions; 100 rules provide 78% coverage; 272 rules provide 90% coverage; 500 rules provide 95% coverage; 956 rules provide 99% coverage; 1221 rules provide"
- [intro] Rule set source and size: "A set of biological reaction rules and cofactors are provided by default. These consist of approximately 70,000 MetaCyc reactions condensed into generic rules"
- [intro] Pickaxe application workflow: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [readme] Iterative rule application: "Pickaxe creates a network expansion by applying these reaction rules iteratively to your starting set of compounds, going for as many generations as you specify"
- [intro] SMARTS rule representation: "Rules are generated using `SMARTS` which represent reactions in a string"
- [intro] Scalability example: "For example, expanding 10,000 compounds from KEGG with 272 rules from metacyc yields 5 million compounds"
