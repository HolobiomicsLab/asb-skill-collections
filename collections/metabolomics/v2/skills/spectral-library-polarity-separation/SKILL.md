---
name: spectral-library-polarity-separation
description: Use when you have loaded an MS2 library (from NIST, GNPS, or other sources via read_lib()) that contains both positive and negative ionization modes mixed in a single file, and you need to produce two separate, polarity-specific MSP files for use in MS-DIAL or similar tandem MS analysis software.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0630
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - RIKEN
  - MoNA
  - GNPS
  - MS-DIAL
  - read_lib
  - write_MS2_msp
  - complete_mgf
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
  - build: coll_mspcompiler_cq
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
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

# spectral-library-polarity-separation

## Summary

Separate mixed-polarity tandem mass spectral (MS2) libraries into positive and negative ionization mode files for MS-DIAL compatibility. This skill is essential when compiled libraries from sources like NIST or GNPS contain both polarities in a single MSP or MGF file but downstream analysis requires polarity-specific spectral databases.

## When to use

Apply this skill when you have loaded an MS2 library (from NIST, GNPS, or other sources via read_lib()) that contains both positive and negative ionization modes mixed in a single file, and you need to produce two separate, polarity-specific MSP files for use in MS-DIAL or similar tandem MS analysis software.

## When NOT to use

- Library is already separated into distinct positive and negative files
- Input is an EI (electron ionization) library, which does not use ionization polarity
- You need to preserve mixed-polarity records in a single file for deconvolution or comparative analysis

## Inputs

- MS2 library object (loaded via read_lib with type='MS2')
- MGF-format spectral library (loaded via read_lib with format='mgf')
- Library with both positive and negative ionization modes

## Outputs

- Positive-mode MS2 library object (polarity='pos')
- Negative-mode MS2 library object (polarity='neg')
- MSP file for positive mode (written via write_MS2_msp)
- MSP file for negative mode (written via write_MS2_msp)

## How to apply

After reading the MS2 library (using read_lib() with type='MS2' or format='mgf'), call separate_polarity() twice—once with polarity='pos' and once with polarity='neg'—to partition the library object into positive and negative subsets. For NIST MS2, this step follows structure assignment (assign_smiles()) and precedes final writing. For GNPS libraries in MGF format, call complete_mgf() first to calculate molecular formula from SMILES where missing, then separate_polarity(). The separation logic filters records by the ionization mode field; verification is performed by confirming no mixed polarities remain within a single output file and that all records are retained across the two outputs.

## Related tools

- **mspcompiler** (R package that implements separate_polarity() function for partitioning MS2 libraries by ionization mode) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Downstream software that consumes polarity-separated MSP files as spectral databases)
- **read_lib** (mspcompiler function to load MS2 libraries from MSP or MGF files before polarity separation) — https://github.com/QizhiSu/mspcompiler
- **write_MS2_msp** (mspcompiler function to write polarity-separated libraries to MS-DIAL-compatible MSP format) — https://github.com/QizhiSu/mspcompiler
- **complete_mgf** (mspcompiler function to compute molecular formula from SMILES in GNPS MGF libraries before polarity separation) — https://github.com/QizhiSu/mspcompiler

## Examples

```
nist_ms2_pos <- separate_polarity(nist_ms2, polarity = "pos")
nist_ms2_neg <- separate_polarity(nist_ms2, polarity = "neg")
write_MS2_msp(nist_ms2_pos, "D:/MS_libraries/nist_ms2_pos.msp")
write_MS2_msp(nist_ms2_neg, "D:/MS_libraries/nist_ms2_neg.msp")
```

## Evaluation signals

- Output MSP files contain no records with mixed ionization polarities (all records in positive file marked '+', all in negative file marked '−' or 'neg')
- Record count across both output files equals the input library record count (no loss or duplication)
- Output files conform to MS-DIAL MSP specification for header, polarity field, and spectral peak format
- Each output file header contains correct polarity annotation readable by MS-DIAL import functions

## Limitations

- Separation depends on correct polarity annotation in the source library; mislabeled or missing polarity fields will cause misclassification
- GNPS libraries in MGF format require prior call to complete_mgf() to calculate molecular formula; separation alone does not fill missing MF values
- Large libraries (hundreds of thousands of records) processed without parallel computing may be time-consuming; mspcompiler examples use future and future.apply for parallelization

## Evidence

- [readme] MS2 libraries can be processed in a similar way, but positive and negative modes are normally separated into 2 msp files.: "positive and negative modes are normally separated into 2 msp files"
- [readme] The exported msp file has both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function.: "both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function"
- [other] separate_polarity() with polarity='pos' and polarity='neg'. Combine all four sources (NIST, RIKEN, MoNA, GNPS) into two polarity-specific objects using c(). Write polarity-separated libraries to MSP format using write_MS2_msp()...: "Separate both NIST and GNPS libraries into positive and negative modes using separate_polarity() with polarity='pos' and polarity='neg'"
- [other] Validation: output MSP files conform to MS-DIAL format specification and contain no mixed polarities within a single file.: "output MSP files conform to MS-DIAL format specification and contain no mixed polarities within a single file"
- [other] For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing.: "use complete_mgf() to calculate Molecular Formula from SMILES where missing"
