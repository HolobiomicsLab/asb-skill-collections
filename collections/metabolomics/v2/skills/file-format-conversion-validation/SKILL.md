---
name: file-format-conversion-validation
description: Use when when you have raw mzML or mzXML mass spectrometry data files that need to be archived or transmitted with minimal storage footprint, and you must verify that the decompressed output exactly reproduces the original input at the byte level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3520
  tools:
  - mspack
  - msconvert
  - gzip
  - bsc
derived_from:
- doi: 10.1093/bioinformatics/btab636/6363791
  title: mspack
evidence_spans:
- mspack is a C++ program for lossless and lossy mass spectrometry data compression
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspack_cq
    doi: 10.1093/bioinformatics/btab636/6363791
    title: mspack
  dedup_kept_from: coll_mspack_cq
schema_version: 0.2.0
---

# file-format-conversion-validation

## Summary

Validate that mass spectrometry data files (mzML, mzXML) can be losslessly compressed and then decompressed to bit-identical fidelity using mspack. This skill ensures that format conversion and compression pipelines preserve all original data integrity.

## When to use

When you have raw mzML or mzXML mass spectrometry data files that need to be archived or transmitted with minimal storage footprint, and you must verify that the decompressed output exactly reproduces the original input at the byte level. This is critical for regulatory compliance, reproducibility, and data curation in proteomics and metabolomics workflows.

## When NOT to use

- Input mzML or mzXML files already contain pre-compressed arrays (zlib, msnumpress); convert first with msconvert.
- mzXML files that exceed 32-bit addressing or require block-based I/O; mspack mzXML support is limited and format-specific features may be lost.
- Data with ion mobility or other third-party dimensions where mz values are not strictly increasing; the current mspack implementation depends on monotonic mz ordering.

## Inputs

- mzML mass spectrometry data file (uncompressed)
- mzXML mass spectrometry data file (uncompressed)
- Raw mz and intensity arrays in XML format

## Outputs

- Compressed mass spectrometry file (.mgz or .bsc extension)
- Decompressed mzML or mzXML file
- Byte-level comparison report or checksum verification

## How to apply

Load an mzML or mzXML mass spectrometry file and apply mspack's lossless compression (using --mzmle or --mzxmle flags with the .mgz or .bsc backend) to produce a compressed binary artifact. Decompress the compressed file using mspack's corresponding decompression flag (--mzmld or --mzxmld) to recover the data. Perform a byte-by-byte comparison (e.g., SHA1 checksum or hexdump diff) between the decompressed output and the original input file to confirm bit-identical recovery. Note that whitespace normalization and SHA1 tag recalculation are expected and functionally inconsequential for XML formats. If your data contains compressed arrays (e.g., zlib or msnumpress), first convert using msconvert to extract raw mz and intensity arrays before applying mspack compression.

## Related tools

- **mspack** (Performs lossless and lossy compression/decompression of mzML and mzXML mass spectrometry data files with format-agnostic API) — https://github.com/fhanau/mspack
- **msconvert** (Converts pre-compressed arrays (zlib, msnumpress) to raw mz and intensity arrays for mspack compatibility)
- **gzip** (Backend compression engine for mspack .mgz file format) — https://ftp.gnu.org/gnu/gzip/
- **bsc** (Optional high-compression backend for mspack .bsc file format; slower but better ratio) — https://github.com/IlyaGrebnov/libbsc

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz && ./mspack --mzmld BSA.mgz BSA-decoded.mzml && diff <(sha1sum examples/BSA1.mzml) <(sha1sum BSA-decoded.mzml)
```

## Evaluation signals

- Decompressed file byte-count matches original input file byte-count
- SHA1 or MD5 checksum of decompressed output matches checksum of original input (after accounting for XML whitespace normalization)
- Hexdump or binary diff shows zero differences in functional data content (mz values, intensity values, scan metadata)
- Compressed file size is significantly smaller than original (high compression ratio achieved)
- Round-trip cycle (compress → decompress) completes without error and produces valid mzML/mzXML that parses successfully

## Limitations

- Whitespace is not preserved in decoded XML files; however, this does not cause functional differences as XML is invariant to whitespace.
- SHA1 checksum tags are recalculated during decompression, so byte-identical comparison must account for this tag regeneration.
- Current implementation depends on mz values being strictly increasing; fails or produces incorrect results if a third dimension (e.g., ion mobility) is present alongside mz and intensity.
- Only raw mz and intensity arrays are supported; pre-compressed arrays (zlib, msnumpress) must be converted using msconvert first.
- mzXML support is limited to 32-bit files and does not support block-based I/O features; mzML is the recommended format.
- Compilation on Windows using non-gcc/clang compilers may fail due to missing headers; Unix environment strongly recommended.

## Evidence

- [other] Does mspack's lossless compression pipeline preserve bit-identical fidelity when compressing and then decompressing mzML or mzXML mass spectrometry data files?: "research_question from task_001: Does mspack's lossless compression pipeline preserve bit-identical fidelity when compressing and then decompressing mzML or mzXML mass spectrometry data files?"
- [readme] mspack is a C++ program for lossless and lossy mass spectrometry data compression, achieving a high compression ratio without sacrificing performance. It includes an example implementation for mzXML and mzML as well as a format-agnostic API.: "mspack is a C++ program for lossless and lossy mass spectrometry data compression, achieving a high compression ratio without sacrificing performance. It includes an example implementation for mzXML"
- [other] 1. Load an mzML or mzXML mass spectrometry file. 2. Apply mspack lossless compression to produce a compressed binary file. 3. Decompress the compressed file using mspack's decompression function. 4. Compare the decompressed output byte-by-byte with the original input file to confirm bit-identical recovery.: "workflow from task_001: Load an mzML or mzXML mass spectrometry file. Apply mspack lossless compression to produce a compressed binary file. Decompress using mspack's decompression function. Compare"
- [readme] Due to the XML library we use, whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace. SHA1 checksum tags are recalculated when needed.: "whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace. SHA1 checksum"
- [readme] The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility in addition to mz and intensity.: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility in addition to mz and intensity."
- [readme] The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert so it can be used by mspack.: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert so it can be used by mspack."
- [readme] The mzXML implementation does not support all features as the format has been superseded by mzML. mzXML is limited to 32-bit files and does not support the block-based I/O feature.: "The mzXML implementation does not support all features as the format has been superseded by mzML. mzXML is limited to 32-bit files and does not support the block-based I/O feature."
