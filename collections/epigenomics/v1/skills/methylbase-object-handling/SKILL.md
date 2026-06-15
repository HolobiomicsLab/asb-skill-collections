---
name: methylbase-object-handling
description: Use when after reading in per-sample methylation call files with methRead() and obtaining methylRawList objects, but before calculating differential methylation or performing annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3182
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - R
  - methylKit
  - Bismark
  - MethylDackel
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- packageVersion('methylKit')
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_methylkit
    doi: 10.1186/gb-2012-13-10-r87
    title: methylkit
  dedup_kept_from: coll_methylkit
schema_version: 0.2.0
---

# methylbase-object-handling

## Summary

Create and manipulate methylBase objects in methylKit by merging methylRaw samples across common genomic bases and applying coverage filters to ensure consistent sample representation for downstream differential methylation analysis. methylBase objects are the core data structure that enable comparative and statistical analysis across replicate bisulfite sequencing experiments.

## When to use

After reading in per-sample methylation call files with methRead() and obtaining methylRawList objects, but before calculating differential methylation or performing annotation. Use this skill when you have multiple bisulfite sequencing samples and need to restrict analysis to bases covered in all samples to avoid bias from incomplete data.

## When NOT to use

- Input is already a methylBase object or other pre-processed comparative methylation object.
- Analysis requires per-sample coverage variation to be preserved (e.g., when sample-level heterogeneity is a key variable).
- Input data are from a single sample only; methylBase is designed for multi-sample comparative analysis.

## Inputs

- methylRawList object (output from methRead())
- coverage cutoff parameters (default: min 10X, max 99.9th percentile)

## Outputs

- methylBase object with merged sample data
- filtered methylRawList with coverage-corrected samples

## How to apply

First, apply filterByCoverage() to each sample in the methylRawList to remove bases with coverage below a quality threshold (default minimum 10X) and discard bases exceeding the 99.9th percentile of coverage in each sample to remove PCR bias artifacts. Then execute the unite() function to merge all filtered samples, creating a methylBase object that contains only base-pair positions covered in all samples. This unified object standardizes the sample representation and prepares data for statistical testing. The resulting methylBase object serves as input to downstream functions like calculateDiffMeth() for differential methylation testing.

## Related tools

- **methylKit** (Core R package providing methRead(), filterByCoverage(), and unite() functions for methylRawList input, coverage filtering, and methylBase object creation) — https://github.com/al2na/methylKit
- **Bismark** (Bisulfite mapping and methylation calling tool that generates methylation call files compatible with methylKit's methRead() function) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative per-base methylation metrics extraction tool from BAM/CRAM files, producing bedGraph output compatible with methylKit workflows) — https://github.com/dpryan79/MethylDackel

## Examples

```
library(methylKit); myobj <- methRead(list("s1.txt","s2.txt"),sample.id=list("s1","s2"),assembly="hg19",treatment=c(0,1),context="CpG"); filtered <- filterByCoverage(myobj, lo.count=10, lo.perc=NULL, hi.count=NULL, hi.perc=99.9); meth <- unite(filtered,destrand=FALSE)
```

## Evaluation signals

- methylBase object is successfully created with class 'methylBase' (verifiable via class() function in R)
- Number of bases in the unified methylBase object equals the count of positions with coverage in all samples (intersection of covered bases)
- All samples have identical row counts (base-pair positions) after unite(), confirming complete merging without dropout
- Coverage statistics after filterByCoverage() show minimum ≥10X and maximum ≤99.9th percentile in all samples, confirming quality filtering
- methylBase object can be successfully passed as input to calculateDiffMeth() without errors, confirming correct object structure

## Limitations

- Default minimum coverage of 10X per base may be insufficient for low-depth or highly variable experiments; users should evaluate their sequencing depth distribution before applying this threshold.
- Requiring coverage in all samples can dramatically reduce the number of analyzable bases when sample coverage is uneven; trade-off between statistical power and completeness must be considered.
- methylBase filtering to common bases assumes that missing coverage represents true absence rather than technical dropout; samples with systematic coverage gaps may violate this assumption.
- The unite() function operates only on base-pair resolution data; regional or tiling window analysis requires separate workflows not addressed by methylBase object creation alone.

## Evidence

- [intro] In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
- [intro] The code below filters a methylRawList and discards bases that have coverage below 10X and also discards the bases that have more than 99.9th percentile of coverage in each sample: "The code below filters a methylRawList and discards bases that have coverage below 10X and also discards the bases that have more than 99.9th percentile of coverage in each sample"
- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object: "We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object"
- [intro] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing"
