---
name: false-discovery-rate-control-in-spectral-matching
description: Use when after performing spectral library matching (whether unmodified or open modification search) and ranking candidate matches by similarity score, apply FDR control when you need to report a curated set of identifications with quantified confidence.
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
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# false-discovery-rate-control-in-spectral-matching

## Summary

Apply spectrum-level or peptide-level false discovery rate (FDR) filtering to ranked spectral library matches to distinguish true identifications from false positives while maintaining sensitivity across both unmodified and open modification searches. This skill ensures that reported peptide identifications meet a user-specified significance threshold despite the multiple-testing burden of matching thousands of query spectra against large spectral libraries.

## When to use

After performing spectral library matching (whether unmodified or open modification search) and ranking candidate matches by similarity score, apply FDR control when you need to report a curated set of identifications with quantified confidence. Specifically use this skill when: (1) query spectra have been scored against library spectra and sorted by match quality; (2) you require a principled threshold to separate true peptide identifications from spurious matches; (3) you are combining results from multiple search modalities (e.g., unmodified and modified peptide searches) and want to control error across the unified result set.

## When NOT to use

- Input is a pre-filtered, already-FDR-controlled list of identifications from another tool (applying FDR twice risks over-correction).
- Your spectral library lacks a decoy or reverse-sequence counterpart; FDR estimation requires a calibrated null model.
- Query spectra have not yet been scored against library candidates; FDR control requires a ranked score distribution to work meaningfully.

## Inputs

- Ranked list of spectral library matches with similarity scores (from cascade search: unmodified and open modification candidates)
- Target spectral library (with or without decoy sequences)
- Query spectrum dataset
- Decoy spectral library or decoy-augmented library (reverse or shuffled peptide sequences)

## Outputs

- FDR-filtered list of identified spectra with assigned q-values
- Identified peptide sequences with spectrum-level or peptide-level FDR assignments
- Score-to-FDR mapping (threshold curve)
- Summary statistics: number of identifications at target FDR threshold

## How to apply

After cascade search has scored and ranked all candidate matches (both unmodified and modified), sort matches by descending similarity score. Apply target-decoy analysis by computing the FDR as the ratio of decoy (reverse or shuffled) matches to target matches at each score threshold. Select the score cutoff that achieves your target FDR level (commonly 1% or 5% at either spectrum or peptide level). Assign each query spectrum or unique peptide an empirical q-value (adjusted p-value) based on its rank and the decoy hit rate observed at that score level. Report only matches falling below your FDR threshold, along with their assigned q-values. The rationale is that decoy matches approximate the null distribution of random similarity scores, so the ratio of decoys to targets at a given score threshold estimates the false discovery rate in the target matches at that threshold.

## Related tools

- **ANN-SoLo** (Spectral library search engine that performs cascade search and ranking of unmodified and open modification candidates, outputs ranked scores for downstream FDR filtering) — https://github.com/bittremieux/ANN-SoLo

## Evaluation signals

- Verify that the number of decoy matches reported at the chosen score threshold is consistent with the claimed FDR (e.g., at 1% FDR, decoy count ÷ target count ≈ 0.01).
- Check that q-values are non-decreasing with ascending rank (monotonicity property of empirical q-value computation).
- Confirm that sensitivity is preserved: when FDR threshold is relaxed (e.g., 1% → 5%), the number of identifications increases monotonically.
- Validate that the score cutoff is justified: inspect the score distribution of decoy vs. target matches to ensure they are well-separated and the threshold is not in a region of high overlap.
- Cross-check with an independent FDR calculator (e.g., spectrum_utils or Percolator) on a subset of results to ensure consistency.

## Limitations

- FDR control assumes that decoy sequences behave as a realistic null model; if decoys are not representative of true random matches (e.g., decoy sequences are too similar to targets), FDR estimates will be inaccurate.
- The method is sensitive to the scoring metric and library composition; cascade search must provide well-calibrated scores for FDR thresholds to be reliable across diverse peptides and modification states.
- Applying FDR control separately to unmodified and modified search results may lead to different error rates in each subset; unified FDR control across modalities is preferred but requires careful ranking.
- Python 3.6–3.9 required for ANN-SoLo; Python 3.10+ not currently supported (per README).

## Evidence

- [intro] Cascade search strategy combined to maximize identified unmodified and modified spectra while strictly controlling false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] Rank all identified matches and apply FDR control via spectrum-level or peptide-level FDR filtering: "Rank all identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering."
- [intro] Shifted dot product score sensitively matches modified spectra to unmodified counterparts: "and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
