---
name: r-object-inspection-and-validation
description: Use when after performing assignment operations (assign_ri, assign_smiles) or combining multiple library objects (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
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
---

# R Object Inspection and Validation

## Summary

Verify that mass spectral library objects in R have been correctly populated with expected fields (e.g., RI, SMILES, InChIKey) after compilation and assignment operations. This skill ensures data integrity before writing libraries to MSP format or downstream use in MS-DIAL.

## When to use

After performing assignment operations (assign_ri, assign_smiles) or combining multiple library objects (e.g., via c(nist_ei, riken_ei, mona_ei)), inspect the resulting R object to confirm that target fields were populated correctly and no records were inadvertently dropped or corrupted during the workflow.

## When NOT to use

- When you have not yet performed any assignment operations and are simply exploring the raw input library structure.
- When working with libraries that are known to not require RI or SMILES fields (e.g., in-house libraries without structural annotation).
- If the inspection goal is statistical modeling or clustering of spectral features rather than data quality assurance before export.

## Inputs

- Compiled EI library R object (from read_lib or combine operations)
- Compiled MS2 library R object
- Combined library object (result of c() operation on multiple library objects)

## Outputs

- Inspection report (printed to console)
- Validation summary (logical TRUE/FALSE or warning messages)
- Test MSP file subset (optional verification output)

## How to apply

Load the compiled library object in R and inspect its structure using standard R inspection tools (e.g., str(), head(), summary(), or direct column access). For RI assignment, verify that the RI column contains numeric values and check a sample of records to confirm Kovats RI values are present and within expected ranges for the chosen polarity (semi-polar, non-polar, or polar). When verifying SMILES assignment, spot-check that the SMILES field is populated with valid SMILES strings matching the compound identities. For combined objects, confirm the total number of records and absence of NAs in critical fields. As a final validation step, write a small subset of the library to MSP format using write_EI_msp() and manually inspect the resulting MSP file to confirm RI and SMILES fields are present in the output.

## Related tools

- **mspcompiler** (provides R functions (read_lib, assign_ri, assign_smiles, write_EI_msp) that generate and export library objects to be inspected) — https://github.com/QizhiSu/mspcompiler
- **R** (execution environment; built-in functions str(), head(), summary() used for object inspection)
- **MS-DIAL** (downstream application that consumes validated MSP libraries; inspection confirms compatibility) — http://prime.psc.riken.jp/compms/msdial/main.html

## Examples

```
# Inspect combined EI library after RI assignment
str(combine_ei)
head(combine_ei)
# Check RI column for NAs and verify numeric values
summary(combine_ei$RI)
# Write test subset and inspect output
write_EI_msp(combine_ei[1:100], "D:/MS_libraries/test_output.msp")
```

## Evaluation signals

- RI column contains numeric values and no NAs for compounds matched to semi-polar (or specified polarity) GC columns.
- SMILES field is populated with valid SMILES strings (spot-check: compound names match their SMILES chemical structure).
- Total record count in combined object equals or exceeds the sum of input libraries minus expected deduplicates.
- InChIKey or name-based matching succeeded without misalignment (verify via head() on key columns).
- MSP file written from library contains RI and SMILES fields in the output (manual inspection of write_EI_msp() output confirms presence).

## Limitations

- RI assignment filters records by polarity (semi-polar, non-polar, polar) and column type (capillary only); non-capillary RI records are discarded by design, so absence of RI in some compounds is expected.
- RI values with standard deviation >30 across multiple records are discarded; median RI is used when multiple records exist, which may hide inter-lab variation.
- SMILES assignment depends on successful matching by name or InChIKey; compounds with ambiguous or missing names may fail to match and remain unassigned.
- Large libraries (hundreds of thousands of MOL files or compounds) may require substantial memory and time to inspect comprehensively; subset inspection may be necessary on memory-limited systems.

## Evidence

- [other] Verify that RI fields are populated in the resulting library object by inspecting the RI column in the output or writing the output to MSP format using write_EI_msp and confirming RI presence in the file.: "Verify that RI fields are populated in the resulting library object by inspecting the RI column in the output or writing the output to MSP format using write_EI_msp and confirming RI presence in the"
- [readme] Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used. This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard"
- [readme] Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey". nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name"): "Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey"."
- [readme] After read in and organize all these libraries, we can now combine them into a single file, assign experimental RI retrieved from the "ri.dat" and "USER.DBU" files: "After read in and organize all these libraries, we can now combine them into a single file, assign experimental RI retrieved from the "ri.dat" and "USER.DBU" files"
