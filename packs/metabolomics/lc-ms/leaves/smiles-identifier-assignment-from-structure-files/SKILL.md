---
name: smiles-identifier-assignment-from-structure-files
description: Use when when you have a mass spectral library (MSP format) that lacks SMILES annotations but is paired with a folder of MOL structure files (from Lib2NIST export or similar source).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS Search
  - MS-DIAL
  - ChemineR
  - ChemineOB
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- library(future)
- library(future.apply)
- you can transformed it into a msp file by *Lib2NIST*
- The total number of spectra that your NIST library have can be checked in the *MS Search* program
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES Identifier Assignment from Structure Files

## Summary

Assigns SMILES (Simplified Molecular Input Line Entry System) identifiers to mass spectral library records by matching molecular structures extracted from SDF files to compound names or InChI keys. This enriches spectral records with canonicalized chemical structure notation required for MS-DIAL compatibility and downstream cheminformatics workflows.

## When to use

When you have a mass spectral library (MSP format) that lacks SMILES annotations but is paired with a folder of MOL structure files (from Lib2NIST export or similar source). Apply this skill to populate the SMILES field before combining multi-source EI or MS/MS libraries or preparing libraries for MS-DIAL import.

## When NOT to use

- Library records already contain valid SMILES in the SMILES field; skip directly to RI assignment.
- MOL or SDF structure files are missing or corrupt; SMILES extraction will fail or match zero records.
- Compound names in the library differ substantially from reference structure database names; name-based matching will have low recall.

## Inputs

- MSP file (mass spectral library in mspcompiler format, read via read_lib())
- MOL folder (structure files exported from Lib2NIST or source database)
- SDF file (single combined structure file generated from MOL folder)
- Structure metadata table (TSV from extract_structure() with name, InChIKey, and SMILES)

## Outputs

- Annotated library object with SMILES field populated for all records
- Library ready for RI assignment and MS-DIAL export

## How to apply

First, combine all MOL files in the source folder into a single SDF file using combine_mol2sdf(), then extract molecular structures and metadata from that SDF using extract_structure(), producing a lookup table. Next, call assign_smiles() with the library object and the structure table, specifying the matching strategy: use match='name' for Linux/Mac systems or when InChIKey is unavailable (e.g., SWGDRUG), or use match='inchikey' for Windows systems with reliable InChIKey data. The function performs name-based string matching or InChIKey lookup to retrieve SMILES from the structure table and populate the SMILES field in each library record. Validate by checking that the SMILES field is no longer empty and contains valid SMILES strings (alphanumeric with allowed special characters like [, ], @, =, (, )).

## Related tools

- **mspcompiler** (R package providing assign_smiles(), extract_structure(), and combine_mol2sdf() functions for SMILES assignment workflow) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Utility to export NIST library as MSP + MOL folder pair; generates source files for SMILES assignment) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **ChemineR** (R package for molecular structure I/O and SDF parsing; dependency for extract_structure() and combine_mol2sdf())
- **ChemineOB** (R wrapper for Open Babel; enables structure file format conversion and name-based compound lookup)
- **MS-DIAL** (Target software requiring SMILES-annotated MSP files; validates downstream usability of enriched library)

## Examples

```
nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name")
```

## Evaluation signals

- SMILES field is non-empty for ≥95% of library records (check record count before/after and inspect sample records with write_EI_msp() or read_lib() output).
- All assigned SMILES strings conform to standard SMILES grammar (contain only C, H, N, O, S, P, halogens, brackets, bonds, and stereochemistry markers).
- No duplicate SMILES are assigned to distinct compound names; one-to-many matches indicate name collision or structure database ambiguity.
- Downstream RI assignment (assign_ri) and MS-DIAL import complete without errors on the SMILES-enriched library.
- Manual spot-check: verify 5–10 SMILES strings against a canonical tool (e.g., PubChem, ChemSpider) for chemical correctness.

## Limitations

- Name-based matching is unreliable when compound nomenclature differs between library and structure source (e.g., IUPAC vs. common name); InChIKey matching is more robust but requires high-quality InChIKey data in source.
- Processing time scales with MOL folder size (hundreds of thousands of files can require hours); parallel computing via future package is strongly recommended.
- MOL folder relocation after initial combine_mol2sdf() call will break the pipeline; users must finalize folder location before processing.
- SWGDRUG and other specialized libraries lack InChIKey annotations; must use match='name', reducing match specificity.
- Zero matches for a compound indicate that its name does not exist in the structure database or SDF was not generated from all MOL files; no SMILES will be assigned for that record.

## Evidence

- [methods] Assign SMILES to the library: "Assign SMILES to the library."
- [methods] Extract and reorganize SMILES from structured files: "Extract structure based on the sdf file exported before."
- [readme] Name vs. InChIKey matching strategy for different platforms: "If you are working with Linux-based or Mac OS, please use "match = "inchikey". nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name")"
- [readme] SWGDRUG library constraint on matching method: "As the SWGDRUG file does not contain InChIKey information, even though you are working with Linux-based or Mac OS, you should not use "match = inchikey". "match = "name" is more than enough in this"
- [readme] MOL folder consolidation and structure extraction: "Combine all mol files into a single sdf file for subsequent structure retrieval. Extract structure based on the sdf file exported before."
- [readme] Time and resource requirements for parallel processing: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
