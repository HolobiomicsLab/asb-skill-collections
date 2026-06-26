---
name: adduct-type-assignment-positive-mode
description: Use when you have an unknown MS/MS spectrum with a measured precursor
  m/z and want to determine which positive-mode adduct type ([M+H]+, [M+Na]+, [M+K]+,
  etc.) is most likely responsible for ionization.
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

# adduct-type-assignment-positive-mode

## Summary

Enumerate and rank multiple positive-mode adduct types ([M+H]+, [M+Na]+, [M+K]+, etc.) for unknown MS/MS precursor masses using a formula transformer neural network that scores consistency between candidate adduct–formula pairs and observed tandem mass spectra without referencing spectral databases.

## When to use

You have an unknown MS/MS spectrum with a measured precursor m/z and want to determine which positive-mode adduct type ([M+H]+, [M+Na]+, [M+K]+, etc.) is most likely responsible for ionization. This is essential when the precursor mass alone is ambiguous—multiple adduct types can produce the same observed m/z for different neutral masses—and you cannot rely on spectral database matching.

## When NOT to use

- Input spectra are from negative-mode ionization (MIST-CF currently supports positive mode only; see readme: 'Considering multiple adduct types beyond [M+H]+ (still only positive mode)').
- The neutral mass is already known or the precursor mass is unambiguous (adduct assignment becomes trivial).
- You have high-confidence spectral database matches available; database-driven approaches may be faster and equally reliable for well-characterized compounds.

## Inputs

- Mass spectrum in MGF format or m/z–intensity pairs (MS/MS precursor m/z and fragment m/z values with intensities)
- Observed precursor m/z value (in Da)
- Mass tolerance threshold for formula enumeration (e.g., 5 ppm)

## Outputs

- Ranked list of candidate adduct–formula pairs with energy-based scores
- Top-ranked adduct assignment ([M+H]+, [M+Na]+, [M+K]+, etc.)
- Inferred neutral mass corresponding to assigned adduct and formula
- Score per candidate pair (higher indicates better agreement with observed spectrum)

## How to apply

First, enumerate candidate chemical formulas for the observed precursor m/z using SIRIUS decomp, which applies a dynamic programming algorithm to generate all chemically feasible formulas within the mass tolerance. For each enumerated formula, generate candidate adduct–formula pairs spanning multiple positive-mode adduct types beyond [M+H]+ (e.g., [M+Na]+, [M+K]+, [M+NH4]+). Feed each pair into the MIST-CF formula transformer neural network, which embeds the precursor formula, fragment formulas (and their neutral losses), and adduct type as covariates, then computes an energy-based score reflecting agreement between the candidate pair and the observed MS/MS peaks. Rank candidates by descending score; the top-ranked pair indicates both the inferred neutral mass (via formula and adduct) and the most probable ionization mode. The model learns rankings in a data-dependent fashion on MS/MS training sets rather than computing fragmentation trees, allowing it to capture instrument-specific and adduct-specific fragmentation patterns.

## Related tools

- **MIST-CF** (Formula transformer neural network that scores candidate adduct–formula pairs against observed MS/MS spectra and ranks them by energy-based agreement) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Provides the dynamic programming algorithm (SIRIUS decomp) to enumerate all chemically feasible candidate formulas for a given precursor m/z)

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-ranked adduct–formula pair correctly recovers the ground-truth neutral mass (or within experimental mass error) when evaluated on a held-out test set.
- Rank-1 accuracy (fraction of spectra where true adduct is ranked first) is significantly higher than random baseline and comparable to or better than SIRIUS fragmentation-tree approach.
- Score distribution is well-separated between correct and incorrect adduct assignments (higher scores for true adduct, lower for plausible decoys).
- Model performance is consistent across instrument types (e.g., Orbitrap, Q-TOF) when model is trained on mixed instrument data.
- Few MS/MS peaks (e.g., as few as 5–10 fragments) are sufficient to discriminate adducts; performance does not collapse with sparse spectra.

## Limitations

- Negative-mode ionization is not supported; method is restricted to positive-mode adducts only.
- Model performance may degrade on proprietary high-resolution data (e.g., Orbitrap) if trained primarily on lower-resolution spectra; model trained on NIST20 library is recommended but requires commercial license.
- Adduct ranking relies on learned patterns from training data; rare or unconventional adducts absent from training will not be ranked accurately.
- Method assumes chemically valid formulas exist in the enumeration step; SIRIUS decomp may fail or be slow for very high m/z or unusual elemental compositions.
- No direct support for multiply charged ions or negative-mode adducts ([M−H]−, [M+Cl]−, etc.).

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Embedding instrument type used to measure the MS/MS as an additional model 'covariate' to help make predictions: "Embedding instrument type used to measure the MS/MS as an additional model "covariate" to help make predictions"
