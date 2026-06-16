# Evaluation Strategy

## Direct Checks

- Verify file exists: locate igzip format specification document or hex dump reference in repository (github:pymzML__pymzML)
- Verify file exists: BSA1.mzML.gz test dataset is accessible at tests/data/BSA1.mzML.gz
- Script runs: Python implementation of igzip binary header encoder accepts ID bytes, VERSION, IDXLEN, OFFSETLEN, and index-to-offset pairs as parameters and returns bytes object without error
- Output matches reference: byte-for-byte comparison of generated igzip header structure against documented Moby Dick example hex dump (if hex dump is provided in article or SI)
- File format is: verify generated output is valid gzip file with igzip extension header (magic bytes 1f 8b, extra field flag set, igzip subfield present)

## Expert Review

- Verify igzip header structure correctness: expert review that ID bytes, VERSION, IDXLEN, OFFSETLEN fields are encoded in correct byte order (little-endian vs big-endian) per igzip specification
- Verify index-to-offset pair encoding: expert review that offset values are correctly encoded with length specified by OFFSETLEN field
- Verify zero-terminator placement: expert review that header concludes with correct null-terminator byte sequence per igzip format specification
