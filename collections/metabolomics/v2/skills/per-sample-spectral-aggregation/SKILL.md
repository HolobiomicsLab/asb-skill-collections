---
name: per-sample-spectral-aggregation
description: Use when you have raw MS2 spectra from a sample and need to collapse them into a single sample-level representation for comparison across multiple samples, particularly when samples have poor feature overlap, strong retention time shifts between LC methods, or were acquired on different mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - MEMO
  - Python 3.8+
  techniques:
  - tandem-MS
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- conda create --name memo python=3.8
- pip install numpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo
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

# per-sample-spectral-aggregation

## Summary

Aggregate MS2 fragmentation peaks and neutral losses across all spectra within a single sample to produce a numeric fingerprint vector. This skill enables sample-level comparison when individual spectrum alignment is unreliable or retention times vary across LC methods or instruments.

## When to use

Use this skill when you have raw MS2 spectra from a sample and need to collapse them into a single sample-level representation for comparison across multiple samples, particularly when samples have poor feature overlap, strong retention time shifts between LC methods, or were acquired on different mass spectrometer technologies (e.g. Maxis Q-ToF vs Q-Exactive Orbitrap).

## When NOT to use

- Input is already a pre-computed feature matrix or peak table — skip directly to alignment.
- Spectra have been pre-processed into a single consensus spectrum per sample — no aggregation needed.
- Your analysis requires individual spectrum-level similarity scores (e.g. for spectral library matching) rather than sample-level comparison.
- Samples contain only a single spectrum each — aggregation would be trivial.

## Inputs

- MS2 spectra files in mzML, mzXML, or MGF format
- Sample identifier (batch or group label)
- Precursor m/z values per spectrum
- Fragment m/z peaks per spectrum

## Outputs

- Per-sample MS2 fingerprint vector (numeric array)
- Peak occurrence counts (sample-level aggregation)
- Neutral loss occurrence counts (sample-level aggregation)
- Sample-level spectral embedding from spec2vec

## How to apply

Load MS2 spectra files (mzML, mzXML, or MGF formats) using matchms to parse fragmentation data. For each sample, iterate through all spectra and extract precursor m/z values. Count occurrences of all MS2 peaks (m/z fragments above noise threshold) in each spectrum. Calculate neutral losses by subtracting each observed fragment m/z from the precursor m/z. Aggregate peak and neutral loss counts across all spectra within the sample using spec2vec document conversion to handle the spectral embedding. Normalize the combined peak and neutral loss occurrence counts by sample size (total number of spectra) to produce a final numeric fingerprint vector. This vector becomes the sample's representation for downstream alignment and comparison.

## Related tools

- **matchms** (Parses raw MS2 spectra files and extracts precursor m/z and fragment peaks; provides spectrum objects and metadata cleaning) — https://github.com/matchms/matchms
- **spec2vec** (Converts aggregated peak and neutral loss counts into spectral embeddings; learns structural relationships between fragments for document-level vectorization) — https://github.com/iomega/spec2vec
- **MEMO** (Implements the full MS2-based sample vectorization pipeline, integrating matchms and spec2vec for per-sample fingerprint generation and downstream visualization) — https://github.com/mandelbrot-project/memo
- **numpy** (Array operations for counting occurrences and normalizing fingerprint vectors)
- **Python 3.8+** (Runtime environment for matchms, spec2vec, and MEMO execution)

## Examples

```
from memo.io import load_ms2_data
from memo.fingerprints import compute_fingerprints
spectra = load_ms2_data('sample.mzML')
fingerprint = compute_fingerprints(spectra, normalize_by_sample_size=True)
```

## Evaluation signals

- Fingerprint vector length is consistent across all samples (same number of unique peaks and neutral losses counted).
- Peak and neutral loss counts are non-negative integers summing to approximately sample size × average spectrum complexity.
- Normalization by sample size produces values in [0, 1] range or interpretable relative frequency scale.
- Samples from the same experimental group cluster together after fingerprint alignment; samples from different groups show distinct separation.
- Fingerprint vectors contain no NaN or Inf values; numerical stability is maintained when comparing samples with vastly different spectrum counts.

## Limitations

- Neutral loss calculation depends on accurate precursor m/z assignment; errors propagate through loss aggregation.
- Aggregation discards temporal and spectral order information; samples with different fragmentation patterns but same peak/loss frequencies may be indistinguishable.
- Noise threshold for peak detection is not explicitly specified in the method description — threshold choice affects which fragments are counted and must be tuned for each MS instrument type.
- Sample size normalization assumes equal spectral quality across samples; highly contaminated or low-complexity samples may distort fingerprints.
- Performance depends on spec2vec embedding training data; fingerprints are meaningful only for fragment types seen during embedding training.

## Evidence

- [other] MS2 fingerprints are generated by counting the occurrence of MS2 peaks and neutral losses (relative to the precursor ion) in each sample, producing a numeric fingerprint representation.: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [other] Iterate through spectra in each sample and extract precursor m/z values; count occurrences of all MS2 peaks; calculate neutral losses by subtracting fragment m/z from precursor m/z; aggregate across all spectra within each sample.: "1. Load MS2 spectra files using matchms to parse fragmentation data. 2. Iterate through spectra in each sample and extract precursor m/z values. 3. Count occurrences of all MS2 peaks (m/z values"
- [readme] MEMO suits particularly well to compare chemodiverse samples with poor feature overlap or strong retention time shifts across different LC methods and mass spectrometer technologies.: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [readme] matchms is built primarily on matchms and spec2vec packages for handling MS2 spectra parsing and vectorization.: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [other] Fingerprints are normalized by sample size to produce the final numeric representation.: "Generate a numeric fingerprint vector per sample combining peak and neutral loss occurrence counts, normalized by sample size."
