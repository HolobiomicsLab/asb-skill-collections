---
name: mass-spectrum-preprocessing-and-normalization
description: Use when when you have raw MS/MS spectra in MGF or mzML/mzXML formats and need to feed them into Casanovo or similar transformer-based de novo sequencing models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Casanovo
  - PyTorch
  - DepthCharge
  - CUDA Toolkit
  - napari
  - Python
  - MSI-Explorer
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
- doi: 10.1021/acs.analchem.5c01513
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
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_casanovo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-49731-x
  all_source_dois:
  - 10.1038/s41467-024-49731-x
  - 10.1093/bib/bbac542
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-preprocessing-and-normalization

## Summary

Preprocessing and normalization of MS/MS spectra converts raw peak data into a standardized, high-quality format suitable for de novo peptide sequencing inference. This step removes noise, filters low-quality scans, normalizes peak intensities, and retains only the most informative peaks to maximize downstream transformer model performance.

## When to use

When you have raw MS/MS spectra in MGF or mzML/mzXML formats and need to feed them into Casanovo or similar transformer-based de novo sequencing models. Apply this skill before spectrum encoding and neural network inference, especially when working with monoclonal antibody assembly, immunopeptidomics, metaproteomics, or other settings where you need to identify peptides not in a protein database.

## When NOT to use

- Spectra are already preprocessed and normalized by the acquisition instrument or a prior pipeline step.
- Your downstream analysis requires preservation of all detected peaks, including low-intensity noise, for statistical or uncertainty quantification purposes.
- Input spectra are already encoded in a deep learning-friendly format (e.g., DepthCharge tensors); preprocessing has already occurred upstream.

## Inputs

- Annotated MS/MS spectra in MGF format
- Annotated MS/MS spectra in mzML format
- Annotated MS/MS spectra in mzXML format
- Raw peak intensity arrays
- Scan-level metadata (precursor m/z, charge state)

## Outputs

- Normalized peak intensity arrays
- Filtered spectrum objects (low-quality scans removed)
- Peak-selected spectra (top max_peaks retained per scan)
- Preprocessed spectra ready for encoder–decoder input

## How to apply

Load annotated MS/MS spectra from MGF or mzML/mzXML peak files using Casanovo's built-in spectrum reader. Normalize peak intensities across each spectrum to a consistent scale. Filter out low-quality scans by rejecting spectra with fewer peaks than the min_peaks threshold (a configurable quality gate). Retain only the top max_peaks peaks per spectrum, ordered by intensity, to reduce noise while preserving the strongest signal for peptide identification. These filtered, normalized spectra are then encoded (e.g., via DepthCharge with sinusoidal positional encoding) before transformer encoder–decoder inference. The rationale is that normalized, peak-selected spectra improve model robustness by focusing computational resources on the most informative peaks and eliminating unreliable low-abundance noise.

## Related tools

- **Casanovo** (Provides integrated spectrum reader and preprocessing pipeline for MS/MS data ingestion and normalization) — https://github.com/Noble-Lab/casanovo
- **DepthCharge** (Encodes preprocessed spectra using sinusoidal positional encoding of m/z and intensity values for transformer input)
- **PyTorch** (Underlying framework for tensor operations and GPU-accelerated preprocessing computations)
- **CUDA Toolkit** (Enables GPU-accelerated preprocessing operations for high-throughput spectrum normalization)

## Evaluation signals

- Verify that all spectra meet the min_peaks threshold after filtering; confirm no spectra with fewer peaks than the cutoff remain in the dataset.
- Check that peak intensity distributions are normalized to a consistent scale (e.g., 0–1 or unit norm) across all spectra; histogram or quantile plots should show similar distributions.
- Confirm that each spectrum retains exactly max_peaks or fewer peaks (whichever is smaller), ranked by descending intensity.
- Validate that preprocessed spectra pass downstream DepthCharge encoding without shape or value errors, and that transformer encoder accepts the encoded tensors without dimension mismatches.
- Compare de novo peptide sequencing accuracy (amino acid recall, peptide-spectrum match rates) before and after preprocessing; significant improvements indicate preprocessing is beneficial and correctly configured.

## Limitations

- The min_peaks and max_peaks thresholds are user-configurable; poorly chosen thresholds can discard informative spectra or retain too much noise, degrading downstream predictions.
- Normalization strategies (e.g., intensity scaling, log transformation) can interact with the transformer model's learned representations; insufficient tuning may reduce model calibration.
- Preprocessing assumes spectra are properly annotated with precursor m/z and charge state; malformed or missing metadata will cause spectrum reader failures.
- Peak filtering based on intensity rank alone does not account for spectral context (e.g., isotope patterns, neutral loss signatures); overly aggressive filtering may remove diagnostic ions.
- Preprocessing does not correct for systematic instrument artifacts, miscalibration, or contaminant ions; upstream instrument QC and decontamination may be needed for low-quality datasets.

## Evidence

- [full_text] Load annotated MS/MS spectra from an MGF or mzML/mzXML peak file using Casanovo's built-in spectrum reader.: "Load annotated MS/MS spectra from an MGF or mzML/mzXML peak file using Casanovo's built-in spectrum reader."
- [full_text] Normalize intensities, filtering low-quality scans (fewer than min_peaks threshold), and retaining only the top max_peaks peaks per spectrum.: "normalize intensities, filtering low-quality scans (fewer than min_peaks threshold), and retaining only the top max_peaks peaks per spectrum"
- [full_text] Encode spectra using DepthCharge, applying sinusoidal positional encoding to m/z values and intensities.: "Encode spectra using DepthCharge, applying sinusoidal positional encoding to m/z values and intensities."
- [full_text] Casanovo uses a transformer neural network to translate peaks in MS/MS spectra into amino acid sequences.: "Casanovo uses a transformer neural network to translate peaks in MS/MS spectra into amino acid sequences."
- [readme] Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset: "Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset"
