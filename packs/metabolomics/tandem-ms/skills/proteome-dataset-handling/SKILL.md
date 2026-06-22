---
name: proteome-dataset-handling
description: 'Use when you have a collection of MS/MS spectra in MGF format and need to prepare them for GPU-based clustering. Dataset size and available GPU memory are critical: use GTX 1080Ti for smaller proteome datasets; use GTX 3090 for datasets like PXD000561 that exceed GTX 1080Ti capacity.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8+
  - HyperSpec
  - Python
  - CUDA
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00612
  title: HyperSpec
evidence_spans:
- HyperSpec requires `Python 3.8+` with `CUDA` environment
- HyperSpec requires `Python 3.8+` with `CUDA` environment.
- github.com__wh-xu__Hyper-Spec
- github.com/wh-xu/Hyper-Spec
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hyperspec_cq
    doi: 10.1021/acs.jproteome.2c00612
    title: HyperSpec
  dedup_kept_from: coll_hyperspec_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00612
  all_source_dois:
  - 10.1021/acs.jproteome.2c00612
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# proteome-dataset-handling

## Summary

Configure and load mass spectrometry proteome datasets (MGF format) into a GPU-accelerated clustering pipeline, matching dataset scale to available GPU memory (GTX 1080Ti for smaller datasets, GTX 3090 for large-scale datasets like PXD000561 with millions of spectra).

## When to use

You have a collection of MS/MS spectra in MGF format and need to prepare them for GPU-based clustering. Dataset size and available GPU memory are critical: use GTX 1080Ti for smaller proteome datasets; use GTX 3090 for datasets like PXD000561 that exceed GTX 1080Ti capacity. Preprocessing must normalize spectra by removing precursor peaks, filtering by intensity thresholds, and binning m/z values before encoding into hypervectors.

## When NOT to use

- Input spectra are already in hyperdimensional vector format or have been encoded by another method
- Dataset is smaller than a few thousand spectra and does not require GPU acceleration
- Spectra are in formats other than MGF (mzML, mzXML, or other formats must be converted first)

## Inputs

- Directory containing MGF files (mass spectrometry peak lists)
- ProteomeXchange dataset identifiers (e.g., PXD000561)
- Preprocessing parameter configuration (peak filtering, intensity scaling, tolerance values)

## Outputs

- Preprocessed spectra checkpoint file (HyperSpec checkpoint format)
- Encoded hypervectors in hyperdimensional space (binary representations)
- Dataset metadata: precursor m/z, charge state, retention time per spectrum

## How to apply

First, verify your GPU type matches the dataset scale (GTX 3090 for large datasets like PXD000561, GTX 1080Ti for smaller proteomes). Second, organize all MGF files in a single input directory. Third, execute the HyperSpec preprocessing pipeline with appropriate CPU core allocation (default: 6 cores) and filtering parameters: set --min_peaks to exclude low-quality spectra, --min_intensity to filter noise, --max_peaks_used to cap high-intensity peaks, and --remove_precursor_tol (typically 0.5 Da) to eliminate precursor contamination. Fourth, apply intensity scaling (root, log, rank, or off) based on your spectral characteristics. Finally, configure charge filtering (--cluster_charges 2 3) to focus on the most abundant charge states. The preprocessing stage projects spectra into normalized feature space before GPU-accelerated hyperdimensional encoding.

## Related tools

- **HyperSpec** (GPU-accelerated mass spectra clustering framework that loads and preprocesses MGF files into hyperdimensional space) — https://github.com/wh-xu/Hyper-Spec
- **Python** (Runtime environment for HyperSpec execution; version 3.8+ required)
- **CUDA** (GPU compute framework enabling GPU-accelerated preprocessing and clustering)

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --min_peaks=10 --min_intensity=1.0 --max_peaks_used=100 --remove_precursor_tol=0.5 --scaling=root --cluster_charges 2 3
```

## Evaluation signals

- Input MGF directory is accessible and contains valid peak list files with m/z and intensity pairs
- Preprocessing pipeline completes without errors; checkpoint file is created or batch encoding proceeds
- Output spectra metadata includes valid ranges: precursor_mz > 0, precursor_charge ∈ {1,2,3,...}, retention_time ≥ 0
- Number of spectra after filtering matches expected retention (e.g., after charge filtering and peak count thresholds)
- GPU memory utilization remains within limits for the selected GPU type (no out-of-memory errors during encoding)

## Limitations

- Clustering for large datasets like PXD000561 requires GTX 3090 GPU with larger memory; GTX 1080Ti will fail on such datasets
- System requires Linux platform with properly configured CUDA environment; Windows and macOS support not documented
- HyperSpec has been tested only on GTX 1080Ti and GTX 3090; other NVIDIA GPUs may require additional validation
- High-performance SSD storage is recommended for best performance; standard storage may create I/O bottlenecks with large datasets
- MGF format is required; other mass spectrometry formats (mzML, mzXML) must be converted beforehand

## Evidence

- [readme] System Requirements: _HyperSpec_ requires `Python 3.8+` with `CUDA` environment: "_HyperSpec_ requires `Python 3.8+` with `CUDA` environment. A GPU should be installed properly."
- [readme] GPU allocation by dataset scale: "Clustering for PXD000561 dataset requires GTX 3090 with larger memory. Clustering for other dataset with smaller scale requires GTX 1080Ti."
- [readme] Input format and preprocessing workflow: "_HyperSpec_ supports running using the command line and takes `MGF` peak files as input and exports the clustering result as a CSV file"
- [readme] Preprocessing parameters for dataset handling: "--cpu_core_preprocess [CPU_CORE_PREPROCESS], --min_peaks [MIN_PEAKS], --min_intensity [MIN_INTENSITY], --max_peaks_used [MAX_PEAKS_USED], --scaling {off,root,log,rank}, --remove_precursor_tol"
- [readme] Performance-critical infrastructure recommendation: "We recommend using high-performance SSD as the storage device for the best performance."
- [readme] Brain-inspired hyperdimensional encoding and bucketing: "_HyperSpec_ first encodes the processed spectra into binary hypervector (HV) with ultra-high dimension (>1000) based on level-id encoding method."
