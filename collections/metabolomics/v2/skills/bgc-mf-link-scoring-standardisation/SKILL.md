---
name: bgc-mf-link-scoring-standardisation
description: Use when you have computed raw strain correlation scores and IOKR scores for the same set of GCF–MF (gene cluster family–molecular feature) pairs, and you want to compare or combine them fairly without one score dominating due to scale differences.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_3371
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# BGC–MF Link Scoring Standardisation

## Summary

Standardise raw strain correlation and IOKR scores for genomic-metabolomic (BGC–MF) links to enable fair comparison across heterogeneous scoring functions and improve enrichment of validated links. This skill transforms incomparable raw scores into z-score equivalents using hypergeometric null distributions, making it possible to combine them into a single ranking function.

## When to use

You have computed raw strain correlation scores and IOKR scores for the same set of GCF–MF (gene cluster family–molecular feature) pairs, and you want to compare or combine them fairly without one score dominating due to scale differences. Apply this when you observe that raw correlation scores span orders of magnitude (e.g. 0–100) while IOKR scores cluster near 0 (e.g. 0–0.05), and you need a unified metric to rank candidate links or filter by joint percentile thresholds.

## When NOT to use

- You have only one scoring function and no intention to combine scores; standardisation is unnecessary overhead.
- Your raw scores are already on comparable scales (e.g. both log-transformed or both in 0–1 range); compare them directly via percentile filtering before standardising.
- You lack a high-quality ground truth of validated links; standardisation assumes the null distribution is correct, but validation requires independent confirmation of enrichment.

## Inputs

- Raw strain correlation scores (σ_corr) for all GCF–MF pairs
- Raw IOKR scores (σ_IOKR) for all GCF–MF pairs
- Strain co-occurrence matrix or hypergeometric parameters (expected value and variance for correlation null distribution)
- IOKR score distribution statistics (mean and variance across all candidate pairs)
- Set of known validated links (ground truth from Paired Omics Data Platform or MIBiG–GNPS curated correspondence)

## Outputs

- Standardised strain correlation scores (σ*_corr) for all GCF–MF pairs
- Standardised IOKR scores (σ*_IOKR) for all GCF–MF pairs
- Combined composite scores (e.g. sgn(s'_corr)|s'_corr|^0.5 + sgn(s'_IOKR)|s'_IOKR|^0.5) for all GCF–MF pairs
- Ranked and percentile-filtered link tables (at 90th percentile threshold, independently and jointly)
- Enrichment statistics (proportion of validated links per score group, p-values from Fisher exact test)

## How to apply

For each scoring function independently, compute the expected value and variance under the null distribution: for strain correlation, use a hypergeometric null model over all possible strain co-occurrence patterns; for IOKR, calculate expected value and variance across all candidate BGC–spectrum pairs in the dataset. Then standardise each raw score as σ* = (σ − E[σ]) / √Var(σ), where σ is the raw score. This produces standardised scores (σ*_corr and σ*_IOKR) that are comparable on the same scale and can be combined using an ℓp-norm function (e.g. sgn(s'_corr)|s'_corr|^0.5 + sgn(s'_IOKR)|s'_IOKR|^0.5). Validate the standardisation by checking that validated links have significantly higher mean standardised scores than random links (use t-test or Mann–Whitney U), and confirm that filtering links above the 90th percentile for both standardised scores jointly increases the proportion of validated links compared to filtering by either score alone.

## Related tools

- **NPLinker** (Framework implementing strain correlation and IOKR scoring and standardisation for BGC–MF linking) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects BGCs in microbial genomes; output clusters are grouped by BiG-SCAPE into GCFs that form the genomic side of the GCF–MF pairs)
- **BiG-SCAPE** (Clusters BGCs into GCFs (gene cluster families) used in strain correlation and IOKR score computation)

## Evaluation signals

- Standardised scores for validated links have significantly higher mean (or median) than scores for all hypothetical links, confirmed by t-test or Mann–Whitney U at p < 0.001
- After standardisation, σ*_corr and σ*_IOKR have similar distributional properties (e.g. comparable range, symmetry, or kurtosis), enabling fair visual and statistical comparison
- Links filtered at the joint 90th percentile (both σ*_corr > 90th AND σ*_IOKR > 90th) show ≥2-fold enrichment of validated links compared to either individual scoring function alone, and p-value < 0.01 (Fisher exact test)
- Composite score distribution (e.g. via ℓp-norm combination) shows monotonic increase in enrichment (proportion of validated links) as composite score increases, across decile or percentile bins
- Expected value and variance calculations are reproducible: recomputing from the same raw score distributions yields identical standardised scores to ≥6 decimal places

## Limitations

- Standardisation assumes the null distribution (hypergeometric for correlation, empirical for IOKR) is accurate; misspecification of the null model will bias standardised scores.
- IOKR scores depend strongly on the choice of molecular fingerprint and kernel function; different fingerprints yield non-comparable IOKR distributions, requiring re-standardisation for each fingerprint choice.
- IOKR scores can only be computed for BGCs with considerable homology to MIBiG entries; BGCs novel or distant from known structures will have poor or no IOKR ranking, limiting applicability of the combined score in discovery settings.
- Performance breakdown by natural product compound class is difficult due to insufficient test set size for each class, so standardisation improvements may not generalise equally across all chemical classes.
- Strain correlation relies on shared strain co-occurrence; in single-strain datasets or datasets with sparse sampling, strain correlation scores will be uninformative, and the combined score will depend almost entirely on IOKR.

## Evidence

- [methods] hypergeometric null distribution with expected value and variance adjustment: "Compute raw and standardised strain correlation scores (σ_corr and σ*_corr) for each GCF-MF pair using hypergeometric null distribution with expected value and variance adjustment."
- [abstract] standardised scores enable comparison across scoring functions: "Based on standardising a commonly used score, we introduce a new, more effective score"
- [results] joint percentile filtering shows synergy between scores: "Links scoring above the 90th percentile for both standardised strain correlation and IOKR scores show significantly higher enrichment for validated links (p=2.633×10−4 from IOKR and p=0.0208 from"
- [results] standardisation improves discriminative power: "Standardised correlation: -0.0060 (all), 3.6717 (validated), p-value 6.8302 × 10−64"
- [results] combining standardised scores via ℓp-norm: "Our combined scoring function is: s'1/2 = sgn(s'corr)|s'corr|1/2 + sgn(s'IOKR)|s'IOKR|1/2"
- [discussion] IOKR dependence on fingerprint and kernel choice: "IOKR is also highly dependent on the choice of both kernel function and molecular fingerprints"
- [discussion] IOKR limitation to MIBiG-homologous BGCs: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the"
