---
name: neutral-loss-calculation-from-precursor
description: Use when when converting MS/MS spectra into spectral documents for Spec2Vec embedding, and you want to capture chemical relationships implicit in the fragmentation pattern (e.g., loss of water, ammonia, or CO2) that may correlate with structural similarity. Use this when the neutral loss range (5.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - gensim
  - matchms
  - Numba
  - Pandas
  - Word2Vec
  - spec2vec
  - Python 3.8
  - numpy
  - MEMO
  - memo-ms
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
- doi: 10.3389/fbinf.2022.842964
  title: ''
evidence_spans:
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  - build: coll_memo
    doi: 10.3389/fbinf.2022.842964
    title: memo
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
---

# neutral-loss-calculation-from-precursor

## Summary

Calculate neutral loss peaks from MS/MS spectra by subtracting each fragment m/z from the precursor m/z, then represent these losses as vocabulary words for Word2Vec embedding in spectral document construction. This enriches spectral documents with chemical fragmentation information beyond direct fragments alone.

## When to use

When converting MS/MS spectra into spectral documents for Spec2Vec embedding, and you want to capture chemical relationships implicit in the fragmentation pattern (e.g., loss of water, ammonia, or CO2) that may correlate with structural similarity. Use this when the neutral loss range (5.0–200.0 Da) is likely to contain informative losses for your molecule class and you have a precursor m/z available.

## When NOT to use

- Input is GC-MS data where neutral losses are usually not measured and fragmentation patterns differ fundamentally from LC-MS.
- Precursor m/z is unavailable or unreliable; neutral loss calculation depends entirely on accurate precursor mass.
- The molecule class or adduct type produces fragments predominantly outside the 5.0–200.0 Da loss range; losses will be sparse and uninformative.

## Inputs

- MS/MS spectrum (precursor m/z and list of fragment peaks with m/z and intensity)
- Pre-processed peak list (m/z values binned to 2 decimal places, intensity normalized)
- Precursor mass (required to calculate neutral losses)

## Outputs

- List of neutral loss tokens ('[redacted-email]') for the spectrum
- Augmented spectrum document (combined peak and loss tokens ready for Word2Vec embedding)
- Missing fraction metric (fraction of spectrum intensity not represented in trained model)

## How to apply

For each peak in a pre-processed MS/MS spectrum, compute the neutral loss as (precursor m/z − peak m/z). Retain only losses within the range 5.0–200.0 Da, as smaller values are noise and larger values are beyond typical fragment mass differences. Represent each loss as a word token '[redacted-email]' using the same decimal precision (2 decimal places, binned m/z) as peak tokens. Include these loss tokens alongside peak tokens ('[redacted-email]') in the assembled spectrum document. Weight both peak and loss words by the square root of normalized peak intensity when aggregating into the final spectrum vector. Filter out spectra where the missing fraction (proportion of spectrum intensity from unknown peaks/losses not covered by the Word2Vec model) exceeds a threshold (e.g., 0.05) to avoid poor embeddings.

## Related tools

- **Word2Vec** (Learns embeddings of peak and loss tokens from spectral documents; neutral losses are treated as vocabulary words alongside peaks)
- **spec2vec** (Reference implementation that computes neutral losses and incorporates them into spectrum documents for Spec2Vec similarity scoring) — https://github.com/iomega/spec2vec
- **matchms** (Python package providing spectrum I/O, preprocessing, peak filtering, and neutral loss calculation implementations) — https://github.com/matchms/matchms
- **gensim** (Underlying library providing Word2Vec implementation used to train embeddings on assembled spectrum documents)

## Examples

```
from matchms import Spectrum; from spec2vec import Spec2VecModified; precursor_mz = 500.25; peaks = [(100.05, 10), (150.10, 20), (485.20, 15)]; losses = [precursor_mz - mz for mz, _ in peaks if 5.0 <= precursor_mz - mz <= 200.0]; print(f"Neutral losses: {losses}")
```

## Evaluation signals

- Verify that all neutral loss values fall within the range [5.0, 200.0] Da; losses outside this range should be absent from the final spectrum document.
- Check that loss tokens are formatted consistently as '[redacted-email]' with exactly 2 decimal places, matching the precision of peak tokens.
- Confirm that the number of loss tokens per spectrum is plausible (typically 5–50 losses depending on precursor mass and fragment density); suspiciously high counts may indicate double-counting or binning errors.
- Verify that missing fraction is calculated as the sum of normalized intensities of peaks/losses absent from the Word2Vec vocabulary, and that spectra with missing_fraction ≥ 0.05 are filtered out before computing similarity scores.
- Spot-check a sample spectrum: manually verify that a few neutral losses (e.g., precursor 500.2 with peak 485.1 should yield loss 15.1) are correctly computed and represented in the document.

## Limitations

- Neutral losses are only meaningful for LC-MS data; GC-MS spectra do not typically exhibit measured neutral loss peaks, limiting applicability.
- Neutral loss information is sensitive to precursor mass accuracy; errors in precursor m/z (>2 ppm) can cause losses to fall outside the learned Word2Vec vocabulary or to be misaligned across spectra.
- The fixed range [5.0, 200.0] Da may miss informative losses for extreme molecule masses; very large molecules or specialized fragmentation patterns may benefit from tuning this threshold.
- Spec2Vec performance depends on a pre-trained Word2Vec model; if the training dataset does not contain sufficient examples of fragment–loss patterns for your target molecules, retraining on new data may be required.
- The missing fraction threshold (e.g., <0.05) is heuristic; spectra with high missing fractions may still produce usable embeddings but with higher uncertainty.

## Evidence

- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak: "neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak"
- [full_text] Spec2Vec converts spectra into documents by representing each peak as a word ("[redacted-email]") and adding neutral losses ("[redacted-email]") between 5.0–200.0 Da calculated as precursor − peak. The spectrum is then represented as a low-dimensional vector calculated as the weighted sum of all its fragment and loss vectors from a trained Word2Vec model.: "weighted sum of all its fragment and loss vectors from a trained Word2Vec model"
- [full_text] For each spectrum, compute a weighted spectrum vector as the sum of Word2Vec word embeddings, weighted by the square root of normalized peak intensity.: "weighted by the square root of normalized peak intensity"
- [methods] By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided: "By setting a threshold for the missing fraction (e.g. <0.05), returning Spec2Vec similarity scores for spectra far outside the learned peaks (and losses) can be avoided"
- [discussion] For GC-MS, neutral losses are usually not measured.: "For GC-MS, neutral losses are usually not measured."
- [readme] spec2vec does so for mass fragments and neutral losses in MS/MS spectra. The spectral similarity score is based on spectral embeddings learnt from the fragmental relationships within a large set of spectral data.: "does so for mass fragments and neutral losses in MS/MS spectra"
