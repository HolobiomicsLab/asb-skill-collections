---
name: mgf-metadata-completion-from-smiles
description: Use when when processing MGF-format MS2 spectral libraries (e.g., GNPS) that contain SMILES but lack the Molecular Formula field, and you need to prepare the library for MS-DIAL import or polarity-based separation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0157
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - RIKEN
  - MoNA
  - GNPS
  - MS-DIAL
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
- The MS-DIAL developers have compiled an EI library with Kovat RI included
- The RIKEN MS2 libraries can be download from the MS-DIAL homepage
- The MassBank of North America (MoNA) has an EI library available
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

# MGF Metadata Completion from SMILES

## Summary

Complete missing Molecular Formula (MF) fields in MGF-format mass spectral libraries by calculating MF from existing SMILES strings. This is essential for libraries like GNPS that lack comprehensive metadata annotation required by downstream MS-DIAL processing.

## When to use

When processing MGF-format MS2 spectral libraries (e.g., GNPS) that contain SMILES but lack the Molecular Formula field, and you need to prepare the library for MS-DIAL import or polarity-based separation workflows.

## When NOT to use

- Input library already has complete Molecular Formula metadata (e.g., RIKEN MS2 libraries).
- SMILES field is absent or unpopulated in the library; MF cannot be calculated without structure information.
- Working with EI-format libraries, which do not use MGF input format.

## Inputs

- MGF-format spectral library file (e.g., ALL_GNPS.mgf)
- Library object in R with SMILES field populated, MF field absent or incomplete

## Outputs

- Library object with Molecular Formula field populated for all entries
- Ready for downstream polarity separation and MSP export

## How to apply

After loading an MGF-format library using read_lib() with format='mgf', apply the complete_mgf() function to infer missing Molecular Formula values directly from SMILES strings present in the library records. This step should be performed before separating by ionization polarity (separate_polarity()) and writing output MSP files. The function iterates over library entries, identifies records lacking MF, and computes MF from the SMILES chemical structure representation using standard chemistry rules (element composition from the structure graph).

## Related tools

- **mspcompiler** (R package providing complete_mgf() function for MGF metadata inference from SMILES) — https://github.com/QizhiSu/mspcompiler
- **R** (Environment for executing complete_mgf() and library processing functions)
- **MS-DIAL** (Downstream software requiring complete Molecular Formula metadata in MSP files)
- **GNPS** (Source library in MGF format containing SMILES but lacking MF) — https://gnps.ucsd.edu/ProteoSAFe/libraries.jsp

## Examples

```
gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")
gnps <- complete_mgf(gnps)
```

## Evaluation signals

- All spectral records in the output library contain a non-empty Molecular Formula field
- Molecular Formula values are chemically valid (e.g., match expected elemental composition from SMILES structure)
- No records are dropped or lost during MF calculation; record count matches input library
- Output library successfully passes subsequent separate_polarity() and write_MS2_msp() steps without errors
- Generated MSP files conform to MS-DIAL format specification with MF field present

## Limitations

- Requires SMILES field to be present and correctly formatted in the input library; malformed SMILES will cause calculation failure or incorrect MF inference.
- MF calculation relies on chemical structure parsing; ambiguous or non-standard SMILES notations may produce unexpected results.
- Function is designed only for MGF-format input; MSP and other spectral formats require alternative preparation steps.
- Large libraries (hundreds of thousands of records) may experience memory or computational overhead during batch MF calculation.

## Evidence

- [readme] GNPS library lacks MF field, requiring computation from SMILES: "this library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function"
- [other] complete_mgf() is the dedicated function for MGF metadata completion: "complete_mgf() to calculate Molecular Formula from SMILES where missing"
- [readme] complete_mgf() must be applied to GNPS library in MGF format before polarity separation: "gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf")
# Compute MF
gnps <- complete_mgf(gnps)
gnps_pos <- separate_polarity(gnps, polarity = "pos")"
- [methods] MGF metadata completion is part of standardized MS2 library compilation workflow: "For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing"
