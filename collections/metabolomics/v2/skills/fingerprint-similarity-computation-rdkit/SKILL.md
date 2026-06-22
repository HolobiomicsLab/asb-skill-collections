---
name: fingerprint-similarity-computation-rdkit
description: Use when when implementing a similarity-based filter for Pickaxe compound expansion that must retain or remove candidates based on their structural resemblance to a target compound set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0659
  tools:
  - RDKit
  - Python
  - pytest
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- MINE-Database requires the use of rdkit, which currently is unavailable to install on pip
- Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.
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

# fingerprint-similarity-computation-rdkit

## Summary

Compute RDKit molecular fingerprints for compounds and calculate Tanimoto similarity scores to identify structurally related compounds. This is essential for filtering compound libraries during reaction network expansion based on similarity thresholds to target structures.

## When to use

When implementing a similarity-based filter for Pickaxe compound expansion that must retain or remove candidates based on their structural resemblance to a target compound set. Use this skill whenever you need to quantify how similar a generated compound is to known targets using fingerprint-based metrics (e.g., Morgan fingerprints).

## When NOT to use

- When you need to preserve all generated compounds without filtering; similarity computation is applied only when explicit filtering is required.
- When target structures are not available or not meaningful for the use case (e.g., de novo generation without reference compounds).
- When real-time performance is critical and fingerprint computation cost cannot be amortized; precomputation and caching help but do not eliminate overhead.

## Inputs

- Target compound list (SMILES strings or file path)
- Per-generation Tanimoto threshold value (float, 0.0–1.0)
- Candidate compound set (compound IDs and SMILES or structures)
- Current generation number (for per-generation threshold lookup if applicable)

## Outputs

- Set of compound IDs to filter out (below-threshold compounds)
- RDKit fingerprint objects (cached for targets)
- Maximum Tanimoto similarity score per candidate compound
- Filter application summary (optional: number removed, retention rate)

## How to apply

Generate RDKit fingerprints (Morgan or Tanimoto-compatible types) for all target compounds once during filter initialization and cache them. For each candidate compound during filtering, compute its RDKit fingerprint and then calculate the maximum Tanimoto similarity score between that candidate and all target fingerprints using RDKit's Tanimoto metric. Compare the maximum similarity against a per-generation threshold value (range 0.0–1.0). The Tanimoto score provides a normalized similarity measure between 0 (completely dissimilar) and 1 (identical), allowing threshold-based retention or removal decisions. This approach balances computational efficiency (precompute target fingerprints) with interpretability (threshold-based decisions).

## Related tools

- **RDKit** (Compute molecular fingerprints (Morgan or other types) and calculate Tanimoto similarity scores between pairs of fingerprints) — https://rdkit.org/docs/api-docs.html
- **Python** (Language for implementing Filter subclass with fingerprint computation and similarity thresholding logic)
- **pytest** (Unit testing framework to verify threshold enforcement, edge cases, and fingerprint computation correctness) — https://docs.pytest.org/en/stable/

## Examples

```
from rdkit import Chem; from rdkit.Chem import AllChem; target_smiles = ['CC(=O)O']; targets = [Chem.MolToSmiles(Chem.MolFromSmiles(s)) for s in target_smiles]; target_fps = [AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2, nBits=2048) for s in target_smiles]; candidate_smiles = 'CCO'; candidate_fp = AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(candidate_smiles), 2, nBits=2048); from rdkit.DataStructs import TanimotoSimilarity; max_sim = max([TanimotoSimilarity(candidate_fp, t_fp) for t_fp in target_fps]); threshold = 0.7; keep = max_sim >= threshold
```

## Evaluation signals

- Verify that all target compounds produce valid RDKit fingerprints and are cached before filtering begins (no repeated computation).
- For each candidate compound, confirm that the reported maximum Tanimoto similarity score is between 0.0 and 1.0 (inclusive) and matches manual RDKit computation.
- Verify that compounds with maximum similarity >= threshold are retained and those with similarity < threshold are filtered out; test boundary cases (similarity exactly at threshold).
- Check that filter statistics (count retained, count removed, retention rate) are mathematically consistent and logged correctly.
- Unit tests should cover edge cases: empty target set, single target, single candidate, threshold = 0.0 (all retained), threshold = 1.0 (only identical retained).

## Limitations

- Fingerprint type (Morgan, Tanimoto-compatible) choice affects similarity scores; different fingerprint algorithms may yield different results for the same compound pair.
- Tanimoto similarity depends on fingerprint bit size and features; small changes in fingerprint parameters can alter threshold decisions.
- Precomputation of target fingerprints assumes targets are fixed; dynamically changing targets would require recomputation, reducing efficiency.
- Threshold value is rigid and global per generation; no adaptive or learned thresholds are supported by this basic implementation.

## Evidence

- [other] The Tanimoto threshold filter computes the maximum RDKFingerprint Tanimoto similarity score for each compound against all target compounds, then compares this maximum similarity to a per-generation threshold value; compounds meeting or exceeding the threshold are retained for reaction in the next generation.: "The Tanimoto threshold filter computes the maximum RDKFingerprint Tanimoto similarity score for each compound against all target compounds, then compares this maximum similarity to a per-generation"
- [other] In _choose_cpds_to_filter, iterate through candidate compounds, compute the maximum Tanimoto similarity to any target fingerprint using RDKit, and return the set of compound IDs with similarity strictly below the threshold to be filtered out.: "iterate through candidate compounds, compute the maximum Tanimoto similarity to any target fingerprint using RDKit, and return the set of compound IDs with similarity strictly below the threshold to"
- [other] Generate RDKit fingerprints (Morgan or Tanimoto-compatible fingerprints) for all target compounds and store them.: "Generate RDKit fingerprints (Morgan or Tanimoto-compatible fingerprints) for all target compounds and store them"
- [other] Default filters are created using RDKit, a python library providing a collection of cheminformatic tools.: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools"
- [intro] Before each generation the maximum similarity for each compound set to be reacted is compared to a threshold. Compounds greater than or equal to the threshold are reacted: "Before each generation the maximum similarity for each compound set to be reacted is compared to a threshold. Compounds greater than or equal to the threshold are reacted"
