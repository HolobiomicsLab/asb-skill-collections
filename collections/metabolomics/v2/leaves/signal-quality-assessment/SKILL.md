---
name: signal-quality-assessment
description: Use when you have imported raw MSI spectral data in imzML format and
  need to improve signal-to-noise ratio before performing mean intensity calculations,
  ROI analysis, or database annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - napari
  - Python
  - MSI-Explorer
  techniques:
  - CE-MS
  - MS-imaging
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5c01513
  title: MSI-Explorer
evidence_spans:
- The MSI-Explorer napari plugin is a powerful tool designed for targeted biochemical
  annotations in MSI data.
- '[![Python Version](https://img.shields.io/pypi/pyversions/MSI-Explorer.svg?color=green)](https://python.org)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msi_explorer_cq
    doi: 10.1021/acs.analchem.5c01513
    title: MSI-Explorer
  dedup_kept_from: coll_msi_explorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01513
  all_source_dois:
  - 10.1021/acs.analchem.5c01513
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# signal-quality-assessment

## Summary

Evaluate and enhance MSI spectral data quality by applying noise reduction and intensity normalization to remove background noise and standardize signal across all pixels and m/z values. This preprocessing step is essential before downstream biochemical annotation and ROI analysis to ensure reliable intensity measurements and comparisons.

## When to use

Apply this skill when you have imported raw MSI spectral data in imzML format and need to improve signal-to-noise ratio before performing mean intensity calculations, ROI analysis, or database annotation. Use it when spectra contain background noise or exhibit intensity variations across pixels that would compromise quantitative comparisons.

## When NOT to use

- Input data is already preprocessed or has been validated as high-quality without artifacts
- Spectra do not contain background noise or intensity artifacts (e.g., simulated or synthetic data)
- Analysis requires preservation of absolute intensity values for external quantitative comparison without normalization

## Inputs

- Raw MSI spectral data in imzML format
- Mass spectrometry imaging dataset with pixel-wise spectra
- Profile or centroid mode spectra

## Outputs

- Noise-reduced and intensity-normalized MSI spectra
- Preprocessed data compatible with downstream visualization and ROI analysis
- Mean spectrum plot showing quality improvement
- Mean spectrum data exportable as CSV

## How to apply

Load raw MSI spectral data using the MSI-Explorer napari plugin in Python. First, apply noise reduction by selecting a user-defined percentage threshold (e.g., 3%) to remove background signal and improve signal-to-noise ratio. Then apply one of four normalization methods—Total Ion Current (TIC), Root Mean Square (RMS), Median, or Reference Peak (internal standard)—depending on your experimental design and whether you have a known internal standard. Optionally apply hotspot removal at a quantile threshold (e.g., 99.99%) to suppress anomalous high-intensity pixels. Execute all preprocessing steps together, then verify output quality by calculating and visualizing the mean spectrum to confirm noise reduction and normalization have been applied appropriately.

## Related tools

- **napari** (Interactive visualization platform and plugin host for MSI data viewing and ROI selection during preprocessing) — https://github.com/napari/napari
- **MSI-Explorer** (napari plugin that implements noise reduction, normalization, and hotspot removal preprocessing workflows) — https://github.com/MMV-Lab/MSI-Explorer
- **Python** (Programming environment for loading, processing, and scripting MSI preprocessing pipelines)

## Evaluation signals

- Signal-to-noise ratio visibly improves in the mean spectrum plot after noise reduction is applied
- Intensity distributions are standardized across all pixels and m/z values after normalization (verified by comparing pre- and post-normalization spectra)
- No systematic bias or artifacts are introduced by the chosen normalization method
- Exported mean spectrum data shows consistent intensity scaling across replicates or regions after preprocessing
- Hotspot removal does not eliminate biologically relevant peaks (verify by checking that known metabolite m/z values are retained)

## Limitations

- Noise reduction percentage and normalization method must be chosen empirically based on dataset characteristics; no automatic selection is described
- Hotspot removal uses a fixed quantile threshold (99.99% default) which may not be optimal for all tissue types or acquisition modes
- Profile-mode spectra are converted to centroid mode via user prompt, which may alter downstream analysis if not handled consistently
- Normalization assumes that the chosen method (TIC, RMS, Median, or reference peak) is appropriate for the biological system and does not conflate abundance with instrumental sensitivity

## Evidence

- [other] MSI-Explorer includes a pre-processing module that performs noise reduction and normalization on imported MSI spectra as part of its workflow.: "MSI-Explorer includes a pre-processing module that performs noise reduction and normalization on imported MSI spectra"
- [other] Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset.: "Apply noise reduction filtering to remove background signal and improve signal-to-noise ratio across the spectral dataset"
- [other] Apply intensity normalization to standardize spectral intensities across all pixels and m/z values.: "Apply intensity normalization to standardize spectral intensities across all pixels and m/z values"
- [readme] The normalization methods that the user can apply are Total ion current (TIC), Root mean square (RMS), Medium, Reference peak (or internal standard): "The normalization methods that the user can apply are - Total ion current (TIC) - Root mean square (RMS) - Medium - Reference peak (or internal standard)"
- [readme] Users can choose their desired level of noise reduction (shown as a percentage) for their experiment.: "Users can choose their desired level of noise reduction (shown as a percentage) for their experiment"
- [readme] Hotspot removal can also be applied using a default threshold of 99.99%.: "Hotspot removal can also be applied using a default threshold of 99.99%"
- [readme] After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity.: "After pre-processing steps are chosen, click `Execute` and `Show true mean spectrum` to calculate the mean intensity"
