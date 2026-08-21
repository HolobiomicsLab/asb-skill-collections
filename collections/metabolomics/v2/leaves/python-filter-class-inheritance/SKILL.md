---
name: python-filter-class-inheritance
description: Use when you need to filter compounds during Pickaxe network expansion
  based on domain-specific criteria (e.g., mass matching, similarity thresholds, retention
  time windows) that are not covered by built-in filters.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - RDKit
  - pytest
  - MINE-Database
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- MINE-Database, also referred to as Pickaxe, is a python library allows you to efficiently
  create reaction networks
- Pickaxe supports running through a command line interface
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

# Implement Custom Filter Subclass via Class Inheritance

## Summary

Create domain-specific filter logic in MINE-Database by subclassing the Filter base class and implementing abstract methods to retain or discard compounds during iterative reaction network expansion. This skill enables filters to be applied before each generation to reduce the compound search space according to user-defined criteria.

## When to use

You need to filter compounds during Pickaxe network expansion based on domain-specific criteria (e.g., mass matching, similarity thresholds, retention time windows) that are not covered by built-in filters. Use this skill when your filtering logic requires custom compound comparison logic, external data (CSV peak lists, target structures), or cheminformatic calculations on SMILES strings.

## When NOT to use

- You need to filter compounds based on criteria already implemented in existing MINE-Database filters (e.g., Tanimoto similarity threshold or target compound matching). Use the built-in filter instead.
- Your filtering criterion is a simple arithmetic threshold on a standard molecular property (molecular weight, logP) that can be handled by a general-purpose chemistry library. Consider whether a simpler, non-class-based approach suffices.
- The filtering logic does not require access to compound SMILES strings or external reference data. A Filter subclass adds unnecessary complexity.

## Inputs

- Filter base class (inherited from minedatabase/filters.py)
- Compound dictionaries with SMILES strings and IDs (generated at each expansion round)
- Optional external data: CSV metabolomics peak list (m/z and retention time), target structure SMILES list, or reference compound sets
- Filter parameters: mass_tolerance (Da), retention_time_tolerance, data file paths, similarity thresholds

## Outputs

- Filter subclass (Python class in minedatabase/filters.py with implemented abstract methods)
- Set of compound IDs to filter out (remove from expansion)
- Optional: log summaries printed via _pre_print and _post_print methods
- Unit test suite (pytest functions in tests/test_unit/test_filters.py)

## How to apply

Create a Filter subclass in minedatabase/filters.py that inherits from the Filter base class and implements three required abstract methods: __init__ (to accept and store filtering parameters such as mass_tolerance, data file paths, or threshold values), filter_name (to return a descriptive string name), and _choose_cpds_to_filter (the core method that iterates over compound dictionaries at each generation, applies your filtering logic using RDKit molecular properties or external data matching, and returns a set of compound IDs to remove). Optionally implement _pre_print and _post_print to log filtering statistics. Use RDKit to compute molecular weights from SMILES, compare against tolerance windows or reference data, and return the set of IDs that fail the filter criterion. Write unit tests in tests/test_unit/test_filters.py covering edge cases (empty input sets, boundary tolerance values, multiple adduct forms or data formats) to validate that filter_name returns a string, _choose_cpds_to_filter returns a set, and known compounds are correctly retained or removed.

## Related tools

- **RDKit** (Compute molecular weights from SMILES strings and generate cheminformatic descriptors (e.g., via mordred) for filtering logic) — https://rdkit.org/docs/api-docs.html
- **pytest** (Write and run unit tests for Filter subclass methods to validate edge cases and correctness) — https://docs.pytest.org/en/stable/
- **Python** (Language for implementing Filter subclass and writing filtering logic)
- **MINE-Database** (Framework containing Filter base class, compound generation pipeline, and integration point for custom filters) — https://github.com/tyo-nu/MINE-Database

## Examples

```
class MetabolomicsFilter(Filter):
    def __init__(self, metabolomics_file, mass_tolerance=0.01):
        self.metabolomics_file = metabolomics_file
        self.mass_tolerance = mass_tolerance
    def filter_name(self):
        return 'metabolomics_filter'
    def _choose_cpds_to_filter(self, compounds):
        peaks = set(float(m) for m in pd.read_csv(self.metabolomics_file)['mz'])
        return {c['_id'] for c in compounds if not any(abs(Descriptors.ExactMolWt(Chem.MolFromSmiles(c['SMILES'])) - p) < self.mass_tolerance for p in peaks)}
```

## Evaluation signals

- Verify filter_name() returns a non-empty string describing the filter.
- Verify _choose_cpds_to_filter() returns a set (not a list or dict) of compound IDs.
- Test with empty compound set (should return empty set); test with peaks/reference data outside tolerance (should filter out all compounds); test with boundary tolerance values to confirm correct inclusion/exclusion.
- Run unit tests with pytest and confirm all fixtures pass; check that known compounds matching reference data are retained and non-matching compounds are removed.
- Verify the filter integrates into pickaxe_run.py and can be applied before each generation without errors.

## Limitations

- The Filter base class requires implementing three abstract methods; incomplete or incorrect implementation will raise errors at runtime.
- External data files (peak lists, target structures) must be in the expected CSV or SMILES format; malformed files or missing columns will cause parsing errors.
- RDKit molecular weight calculations assume valid SMILES strings; invalid or uncanonical SMILES will fail or produce incorrect masses.
- Mass tolerance and retention time tolerance windows are user-specified; overly narrow tolerances may filter out all candidates (false negatives) and overly broad tolerances may retain too many false positives.
- Performance scales with compound set size and number of reference peaks/targets; filtering large sets (millions of compounds) against large reference databases may be slow.

## Evidence

- [other] Write custom Filter subclass inheritance pattern: "Write custom Filter subclass in minedatabase/filters.py"
- [other] Abstract methods required in Filter subclass: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [other] RDKit for molecular weight computation from SMILES: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools."
- [intro] Metabolomics filter applies mass and retention time matching: "It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
- [intro] Filters applied before each generation during network expansion: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [other] Unit test location and pytest usage: "Write unit test(s) for this custom filter in tests/test_unit/test_filters.py"
- [other] Pre and post print methods for logging: "_post_print - This method prints to stdout just after the filter is applied. Useful for printing a summary of filtering results."
