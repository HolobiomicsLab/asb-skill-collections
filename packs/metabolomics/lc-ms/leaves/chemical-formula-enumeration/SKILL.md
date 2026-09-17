---
name: chemical-formula-enumeration
description: Use when you have an unknown MS/MS spectrum with a measured precursor
  m/z and want to generate a list of plausible chemical formula–adduct pairs to rank
  or filter downstream.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MIST-CF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- MIST-CF ranks chemical formula and adduct assignments
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-formula-enumeration

## Summary

Enumerate candidate chemical formulas for an observed MS1 precursor mass using deterministic dynamic programming, producing a ranked list of formula–adduct pairs. This step is foundational for de novo metabolite annotation from tandem mass spectra when database matching is not available or insufficient.

## When to use

Apply this skill when you have an unknown MS/MS spectrum with a measured precursor m/z and want to generate a list of plausible chemical formula–adduct pairs to rank or filter downstream. It is particularly valuable in de novo settings where no reference spectral library is available, or when the unknown metabolite is unlikely to be in existing databases.

## When NOT to use

- Input is already a curated set of known formulas from a reference library; enumeration is redundant.
- Negative-mode ionization is required; MIST-CF currently supports only positive mode adducts.
- The precursor m/z is from low-resolution or heavily noise-corrupted data where mass tolerance cannot be reliably specified.

## Inputs

- Observed MS1 precursor m/z value
- Mass spectrometry data (instrument resolution / mass tolerance specification)
- Chemical element constraints (valence rules, allowed elements)

## Outputs

- List of candidate chemical formula–adduct pairs with calculated m/z values
- Enumerated candidate set (formula string, adduct string, computed m/z)

## How to apply

Use SIRIUS's `decomp` dynamic programming algorithm to enumerate all candidate chemical formulas consistent with the observed MS1 precursor mass, typically applying chemical constraints (e.g., element valence, mass tolerance in ppm). For each candidate formula, enumerate plausible positive-mode adducts (e.g., [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+). The enumeration step does not score or rank candidates; it serves as input to downstream neural network–based scoring (e.g., MIST-CF). Typical mass tolerance is within instrumental resolution (e.g., ±5 ppm for high-resolution instruments). The output is a list of (formula, adduct, m/z_calculated) tuples; verify that the calculated m/z matches the observed precursor mass within stated tolerance.

## Related tools

- **SIRIUS** (Provides the `decomp` dynamic programming module to enumerate candidate chemical formulas from precursor mass; MIST-CF uses this instead of computing fragmentation trees.) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Consumes enumerated formula–adduct candidates and ranks them using a formula transformer neural network architecture.) — https://github.com/samgoldman97/mist-cf

## Examples

```
# Set SIRIUS environment variable and invoke the decomp algorithm
export SIRIUS_PATH=/path/to/sirius-5.5.7
${SIRIUS_PATH}/bin/sirius decomp --ionization '[M+H]+' --mz 345.1234 --ppm 5
```

## Evaluation signals

- Enumerated candidate list is non-empty and contains the true formula–adduct pair (ground truth recall).
- Calculated m/z for each candidate matches its formula and adduct identity (formula correctness).
- All candidate m/z values fall within the specified mass tolerance window (e.g., ±5 ppm) of the observed precursor.
- Candidate list size is reasonable (e.g., <1000 for typical metabolites at high resolution) to enable downstream neural network scoring without computational bottleneck.
- Enumeration does not filter or rank candidates; output is an unranked list passed to downstream scoring module.

## Limitations

- SIRIUS enumeration relies on chemical valence rules; unusual or exotic chemical structures may be missed or incorrectly scored.
- Currently supports only positive-mode adducts; negative-mode ionization is not yet supported.
- Mass tolerance specification is user-dependent and instrument-specific; too-tight tolerance may exclude true formulas; too-loose tolerance inflates candidate list size.
- Enumeration does not use spectral fragmentation information; ranking and filtering of candidates requires downstream neural network–based scoring (e.g., MIST-CF) or other scoring methods.

## Evidence

- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`, which is provided as an independent module."
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [other] Apply the internal chemical subformula assignment protocol to enumerate candidate formulas and adduct types (including [M+H]+ and other positive mode adducts).: "Apply the internal chemical subformula assignment protocol to enumerate candidate formulas and adduct types (including [M+H]+ and other positive mode adducts)."
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
