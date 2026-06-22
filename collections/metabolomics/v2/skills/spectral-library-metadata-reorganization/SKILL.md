---
name: spectral-library-metadata-reorganization
description: Use when when ingesting mass spectral libraries (EI or MS2) where SMILES information is embedded in the Comment field rather than in a dedicated SMILES metadata field—particularly common in MoNA GC-MS and LC-MS/MS exports.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - mspcompiler
  - R
  - MS-DIAL
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05389
  all_source_dois:
  - 10.1021/acs.analchem.2c05389
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-metadata-reorganization

## Summary

Reorganize embedded chemical metadata within mass spectral library records by extracting SMILES notation from unstructured comment fields and populating dedicated structured metadata slots. This ensures proper organization and downstream compatibility with spectral matching and analysis tools like MS-DIAL.

## When to use

When ingesting mass spectral libraries (EI or MS2) where SMILES information is embedded in the Comment field rather than in a dedicated SMILES metadata field—particularly common in MoNA GC-MS and LC-MS/MS exports. Apply this skill before combining multiple spectral libraries or assigning additional derived metadata (e.g., molecular formula, retention index).

## When NOT to use

- Input library already has SMILES information in a dedicated SMILES field
- Comment field does not contain SMILES notation or contains only free-text comments
- Library format is not MSP (e.g., mgf format; use complete_mgf() instead)

## Inputs

- MSP format spectral library file with Comment field containing embedded SMILES
- Loaded library object from read_lib()

## Outputs

- Reorganized library object with SMILES field populated from Comment field
- MSP format file with dedicated SMILES metadata field (after write_EI_msp() or write_MS2_msp())

## How to apply

Load the MSP file into R using read_lib() with the appropriate type parameter ('EI' or 'MS2'). Parse the Comment field of each record to identify and extract SMILES notation strings using pattern matching. Validate extracted SMILES for chemical plausibility (balanced brackets, valid SMILES syntax). Populate the SMILES field for each record with the extracted and validated value using the reorganize_mona() function. Verify that all records with Comment-embedded SMILES now have a non-empty SMILES field and confirm the reorganized library object is returned with proper structure intact.

## Related tools

- **mspcompiler** (R package providing reorganize_mona() function to extract and relocate SMILES from Comment field to SMILES field) — https://github.com/QizhiSu/mspcompiler
- **R** (Runtime environment for executing read_lib() and reorganize_mona() functions)
- **MS-DIAL** (Downstream spectral matching and analysis tool that requires properly organized SMILES in dedicated field)

## Examples

```
mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type = "EI"); mona_ei <- reorganize_mona(mona_ei)
```

## Evaluation signals

- All records with Comment-embedded SMILES now have a non-empty SMILES field after reorganization
- SMILES strings validate syntactically (balanced brackets, valid atom/bond notation)
- No data loss: record count and spectrum peak information remain unchanged
- Reorganized library object structure passes schema validation for MSP format
- Comment field still retains original content or is appropriately cleared per library requirements

## Limitations

- Requires SMILES notation to be present in the Comment field; fails silently or returns empty SMILES if pattern does not match expected format
- Does not handle malformed or incomplete SMILES strings; validation detects syntax errors but does not repair them
- Function is library-specific (reorganize_mona); MoNA-specific patterns may not generalize to other libraries with different Comment field conventions
- No changelog or version tracking documented; compatibility with different mspcompiler versions not specified

## Evidence

- [readme] This file has SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field: "This file has SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field"
- [methods] Parse the Comment field of each record to identify and extract SMILES notation strings. Validate extracted SMILES strings for chemical plausibility (e.g., balanced brackets, valid SMILES syntax).: "Parse the Comment field of each record to identify and extract SMILES notation strings. Validate extracted SMILES strings for chemical plausibility (e.g., balanced brackets, valid SMILES syntax)."
- [readme] mona_ei <- reorganize_mona(mona_ei): "mona_ei <- reorganize_mona(mona_ei)"
- [methods] Reorganize SMILES field from MoNA Comment field: "Reorganize SMILES field from MoNA Comment field"
