---
name: statistical-distribution-visualization
description: Use when after computing aggregate statistics (mean, median, standard deviation, frequency distributions, similarity coefficients) over a large dataset of molecular fingerprints or feature vectors, when you need to verify that computed metrics exhibit expected distributional shapes and to identify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3314
  - http://edamontology.org/topic_2275
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - biosynfoni
  - pip
  - matplotlib
  - seaborn
  - numpy
  - Python
  - Jupyter
  - matplotlib / seaborn
  - pandas
derived_from:
- doi: 10.1186/s13321-025-01081-6
  title: biosynfoni
- doi: 10.1371/journal.pcbi.1009105
  title: ''
evidence_spans:
- biosynfoni
- a biosynformatic molecular fingerprint tailored to natural product chem- and bioinformatic research
- pip install -e .[dev]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_biosynfoni
    doi: 10.1186/s13321-025-01081-6
    title: biosynfoni
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_biosynfoni
schema_version: 0.2.0
---

# statistical-distribution-visualization

## Summary

Generate and display distribution plots (histograms, density curves) for computed statistical metrics to characterize the shape, spread, and shape of a dataset's key properties. This skill is essential for exploratory analysis of fingerprint or molecular feature datasets where understanding distributional properties (bit-frequency distributions, sparsity, similarity scores) directly informs downstream model selection and data quality assessment.

## When to use

Apply this skill after computing aggregate statistics (mean, median, standard deviation, frequency distributions, similarity coefficients) over a large dataset of molecular fingerprints or feature vectors, when you need to verify that computed metrics exhibit expected distributional shapes and to identify outliers or unexpected modes in the data.

## When NOT to use

- Input fingerprint vectors have not yet been loaded or parsed from the dataset—load and parse first.
- Summary statistics (bit-frequencies, sparsity, similarity) have not been computed—compute aggregates before visualization.
- Dataset size is extremely small (n < 10) such that distributional visualization would be uninformative.

## Inputs

- bit-frequency vector (array of counts per fingerprint position)
- sparsity metric array (proportion of zero bits per fingerprint)
- pairwise Tanimoto similarity matrix or 1D array of similarity scores
- summary statistics table (mean, median, std dev for each metric)

## Outputs

- histogram plot of bit-frequency distribution
- histogram or density plot of sparsity values
- histogram or density plot of pairwise Tanimoto similarity scores
- publication-ready figure(s) with labeled axes and legends

## How to apply

After computing summary statistics (bit-frequency distribution, sparsity metric, and pairwise Tanimoto similarity coefficients), generate distribution plots by plotting histograms or density curves for each computed metric. For bit-frequencies, create a plot showing the frequency of 1-bits at each fingerprint position; for sparsity, plot the distribution of zero-bit proportions across all vectors; for similarity, plot the histogram of pairwise Tanimoto scores. Validate that plots display expected distributional shapes—e.g., bit-frequencies should approximate a binomial or uniform distribution depending on the fingerprint design, sparsity should show the proportion of sparse vs. dense fingerprints, and Tanimoto similarities should reflect the chemical diversity of the dataset. Use matplotlib or seaborn for visualization and ensure plots are publication-ready with clear axes labels and legends.

## Related tools

- **biosynfoni** (source of molecular fingerprint vectors and computed bit-frequency, sparsity, and similarity metrics to be visualized) — https://github.com/lucinamay/biosynfoni
- **matplotlib** (core plotting library for generating histograms and density curves)
- **seaborn** (high-level statistical visualization wrapper for polished distribution plots)
- **numpy** (numerical array operations for computing histogram bins and percentiles)

## Evaluation signals

- All three distribution plots (bit-frequency, sparsity, Tanimoto similarity) are generated and display without errors.
- Plots have clear, labeled axes (e.g., 'Bit Position', 'Frequency'; 'Sparsity', 'Count'; 'Tanimoto Similarity', 'Frequency') and informative titles.
- Bit-frequency histogram shows the distribution across all fingerprint positions with no missing bins.
- Sparsity distribution is unimodal or bimodal as expected for the fingerprint design, with range [0, 1].
- Tanimoto similarity plot shows expected chemical diversity pattern—e.g., a mode near 0 for diverse molecules or bimodal for clustered datasets.

## Limitations

- Visualization quality and interpretability depend on choice of bin width (too narrow → noise; too wide → loss of detail); no guidance is provided on optimal binning for fingerprint metrics.
- The skill assumes fingerprints are in a standard format (bit vectors or count vectors); fingerprints with non-standard encoding may require custom preprocessing before visualization.
- Distribution shape interpretation requires domain knowledge of fingerprint design; unexpected distributions may indicate data quality issues, encoding errors, or unusual dataset composition but do not automatically signal the root cause.

## Evidence

- [other] Compute bit-frequency distribution across all positions in the fingerprint vectors.: "Compute bit-frequency distribution across all positions in the fingerprint vectors."
- [other] Create distribution plots (histogram/density) for bit-frequencies, sparsity values, and pairwise Tanimoto similarity.: "Create distribution plots (histogram/density) for bit-frequencies, sparsity values, and pairwise Tanimoto similarity."
- [other] Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores.: "Generate summary statistics table including mean, median, and standard deviation of bit-frequencies, sparsity, and similarity scores."
- [other] Validation: verify that plots display expected distributional shapes.: "Validation: verify that summary statistics table contains all computed metrics with no missing values and that plots display expected distributional shapes."
