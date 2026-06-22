---
name: ms2-fingerprint-vector-generation
description: Use when you have LC-MS/MS data in mzML, mzXML, or MGF format from one or more metabolomics samples and need to compare samples that may have poor overlap in detected features, strong retention time shifts between runs, or were acquired on different LC methods or MS technologies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - spec2vec
  - Python
  - numpy
  - MEMO
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra and converting them into documents.
- conda create --name memo python=3.8
- pip install numpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms2-fingerprint-vector-generation

## Summary

Generate sample-level MS2 fingerprint vectors by counting occurrences of MS2 fragment peaks and neutral losses across all spectra in a metabolomics sample. This retention-time-agnostic representation enables cross-sample comparison for chemodiverse datasets with poor feature overlap or strong LC/MS method variation.

## When to use

You have LC-MS/MS data in mzML, mzXML, or MGF format from one or more metabolomics samples and need to compare samples that may have poor overlap in detected features, strong retention time shifts between runs, or were acquired on different LC methods or MS technologies (e.g., Q-ToF vs. Orbitrap). Use this skill as the first stage of MEMO sample vectorization before cross-sample alignment.

## When NOT to use

- Input is already a feature table or aligned peak matrix (fingerprinting is not needed; proceed directly to cross-sample comparison).
- Sample contains only MS1 data or precursor masses without fragmentation spectra.
- You require compound-level or molecular-species-level annotations; MS2 fingerprints are agnostic to chemical identity and focus on fragment patterns.

## Inputs

- MS2 spectra in mzML, mzXML, MGF, or msp format from a single metabolomics sample
- Sample metadata (optional: precursor m/z, retention time, spectrum quality scores)

## Outputs

- MS2 fingerprint vector: dictionary or array mapping (peak m/z, neutral loss m/z) to occurrence counts
- Serialized fingerprint: JSON or CSV file with peak/loss identifiers and their frequencies
- Sample-level feature vector suitable for cross-sample alignment and comparison

## How to apply

Parse MS2 spectra from the sample file using matchms to extract and normalize fragmentation data. For each spectrum, extract all m/z peak values and compute neutral losses by subtracting each peak m/z from the precursor m/z. Aggregate counts of each unique peak m/z and neutral loss value across all spectra in the sample into a frequency dictionary or vector. Normalize or weight counts as needed (e.g., to account for spectrum abundance or quality). Serialize the resulting fingerprint as a JSON or CSV mapping peak/loss identifiers to occurrence frequencies, which becomes a fixed-length feature vector for downstream sample-to-sample comparison.

## Related tools

- **matchms** (Parse, normalize, and clean MS2 spectra from standard file formats (mzML, mzXML, MGF, msp); extract metadata and peaks.) — https://github.com/matchms/matchms
- **spec2vec** (Compute spectral embeddings of MS2 fragments and neutral losses for downstream similarity scoring (alternative to raw fingerprint comparison).) — https://github.com/iomega/spec2vec
- **numpy** (Aggregate and manipulate peak/loss count arrays; perform vectorization and normalization of fingerprint data.)
- **MEMO** (End-to-end workflow for MS2 fingerprint generation, sample alignment, and visualization (wraps matchms and spec2vec).) — https://github.com/mandelbrot-project/memo

## Examples

```
from matchms.importing import load_from_mgf
from collections import Counter
import json

spectra = load_from_mgf('sample.mgf')
fingerprint = Counter()
for spec in spectra:
    precursor = spec.precursor_mz
    for peak_mz in spec.peaks.mz:
        fingerprint[round(peak_mz, 2)] += 1
        neutral_loss = round(precursor - peak_mz, 2)
        fingerprint[f'NL_{neutral_loss}'] += 1

with open('sample_fingerprint.json', 'w') as f:
    json.dump(dict(fingerprint), f)
```

## Evaluation signals

- Fingerprint vector has non-zero entries for peaks and neutral losses observed in the sample; all unique identifiers are present and counts are positive integers.
- Fingerprint dimensions match the union of all peak m/z and neutral loss values detected across all spectra in the sample.
- Peak m/z values fall within the MS instrument's measurable range; neutral losses are between 0 and the precursor m/z (no invalid values).
- Fingerprint can be aligned with fingerprints from other samples without dimension mismatch (feature padding/union is consistent across samples).
- Downstream cross-sample similarity or distance metrics (e.g., cosine, Euclidean, or spec2vec embeddings) are computable between fingerprint pairs.

## Limitations

- Fingerprints are retention-time-agnostic and do not encode temporal separation; they aggregate all spectra in a sample regardless of elution order or peak shape.
- Rare or low-abundance fragments may be present with count = 1, reducing statistical power for downstream comparison; consider filtering or smoothing thresholds based on sample size and instrument noise.
- Peak and neutral loss identities are defined by m/z value alone; isobaric compounds or very high mass resolution may lead to artificial fragmentation of a single neutral loss across multiple m/z bins.
- Fingerprints require careful blank/background filtering in a subsequent step to remove instrument or solvent artifacts; unfiltered fingerprints may not reflect true sample composition.
- Method is insensitive to retention time shifts by design; coeluting isomers or charge-state variants are conflated in the same fingerprint.

## Evidence

- [intro] MS2 fingerprints are generated by counting the occurrence of MS2 peaks and neutral losses (relative to the precursor) within each sample.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [other] Workflow steps for MS2 fingerprint generation include spectrum parsing, peak extraction, neutral loss calculation, and aggregation into a count dictionary.: "1. Load MS2 spectra from the input sample file using matchms to parse and normalize fragmentation data. 2. Extract all m/z peaks from each MS2 spectrum and compute neutral losses by subtracting each"
- [intro] MEMO suits particularly well to compare chemodiverse samples with poor feature overlap or strong retention time shifts across different LC methods or MS technologies.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [readme] matchms is the core package for spectrum parsing and preprocessing in MEMO fingerprint workflows.: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [intro] Fingerprints are serialized and made available for downstream cross-sample alignment and filtering.: "These fingerprints can in a second stage be aligned to compare different samples"
