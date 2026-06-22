---
name: peak-to-formula-assignment-mapping
description: Use when when you have a fragment peak list (m/z values and intensities) from MS/MS data and need to assign candidate chemical subformulae to each peak as part of a de novo chemical formula inference pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0611
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

# peak-to-formula-assignment-mapping

## Summary

Assign chemical subformulae to fragment peaks in tandem mass spectra by enumerating valid molecular formulas within mass tolerance windows and ranking them by energy-based scoring, without relying on external fragmentation tree databases. This creates a structured peak-to-formula mapping table for use in downstream formula ranking models.

## When to use

When you have a fragment peak list (m/z values and intensities) from MS/MS data and need to assign candidate chemical subformulae to each peak as part of a de novo chemical formula inference pipeline. Apply this skill during data preprocessing when you want to avoid SIRIUS fragmentation tree computation and instead use an internal energy-based ranking approach compatible with transformer-based scoring architectures.

## When NOT to use

- Input is already a precomputed SIRIUS fragmentation tree or other external tree structure—use direct tree parsing instead.
- You require negative ionization mode support; MIST-CF's internal protocol is currently limited to positive mode adducts.
- Your mass spectrometry data has very low mass resolution (>100 ppm error); enumeration and ranking will fail due to ambiguous peak assignments.

## Inputs

- Fragment peak list (m/z values and intensities from MS/MS spectrum)
- Mass tolerance window (e.g., ppm threshold for mass accuracy)
- Chemical validity constraints (valence rules, atom count limits)

## Outputs

- Peak-to-formula mapping table (structured format with m/z, intensity, assigned subformula)
- Ranked candidate subformula list per peak (optional, for diagnostics)

## How to apply

Load the fragment peak list (m/z and intensity pairs) from input mass spectrum data. For each fragment peak, enumerate all valid chemical subformulae that fall within the specified mass tolerance window (typically a few parts-per-million for high-resolution instruments). Apply chemical validity constraints—enforce valence rules and atom count limits to filter chemically infeasible candidates. Rank the remaining candidate subformulae using an energy-based scoring function that does not reference external fragmentation trees or spectrum databases. Assign the highest-scoring subformula to each peak. Export the result as a structured table mapping each peak (m/z, intensity) to its assigned subformula. This internal protocol avoids the computational overhead of tree generation while maintaining compatibility with data-dependent learning in neural architectures.

## Related tools

- **SIRIUS** (Provides the dynamic programming algorithm (SIRIUS decomp) for enumerating all valid formulas within mass tolerance; used as reference for formula candidate space definition but not for fragmentation tree generation in this skill) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Host framework that applies the internal chemical subformula assignment protocol as part of its data preprocessing pipeline before formula transformer neural network inference) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- All assigned subformulae satisfy valence rules and atom count constraints (chemical validity).
- Each assigned subformula is the highest-ranked candidate for its peak according to the energy-based scoring function.
- The peak-to-formula mapping table has one row per input fragment peak with no missing assignments.
- Mass error between observed m/z and the monoisotopic mass of assigned subformula falls within the specified tolerance window (e.g., ±5 ppm).
- When compared against SIRIUS fragmentation trees on the same spectra, the internal protocol produces consistent or superior downstream formula ranking performance (higher top-k accuracy on held-out test data).

## Limitations

- Currently supports positive mode ionization only; negative mode adducts not yet handled.
- Energy-based scoring function performance depends on training data quality and representativeness; may underperform on instrument types or chemical classes not well represented in training.
- Enumeration of valid formulas requires sufficient mass accuracy; very-low-resolution or uncalibrated instruments will produce spurious candidates.
- The internal protocol trades off database independence against loss of empirical fragmentation knowledge that SIRIUS tree construction can provide.

## Evidence

- [other] For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window. Apply chemical validity constraints (valence rules, atom count limits) to filter candidates. Rank candidate subformulae by energy-based scoring without referencing external fragmentation trees.: "For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window. 2. Apply chemical validity constraints (valence rules, atom count limits) to filter candidates. 3."
- [other] MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage.: "MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
