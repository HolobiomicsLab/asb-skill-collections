---
name: metadata-field-extraction-and-restructuring
description: Use when reading mass spectral library files (particularly MoNA EI or MS2 libraries) where structural metadata like SMILES information is embedded in general-purpose fields (e.g., Comment field) rather than in the dedicated SMILES field expected by mspcompiler's downstream processing steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0153
  tools:
  - mspcompiler
  - R
  - MoNA
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- The MassBank of North America (MoNA) has an EI library available
- The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
schema_version: 0.2.0
---

# metadata-field-extraction-and-restructuring

## Summary

Extract and restructure embedded metadata fields from mass spectral library records into standardized fields required by downstream pipeline steps. This skill is essential when source library formats embed critical information (such as SMILES strings) in unstructured or non-standard fields (such as Comment fields) that must be isolated and placed into the expected schema before compilation and use in MS-DIAL.

## When to use

Apply this skill when reading mass spectral library files (particularly MoNA EI or MS2 libraries) where structural metadata like SMILES information is embedded in general-purpose fields (e.g., Comment field) rather than in the dedicated SMILES field expected by mspcompiler's downstream processing steps. Use it after read_lib() has parsed the MSP file into an R list object but before assign_smiles(), assign_ri(), or write_EI_msp() operations.

## When NOT to use

- Input is a NIST EI library already converted via Lib2NIST — these files have proper field structure and do not require reorganize_mona().
- Input is a RIKEN library file — RIKEN libraries already have SMILES and InChIKey well-organized and require no restructuring.
- SMILES information is already in the dedicated SMILES field — reorganize_mona() is redundant.

## Inputs

- MoNA EI library MSP file (GC-MS Spectra format)
- MoNA MS2 library MSP file (LC-MS/MS Positive or Negative Mode format)
- Parsed library object in R list format (output from read_lib())

## Outputs

- Restructured library object with SMILES field populated
- Library object ready for downstream RI assignment and MSP output

## How to apply

Load the MoNA library MSP file using read_lib() with the appropriate type parameter ('EI' for GC-MS or 'MS2' for LC-MS/MS), which parses the file into an internal R list structure. Apply the reorganize_mona() function to systematically extract SMILES information from the Comment field and populate the dedicated SMILES field in the library object. Verify the output by checking that the SMILES field is now populated across all records and that the total row count matches the input library size. This restructuring ensures that subsequent functions like assign_ri() and write_EI_msp() can locate and process the SMILES data without additional parsing.

## Related tools

- **mspcompiler** (Provides the reorganize_mona() function for extracting and restructuring SMILES metadata and integrates the skill into the mass spectral library compilation pipeline) — https://github.com/QizhiSu/mspcompiler
- **R** (Execution environment for running read_lib() and reorganize_mona() functions)
- **MoNA** (Source of EI and MS2 library files requiring SMILES field restructuring) — https://mona.fiehnlab.ucdavis.edu/downloads

## Examples

```
mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI")
mona_ei <- reorganize_mona(mona_ei)
```

## Evaluation signals

- SMILES field is populated in all records after reorganize_mona() execution; verify by checking library$SMILES is not empty
- Row count of output library matches input library — no records lost during restructuring
- SMILES values are valid chemical notation (contain no embedded Comment field text or special characters indicative of parsing failure)
- Downstream functions (assign_ri(), write_EI_msp()) execute without field-not-found errors, confirming proper schema structure
- Spot-check sample records: manually confirm that SMILES extracted from Comment field are chemically accurate and match the compound names

## Limitations

- Reorganize_mona() is specific to MoNA library format; it will not work correctly on NIST, RIKEN, SWGDRUG, or other library sources that use different metadata structures.
- If the Comment field in the input file lacks SMILES information or uses a non-standard encoding, reorganize_mona() may populate SMILES with incorrect or empty values.
- The function does not validate SMILES syntax; chemically invalid SMILES may pass through and cause failures in downstream structure-based operations (e.g., assign_ri() with ChemineR).

## Evidence

- [readme] This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function.: "This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function."
- [other] The reorganize_mona function as a pipeline step that transforms MoNA EI library files into the internal list format expected by downstream processing steps.: "reorganize_mona function as a pipeline step that transforms MoNA EI library files into the internal list format expected by downstream processing steps"
- [other] Apply reorganize_mona() function to extract SMILES information from the Comment field and populate the SMILES field in the library object. Verify the output object contains the expected field structure (SMILES field populated) and that row count matches the input.: "Apply reorganize_mona() function to extract SMILES information from the Comment field and populate the SMILES field in the library object. Verify the output object contains the expected field"
- [other] Load the MoNA EI library MSP file using read_lib() with type='EI' to parse the initial msp structure into an R list object.: "Load the MoNA EI library MSP file using read_lib() with type='EI' to parse the initial msp structure into an R list object."
- [readme] mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI")
mona_ei <- reorganize_mona(mona_ei): "mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI")
mona_ei <- reorganize_mona(mona_ei)"
