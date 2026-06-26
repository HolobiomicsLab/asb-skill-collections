---
name: library-object-validation
description: Use when after applying mspcompiler pipeline transformation steps (e.g.,
  reorganize_mona, assign_smiles, assign_ri, read_multilibs, separate_polarity, complete_mgf)
  to confirm the operation succeeded without data loss or structural corruption.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mspcompiler
  - R
  - MoNA
  - future
  - future.apply
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- The MassBank of North America (MoNA) has an EI library available
- The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads
- library(future)
- library(future.apply)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05389
  all_source_dois:
  - 10.1021/acs.analchem.2c05389
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Validate mass spectral library object structure and content

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that a compiled mass spectral library object (EI or MS2) contains the expected field structure, populated key columns (especially SMILES and retention index fields), and correct row counts after pipeline transformation steps. This ensures data integrity before downstream processing or file export.

## When to use

After applying mspcompiler pipeline transformation steps (e.g., reorganize_mona, assign_smiles, assign_ri, read_multilibs, separate_polarity, complete_mgf) to confirm the operation succeeded without data loss or structural corruption. Use before writing the library to MSP or MGF format, or before combining multiple library objects.

## When NOT to use

- Library object has not yet undergone any transformation (use for spot-checks post-transformation, not as a prerequisite to the first read_lib call)
- Input is a raw MSP or MGF file (validate the parsed R object after read_lib, not the file itself)
- Task is to clean or repair corrupted library data (validation detects problems; use dedicated cleaning functions to fix them)

## Inputs

- R list object representing a mass spectral library (output from read_lib, read_multilibs, reorganize_mona, assign_smiles, assign_ri, separate_polarity, or complete_mgf)
- Expected row count (from input documentation or prior operation)

## Outputs

- Validation report (boolean pass/fail or list of structural issues detected)
- Confirmed library object ready for downstream processing or export

## How to apply

Inspect the output library object to verify: (1) all required fields are present (e.g., Name, Formula, SMILES, Retention Index where applicable); (2) key fields that were just populated or transformed (e.g., SMILES field after reorganize_mona or assign_smiles, RI values after assign_ri) contain non-null, non-empty values; (3) the total record count matches the input (or expected merged count if combining libraries); (4) field types and content format conform to msp/mgf specification (e.g., SMILES strings are valid, RI values are numeric). Use the structure() and summary() functions in R or manual spot-checks on a sample of records to confirm these invariants before proceeding to write operations.

## Related tools

- **mspcompiler** (Provides pipeline functions (reorganize_mona, assign_smiles, assign_ri, read_lib, read_multilibs, separate_polarity, complete_mgf) whose outputs require validation) — https://github.com/QizhiSu/mspcompiler
- **R** (Language for constructing validation checks (structure(), summary(), nrow(), lapply() inspection))

## Examples

```
# After running: mona_ei <- reorganize_mona(mona_ei)
# Validate with:
cat('Record count:', nrow(mona_ei), '\n')
cat('SMILES populated:', sum(!is.na(mona_ei$SMILES) & mona_ei$SMILES != ''), 'of', nrow(mona_ei), '\n')
head(mona_ei[c('Name', 'SMILES')])
```

## Evaluation signals

- All records retain their original count (nrow() matches input or expected merge total)
- No new NA or empty string values appear unexpectedly in previously-populated fields
- SMILES field is populated and non-empty for records after reorganize_mona or assign_smiles (when expected from input source)
- Retention Index (RI) field contains numeric values within plausible range (e.g., 0–10000 for Kovat indices) after assign_ri
- Field names and structure match downstream consumption requirements (e.g., MS-DIAL MSP importer or MGF standard)

## Limitations

- Validation only checks structural integrity and field presence; it does not verify chemical accuracy or correctness of individual SMILES or RI values
- When combining libraries via concatenation (c()), validation must account for polarity-specific or source-specific field variations (e.g., some sources may lack RI data)
- Spot-checking a sample of records is manual and may miss rare field corruption; comprehensive programmatic validation of all rows is recommended for large libraries (>100k spectra)

## Evidence

- [methods] Verify the output object contains the expected field structure (SMILES field populated) and that row count matches the input.: "Verify the output object contains the expected field structure (SMILES field populated) and that row count matches the input."
- [readme] Once you have the \*.MSP file (normally hundreds megabytes) and the correspondent \*.MOL folder (hundreds thousands .MOL files inside the folder) exported, you can use the following code to add *SMILES* and *Retention Index (RI)*.: "Once you have the \*.MSP file (normally hundreds megabytes) and the correspondent \*.MOL folder (hundreds thousands .MOL files inside the folder) exported, you can use the following code to add"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
