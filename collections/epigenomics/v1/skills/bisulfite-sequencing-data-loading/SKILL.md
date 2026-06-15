---
name: bisulfite-sequencing-data-loading
description: Use when you have raw methylation call files from Bismark, MethylDackel, or similar bisulfite alignment tools (bedGraph, cytosine report, or tabix-indexed formats) and need to import them into R as methylRaw or methylRawListDB objects for downstream differential methylation analysis, quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3182
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

# bisulfite-sequencing-data-loading

## Summary

Load and parse DNA methylation call files from bisulfite sequencing experiments (RRBS, WGBS, target-capture) into in-memory or disk-backed R objects, supporting both standard text formats and tabix-indexed bgzipped storage for memory-efficient batch processing.

## When to use

You have raw methylation call files from Bismark, MethylDackel, or similar bisulfite alignment tools (bedGraph, cytosine report, or tabix-indexed formats) and need to import them into R as methylRaw or methylRawListDB objects for downstream differential methylation analysis, quality filtering, or annotation.

## When NOT to use

- Input files are already formatted as a unified methylBase object or methylDiff object (skip directly to filtering or differential methylation analysis)
- You are working with non-bisulfite methylation data (e.g., whole-genome or targeted 5hmC without proper bisulfite conversion controls)
- Raw sequencing reads (FASTQ) are provided instead of methylation call files; align with Bismark or MethylDackel first

## Inputs

- Methylation call files (cytosineReport, bedGraph, or tabix-indexed bgzipped format from Bismark/MethylDackel)
- Sample metadata (treatment/condition assignment)
- Assembly/genome identifier (e.g., 'hg19', 'mm9')

## Outputs

- methylRaw object (single sample, in-memory)
- methylRawList object (multiple samples, in-memory)
- methylRawListDB object (multiple samples, disk-backed tabix storage)

## How to apply

Use the methRead() function from methylKit to read methylation call files, specifying the file format (e.g., 'cytosineReport', 'bedGraph') and assembly. For memory-constrained analyses with large sample cohorts, set dbtype='tabix' to create a methylRawListDB object backed by bgzipped tabix-indexed files on disk rather than in-memory storage. By default, methRead() applies a minimum coverage threshold of 10 reads per base to ensure quality methylation percentage estimates. Verify the resulting methylRaw or methylRawListDB object structure and confirm that the dbpath slot references valid bgzipped tabix file paths when using database-mode storage. The function automatically handles CpG, CHG, and CHH context methylation calls depending on your input file's content and the bisulfite sequencing protocol (RRBS vs. WGBS).

## Related tools

- **methylKit** (R package providing methRead() function to parse methylation call files and create methylRaw/methylRawListDB objects) — https://github.com/al2na/methylKit
- **Bismark** (Bisulfite-treated read aligner and methylation caller; produces cytosineReport or bedGraph output files consumed by methRead()) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative methylation extractor from BAM alignments; outputs bedGraph-compatible methylation metrics) — https://github.com/dpryan79/MethylDackel

## Examples

```
methRead(location=c('sample1.CpG_report.txt','sample2.CpG_report.txt'),sample.id=c('s1','s2'),assembly='hg19',context='CpG',dbtype='tabix')
```

## Evaluation signals

- Returned methylRaw or methylRawListDB object is valid and contains non-zero number of CpG sites with methylation percentages (0–100 range)
- For in-memory objects: data is fully loaded in R session; for tabix-backed objects: dbpath slot correctly references bgzipped files and file paths are readable
- Coverage distribution meets the minimum threshold of 10 reads per base by default; inspect coverage statistics via coverage() function to confirm filtering was applied
- methylRawList or methylRawListDB contains the expected number of samples matching the input file list
- Methylation percentages and read counts are consistent with input file values; spot-check a random CpG site across files

## Limitations

- By default requires minimum coverage of 10 reads per base; low-coverage experiments may lose data; can be disabled but risks inflated noise
- Supports standard bisulfite sequencing contexts (CpG, CHG, CHH); non-standard or damaged methylation calls require pre-filtering of input files
- Tabix-indexed storage (dbtype='tabix') requires files to be bgzipped and properly indexed; malformed or unindexed files will cause object creation to fail
- methRead() expects sorted, tab-delimited input with specific column order; files from non-standard callers or with custom column orders may fail to parse correctly

## Evidence

- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object: "We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object"
- [intro] By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage: "By default methRead requires a minimum coverage of 10 reads per base to ensure good quality of the data and a high confidence methylation percentage"
- [other] The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk. The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage.: "The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk. The dbpath slot of each methylRaw object"
- [readme] methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but also target-capture methods such as Agilent SureSelect methyl-seq.: "methylKit is an R package for DNA methylation analysis and annotation from high-throughput bisulfite sequencing. The package is designed to deal with sequencing data from RRBS and its variants, but"
- [readme] MethylDackel will process a coordinate-sorted and indexed BAM or CRAM file containing some form of BS-seq alignments and extract per-base methylation metrics from them.: "MethylDackel will process a coordinate-sorted and indexed BAM or CRAM file containing some form of BS-seq alignments and extract per-base methylation metrics from them"
