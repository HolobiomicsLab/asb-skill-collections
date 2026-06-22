---
name: multiplexed-spectrum-decomposition
description: Use when you have SWATH-MS data (mzML or vendor binary format) where precursor isolation windows intentionally capture multiple co-eluting compounds, resulting in multiplexed MS/MS spectra that contain mixed fragment ion peaks from unknown metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - DecoMetDIA
derived_from:
- doi: 10.1021/acs.analchem.9b02655
  title: DecoMetDIA
evidence_spans:
- DecoMetDIA was developed to process SWATH-MS based data for metabolomics.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_decometdia_cq
    doi: 10.1021/acs.analchem.9b02655
    title: DecoMetDIA
  dedup_kept_from: coll_decometdia_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b02655
  all_source_dois:
  - 10.1021/acs.analchem.9b02655
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiplexed-spectrum-decomposition

## Summary

Algorithmic separation of overlapping MS/MS spectra acquired under SWATH-MS multiplexing into individual component spectra to enable untargeted metabolite identification. This skill is essential when precursor ion windows capture multiple co-eluting analytes whose fragment spectra overlap in m/z and intensity space.

## When to use

You have SWATH-MS data (mzML or vendor binary format) where precursor isolation windows intentionally capture multiple co-eluting compounds, resulting in multiplexed MS/MS spectra that contain mixed fragment ion peaks from unknown metabolites. Apply this skill before spectral library matching when standard deconvolution approaches fail due to the complexity and number of overlapping signals.

## When NOT to use

- Input data are already separated single-precursor MS/MS spectra (e.g., from targeted MRM or DDA with narrow isolation windows); deconvolution is unnecessary.
- SWATH-MS precursor windows are too wide or retention time binning is too coarse to meaningfully group co-eluting analytes; data quality is insufficient for reliable decomposition.
- The application requires real-time or streaming analysis; DecoMetDIA requires full batch processing of raw data files.

## Inputs

- SWATH-MS raw data files (mzML format or vendor-specific binary)
- Precursor ion window definitions (m/z ranges and retention time windows)
- Multiplexed MS/MS spectra (mixed fragment ion peaks from co-eluting analytes)

## Outputs

- Deconvoluted MS/MS spectra (individual component spectra, one per analyte)
- Annotated spectral data (MGF or mzTab format with precursor m/z, retention time, intensity)
- Spectral quality metrics (peak counts, intensity distributions, mass accuracy)

## How to apply

Load SWATH-MS raw data into DecoMetDIA and apply precursor ion isolation and retention time windowing to group co-eluting fragment spectra. The tool then performs multiplexed spectrum decomposition—an algorithm that separates overlapping MS/MS spectra into individual component spectra by decomposing the mixed signal into constituent peaks and their precursor-fragment relationships. After deconvolution, validate the separated spectra by checking peak counts, intensity distributions, and mass accuracy against known standards or in silico predictions. Export deconvoluted spectra with precursor m/z, retention time, and intensity annotations in MGF or mzTab format for downstream metabolite identification.

## Related tools

- **DecoMetDIA** (R package implementing multiplexed spectrum decomposition algorithm with Rcpp components for SWATH-MS data processing) — https://github.com/ZhuMSLab/DecoMetDIA

## Examples

```
devtools::install_github("ZhuMSLab/DecoMetDIA"); library(DecoMetDIA); result <- decoMetDIA(rawfile="sample.mzML", precursor_windows=list(mz_range=c(100, 1200), rt_bin=30))
```

## Evaluation signals

- Deconvoluted spectra exhibit appropriate peak counts and intensity distributions consistent with single-analyte MS/MS spectra, not residual multiplex patterns.
- Mass accuracy of fragment ions in separated spectra matches instrument calibration tolerances (typically <5 ppm for high-resolution instruments).
- Precursor m/z and retention time annotations are preserved and consistent with input isolation windows and chromatographic alignment.
- Separated spectra can be matched to metabolite standards or database entries with cosine similarity or other spectral similarity metrics above acceptance thresholds.
- Signal-to-noise ratio and peak intensity distributions improve after deconvolution compared to raw multiplexed spectra, indicating successful decomposition.

## Limitations

- Deconvolution accuracy depends on the number and degree of overlap of co-eluting analytes; highly overlapped spectra may yield ambiguous or incomplete decomposition.
- The algorithm requires sufficient chromatographic resolution and retention time precision to correctly group spectra into windows; poor chromatography increases decomposition errors.
- DecoMetDIA requires compilation with Rcpp on installation; Windows users must have RTools installed, and compilation may fail on systems lacking appropriate build tools.
- The tool is designed for untargeted metabolomics; applicability to other MS/MS multiplexing schemes (e.g., data-independent acquisition with different window strategies) is not addressed in the publication.

## Evidence

- [readme] DecoMetDIA was developed to process SWATH-MS based data for metabolomics: "DecoMetDIA was developed to process SWATH-MS based data for metabolomics."
- [other] Deconvolution workflow and algorithm description: "Perform spectral deconvolution using DecoMetDIA's multiplexed spectrum decomposition algorithm to separate overlapping MS/MS spectra into individual component spectra."
- [other] Input and output data formats: "Load SWATH-MS raw data files (mzML or vendor format) into DecoMetDIA. ... Export deconvoluted spectra with associated precursor m/z, retention time, and intensity annotations in MGF or mzTab format."
- [other] Validation criteria for deconvoluted spectra: "Validate deconvoluted spectra quality by checking for appropriate peak counts, intensity distributions, and mass accuracy."
- [readme] Installation and technical requirements: "DecoMetDIA was developed as an R package with Rcpp code. Compiling is needed when installing. On Windows OS, RTools should be installed first."
