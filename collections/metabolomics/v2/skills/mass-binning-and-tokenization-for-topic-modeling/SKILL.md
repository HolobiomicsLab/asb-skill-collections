---
name: mass-binning-and-tokenization-for-topic-modeling
description: Use when you have extracted and intensity-normalized fragment ion masses and neutral loss values from MS/MS spectra and need to prepare them for unsupervised topic modeling to discover recurring fragmentation motifs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
  - Latent Dirichlet Allocation (LDA)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- from MS2LDA.Preprocessing import load_and_clean
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- These steps assume you have Conda installed
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-binning-and-tokenization-for-topic-modeling

## Summary

Convert normalized MS/MS fragment ion masses and neutral losses into discrete mass tokens (bins) suitable for Latent Dirichlet Allocation topic modeling. This discretization step bridges raw spectral data and the bag-of-fragments document representation required by LDA-based motif discovery.

## When to use

Apply this skill when you have extracted and intensity-normalized fragment ion masses and neutral loss values from MS/MS spectra and need to prepare them for unsupervised topic modeling to discover recurring fragmentation motifs. The input should be a collection of mass values (both fragment ions and calculated neutral losses) with associated intensity measures, and your goal is to identify hidden substructure patterns without prior compound identification.

## When NOT to use

- Input spectra are already in a pre-processed bag-of-words or document-term matrix format — skip directly to LDA modeling.
- Your analysis goal is spectrum-to-spectrum similarity matching or library searching rather than unsupervised motif discovery across a large dataset.
- Fragment mass accuracy and assignment are uncertain or have not been validated; binning will propagate assignment errors into the token vocabulary.

## Inputs

- Extracted fragment ion masses per spectrum (floating-point m/z values)
- Calculated neutral loss masses for all observed fragment pairs
- Peak intensity values associated with each fragment and loss
- Minimum intensity threshold or statistical significance cutoff (numeric)

## Outputs

- Discretized bag-of-fragments corpus (document-term matrix or serialized equivalent)
- Binned mass token vocabulary (mapping of discrete bins to mass ranges)
- Filtered token counts per spectrum (integer matrix suitable for LDA input)

## How to apply

After extracting fragment ion masses and calculating neutral loss values for all observed fragment pairs in each spectrum, bin the continuous mass values into discrete mass tokens using a binning scheme that balances mass resolution with statistical power for LDA inference. Filter out fragments and losses below a minimum intensity threshold or statistical significance cutoff to reduce noise. The binning process groups masses within predefined mass windows (e.g., integer bins or bins defined by mass accuracy tolerance) so that each spectrum is represented as a discrete bag-of-token counts rather than continuous mass values. This discretization enables LDA to treat fragmentation patterns as word-like tokens that can be grouped into topics (Mass2Motifs) across multiple spectra. The resulting corpus is a document-term matrix where documents are individual spectra, terms are mass tokens, and values are token counts.

## Related tools

- **MS2LDA.Preprocessing.generate_corpus** (Performs binning of fragments and losses into discrete mass tokens and generates the final bag-of-fragments corpus representation for LDA input) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA.Preprocessing.load_and_clean** (Loads and normalizes MS/MS spectra before mass extraction and binning) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Topic modeling algorithm that consumes the binned token corpus to infer Mass2Motifs from fragmentation patterns)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus
spectra = load_and_clean('compounds.mgf')
corpus = generate_corpus(spectra, min_intensity_threshold=10, mass_bin_width=1.0)
```

## Evaluation signals

- Verify that the output corpus is a valid document-term matrix (number of documents matches input spectrum count, term vocabulary size is consistent across documents, all values are non-negative integers).
- Confirm that binned tokens are discrete and reproducible — rerunning the binning on the same input produces identical token assignments and counts.
- Check that filtering removed only tokens below the specified intensity threshold; inspect histograms of token intensity before and after filtering to confirm appropriate noise reduction.
- Validate that the token vocabulary covers the expected m/z range for the instrument and compound class being studied (e.g., singly-charged ions for small molecules typically span 50–2000 m/z).
- Run LDA on the generated corpus and verify that inferred Mass2Motifs correspond to known fragmentation patterns (e.g., loss of water, loss of CO₂, neutral losses characteristic of functional groups) for validation compounds.

## Limitations

- Binning resolution is a critical parameter: coarse bins merge distinct fragments and reduce sensitivity to specific structural features, while fine bins increase sparsity and may oversegment noise. The article does not specify a default bin width; practitioners must determine this empirically or based on instrument mass accuracy.
- Neutral loss calculation assumes all observed fragment pairs represent meaningful chemical losses; abundant noise fragments may generate spurious loss values that are difficult to filter out.
- Intensity-based filtering thresholds are data- and instrument-dependent; no universal cutoff is provided in the article. Under-filtering retains noise; over-filtering may discard genuine low-abundance diagnostic losses.
- The bag-of-fragments representation discards peak intensity information after filtering, treating all tokens equally in the LDA model; intensity variation is not directly modeled.

## Evidence

- [other] The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling.: "The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling."
- [other] Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens.: "Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens."
- [other] Extract fragment ion masses and normalize peak intensities within each spectrum.: "Extract fragment ion masses and normalize peak intensities within each spectrum."
- [other] Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff.: "Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff."
- [readme] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
- [readme] identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
