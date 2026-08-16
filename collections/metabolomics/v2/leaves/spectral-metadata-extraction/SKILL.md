---
name: spectral-metadata-extraction
description: Use when after loading an MSP spectral library file into memory using
  mssearchr's MSP parser, when you need to verify that each spectrum record contains
  complete and valid metadata (precursor m/z values, peak lists, header annotations)
  before writing the parsed spectra to a new MSP file or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3237
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - mssearchr
  - R
  - R GUI (SMART)
  - SMART
  - Python
  - spectrum_utils
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.5c00322
  title: mspepsearchr
- doi: 10.1021/acs.analchem.5c03225
  title: ''
- doi: 10.1021/acs.analchem.9b04884
  title: ''
evidence_spans:
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users for conducting library searches against electron ionization mass spectral
  databases.
- The primary goal of the `mssearchr` package is to enhance the capabilities of R
  users
- enhance the capabilities of R users for conducting library searches
- SMART written in R and R GUI has been developed as user-friendly software
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dimple_cq
    doi: 10.1101/2025.09.22.677919v1
    title: DIMPLE
  - build: coll_lcmsworld_cq
    doi: 10.1021/acs.jproteome.0c00618
    title: lcmsWorld
  - build: coll_mspepsearchr_cq
    doi: 10.1021/jasms.5c00322
    title: mspepsearchr
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_mspepsearchr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00322
  all_source_dois:
  - 10.1021/jasms.5c00322
  - 10.1021/acs.analchem.5c03225
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-metadata-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and validate key spectral metadata fields (precursor m/z, peaks, annotations) from mass spectral records parsed from MSP library files. This skill ensures structural and semantic correctness of spectral data before downstream analysis or file export.

## When to use

Apply this skill after loading an MSP spectral library file into memory using mssearchr's MSP parser, when you need to verify that each spectrum record contains complete and valid metadata (precursor m/z values, peak lists, header annotations) before writing the parsed spectra to a new MSP file or performing library search operations.

## When NOT to use

- Input spectra are already validated and certified by an upstream quality-control pipeline — extraction and re-validation would be redundant.
- You are performing raw peak detection or deconvolution (not metadata annotation) — use signal processing tools instead.
- The MSP file is known to be non-standard or uses a custom dialect not conforming to MSP specification — validate dialect first or use a custom parser.

## Inputs

- parsed MSP spectrum objects (in-memory R list or data frame)
- individual spectrum records with header fields and peak data

## Outputs

- validated metadata dictionary per spectrum (precursor m/z, peaks, annotations)
- validation report (pass/fail per record, error flags for missing/malformed fields)
- cleaned spectrum objects ready for writing or search

## How to apply

After parsing an MSP file into an in-memory R data structure (list or data frame of spectrum objects) using mssearchr, iterate over each spectrum record and extract the key metadata fields: precursor m/z, peak list with intensity values, and metadata annotations (retention index, compound name, etc.). Validate each field against MSP specification requirements: check that precursor m/z is numeric and within expected mass range, verify that peak lists are non-empty and formatted as m/z–intensity pairs, and confirm that required header fields are populated. Compare extracted metadata to source records to detect parsing errors, missing values, or format violations. Flag records that fail validation for manual review or correction before proceeding to file output or spectral searching.

## Related tools

- **mssearchr** (parses MSP files into in-memory R data structures; provides MSP reader and writer functions for spectrum object manipulation and validation) — https://github.com/AndreySamokhin/mssearchr
- **R** (execution environment for mssearchr package and metadata extraction workflows)

## Examples

```
# After loading MSP file with mssearchr, extract and validate metadata:
spectra <- read_msp('library.msp')
for (i in seq_along(spectra)) {
  spectrum <- spectra[[i]]
  precursor_mz <- spectrum$precursor_mz
  peaks <- spectrum$peaks
  validate_metadata(precursor_mz, peaks, spectrum$annotations)
}
```

## Evaluation signals

- All spectrum records in the output contain non-null precursor m/z values within the expected mass range for the instrument.
- Each record's peak list is non-empty, formatted as m/z–intensity pairs, and contains no NaN or negative values.
- Metadata annotations (compound name, retention index, etc.) match the original MSP input file when spot-checked against source records.
- Writing the extracted and validated spectra back to a new MSP file produces a structurally valid output that re-parses without errors.
- Comparison of parsed fields from the output MSP file to the original input records shows zero or minimal discrepancies (accounting for floating-point precision).

## Limitations

- The skill assumes the input MSP file is well-formed; malformed header syntax or non-standard field ordering may cause extraction failures.
- Validation rules are tied to MSP specification compliance; custom or legacy MSP dialects may not conform to standard field names or value ranges.
- The skill does not perform spectral peak deconvolution, isotope correction, or advanced quality metrics — it validates only metadata structure and basic semantic correctness.

## Evidence

- [other] Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations).: "Extract and validate key spectral fields from each record (precursor m/z, peaks, metadata annotations)."
- [other] Load an MSP spectral library file using mssearchr's MSP parser into an in-memory R data structure (list or data frame of spectrum objects).: "Load an MSP spectral library file using mssearchr's MSP parser into an in-memory R data structure (list or data frame of spectrum objects)."
- [readme] reading/writing *msp* files: "reading/writing *msp* files"
- [other] Verify output file structure by reading it back and comparing parsed fields to the original input records.: "Verify output file structure by reading it back and comparing parsed fields to the original input records."
