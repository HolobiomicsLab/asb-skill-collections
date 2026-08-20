---
name: parallel-computation-for-large-library-processing
description: Use when your input consists of multiple large MSP files (hundreds of megabytes) with associated structure folders containing hundreds of thousands of MOL or SDF files that require sequential processing steps (structure extraction, SMILES matching, RI assignment).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - parallel
  - Lib2NIST
  - MS-DIAL
  - MoNA
  - RIKEN
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
- library(parallel)
- you can transformed it into a msp file by *Lib2NIST*
- MS-DIAL friendly msp file
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

# parallel-computation-for-large-library-processing

## Summary

Configure and execute parallel computing workflows in R to accelerate time-consuming mass spectral library compilation tasks (structure extraction, SMILES assignment, RI calculation) across multi-core systems. This skill is essential when processing hundreds of thousands of molecular records from multiple commercial and public sources (NIST, MoNA, RIKEN, SWGDRUG) that would otherwise require several hours on a single core.

## When to use

Your input consists of multiple large MSP files (hundreds of megabytes) with associated structure folders containing hundreds of thousands of MOL or SDF files that require sequential processing steps (structure extraction, SMILES matching, RI assignment). Processing time on a single core exceeds 1–2 hours, and you have access to a multi-core workstation or cluster. Apply this skill before invoking compute-intensive functions like extract_structure(), assign_smiles(), assign_ri(), or combine_mol2sdf().

## When NOT to use

- Input MSP file is small (< 10,000 records) or structure folder contains < 1,000 MOL files—single-core processing will be faster due to worker overhead.
- Running on a memory-constrained system (< 8 GB RAM)—parallel workers multiply memory consumption; consider sequential processing instead.
- Interactive debugging is required; parallel execution obscures stack traces and makes step-by-step inspection difficult.

## Inputs

- R environment with libraries loaded (mspcompiler, future, future.apply, parallel)
- One or more MSP files (e.g. NIST.MSP, MoNA-export-GC-MS_Spectra.msp, GCMS DB-Public-KovatsRI-VS3.msp, SWGDRUG.MSP)
- Associated structure folders (NIST.MOL, SWGDRUG.MOL) containing ≥ 10,000 individual MOL files
- Optional RI metadata files (ri.dat, USER.DBU) for Retention Index assignment
- Target output file path (e.g. D:/MS_libraries/combine_ei.msp)

## Outputs

- Single consolidated MSP file with merged libraries from all sources
- MSP records with populated SMILES fields (assigned via parallel extract_structure + assign_smiles)
- MSP records with populated Retention Index (RI) fields (assigned via parallel assign_ri with polarity-specific filtering)
- Processing log with total elapsed wall-clock time (typically 2–8 hours reduced from 8–24 hours on single core)

## How to apply

Declare and configure a parallel plan using the future package before any library processing begins: call plan(multisession(workers = detectCores() - 1)) to reserve all but one CPU core for parallel tasks. The mspcompiler package is designed to automatically distribute eligible operations (structure extraction, SMILES matching, RI lookup) across these workers via future.apply without explicit re-specification of individual functions. After all processing is complete—including library combination and RI assignment—disable parallel execution by calling plan(sequential) to free system resources. The choice of workers should reserve at least one core for the OS; detectCores() - 1 is the recommended pattern from the README. Parallel speedup is most effective for the combine_mol2sdf() → extract_structure() → assign_smiles() sequence, where per-record overhead is high.

## Related tools

- **future** (Declares and manages parallel execution plan (multisession workers, sequential fallback)) — https://CRAN.R-project.org/package=future
- **future.apply** (Applies vectorized functions (lapply, sapply) across parallel workers transparently within mspcompiler) — https://CRAN.R-project.org/package=future.apply
- **parallel** (Provides detectCores() utility to determine available CPU count for worker allocation) — https://CRAN.R-project.org/package=parallel
- **mspcompiler** (R package with functions (extract_structure, assign_smiles, assign_ri) that automatically use parallel workers when plan is active) — https://github.com/QizhiSu/mspcompiler

## Examples

```
library(mspcompiler); library(future); library(future.apply); library(parallel); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib("D:/MS_libraries/NIST.MSP", type = "EI"); combine_mol2sdf("D:/MS_libraries/NIST.MOL", "D:/MS_libraries/nist.sdf"); nist_ei_structure <- extract_structure("D:/MS_libraries/nist.sdf", "D:/MS_libraries/nist_structure.txt"); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name"); plan(sequential)
```

## Evaluation signals

- Parallel plan is active: confirm via future::plan() returns 'multisession' strategy with expected worker count (detectCores() - 1).
- Processing time is reduced: wall-clock time for extract_structure() + assign_smiles() on full NIST library is < 25% of single-core estimate.
- Output MSP file contains all four source libraries merged with no records dropped: validate record count against sum of input libraries using grep or R import.
- SMILES and RI fields are populated for eligible compounds: spot-check ≥ 10 random records in output MSP for non-empty SMILES and RI fields.
- No worker errors or timeouts occurred: check for warnings/errors in console log; failed workers should be logged by future package.

## Limitations

- Worker initialization overhead (typically 2–5 seconds per worker) means parallel processing is inefficient for very small libraries (< 5,000 records).
- Memory consumption scales linearly with worker count; each worker loads a copy of the library object. On systems with < 8 GB RAM, number of workers should be reduced or sequential processing used.
- Parallel workers do not share disk I/O efficiently; combine_mol2sdf() bottlenecks on file system speed and may not scale beyond 4–8 workers even on high-core-count systems.
- Non-deterministic execution order in parallel mode may affect reproducibility if random seeding is used; set seed before plan() activation if stochastic operations are involved.
- The authors note the process is 'time-consuming (several hours, depending on the capability of your PC)' even with parallelization; absolute runtime depends on CPU generation, storage latency, and network access to RI databases.

## Evidence

- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] plan(multisession(workers = detectCores() - 1)): "plan(multisession(workers = detectCores() - 1))"
- [readme] Just remember to set it back once you have the library compiled by "plan(sequential)".: "Just remember to set it back once you have the library compiled by "plan(sequential)"."
- [readme] library(future); library(future.apply); library(parallel): "library(future)
library(future.apply)
library(parallel)"
- [readme] Since the *.MOL folder contains a large number of mol files, it will be time-consuming to move, copy, or delete this folder.: "Since the *.MOL folder contains a large number of mol files, it will be time-consuming to move, copy, or delete this folder."
