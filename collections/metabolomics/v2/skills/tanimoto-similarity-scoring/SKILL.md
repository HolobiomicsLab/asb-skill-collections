---
name: tanimoto-similarity-scoring
description: Use when when running iterative reaction network expansion (Pickaxe) and you need to reduce the combinatorial explosion of generated compounds by prioritizing those structurally similar to a reference set (e.g., known metabolites, drug targets, or desired scaffolds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0154
  tools:
  - RDKit
  - Pickaxe
  - pytest
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

# tanimoto-similarity-scoring

## Summary

Compute maximum Tanimoto similarity scores between generated compounds and a target compound set using RDKit fingerprints, then scale and sample the results to prioritize structurally similar compounds for reaction network expansion. This skill enables controlled exploration of chemical space by focusing generative reactions on compounds most similar to known targets.

## When to use

When running iterative reaction network expansion (Pickaxe) and you need to reduce the combinatorial explosion of generated compounds by prioritizing those structurally similar to a reference set (e.g., known metabolites, drug targets, or desired scaffolds). Specifically, use this skill before each generation when the compound set exceeds your computational budget or when you want to bias the network toward biologically or chemically relevant structures.

## When NOT to use

- Input compounds are already pre-screened or filtered by a previous similarity step; applying redundant Tanimoto filtering will waste computation without reducing compound set size further.
- You have no prior knowledge of target structures or reference compounds; scoring will be uninformative without meaningful targets to compare against.
- Sample size exceeds or equals the total compound set; sampling cannot reduce set size and will degrade diversity.

## Inputs

- Set of generated compounds (SMILES format)
- Target compound set (SMILES format, fingerprints)
- Sample size parameter (integer: number of compounds to retain)
- Weighting exponent (numeric, default 4 for T^4 scaling)

## Outputs

- Filtered compound set (SMILES format, subset of input)
- Tanimoto similarity scores per retained compound
- Sampling probabilities (inverse complementary CDF distribution)

## How to apply

For each compound in the current generation, compute its Tanimoto similarity to every compound in the target set using RDKit's molecular fingerprint comparison, retaining the maximum similarity score per compound. Scale these maximum scores using a weighting function (default T^4 to emphasize high-similarity compounds). Apply inverse complementary cumulative distribution function (CDF) sampling to select exactly N compounds (sample_size parameter) from the weighted distribution for advancement to the next generation. This two-stage approach—scaling then probabilistic sampling—ensures both deterministic prioritization of similar compounds and stochastic exploration of the broader chemical space.

## Related tools

- **RDKit** (Compute molecular fingerprints and Tanimoto similarity scores between compounds; handle SMILES parsing and structure comparison) — https://rdkit.org/docs/api-docs.html
- **Pickaxe** (Orchestrate iterative reaction network expansion and invoke the Tanimoto similarity filter before each generation) — https://github.com/tyo-nu/MINE-Database
- **pytest** (Write and execute unit tests verifying correct similarity calculation, weight scaling, and inverse CDF sampling behavior) — https://docs.pytest.org/en/stable/

## Examples

```
# In pickaxe_run.py: instantiate and apply Tanimoto sampling filter
from minedatabase.filters import TanimotoSamplingFilter
target_smiles = ['CCO', 'c1ccccc1']  # target compounds as SMILES
filter_obj = TanimotoSamplingFilter(sample_size=1000, target_compounds=target_smiles, weighting_exponent=4)
pickaxe.filters.append(filter_obj)
```

## Evaluation signals

- Maximum Tanimoto similarity scores lie in [0, 1] and correctly reflect fingerprint overlap between each compound and the target set.
- Scaled weights (T^4) monotonically increase with raw similarity and are strictly positive; inspect a sample of raw vs. scaled scores to confirm scaling is applied.
- Exactly sample_size compounds are retained in each generation, and compounds with higher scaled scores have higher probability of selection (verify via probability mass function from inverse CDF sampler).
- Retained compounds show higher average similarity to targets than a random sample of the same size (statistical comparison, e.g., t-test).
- No duplicate compounds in the output, and all retained compounds are present in the input set (set membership and cardinality checks).

## Limitations

- Fingerprint similarity (Tanimoto) captures only structural/topological similarity; compounds with high Tanimoto scores may have very different biological or physicochemical properties.
- Performance and memory scale with the product of generated compounds × target compounds; very large target sets or intermediate generations may require sampling or batching.
- The default T^4 weighting is empirical and may be suboptimal for sparse fingerprint spaces or when most compounds have low similarity; parameter tuning may be required for domain-specific applications.
- Inverse CDF sampling introduces stochasticity; reproducibility requires fixing the random seed, and deterministic filtering (thresholding) may be preferable if variability is undesired.

## Evidence

- [other] The Tanimoto sampling filter scales each compound's maximum Tanimoto similarity score using a weighting function (default T^4), then applies inverse complementary distribution function sampling to select N compounds (sample_size) from the scaled distribution for the next generation.: "The Tanimoto sampling filter scales each compound's maximum Tanimoto similarity score using a weighting function (default T^4), then applies inverse complementary distribution function sampling to"
- [other] compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse complementary CDF sampling to select sample_size compounds to keep: "compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse complementary CDF sampling"
- [intro] Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded: "Specified filters are applied before each generation (and at the end of the run if specified) to reduce the number of compounds to be expanded"
- [intro] This tanimoto score is scaled and then the distribution is sampled by inverse complementary distribution function sampling to select N compounds: "This tanimoto score is scaled and then the distribution is sampled by inverse complementary distribution function sampling to select N compounds"
- [other] Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools"
