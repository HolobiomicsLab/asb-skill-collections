---
name: ms2-peak-detection-and-counting
description: Use when you have raw MS2 spectral data (MGF, mzML, or msp format) and
  need to generate a sample-level fingerprint for comparison across metabolomics samples,
  especially when samples were acquired using different LC methods, mass spectrometer
  technologies, or exhibit poor feature overlap or large.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - matchms
  - spec2vec
  - Python 3.8
  - numpy
  - scikit-bio
  - memo-ms
  - MEMO
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra
- conda create --name memo python=3.8
- pip install numpy
- conda install -c conda-forge scikit-bio
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms2-peak-detection-and-counting

## Summary

Detect and count MS2 fragment peaks and neutral losses from raw fragmentation spectra to quantify the occurrence of each m/z value and derived neutral loss within a sample. This foundational operation transforms raw spectral data into numeric fingerprints for sample comparison.

## When to use

Apply this skill when you have raw MS2 spectral data (MGF, mzML, or msp format) and need to generate a sample-level fingerprint for comparison across metabolomics samples, especially when samples were acquired using different LC methods, mass spectrometer technologies, or exhibit poor feature overlap or large retention time shifts.

## When NOT to use

- Input is already a feature intensity table (e.g., aligned feature abundance matrix) without associated MS2 spectra—use MEMO only on raw spectral data or aligned tables paired with their corresponding fragmentation spectra.
- MS2 spectra are unavailable or insufficient in count (< 1–2 spectra per sample)—fingerprints require multiple fragmentation events to aggregate meaningful peak/loss distributions.
- Analysis goal is to match or identify compounds by spectral library search—use traditional spectral similarity (cosine, modified cosine) or database spectral matching instead.

## Inputs

- Raw MS2 spectra file (MGF, mzML, or msp format)
- Sample identifier or grouping metadata
- Precursor m/z list and fragment peak lists
- Instrument noise threshold (optional; defaults to matchms implementation)

## Outputs

- Per-sample MS2 fingerprint vector (numeric counts of peaks and neutral losses)
- MemoMatrix (feature × sample matrix of peak/neutral loss counts)
- Peak and neutral loss occurrence count tables

## How to apply

Load MS2 spectra files using matchms to parse fragmentation metadata and peak lists. Iterate through all spectra in each sample and extract the precursor m/z value. For each spectrum, count all observed MS2 peaks (m/z values above the instrument noise threshold). Calculate neutral losses by subtracting each observed fragment m/z from the precursor m/z. Count occurrences of all unique neutral losses per sample. Aggregate peak and neutral loss counts across all spectra within the sample using spec2vec document conversion or direct summation. Normalize counts by sample size or total spectral count to produce a numeric fingerprint vector combining peak and neutral loss occurrence frequencies. The resulting per-sample vectors can then be compared or aligned using distance or similarity metrics.

## Related tools

- **matchms** (Parses raw MS2 spectral files (MGF, mzML, msp) and filters peaks; provides API for iterating spectra and accessing precursor m/z and fragment lists) — https://github.com/matchms/matchms
- **spec2vec** (Performs document conversion (spectral embeddings based on fragment and neutral loss relationships) to aggregate and normalize peak/neutral loss counts across spectra) — https://github.com/iomega/spec2vec
- **memo-ms** (Implements the memo_from_aligned function to count MS2 peaks and neutral losses and construct the MemoMatrix directly from aligned feature tables and spectra) — https://github.com/mandelbrot-project/memo
- **numpy** (Efficient numeric array operations for aggregating and normalizing peak/neutral loss counts)
- **MEMO** (Overall MS2-based sample vectorization framework that orchestrates peak detection, counting, and fingerprint generation) — https://github.com/mandelbrot-project/memo

## Examples

```
from matchms.importing import load_from_mgf; from memo.memo import memo_from_aligned; spectra = list(load_from_mgf('samples.mgf')); memo_matrix = memo_from_aligned(spectra, feature_table='aligned_features.csv')
```

## Evaluation signals

- Verify that each peak count and neutral loss count is a positive integer and reflects the cumulative occurrences across all spectra in the sample.
- Check that the MemoMatrix has the correct dimensions: rows = unique peaks/neutral losses, columns = samples; verify presence of expected feature identifiers and sample names.
- Confirm that fingerprint vectors are normalized by sample size (e.g., divided by total spectral count) so that samples with different numbers of spectra are comparable.
- Cross-validate against reference outputs from memo_publication_examples repository to ensure reproducibility of fingerprint structure and content.
- Test that neutral loss values are reasonable (positive, less than or equal to precursor m/z) and that peak m/z values fall within the observed mass range of the instrument.

## Limitations

- Peak counting is sensitive to instrument noise threshold settings; peaks below the threshold are silently discarded, potentially losing low-abundance fragment information.
- Neutral loss aggregation assumes accurate precursor m/z assignment; errors in precursor detection propagate directly to neutral loss calculation.
- Method is agnostic to retention time, which prevents disambiguation of isomers or co-eluting compounds with identical MS2 fragmentation patterns.
- Fingerprints lose intensity information (all peaks are counted equally) and depend heavily on sample size normalization; samples with vastly different spectral depths may remain difficult to compare.
- Works best for chemodiverse samples with poor feature overlap; samples with strong feature conservation may show redundant peak counts and offer limited discrimination.

## Evidence

- [intro] The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an MS2 fingerprint of the sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint* of the sample"
- [other] Load MS2 spectra files using matchms to parse fragmentation data and iterate through spectra to extract precursor m/z and count peaks and neutral losses: "1. Load MS2 spectra files using matchms to parse fragmentation data. 2. Iterate through spectra in each sample and extract precursor m/z values. 3. Count occurrences of all MS2 peaks (m/z values"
- [other] Calculate neutral losses and aggregate counts using spec2vec document conversion: "4. Calculate neutral losses by subtracting observed fragment m/z from precursor m/z for each peak. 5. Count occurrences of all unique neutral losses per sample. 6. Aggregate peak and neutral loss"
- [intro] MEMO suits particularly well to compare chemodiverse samples with poor features overlap or strong RT shift across different LC methods and mass spectrometers: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift, acquired using different LC methods or even different mass"
- [other] memo_from_aligned function generates MemoMatrix by counting MS2 peak and neutral loss occurrences: "Execute the memo_from_aligned function from the memo-ms package to count MS2 peak and neutral loss occurrences across samples and construct the MemoMatrix"
- [readme] MEMO is mainly built on matchms and spec2vec packages for handling MS2 spectra: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
