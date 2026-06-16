---
name: mass-spectrometry-adduct-annotation
description: Use when you have preprocessed MS/MS spectra with measured precursor m/z values but the ionization adduct type is unknown or ambiguous—particularly in metabolomics workflows where multiple adducts co-occur or in de novo formula annotation without access to curated spectral databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
---

# mass-spectrometry-adduct-annotation

## Summary

Rank and assign ionization adducts (e.g., [M+H]+, [M+Na]+, [M+K]+) to unknown precursor m/z values in tandem MS/MS spectra using a neural network energy-based scoring model. This skill is essential when precursor mass alone is ambiguous across multiple possible adduct types and chemical formulas.

## When to use

Apply this skill when you have preprocessed MS/MS spectra with measured precursor m/z values but the ionization adduct type is unknown or ambiguous—particularly in metabolomics workflows where multiple adducts co-occur or in de novo formula annotation without access to curated spectral databases. MIST-CF's multi-adduct support (beyond [M+H]+ alone) is most valuable when working with positive-mode spectra that may contain sodium, potassium, or other common adducts.

## When NOT to use

- Spectrum is already annotated with a high-confidence adduct from MS1 isotope pattern or prior orthogonal measurement; use direct formula search instead.
- Negative-mode spectra or exotic adducts (e.g., [M−H]−, [M+Cl]−) not covered by the model training regime; MIST-CF is currently limited to positive-mode adducts only.
- Input is a feature matrix or pre-aggregated spectral library; this skill operates on individual, peak-resolved MS/MS spectra.

## Inputs

- MS/MS spectrum (mgf or mzML format): list of fragment m/z–intensity pairs
- precursor m/z value (float, typically 100–2000)
- instrument type (covariate: e.g., Orbitrap, Q-TOF)

## Outputs

- ranked list of candidate (chemical_formula, adduct_type, energy_score) tuples
- top-1, top-3, top-k accuracy metrics (per spectrum and aggregated)
- comparison table: MIST-CF vs. SIRIUS top-k accuracy on benchmark dataset

## How to apply

Load the preprocessed MS/MS spectrum and its precursor m/z value into the MIST-CF formula transformer model. The model internally generates candidate chemical formulas using a dynamic programming algorithm (SIRIUS decomposition) for that precursor mass, then scores each candidate formula–adduct pair by computing the agreement (energy-based score) between the predicted spectrum and observed fragment intensities. The model learns this scoring function in a data-dependent fashion from training spectra rather than using hardcoded fragmentation rules. Evaluate ranking by computing top-1, top-3, and top-k accuracy: check how often the true formula and adduct combination appear in the model's ranked list. Compare your top-k accuracy against a SIRIUS baseline to validate the improvement from end-to-end learning.

## Related tools

- **MIST-CF** (primary neural-network model for energy-based adduct and formula ranking; implements formula transformer architecture with sinusoidal embeddings and multi-adduct scoring) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (formula enumeration backend (SIRIUS decomp); generates candidate formulas for a given precursor m/z via dynamic programming; used as baseline for performance comparison) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (prior work that developed sinusoidal formula embeddings; embeddings are reused in MIST-CF to represent chemical formula candidates) — https://arxiv.org/abs/2303.06470

## Examples

```
. quickstart/run_model.sh
```

## Evaluation signals

- Top-1 accuracy (does the model rank the true formula–adduct pair first?) should exceed SIRIUS baseline by ≥5–10 percentage points on benchmark datasets like NPLIB1 or CASMI 2022.
- Top-k accuracy curves (k=1,3,5,10) should be monotonic and plateau; inspect for unexpected drops indicating systematic failure modes.
- Per-adduct accuracy breakdown (e.g., [M+H]+ vs. [M+Na]+ vs. [M+K]+) should show balanced performance across adduct types; large gaps suggest class imbalance in training data.
- Spectrum-level agreement between predicted fragments and observed intensities (energy score) should correlate with ranking correctness: high-scoring candidates should match ground truth more often.
- Model output ranking should not collapse to a single candidate with probability ≈1.0 (overfitting); calibrated soft rankings across top-k candidates indicate healthy uncertainty.

## Limitations

- MIST-CF operates in positive-mode only; negative-mode spectra ([M−H]−, [M+Cl]−) require model retraining or a separate negative-mode checkpoint.
- Ranking performance depends heavily on training set composition: models trained on NPLIB1 (natural products) may underperform on synthetic or pharmaceutical spectra with different fragmentation patterns.
- The model requires SIRIUS decomp to enumerate candidate formulas first; enumeration speed and completeness are inherited from SIRIUS's dynamic programming algorithm and may struggle with very high or very low m/z ranges.
- Adduct type coverage is limited to common adducts observed during training; exotic adducts (e.g., [M+2Na]2+, [M+NH4]+) not represented in the training set will not be ranked.
- Ground-truth formula–adduct pairs must be known during evaluation; if ground truth is uncertain or multimodal (multiple plausible annotations for one spectrum), accuracy metrics become less reliable.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilize the dynamic programming algorithm implemented by SIRIUS, SIRIUS decomp, which is provided as an independent module: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`, which is provided as an independent module"
- [other] Evaluate ranking performance by computing top-1, top-3, and top-k accuracy metrics for formula and adduct predictions: "Evaluate ranking performance by computing top-1, top-3, and top-k accuracy metrics for formula and adduct predictions"
- [other] Compare MIST-CF top-k accuracy results against SIRIUS baseline predictions on the same dataset: "Compare MIST-CF top-k accuracy results against SIRIUS baseline predictions on the same dataset"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data): "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)"
