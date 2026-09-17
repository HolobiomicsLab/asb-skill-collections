---
name: bruker-nmr-spectral-data-import
description: Use when you have raw Bruker NMR spectral files (from a Bruker instrument)
  in a directory and need to prepare them for automated metabolite identification
  and quantification using ASICS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ASICS
  - R
  techniques:
  - NMR
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04232
  title: ASICS
- doi: 10.1007/s11306-017-1244-5
  title: ''
evidence_spans:
- The **R** package `ASICS` is a fully automated procedure to identify and quantify
  metabolites in $^1$H 1D-NMR spectra
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bruker-nmr-spectral-data-import

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Import Bruker NMR spectral data files into an R data frame, then convert to a Spectra object for downstream metabolite identification and quantification. This is a required preprocessing step in the ASICS pipeline for 1H NMR metabolomics analysis.

## When to use

You have raw Bruker NMR spectral files (from a Bruker instrument) in a directory and need to prepare them for automated metabolite identification and quantification using ASICS. This step is mandatory before running metabolite quantification, as the Spectra object is the required input format for ASICS analysis.

## When NOT to use

- Input spectral data are already in a different format (mzML, NetCDF, text CSV) — use format-specific importers instead
- Data have already been imported and converted to a Spectra object — proceed directly to ASICS quantification
- You are using a non-Bruker NMR instrument or vendor format — this function is specific to Bruker file structures

## Inputs

- Bruker NMR spectral data files (raw instrument output in Bruker directory format)
- Directory path to Bruker files (character string)

## Outputs

- Data frame with imported spectral data (rows = chemical shift bins, columns = samples)
- Spectra object (S4 class required for downstream ASICS quantification)

## How to apply

Load the ASICS R package and use the importSpectraBruker() function to import all Bruker spectral files from a specified directory into a data frame. Specify the full path to the directory containing the Bruker files. Once imported, immediately create a Spectra object from the resulting data frame using the createSpectra() function. This object structure is required by downstream ASICS quantification functions. Verify that the Spectra object contains the expected number of samples and that spectral data are properly formatted before proceeding to quantification.

## Related tools

- **ASICS** (R package providing importSpectraBruker() and createSpectra() functions for Bruker import and Spectra object creation; also performs downstream metabolite identification and quantification) — https://github.com/GaelleLefort/ASICS
- **R** (Execution environment for ASICS package and all import/preprocessing functions)

## Examples

```
library(ASICS); dir_path <- system.file('example_spectra', package='ASICS'); data_frame <- importSpectraBruker(dir_path); spectra_obj <- createSpectra(data_frame)
```

## Evaluation signals

- Data frame returned by importSpectraBruker() contains numeric matrix with correct dimensions (rows = chemical shift points, columns = number of samples)
- Spectra object is successfully created without errors using createSpectra()
- Spectra object class is confirmed (S4 class with expected slots for spectral data and sample metadata)
- No missing values or NaN entries in the imported spectral intensity data
- Chemical shift scale and spectral range are consistent with expected 1H NMR parameters (e.g., 0–10 ppm typical range)

## Limitations

- Function is specific to Bruker instrument file format; incompatible with other vendor formats (Varian, JEOL, Bruker JCAMP-DX)
- Requires correct directory structure as output by Bruker instruments; manually reorganized or corrupted Bruker files may fail to import
- No changelog or version history available in the provided context, limiting traceability of format support changes

## Evidence

- [other] Data are imported in a data frame from Bruker files with the importSpectraBruker function: "Data are imported in a data frame from Bruker files with the `importSpectraBruker` function"
- [other] Spectra object is required step for quantification: "from the data frame, a `Spectra` object is created. This is a required step for the quantification"
- [other] ASICS enables automated identification and quantification of metabolites in 1H NMR spectra: "fully automated procedure to identify and quantify metabolites in $^1$H 1D-NMR spectra of biological mixtures"
- [other] ASICS is an R package: "The **R** package `ASICS` is a fully automated procedure to identify and quantify metabolites"
