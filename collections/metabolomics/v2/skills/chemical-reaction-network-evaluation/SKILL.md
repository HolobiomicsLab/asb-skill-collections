---
name: chemical-reaction-network-evaluation
description: Use when you have a rule-based reaction prediction system (like Pickaxe) with a large rule set (e.g., ~1221 MetaCyc generalized rules), and you need to understand the scaling relationship between rule count and reaction coverage to decide how many rules to deploy for a specific application.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2275
  tools:
  - RDKit
  - Python
  - MINE-Database (Pickaxe)
  - MongoDB or TSV export
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

# chemical-reaction-network-evaluation

## Summary

Evaluate the empirical relationship between the number of generalized reaction rules applied and the coverage percentage of a reference reaction database (e.g., MetaCyc). This skill quantifies the trade-off between computational cost and reaction prediction completeness by systematically measuring how many distinct reactions can be represented as rule subsets grow.

## When to use

You have a rule-based reaction prediction system (like Pickaxe) with a large rule set (e.g., ~1221 MetaCyc generalized rules), and you need to understand the scaling relationship between rule count and reaction coverage to decide how many rules to deploy for a specific application. Use this when you want to balance prediction scope against runtime or memory constraints.

## When NOT to use

- You only have a small, domain-specific rule set (<50 rules) where coverage plateaus immediately; scaling analysis is less informative.
- Your reference database is not well-defined or lacks quantitative reaction annotations; you cannot reliably measure coverage.
- You need real-time or online rule selection; this is a one-time characterization study, not a live optimization approach.

## Inputs

- Full generalized reaction rule set (SMARTS strings, ~1221 rules for MetaCyc)
- Representative compound set (SMILES strings or structure identifiers)
- Reference reaction database (MetaCyc reactions to match against)

## Outputs

- Coverage table (TSV format): (number_of_rules, coverage_percent) pairs
- Scaling relationship plot or summary statistics
- Rule subset definitions (ranked or frequency-ordered)

## How to apply

Load the full generalized reaction rule set from a database (e.g., the ~70,000 MetaCyc reactions condensed into ~1221 generic SMARTS rules). Select ordered rule subsets of increasing size (e.g., 20, 100, 272, 500, 956, 1221 rules) using rule importance or frequency-based ranking. For each subset, apply the rules to a representative set of compounds from the target database and compute the percentage of total reactions in the reference database that can be represented. Aggregate the (number_of_rules, coverage_percent) pairs into a table and verify the coverage relationship follows an expected scaling curve (e.g., diminishing returns at higher rule counts). The scaling curve informs optimal rule selection for downstream applications.

## Related tools

- **RDKit** (Apply SMARTS reaction rules to compounds; compute molecular similarity and filter compounds by structure) — https://rdkit.org/docs/api-docs.html
- **Python** (Implement rule selection logic, iteration over rule subsets, coverage computation, and table aggregation)
- **MINE-Database (Pickaxe)** (Load and apply generalized reaction rules; predict reactions from starting compounds) — https://github.com/tyo-nu/MINE-Database
- **MongoDB or TSV export** (Store or serialize rule subsets and coverage results for analysis)

## Evaluation signals

- Coverage percentages increase monotonically with rule count (no non-monotonic dips).
- Coverage curve reaches 100% when all rules are included; no residual uncovered reactions.
- Intermediate coverage values match published reference values (e.g., 272 rules = 90% coverage for MetaCyc) to within ±2%.
- Rule subset sizes and coverage percentages are reproducible across multiple runs with the same ranking strategy.
- Output TSV file is well-formed with headers (number_of_rules, coverage_percent) and matches the row count of rule subsets tested.

## Limitations

- Scaling relationship is specific to the reference database and rule set used; results for MetaCyc may not generalize to KEGG or custom rule sets.
- Coverage measurement depends on the representativeness of the compound set tested; biased or incomplete compound selection will underestimate or overestimate coverage.
- Rule importance/frequency ranking is heuristic; different ranking strategies (e.g., by cofactor requirement, reaction class) may yield different scaling curves.
- The study characterizes average-case coverage; some compound subsets or reaction classes may have coverage profiles that deviate significantly from the aggregate curve.

## Evidence

- [intro] Scaling relationship between rule count and coverage: "20 rules provide 50% coverage, 100 rules provide 78% coverage, 272 rules provide 90% coverage, 500 rules provide 95% coverage, 956 rules provide 99% coverage, and all 1221 rules provide 100% coverage"
- [intro] MetaCyc rule set composition: "approximately 70,000 MetaCyc reactions condensed into generic rules"
- [intro] Rule application methodology: "Pickaxe applies reaction rules, representing reaction transformation patterns, to a list of user-specified compounds in order to predict reactions"
- [intro] Rule representation format: "Rules are generated using `SMARTS` which represent reactions in a string"
- [intro] Output format and workflow: "There are two ways to output data: 1. Writing to a mongo database that is specified by a `mongo uri`, either local or in mongo_uri.csv 2. Local .tsv files"
