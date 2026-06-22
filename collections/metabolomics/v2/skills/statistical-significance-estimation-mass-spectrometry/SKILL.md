---
name: statistical-significance-estimation-mass-spectrometry
description: Use when after aligning fragment ions between two tandem mass spectra (query and reference) using maximum weight matching and you need to assign confidence scores to the matched ion pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0591
  tools:
  - SIMILE
  - Python
derived_from:
- doi: 10.1038/s41467-022-30118-9
  title: SIMILE
evidence_spans:
- SIMILE (Significant Interrelation of MS/MS Ions via Laplacian Embedding) is a Python library
- is a Python library for interrelating fragmentation spectra with significance estimation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_simile_cq
    doi: 10.1038/s41467-022-30118-9
    title: SIMILE
  dedup_kept_from: coll_simile_cq
schema_version: 0.2.0
---

# statistical-significance-estimation-mass-spectrometry

## Summary

Estimate statistical significance of fragment ion matches between tandem mass spectra using a null distribution generated from intraspectral comparisons. This skill enables confident identification of true spectral similarity by computing p-values that account for the stochastic properties of the fragmentation process.

## When to use

Apply this skill after aligning fragment ions between two tandem mass spectra (query and reference) using maximum weight matching and you need to assign confidence scores to the matched ion pairs. Use it when you have precursor m/z values, fragment ion peaks with intensities, and mass difference frequencies across the spectra, and you want to distinguish true spectral relationships from random coincidental matches.

## When NOT to use

- You have only a single spectrum or fewer than two spectra to compare—significance estimation requires pairwise comparisons
- Your fragment ion peaks are not pre-aligned or you lack mass difference information—the z-test depends on the similarity matrix and matching matrix as inputs
- You are analyzing spectra from unrelated chemical compounds with no expectation of shared fragment ions—the null distribution assumes a shared fragmentation mechanism

## Inputs

- Precursor m/z values for query and reference spectra
- Fragment ion m/z and intensity values for each spectrum
- Similarity matrix computed from fragment ion mass differences
- Maximum weight matching matrix from fragment ion alignment
- Symmetric/asymmetric comparison matrix (pro/con matches)

## Outputs

- Statistical significance scores (z-scores) for each spectrum pair
- P-values for matched fragment ion pairs
- Null distribution of expected similarity scores
- Matching ions report with mass deltas, scores, and p-values

## How to apply

After constructing a similarity matrix from fragment ion mass differences and computing maximum weight matching between spectra, generate a null distribution by permuting intra- and inter-spectral fragment similarity scores. Apply a z-test that compares the observed matched fragment ion scores against this null distribution, leveraging the asymmetry of the SIMILE max weight matrix to generate p-values for each spectrum pair. The resulting p-value quantifies the likelihood that matched fragment ions are siblings (related by the fragmentation process) rather than random alignments. Compute multiple comparison statistics when analyzing more than two spectra to account for multiple testing.

## Related tools

- **SIMILE** (Python library that computes similarity matrices, maximum weight matching, and z-test for significance estimation of fragment ion relationships) — https://github.com/biorack/simile
- **Python** (Programming environment for running SIMILE statistical calculations and hypothesis testing)

## Examples

```
spec_scores, pval, null_dist = sml.z_test(S, M, C, spec_ids, return_dist=True, log_size=5)
```

## Evaluation signals

- P-values are distributed between 0 and 1 and reflect the expected Type I error rate under the null hypothesis
- Matched ion pairs with p < 0.05 (or other chosen alpha threshold) have higher observed similarity scores than expected by chance
- Symmetric matches (reciprocal alignments between spectra) receive lower (more significant) p-values than asymmetric matches
- The null distribution shape matches the observed distribution of fragment ion similarity scores within individual spectra
- Spectra with known chemical relationships yield lower p-values than unrelated spectrum pairs

## Limitations

- The null distribution relies on intra- and inter-spectral similarity score permutations; results are sensitive to the choice of mass tolerance and transition matrix construction
- Performance depends on fragment ion diversity and abundance patterns; spectra with few or highly redundant mass differences may have unreliable null distributions
- Multiple comparison statistics are required when testing many spectrum pairs, which may reduce statistical power or require stricter significance thresholds
- The method assumes that fragmentation follows a Markovian process where fragment relationships can be modeled as random walks on a transition graph; violation of this assumption may invalidate p-values

## Evidence

- [readme] A null distribution for spectral similarity which leverages intraspectral comparisons to add confidence to interspectral comparisons: "A null distribution for spectral similarity which leverages intraspectral comparisons to add confidence to interspectral comparisons."
- [readme] Calculate significance of max weight matching between fragment ions for all combination of spectra: "Calculate significance of max weight matching between fragment ions for all combination of spectra"
- [readme] By leveraging SIMILE's fragment ion similarity measure which conforms to this analogy, we can ask how likely it is that the fragment ions matched up between fragmentation spectra by SIMILE are siblings. Taking this line of reasoning to its natural conclusion yields a null distibution generated by permuting intra and inter spectral fragment similarity scores to yield p-values.: "yields a null distibution generated by permuting intra and inter spectral fragment similarity scores to yield p-values"
- [other] Extract matched ion pairs, compute mass deltas (m/z differences), and calculate statistical significance scores for each match: "Extract matched ion pairs, compute mass deltas (m/z differences), and calculate statistical significance scores for each match."
- [readme] MUCH faster mass delta counting and significance testing: "MUCH faster mass delta counting and significance testing"
