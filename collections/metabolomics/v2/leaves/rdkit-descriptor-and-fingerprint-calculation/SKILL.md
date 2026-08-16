---
name: rdkit-descriptor-and-fingerprint-calculation
description: Use when you need to (1) compare structural similarity between generated
  compounds and target/reference structures using Tanimoto similarity scores, (2)
  extract molecular descriptors for machine learning models that predict reaction
  feasibility, (3) implement compound filtering based on chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0209
  tools:
  - RDKit
  - mordred
  - pytest
  - MINE-Database (Pickaxe)
  license_tier: open
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans:
- MINE-Database requires the use of rdkit, which currently is unavailable to install
  on pip
- Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html),
  a python library providing a collection of cheminformatic tools.
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

# RDKit Descriptor and Fingerprint Calculation

## Summary

Calculate molecular fingerprints and cheminformatic descriptors from SMILES strings using RDKit to enable similarity-based compound filtering and feature-driven machine learning in reaction network expansion. This skill is essential for quantifying structural similarity between compounds and extracting predictive features for reaction generation pipelines.

## When to use

Apply this skill when you need to (1) compare structural similarity between generated compounds and target/reference structures using Tanimoto similarity scores, (2) extract molecular descriptors for machine learning models that predict reaction feasibility, (3) implement compound filtering based on chemical space constraints before each generation in a reaction network expansion, or (4) rank or sample compounds from large sets using similarity-weighted distributions.

## When NOT to use

- Fingerprints are already computed and cached; use stored vectors instead to avoid redundant calculation.
- SMILES strings are invalid or cannot be parsed into RDKit molecule objects; validate SMILES syntax before fingerprinting.
- Similarity threshold or sampling strategy is unknown; define filtering criteria (e.g., T > 0.7 or sample_size constraint) before applying the skill.

## Inputs

- SMILES string list (compounds to fingerprint)
- SMILES string list (target/reference structures)
- RDKit molecule objects (optional pre-parsed input)
- Sample size parameter (integer: number of compounds to select)
- Weight exponent (default: 4, for T^4 scaling)

## Outputs

- Molecular fingerprint vectors (RDKit BitVect objects)
- Tanimoto similarity matrix (compound × target)
- Maximum similarity scores per compound (1D array)
- Scaled similarity distribution (probability weights)
- Filtered compound list (subset of input compounds)
- Molecular descriptors (mordred or RDKit-native)

## How to apply

Use RDKit to convert SMILES strings to molecular objects, then compute molecular fingerprints (default: Morgan fingerprints) for each compound and reference set. Calculate pairwise Tanimoto similarity scores between fingerprints to quantify structural similarity. For filtering workflows, compute the maximum Tanimoto similarity of each compound to the target set, then optionally scale scores using a weighting function (e.g., T^4 for emphasis on high-similarity compounds). Apply the scaled similarities as probabilities in inverse complementary cumulative distribution function (CDF) sampling to deterministically select N compounds for the next generation. Integrate descriptor calculations into the Filter abstract base class by implementing the _choose_cpds_to_filter method to loop through compounds at each generation, compute similarities, apply thresholds or sampling, and return the filtered set.

## Related tools

- **RDKit** (Compute Morgan fingerprints, Tanimoto similarity scores, and molecular descriptors from SMILES strings; parse and manipulate chemical structures.) — https://rdkit.org/docs/api-docs.html
- **mordred** (Calculate extended molecular descriptors for machine learning feature engineering in reaction feasibility prediction.)
- **pytest** (Write and execute unit tests to verify fingerprint calculation correctness, Tanimoto similarity computation, and sampling behavior.) — https://docs.pytest.org/en/stable/
- **MINE-Database (Pickaxe)** (Integration point: instantiate custom Filter subclass with fingerprint/similarity logic and append to pickaxe.filters list for per-generation filtering.) — https://github.com/tyo-nu/MINE-Database

## Examples

```
from rdkit.Chem import AllChem; from rdkit import Chem; smi = 'CC(C)C'; mol = Chem.MolFromSmiles(smi); fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048); print(Chem.DataStructs.TanimotoSimilarity(fp, fp))
```

## Evaluation signals

- Fingerprint vectors are non-empty BitVect objects of consistent length for all input compounds.
- Tanimoto similarities fall within [0.0, 1.0] range; max similarity of a compound to itself equals 1.0.
- Scaled weights (T^4) increase non-linearly with similarity; weight(0.5) < weight(0.9) by factor >5.
- Inverse complementary CDF sampling selects exactly sample_size compounds with probability proportional to scaled similarity.
- Filtered compound set size equals sample_size; all retained compounds have higher mean Tanimoto score than discarded compounds (when sorted by similarity).
- Unit tests in tests/test_unit/test_filters.py pass, confirming similarity calculation, weight scaling, and sampling determinism.

## Limitations

- Default fingerprint type (Morgan) may not capture all chemical features relevant to specific reaction types; consider alternative fingerprints (e.g., RDKit, MACCS keys) for specialized domains.
- Tanimoto similarity assumes fingerprints are binary; continuous fingerprints require Tanimoto formula adaptation (Tanimoto coefficient for continuous vectors).
- Computational cost scales quadratically with compound set size; large reaction networks (>1M compounds) may require chunking or approximate similarity methods.
- T^4 weighting is a heuristic default; optimal exponent is problem-dependent and may require tuning for different chemical spaces or reaction rule sets.
- Inverse complementary CDF sampling is stochastic; results vary across runs unless random seed is fixed; use for reproducibility testing.

## Evidence

- [other] The Tanimoto sampling filter scales each compound's maximum Tanimoto similarity score using a weighting function (default T^4), then applies inverse complementary distribution function sampling to select N compounds.: "scales each compound's maximum Tanimoto similarity score using a weighting function (default T^4), then applies inverse complementary distribution function sampling to select N compounds"
- [other] Compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse complementary CDF sampling to select sample_size compounds to keep.: "compute the maximum Tanimoto similarity for each compound to the target set using RDKit fingerprints, scale similarities by the T^4 weight function, and apply inverse complementary CDF sampling to"
- [other] Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools"
- [intro] Before each generation the maximum similarity for each compound set to be reacted is compared to a threshold. Compounds greater than or equal to the threshold are reacted: "maximum similarity for each compound set to be reacted is compared to a threshold. Compounds greater than or equal to the threshold are reacted"
- [intro] rt_important_features specifies which mordred descriptors to use as input into the model: "rt_important_features specifies which mordred descriptors to use as input into the model"
- [other] Subclass the Filter abstract base class in minedatabase/filters.py and implement the __init__ method to initialize sample_size and target compound fingerprints.: "Subclass the Filter abstract base class in minedatabase/filters.py and implement the __init__ method to initialize sample_size and target compound fingerprints"
