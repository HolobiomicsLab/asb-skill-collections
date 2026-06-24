---
name: de-novo-mass-spectrum-interpretation
description: Use when you have MS/MS spectra (centroided m/z and intensity pairs)
  and corresponding MS1 precursor masses but lack reference spectra or a priori formula
  information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - MIST
  - MIST-CF
  - SCARF
  - SIRIUS
  techniques:
  - LC-MS
  license_tier: restricted
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

# de-novo-mass-spectrum-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Infer chemical formula and adduct type for an unknown metabolite directly from tandem mass spectra (MS/MS) without referencing spectral databases or computing fragmentation trees. This skill uses a neural network-based formula transformer to rank candidate formulas and assign subformulas to fragment peaks in a data-dependent fashion.

## When to use

You have MS/MS spectra (centroided m/z and intensity pairs) and corresponding MS1 precursor masses but lack reference spectra or a priori formula information. Apply this skill when you need to annotate chemical formulas for unknowns in a de novo setting, particularly when rapid ranking of multiple formula–adduct candidates is required without external database lookups.

## When NOT to use

- Input spectra are profile (uncentroided) or have very low mass resolution (<5 ppm); MIST-CF expects centroided data with accurate m/z assignments.
- Negative-mode MS/MS data; MIST-CF currently handles only positive-mode ionization.
- A reference database with high-confidence spectral annotations is available and can be queried; database matching may be faster and more reliable than de novo inference.
- Precursor mass is unknown or uncertain by more than ±10 ppm; formula enumeration depends on accurate precursor m/z.

## Inputs

- MS/MS spectra (centroided m/z and intensity pairs in .mgf or similar format)
- MS1 precursor mass (or m/z value with charge state)
- Precursor formula candidate set (enumerated via SIRIUS decomp or equivalent)
- Candidate adduct types (e.g., [M+H]+, [M+Na]+, [M+K]+)

## Outputs

- Ranked list of chemical formula–adduct assignments per spectrum
- Per-peak subformula predictions with confidence scores
- Energy-based model scores reflecting agreement between formula candidate and spectrum
- Exact-match accuracy and top-k ranking metrics on held-out test set

## How to apply

Load MS/MS spectra and precursor masses into the MIST-CF pipeline. Use SIRIUS decomp to enumerate candidate formulas matching the precursor m/z within a specified mass tolerance (typical workflows use 5 ppm or better accuracy). Feed the precursor formula, fragment m/z values, and observed intensities into the formula transformer neural network, which ranks subformula assignments per peak conditioned on the precursor formula and m/z. The transformer learns peak-to-subformula mappings in a data-dependent manner without pre-computing fragmentation trees. Score and rank the candidate formulas using an energy-based model that aggregates peak-level predictions. Evaluate by comparing predicted formulas and adducts against ground truth using exact-match accuracy and top-k ranking metrics.

## Related tools

- **MIST-CF** (Core neural network model for formula transformer inference; ranks formula–adduct candidates and assigns subformulas to peaks.) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Generates candidate formulas via dynamic programming (SIRIUS decomp); enumerates all chemically valid formulas within mass tolerance of precursor.) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings used in the MIST-CF transformer architecture.) — https://arxiv.org/abs/2303.06470
- **MIST** (Original metabolite inference system with spectrum transformer; extended by MIST-CF for de novo formula assignment.) — https://www.nature.com/articles/s42256-023-00708-3

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Exact-match accuracy: fraction of spectra for which the top-ranked formula–adduct pair matches the ground truth label.
- Top-k ranking metric: fraction of correct formulas appearing in the model's top-k predictions (e.g., top-5 or top-10).
- Per-peak subformula accuracy: agreement between predicted subformula assignments and reference labels, aggregated across all peaks in the held-out test set.
- Comparison against SIRIUS baseline: MIST-CF should match or exceed SIRIUS ranking performance on the same spectrum set without database filtering.
- Energy-based model score distribution: ranked candidates should show clear separation between correct and incorrect formula–adduct assignments in the score distribution.

## Limitations

- Currently supports positive-mode ionization only; negative-mode spectra require separate model training or adaptation.
- Performance may degrade on data from mass analyzers (e.g., Orbitrap, Q-TOF) not represented in the training set; models trained on NPLIB1 may be less performant on high-resolution Orbitrap data than models trained on NIST20.
- Depends on accurate precursor m/z and centroided peak detection; noisy or mis-calibrated spectra will reduce formula enumeration and ranking quality.
- Subformula assignment relies on learned neural network patterns; edge cases with unusual fragmentation modes or highly modified compounds may not generalize from training data.
- Computational cost scales with the number of candidate formulas; spectra with many near-isobaric candidates will require longer inference time.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] annotating MS1 precursor masses from MS/MS data in a de novo setting: "annotating MS1 precursor masses from MS/MS data in a _de novo_ setting"
- [other] MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks in a data-dependent fashion without external fragmentation tree computation.: "MIST-CF implements an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees, enabling the formula transformer neural network to assign subformulas to peaks"
- [other] For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees or querying external spectrum databases.: "For each spectrum, generate per-peak subformula predictions without computing SIRIUS fragmentation trees or querying external spectrum databases"
- [readme] Model output will be saved in quickstart/mist_cf_out/. This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
