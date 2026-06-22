---
name: gcf-mf-link-scoring-computation
description: Use when you have paired GCF and MF datasets with strain membership information and need to rank candidate GCF–MF links to identify which biosynthetic gene clusters likely produce detected metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2814
  tools:
  - NumPy or SciPy
  - Python
  - NPLinker
  - antiSMASH
  - BiG-SCAPE
  - GNPS
  - MIBiG
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- follows the hypergeometric distribution as previously stated
- NPLinker, a Python module to accelerate and support the process of automatically linking GCFs
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker_cq
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker_cq
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

# GCF-MF Link Scoring Computation

## Summary

Computes standardised strain correlation scores and IOKR scores for Gene Cluster Family (GCF) to Metabolite Feature (MF) links, then combines them into a unified ranking to prioritise true genomic–metabolomic associations. This skill addresses the inability of raw strain correlation scores to be reliably compared across links of different sizes by standardising via hypergeometric null-model normalisation.

## When to use

Apply this skill when you have paired GCF and MF datasets with strain membership information and need to rank candidate GCF–MF links to identify which biosynthetic gene clusters likely produce detected metabolites. Use it specifically when raw strain correlation scores show high variance across links of different sizes, making direct score comparison unreliable, or when you want to combine orthogonal scoring signals (strain overlap and spectral similarity) to increase confidence in link predictions.

## When NOT to use

- Input GCF–MF links already have comparable, pre-standardised scores across all link sizes—skip standardisation and proceed directly to IOKR scoring and combination.
- Strain metadata is absent, incomplete, or unreliable—raw strain overlap cannot be computed, so hypergeometric standardisation cannot be applied; consider IOKR scoring alone.
- BGCs in the dataset show minimal homology to MIBiG reference sequences—IOKR relies on MIBiG homology assignment and will have reduced discriminative power.

## Inputs

- GCF strain-set membership data (sets G, population size N)
- MF strain-set membership data (sets M)
- Raw strain correlation scores (four-term rule applied to each GCF–MF pair)
- IOKR scores for GCF–MF pairs (computed from spectral fingerprint similarity to MIBiG reference BGCs)
- Molecular fingerprints and training spectra from GNPS or MIBiG

## Outputs

- Table with GCF ID, MF ID, raw strain correlation score, hypergeometric expected value, variance, and standardised strain correlation score
- Table with GCF ID, MF ID, and standardised IOKR score
- Ranked list of GCF–MF links sorted by combined score (ℓ_p norm)
- Filtered subset of top-scoring links (e.g., above 90th percentile on both scores) enriched for validated associations

## How to apply

First, compute raw strain correlation scores for each GCF–MF pair using the four-term scoring rule: +10 if a strain produces the metabolite AND has the BGC; −10 if it produces the metabolite but lacks the BGC; +1 if it neither produces nor has the BGC; 0 otherwise. Next, standardise these raw scores by calculating the hypergeometric expected value E[σ_corr(M, G)] and variance Var[σ_corr(M, G)] based on the null hypothesis that strain overlap follows a hypergeometric distribution with population size N, GCF size g, MF size m, and observed overlap o. Compute the standardised score as s*_corr = (σ_corr − E[σ_corr]) / √Var[σ_corr] for each link. In parallel, score links using IOKR (a feature-based method independent of product class) and standardise IOKR scores using the same z-score transformation. Finally, combine the two standardised scores using an ℓ_p norm with sign preservation (e.g., s_sum = sgn(s_corr)|s_corr|^p + sgn(s_IOKR)|s_IOKR|^p with p = 0.5) to produce a unified ranking. Filter the top-scoring links (e.g., 90th percentile on both scores) for validation and prioritisation.

## Related tools

