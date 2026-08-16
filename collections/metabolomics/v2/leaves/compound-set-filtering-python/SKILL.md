---
name: compound-set-filtering-python
description: Use when when running Pickaxe reaction network expansion and you need
  to reduce the candidate compound set before each generation using criteria not covered
  by built-in filters (e.g., similarity thresholds, metabolomics matching, or target-based
  selection).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3047
  tools:
  - Python
  - RDKit
  - pytest
  - MINE-Database (Pickaxe)
  license_tier: open
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

# compound-set-filtering-python

## Summary

Implement a custom Python filter subclass within the MINE-Database (Pickaxe) framework to selectively retain or discard compounds during iterative reaction network expansion based on user-defined criteria. This skill enables control over compound set size and chemical space exploration by applying filtering logic before each generation of reactions.

## When to use

When running Pickaxe reaction network expansion and you need to reduce the candidate compound set before each generation using criteria not covered by built-in filters (e.g., similarity thresholds, metabolomics matching, or target-based selection). Use this when you want to constrain computational cost, focus on biologically relevant chemistry, or implement domain-specific retention logic.

## When NOT to use

- If you require filtering logic based on pre-computed properties already stored in MongoDB; use direct database queries instead.
- If you need real-time interactive filtering during Pickaxe execution; the framework applies filters only before each full generation.
- If your filtering criterion requires external tools or services not available as Python libraries or file-based inputs.

## Inputs

- Compound pool (set of compound IDs from current generation)
- Reference compound list (SMILES strings or file path)
- Filter parameters (thresholds, tolerances, metadata files)
- RDKit-compatible compound structures (implicit via Pickaxe)

## Outputs

- Set of compound IDs to filter out (remove from next generation)
- Optionally: filtering statistics and logs (via _post_print)

## How to apply

Create a Filter subclass in minedatabase/filters.py that inherits from the Filter base class and implements the _choose_cpds_to_filter method, which receives the current compound pool and returns the set of compound IDs to be filtered out. Initialize the filter with required parameters (e.g., target compounds as SMILES, threshold values, or metadata files) in __init__. For threshold-based filters like Tanimoto similarity, generate RDKit fingerprints (Morgan or Tanimoto-compatible) for reference compounds and store them; in _choose_cpds_to_filter, iterate through candidate compounds, compute similarity metrics, and return compounds failing the criterion. Optionally implement _pre_print and _post_print methods to log filtering statistics. Write pytest-based unit tests in tests/test_unit/test_filters.py to verify threshold enforcement, edge cases, and consistency across generations. Register the filter in pickaxe_run.py to expose its parameters and integrate it into the Pickaxe workflow.

## Related tools

- **RDKit** (Compute molecular fingerprints (Morgan, Tanimoto-compatible) and similarity scores for filtering decisions) — https://rdkit.org/docs/api-docs.html
- **pytest** (Write and execute unit tests for filter correctness, edge cases, and threshold validation) — https://docs.pytest.org/en/stable/
- **Python** (Language for implementing Filter subclass and integration into Pickaxe framework)
- **MINE-Database (Pickaxe)** (Host framework that calls _choose_cpds_to_filter before each generation and applies filtered set) — https://github.com/tyo-nu/MINE-Database

## Examples

```
class TanimotoThresholdFilter(Filter):
    def __init__(self, target_smiles_list, threshold=0.7):
        self.targets = target_smiles_list
        self.threshold = threshold
        self.target_fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2) for s in target_smiles_list]
    
    def _choose_cpds_to_filter(self, cpd_set):
        to_remove = set()
        for cpd_id in cpd_set:
            cpd_mol = Chem.MolFromSmiles(self.db.get_compound(cpd_id).structure)
            cpd_fp = AllChem.GetMorganFingerprintAsBitVect(cpd_mol, 2)
            max_sim = max([DataStructs.TanimotoSimilarity(cpd_fp, tfp) for tfp in self.target_fps])
            if max_sim < self.threshold:
                to_remove.add(cpd_id)
        return to_remove
```

## Evaluation signals

- Verify that _choose_cpds_to_filter correctly returns compound IDs with similarity strictly below (or above, depending on logic) the specified threshold, using unit tests with known compound pairs.
- Check that filtering reduces the compound pool consistently across generations according to the threshold criterion; plot or log removal counts per generation.
- Confirm that the filter integrates into pickaxe_run.py without import errors and that parameters (threshold, target compounds, file paths) are correctly exposed and passed.
- Validate that _pre_print and _post_print output to stdout as expected, including summary statistics (e.g., 'Filtered X compounds, Y remain').
- Run a small end-to-end Pickaxe expansion with your filter enabled and verify that final compound counts and metadata match expectations given the threshold and input set.

## Limitations

- Filter is applied only before each full generation, not mid-generation, limiting fine-grained control over reaction scope.
- Fingerprint computation (RDKit Morgan, Tanimoto) scales linearly with compound pool size; large expansions (millions of compounds) may incur significant computational overhead.
- Filtering logic is evaluated in-memory; filters requiring external database queries or API calls must cache or pre-load reference data to avoid bottlenecks.
- No built-in support for filtering based on multiple independent criteria; chaining multiple Filter instances requires custom orchestration in pickaxe_run.py.

## Evidence

- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [other] The Tanimoto threshold filter computes the maximum RDKFingerprint Tanimoto similarity score for each compound against all target compounds, then compares this maximum similarity to a per-generation threshold value; compounds meeting or exceeding the threshold are retained for reaction in the next generation.: "The Tanimoto threshold filter computes the maximum RDKFingerprint Tanimoto similarity score for each compound against all target compounds, then compares this maximum similarity to a per-generation"
- [other] Write custom Filter subclass in minedatabase/filters.py and expose options for this filter subclass and add it to a pickaxe run in pickaxe_run.py: "Write custom Filter subclass in minedatabase/filters.py"
- [other] _choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep: "_choose_cpds_to_filter - This is the main method you need to implement, where you can loop through the compounds at each generation and decide which ones to keep"
- [other] Write unit test(s) for this custom filter in tests/test_unit/test_filters.py: "Write unit test(s) for this custom filter in tests/test_unit/test_filters.py"
- [other] Creating a custom filter requires a working knowledge of python. We utilize pytest and have defined useful fixtures for use in the tests.: "Creating a custom filter requires a working knowledge of python. We utilize pytest and have defined useful fixtures for use in the tests."
- [other] Default filters are created using RDKit, a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools."
