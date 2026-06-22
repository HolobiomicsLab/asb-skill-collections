---
name: spectral-corpus-representation
description: Use when you have a collection of tandem mass spectrometry spectra in mzML or similar format and need to prepare them for LDA-based motif discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
  - Python
  - MS2LDA.Preprocessing
  - Conda
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Apply LDA to the processed spectra
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# spectral-corpus-representation

## Summary

Convert tandem mass spectrometry (MS/MS) spectra into a bag-of-fragments corpus representation suitable for unsupervised topic modeling. This preprocessing step transforms raw spectral data into a format that encodes fragment masses and neutral losses as discrete tokens, enabling Latent Dirichlet Allocation to discover recurring fragmentation patterns without prior compound identification.

## When to use

You have a collection of tandem mass spectrometry spectra in mzML or similar format and need to prepare them for LDA-based motif discovery. This skill is necessary when your goal is to identify recurring substructures (Mass2Motifs) across a spectral dataset and you require a token-based representation that treats fragments and losses as vocabulary items for topic modeling.

## When NOT to use

- Spectra are already in a pre-computed feature matrix or abundance table format (e.g., ready for direct statistical modeling)
- Your analysis goal is compound identification rather than de novo substructure discovery — use spectral library search or MS/MS matching instead
- Spectra contain ambiguous or severely fragmented precursor ions that cannot be reliably attributed to specific neutral losses

## Inputs

- preprocessed MS/MS spectra (mzML or converted format)
- spectral metadata (scan identifiers, precursor masses, collision energies)
- instrument-specific mass accuracy parameters (ppm tolerance)

## Outputs

- bag-of-fragments corpus (sparse matrix or MS2LDA-compatible format)
- fragment/loss vocabulary (token-to-mass mapping)
- filtered spectral dataset (noise and low-intensity fragments removed)

## How to apply

Load preprocessed spectra (converted to a standard format) and apply MS2LDA's Preprocessing module to filter and clean spectra for the ion mode of interest (positive or negative). Extract neutral losses and convert each spectrum into a bag-of-fragments vector, where each fragment mass and neutral loss is treated as a token. Filter out noise by applying mass tolerance windows and intensity thresholds to exclude low-abundance artifacts. Serialize the resulting corpus in the format expected by MS2LDA.modeling (typically a matrix or sparse representation where rows are spectra and columns are fragment/loss tokens with their counts). The corpus is then ready for LDA model initialization and training.

## Related tools

- **MS2LDA.Preprocessing** (Core module that implements load_and_clean, fragment extraction, neutral loss calculation, and noise filtering to generate the bag-of-fragments representation) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming environment for configuring PYTHONPATH and invoking MS2LDA.Preprocessing functions to construct and serialize the corpus)
- **Conda** (Environment manager used to configure the Python environment and activate the MS2LDA package dependencies)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean; corpus = load_and_clean('spectra.mzML', ion_mode='positive', ppm_tolerance=5, min_intensity=50)
```

## Evaluation signals

- The generated corpus has non-zero fragment/loss token counts for each spectrum; check that no spectra are reduced to empty vectors
- The vocabulary size and token distribution are consistent with the input spectral dataset size and expected fragmentation complexity
- Noise filtering has removed low-intensity artifacts: compare pre- and post-filtering fragment count distributions and verify that spurious m/z peaks are excluded
- The serialized corpus format (matrix dimensions, sparsity, token counts) matches MS2LDA.modeling's expected input schema
- Manual inspection of a sample of spectra confirms that major fragments and known neutral losses (e.g., H₂O, NH₃, CO₂) are preserved and tokenized correctly

## Limitations

- Bag-of-fragments representation loses positional and intensity-rank information; fragments are treated as unordered counts rather than sequential fragmentation patterns
- Mass tolerance parameters (ppm) must be carefully tuned to the instrument's accuracy; miscalibration can lead to fragmentation artifacts or merger of distinct peaks
- Spectra with very few fragments or very high noise levels may be underdimensional after filtering, reducing their informativeness for LDA inference
- Ion mode (positive vs. negative) must be correctly specified; mixing ion modes without separate corpus construction can confound motif discovery

## Evidence

- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
- [methods] Extract neutral losses: "Extract neutral losses"
- [other] Load the preprocessed bag-of-fragments corpus (generated by the Preprocessing module) in the format expected by MS2LDA.modeling: "Load the preprocessed bag-of-fragments corpus (generated by the Preprocessing module) in the format expected by MS2LDA.modeling"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
