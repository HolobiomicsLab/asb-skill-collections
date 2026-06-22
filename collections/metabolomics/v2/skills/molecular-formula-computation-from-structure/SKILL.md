---
name: molecular-formula-computation-from-structure
description: Use when processing tandem MS/MS libraries in mgf format (such as GNPS) that lack a Molecular Formula (MF) field but contain valid SMILES strings. The computed formulas are required before combining libraries or writing them to msp format for MS-DIAL compatibility.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0393
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - MS-DIAL
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- MS-DIAL friendly msp file
- organize them into a neat and up-to-date msp file that can be used in MS-DIAL.
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

# Molecular formula computation from structure

## Summary

Compute molecular formulas from SMILES strings or structural representations when the molecular formula field is missing or incomplete in tandem MS/MS libraries. This is essential for preparing libraries (e.g., GNPS in mgf format) for downstream MS-DIAL annotation where molecular formula is a required metadata field.

## When to use

Apply this skill when processing tandem MS/MS libraries in mgf format (such as GNPS) that lack a Molecular Formula (MF) field but contain valid SMILES strings. The computed formulas are required before combining libraries or writing them to msp format for MS-DIAL compatibility.

## When NOT to use

- Library already contains a complete and validated Molecular Formula field
- SMILES information is missing or malformed in the input library; computation will fail or produce invalid formulas
- Input is an EI library or already in msp format; use read_lib() with appropriate type parameter instead

## Inputs

- MS/MS library object in mgf format (loaded via read_lib with format='mgf')
- Library records with SMILES field populated

## Outputs

- MS/MS library object with Molecular Formula (MF) field computed and populated from SMILES
- msp-compatible library ready for polarity separation and MS-DIAL writing

## How to apply

Load the MS/MS library in mgf format using read_lib() with format="mgf" parameter. Verify that SMILES information is present in the loaded library object. Apply the complete_mgf() function to compute molecular formulas from the existing SMILES strings. The function generates the MF field by parsing the SMILES representation. After computation, validate that the MF field is now populated in all records (or at least the subset with valid SMILES). This step must occur before polarity separation or library concatenation, as downstream writing functions expect the MF field to be present.

## Related tools

- **mspcompiler** (R package providing complete_mgf() function to compute molecular formulas from SMILES in mgf-format MS/MS libraries) — https://github.com/QizhiSu/mspcompiler
- **R** (Runtime environment for executing complete_mgf() function)
- **MS-DIAL** (Target annotation software that requires computed Molecular Formula field in msp input files)

## Examples

```
gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")
gnps <- complete_mgf(gnps)
```

## Evaluation signals

- Verify that the MF field is present in all library records post-computation (inspect with str() or head() on the library object)
- Confirm MF values follow expected chemical formula syntax (e.g., C6H12O6, not empty or null)
- Cross-check a subset of computed formulas against known compounds by comparing molecular weight or exact mass
- Ensure no records are lost or duplicated during computation; row count should remain unchanged
- Subsequent write_MS2_msp() call should complete without errors indicating missing MF field

## Limitations

- Computation accuracy depends entirely on the validity and canonicalization of input SMILES strings; malformed SMILES will produce incorrect or missing formulas
- Function does not validate the chemical plausibility of computed formulas; invalid SMILES may yield syntactically correct but chemically nonsensical formulas
- GNPS library or other mgf-format sources may have incomplete or inconsistent SMILES coverage; records lacking SMILES will not receive computed formulas
- Time complexity scales with library size; processing large libraries (e.g., all-GNPS) may require hours on standard hardware

## Evidence

- [methods] GNPS library does not have the Molecular Formula field, so formulas must be computed from SMILES: "this library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function"
- [readme] The complete_mgf function specifically calculates molecular formula from SMILES in mgf-format libraries: "Compute MF
gnps <- complete_mgf(gnps)"
- [methods] Molecular Formula computation is a prerequisite step before separating polarity in combined libraries: "so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function. Finally, both positive and negative modes are in a single file as well"
- [readme] GNPS library processing workflow explicitly shows complete_mgf applied to mgf input before polarity separation: "gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")
# Compute MF
gnps <- complete_mgf(gnps)
gnps_pos <- separate_polarity(gnps, polarity = "pos")"
