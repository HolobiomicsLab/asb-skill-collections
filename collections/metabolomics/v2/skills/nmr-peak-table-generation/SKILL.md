---
name: nmr-peak-table-generation
description: Use when you have raw 1D NMR spectra (in NMRPipe or similar format) from biological samples (urine, worm, or other metabolomics experiments) and need to extract a structured peak table with chemical shifts and intensities for downstream metabolite identification or quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - SAND
  - NMRPipe
  - NMRBox
derived_from:
- doi: 10.1021/acs.analchem.3c03078
  title: SAND
evidence_spans:
- Any user is welcome to make new modificaitons on the SAND code, particularly its version for NMRBox
- interface to NMRPipe (pipe_scripts/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sand_cq
    doi: 10.1021/acs.analchem.3c03078
    title: SAND
  dedup_kept_from: coll_sand_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c03078
  all_source_dois:
  - 10.1021/acs.analchem.3c03078
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-peak-table-generation

## Summary

Automated conversion of 1D NMR spectra into quantitative peak tables through spectral deconvolution. This skill applies SAND's automatic processing and deconvolution workflow to extract peak positions, intensities, and assignments from raw NMR data (urine, worm, or other experimental datasets).

## When to use

Apply this skill when you have raw 1D NMR spectra (in NMRPipe or similar format) from biological samples (urine, worm, or other metabolomics experiments) and need to extract a structured peak table with chemical shifts and intensities for downstream metabolite identification or quantification. The skill is appropriate when manual peak-picking is impractical and you require consistent, automated deconvolution across multiple spectra.

## When NOT to use

- The input spectrum is already a manually curated, validated peak table — skip this skill and proceed directly to metabolite annotation.
- The NMR data is 2D (COSY, HSQC, HMBC) or multi-dimensional — SAND is currently designed for 1D spectra only.
- The sample is from a data type not yet supported by SAND (e.g., tissue, plasma, or other biological matrices beyond urine and worm) — the article notes plans for expansion but current validation is limited to the tested datasets.

## Inputs

- 1D NMR spectra in NMRPipe format or compatible binary/text formats
- Urine or worm NMR datasets (experimental or simulated)
- Raw spectral data files from standard NMR instruments

## Outputs

- Peak tables in tabular format (CSV, text, or database format)
- Peak assignments with chemical shift values
- Peak intensities and line-shape parameters
- Processed spectral data

## How to apply

Set up SAND_V7 in the NMRBox environment following the installation script at NMRBox_ADMIN_versions/SAND_V7/install_SAND.sh. Load your 1D NMR spectra (acquired on standard instruments and processed via NMRPipe) into SAND. Execute SAND's automatic processing and deconvolution workflow, which handles both simulated and experimental datasets with the same pipeline. The workflow automatically identifies peaks, estimates line shapes, and generates peak-table output in a standard tabular format. Verify successful execution by confirming that peak-table files are produced with expected columns (chemical shift, intensity, line width, or similar) and that the number of identified peaks is consistent with the spectral complexity of your sample class.

## Related tools

- **SAND** (Core deconvolution engine performing automatic processing and peak extraction from 1D NMR spectra) — https://github.com/edisonomics/SAND
- **NMRBox** (Containerized environment and service platform hosting SAND_V7 for local execution and web-based access) — https://nmrbox.org
- **NMRPipe** (Upstream spectral processing tool; SAND interfaces with NMRPipe for preprocessing spectra before deconvolution)

## Evaluation signals

- Peak-table output files are generated in the expected format with non-empty rows corresponding to detected peaks.
- Chemical shift values fall within the biologically plausible range (0–10 ppm for 1H NMR; 0–220 ppm for 13C NMR) and align with known metabolites in the sample class (e.g., urine or worm).
- Peak counts are consistent across replicate spectra of the same sample type and reasonable given the spectral complexity (e.g., 30–100 peaks for typical urine spectra).
- Line shapes and intensities are physically reasonable (positive intensities, reasonable line widths in Hz).
- The workflow completes without errors in the NMRBox environment and all intermediate processing steps (deconvolution, fitting) converge.

## Limitations

- SAND is currently validated only on urine and worm datasets; generalization to other biological matrices (plasma, tissue, cerebrospinal fluid) has not been reported.
- Only 1D NMR spectra are supported; extension to 2D and other NMR data types is planned but not yet implemented.
- The article does not provide quantitative performance metrics (sensitivity, specificity, false discovery rate) for peak detection or comparison to manual annotation standards.
- No changelog is available to track improvements, bug fixes, or parameter tuning between versions.

## Evidence

- [readme] SAND automatic process and deconvolute 1D NMR spectra into peak tables.: "SAND automatic process and deconvolute 1D NMR spectra into peak tables."
- [readme] Tested on urine and worm datasets with plans for expansion: "We have tested SAND on urine and worm dataset and will expand it to other new data."
- [readme] Similar workflow for simulated and experimental datasets: "Similar workflow works for simulated and expermental datasets."
- [methods] Installation and setup via NMRBox environment: "latest interface to NMRBox (SAND_V7), and interface to NMRPipe"
- [methods] Testing workflow on NMRBox before deployment: "Any updtes is expected to run NMRBox environemt and pass the test before merge."
