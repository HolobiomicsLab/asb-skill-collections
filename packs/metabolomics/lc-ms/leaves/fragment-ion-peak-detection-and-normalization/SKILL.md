---
name: fragment-ion-peak-detection-and-normalization
description: Use when immediately after loading raw MS/MS spectra from .mgf, .msp,
  or .mzML files, before generating the bag-of-fragments corpus or extracting neutral
  losses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely
  to explain the observed fragmentation patterns
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-peak-detection-and-normalization

## Summary

Detect fragment ion m/z peaks in tandem mass spectrometry spectra and normalize their intensities to a common scale, preparing individual spectra for bag-of-fragments corpus generation. This is the foundational processing step that converts raw MS/MS peak lists into normalized, noise-filtered representations suitable for topic modeling.

## When to use

Apply this skill immediately after loading raw MS/MS spectra from .mgf, .msp, or .mzML files, before generating the bag-of-fragments corpus or extracting neutral losses. Use it whenever you have unprocessed tandem mass spectrometry data and need to prepare it for unsupervised motif discovery via LDA or other statistical analysis that requires uniform intensity scaling across spectra.

## When NOT to use

- Input is already a processed bag-of-fragments or document-term matrix — skip to LDA modeling.
- Spectra have already been intensity-normalized by the instrument software and you are working with pre-processed vendor output designed for immediate motif analysis.
- Your analysis goal requires preserves absolute intensity information for quantitative comparison; normalization loses this information.

## Inputs

- Raw MS/MS spectra in .mgf format
- Raw MS/MS spectra in .msp format
- Raw MS/MS spectra in .mzML format
- Peak list with m/z values and intensities per spectrum

## Outputs

- Normalized peak list per spectrum (m/z and relative intensity pairs)
- Filtered fragment ion masses above noise threshold
- Intensity-normalized spectrum ready for neutral loss extraction

## How to apply

Load each MS/MS spectrum using MS2LDA.Preprocessing.load_and_clean, which handles multiple input formats. Extract all fragment ion m/z values and their corresponding intensity measurements from the spectrum. Normalize peak intensities within each spectrum to a common scale (typically relative intensity 0–100 or 0–1), which ensures that high-intensity peaks in one spectrum do not dominate learning relative to lower-intensity peaks in another. Remove peaks below a minimum intensity threshold or statistical significance cutoff to eliminate instrument noise. This normalized peak list forms the basis for subsequent neutral loss calculation and corpus generation. The rationale is that intensity normalization makes fragmentation patterns comparable across different acquisition conditions and spectral qualities, while noise filtering reduces spurious fragment masses that would otherwise degrade motif quality.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Load raw MS/MS spectra in multiple formats (.mgf, .msp, .mzML) and perform initial cleaning to extract and normalize fragment ion peaks) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Framework within which preprocessing and peak normalization are integrated as the first workflow stage) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Programming language for implementing peak detection and intensity normalization logic)
- **Conda** (Environment manager to provision MS2LDA and its dependencies for peak processing)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean; spectra = load_and_clean('data.mgf', min_intensity=10, normalize=True)
```

## Evaluation signals

- All peaks in a normalized spectrum have intensities in the range [0, 100] or [0, 1] after normalization.
- Noise filtering removes peaks below the specified minimum intensity threshold; verify that the fraction of peaks retained is consistent with typical MS/MS spectral complexity (e.g., 5–50 significant peaks per spectrum).
- No m/z values are duplicated or out of chemical range (typically 50–2000 m/z for small molecules).
- The distribution of normalized intensities across the dataset is roughly comparable across spectra of different precursor masses, indicating successful intensity normalization.
- Downstream neutral loss calculation produces valid losses (positive mass differences between detected fragments) without NaN or invalid values.

## Limitations

- Intensity normalization discards absolute quantitative information; if you need to compare absolute peak heights across samples, this skill is not appropriate.
- The choice of minimum intensity threshold is heuristic and may remove low-abundance but structurally informative fragments; threshold tuning requires empirical validation against known standards.
- Load_and_clean assumes standardized spectrum metadata (e.g., precursor m/z, charge state) in the input file; malformed or missing metadata may cause silent failures or incorrect peak assignment.
- Overlapping or very closely-spaced peaks (within instrument mass resolution) may not be resolved as separate fragments; MS/MS data quality and instrument resolution limit the fineness of peak detection.

## Evidence

- [methods] Extract fragment ion masses and normalize peak intensities within each spectrum.: "Extract fragment ion masses and normalize peak intensities within each spectrum."
- [methods] Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module.: "Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module."
- [methods] Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff.: "Filter noise by removing fragments and losses below a minimum intensity threshold or statistical significance cutoff."
- [methods] from MS2LDA.Preprocessing import load_and_clean: "from MS2LDA.Preprocessing import load_and_clean"
- [methods] Convert MS/MS spectra into a bag-of-fragments format: "Convert MS/MS spectra into a bag-of-fragments format"
