---
name: neural-network-based-molecular-formula-inference
description: Use when you have MS/MS spectra with unknown precursor m/z values and need to assign the most likely chemical formula and adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+) in a de novo setting where spectrum database matching is unavailable or undesirable.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3174
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

# neural-network-based-molecular-formula-inference

## Summary

Use a formula transformer neural network to rank candidate chemical formulas and adduct assignments directly from tandem MS/MS spectra without fragmentation tree computation. This approach learns data-dependent patterns and considers multiple adduct types, enabling de novo precursor mass annotation for unknown metabolites.

## When to use

You have MS/MS spectra with unknown precursor m/z values and need to assign the most likely chemical formula and adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+) in a de novo setting where spectrum database matching is unavailable or undesirable. Apply this skill when you want to avoid the computational overhead and assumptions of fragmentation tree methods (e.g., SIRIUS) and instead leverage empirical patterns learned from labeled MS/MS training data.

## When NOT to use

- Input spectra are in negative ionization mode; the current MIST-CF model is trained only on positive mode data.
- You have access to a comprehensive spectrum database and database matching is the primary goal; formula inference adds no unique value.
- The precursor m/z is already reliably assigned; this skill targets unknown or ambiguous precursor mass annotations.

## Inputs

- MS/MS spectra (in .mgf or equivalent format) with precursor m/z values
- Preprocessed spectrum intensities (normalized and noise-filtered)
- Candidate chemical formula list (enumerated using SIRIUS decomp or equivalent)
- Training dataset of MS/MS spectra with ground-truth chemical formulas and adduct annotations (e.g., NPLIB1, NIST20)

## Outputs

- Ranked list of candidate chemical formulas with adduct types per spectrum
- Energy-based scores for each formula–adduct pair
- Top-k accuracy metrics (top-1, top-3, top-k) for formula and adduct predictions
- Performance comparison tables and ranking accuracy plots against baseline methods

## How to apply

Preprocess MS/MS spectra by normalizing intensities and filtering noise, then extract precursor m/z values. Feed each spectrum into a trained formula transformer neural network that embeds both the spectrum peaks (including neutral loss fragments) and candidate chemical formulas using sinusoidal embeddings. The network scores agreement between each formula candidate and the observed spectrum using an energy-based model, producing a ranked list of formula–adduct pairs. Use a fast filter model (trained separately on molecular databases) to reduce the candidate formula space before full ranking to improve computational efficiency. Evaluate ranking performance using top-k accuracy metrics (top-1, top-3, top-k) on held-out test spectra, and compare against baseline methods (e.g., SIRIUS) on the same dataset.

## Related tools

- **MIST-CF** (Primary formula transformer neural network for ranking chemical formulas and adducts from MS/MS spectra; core inference engine) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Used internally for formula enumeration via dynamic programming algorithm (SIRIUS decomp); generates candidate formula space; also serves as baseline comparison method) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings used in MIST-CF to represent chemical formulas in a learnable latent space) — https://arxiv.org/abs/2303.06470
- **MIST** (Parent model for fingerprint prediction; MIST-CF is an extension that replaces MIST's formula transformer with architectural advances (internal subformula assignment, multiple adducts, sinusoidal embeddings, instrument covariates, neutral loss embedding)) — https://www.nature.com/articles/s42256-023-00708-3

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-k accuracy (top-1, top-3, top-k) for chemical formula predictions is ≥ X% on held-out test set, compared against baseline SIRIUS rankings on the same spectra.
- Top-k accuracy for adduct type assignment (e.g., [M+H]+ vs. [M+Na]+ vs. [M+K]+) shows measurable improvement over baseline methods.
- Energy-based scores are well-calibrated: higher-ranked formulas receive lower (more favorable) energy scores, and ground-truth formula ranks in top-1 or top-3 for majority of spectra.
- Performance remains consistent across instrument types (e.g., Orbitrap, QTOF) when instrument type is embedded as a model covariate.
- Few MS2 peaks (e.g., top 10–20 by intensity) are sufficient to achieve ≥ 90% of full-spectrum ranking accuracy, validating efficient learned patterns.

## Limitations

- Model is trained on positive ionization mode spectra only; negative mode performance is not addressed. README states 'still only positive mode'.
- Model trained on NPLIB1 public data may show reduced performance on Orbitrap or higher-resolution data; NIST20-trained models perform better but are proprietary and available only to users with a NIST license.
- Relies on SIRIUS decomp for initial formula enumeration; if SIRIUS misses true formula in the candidate list, neural ranking cannot recover it.
- Fragmentation tree structural information is not directly exploited; energy-based ranking may miss mechanistic patterns captured by tree-based methods in some edge cases.
- Computational cost of spectrum transformation and scoring scales with candidate formula space size; fast filter model is essential for efficiency but introduces a separate learned model dependency.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Utilizing sinusoidal formula embeddings as developed in our previous work SCARF: "Utilizing sinusoidal formula embeddings as developed in our previous work SCARF"
- [readme] Embedding neutral loss fragment formula for each peak in addition to the fragment formula: "Embedding the neutral loss fragment formula for each peak in addition to the fragment formula"
- [other] Preprocess MS/MS spectra (normalize intensities, filter noise) and extract precursor m/z values. 3. Run MIST-CF formula transformer neural network to generate ranked candidate chemical formulas and adduct assignments using energy-based scoring: "Preprocess MS/MS spectra (normalize intensities, filter noise) and extract precursor m/z values. Run MIST-CF formula transformer neural network to generate ranked candidate chemical formulas and"
- [other] Evaluate ranking performance by computing top-1, top-3, and top-k accuracy metrics for formula and adduct predictions: "Evaluate ranking performance by computing top-1, top-3, and top-k accuracy metrics for formula and adduct predictions"
- [readme] Show that few MS2 peaks are sufficient to learn candidate formula ranking.: "Show that few MS2 peaks are sufficient to learn candidate formula ranking"
