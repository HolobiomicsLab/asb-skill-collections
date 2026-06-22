---
name: false-discovery-rate-control
description: Use when you have generated candidate peptide-spectrum matches from a spectral library search (especially open modification searches using cascade strategies) and need to assign statistical confidence to those matches. Use it whenever the scoring metric (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
schema_version: 0.2.0
---

# false-discovery-rate-control

## Summary

A statistical filtering strategy applied after spectral library searching to control the proportion of false positive peptide-spectrum matches (PSMs) while maximizing sensitivity of identification. FDR control is essential in open modification searching where shifted dot product scoring alone cannot reliably distinguish true matches from random matches across the modified mass space.

## When to use

Apply this skill when you have generated candidate peptide-spectrum matches from a spectral library search (especially open modification searches using cascade strategies) and need to assign statistical confidence to those matches. Use it whenever the scoring metric (e.g., shifted dot product) alone is insufficient to guarantee match validity, or when you need to report results with a bounded false positive rate (e.g., '1% FDR' means ≤1% of reported PSMs are expected to be incorrect).

## When NOT to use

- Input PSMs already have independently validated confidence scores from orthogonal methods (e.g., isotope labeling, complementary MS/MS fragmentation); FDR control assumes scores are the only confidence metric.
- Library size is extremely small (<100 unique sequences); decoy generation and target-decoy ratio estimation become unreliable.
- You are working with closed-modification searches where the search space is small and false match rates are negligible; simpler filtering by score threshold may suffice.

## Inputs

- Candidate peptide-spectrum matches with assigned scores (e.g., shifted dot product scores)
- Target spectral library (original sequences)
- Decoy spectral library (reversed or shuffled sequences, same size as target)

## Outputs

- Filtered set of high-confidence peptide-spectrum matches
- FDR-corrected score threshold applied
- Per-PSM FDR q-value or posterior error probability (optional)

## How to apply

After executing the cascade search strategy and computing shifted dot product scores for all candidate PSMs, apply target-decoy FDR control: (1) generate decoy spectra by reversing or shuffling the library sequences; (2) score both target and decoy PSMs using the same scoring function; (3) sort all PSMs by score and compute the ratio of decoys to targets at each score threshold; (4) select the threshold where (number of decoy PSMs) / (number of target PSMs) ≤ target FDR level (commonly 0.01 for 1% FDR); (5) report only target PSMs that exceed this threshold. This approach controls the expected proportion of false positives in the reported result set while preserving the highest-scoring true identifications.

## Related tools

- **ANN-SoLo** (Spectral library search engine that integrates FDR control as a filtering step after cascade search and shifted dot product scoring to produce confidence-filtered PSM output) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- Verify that the number of reported PSMs at 1% FDR is approximately 99% of the total matches passing the threshold (i.e., ≤1% decoy-to-target ratio).
- Confirm that decoy PSM count never exceeds target PSM count at any score threshold in the filtered set (monotonic FDR constraint).
- Check that high-confidence matches (e.g., cosine similarity > 0.8) are retained while borderline matches (cosine < 0.6) are filtered, indicating score-dependent filtering is working.
- Validate that known positive controls (e.g., reference peptides with confirmed modifications) appear in the filtered set; absence suggests over-filtering.
- Cross-check reported identifications against external databases (e.g., PTMiner, PhosphoSitePlus for post-translational modifications) to confirm false positive rate is consistent with claimed FDR level.

## Limitations

- FDR control assumes decoy and target PSMs are generated and scored identically; bias in decoy generation (e.g., non-random shuffling) can inflate or deflate estimated FDR.
- In open modification searches, the effective search space is much larger than closed searches; FDR thresholds may need to be more stringent (e.g., 0.5% FDR instead of 1%) to achieve equivalent error rates in absolute terms.
- Target-decoy FDR control estimates average false positive rate across the result set but does not provide per-peptide confidence; some individual matches may have higher error probability than the global FDR.
- Small sample sizes or sparse peptide databases can lead to unstable FDR estimation near the threshold boundary.

## Evidence

- [readme] cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [intro] ANN-SoLo uses approximate nearest neighbor indexing combined with cascade search to control false discovery rate: "combined with a cascade search strategy to maximize identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] FDR control is applied after scoring as a filtering step: "Apply false discovery rate control to filter identifications and produce the final peptide-spectrum match output"
