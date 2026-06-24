---
name: mzml-spectral-parsing
description: Use when when beginning a metabolomics annotation workflow with raw MS2
  spectral data in .mzML format. This step is necessary when you have vendor-converted
  or standard .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - SIRIUS
  - MetFrag
  - R
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-023-00695-y
  title: MAW
evidence_spans:
- performs spectral database dereplication using R Package
- spectral database dereplication using R Package Spectra
- compound database dereplication using SIRIUS OR MetFrag
- compound database dereplication using SIRIUS
- workflow takes MS2 .mzML format data files as an input in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maw_cq
    doi: 10.1186/s13321-023-00695-y
    title: MAW
  dedup_kept_from: coll_maw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-023-00695-y
  all_source_dois:
  - 10.1186/s13321-023-00695-y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML spectral parsing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load and parse MS2 .mzML format mass spectrometry spectral data into memory using the Spectra R package, preparing it for downstream spectral database dereplication and compound annotation. This is the entry point for the MAW metabolomics annotation workflow.

## When to use

When beginning a metabolomics annotation workflow with raw MS2 spectral data in .mzML format. This step is necessary when you have vendor-converted or standard .mzML files and need to extract spectrum objects (precursor m/z, retention time, fragmentation patterns) for querying against spectral or compound databases.

## When NOT to use

- Input data is already in a parsed R Spectra object or equivalent in-memory format; re-parsing would be redundant.
- Data is in vendor-specific binary format (e.g., raw .raw Thermo files) without prior conversion to .mzML; use vendor conversion tools or MSConvert first.
- Performing only computational annotation without access to raw spectral data (e.g., using pre-computed spectral libraries or metadata tables).

## Inputs

- MS2 .mzML format spectral data files
- File path to .mzML file

## Outputs

- Spectra R object containing parsed MS2 spectra with precursor m/z, retention time, fragmentation m/z, and intensity arrays
- In-memory spectrum collection ready for dereplication and annotation

## How to apply

Use the R Spectra package to import .mzML files into R memory as spectrum objects. The Spectra package handles the binary encoding, metadata parsing, and spectrum extraction from the mzML XML structure. Load the data early in the workflow, before any filtering or database dispatch. Verify that all spectra are imported with complete precursor m/z, MS level, and fragmentation intensity arrays intact. This parsed object is then passed to subsequent dereplication steps (spectral matching via GNPS/HMDB/MassBank or compound prediction via SIRIUS/MetFrag).

## Related tools

- **Spectra** (R package for parsing and managing MS2 spectral data from .mzML files into structured Spectra objects) — https://rformassspectrometry.github.io/Spectra/
- **R** (Host language and runtime for executing Spectra-based spectral parsing workflows)

## Examples

```
# In R, after installing Spectra package:
library(Spectra)
spectra_obj <- Spectra("your_file_name.mzML")
# spectra_obj now contains parsed MS2 spectra ready for dereplication
```

## Evaluation signals

- All MS2 spectra from the .mzML file are successfully imported with no missing precursor m/z or fragmentation data.
- Spectra object contains correct metadata: precursor m/z, retention time, MS level (=2), collision energy where available.
- Number of spectra in the Spectra object matches the expected count from the original .mzML file.
- Fragmentation intensity arrays are non-empty and span the expected m/z range (e.g., above precursor m/z for fragment ions).
- Spectra object can be passed without error to downstream dereplication functions (GNPS/HMDB/MassBank matching or SIRIUS/MetFrag dispatch).

## Limitations

- Spectra package requires .mzML format; other formats (netCDF, mzXML, vendor raw) must be pre-converted.
- Large .mzML files (>10 GB) may require significant RAM for in-memory storage; batch processing or HPC recommended per README.
- Metadata completeness depends on .mzML source; some vendors omit collision energy or retention time, which may affect downstream annotation confidence.
- The parsed Spectra object is stored in R memory and is session-dependent; results must be exported before session closure.

## Evidence

- [intro] The workflow takes MS2 .mzML format data files as an input in R: "workflow takes MS2 .mzML format data files as an input in R"
- [intro] Spectral database dereplication is performed using the R Package Spectra: "performs spectral database dereplication using R Package Spectra"
- [other] Load MS2 .mzML spectral data in R using the Spectra package: "Load MS2 .mzML spectral data in R using the Spectra package"
