---
name: nmr-spectrum-object-construction
description: Use when you have Bruker NMR spectral files (raw instrumental output) and need to prepare them for automated metabolite identification and quantification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0218
  tools:
  - ASICS
  - R
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.0c04232
  title: ASICS
- doi: 10.1007/s11306-017-1244-5
  title: ''
evidence_spans:
- The **R** package `ASICS` is a fully automated procedure to identify and quantify metabolites in $^1$H 1D-NMR spectra
- The **R** package `ASICS`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asics_cq
    doi: 10.1021/acs.analchem.0c04232
    title: ASICS
  dedup_kept_from: coll_asics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04232
  all_source_dois:
  - 10.1021/acs.analchem.0c04232
  - 10.1007/s11306-017-1244-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# NMR Spectrum Object Construction

## Summary

Convert raw Bruker NMR spectral data files into a structured Spectra object, a required intermediate representation that enables downstream metabolite identification and quantification in the ASICS pipeline. This skill bridges raw instrumental output and quantitative analysis.

## When to use

You have Bruker NMR spectral files (raw instrumental output) and need to prepare them for automated metabolite identification and quantification. Apply this skill immediately after data acquisition and before running ASICS metabolite identification, as the Spectra object is a mandatory input for quantification.

## When NOT to use

- Input spectral data are already in a non-Bruker format (e.g., mzML, NetCDF, plain CSV) — use format-specific import functions instead of importSpectraBruker()
- A Spectra object has already been constructed from your data — applying this skill again will duplicate processing and waste computation
- Your analysis does not require automated metabolite quantification — if you only need visual inspection or manual peak picking, Spectra object construction may be unnecessary

## Inputs

- Bruker NMR spectral files (raw instrumental format from Bruker spectrometer)
- Directory path containing Bruker spectral data files

## Outputs

- Spectra object (structured R object containing normalized 1H NMR spectral data)
- Data frame (intermediate representation with spectral intensities and chemical shifts)

## How to apply

Load the ASICS R package and use the importSpectraBruker() function to read Bruker spectral files from a specified directory into a data frame, preserving the spectral intensity values and chemical shift information. Pass the resulting data frame to createSpectra() to construct a Spectra object, which normalizes and structures the data into the format required by downstream ASICS quantification. This two-step process (import → object creation) is mandatory; the Spectra object cannot be bypassed because it enforces the schema and metadata required for metabolite matching algorithms.

## Related tools

- **ASICS** (R package that provides importSpectraBruker() and createSpectra() functions for constructing Spectra objects and performing downstream metabolite identification and quantification) — https://github.com/GaelleLefort/ASICS
- **R** (Programming environment in which ASICS and Spectra object construction are executed)

## Examples

```
library(ASICS); spectra_dir <- system.file('example_spectra', package='ASICS'); df <- importSpectraBruker(spectra_dir); spectra_obj <- createSpectra(df)
```

## Evaluation signals

- The returned object is of class 'Spectra' (or equivalent ASICS class) and can be passed directly to the ASICS() quantification function without error
- Spectral intensities are numeric, properly aligned to chemical shift scale (typically 0–10 ppm for 1H NMR), and have no missing or NaN values in the quantification region
- The number of spectral data points and metadata (e.g., sample identifiers, acquisition parameters) matches the input Bruker file count and directory contents
- Object summary or str() output shows structured fields for spectra matrix, chemical shift axis, and sample annotations expected by createSpectra()

## Limitations

- importSpectraBruker() is specific to Bruker format; data from other NMR vendors (Varian, JEOL, Agilent) require alternative import functions or manual conversion
- The Spectra object construction assumes 1D 1H NMR data; multi-dimensional NMR (COSY, HSQC) or non-proton nuclei (13C, 31P) may require modified or separate workflows
- No preprocessing of spectral artifacts (phasing, baseline correction, solvent suppression) is applied during importSpectraBruker() → createSpectra(); these steps may be necessary upstream depending on data quality

## Evidence

- [other] import_and_object_creation_workflow: "Data are imported in a data frame from Bruker files with the `importSpectraBruker` function"
- [other] spectra_object_mandatory_for_quantification: "from the data frame, a `Spectra` object is created. This is a required step for the quantification"
- [other] asics_package_context: "The **R** package `ASICS` is a fully automated procedure to identify and quantify metabolites in $^1$H 1D-NMR spectra"
- [other] quantification_depends_on_object: "Identification and quantification of metabolites can now be carried out using only the function `ASICS`"
