---
name: score-distribution-visualization
description: Use when after computing link scores (e.g., strain correlation, IOKR, or combined scores) across GCF-MF pairs, use this skill to assess whether scores achieve sufficient separation between validated links and the background population.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3697
  - http://edamontology.org/topic_0092
  tools:
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
  - NPLinker
derived_from:
- doi: 10.1371/journal.pcbi.1008920
  title: NPLinker
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- the metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- we use library MS2 spectra from the public, community-driven GNPS knowledge base [33] as a training set for the IOKR model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1371/journal.pcbi.1008920
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
---

# score-distribution-visualization

## Summary

Visualization of raw and standardised scoring distributions for genomic-metabolomic links across validated and all-link populations to assess scoring method effectiveness. This skill enables visual and statistical comparison of how well a scoring function separates true links from decoys.

## When to use

After computing link scores (e.g., strain correlation, IOKR, or combined scores) across GCF-MF pairs, use this skill to assess whether scores achieve sufficient separation between validated links and the background population. This is essential before deciding whether a score is ready for ranking or whether standardisation or alternative scoring schemes are needed.

## When NOT to use

- Scores have not yet been computed or are incomplete for the link population — visualisation requires complete score vectors.
- Validation labels are absent or unreliable, preventing meaningful separation assessment.
- The goal is to rank individual links for a single discovery task, not to evaluate a scoring function's general performance across a benchmark dataset — visualization is for benchmarking and method development, not for operational ranking.

## Inputs

- Raw link scores (numeric vector indexed by GCF-MF pair ID)
- Standardised link scores (numeric vector indexed by GCF-MF pair ID)
- Validation status labels (binary: validated=True/False for each GCF-MF pair)
- GCF sizes (#G), MF sizes (#m), and population size (#N) for each link (optional, for stratified analysis)

## Outputs

- Histogram plots (raw and standardised scores, overlaid by validation status)
- Boxplots (raw and standardised scores, grouped by validated vs. all links)
- Descriptive statistics table (mean, median, std, p-values for each score type and dataset)
- t-test or Mann–Whitney U test p-values comparing validated and all-link distributions

## How to apply

Load the computed raw and standardised score values for all GCF-MF pairs, along with validation status labels (validated vs. non-validated). Generate paired histograms and boxplots contrasting score distributions for validated links versus all hypothetical links. Compute descriptive statistics (mean, median) and perform t-tests to quantify separation (e.g., test whether validated links score significantly higher). Highlight validated links in the plots to reveal overlap, multimodality, or threshold effects. If standardisation was applied, overlay raw and standardised distributions side-by-side to visualise the impact on comparability across links of different GCF/MF sizes. Report p-values and effect sizes to confirm whether the visual separation is statistically significant.

## Related tools

- **NPLinker** (Framework providing strain correlation and IOKR scoring functions whose outputs are visualised) — https://github.com/sdrogers/nplinker
- **BiG-SCAPE** (Produces GCF clustering that defines the link space (GCF-MF pairs) to be scored and visualised)
- **antiSMASH** (Detects BGCs that are clustered into GCFs, anchoring the genomic link space)
- **GNPS** (Provides metabolomic spectra and validated spectral-BGC associations used as ground truth labels)

## Examples

```
import numpy as np; import matplotlib.pyplot as plt; raw_scores = load_scores('raw_correlation.csv'); std_scores = load_scores('standardised_correlation.csv'); validation = load_validation('validated_links.csv'); plt.figure(figsize=(12, 5)); plt.subplot(1, 2, 1); plt.hist(raw_scores[~validation], bins=50, alpha=0.6, label='all'); plt.hist(raw_scores[validation], bins=50, alpha=0.6, label='validated'); plt.xlabel('Raw correlation score'); plt.ylabel('Frequency'); plt.legend(); plt.subplot(1, 2, 2); plt.hist(std_scores[~validation], bins=50, alpha=0.6, label='all'); plt.hist(std_scores[validation], bins=50, alpha=0.6, label='validated'); plt.xlabel('Standardised correlation score'); plt.ylabel('Frequency'); plt.legend(); plt.tight_layout(); plt.savefig('score_distributions.png'); print(f'Raw: mean(all)={raw_scores[~validation].mean():.4f}, mean(validated)={raw_scores[validation].mean():.4f}'); print(f'Std: mean(all)={std_scores[~validation].mean():.4f}, mean(validated)={std_scores[validation].mean():.4f}')
```

## Evaluation signals

- Validated links show a significantly higher mean score than all links (p < 0.01 by t-test), confirming that the score discriminates truth from noise.
- Histograms/boxplots show minimal overlap between validated and all-link distributions, or a sharp threshold above which validated links are enriched.
- Standardised score distributions have mean ~0 for all links and elevated mean (e.g., >3) for validated links, as demonstrated in the paper.
- p-value improves dramatically upon standardisation (e.g., from p=0.0001 to p=6.8×10⁻⁶⁴), indicating that standardisation successfully removes size-related biases.
- Distribution shapes are consistent across independent datasets (e.g., Crüsemann, Gross, Leão) when the skill is applied to multiple cohorts.

## Limitations

- Visualization effectiveness depends on the quality and completeness of validation labels; sparse or noisy labels obscure true separation.
- For datasets with highly imbalanced validated/all-link ratios, boxplots may compress the dynamic range; supplementary statistics (percentiles, quantile plots) are recommended.
- Visual inspection is subjective; reproducible thresholds for 'adequate separation' must be defined a priori (e.g., 90th percentile enrichment, effect size d > 1).
- The skill assesses population-level discrimination; it does not guarantee that any individual high-scoring link is correct — validation by manual inspection (e.g., MS2 peak matching) is still required.

## Evidence

- [other] Generate distributions (histograms and boxplots) comparing raw versus standardised scores for validated links versus all links across the three datasets.: "Generate distributions (histograms and boxplots) comparing raw versus standardised scores for validated links versus all links across the three datasets."
- [other] Compute mean scores and p-values (t-test) for validated links versus all links under both scoring schemes to verify standardisation improves separation.: "Compute mean scores and p-values (t-test) for validated links versus all links under both scoring schemes to verify standardisation improves separation."
- [other] The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively, demonstrating that standardisation successfully enables comparison across links with different GCF and MF sizes.: "The standardised correlation score achieves a mean of -0.0060 for all links and 3.6717 for validated links (p=6.8302 × 10−64), compared to the raw score's means of 83.5144 and 14.6667 respectively"
- [results] we examine the distribution of scores for validated links in relation to the scores for all hypothetical links: "we examine the distribution of scores for validated links in relation to the scores for all hypothetical links"
- [results] both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links: "both the IOKR and standardised strain correlation scores are significantly enriched (p-value of 0.0139 and 2.483 × 10−11, respectively) for validated links"
- [other] Reproduce S1 Fig showing raw and standardised strain correlation score distributions with validated links highlighted.: "Reproduce S1 Fig showing raw and standardised strain correlation score distributions with validated links highlighted."
