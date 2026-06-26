---
name: parallel-computing-workflow-orchestration
description: Use when when compiling EI or MS/MS spectral libraries from multiple
  gigabyte-scale sources (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - parallel
  - Lib2NIST
  - MS Search
  - MS-DIAL
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- library(future)
- library(future.apply)
- library(parallel)
- you can transformed it into a msp file by *Lib2NIST*
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

# parallel-computing-workflow-orchestration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Orchestrate computationally intensive mass spectrometry library compilation workflows across multiple processor cores using the R future package to reduce wall-clock time. This skill enables safe parallel execution of library reading, structure extraction, SMILES assignment, and retention index computation on large-scale MSP and MOL file sets without race conditions or data corruption.

## When to use

When compiling EI or MS/MS spectral libraries from multiple gigabyte-scale sources (e.g., NIST, RIKEN, MoNA, SWGDRUG) that require sequential steps of MOL-to-SDF conversion, structure extraction, SMILES assignment, and RI assignment—processes that are individually time-consuming (hours on single cores) and benefit from multi-core parallelization. Triggers include: library size >100 MB, MOL folder containing >100,000 files, or workflow consisting of independent per-spectrum or per-file operations.

## When NOT to use

- Input libraries are already small (<50 MB) or few (<10,000 spectra): parallelization overhead outweighs gains; use sequential execution instead.
- Workflow includes non-parallelizable steps or shared mutable state: future cannot safely parallelize write operations on a single output file; final output must be serialized.
- System has <4 CPU cores: detectCores() - 1 yields <3 workers; multisession overhead and context-switching cost more than serial execution.

## Inputs

- MSP file (NIST EI library)
- MOL folder (structure files linked to MSP records)
- MSP file (RIKEN EI library with Kovats RI)
- MSP file (MoNA GC-MS Spectra)
- MSP file (SWGDRUG EI library)
- ri.dat file (NIST retention index data)
- USER.DBU file (NIST user RI database)
- SDF file (combined molecular structures)

## Outputs

- Combined EI MSP file (combine_ei.msp) with SMILES, InChIKey, and assigned RI
- Combined MS/MS positive-mode MSP file (combine_ms2_pos.msp)
- Combined MS/MS negative-mode MSP file (combine_ms2_neg.msp)
- Structure text file (e.g., nist_structure.txt) mapping names to SMILES

## How to apply

Before initiating the workflow, call `plan(multisession(workers = detectCores() - 1))` from the future package to allocate worker processes equal to available CPU cores minus one, reserving one core for OS overhead. Execute the workflow steps (read_lib, combine_mol2sdf, extract_structure, assign_smiles, assign_ri) sequentially in the main process; the future package transparently distributes eligible operations to workers. After all libraries are combined and written, immediately call `plan(sequential)` to disable parallel computing and free resources. The rationale: parallelizing I/O-bound structure extraction and SMILES matching (which dominate runtime) while keeping library coordination sequential avoids lock contention. Avoid parallelizing write operations; write_EI_msp and write_MS2_msp must run sequentially after all parallel tasks complete.

## Related tools

- **future** (Orchestrates parallel execution plan; allocates worker processes via multisession and coordinates distributed computation across workers) — https://cran.r-project.org/package=future
- **future.apply** (Provides parallelized functional programming primitives (fapply, flapply) for element-wise operations on lists of spectra or files) — https://cran.r-project.org/package=future.apply
- **parallel** (Native R parallelization utilities; used alongside future for detecting available CPU cores via detectCores()) — https://stat.ethz.ch/R-manual/R-devel/library/parallel/doc/parallel.pdf
- **mspcompiler** (Implements library reading, structure extraction, SMILES assignment, and RI assignment functions that benefit from parallelization; manages MSP/MOL/SDF I/O) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Consumes final combined MSP files; imposes schema constraints on SMILES field, RI field format, and RI values (capillary-only, SD ≤ 30))
- **Lib2NIST** (Pre-processing tool to convert NIST commercial library format (.L) into text MSP + MOL files suitable for mspcompiler input) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17

## Examples

```
library(future); library(mspcompiler); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib("D:/MS_libraries/NIST.MSP", type = "EI"); combine_ei <- c(nist_ei, riken_ei, mona_ei, swgdrug_ei); combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar"); plan(sequential); write_EI_msp(combine_ei, "D:/MS_libraries/combine_ei.msp")
```

## Evaluation signals

- Parallel execution completes in <50% of sequential time for >100 MB libraries on ≥4-core systems; wall-clock reduction is measurable.
- Output MSP file contains all spectra from all four source libraries without duplication; row count matches expected sum of source counts.
- All SMILES fields are populated and valid (parseable by RDKit/Rcdk); no empty or malformed SMILES strings.
- RI assignments meet MS-DIAL schema: only capillary columns retained, RI standard deviation ≤ 30 per compound, semi-polar/non-polar/polar polarity correctly assigned.
- Output file is readable by MS-DIAL software without parse errors; no corrupted MSP records or truncated fields caused by parallel writes.

## Limitations

- MOL-to-SDF conversion (combine_mol2sdf) and structure extraction (extract_structure) are not parallelized internally; they serialize all file I/O, limiting speedup to downstream operations (assign_smiles, assign_ri).
- Platform-dependent SMILES assignment: Linux/macOS must use match='inchikey', but SWGDRUG source lacks InChIKey; users must branch on library type.
- RI assignment filtering (standard deviation >30 threshold, capillary-only, median aggregation) is deterministic but may discard valid measurements; no user override provided for stringency.
- Large MOL folders (>100,000 files) are time-consuming to move, copy, or delete on common filesystems; users must plan disk layout before export from Lib2NIST.
- Memory overhead of multisession workers: each worker replicates read-only library objects; for multi-gigabyte libraries, total memory ≈ library_size × (num_workers + 1); may exceed available RAM on modest hardware.

## Evidence

- [other] Set up parallel computing with future package using available processor cores minus one.: "Set up parallel computing. Just remember to set it back once you have the library compiled by "plan(sequential)". We will include it later."
- [readme] Combine all organized EI libraries into a single object and apply RI assignment functions.: "After read in and organize all these libraries, we can now combine them into a single file, assign experimental RI retrieved from the "ri.dat" and "USER.DBU" files"
- [readme] Retain existing Kovats RI values from RIKEN and filter RI assignments by column polarity and capillary type with SD threshold.: "Providing that "capillary" GC columns are commonly used. This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single"
- [readme] The whole library compilation process is time-consuming and benefits from parallel computation.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] Reorganize SMILES from MoNA Comment field into the SMILES field using reorganize_mona function.: "This file has SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field"
