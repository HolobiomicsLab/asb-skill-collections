---
name: filter-threshold-parameterization
description: Use when when expanding a compound set through multi-generation Pickaxe
  runs, use this skill if you want to retain compounds based on a similarity or property
  metric (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0176
  tools:
  - RDKit
  - pytest
  - Python
  - Pickaxe (MINE-Database)
  license_tier: open
  provenance_tier: literature
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

# filter-threshold-parameterization

## Summary

Parameterize compound filters with generation-specific threshold values to control selective retention of compounds during iterative reaction network expansion. This skill applies when you need to tune filtering stringency across successive Pickaxe generations to balance coverage against computational/chemical feasibility.

## When to use

When expanding a compound set through multi-generation Pickaxe runs, use this skill if you want to retain compounds based on a similarity or property metric (e.g., Tanimoto similarity to targets, metabolomics peak match) and wish to apply different retention thresholds at each generation—typically tightening thresholds in later generations to reduce bloat.

## When NOT to use

- If your filter criterion does not reduce to a scalar or vector comparison (e.g., you need heuristic or rule-based selection that cannot be expressed as a threshold comparison).
- If you want to apply the same threshold across all generations without modification; use a simpler fixed-threshold filter instead.
- If your candidate compound set is already pre-filtered or curated by external means and does not require generation-specific refinement.

## Inputs

- target compound list (SMILES strings or file path)
- per-generation threshold value (0.0–1.0 scalar or per-generation list)
- candidate compound set (from prior Pickaxe generation)
- RDKit fingerprint type specification (e.g., Morgan, Tanimoto-compatible)

## Outputs

- set of compound IDs to be filtered out (below threshold)
- set of compound IDs retained for reaction in next generation
- filter application log (optional: threshold enforcement summary and removal statistics)

## How to apply

Define a per-generation threshold value (typically a scalar in the range 0.0–1.0) that is passed to the Filter subclass at initialization. Implement the _choose_cpds_to_filter method to compute the filtering metric (e.g., maximum Tanimoto similarity using RDKit fingerprints) for each candidate compound, then compare it against the per-generation threshold to decide retention. Return the set of compound IDs that fail the threshold (to be filtered out). Optionally implement _pre_print and _post_print to log threshold enforcement and removal statistics for audit trail and debugging.

## Related tools

- **RDKit** (computes Morgan fingerprints and Tanimoto similarity scores for threshold comparison) — https://rdkit.org/docs/api-docs.html
- **pytest** (unit testing framework for validating threshold enforcement and edge cases in filter implementations) — https://docs.pytest.org/en/stable/
- **Python** (language for implementing Filter subclass and parameterized threshold logic)
- **Pickaxe (MINE-Database)** (iterative reaction network expansion engine that applies filters before each generation) — https://github.com/tyo-nu/MINE-Database

## Examples

```
# In a Pickaxe run setup, instantiate a Tanimoto threshold filter with per-generation thresholds:
from minedatabase.filters import TanimotoThresholdFilter
filter_obj = TanimotoThresholdFilter(target_compounds='targets.smi', threshold_list=[0.85, 0.80, 0.75])
# Then pass it to Pickaxe during network expansion; it will retain only compounds with max Tanimoto similarity >= the generation-specific threshold before each reaction round.
```

## Evaluation signals

- Verify that compounds with metric scores strictly below the threshold are removed; those meeting or exceeding the threshold are retained.
- Confirm that threshold values are applied consistently and independently for each generation if a per-generation list is supplied.
- Inspect filter logs (_post_print output) to validate removal statistics match the set of IDs returned by _choose_cpds_to_filter.
- Unit test edge cases: empty candidate set, all compounds below threshold (full removal), all compounds above threshold (no removal), threshold boundary cases (e.g., metric == threshold).
- Cross-check that compound retention aligns with expected fingerprint similarity distributions using RDKit directly on a small test set.

## Limitations

- Threshold values (0.0–1.0) are problem-specific and require empirical tuning; no universal defaults are provided in the article.
- RDKit fingerprint type (Morgan, Tanimoto-compatible) must be chosen carefully; some fingerprints may not be appropriate for all chemical spaces.
- Per-generation thresholds require predefined values for all generations in advance; adaptive or feedback-based threshold adjustment is not addressed.
- Filtering before each generation can result in local optima if early-generation thresholds remove compounds that could seed valuable chemistry in later generations.
- Computational cost scales with candidate set size and number of targets; large expansions may require fingerprint caching or batch processing for performance.

## Evidence

- [other] per-generation threshold value (0.0–1.0): "In __init__, accept a target compound list (as SMILES or loaded from file) and a per-generation threshold value (0.0–1.0)."
- [other] Tanimoto threshold filter logic: "In _choose_cpds_to_filter, iterate through candidate compounds, compute the maximum Tanimoto similarity to any target fingerprint using RDKit, and return the set of compound IDs with similarity"
- [intro] Filter application before each generation: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [intro] Tanimoto threshold filter reference: "Before each generation the maximum similarity for each compound set to be reacted is compared to a threshold. Compounds greater than or equal to the threshold are reacted"
- [other] Filter logging and audit trail: "Optionally implement _pre_print and _post_print to log filter application status and removal statistics."
- [intro] RDKit fingerprint use: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools."
- [other] Testing framework requirement: "Write unit tests in tests/test_unit/test_filters.py using pytest fixtures to verify threshold enforcement and edge cases."
- [other] Filter subclass implementation location: "Write custom Filter subclass in minedatabase/filters.py"
