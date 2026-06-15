---
name: tabix-index-validation-and-inspection
description: Use when after creating a methylRawListDB object via methRead() with dbtype='tabix', or when loading pre-existing tabix-backed methylation files, to verify that bgzipped files are correctly indexed and contain required methylKit metadata headers (≥v1.13.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0654
  tools:
  - R
  - methylKit
  - tabix
  - htslib/bgzip
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

# tabix-index-validation-and-inspection

## Summary

Validate and inspect tabix-indexed bgzipped methylation data files to confirm correct indexing, file integrity, and methylKit metadata presence. This skill ensures that disk-backed methylRawListDB objects reference valid external tabix files with proper headers before downstream analysis.

## When to use

After creating a methylRawListDB object via methRead() with dbtype='tabix', or when loading pre-existing tabix-backed methylation files, to verify that bgzipped files are correctly indexed and contain required methylKit metadata headers (≥v1.13.1) before proceeding with differential methylation analysis or sample merging.

## When NOT to use

- Input data is already loaded in memory as a standard methylRawList (non-database-backed) object
- Tabix files are not available or have been deleted after initial loading
- methylKit version is < 1.13.1 and does not support tabix-backed database mode

## Inputs

- methylRawListDB object created with dbtype='tabix'
- bgzipped tabix-indexed methylation files (.gz with .tbi index)
- methylKit metadata headers within tabix files

## Outputs

- Validated methylRawListDB object with confirmed dbpath references
- Inspection report of tabix file headers and metadata
- File integrity assessment (presence of index, header validity, version check)

## How to apply

Verify that the methylRawListDB object's dbpath slot in each constituent methylRaw object references valid file paths to bgzipped tabix files. Inspect the tabix file headers using appropriate tools (e.g., zcat or tabix command-line utilities) to confirm presence of methylKit-specific metadata and version information. Cross-check that file timestamps and index (.tbi) presence match expected standards for database-mode storage. Validate object structure by examining the methylRawListDB list composition and ensuring coverage statistics align with input file contents. Compare object integrity metrics (total bases, sample counts) against the raw tabix file statistics to confirm lossless loading from external storage.

## Related tools

- **methylKit** (R package that creates and manages methylRawListDB objects backed by tabix-indexed files; methRead() function with dbtype='tabix' parameter initiates database-mode storage) — https://github.com/al2na/methylKit
- **tabix** (Command-line utility for creating and querying tabix-indexed bgzipped files; used to inspect file headers and verify index integrity)
- **htslib/bgzip** (Compression and indexing library underlying tabix functionality; handles bgzipped file format and random-access seeking)

## Examples

```
# In R: Verify methylRawListDB object structure after loading methylRaw_list <- methRead(file_list, sample.id=sample_ids, assembly='hg19', dbtype='tabix'); lapply(methylRaw_list, function(x) { cat('dbpath:', x@dbpath, '\n'); system(paste('tabix -H', x@dbpath)) })
```

## Evaluation signals

- dbpath slot of each methylRaw object within methylRawListDB references valid, accessible file paths to .gz files with corresponding .tbi index files present
- Tabix file headers contain methylKit-specific metadata markers and version string ≥ 1.13.1
- Sample count, total base coverage, and methylation statistics extracted from tabix headers match those in the loaded methylRawListDB object
- No errors or warnings when querying tabix file structure with tabix -H or equivalent inspection command
- File modification timestamps and index freshness indicate consistent write-once storage without subsequent modification

## Limitations

- Validation requires tabix files to remain on disk at their original paths; moving or deleting indexed files after loading will invalidate the methylRawListDB object
- Header inspection depends on correct bgzip compression and tabix indexing at file creation time; pre-existing malformed files cannot be repaired by validation alone
- methylKit versions < 1.13.1 do not support tabix-backed database mode, making this skill inapplicable to legacy workflows
- Validation of tabix integrity is read-only and does not confirm correctness of methylation values themselves, only file structure and metadata

## Evidence

- [other] The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk.: "The methRead() function with dbtype='tabix' parameter creates a methylRawListDB object that stores methylation data in bgzipped tabix files indexed on disk."
- [other] The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage.: "The dbpath slot of each methylRaw object within the list is populated with the file path to the tabix file, enabling data retrieval from the external file rather than memory storage."
- [other] Verify that the resulting methylRawListDB object's dbpath slot references valid bgzipped tabix file paths.: "Verify that the resulting methylRawListDB object's dbpath slot references valid bgzipped tabix file paths."
- [other] Inspect the tabix file headers to confirm presence of methylKit metadata and version information (≥ 1.13.1).: "Inspect the tabix file headers to confirm presence of methylKit metadata and version information (≥ 1.13.1)."
- [other] Validate that the object structure and file integrity match expected methylKit standards for database-mode storage.: "Validate that the object structure and file integrity match expected methylKit standards for database-mode storage."
