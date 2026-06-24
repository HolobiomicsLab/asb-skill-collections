---
name: fragment-peak-chemical-annotation
description: Use when you have MS/MS spectra with assigned precursor formulas and
  need to annotate the chemical composition of individual fragment peaks for metabolite
  structure elucidation or fragmentation pathway analysis. Apply this skill when you
  want to avoid external fragmentation tree computation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0591
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - MIST
  - MIST-CF
  - SCARF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum
  using an end-to-end energy based modeling approach
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-peak-chemical-annotation

## Summary

Assign chemical subformulas to individual MS/MS fragment peaks using a neural network-based formula transformer that ranks candidate subformulas conditioned on the precursor formula and observed m/z value, without computing fragmentation trees. This enables per-peak chemical annotation in a data-dependent fashion for tandem mass spectra.

## When to use

You have MS/MS spectra with assigned precursor formulas and need to annotate the chemical composition of individual fragment peaks for metabolite structure elucidation or fragmentation pathway analysis. Apply this skill when you want to avoid external fragmentation tree computation (e.g., SIRIUS) and need rapid, learnable per-peak subformula rankings.

## When NOT to use

- Precursor formula is unknown or not yet assigned—use precursor formula inference first.
- Input spectra are in negative ionization mode—MIST-CF currently supports positive mode only.
- You require explainability at the fragmentation mechanism level—the neural network assigns subformulas without computing fragmentation trees and may not reveal intermediate neutral losses or bond cleavage pathways.

## Inputs

- MS/MS spectrum (m/z and intensity pairs)
- MS1 precursor mass
- Assigned precursor chemical formula
- List of candidate subformulas for each fragment peak (from chemical composition space)

## Outputs

- Ranked subformula candidates per fragment peak
- Per-peak subformula prediction score
- Per-peak accuracy metrics
- Exact-match rate per spectrum
- Ranking metrics (top-k recall)

## How to apply

Load MS/MS spectra and their corresponding MS1 precursor masses along with assigned precursor formulas. Pass each spectrum and its peaks to the MIST-CF formula transformer, which internally ranks candidate subformulas for each observed fragment peak by conditioning on the precursor formula and the observed m/z value. The transformer outputs per-peak subformula predictions ranked by score without computing SIRIUS fragmentation trees or querying external spectrum databases. Evaluate predictions by comparing against reference subformula labels, computing per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k predictions). The ranking score reflects agreement between the candidate subformula and the observed MS/MS peaks.

## Related tools

- **MIST-CF** (Formula transformer neural network that ranks chemical formula and adduct assignments for unknown mass spectra and assigns subformulas to fragment peaks in a data-dependent fashion) — https://github.com/samgoldman97/mist-cf
- **MIST** (Parent framework extended by MIST-CF for annotating MS1 precursor masses from MS/MS data) — https://www.nature.com/articles/s42256-023-00708-3
- **SIRIUS** (Provides dynamic programming algorithm (SIRIUS decomp) for enumerating candidate formulas; MIST-CF replaces SIRIUS fragmentation trees with an internal subformula assignment protocol) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings used by MIST-CF to represent candidate chemical formulas) — https://arxiv.org/abs/2303.06470

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Per-peak accuracy: fraction of peaks for which the correct subformula is ranked first by the model
- Exact-match rate per spectrum: percentage of spectra where all fragment peaks receive the correct subformula assignment
- Top-k ranking recall: fraction of correct subformulas that appear in the top-k predictions for each peak (e.g., top-5)
- Landmark error distribution: comparison of predicted vs. reference subformula assignments on held-out test data, stratified by peak m/z or intensity
- Consistency check: verify that all predicted subformulas are chemically valid (mass and elemental composition consistent with observed m/z and precursor formula)

## Limitations

- Positive ionization mode only; negative mode spectra are not supported.
- Model performance may be lower on high-resolution Orbitrap data compared to lower-resolution instruments if trained exclusively on lower-resolution training data (e.g., models trained on NPLIB1 may underperform on commercial NIST20 spectra).
- Subformula prediction is data-dependent and conditioned on training set; out-of-distribution molecules or rare fragmentation patterns may receive poor rankings.
- No fragmentation tree output: the model does not explicitly model neutral losses or sequential cleavage pathways, limiting interpretability of fragmentation mechanisms.

## Evidence

- [other] MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees: "MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Rank chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [other] For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees: "For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees or querying external spectrum databases"
- [other] Comparing predicted subformula assignments against reference labels and compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics: "Compare predicted subformula assignments against reference labels and compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k"
