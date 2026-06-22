---
name: bag-of-words-document-representation-generation
description: Use when you have raw MS/MS spectral data in standard mass spectrometry formats and need to prepare it for unsupervised substructure discovery via topic modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
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

# bag-of-words-document-representation-generation

## Summary

Convert tandem mass spectrometry (MS/MS) spectra into a bag-of-fragments corpus representation by extracting fragment ion masses, calculating neutral losses, filtering noise, and binning discrete mass tokens into a document-term matrix suitable for topic modeling. This preprocessing step transforms raw spectra from multiple file formats (.mgf, .msp, .mzML) into a machine-learning-ready input for Latent Dirichlet Allocation (LDA).

## When to use

Apply this skill when you have raw MS/MS spectral data in standard mass spectrometry formats and need to prepare it for unsupervised substructure discovery via topic modeling. Specifically, use it before LDA training to convert spectra into a bag-of-fragments corpus when you want to identify recurring fragmentation motifs (Mass2Motifs) without prior compound identification.

## When NOT to use

- Input is already a processed feature table or document-term matrix; re-binning would lose information.
- Spectra are from non-tandem (MS1-only) data; neutral loss extraction and fragmentation patterns require MS/MS data.
- Ion mode (positive vs. negative) has not been annotated; preprocessing requires mode-specific filtering to avoid cross-contamination.

## Inputs

- Raw MS/MS spectra in .mgf format (Mascot Generic Format)
- Raw MS/MS spectra in .msp format (NIST MS Search format)
- Raw MS/MS spectra in .mzML format (mzML XML format)
- Spectral metadata (precursor m/z, retention time, ion mode)

## Outputs

- Bag-of-fragments corpus (document-term matrix)
- Discrete mass tokens (binned fragment ion and neutral loss m/z values)
- Serialized corpus representation compatible with LDA model input
- Noise-filtered fragment and loss lists with intensity values

## How to apply

Load MS/MS spectra from input files (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module to extract fragment ion masses and normalize peak intensities within each spectrum. Calculate neutral loss values for all observed fragment pairs, then filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff to reduce spurious features. Finally, generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens and constructing a document-term matrix. The rationale is that this bag-of-words encoding (analogous to term frequency in text LDA) allows the topic model to discover latent motifs by learning which fragment and loss combinations co-occur across the spectral dataset.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Load and clean MS/MS spectra from multiple file formats; normalize peak intensities within each spectrum) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA.Preprocessing.generate_corpus** (Bin fragments and neutral losses into discrete mass tokens; generate document-term matrix corpus representation) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Framework that applies LDA to bag-of-fragments corpus to infer Mass2Motifs) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language for executing preprocessing module calls and corpus generation)
- **Conda** (Environment management for MS2LDA installation and dependency resolution)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus
spectra = load_and_clean('input_spectra.mgf', min_intensity=0.01, ion_mode='positive')
corpus = generate_corpus(spectra, fragment_bin_width=0.1, loss_bin_width=0.1)
```

## Evaluation signals

- Verify that all input spectra are successfully loaded and parsed; check that precursor m/z and fragment ion m/z values are within expected mass ranges (e.g., 0–2000 m/z for typical small-molecule MS).
- Confirm that peak intensity normalization produces spectra with maximum intensity = 1.0 or 100% relative intensity per spectrum.
- Check that neutral loss values are correctly calculated as differences between precursor m/z and fragment m/z, and that all losses are positive and less than precursor m/z.
- Validate that noise filtering reduces corpus sparsity and removes low-intensity artifacts; compare pre- and post-filter fragment/loss counts and intensity distributions.
- Inspect the output document-term matrix dimensions (n_spectra × n_mass_tokens) and verify that mass tokens are evenly distributed and that no single token dominates; confirm serialization format matches expected LDA input (e.g., gensim corpus or matrix format).

## Limitations

- Preprocessing quality depends on input file format correctness and completeness; malformed or incomplete .mgf/.msp/.mzML files may fail to parse or produce incomplete spectra.
- Neutral loss calculation assumes accurate precursor m/z annotation; incorrect or missing precursor m/z values will propagate errors into loss values and the final corpus.
- Noise filtering threshold selection (minimum intensity cutoff or statistical significance level) is data-dependent and requires tuning; overly aggressive filtering may remove genuine low-abundance fragments, while insufficient filtering retains noise and increases corpus dimensionality.
- Bag-of-fragments representation discards spectral ordering and intensity rank information, potentially losing fine-grained fragmentation sequence details that may be informative for some applications.
- The approach is designed for small-molecule tandem mass spectrometry; applicability to large biomolecules (proteins, peptides) or other MS modalities (MALDI, ETD, etc.) has not been tested in the provided materials.

## Evidence

- [other] The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling.: "The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling."
- [other] Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module."
- [other] Extract fragment ion masses and normalize peak intensities within each spectrum.: "Extract fragment ion masses and normalize peak intensities within each spectrum."
- [other] Calculate neutral loss values for all observed fragment pairs.: "Calculate neutral loss values for all observed fragment pairs."
- [other] Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff.: "Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff."
- [other] Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens.: "Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens."
- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
- [methods] Preprocessing → filter & clean your spectra (positive/negative ion mode): "Preprocessing → filter & clean your spectra (positive/negative ion mode)"
- [intro] identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
