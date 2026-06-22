---
name: abstract-method-subclassing-filter-base
description: Use when when you need to apply domain-specific filtering logic to compounds during Pickaxe expansion—for example, retaining only compounds within a Tanimoto similarity threshold to known targets, or compounds matching experimentally detected masses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3318
  tools:
  - RDKit
  - pytest
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

# abstract-method-subclassing-filter-base

## Summary

Implement a custom compound filter for Pickaxe by subclassing the Filter base class and defining _choose_cpds_to_filter, _pre_print, and _post_print methods. This skill enables selective compound retention during iterative reaction network expansion based on user-defined criteria.

## When to use

When you need to apply domain-specific filtering logic to compounds during Pickaxe expansion—for example, retaining only compounds within a Tanimoto similarity threshold to known targets, or compounds matching experimentally detected masses. Use this when the built-in filters (Tanimoto threshold, Tanimoto sampling, metabolomics, target) do not capture your filtering requirement.

## When NOT to use

- Filter logic requires real-time compound property calculations (e.g., thermodynamic stability via eQuilibrator) not pre-computed in the store—consider pre-computing or refactoring.
- You need to filter based on reaction rule properties or cofactor availability rather than compound properties—use reaction-level filtering logic instead.
- Input compound set is empty or None—the filter will receive an empty set and should gracefully return an empty removal set.

## Inputs

- candidate compound set (list or iterator of compound IDs) at each generation
- compound data store (access to SMILES, fingerprints, metadata)
- filter parameters (threshold value, target compound list as SMILES or file path, etc.)

## Outputs

- set of compound IDs to remove (compounds that failed filter criterion)
- optionally, logging output from _pre_print and _post_print (stdout)

## How to apply

Create a new Filter subclass in minedatabase/filters.py with three core methods: __init__ to accept filter parameters (e.g., threshold values, target compound lists), _choose_cpds_to_filter to iterate through candidate compounds, compute your filtering metric (e.g., maximum Tanimoto similarity using RDKit fingerprints), and return the set of compound IDs to remove, and optionally _pre_print and _post_print to log filtering status and removal statistics. The filtering decision is invoked before each generation, so your _choose_cpds_to_filter method receives the candidate compound set and must return those compounds that fail the filter criterion. Expose your filter subclass in pickaxe_run.py and write unit tests in tests/test_unit/test_filters.py using pytest fixtures to verify threshold enforcement and edge cases.

## Related tools

- **RDKit** (compute molecular fingerprints and similarity scores (e.g., Tanimoto) for filtering logic) — https://rdkit.org/docs/api-docs.html
- **pytest** (write and execute unit tests for filter subclass with predefined fixtures) — https://docs.pytest.org/en/stable/
- **Python** (implement Filter subclass with required methods)

## Examples

```
class MyTanimotoFilter(Filter):
    def __init__(self, targets_smiles, threshold):
        self.targets = targets_smiles
        self.threshold = threshold
    def _choose_cpds_to_filter(self, cpds):
        return {cid for cid in cpds if max_tanimoto_similarity(cid, self.targets) < self.threshold}
```

## Evaluation signals

- Subclass properly inherits from Filter base class and implements all required methods (__init__, filter_name, _choose_cpds_to_filter) without errors.
- Unit tests in tests/test_unit/test_filters.py pass, including edge cases (empty compound set, all compounds pass/fail, threshold boundary conditions).
- Filtered compound set size decreases predictably (or as expected) at each generation when integrated into a Pickaxe run; removal statistics logged by _post_print align with filter criterion.
- Filter is exposed and configurable in pickaxe_run.py; a full Pickaxe run completes without exception when the custom filter is active.
- Output compound set schema is preserved (compound IDs match those in the input candidate set); no spurious or duplicate removals occur.

## Limitations

- Filter execution occurs serially before each generation; computationally expensive metrics (e.g., full-graph similarity to all targets for large sets) may slow expansion.
- Filter has access only to compounds stored in the database; pre-computed or external data (e.g., experimental metadata) must be provided at __init__ time or stored in advance.
- Filter decisions are independent at each generation; no inter-generational memory or dynamic threshold adjustment is built into the base pattern.
- Filter method must return a set of IDs to *remove*, not retain; inverted logic may cause confusion if the filtering criterion is naturally expressed as 'keep compounds where X > threshold'.

## Evidence

- [other] Create a Filter subclass in minedatabase/filters.py with __init__, filter_name, and _choose_cpds_to_filter methods.: "Create a Filter subclass in minedatabase/filters.py with __init__, filter_name, and _choose_cpds_to_filter methods."
- [other] _choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [other] _pre_print - This method prints to stdout just before the filter is applied.: "_pre_print - This method prints to stdout just before the filter is applied."
- [other] _post_print - This method prints to stdout just after the filter is applied. Useful for printing a summary of filtering results.: "_post_print - This method prints to stdout just after the filter is applied. Useful for printing a summary of filtering results."
- [other] Write unit test(s) for this custom filter in tests/test_unit/test_filters.py: "Write unit test(s) for this custom filter in tests/test_unit/test_filters.py"
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [other] Creating a custom filter requires a working knowledge of python.: "Creating a custom filter requires a working knowledge of python."
