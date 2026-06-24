---
name: spectral-similarity-scoring
description: Use when when you have extracted low-resolution mass spectra from individual
  chromatographic peaks in GC-MS data and need to match them against a spectral library
  (e.g., PNNLMetV20191015.MSL) to identify the unknown compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0657
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - LowResMassSpectralMatch
  - PNNLMetV20191015.MSL
  - MetaMS
  - masscube
  - Python
  - Spectra
  - R
  - GNPS
  - HMDB
  - MassBank
  - MetaboShiny
  - TandemMatch
  - SIMILE
  techniques:
  - GC-MS
  - CE-MS
  license_tier: restricted
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
- doi: 10.1038/s41467-025-60640-5
  title: ''
- doi: 10.1186/s13321-023-00695-y
  title: ''
- doi: 10.1007/s11306-020-01717-8
  title: ''
- doi: 10.1021/jasms.4c00146
  title: ''
- doi: 10.1038/s41467-022-30118-9
  title: ''
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters
  import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  - build: coll_simile_cq
    doi: 10.1038/s41467-022-30118-9
    title: SIMILE
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  - 10.1038/s41467-025-60640-5
  - 10.1186/s13321-023-00695-y
  - 10.1007/s11306-020-01717-8
  - 10.1021/jasms.4c00146
  - 10.1038/s41467-022-30118-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantify the similarity between an experimental mass spectrum and library reference spectra using cosine similarity and retention-index proximity metrics. This skill is essential for automated compound identification in GC-MS workflows where multiple spectral candidates must be ranked and selected.

## When to use

When you have extracted low-resolution mass spectra from individual chromatographic peaks in GC-MS data and need to match them against a spectral library (e.g., PNNLMetV20191015.MSL) to identify the unknown compound. Use this skill after peak detection and retention index calibration, when you have both experimental m/z intensities and retention index values ready for comparison.

## When NOT to use

- Input spectrum is high-resolution (e.g., FT-ICR or Orbitrap data) — use fine isotopic structure and molecular formula assignment instead of library matching.
- Reference library is unavailable or does not cover the expected compound class — consider manual annotation or alternative identification strategies.
- Retention index calibration has failed or produced unreliable RI values — the secondary RI filtering criterion will be uninformative and may exclude correct matches.

## Inputs

- Low-resolution mass spectrum (m/z–intensity pairs) extracted from a single GC-MS peak
- Retention index value (RI) for the detected peak
- Reference spectral library in MSL format (e.g., PNNLMetV20191015.MSL) with library entries containing m/z–intensity spectra, CAS numbers, compound names, and reference retention indices

## Outputs

- Match result table with columns: compound name, CAS number, retention index, spectral match score (cosine similarity), and match rank
- Ranked list of candidate compounds sorted by score (highest similarity first)
- Exported results in CSV or HDF format for downstream curation

## How to apply

Apply the LowResMassSpectralMatch class from CoreMS, which scores candidate matches by computing cosine similarity between the experimental spectrum and each library reference spectrum, then filters and ranks candidates using retention-index proximity as a secondary criterion. The workflow loads the reference spectral library, iterates through each detected peak's mass spectrum, performs the cosine similarity calculation across all library entries, and aggregates results into a structured table with compound name, CAS number, spectral match score, and match rank. The cosine similarity metric weights both m/z values and their corresponding intensities, penalizing candidates whose retention indices deviate significantly from the experimental value.

## Related tools

- **CoreMS** (Provides LowResMassSpectralMatch class for spectral library matching and cosine similarity scoring against reference MSL databases) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Structures and exports match results (compound name, CAS, RI, score, rank) to CSV and tabular formats)
- **numpy** (Performs cosine similarity vector calculations between experimental and library spectra)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; from corems.gcms import GCMSData; gc_data = GCMSData('sample.cdf'); gc_data.calibrate_ri(); results = gc_data.spectral_match(library='PNNLMetV20191015.MSL'); results.to_csv('matches.csv')
```

## Evaluation signals

- Output table has same number of rows as input peaks, with no null compound names or scores for high-confidence matches (top rank).
- Cosine similarity scores are bounded in [0, 1] with top-ranked match having score ≥ 0.7 (typical threshold for GC-MS matches).
- Retention index difference between experimental and matched library entry is within tolerance (typically ±5 RI units for well-calibrated systems).
- Spot-check: for a known compound standard, verify that the correct library entry appears at or near rank 1 with highest score.
- Compare match scores across all candidates for each peak; verify score distribution is not uniform (indicating discriminative power of the metric).

## Limitations

- Cosine similarity alone does not account for spectral noise, baseline artifacts, or peak deconvolution errors — poor spectrum quality degrades match confidence.
- Library matching is fundamentally limited by reference library completeness; unknown or new compounds will not match, and novel isomers cannot be distinguished if their spectra are identical.
- Retention index calibration errors or use of different RI standards (Kovats vs. van den Dool) between experiment and library can cause false-negative matches despite high spectral similarity.
- Low-resolution GC-MS spectra often contain multiple isobaric fragments, reducing specificity compared to high-resolution or MS/MS approaches; multiple library candidates may have similar scores.

## Evidence

- [other] Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index proximity.: "Extract low-resolution mass spectra from each peak and perform LowResMassSpectralMatch against the PNNLMetV20191015.MSL spectral library, scoring matches by cosine similarity and retention-index"
- [other] Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank.: "Aggregate results into a structured table with compound name, CAS number, retention index, spectral match score, and match rank."
- [readme] Automatic molecular match algorithm with all spectral similarity methods: "Automatic molecular match algorithm with all spectral similarity methods"
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
