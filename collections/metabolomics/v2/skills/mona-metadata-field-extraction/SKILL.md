---
name: mona-metadata-field-extraction
description: Use when when you have loaded a MoNA mass spectral library (GC-MS or LC-MS/MS) in MSP format and observe that SMILES strings are present in the Comment field rather than in a dedicated SMILES metadata field.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - mspcompiler
  - R
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler_cq
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler_cq
schema_version: 0.2.0
---

# MoNA metadata field extraction

## Summary

Extract SMILES notation embedded in the Comment field of MoNA mass spectral library records and relocate it to the dedicated SMILES metadata field for proper organization and downstream processing. This skill is essential when working with MoNA EI or LC-MS/MS libraries where structural information is stored in an unstructured comment rather than a dedicated metadata slot.

## When to use

When you have loaded a MoNA mass spectral library (GC-MS or LC-MS/MS) in MSP format and observe that SMILES strings are present in the Comment field rather than in a dedicated SMILES metadata field. This is the standard format for MoNA exports and must be corrected before combining libraries or performing structure-dependent analyses (e.g., molecular formula calculation, retention index assignment).

## When NOT to use

- If SMILES information is already in a dedicated SMILES field; reorganize_mona() is designed for MoNA-specific formatting and would be redundant.
- If the library source is NIST, RIKEN, or SWGDRUG (these sources do not embed SMILES in Comment fields).
- If you only need the Comment field as-is and do not require structured SMILES for downstream analysis (e.g., molecular formula calculation, spectral matching).

## Inputs

- MoNA MSP file (GC-MS Spectra or LC-MS/MS mode)
- Loaded library object from read_lib() with type='EI' or type='MS2'

## Outputs

- Reorganized library object with SMILES field populated from Comment field
- Library ready for downstream enrichment (molecular formula, polarity separation, RI assignment)

## How to apply

Load the MoNA MSP file using read_lib() with the appropriate type (EI for GC-MS or MS2 for LC-MS/MS). Apply the reorganize_mona() function to each library object, which parses the Comment field line-by-line to identify and extract SMILES notation strings (typically prefixed with identifiers like 'SMILES=' or similar markers), validates the syntax for chemical plausibility (balanced brackets, valid atom symbols, charge notation), and populates the SMILES metadata field. The function operates in-place on the library object. After reorganization, verify that records originally containing Comment-embedded SMILES now have non-empty SMILES fields and that the Comment field still retains any non-SMILES content. This step must precede any structure-based enrichment (molecular formula calculation, polarity separation) and should be applied to each MoNA library independently before combining with other sources.

## Related tools

- **mspcompiler** (R package providing read_lib() to load MSP files and reorganize_mona() to extract and relocate SMILES from Comment field) — https://github.com/QizhiSu/mspcompiler
- **R** (Execution environment for mspcompiler functions)

## Examples

```
mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI")
mona_ei <- reorganize_mona(mona_ei)
```

## Evaluation signals

- All records that originally had SMILES in the Comment field now have a non-empty SMILES field matching the extracted pattern.
- SMILES strings pass basic syntax validation: balanced parentheses, valid element symbols (C, H, N, O, P, S, etc.), and valid bond notation (-, =, #, :).
- The Comment field retains any descriptive text that is not SMILES notation (e.g., acquisition parameters, source attribution).
- No records are lost or truncated during the reorganization; record count and other metadata remain unchanged.
- Downstream functions (e.g., complete_mgf for molecular formula calculation) successfully operate on the reorganized library without errors related to missing SMILES.

## Limitations

- The reorganize_mona() function is specific to MoNA formatting conventions; it may not work with other libraries that embed SMILES in different fields or formats.
- If SMILES strings in the Comment field are malformed or non-standard, they may fail validation or be rejected; the function does not attempt to repair invalid SMILES.
- Some MoNA records may not contain SMILES information at all; these records will have empty SMILES fields after reorganization.
- The function assumes SMILES is the only structured data in the Comment field or is clearly delimited; ambiguous or mixed content may lead to incorrect extraction.

## Evidence

- [readme] MoNA library SMILES extraction requirement: "This file has SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field"
- [readme] reorganize_mona function purpose: "the SMILES has to be extracted from the *Comment* and put into the *SMILES* field by the *reorganize_mona* function."
- [readme] MoNA EI library download and processing: "The MassBank of North America (MoNA) has an EI library available for download as well, <https://mona.fiehnlab.ucdavis.edu/downloads>. Please download "GC-MS Spectra" in "MSP" form."
- [methods] Reorganize SMILES workflow step: "Reorganize SMILES field from MoNA Comment field"
- [readme] MoNA MS2 library reorganization: "mona_ms2_pos <- reorganize_mona(mona_ms2_pos)"
