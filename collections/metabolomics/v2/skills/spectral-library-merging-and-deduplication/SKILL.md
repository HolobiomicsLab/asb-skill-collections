---
name: spectral-library-merging-and-deduplication
description: Use when when building a comprehensive reference spectral library for metabolomics or chemical identification, you have multiple source libraries in different formats (msp, mgf, NIST binary) and ionization modes (positive/negative MS/MS or EI) that need to be combined into a single.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
  tools:
  - mspcompiler
  - R
  - MS-DIAL
  - Lib2NIST
  - ChemmineR
  techniques:
  - LC-MS
  - GC-MS
  - ion-mobility-MS
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

# spectral-library-merging-and-deduplication

## Summary

Merge and organize multiple mass spectral libraries (EI, MS/MS) from heterogeneous sources (NIST, RIKEN, MoNA, GNPS) into unified, polarity-separated msp files compatible with MS-DIAL. This skill handles format conversion, structure annotation, and deduplication across public and commercial library resources.

## When to use

When building a comprehensive reference spectral library for metabolomics or chemical identification, you have multiple source libraries in different formats (msp, mgf, NIST binary) and ionization modes (positive/negative MS/MS or EI) that need to be combined into a single, MS-DIAL-compatible resource with consistent SMILES, molecular formula, and optional retention index metadata.

## When NOT to use

- Input libraries are already merged and deduplicated — use this only when combining disparate, independently-sourced spectral datasets.
- Only processing a single homogeneous library from one vendor — the merging and polarity-separation logic adds unnecessary overhead.
- Working with ion mobility or high-resolution MS data not represented in msp or mgf format — mspcompiler is designed for tandem MS/MS and EI libraries only.

## Inputs

- NIST EI library (msp + MOL files exported via Lib2NIST)
- RIKEN MS/MS libraries (MSMS-Public-Pos-VS15.msp, MSMS-Public-Neg-VS15.msp)
- MoNA GC-MS or LC-MS/MS libraries (msp format)
- SWGDRUG EI library (msp + MOL files)
- GNPS library (mgf format)
- NIST retention index files (ri.dat, USER.DBU)

## Outputs

- Combined positive-mode MS/MS library (combine_ms2_pos.msp)
- Combined negative-mode MS/MS library (combine_ms2_neg.msp)
- Combined EI library (combine_ei.msp)
- Structure annotation file (extracted from sdf, txt format)

## How to apply

Load each source library using read_lib() with appropriate type ('EI', 'MS2') or format ('mgf') parameter. For NIST and SWGDRUG libraries, export via Lib2NIST to msp + MOL files, then combine MOL files to sdf, extract structures, and assign SMILES using assign_smiles() with match='name' (Windows) or match='inchikey' (Linux/Mac). For MoNA libraries, use reorganize_mona() to extract SMILES from the Comment field into the SMILES field. For GNPS (mgf format), use complete_mgf() to compute molecular formula from SMILES. Separate mixed-polarity libraries using separate_polarity(polarity='pos') and separate_polarity(polarity='neg'). Concatenate all positive-mode libraries into one object and all negative-mode libraries into another. Optionally assign experimental retention indices from NIST ri.dat/USER.DBU files using assign_ri() specifying column polarity ('semi-polar', 'non-polar', 'polar'). Finally, write the combined libraries using write_MS2_msp() or write_EI_msp() to generate final output files.

## Related tools

- **mspcompiler** (R package that reads, reorganizes, merges, and writes MS libraries in msp format; core tool for library compilation and polarity separation) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Converts NIST binary library format to msp and MOL files for subsequent structure extraction and SMILES assignment) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS-DIAL** (Target software that consumes the polarity-separated msp output files for metabolite identification and annotation)
- **R** (Execution environment for mspcompiler functions; required for parallel computation using future and future.apply packages)
- **ChemmineR** (R package dependency for structure manipulation and SMILES-to-InChIKey matching in assign_smiles())

## Examples

```
gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf"); gnps <- complete_mgf(gnps); gnps_pos <- separate_polarity(gnps, polarity = "pos"); gnps_neg <- separate_polarity(gnps, polarity = "neg"); combine_ms2_pos <- c(nist_ms2_pos, riken_ms2_pos, mona_ms2_pos, gnps_pos); write_MS2_msp(combine_ms2_pos, "D:MS_libraries/combine_ms2_pos.msp")
```

## Evaluation signals

- Output msp files contain complete records with SMILES, Molecular Formula, Precursor m/z, and Fragment m/z fields for all entries.
- Positive-mode and negative-mode MS/MS libraries are properly separated (verified by checking polarity field in output records).
- No duplicate entries exist within each polarity-separated library (count unique compound names/InChIKeys before and after merge).
- Retention index values are present and consistent with column polarity specification (semi-polar, non-polar, or polar) if assign_ri() was applied.
- Output files are readable by MS-DIAL without format or schema errors (validated by importing into MS-DIAL and checking parameter tree).

## Limitations

- The entire mol-to-sdf-to-structure extraction workflow is time-consuming (several hours) due to large file counts; parallel computing with future/future.apply packages is essential but requires careful resource management.
- SMILES-to-InChIKey matching on Windows requires match='name' instead of match='inchikey' due to ChemmineOB build limitations; this may reduce matching accuracy for compounds with similar names.
- Retention index assignment filters to capillary GC columns only and discards Lee RI values; non-capillary GC data will be excluded from the final RI annotations.
- When multiple RI records exist for a single compound, the median is used and records with standard deviation > 30 are discarded; this removes high-variability data but may lose important column-specific variation.
- The GNPS library processing requires pre-computed SMILES; entries lacking SMILES cannot contribute molecular formula via complete_mgf().

## Evidence

- [methods] separate polarity into positive and negative modes: "separate them by the separate_polarity function"
- [intro] polarity-separated msp files for MS-DIAL: "msp file that can be used in MS-DIAL"
- [intro] multiple heterogeneous sources: "compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS"
- [methods] Lib2NIST export format: "Select "Text File(.MSP) + MOLfiles linked by BOTH" in *Output Format*"
- [methods] SMILES extraction from MoNA: "This file has SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field"
- [readme] GNPS mgf handling: "the GNPS library is organized in mgf format, so it has to be treated differently. Hence, we have to set *format = "mgf"* in the *read_lib* function"
- [readme] time-consuming parallel processing requirement: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] RI filtering thresholds: "When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded."
