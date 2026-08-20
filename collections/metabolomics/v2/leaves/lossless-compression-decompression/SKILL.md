---
name: lossless-compression-decompression
description: Use when when you have raw mzML or mzXML mass spectrometry files with
  uncompressed numeric arrays (not pre-compressed with zlib or msnumpress) and need
  to reduce file size for archival or transfer while guaranteeing that decompressed
  data is byte-identical to the original.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - mspack
  - gzip
  - bsc
  - msconvert
  techniques:
  - ion-mobility-MS
  license_tier: open
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab636/6363791
  all_source_dois:
  - 10.1093/bioinformatics/btab636/6363791
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lossless-compression-decompression

## Summary

Compress and decompress mass spectrometry data files (mzML, mzXML) using mspack's lossless pipeline while verifying bit-identical round-trip fidelity. This skill is essential when storage or transmission bandwidth is constrained but functional integrity of spectral intensities and m/z values must be preserved exactly.

## When to use

When you have raw mzML or mzXML mass spectrometry files with uncompressed numeric arrays (not pre-compressed with zlib or msnumpress) and need to reduce file size for archival or transfer while guaranteeing that decompressed data is byte-identical to the original. Apply this skill before transmitting large cohorts of spectra or when storage quotas are tight but downstream analysis requires exact numerical recovery.

## When NOT to use

- Input mzML/mzXML files already have compressed numeric arrays (e.g., zlib or msnumpress); convert them with msconvert first.
- You need lossy compression to reduce file size further; use mspack's --mz-fixed-abs and --int-log flags instead.
- Input is mzXML with 3+ data dimensions (e.g., ion mobility in addition to m/z and intensity); mspack's mzXML implementation requires strictly increasing m/z values, which fails with mobility data.

## Inputs

- mzML mass spectrometry file with raw numeric arrays
- mzXML mass spectrometry file with raw numeric arrays

## Outputs

- Compressed binary file (.mgz or .bsc)
- Decompressed mzML or mzXML file
- Byte-for-byte comparison report or checksum validation

## How to apply

Load an mzML or mzXML mass spectrometry file containing raw (uncompressed) m/z and intensity arrays. Run mspack's lossless encoder (--mzmle for mzML or --mzxmle for mzXML) to produce a compressed binary file using either gzip (.mgz) or bsc (.bsc) backend; bsc offers better compression but is slower. Then decompress using the corresponding decoder (--mzmld or --mzxmld). Compare the decompressed output byte-by-byte with the original input file using tools like diff or SHA1 checksums (which mspack recalculates automatically). Success is confirmed when the comparison shows zero differences, indicating bit-identical recovery of all numeric and structural data.

## Related tools

- **mspack** (C++ program for lossless compression and decompression of mzML and mzXML mass spectrometry data files) — https://github.com/fhanau/mspack
- **gzip** (Compression backend for lossless encoding (.mgz file extension))
- **bsc** (Optional compression backend offering better compression than gzip but slower runtime (.bsc file extension)) — https://github.com/IlyaGrebnov/libbsc
- **msconvert** (Preprocessing tool to convert pre-compressed (zlib/msnumpress) arrays to raw format before mspack encoding)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz && ./mspack --mzmld BSA.mgz BSA-decoded.mzml && diff examples/BSA1.mzml BSA-decoded.mzml
```

## Evaluation signals

- Decompressed file is byte-identical to original (confirmed by diff or binary comparison)
- SHA1 checksum of decompressed file matches original input file
- XML structure, m/z array values, and intensity array values are numerically identical post-decompression
- Compressed file size is smaller than original by a measurable ratio (typical high compression reported for mass spectrometry data)
- Round-trip encode → decode cycle completes without errors or truncation warnings

## Limitations

- Whitespace is not preserved in decoded XML; however, this does not cause functional differences as XML is invariant to whitespace.
- Current implementation requires m/z values to be strictly increasing; fails when a third data dimension (e.g., ion mobility) is present.
- Only raw m/z and intensity arrays are supported; pre-compressed arrays must be converted with msconvert first.
- mzXML implementation does not support all features (format has been superseded by mzML) and is limited to 32-bit files without block-based I/O.
- Compiled binary requires C++11 compatible compiler (gcc/clang preferred); Windows compilation with other compilers may fail due to missing headers.

## Evidence

- [other] Preserve bit-identical fidelity requirement: "Does mspack's lossless compression pipeline preserve bit-identical fidelity when compressing and then decompressing mzML or mzXML mass spectrometry data files?"
- [other] Workflow overview from task definition: "1. Load an mzML or mzXML mass spectrometry file. 2. Apply mspack lossless compression to produce a compressed binary file. 3. Decompress the compressed file using mspack's decompression function. 4."
- [readme] mspack achieves high compression for mass spectrometry: "mspack is a C++ program for lossless and lossy mass spectrometry data compression, achieving a high compression ratio without sacrificing performance."
- [readme] Format support and API: "It includes an example implementation for mzXML and mzML as well as a format-agnostic API."
- [readme] Encoder/decoder command syntax: "mzML encode: mspack --mzmle (options) <in> <out><.mgz|.bsc>; mzml decode: mspack --mzmld <in><.mgz|.bsc> <out>"
- [readme] Whitespace caveat: "Due to the XML library we use, whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or"
- [readme] m/z ordering requirement: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility in addition to mz and intensity."
- [readme] Raw array requirement: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert so it can be used by mspack."
- [readme] Backend options: "Use the .mgz file extension to use the gzip backend and .bsc to use bsc, which will improve compression significantly, but slow down compression."
