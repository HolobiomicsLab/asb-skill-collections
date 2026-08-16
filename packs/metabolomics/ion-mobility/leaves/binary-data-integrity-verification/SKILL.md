---
name: binary-data-integrity-verification
description: Use when after implementing a lossless compression–decompression cycle on mzML or mzXML mass spectrometry files, or when validating that a lossy compression pipeline meets acceptable error thresholds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - mspack
  - gzip
  - bsc (libbsc)
  - msconvert
  techniques:
  - ion-mobility-MS
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

# binary-data-integrity-verification

## Summary

Verify that lossy or lossless compression pipelines preserve data fidelity by performing byte-by-byte or functional comparison of input and decompressed outputs. This skill is essential for validating mass spectrometry data compression workflows where bit-identical recovery or acceptable information loss must be guaranteed.

## When to use

Apply this skill after implementing a lossless compression–decompression cycle on mzML or mzXML mass spectrometry files, or when validating that a lossy compression pipeline meets acceptable error thresholds. Use it whenever you need to confirm that no unintended data corruption has occurred during compression serialization and deserialization.

## When NOT to use

- Input arrays are already compressed with zlib or msnumpress — convert using msconvert first before applying mspack compression
- mz values are not monotonically increasing or a third dimension (e.g. ion mobility) is present — mspack implementation depends on sorted mz values
- Using mzXML with 64-bit data or block-based I/O features — mzXML support is limited to 32-bit files without block-based I/O

## Inputs

- mzML mass spectrometry data file (raw, uncompressed)
- mzXML mass spectrometry data file (raw, uncompressed)
- compressed binary file (.mgz or .bsc)

## Outputs

- decompressed mzML or mzXML file
- byte-comparison report (match/mismatch)
- functional equivalence validation report

## How to apply

Load the original mzML or mzXML mass spectrometry file. Apply mspack lossless compression using the appropriate encoder (--mzmle or --mzxmle) to produce a compressed binary file with .mgz or .bsc extension. Decompress the compressed file using the corresponding decoder (--mzmld or --mzxmld) to recover a decompressed output file. Perform byte-by-byte comparison between the decompressed output and the original input to confirm bit-identical recovery. Note that for lossless compression, the XML structure (including whitespace normalization and SHA1 recalculation) will differ syntactically but remain functionally equivalent; validate that raw mz and intensity arrays match exactly.

## Related tools

- **mspack** (Performs lossless and lossy compression/decompression of mzML and mzXML files; provides the codec pipeline being validated) — https://github.com/fhanau/mspack
- **gzip** (Compression backend for .mgz format output during mspack encoding)
- **bsc (libbsc)** (Alternative compression backend for .bsc format output, provides improved compression ratio at slower speed) — https://github.com/IlyaGrebnov/libbsc
- **msconvert** (Pre-processing tool to convert zlib or msnumpress-compressed arrays to raw format before mspack compression)

## Examples

```
./mspack --mzmle examples/BSA1.mzml BSA.mgz && ./mspack --mzmld BSA.mgz BSA-decoded.mzml && diff <(xxd examples/BSA1.mzml) <(xxd BSA-decoded.mzml)
```

## Evaluation signals

- Byte-by-byte identity match between decompressed output and original input file (for lossless mode)
- SHA1 checksums in XML headers match or are correctly recalculated post-decompression
- Decompressed mz and intensity array values are identical to originals (element-by-element comparison)
- XML parse succeeds on decompressed output and all mass spectrometry-relevant elements (spectrum, precursor, product ion lists) are present and structurally valid
- File size reduction ratio is within expected bounds for the chosen backend (gzip vs. bsc) and compression mode (lossless vs. lossy with --mz-fixed-abs or --int-log)

## Limitations

- Whitespace is not preserved in decoded XML files due to tinyxml2 library behavior, though this does not cause functional difference for XML-invariant data
- Implementation depends on mz values being monotonically increasing; presence of a third data dimension (e.g. ion mobility) may violate this assumption
- Can only process raw mz and intensity arrays; pre-compressed arrays (zlib, msnumpress) must be converted to raw format using msconvert beforehand
- mzXML support is limited to 32-bit files and does not support block-based I/O features; mzML is the preferred format

## Evidence

- [readme] mspack is a C++ program for lossless and lossy mass spectrometry data compression, achieving a high compression ratio without sacrificing performance.: "mspack is a C++ program for lossless and lossy mass spectrometry data compression, achieving a high compression ratio without sacrificing performance"
- [other] Load an mzML or mzXML mass spectrometry file. Apply mspack lossless compression to produce a compressed binary file. Decompress the compressed file using mspack's decompression function. Compare the decompressed output byte-by-byte with the original input file to confirm bit-identical recovery.: "Compare the decompressed output byte-by-byte with the original input file to confirm bit-identical recovery"
- [other] Does mspack's lossless compression pipeline preserve bit-identical fidelity when compressing and then decompressing mzML or mzXML mass spectrometry data files?: "Does mspack's lossless compression pipeline preserve bit-identical fidelity when compressing and then decompressing mzML or mzXML mass spectrometry data files?"
- [readme] Due to the XML library we use, whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace. SHA1 checksum tags are recalculated when needed.: "whitespace is not preserved in the decoded file, although this does not cause a functional difference for the decoded file as XML is invariant to the addition or removal of whitespace. SHA1 checksum"
- [readme] The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility in addition to mz and intensity.: "The current implementation depends on the mz values being increasing. This is sometimes not the case if a third data point is present, i.e. ion mobility in addition to mz and intensity"
- [readme] The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert so it can be used by mspack.: "The implementation can only use raw mz and intensity arrays. If the arrays are compressed with e.g. zlib or msnumpress, the file can be converted using msconvert so it can be used by mspack"
