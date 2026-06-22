---
name: molecular-fingerprint-bit-frequency-analysis
description: Use when you have loaded a collection of molecular fingerprint vectors (e.g., from biosynfoni fingerprints deposited in Zenodo) and need to assess their statistical properties before using them for classification, similarity search, or method validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0292
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  tools:
  - biosynfoni
  - pip
  - black
  - pytest
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
- doi: 10.5281/zenodo.14822624
  title: ''
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.26434/chemrxiv-2025-cwq74
    title: biosynfoni
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26434/chemrxiv-2025-cwq74
  all_source_dois:
  - 10.26434/chemrxiv-2025-cwq74
  - 10.5281/zenodo.14822624
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-bit-frequency-analysis

## Summary

Compute and characterize the statistical distribution of bit frequencies across molecular fingerprint vectors in a deposited dataset. This skill quantifies sparsity, bit-level activation patterns, and pairwise similarity to validate fingerprint properties and suitability for downstream bioinformatic research.

## When to use

Apply this skill when you have loaded a collection of molecular fingerprint vectors (e.g., from biosynfoni fingerprints deposited in Zenodo) and need to assess their statistical properties before using them for classification, similarity search, or method validation. Use it to establish baseline characterization of bit-frequency distributions, sparsity metrics, and pairwise Tanimoto similarity patterns across the full dataset.

## When NOT to use

- Input fingerprints are already labeled or pre-filtered by a classification model — use this skill on the raw, unfiltered dataset instead.
- Fingerprints are from a heterogeneous mix of sources with fundamentally different bit encodings — normalize to a common fingerprint schema first.
- Only a small subset of molecules is available (e.g., < 100 molecules) — statistical properties may not be reliable or generalizable.

## Inputs

- biosynfoni fingerprint vector dataset (numpy arrays or count vectors from 10.5281/zenodo.14822624)
- Complete collection of molecular fingerprints (all vectors from the deposited resource)

## Outputs

- Summary statistics table with mean, median, standard deviation for bit-frequencies, sparsity, and Tanimoto similarity
- Bit-frequency distribution (proportion of '1' bits per position across dataset)
- Sparsity metric per fingerprint and aggregate sparsity distribution
- Pairwise Tanimoto similarity coefficient matrix and aggregated similarity distribution
- Distribution plots (histograms/density plots) for bit-frequencies, sparsity values, and pairwise similarity

## How to apply

Install the biosynfoni package in development mode (pip install -e .[dev]) and load all fingerprint vectors from the source dataset. Compute bit-frequency distribution by counting the proportion of molecules with a '1' bit at each fingerprint position across all positions. Calculate sparsity as the proportion of zero bits in each fingerprint vector and aggregate across the dataset. Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs using the formula (intersection / union) of bit sets. Generate summary statistics (mean, median, standard deviation) for bit-frequencies, sparsity values, and Tanimoto similarity scores. Visualize distributions using histograms or density plots for each metric. Validate by confirming the summary statistics table contains all computed metrics with no missing values and that distribution plots exhibit expected shapes (e.g., unimodal or right-skewed for similarity).

## Related tools

- **biosynfoni** (Generate or load molecular fingerprint vectors and provide the count-based fingerprint format for analysis) — https://github.com/lucinamay/biosynfoni
- **pip** (Install biosynfoni and its development dependencies in editable mode)
- **black** (Code formatting utility for maintaining consistent style during analysis script development) — https://github.com/psf/black
- **pytest** (Unit testing framework for validating correctness of statistical computations)

## Examples

```
from biosynfoni import Biosynfoni; import numpy as np; fps = [Biosynfoni(mol).fingerprint for mol in mols]; bit_freqs = np.mean(fps, axis=0); sparsity = np.mean(fps == 0); similarities = [1 - scipy.spatial.distance.cdist([fps[i]], fps[i+1:], metric='jaccard') for i in range(len(fps)-1)]
```

## Evaluation signals

- Summary statistics table is complete with no missing values for all three metrics (bit-frequency, sparsity, Tanimoto similarity)
- Bit-frequency values are bounded in [0, 1] representing valid proportions; median sparsity is consistent with expected natural product fingerprint density
- Tanimoto similarity coefficients are bounded in [0, 1] with expected distribution shape (e.g., right-skewed for diverse chemical space)
- Distribution plots display expected shapes and match computed summary statistics (e.g., histogram bins sum to total fingerprint count; density curve integrates to 1)
- No NaN or infinite values in computed statistics; all pairwise similarity computations complete without convergence errors

## Limitations

- Bit-frequency analysis assumes all fingerprint vectors use the same bit-length and encoding scheme; heterogeneous fingerprint formats must be harmonized first.
- Pairwise Tanimoto similarity computation scales as O(n²) in memory and time, which may be infeasible for datasets with > 1 million fingerprints without sparse matrix representations or sampling strategies.
- Summary statistics are descriptive only and do not test for statistical significance of distributional differences across fingerprint subsets; use hypothesis testing (e.g., Kolmogorov–Smirnov) for comparative claims.
- Sparsity and bit-frequency characteristics are specific to the biosynfoni fingerprint design and may not generalize to other molecular fingerprint schemes (ECFP, MACCS, Morgan, etc.).

## Evidence

- [other] What are the statistical properties of the biosynfoni fingerprint vectors in the deposited dataset, including bit-frequency distributions, sparsity characteristics, and pairwise similarity patterns?: "What are the statistical properties of the biosynfoni fingerprint vectors in the deposited dataset, including bit-frequency distributions, sparsity characteristics, and pairwise similarity patterns?"
- [other] Install biosynfoni package in development mode using pip install -e .[dev] from the project root. Load all fingerprint vectors from the Zenodo dataset deposit (10.5281/zenodo.14822624). Compute bit-frequency distribution across all positions in the fingerprint vectors.: "Install biosynfoni package in development mode using pip install -e .[dev] from the project root. Load all fingerprint vectors from the Zenodo dataset deposit (10.5281/zenodo.14822624). Compute"
- [other] Calculate sparsity metric (proportion of zero bits) across the dataset. Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs.: "Calculate sparsity metric (proportion of zero bits) across the dataset. Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs."
- [other] Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores. Create distribution plots (histogram/density) for bit-frequencies, sparsity values, and pairwise Tanimoto similarity.: "Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores. Create distribution plots (histogram/density) for"
- [other] Validation: verify that summary statistics table contains all computed metrics with no missing values and that plots display expected distributional shapes.: "Validation: verify that summary statistics table contains all computed metrics with no missing values and that plots display expected distributional shapes."
- [other] biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research, providing a dataset suitable for statistical characterization of fingerprint properties.: "biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research, providing a dataset suitable for statistical characterization of fingerprint"
- [readme] a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
