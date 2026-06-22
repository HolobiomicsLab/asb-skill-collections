---
name: tandem-mass-spectra-interpretation
description: Use when you have an unknown MS/MS spectrum (tandem mass spectrum) with a measured precursor m/z and fragment peaks, and you need to assign the most likely molecular formula and ionization adduct (e.g., [M+H]+, [M+Na]+, [M+K]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tandem Mass Spectra Interpretation

## Summary

Rank chemical formula and adduct assignments for unknown MS/MS spectra using energy-based neural network scoring, without relying on spectral databases. This skill applies a transformer architecture to learn fragment-formula relationships directly from data, supporting multiple adduct types in positive ionization mode.

## When to use

You have an unknown MS/MS spectrum (tandem mass spectrum) with a measured precursor m/z and fragment peaks, and you need to assign the most likely molecular formula and ionization adduct (e.g., [M+H]+, [M+Na]+, [M+K]+). Use this skill when database-free de novo annotation is required, particularly for natural products or compounds outside curated spectral libraries, or when evaluating formula-adduct hypotheses for instrument types (Orbitrap, Q-TOF) represented in your training data.

## When NOT to use

- Input spectrum is from negative ionization mode; MIST-CF currently supports positive mode only.
- Precursor m/z is outside the mass range covered by the training data (NPLIB1: ~50–2000 Da); model generalization is unvalidated.
- You require structure prediction, not just formula and adduct; use MIST or similar fingerprint-based methods for molecular structure.

## Inputs

- MS/MS spectrum: MGF file or structured object with precursor m/z, fragment m/z array, and intensity array
- Precursor mass (monoisotopic m/z)
- Candidate molecular formula list (enumerated by SIRIUS decomp or provided externally)
- Instrument type metadata (e.g., Orbitrap, Q-TOF, MALDI) — optional but improves scoring
- List of allowed adduct types to consider (default: positive-mode adducts [M+H]+, [M+Na]+, [M+K]+, [M+NH4]+)

## Outputs

- Ranked list of (formula, adduct, energy_score) tuples, ordered by ascending energy score
- Top-1 and top-k formula-adduct predictions with confidence scores
- Comparison report (if evaluated against ground truth): top-1 and top-k accuracy, delta vs. [M+H]+-only baseline

## How to apply

Load a preprocessed MS/MS spectrum (as MGF or similar format containing m/z and intensity pairs for fragments, plus precursor m/z). Use SIRIUS decomp to enumerate candidate formulas consistent with the precursor mass (within instrument-specific tolerance). Pass the spectrum and formula candidates through MIST-CF's energy-based transformer model, which internally assigns fragment subformulas and scores agreement between each candidate formula-adduct pair and the observed fragment pattern. Rank formulas by the model's energy score (lower is better). For multi-adduct support, the model considers positive-mode adducts beyond [M+H]+ (e.g., [M+Na]+, [M+K]+, [M+NH4]+) jointly during scoring. Return the top-k ranked formula-adduct predictions; evaluate using top-1 and top-k accuracy metrics on ground-truth benchmarks (e.g., NPLIB1, NIST20, CASMI 2022). Performance is sensitive to instrument type and the number of MS/MS peaks available (few peaks, <10, may reduce accuracy).

## Related tools

- **MIST-CF** (Primary neural network model: ranks formula-adduct pairs via energy-based transformer scoring; directly executes the skill.) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Enumerates candidate molecular formulas from precursor mass using dynamic programming decomposition; required preprocessing to generate formula candidate list.) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST** (Parent tool for fingerprint prediction; MIST-CF extends MIST with chemical formula ranking capability.) — https://www.nature.com/articles/s42256-023-00708-3
- **SCARF** (Provides sinusoidal formula embedding representation used in MIST-CF's transformer architecture.) — https://arxiv.org/abs/2303.06470

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh && python -c "from mist_cf.mist_cf_score.predict import predict_spectra; predict_spectra(spec_file='data/demo_specs.mgf', model_path='quickstart/model.pt', output_dir='quickstart/mist_cf_out/') "
```

## Evaluation signals

- Top-1 accuracy: fraction of test spectra for which the highest-ranked (formula, adduct) pair matches ground truth; typical reported value ~70–85% on NPLIB1, ~60–75% on CASMI 2022.
- Top-k accuracy: fraction of spectra where correct pair appears in top-k predictions (k=5, 10, etc.); should increase monotonically with k.
- Performance delta (multi-adduct vs. [M+H]+-only): multi-adduct mode accuracy ≥ [M+H]+-only accuracy, validating the contribution of adduct diversity.
- Energy score distribution: correct formula-adduct pairs should cluster at lower energy scores than incorrect ones; inspect rank histograms for separation.
- Consistency across instrument types: if training includes Orbitrap and Q-TOF data, accuracy should remain within 5–10% when evaluated on held-out spectra from same instrument.

## Limitations

- Positive ionization mode only; negative mode MS/MS spectra are not supported.
- Model trained on NPLIB1 (natural products) may be less performant on synthetic or pharmaceutical compounds; NIST20 models available upon request but require commercial license.
- Requires precursor m/z as input; does not perform MS1 feature detection or peak picking.
- Formula enumeration via SIRIUS is deterministic but mass tolerance and allowed atom counts (C, H, N, O, P, S, F, Cl, Br, I) must match training assumptions; unusual elements or isotope patterns not handled.
- Few MS/MS peaks (<10) reduce ranking accuracy; high-noise or low-resolution spectra may yield lower confidence.
- No explanation of which fragments drove ranking decision; energy scores are model-internal and not interpretable as fragmentation mechanisms.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [intro] MIST-CF considers multiple adduct types beyond [M+H]+ in positive mode: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [full_text] What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?: "What is the performance improvement in chemical formula ranking accuracy when MIST-CF incorporates support for multiple adduct types compared to restricting predictions to [M+H]+ only?"
- [full_text] Run MIST-CF inference in full multi-adduct mode using the complete energy-based modeling approach, allowing ranking across multiple positive-mode adduct types, and record ranked predictions: "Run MIST-CF inference in full multi-adduct mode using the complete energy-based modeling approach, allowing ranking across multiple positive-mode adduct types"
- [full_text] Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes: "Compute ranking accuracy metrics (top-1 and top-k correct formula-adduct pair identification) for both modes"
