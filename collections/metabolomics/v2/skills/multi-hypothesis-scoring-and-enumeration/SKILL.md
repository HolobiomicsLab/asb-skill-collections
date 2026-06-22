---
name: multi-hypothesis-scoring-and-enumeration
description: Use when when you have an unknown tandem mass spectrum (MS/MS peaks with m/z and intensity) and need to assign both the precursor chemical formula and its ionization adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - SIRIUS
  - MIST-CF formula transformer
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf_cq
schema_version: 0.2.0
---

# multi-hypothesis-scoring-and-enumeration

## Summary

Score and rank multiple candidate chemical formula–adduct pairs for an unknown tandem mass spectrum using end-to-end energy-based neural modeling, without relying on spectrum databases. This skill enumerates plausible formula and adduct hypotheses, scores each against observed fragment patterns, and returns ranked predictions with confidence signals.

## When to use

When you have an unknown tandem mass spectrum (MS/MS peaks with m/z and intensity) and need to assign both the precursor chemical formula and its ionization adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+). Apply this skill when reference spectra are unavailable, when non-protonated positive-mode adducts are likely, or when you need de novo annotation without database lookup.

## When NOT to use

- Input spectrum is already annotated with a known formula and adduct type; use this skill for discovery/validation, not for re-scoring known assignments.
- Negative-mode ionization spectra; MIST-CF currently supports positive mode only.
- MS1-only data without tandem MS/MS fragment peaks; the skill requires MS/MS fragmentation patterns to score formula–adduct hypotheses.

## Inputs

- Tandem mass spectrum (MS/MS) in MGF format with m/z, intensity, and precursor m/z
- Trained MIST-CF formula transformer model checkpoint
- List of candidate chemical formulas (enumerated from precursor m/z by SIRIUS decomp or equivalent)
- Set of plausible adduct types for positive mode ([M+H]+, [M+Na]+, [M+K]+, [M+NH4]+, etc.)

## Outputs

- Ranked list of (chemical_formula, adduct_type, score) tuples per spectrum
- Ranking metrics (rank of ground-truth adduct, recall@k)
- Per-spectrum scoring details (energy-based model scores for top candidates)

## How to apply

Load a trained MIST-CF formula transformer model and provide a test spectrum in MGF format. Enumerate candidate chemical formulas using the internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees). For each spectrum–formula pair, also enumerate plausible adduct hypotheses (expanding beyond [M+H]+ to include [M+Na]+, [M+K]+, [M+NH4]+). Score all formula–adduct combinations by computing agreement between the precursor formula candidate, the observed spectrum peaks, and their annotated fragment formulas using the learned transformer. Rank candidates by score and report top-k predictions. Compute ranking metrics (e.g., rank of ground-truth adduct, recall@k) to evaluate whether multi-adduct consideration improves accuracy over single-adduct baselines.

## Related tools

- **SIRIUS** (Enumerate candidate chemical formulas via dynamic programming (SIRIUS decomp) to generate hypothesis space for scoring; internal subformula assignment protocol is used instead of SIRIUS fragmentation trees) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF formula transformer** (Trained neural network model that scores formula–adduct pairs and ranks candidates by agreement with observed spectrum) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Ground-truth chemical formula and adduct type appear in top-k ranked predictions (recall@k metric); compare against baseline single-adduct mode to confirm multi-adduct improvement.
- Rank of ground-truth adduct is significantly lower (better) when multiple adduct types are enumerated vs. [M+H]+-only baseline.
- Score distributions for correct vs. incorrect formula–adduct pairs are well-separated and monotonically ordered by model confidence.
- Prospective validation on held-out test spectra (e.g., CASMI 2022 challenge) shows improved accuracy over SIRIUS or FFN baseline models.
- Model predictions remain stable and reproducible across multiple random seeds and data splits.

## Limitations

- Positive-mode ionization only; negative-mode adduct types ([M−H]−, [M+Cl]−, etc.) are not yet supported.
- Performance depends on availability of training data matching the instrument type (e.g., Orbitrap vs. lower-resolution instruments); models trained on NPLIB1 alone may underperform on commercial NIST20 spectra.
- Requires precursor m/z as input; cannot infer molecular weight without prior mass measurement.
- Internal subformula assignment protocol has not been benchmarked against all possible formula enumerations; some low-abundance valid formulas may be pruned during enumeration.
- Scoring relies on learned energy-based patterns; out-of-distribution spectra or rare adduct types may receive unreliable scores.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [other] Considering multiple adduct types beyond [M+H]+ in positive mode represents an advance over the original MIST model.: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] MIST-CF adopts a formula transformer neural network architecture and learns in a data-dependent fashion instead of computing fragmentation trees.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees) is an advance in the MIST-CF architecture.: "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [other] For each spectrum, run the extended adduct-assignment protocol using the internal chemical subformula assignment method to score and rank candidate adduct-formula pairs.: "For each spectrum, run the extended adduct-assignment protocol using the internal chemical subformula assignment method to score and rank candidate adduct-formula pairs."
- [other] Compute ranking metrics (e.g., rank of ground-truth adduct, recall@k) and collate results in a structured table. Compare ranking accuracy against baseline (single [M+H]+ mode) to quantify improvement from multi-adduct consideration.: "Compute ranking metrics (e.g., rank of ground-truth adduct, recall@k) and collate results in a structured table. Compare ranking accuracy against baseline (single [M+H]+ mode) to quantify improvement"
