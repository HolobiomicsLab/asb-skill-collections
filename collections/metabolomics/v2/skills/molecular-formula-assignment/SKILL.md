---
name: molecular-formula-assignment
description: 'Use when you have acquired MS/MS spectra (in MGF format with required fields: TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) from known or unknown compounds and need to predict their molecular formulas with ranked candidates and confidence scores.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0718
  - http://edamontology.org/topic_3172
  tools:
  - FIDDLE
  - msfiddle
  - BUDDY
  - SIRIUS
derived_from:
- doi: 10.1038/s41467-025-66060-9
  title: fiddle
evidence_spans:
- FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fiddle_cq
    doi: 10.1038/s41467-025-66060-9
    title: fiddle
  dedup_kept_from: coll_fiddle_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-66060-9
  all_source_dois:
  - 10.1038/s41467-025-66060-9
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-assignment

## Summary

Use a deep learning rescore model to assign and rank molecular formula candidates from tandem MS/MS spectra, leveraging a redesigned Siamese architecture to generate confidence-scored formula predictions with standardized output columns.

## When to use

You have acquired MS/MS spectra (in MGF format with required fields: TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) from known or unknown compounds and need to predict their molecular formulas with ranked candidates and confidence scores. This is essential when you want to move beyond a single formula prediction to a ranked set of candidates with rescore confidence values suitable for downstream structural elucidation.

## When NOT to use

- Input spectra lack required MGF metadata fields (TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY) — the pipeline will fail or produce invalid predictions.
- You need only a single best-guess formula, not a ranked candidate list — this skill's primary value is in multi-candidate ranking and rescoring; single-formula use cases do not leverage the rescore model.
- Spectra are from an instrument type not represented in the pre-trained model checkpoints (currently orbitrap or qtof only) — performance on novel instrument types is not validated.

## Inputs

- MGF file (tandem mass spectra with TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, COLLISION_ENERGY fields)
- Precursor m/z and adduct type [M+H]+ or [M-H]- for neutral mass calculation
- Collision energy value (numeric or 'Unknown')
- Instrument type indicator (orbitrap or qtof)

## Outputs

- CSV table with one row per spectrum including: ID, Mass, Pred Formula, Pred Mass, Refined Formula (0..4), Refined Mass (0..4), Rescore (0..4) confidence scores
- Ranked list of candidate molecular formulas per spectrum with associated confidence scores

## How to apply

Load your MS/MS spectra via the msfiddle Python API or CLI, specifying the appropriate instrument type (orbitrap or qtof). Execute the FIDDLE v2.0.0 two-stage pipeline: (1) the TCN formula prediction model generates an initial candidate set, and (2) the Siamese-architecture rescore model re-ranks these candidates and assigns confidence scores (Rescore k columns) to each ranked formula. Extract the ranked output with standardized column naming (e.g., 'Refined Formula (0..4)', 'Rescore (0..4)') and export to CSV. The rescore model's Siamese architecture is specifically designed to learn pairwise comparisons between candidates, improving discrimination of correct formulas in competitive ranking scenarios.

## Related tools

- **FIDDLE** (Main deep learning framework providing the two-stage TCN formula prediction and Siamese-architecture rescore model for MS/MS spectral inference and formula ranking) — https://github.com/JosieHong/FIDDLE
- **msfiddle** (PyPI package wrapper providing CLI and Python API for streamlined access to FIDDLE pre-trained models without full research codebase setup) — https://github.com/josiehong/msfiddle
- **BUDDY** (Optional external tool for generating candidate formula sets that can be integrated into FIDDLE rescoring workflow via buddy_path parameter) — https://github.com/Philipbear/msbuddy
- **SIRIUS** (Optional external tool for generating candidate formula sets that can be integrated into FIDDLE rescoring workflow via sirius_path parameter) — https://v6.docs.sirius-ms.io/

## Examples

```
msfiddle --test_data /path/to/caffeine.mgf --instrument_type orbitrap --result_path /path/to/output_formulas.csv --device 0
```

## Evaluation signals

- Output CSV contains exactly one row per input spectrum with no missing values in ID, Mass, Pred Formula, and Rescore (0..4) columns.
- Rescore confidence scores range between 0 and 1 and are monotonically decreasing across Rescore (0) to Rescore (4) for each spectrum.
- Refined Formula (0..4) columns contain valid chemical formulas (non-empty strings with standard element symbols and counts).
- Refined Mass (0..4) values match the calculated neutral mass within expected measurement error (~5 ppm for orbitrap, ~10 ppm for qtof).
- Pred Mass and Refined Mass (0) are identical or very close, confirming that the top-ranked refined candidate is consistent with the neural model's initial prediction.

## Limitations

- Pre-trained checkpoints are limited to orbitrap and qtof instruments; performance on other instrument types (e.g., ion trap, MALDI) is not validated.
- Model predictions assume the precursor ion mass-to-charge and adduct type are correctly specified in the MGF file; systematic errors in these fields will propagate to incorrect formula assignments.
- Siamese rescore model was redesigned in v2.0.0 (breaking change), so results from v1.x checkpoints are not directly comparable; users must use v2.0.0+ checkpoints for consistent rescoring behavior.
- The method requires collision energy to be specified; spectra with missing or 'Unknown' collision energy may have reduced rescoring accuracy.
- Output is a ranked candidate list, not a binary classification; user must apply domain-specific knowledge or downstream structural analysis to select the final formula from the ranked set.

## Evidence

- [readme] FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra: "FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra"
- [readme] The rescore model has been redesigned with a Siamese architecture in v2.0.0: "The rescore model has been redesigned (Siamese architecture)"
- [other] Extract rescore predictions and rename Rescore (k) output columns to standardized format: "Extract rescore predictions and rename Rescore (k) output columns to standardized format"
- [readme] Output columns include Refined Formula (0..4) and Rescore (0..4): "Refined Formula (0..4)' | Ranked refined formula candidates for the default top-5 output. | `Refined Mass (0..4)' | Masses for the default top-5 refined candidates. | `Rescore (0..4)'"
- [readme] Required MGF fields are TITLE, PRECURSOR_MZ, PRECURSOR_TYPE, and COLLISION_ENERGY: "The required MGF fields are `TITLE`, `PRECURSOR_MZ`, `PRECURSOR_TYPE`, and `COLLISION_ENERGY`"
- [readme] Two-stage pipeline: TCN formula prediction followed by Siamese rescore model ranking: "For repeated or batched prediction, reuse `MsFiddlePredictor` so checkpoints are loaded once"
- [readme] Instrument type parameter accepts orbitrap (default) or qtof: "`--instrument_type` accepts `orbitrap` (default) or `qtof`"
