---
name: ms2-data-preprocessing-pipeline
description: Use when you have raw MS2 spectra files (mzML, mgf, msp, mzxml) that may contain multiple MS2 spectra per feature and require reduction or standardization before library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MZMine
  - matchms
  techniques:
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Data Preprocessing Pipeline

## Summary

A systematic preprocessing workflow that prepares raw MS/MS spectral data for library matching by applying normalization, noise filtering, and quality validation. This skill is essential to ensure query spectra meet format and intensity standards before MS2Query analogue and exact-match searching.

## When to use

Apply this skill when you have raw MS2 spectra files (mzML, mgf, msp, mzxml) that may contain multiple MS2 spectra per feature and require reduction or standardization before library matching. Preprocessing is necessary if your files contain many MS2 spectra per feature, since MS2Query does not perform peak picking or clustering internally.

## When NOT to use

- Your spectra are already peak-picked and clustered by a dedicated tool (e.g., MZMine output used directly without further reduction).
- Input is a single, high-quality MS/MS spectrum with minimal noise and no redundancy.
- You are performing de novo structure elucidation rather than library matching, where alternative preprocessing strategies may be required.

## Inputs

- Raw MS/MS spectrum files (mzML, mgf, msp, mzxml, json, or pickled matchms objects)
- Spectrum metadata including precursor m/z and intensity values
- Optional: clustering or feature selection parameters

## Outputs

- Preprocessed spectrum objects with normalized intensities
- Filtered spectrum objects with noise and low-intensity peaks removed
- Quality-validated spectrum collection ready for MS2Query library matching
- Preprocessing log or summary (optional)

## How to apply

Begin by loading raw MS2 spectra from your input file using a spectral parsing library (matchms or equivalent). Apply normalization to standardize spectral intensities across all query spectra to a common scale (e.g., maximum intensity = 1 or L2-norm). Next, apply filtering to remove noise and low-intensity peaks by removing peaks below a minimum intensity threshold or by clustering similar spectra to reduce redundancy using tools like MZMine. Finally, validate the cleaned spectra by checking that they conform to expected format requirements (presence of precursor m/z, intensity values within valid range) and quality criteria (minimum number of peaks, signal-to-noise ratio) before proceeding to library matching. The README recommends MZMine for preprocessing and using the MGF file output from feature-based molecular networking as input to MS2Query.

## Related tools

- **MS2Query** (Target tool that consumes preprocessed spectra for analogue and exact-match searching) — https://github.com/iomega/ms2query
- **MZMine** (Recommended preprocessing and feature-based molecular networking tool for peak picking and clustering of similar MS2 spectra) — https://mzmine.github.io/mzmine_documentation/index.html
- **matchms** (Python library for spectrum object parsing and manipulation during preprocessing)

## Examples

```
from ms2query.run_ms2query import download_zenodo_files, run_complete_folder; from ms2query.ms2library import create_library_object_from_one_dir; ms2query_library_files_directory = './ms2query_library_files'; download_zenodo_files('positive', ms2query_library_files_directory); ms2library = create_library_object_from_one_dir(ms2query_library_files_directory); run_complete_folder(ms2library, './path_to_preprocessed_spectra')
```

## Evaluation signals

- All query spectra contain valid precursor m/z values and at least one intensity peak above the noise threshold.
- Normalized intensity values fall within expected range (e.g., 0–1 or 0–100) consistently across all query spectra.
- Spectrum file size and peak count are reduced proportionally after filtering, indicating successful noise removal.
- Preprocessed spectra match the input schema expected by MS2Query (format: mzML, json, mgf, msp, mzxml, usi, or pickled matchms object).
- When run on dummy spectra, preprocessed output produces results consistent with expected_results_dummy_data.csv, indicating format correctness.

## Limitations

- MS2Query does not perform internal peak picking or clustering; preprocessing must be completed upstream, ideally using MZMine, before MS2Query execution.
- The article and README do not provide explicit details about specific normalization algorithms (e.g., L2-norm vs. max-intensity normalization) or recommended intensity thresholds for filtering, leaving some parameter choices to user discretion.
- Preprocessing parameters (filtering thresholds, clustering criteria) are not standardized across tools; user must validate that their chosen preprocessing parameters are appropriate for their data and research goals.
- The skill assumes access to spectra with annotated metadata (e.g., precursor m/z); spectra lacking this metadata cannot be reliably preprocessed.

## Evidence

- [other] Define spectrum pre-processing function signatures for normalisation and filtering operations on raw query spectral data. Implement normalisation logic to standardize spectral intensities across raw query spectra. Implement filtering logic to remove noise and low-intensity peaks from raw query spectra.: "Define spectrum pre-processing function signatures for normalisation and filtering operations on raw query spectral data. 2. Implement normalisation logic to standardize spectral intensities across"
- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [readme] One reliable method is using MZMine for preprocessing, https://mzmine.github.io/mzmine_documentation/index.html. As input for MS2Query you can use the MGF file of the FBMN output of MZMine: "One reliable method is using MZMine for preprocessing, https://mzmine.github.io/mzmine_documentation/index.html. As input for MS2Query you can use the MGF file of the FBMN output"
- [other] Validate cleaned spectra meet expected format and quality criteria before library matching.: "Validate cleaned spectra meet expected format and quality criteria before library matching."
- [readme] Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object: "Accepted formats are: "mzML", "json", "mgf", "msp", "mzxml", "usi" or a pickled matchms object"
