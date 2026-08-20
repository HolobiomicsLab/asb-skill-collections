---
name: distribution-statistics-summarization
description: Use when you have loaded a collection of molecular fingerprint vectors
  (such as biosynfoni fingerprints from a deposited dataset) and need to characterize
  their statistical and distributional properties before using them for machine learning,
  similarity searching, or method validation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3318
  tools:
  - biosynfoni
  - pip
  - RDKit
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.26434/chemrxiv-2025-cwq74
  title: biosynfoni
- doi: 10.5281/zenodo.14822624
  title: ''
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic
  research
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# distribution-statistics-summarization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute summary statistics and distributional characteristics of molecular fingerprint vector collections, including bit-frequency distributions, sparsity metrics, and pairwise similarity coefficients. This skill enables quantitative characterization of fingerprint datasets to understand their statistical properties and suitability for downstream applications.

## When to use

Apply this skill when you have loaded a collection of molecular fingerprint vectors (such as biosynfoni fingerprints from a deposited dataset) and need to characterize their statistical and distributional properties before using them for machine learning, similarity searching, or method validation. Trigger conditions include: (1) received a new fingerprint dataset and need baseline statistical characterization; (2) comparing fingerprint encoding schemes or dataset sources; (3) validating that a fingerprint resource meets expected sparsity or similarity criteria.

## When NOT to use

- Fingerprint vectors have not yet been loaded or are not available in a standard array/matrix format.
- You only have a small sample of fingerprints (n < ~100) and need robust population statistics — consider alternatives or acknowledge reduced confidence in tail behavior.
- The goal is to predict molecular properties or perform classification; use supervised feature selection or model evaluation metrics instead of unsupervised distributional summary.

## Inputs

- collection of molecular fingerprint vectors (e.g., biosynfoni count fingerprints from a Zenodo dataset)
- fingerprint format (vector of integers or bit positions)

## Outputs

- summary statistics table (mean, median, standard deviation of bit-frequencies, sparsity, and pairwise Tanimoto similarity)
- bit-frequency distribution (histogram or density plot)
- sparsity distribution (histogram or density plot)
- pairwise Tanimoto similarity distribution (histogram or density plot)

## How to apply

Load all fingerprint vectors from the dataset (e.g., from Zenodo deposit 10.5281/zenodo.14822624 using the biosynfoni package). Compute bit-frequency distribution by counting the proportion of vectors with a '1' at each bit position across the full collection. Calculate the sparsity metric as the proportion of zero bits per vector, then aggregate across all vectors. Compute pairwise Tanimoto similarity coefficients for all vector pairs to characterize inter-fingerprint relatedness. Generate a summary statistics table reporting mean, median, and standard deviation of bit-frequencies, sparsity values, and pairwise similarity scores. Create histograms or density plots for each distribution to visualize bit-frequency, sparsity, and Tanimoto similarity patterns. The rationale is that these statistics reveal whether the fingerprint encoding is appropriately sparse, whether bits are informative (non-uniform frequency), and whether the similarity landscape is suitable for chemical space exploration.

## Related tools

- **biosynfoni** (Load and convert molecular structures to biosynfoni fingerprint vectors for statistical analysis) — https://github.com/lucinamay/biosynfoni
- **pip** (Install biosynfoni package in development mode (pip install -e .[dev]) to access fingerprint computation)
- **RDKit** (Parse molecular structures (SMILES, InChI, SDF) required as input to biosynfoni fingerprinting)

## Examples

```
from biosynfoni import Biosynfoni
import numpy as np
from scipy.spatial.distance import pdist
fps = [Biosynfoni(mol).fingerprint for mol in molecules]
bit_freq = np.mean(np.array(fps), axis=0)
sparsity = 1.0 - (np.count_nonzero(fps) / np.array(fps).size)
tanimoto_dist = pdist(fps, metric='jaccard')
print(f'Mean bit frequency: {bit_freq.mean():.3f}, Sparsity: {sparsity:.3f}')
```

## Evaluation signals

- Summary statistics table contains all computed metrics (mean, median, std dev for bit-frequencies, sparsity, and Tanimoto similarity) with no missing or NaN values.
- Distribution plots display expected shapes: bit-frequency histogram should show variation across positions (not uniform); sparsity histogram should concentrate toward sparse region (high proportion of zeros); Tanimoto similarity distribution should reflect molecular diversity in the dataset.
- Sparsity metric values fall within expected range (0–1) for molecular fingerprints, typically > 0.5 indicating sparse encodings.
- Pairwise Tanimoto coefficients are bounded in [0, 1] with mean and median values consistent with chemical similarity expectations for the underlying dataset (e.g., natural products should show moderate baseline similarity).
- Number of fingerprint vectors processed equals the count declared in the Zenodo dataset deposit metadata, confirming complete data loading.

## Limitations

- Computational cost scales quadratically (O(n²)) with fingerprint count when computing all-pairs Tanimoto similarity; large datasets (n > 100k) may require sparse approximations or sampling strategies.
- Summary statistics assume fingerprints are independent samples; if the dataset contains replicate or near-duplicate molecules, distributional estimates may be biased.
- Bit-frequency and sparsity statistics are sensitive to fingerprint bit-width and encoding scheme (count vs. binary); comparisons across different fingerprint types require normalization.
- No changelog found — version history and update documentation absent for biosynfoni, which may affect reproducibility across different installation dates.

## Evidence

- [other] Compute bit-frequency distribution across all positions in the fingerprint vectors.: "Compute bit-frequency distribution across all positions in the fingerprint vectors"
- [other] Calculate sparsity metric (proportion of zero bits) across the dataset.: "Calculate sparsity metric (proportion of zero bits) across the dataset"
- [other] Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs.: "Compute pairwise Tanimoto similarity coefficients for all fingerprint vector pairs"
- [other] Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores.: "Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores"
- [intro] biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research: "biosynfoni is a molecular fingerprint resource designed for natural product chemistry and bioinformatic research"
- [readme] a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research: "a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research"
- [other] Validation: verify that summary statistics table contains all computed metrics with no missing values and that plots display expected distributional shapes.: "Validation: verify that summary statistics table contains all computed metrics with no missing values and that plots display expected distributional shapes"
