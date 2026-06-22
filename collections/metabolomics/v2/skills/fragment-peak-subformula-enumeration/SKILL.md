---
name: fragment-peak-subformula-enumeration
description: Use when you have a list of fragment peak m/z values and intensities from tandem MS/MS data and need to assign chemical subformulae to each peak for downstream formula ranking or structure inference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - SIRIUS
  - MIST-CF
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

# fragment-peak-subformula-enumeration

## Summary

Enumerate and rank all chemically valid molecular subformulae for each observed fragment peak in a tandem mass spectrum without relying on external fragmentation tree databases. This skill assigns chemical subformulae to fragment m/z values using energy-based scoring and chemical validity constraints, enabling de novo metabolite characterization.

## When to use

Apply this skill when you have a list of fragment peak m/z values and intensities from tandem MS/MS data and need to assign chemical subformulae to each peak for downstream formula ranking or structure inference. This is particularly useful in a de novo setting where spectrum database matching is unavailable or when you want to avoid dependency on pre-computed fragmentation trees (e.g., SIRIUS trees). Use this as a preprocessing step prior to neural network–based formula ranking.

## When NOT to use

- Input is already a pre-computed fragmentation tree (e.g., from SIRIUS) — use tree-based assignment methods instead.
- Fragment peaks lack sufficient mass accuracy (>> 50 ppm error on low-resolution instruments) — enumeration tolerance windows will be too large to rank candidates reliably.
- You require negative ionization mode support — MIST-CF's internal protocol (as of this publication) supports only positive mode adducts.

## Inputs

- fragment peak list (m/z values and intensities from tandem MS/MS spectrum)
- mass tolerance threshold (ppm or Da)
- chemical constraint parameters (valence rules, atom count limits)

## Outputs

- peak-to-subformula mapping table (structured assignment of chemical subformulae to each fragment m/z)
- scored candidate subformulae per peak (ranked by energy-based score)

## How to apply

For each fragment peak in the observed spectrum: (1) Define a mass tolerance window around the observed m/z value (typical tolerance depends on instrument resolution, e.g., ppm error). (2) Enumerate all valid chemical subformulae whose monoisotopic mass falls within this window using exhaustive formula decomposition (SIRIUS's dynamic programming decomposition algorithm provides efficient enumeration). (3) Filter candidate subformulae by applying chemical validity constraints: valence rules (e.g., carbon tetravalency, oxygen divalency), atom count limits (e.g., no more than 50 carbons in a typical small-molecule fragment), and common chemical plausibility heuristics. (4) Score each surviving candidate using energy-based modeling (e.g., fragmentation energy, bond dissociation patterns) without referencing external fragmentation databases. (5) Assign the highest-scoring subformula to each peak. (6) Compile assignments into a structured peak-to-formula mapping table for downstream processing. The rationale is that chemical validity constraints dramatically reduce the combinatorial explosion of candidate formulae, and energy-based scoring ranks them without requiring pre-computed spectral libraries or fragmentation tree databases.

## Related tools

- **SIRIUS** (Provides dynamic programming decomposition algorithm (SIRIUS decomp) for efficient formula enumeration within a mass tolerance window; used to generate candidate subformulae before filtering and scoring) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Implementation framework that applies this internal subformula assignment protocol as an alternative to SIRIUS fragmentation trees, feeding enumerated and ranked subformulae into a formula transformer neural network for ranking chemical formulae) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- Peak-to-formula mapping table is complete (every fragment peak has ≥ 1 assigned subformula) and matches the total number of input peaks.
- All assigned subformulae satisfy chemical validity constraints: valence rules hold (e.g., C4, O2, N3), atom counts are within reasonable bounds, and molecular weight is within the specified mass tolerance of the observed m/z.
- Energy-based scores for assigned subformulae are monotonically ranked (highest score per peak), and scores are numerically stable (no NaNs or infinities).
- Downstream neural network ranking (e.g., via MIST-CF's formula transformer) achieves expected accuracy (e.g., top-1 or top-10 chemical formula recovery) on validation/test spectra, indicating that subformula assignments improve convergence.
- Comparison with SIRIUS fragmentation tree assignments on the same spectrum shows consistency in high-confidence peaks (e.g., Kendall τ correlation > 0.8 on top-scored formulae per peak) while eliminating database dependency.

## Limitations

- Currently supports positive ionization mode only; negative mode not yet implemented.
- Relies on SIRIUS for efficient formula enumeration; without it, brute-force enumeration on large mass windows becomes combinatorially expensive.
- Energy-based scoring is heuristic and may not capture all fragmentation mechanisms; performance depends on quality of the underlying energy model and training data distribution.
- Mass accuracy requirements (typically << 50 ppm) mean that lower-resolution or miscalibrated instruments will produce wider tolerance windows and higher candidate ambiguity.
- Adduct type diversity is limited (supports multiple positive-mode adducts like [M+H]+, [M+Na]+, but not negative or exotic adducts).

## Evidence

- [other] For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window.: "For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window."
- [other] Apply chemical validity constraints (valence rules, atom count limits) to filter candidates.: "Apply chemical validity constraints (valence rules, atom count limits) to filter candidates."
- [other] Rank candidate subformulae by energy-based scoring without referencing external fragmentation trees.: "Rank candidate subformulae by energy-based scoring without referencing external fragmentation trees."
- [other] MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage.: "MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`, which is provided as an independent module.: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`, which is provided as an independent module."
- [other] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [other] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