- **NPLinker** (Framework that integrates the strain correlation and IOKR scoring functions and performs GCF–MF link ranking and validation) — https://github.com/sdrogers/nplinker
- **antiSMASH** (Detects BGCs from microbial genomes; outputs are clustered into GCFs used for strain membership assignment)
- **BiG-SCAPE** (Clusters predicted BGCs into Gene Cluster Families (GCFs); output GCFs are then scored for links to metabolite features)
- **GNPS** (Public repository of MS2 spectra and molecular networking; spectra are used to compute IOKR scores and train fingerprint models)
- **MIBiG** (Reference database of characterised microbial BGCs; used for IOKR training and molecular fingerprint assignment to query BGCs)
- **NumPy or SciPy** (Compute hypergeometric expected value, variance, and standardised scores; perform ℓ_p norm calculations)

## Examples

```
import numpy as np; from scipy.stats import hypergeom; raw_scores = [...]; N, g, m, o = ...; p_o = hypergeom.pmf(range(o+1), N, g, m); E_score = sum([hypergeom.pmf(k, N, g, m) * score_func(k) for k in range(o+1)]); E_score2 = sum([hypergeom.pmf(k, N, g, m) * score_func(k)**2 for k in range(o+1)]); var_score = E_score2 - E_score**2; std_score = (raw_scores - E_score) / np.sqrt(var_score)
```

## Evaluation signals

- Standardised strain correlation scores for validated links have a significantly higher mean than for all links (article reports 3.672 vs. −0.006, p = 6.8 × 10−64), confirming enrichment.
- Standardised IOKR scores likewise show enrichment for validated links with p < 0.05, confirming that standardisation preserves discriminative information.
- Combined score (ℓ_p norm) assigns the best rank to the validated link in ≥50% of test cases (article: 10 out of 15 validated links).
- Links scoring above the 90th percentile on both standardised scores are significantly enriched for validated pairs (p < 0.01) compared to links exceeding either score individually.
- Hypergeometric expected value and variance are finite and positive for all links; standardised scores do not contain NaN or infinite values.

## Limitations

- Standardised strain correlation still cannot distinguish between links showing identical strain presence/absence patterns, limiting its ability to rank correlated but structurally distinct metabolites.
- IOKR is restricted to BGCs showing considerable homology to MIBiG; novel BGCs with no close homologues cannot be reliably scored via molecular fingerprint assignment.
- IOKR performance is highly sensitive to kernel function and parameter choice (e.g., choice of molecular fingerprint substructures), and these dependencies are not fully characterised; requires empirical tuning.
- Combined ℓ_p norm requires choice of exponent p (e.g., p = 0.5); optimal p is data-dependent and not theoretically derived.
- Low absolute top-n accuracy of IOKR alone (top-1: 0.121; top-5: 0.171) means IOKR ranking is weak without strain correlation complementation; biased towards small test sets.

## Evidence

- [other] The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)]: "The standardised strain correlation score is computed by subtracting the hypergeometric expected value E[σ_corr(M,G)] from the raw score and dividing by the variance Var[σ_corr(M,G)]"
- [other] For each GCF-MF link, compute the raw strain correlation score using the four-term rule: +10 if strain produces metabolite AND has BGC; −10 if strain produces metabolite but lacks BGC; +1 if strain neither produces nor has BGC; 0 otherwise: "compute the raw strain correlation score using the four-term rule: +10 if strain produces metabolite AND has BGC; −10 if strain produces metabolite but lacks BGC; +1 if strain neither produces nor"
- [abstract] the most popular strain correlation score has properties that make it impossible to reliably compare score values across links: "the most popular strain correlation score has properties that make it impossible to reliably compare score values across links"
- [results] Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links: "Standardising the score gives a mean score of -0.006 for all links, and 3.672 for validated links"
- [results] Our combined scoring function is therefore s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|: "Our combined scoring function is therefore s_sum = sgn(s_corr)|s_corr| + sgn(s_IOKR)|s_IOKR|"
- [abstract] we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance over either of the individual approaches: "we introduce a method for combining their scores into a single scoring function for genomic and metabolomic links, which shows improved performance"
- [discussion] IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures: "IOKR is also highly dependent on the choice of both kernel function and parameters, as the molecular fingerprints denote particular substructures"
- [discussion] A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which is needed to compute the molecular fingerprint. This restricts its use to: "A drawback of the current IOKR scoring method is its reliance on MIBiG homology to assign molecular structures to BGCs, which restricts its use"
