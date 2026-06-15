---
name: methylkit-database-mode-configuration
description: Use when when analyzing DNA methylation data from bisulfite sequencing (RRBS, target-capture, or whole-genome) and the dataset is too large to fit comfortably in memory, or when you need to process multiple large samples sequentially without reloading data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3196
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
  tools:
  - methylKit
  - R
  - Bismark
  - MethylDackel
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- 'title: "methylKit: User Guide v`r packageVersion(''methylKit'')`"'
- 'title: "methylKit: User Guide'
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

# methylkit-database-mode-configuration

## Summary

Configure methylKit to store methylation data in tabix-indexed bgzipped files on disk rather than in memory, enabling scalable analysis of large bisulfite sequencing datasets. This skill uses the methRead() function with dbtype='tabix' parameter to create memory-efficient methylRawListDB objects backed by external indexed files.

## When to use

When analyzing DNA methylation data from bisulfite sequencing (RRBS, target-capture, or whole-genome) and the dataset is too large to fit comfortably in memory, or when you need to process multiple large samples sequentially without reloading data. Specifically, use this skill when you have CpG methylation call files and want to avoid the memory overhead of storing all methylation data in RAM while preserving fast random access to per-base methylation information.

## When NOT to use

- Input data is already loaded as an in-memory methylRawList or methylBase object — direct conversion or in-memory analysis is more efficient.
- Dataset is small enough to fit comfortably in RAM and analysis speed is critical over memory efficiency.
- Bismark or methylation call files are not in a format recognized by methRead() or lack required metadata headers for tabix indexing.

## Inputs

- CpG methylation call files (typically in Bismark or similar format)
- dbtype parameter specification ('tabix')
- bgzipped tabix-indexed methylation data files on disk

## Outputs

- methylRawListDB object with disk-backed storage
- methylRaw objects with populated dbpath slots referencing external tabix files
- Validated tabix file index structures with methylKit metadata headers

## How to apply

Load CpG methylation call files using the methRead() function with the dbtype='tabix' parameter to create a methylRawListDB object where each methylRaw object maintains a dbpath slot referencing bgzipped tabix-indexed files on disk. The tabix files must contain methylKit metadata headers (version ≥ 1.13.1) and be properly indexed. Verify that the resulting object's structure matches methylKit database-mode standards by inspecting the dbpath slot to confirm valid file paths and examining tabix file headers for metadata integrity. This configuration enables data retrieval from external files rather than memory storage, making it suitable for large-scale methylation studies where coverage statistics and methylation percentages are queried selectively rather than loaded entirely into RAM.

## Related tools

- **methylKit** (Primary R package providing methRead() function with dbtype='tabix' parameter and methylRawListDB class for disk-backed methylation data storage) — https://github.com/al2na/methylKit
- **Bismark** (Upstream bisulfite mapping and methylation calling tool that produces alignment files and methylation call output readable by methylKit's methRead()) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative tool for extracting per-base methylation metrics from BAM/CRAM files in bedGraph format compatible with methylKit input) — https://github.com/dpryan79/MethylDackel

## Examples

```
methylRawListDB_obj <- methRead(list(file1='sample1.txt', file2='sample2.txt'), sample.id=list('s1','s2'), assembly='hg19', dbtype='tabix')
```

## Evaluation signals

- The returned methylRawListDB object is instantiated without errors and contains non-null methylRaw objects in the list.
- Each methylRaw object's dbpath slot contains a valid, non-empty file path string pointing to an existing bgzipped tabix file.
- Tabix file headers can be read and contain methylKit metadata (version information ≥ 1.13.1) confirming proper indexing.
- File integrity validation passes: tabix files are readable, compressed, and indexed with valid .tbi index files present.
- Spot checks of methylation data retrieval (e.g., calling getCoverage() or getMethylationStats() on the database-backed object) return expected data types and ranges without triggering memory errors.

## Limitations

- Tabix file creation and indexing overhead occurs upfront; for small datasets, in-memory methylRawList objects may be faster to instantiate.
- Random access to methylation data is efficient, but sequential scans across large genomic ranges may incur disk I/O latency compared to fully in-memory objects.
- Metadata headers in tabix files must conform to methylKit standards (version ≥ 1.13.1); older or manually created bgzipped files may lack required headers and fail validation.
- Database-mode objects are read-only with respect to the underlying tabix files; modifications require writing new files rather than in-place updates.

## Evidence

- [other] The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk.: "The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk"
- [other] The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage.: "The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage"
- [other] Verify that the resulting methylRawListDB object's dbpath slot references valid bgzipped tabix file paths and inspect tabix file headers to confirm presence of methylKit metadata and version information (≥ 1.13.1).: "Verify that the resulting methylRawListDB object's dbpath slot references valid bgzipped tabix file paths. Inspect the tabix file headers to confirm presence of methylKit metadata and version"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing, designed to deal with sequencing data from RRBS and its variants, but also target-capture methods.: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage.: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
