---
name: filter-subclass-implementation-in-python
description: Use when when you need to apply domain-specific or novel filtering logic to compounds during Pickaxe reaction network expansion—for example, filtering by Tanimoto similarity to targets, mass tolerance to metabolomics peaks, or custom molecular descriptors—and the built-in filters do not meet your.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - RDKit
  - pytest
  - MINE-Database / Pickaxe
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- MINE-Database, also referred to as Pickaxe, is a python library allows you to efficiently create reaction networks
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

# filter-subclass-implementation-in-python

## Summary

Implement a custom compound filter by subclassing the Filter abstract base class in the MINE-Database (Pickaxe) framework, then integrate it into the reaction network generation pipeline. This skill enables selective filtering of compounds during iterative reaction generation to reduce computational load or enforce domain-specific constraints.

## When to use

When you need to apply domain-specific or novel filtering logic to compounds during Pickaxe reaction network expansion—for example, filtering by Tanimoto similarity to targets, mass tolerance to metabolomics peaks, or custom molecular descriptors—and the built-in filters do not meet your requirements.

## When NOT to use

- The built-in threshold or sampling filters already satisfy your requirements exactly.
- You do not have access to the source code or cannot modify pickaxe_run.py and filters.py.
- Your filtering logic does not depend on compound properties or run state (e.g., static allow-lists are better handled as input validation).

## Inputs

- compound_list: list of Compound objects with SMILES structures and identifiers
- filter parameters (e.g., sample_size, target_compounds, mass_tolerance, thresholds)
- optional reference data (e.g., target fingerprints, metabolomics peaks)

## Outputs

- filtered_compound_list: subset of input compounds passing the filter criteria
- cardinality and composition of filtered set
- logging/summary statistics (via _post_print)

## How to apply

Create a new Python class that inherits from the Filter abstract base class in minedatabase/filters.py. Implement __init__ to store filtering parameters (e.g., sample_size, target fingerprints), filter_name() to return a descriptive string, and the core _choose_cpds_to_filter(compound_list) method to iterate through compounds and return a filtered subset. Optionally implement _pre_print() and _post_print() for logging. Use RDKit to compute molecular properties (e.g., Tanimoto similarity via fingerprints) as needed. Instantiate your filter with appropriate parameters, append it to the pickaxe object's filters list in pickaxe_run.py, and write unit tests in tests/test_unit/test_filters.py using pytest to verify correctness of filtering logic, property calculation, and output cardinality.

## Related tools

- **RDKit** (Compute molecular fingerprints and similarity metrics (e.g., Tanimoto) for filtering decisions) — https://rdkit.org/docs/api-docs.html
- **pytest** (Write and execute unit tests for filter correctness, property calculation, and sampling behavior) — https://docs.pytest.org/en/stable/
- **MINE-Database / Pickaxe** (Host framework providing Filter abstract base class, integration pipeline, and compound object model) — https://github.com/tyo-nu/MINE-Database

## Examples

```
class TanimotoSamplingFilter(Filter):
    def __init__(self, sample_size, target_fps):
        self.sample_size = sample_size
        self.target_fps = target_fps
    def _choose_cpds_to_filter(self, cpds):
        scores = [max(DataStructs.TanimotoSimilarity(c.fp, t) for t in self.target_fps) for c in cpds]
        scaled = [s**4 for s in scores]
        return np.random.choice(cpds, self.sample_size, p=scaled/sum(scaled))
```

## Evaluation signals

- Filtered compound list has cardinality ≤ input list (no compounds added, only removed).
- Molecular properties (e.g., Tanimoto similarities) computed by the filter match independent RDKit calculations on the same compounds and targets.
- Sampling distribution (if used) produces a representative subset with correct weight scaling (e.g., T^4 scaling produces higher selection probability for high-similarity compounds).
- Unit tests pass, including edge cases (empty compound list, all compounds filtered, single compound, zero sample_size).
- Filter integrates without errors into pickaxe_run.py: objects instantiate, append to filters list, and run without exceptions during network generation.

## Limitations

- Filter operates only on compounds present in a given generation; it cannot retroactively modify earlier generations.
- Filtering is applied before each generation and optionally at the end; timing and order relative to other filters matter for the final output composition.
- Custom filters require knowledge of Python, RDKit API, and the Pickaxe Filter class interface; performance is limited by the implementation's algorithmic complexity (e.g., O(n²) pairwise similarity computation can be slow for large compound sets).
- Fingerprint choice and Tanimoto similarity metric are fixed in the Tanimoto sampling filter; alternative similarity metrics or fingerprints require subclass modification.

## Evidence

- [other] Subclass the Filter abstract base class in minedatabase/filters.py and implement the __init__ method to initialize sample_size and target compound fingerprints.: "Subclass the Filter abstract base class in minedatabase/filters.py and implement the __init__ method to initialize sample_size and target compound fingerprints."
- [other] _choose_cpds_to_filter method to compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse complementary CDF sampling to select sample_size compounds to keep.: "_choose_cpds_to_filter method to compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse"
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded.: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [other] Write custom Filter subclass in minedatabase/filters.py; Expose options for this filter subclass and add it to a pickaxe run in pickaxe_run.py; Write unit test(s) for this custom filter in tests/test_unit/test_filters.py: "Write custom Filter subclass in minedatabase/filters.py. Expose options for this filter subclass and add it to a pickaxe run in pickaxe_run.py. Write unit test(s) for this custom filter in"
- [other] We utilize pytest and have defined useful fixtures for use in the tests.: "We utilize pytest and have defined useful fixtures for use in the tests."
- [other] Default filters are created using RDKit, a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools."
