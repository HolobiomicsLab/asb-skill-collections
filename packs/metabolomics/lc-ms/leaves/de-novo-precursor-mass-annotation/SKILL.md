---
name: de-novo-precursor-mass-annotation
description: Use when when you have unknown MS/MS spectra with observed precursor m/z values and want to infer the molecular formula and adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+) in a de novo setting without access to spectral libraries.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  tools:
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# de-novo-precursor-mass-annotation

## Summary

Annotate MS1 precursor masses and rank chemical formula and adduct assignments from tandem MS/MS spectra without reference to spectrum databases, using an end-to-end energy-based neural network that scores agreement between candidate formulas and observed peaks.

## When to use

When you have unknown MS/MS spectra with observed precursor m/z values and want to infer the molecular formula and adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+) in a de novo setting without access to spectral libraries. This is appropriate when database-dependent methods are unavailable or when you need to rank multiple formula–adduct hypotheses by their spectral evidence rather than fragmentation tree topology.

## When NOT to use

- When only MS1 data (precursor mass alone) is available without fragmentation information; MIST-CF requires MS/MS peak intensity patterns to score formulas.
- When the mass spectrometry data is in negative ion mode; the current model is trained only for positive mode, although the architecture could be extended.
- When spectrum database matching is feasible and sufficient; library-based methods may be faster and more reliable for well-characterized compounds in curated databases.

## Inputs

- MS/MS spectra in MGF or equivalent format (m/z–intensity peak pairs per spectrum)
- Observed precursor m/z values
- Candidate chemical formula list (enumerated by SIRIUS decomp or similar)
- Trained MIST-CF model checkpoint (neural network weights)
- MS/MS dataset with ground-truth chemical formulas (for evaluation)

## Outputs

- Ranked list of candidate chemical formulas per spectrum (with confidence scores)
- Adduct type assignments (e.g., [M+H]+, [M+Na]+, [M+K]+)
- Top-k accuracy metrics (top-1, top-3, top-k) for formula and adduct predictions
- Comparison table of MIST-CF vs. baseline (SIRIUS) ranking performance

## How to apply

First, preprocess the MS/MS spectra by normalizing intensities and filtering noise, then extract the precursor m/z value for each spectrum. Use SIRIUS decomp (or equivalent) to enumerate all candidate chemical formulas within a specified mass tolerance (typically a few ppm) of the observed precursor m/z. Pass the spectrum (peak list with m/z and intensity pairs) and candidate formula list to the MIST-CF formula transformer neural network, which learns to score and rank formulas based on spectral patterns—specifically by evaluating agreement between observed fragment m/z values and fragment formulas derived from each candidate. The model simultaneously scores multiple adduct types (beyond [M+H]+ in positive mode) by learning their characteristic fragmentation patterns. Evaluate ranking accuracy using top-1, top-3, and top-k accuracy metrics on a held-out test set of spectra with ground-truth formulas.

## Related tools

- **MIST-CF** (Primary formula transformer neural network that ranks chemical formula and adduct assignments by scoring agreement between spectrum and candidate formulas using energy-based modeling) — https://github.com/samgoldman97/mist-cf
- **SIRIUS** (Enumerates candidate chemical formulas from precursor m/z using dynamic programming (SIRIUS decomp); MIST-CF uses its formula enumeration but replaces fragmentation tree computation with learned scoring) — https://bio.informatik.uni-jena.de/software/sirius/
- **SCARF** (Provides sinusoidal formula embeddings used in MIST-CF's formula encoder to represent chemical structure information in a learnable feature space) — https://arxiv.org/abs/2303.06470
- **MIST** (Original framework for annotating molecular properties from MS data; MIST-CF extends it to the de novo precursor mass annotation task) — https://www.nature.com/articles/s42256-023-00708-3

## Examples

```
. quickstart/download_model.sh && . quickstart/run_model.sh
```

## Evaluation signals

- Top-1 and top-k accuracy of formula predictions match or exceed SIRIUS baseline on the same benchmark dataset (e.g., NPLIB1 or CASMI 2022)
- Ranked formulas are sorted by energy-based model confidence scores that correlate with correctness; inspect that true formula ranks higher than decoys
- Adduct type predictions should agree with the chemical formula assignment (e.g., no [M+H]+ assignment to a formula that cannot accept a proton)
- Model output confidence scores are well-calibrated: higher scores should correspond to higher accuracy, verifiable via accuracy-vs-confidence plots or expected calibration error
- When run on the same precursor m/z and spectrum, MIST-CF and SIRIUS should identify overlapping top-k candidate formulas, with MIST-CF reranking them based on spectral fit

## Limitations

- Currently limited to positive ion mode; negative mode requires retraining or model extension.
- Performance depends on model training data; the publicly available model trained on NPLIB1 may be less performant on high-resolution (Orbitrap) spectra; NIST20-trained models are available under license.
- Requires enumeration of candidate formulas via SIRIUS decomp as a preprocessing step; if the true formula falls outside the search space (e.g., due to tight mass tolerance settings), it cannot be ranked.
- The model learns in a data-dependent fashion and does not explicitly compute fragmentation trees, so it may be less interpretable than rule-based fragmentation approaches.
- Performance degrades when very few MS/MS peaks are present; the model benefits from sufficient peak diversity to disambiguate formulas.

## Evidence

- [readme] annotating MS1 precursor masses from MS/MS data in a _de novo_ setting: "This repository provides implementations and code examples for [MIST-CF](https://www.nature.com/articles/s42256-023-00708-3), an extension of [MIST](https://www.nature.com/articles/s42256-023-00708-3)"
- [readme] MIST-CF ranks chemical formula and adduct assignments using energy-based modeling without referencing spectrum databases: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of fragmentation trees, MIST-CF adopts a formula transformer neural network architecture: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] MIST-CF considers multiple adduct types beyond [M+H]+ in positive mode: "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
- [readme] Comparison with SIRIUS: Run SIRIUS prediction, format output, run MIST-CF prediction, then evaluate performance: "Experiment pipeline: 1. *Run SIRIUS prediction*: `run_scripts/sirius_compare/sirius_1_run.py` 2. *Format SIRIUS output*: `run_scripts/sirius_compare/sirius_2_wrangle.py` 3. *Run MIST-CF prediction*:"
- [readme] SIRIUS decomp used to enumerate candidate formulas; MIST-CF replaces fragmentation tree computation: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`, which is provided as an independent module."
- [readme] Public model trained on NPLIB1 may be less performant on Orbitrap data; NIST20 models available upon request: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data). Download links to models trained on NIST20 models are"
