---
name: spectral-peak-filtering-by-quality-threshold
description: Use when you have raw or annotated MS/MS spectra (in MGF, mzML, or mzXML format) destined for de novo peptide sequencing with Casanovo. Use it specifically when your dataset contains variable spectral quality (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Casanovo
  - PyTorch
  - DepthCharge
  - CUDA Toolkit
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
evidence_spans:
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing.
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing
- Pytorch is installed automatically when installing Casanovo
- Upgraded minimum Lightning version to 2.6.
- Upgraded minimum DepthCharge version to 0.4.10.
- Install the latest version of the NVIDIA drivers using the official CUDA Toolkit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_casanovo_cq
    doi: 10.1038/s41467-024-49731-x
    title: Casanovo
  dedup_kept_from: coll_casanovo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-49731-x
  all_source_dois:
  - 10.1038/s41467-024-49731-x
  - 10.1093/bib/bbac542
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-filtering-by-quality-threshold

## Summary

Filter MS/MS spectra by removing low-quality scans and retaining only the most intense peaks per spectrum to improve de novo peptide sequencing accuracy. This preprocessing step ensures that downstream transformer-based sequence prediction operates on high-signal-to-noise spectral data.

## When to use

Apply this skill when you have raw or annotated MS/MS spectra (in MGF, mzML, or mzXML format) destined for de novo peptide sequencing with Casanovo. Use it specifically when your dataset contains variable spectral quality (e.g., from complex samples, low-abundance peptides, or instrument variation) and you want to remove noisy or uninformative scans before neural network inference.

## When NOT to use

- Your spectra have already been preprocessed or quality-filtered by the instrument vendor or an upstream analysis pipeline.
- You are using targeted or data-independent acquisition (DIA) modes where spectrum structure differs fundamentally from data-dependent acquisition (DDA).
- Your research aims to detect or characterize low-abundance modifications or rare peptides that may be represented by weak peaks; aggressive max_peaks filtering could remove diagnostic signals.

## Inputs

- annotated MS/MS spectra (MGF format)
- annotated MS/MS spectra (mzML format)
- annotated MS/MS spectra (mzXML format)

## Outputs

- filtered MS/MS spectra (spectrum reader output)
- peak intensity-normalized spectra ready for DepthCharge encoding

## How to apply

Load annotated MS/MS spectra using Casanovo's built-in spectrum reader, then apply two sequential filters: (1) reject any scan with fewer than min_peaks threshold peaks (removing low-information spectra), and (2) retain only the top max_peaks peaks per spectrum by intensity (concentrating the model's attention on the strongest fragment ion signals). Normalize peak intensities before or during this filtering to ensure consistent scale across spectra. These thresholds are configurable via Casanovo's config.yaml; typical settings use min_peaks to exclude spectra with <10–20 peaks and max_peaks to cap analysis at 100–150 peaks per scan. The rationale is that transformer models trained on high-quality, curated spectra perform better when inference data is similarly preprocessed; retaining only intense peaks reduces computational overhead and noise.

## Related tools

- **Casanovo** (defines and enforces min_peaks and max_peaks filtering thresholds via its spectrum reader and config.yaml; orchestrates the full preprocessing pipeline) — https://github.com/Noble-Lab/casanovo
- **DepthCharge** (receives filtered, normalized peaks and applies sinusoidal positional encoding to m/z values and intensities for transformer input)
- **PyTorch** (underlying deep learning framework used by Casanovo to load and process filtered spectrum tensors)

## Evaluation signals

- Verify that all exported spectra in the output mzTab file contain ≥ min_peaks and ≤ max_peaks peaks (schema validation).
- Check that peak intensities are normalized to a consistent range (e.g., 0–1 or 0–100) across all spectra.
- Confirm that the number of scans retained after filtering matches expectations (e.g., if min_peaks=10 and your raw data has many <10-peak spectra, you should see a noticeable reduction in total scan count).
- Validate that the highest-intensity peaks are preserved in the output; low-intensity peaks should be absent when max_peaks < total input peaks per spectrum.
- Monitor downstream de novo sequencing accuracy (e.g., amino acid recall/precision or match to reference peptides); correctly filtered spectra should yield more confident predictions than unfiltered spectra.

## Limitations

- Setting min_peaks too high may exclude legitimate but sparse spectra from small peptides or low-abundance ions; conversely, setting it too low may retain noisy scans. No universal threshold is appropriate for all instruments or sample types.
- Retaining only the top max_peaks peaks may discard diagnostic peaks for post-translational modifications (PTMs) or unusual fragments that fall outside the intensity top-N. For modification-rich datasets (e.g., glycopeptides, phosphoproteins), aggressive filtering could reduce annotation accuracy.
- The filtering parameters are global; they do not adapt to per-spectrum signal-to-noise ratios or precursor abundance. Spectra from highly abundant peptides and rare peptides use identical thresholds.
- Normalized intensity values depend on the normalization method (e.g., total ion current, max-intensity baseline); different normalization schemes can produce different effective filtering results for the same peak-count thresholds.

## Evidence

- [other] Preprocess spectra by normalizing intensities, filtering low-quality scans (fewer than min_peaks threshold), and retaining only the top max_peaks peaks per spectrum.: "Preprocess spectra by normalizing intensities, filtering low-quality scans (fewer than min_peaks threshold), and retaining only the top max_peaks peaks per spectrum."
- [other] Load annotated MS/MS spectra from an MGF or mzML/mzXML peak file using Casanovo's built-in spectrum reader.: "Load annotated MS/MS spectra from an MGF or mzML/mzXML peak file using Casanovo's built-in spectrum reader."
- [other] Encode spectra using DepthCharge, applying sinusoidal positional encoding to m/z values and intensities.: "Encode spectra using DepthCharge, applying sinusoidal positional encoding to m/z values and intensities."
- [other] Casanovo uses a transformer neural network to translate peaks in MS/MS spectra into amino acid sequences.: "Casanovo uses a transformer neural network to translate peaks in MS/MS spectra into amino acid sequences."
- [readme] Pytorch is installed automatically when installing Casanovo: "Pytorch is installed automatically when installing Casanovo"
