---
name: neutral-loss-extraction-and-weighting
description: Use when you have a collection of annotated MS/MS spectra with precursor
  m/z values and fragment peak lists, and you aim to train or apply a spectral similarity
  model (such as Spec2Vec Word2Vec) that exploits fragmentation chemistry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Spec2Vec
  - matchms
  - gensim
  - NumPy
  - Numba
  - Pandas
  - Word2Vec
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- we introduce Spec2Vec, a novel spectral similarity score
- spec2vec (https://github.com/iomega/spec2vec). Both packages are freely available
  and can be installed via conda
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can
  be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim
  [37]
- Spec2Vec was optimised by making extensive use of Numpy [24]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neutral-loss-extraction-and-weighting

## Summary

Extract neutral losses (mass differences between precursor and fragment ions) from MS/MS spectra and encode them as weighted features for spectral embedding and similarity scoring. This skill is essential for capturing diagnostic fragmentation patterns that inform structural relationships beyond peak m/z alone.

## When to use

You have a collection of annotated MS/MS spectra with precursor m/z values and fragment peak lists, and you aim to train or apply a spectral similarity model (such as Spec2Vec Word2Vec) that exploits fragmentation chemistry. Neutral losses are especially informative when comparing spectra of molecules with high structural similarity but differing in multiple locations, where cosine-based scores often fail.

## When NOT to use

- GC-MS data: neutral losses are usually not reliably measured in gas chromatography–mass spectrometry, limiting their diagnostic value.
- Spectra without precursor m/z annotation: loss calculation requires accurate precursor mass.
- When comparing spectra using only m/z matching (cosine score): neutral loss features are redundant if you do not intend to learn structural embeddings.

## Inputs

- MS/MS spectra with precursor m/z and fragment peaks
- Fragment peak list (m/z, intensity tuples) per spectrum
- Peak intensity vector normalized or raw

## Outputs

- Spectrum document with peak and neutral loss tokens
- Weighted token list (words + intensities) for Word2Vec input
- Spectral embeddings capturing fragmentation relationships

## How to apply

For each spectrum, calculate neutral losses as the mass difference between the precursor m/z and each observed fragment peak (loss = precursor − fragment). Represent each neutral loss as a text token (e.g., '[redacted-email]') with 2-decimal binning precision, analogous to peak representation ('[redacted-email]'). Weight each loss token by the intensity of the corresponding fragment peak, then normalize peak and loss intensities to a maximum of 1.0 per spectrum. Include only neutral losses in the range 5.0–200.0 Da, as smaller differences may be noise and larger values typically represent implausible fragments. Combine the weighted peak and loss tokens into a single spectrum document for Word2Vec training, ensuring that fragmentation relationships are learned from the joint feature space.

## Related tools

- **Spec2Vec** (consumes neutral loss tokens and learns embeddings that encode fragmentation chemistry) — https://github.com/iomega/spec2vec
- **Word2Vec** (learns distributed representations of peak and neutral loss tokens from spectral documents)
- **matchms** (provides spectral data structures and utilities for peak filtering and metadata management prior to neutral loss extraction) — https://github.com/matchms/matchms
- **gensim** (implements the Word2Vec model that consumes token documents with neutral loss and peak representations)

## Examples

```
from matchms import Spectrum; spectrum = Spectrum(mz=[100, 150, 200], intensities=[1.0, 0.5, 0.3], metadata={'precursor_mz': 300}); neutral_losses = [300 - mz for mz in spectrum.mz if 5.0 <= 300 - mz <= 200.0]; loss_tokens = [f'loss@{loss:.2f}' for loss in neutral_losses]; peak_tokens = [f'peak@{mz:.2f}' for mz in spectrum.mz]; spectrum_document = loss_tokens + peak_tokens
```

## Evaluation signals

- Verify that neutral loss range (5.0–200.0 Da) is respected: check that no loss tokens fall outside this window.
- Confirm peak and loss intensity normalization: all spectra should have max intensity ≤ 1.0 and min ≥ 0.0.
- Validate token count and format: all neutral loss tokens match the pattern '[redacted-email]' with exactly 2 decimal places.
- Check missing-fraction coverage: calculate the fraction of spectrum tokens (peaks + losses) with known Word2Vec embeddings; high coverage (e.g., >95%) indicates good feature representation.
- Compare structural similarity rank correlation: Spec2Vec similarity scores computed on neutral loss–aware embeddings should correlate more strongly with structural similarity (InChIKey overlap) than cosine-based scores.

## Limitations

- Spec2Vec requires a large, representative training corpus to learn robust fragmentation relationships; models trained on small or narrow compound sets may have poor generalization.
- Unknown neutral losses not present in the trained Word2Vec model contribute to the 'missing fraction' and reduce confidence in similarity scores; this is especially problematic for rare or novel fragmentation patterns.
- GC-MS data are not suitable because neutral losses are typically not directly measured or reliably inferred; the method is validated only on LC-MS datasets.
- Neutral loss extraction assumes accurate precursor m/z annotation; errors in precursor mass propagate directly into loss calculations and corrupt the learned embeddings.
- Neutral loss features improve structural similarity correlation but do not eliminate the need for retraining on new, structurally distinct datasets with unfamiliar fragmentation patterns.

## Evidence

- [methods] In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak: "In addition to all peaks of a spectrum, neutral losses between 5.0 and 200.0 Da were added as "[redacted-email]". Neutral losses are calculated as precursor − peak"
- [methods] After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]"): "After processing, spectra are converted to documents. For this, every peak is represented by a word that contains its position up to a defined decimal precision ("[redacted-email]")"
- [other] Normalize peak intensities to maximum = 1 for each spectrum: "Normalize peak intensities to maximum = 1 for each spectrum"
- [other] For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words.: "For each spectrum, convert peaks to words with format '[redacted-email]' (2-decimal binning) and add neutral losses (5.0–200.0 Da) as '[redacted-email]' words."
- [intro] Building on that insight, we present a novel spectral similarity score based upon learnt embeddings of spectra. Instead inspired by the success of algorithms from the field of natural language: "Building on that insight, we present a novel spectral similarity score based upon learnt embeddings of spectra. Instead inspired by the success of algorithms from the field of natural language"
- [discussion] For GC-MS, neutral losses are usually not measured.: "For GC-MS, neutral losses are usually not measured."
- [discussion] one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships; however, since this not necessarily needs to be library spectra and in: "one limitation of Spec2Vec as compared to cosine scores is that it needs training data to learn the fragment peak relationships"
