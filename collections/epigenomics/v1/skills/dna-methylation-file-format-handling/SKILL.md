---
name: dna-methylation-file-format-handling
description: Use when you have CpG methylation call files (from Bismark or MethylDackel) and need to load them into R for differential methylation analysis, but anticipate memory constraints or want to avoid loading the entire dataset into memory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3198
  edam_topics:
  - http://edamontology.org/topic_3674
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

# DNA methylation file format handling

## Summary

Configure methylKit's dbtype parameter and tabix-backed storage to load bisulfite sequencing methylation calls into memory-efficient methylRawListDB objects backed by bgzipped indexed files on disk. This skill enables scalable handling of large methylation datasets without loading all data into RAM.

## When to use

You have CpG methylation call files (from Bismark or MethylDackel) and need to load them into R for differential methylation analysis, but anticipate memory constraints or want to avoid loading the entire dataset into memory. Use this skill when dataset size makes in-memory storage impractical or when you need fast random access to specific genomic regions without decompressing the entire file.

## When NOT to use

- Input files are already in HDF5 or other non-tabix disk-backed format (use appropriate dbtype instead)
- Your workflow requires in-memory operations only and dataset size is manageable in RAM (use default in-memory loading without dbtype parameter)
- Methylation calls are not from bisulfite sequencing or lack standard genomic coordinate format (e.g., from base-calling algorithms with non-standard output)

## Inputs

- CpG methylation call files (bedGraph, cov, or Bismark coverage format)
- Sample metadata (group/phenotype assignments for methylation samples)
- Reference genome or annotation (optional, for downstream analysis)

## Outputs

- methylRawListDB object with dbpath slots referencing bgzipped tabix files
- Disk-backed methylRaw objects within the list, each pointing to a tabix-indexed file
- Validated tabix file structure with methylKit metadata headers

## How to apply

Call the methRead() function with the dbtype='tabix' parameter to create a methylRawListDB object that stores methylation data in bgzipped tabix-indexed files on disk rather than in memory. The resulting methylRawListDB object will have its dbpath slot populated with file paths to the bgzipped tabix files, enabling retrieval from external files. Verify that the tabix file headers contain methylKit metadata and version information (≥ 1.13.1), and inspect the object structure to confirm the dbpath slots reference valid bgzipped tabix file paths. By default, methRead() applies a minimum coverage threshold of 10 reads per base to ensure data quality, which can be adjusted as needed. This configuration allows downstream operations like unite(), calculateDiffMeth(), and getMethylDiff() to work on the database-backed object while accessing data from disk on demand.

## Related tools

- **methylKit** (R package that provides methRead() function with dbtype parameter for loading methylation calls into tabix-backed methylRawListDB objects; also provides unite(), calculateDiffMeth(), and downstream analysis functions) — https://github.com/al2na/methylKit
- **Bismark** (Generates bisulfite-sequencing methylation call files in coverage format compatible with methRead() input) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative tool for extracting per-base methylation metrics from BAM files, producing bedGraph output compatible with methRead() input) — https://github.com/dpryan79/MethylDackel

## Examples

```
methRead(location='samples.txt', dbtype='tabix', sample.id=list('s1','s2','s3'), assembly='hg38', treatment=c(0,0,1), context='CpG')
```

## Evaluation signals

- The resulting methylRawListDB object's class attribute should be 'methylRawListDB' and contain multiple methylRaw objects
- Each methylRaw object within the list should have a non-empty dbpath slot containing a file path to a bgzipped (.gz) file
- Tabix index files (.tbi) should exist alongside each bgzipped file and be readable by the system
- The tabix file header should contain methylKit metadata including version information matching or exceeding v1.13.1
- The object should allow downstream methylKit operations (unite(), calculateDiffMeth()) to execute without loading the entire file into memory

## Limitations

- Requires bgzip and tabix indexing infrastructure; not all methylation formats are automatically compatible without preprocessing
- Tabix-backed storage adds disk I/O overhead compared to in-memory storage, which may slow interactive exploration for small datasets
- The minimum coverage threshold default of 10 reads per base may be too stringent or too lenient depending on sequencing depth and tissue heterogeneity; users must validate this threshold for their specific biological context
- Metadata header validation requires methylKit ≥ v1.13.1; earlier versions may not properly support database-mode operations

## Evidence

- [other] The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk.: "The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk."
- [other] The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage.: "The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage."
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object: "We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but also target-capture methods such as Agilent SureSelect methyl-seq.: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but"
