---
name: mass-spectrum-preprocessing
description: Use when you have raw MS/MS spectra in MGF format with variable peak quality, mixed charge states, or instrument artifacts that could confound clustering or similarity measures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python 3.8+
  - HyperSpec (wh-xu/Hyper-Spec)
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00612
  title: HyperSpec
evidence_spans:
- HyperSpec requires `Python 3.8+` with `CUDA` environment
- HyperSpec requires `Python 3.8+` with `CUDA` environment.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-preprocessing

## Summary

Normalize, filter, and prepare raw mass spectrometry data (mz/intensity pairs from MGF files) for downstream clustering or analysis by applying charge filtering, peak intensity thresholding, precursor removal, and optional intensity scaling. This skill converts heterogeneous instrument output into a standardized, quality-controlled representation suitable for hyperdimensional encoding or other comparative methods.

## When to use

Apply this skill when you have raw MS/MS spectra in MGF format with variable peak quality, mixed charge states, or instrument artifacts that could confound clustering or similarity measures. Use it as the mandatory first step before encoding spectra into hyperdimensional vectors or performing distance-based comparisons, especially when working with large proteomics datasets (>1M spectra) where quality control directly impacts downstream performance.

## When NOT to use

- Input is already preprocessed or vendor-normalized; re-filtering may introduce bias or lose information.
- Target analysis requires all charge states or rare low-abundance peaks; aggressive filtering removes biological signal.
- Spectrum-to-spectrum comparison method (e.g., cosine similarity) has its own internal normalization; redundant preprocessing may degrade discriminative power.

## Inputs

- MGF files (mass spectrometry peak lists with mz/intensity pairs)
- Raw MS/MS spectra with precursor m/z, charge, and retention time metadata

## Outputs

- Preprocessed spectra stored in parquet format with columns: bucket, precursor_charge, precursor_mz, identifier, scan, retention_time
- Filtered peak lists (mz/intensity pairs per spectrum meeting quality thresholds)
- Metadata CSV or parquet table for downstream clustering/encoding steps

## How to apply

Load raw mass spectra (mz/intensity pairs) from MGF input files. Apply filtering in this order: (1) select target charge states (e.g., +2 and +3 only); (2) remove peaks below a minimum intensity threshold and cap the number of peaks used (e.g., max_peaks_used parameter); (3) remove precursor ion and nearby fragment ions within a specified tolerance (remove_precursor_tol); (4) apply optional intensity scaling (off, root, log, or rank) to normalize peak heights; (5) enforce m/z range constraints (min_mz, max_mz) and minimum peak count (min_peaks); (6) validate that each spectrum meets minimum information requirements. Export preprocessed spectra with metadata (charge, precursor m/z, retention time) for downstream encoding. Rationale: preprocessing reduces noise, removes redundant charge states, and normalizes intensity distributions, improving clustering quality and reproducibility without sacrificing resolution.

## Related tools

- **Python 3.8+** (Runtime environment for preprocessing script execution with multicore CPU parallelization)
- **HyperSpec (wh-xu/Hyper-Spec)** (Integrated preprocessing module (src/main.py) that encapsulates filtering, scaling, and charge selection before HD encoding) — https://github.com/wh-xu/Hyper-Spec

## Examples

```
python src/main.py ~/dataset/ ./output.csv --cpu_core_preprocess=4 --min_peaks=10 --min_intensity=1.0 --max_peaks_used=100 --remove_precursor_tol=0.5 --scaling=root --cluster_charges 2 3
```

## Evaluation signals

- All output spectra have charge in the target set (e.g., only +2 and +3 present); verify via parquet column value counts or histogram.
- Peak count per spectrum is ≥ min_peaks threshold; none fall below the cutoff after filtering.
- Precursor mass and nearby fragments (within remove_precursor_tol) are removed; spot-check 5–10 spectra to confirm precursor intensity = 0 or absent.
- Intensity scaling (if enabled) produces expected distribution shift (e.g., log scaling compresses high-intensity peaks, rank scaling produces uniform ranks 1..N); compare intensity histograms before/after.
- Metadata fields (bucket, precursor_mz, retention_time) are non-null and within biologically plausible ranges (e.g., mz > 100, retention_time >= 0).

## Limitations

- Preprocessing parameters (eps, min_intensity, max_peaks_used) are dataset-dependent and require manual tuning; no universal default guarantees optimal clustering across diverse instruments or proteomes.
- Aggressive peak filtering (small max_peaks_used or high min_intensity) may discard rare but informative low-abundance fragments, reducing spectral uniqueness.
- Charge state filtering (cluster_charges) removes singly- and highly-charged ions; unsuitable for small-molecule MS or non-proteomics workflows.
- Intensity scaling methods (root, log, rank) introduce non-linear distortions; choice affects downstream similarity metrics and must be validated per use case.

## Evidence

- [other] Load raw mass spectra from input file (mz/intensity pairs): "Load raw mass spectra from input file (mz/intensity pairs)."
- [readme] Enforce min_peaks, precursor filtering, and charge selection via CLI: "--min_peaks MIN_PEAKS
                [--mz_interval MZ_INTERVAL] [--min_mz_range MIN_MZ_RANGE] [--min_mz MIN_MZ] [--max_mz MAX_MZ] 
                [--remove_precursor_tol REMOVE_PRECURSOR_TOL]"
- [readme] Charge state selection as core preprocessing parameter: "[--cluster_charges [CLUSTER_CHARGES ...]]"
- [readme] MGF file format as input standard: "_HyperSpec_ supports running using the command line and takes `MGF` peak files as input"
- [readme] Preprocessed metadata export to parquet: "The exported meta data for clustering results are compressed and stored in `parquet` file, which records `bucket`, `precursor_charge`, `precursor_mz`, `identifier`, `scan`, `retention_time`,"
- [readme] Multicore CPU parallelization for preprocessing: "--cpu_core_preprocess CPU_CORE_PREPROCESS] [--cpu_core_cluster CPU_CORE_CLUSTER]
                [--batch_size BATCH_SIZE] [--use_gpu_cluster] [--min_peaks MIN_PEAKS]"
