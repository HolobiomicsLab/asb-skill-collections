---
name: rust-library-compilation-and-testing
description: Use when when you have access to Rust source code in a repository with a Cargo manifest (Cargo.toml) and need to verify that a library's read and write APIs produce byte-equivalent or structurally equivalent output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Rust
  - Cargo
  - mzPeak Rust library
derived_from:
- doi: 10.1021/acs.jproteome.5c00435
  title: mzpeak
evidence_spans:
- The primary work shown here is written in Rust at the repository root
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzpeak_cq
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.5c00435
  all_source_dois:
  - 10.1021/acs.jproteome.5c00435
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Rust Library Compilation and Testing

## Summary

Compile a Rust library from source using Cargo and validate its round-trip read/write functionality by loading, serializing, and comparing data structures. This skill is essential for verifying that a Rust-based file format implementation (e.g., mzPeak reader/writer) correctly preserves data integrity across serialization cycles.

## When to use

When you have access to Rust source code in a repository with a Cargo manifest (Cargo.toml) and need to verify that a library's read and write APIs produce byte-equivalent or structurally equivalent output. Specifically, apply this when the research question is whether a library successfully implements bidirectional serialization (e.g., can you read a mzPeak file, modify it in memory, write it back, and recover the original data?). This is the appropriate validation step after obtaining a prototype implementation.

## When NOT to use

- The source code does not include a Cargo.toml or the repository structure is incomplete; use a pre-built binary or consult the maintainer instead.
- You only need to read the file format and do not require write validation; use the read-only Python or R implementations instead.
- The library is known to be work-in-progress with no stability guarantees and you require production-grade assurance; defer until a stable release is published.

## Inputs

- Rust source repository with Cargo.toml manifest
- Sample input file in the target format (e.g., mzPeak file)
- Rust toolchain (cargo, rustc)

## Outputs

- Compiled Rust library binary or rlib artifact
- Round-tripped output file in the same format
- Validation report (structural/data equivalence assessment)

## How to apply

Clone or obtain the repository containing the Rust library at its root directory. Ensure Rust and Cargo are installed. Execute `cargo build` to compile the library, targeting the specific read/write API modules documented in the repository. Load a sample input file (e.g., a mzPeak file) using the library's public read API, deserializing it into an in-memory data structure. Immediately serialize that data structure back to disk using the library's write API. Compare the original and round-tripped files using structural equivalence (schema match, field counts, data types) and optionally byte-level comparison if the format is deterministic. Evaluate success by checking that no data loss occurred and that the schemas remain intact across the cycle. If the format permits lossless compression or null-marking (as in mzPeak), verify that reconstructed values fall within acceptable numerical tolerance (e.g., matching peak apex or centroid to within machine precision).

## Related tools

- **Cargo** (Rust package manager and build system used to compile the mzPeak library from source) — https://doc.rust-lang.org/cargo/
- **Rust** (Programming language in which the mzPeak library is written; required for compilation and API access) — https://www.rust-lang.org/
- **mzPeak Rust library** (The target library providing read/write APIs for mzPeak files; located at the root of the HUPO-PSI/mzPeak repository) — https://github.com/HUPO-PSI/mzPeak

## Examples

```
cd /path/to/HUPO-PSI/mzPeak && cargo build --release && cargo test --lib read_write -- --nocapture
```

## Evaluation signals

- Cargo build completes without errors and produces a valid library artifact (rlib or .so)
- The round-tripped file can be parsed without errors using the same read API that loaded the original
- Structural equivalence check: field names, types, array lengths, and nested schema hierarchy match between original and round-tripped files
- Data equivalence: numeric values (m/z, intensity) are identical or fall within documented numerical tolerance (e.g., machine epsilon for floating-point, or reconstruction error bounds for null-marked m/z values)
- For profile data with zero-run stripping or null marking: peak apexes and centroids computed from the reconstructed signal are bitwise identical or differ by less than 1 ppm

## Limitations

- The mzPeak format is currently work-in-progress with no stability guaranteed, so the compiled library API and file format may change without notice between builds.
- Round-trip testing assumes deterministic serialization; if the library applies lossy compression (e.g., Numpress) or optional transformations, byte-level comparison will fail even if data equivalence is maintained within acceptable tolerances.
- Compilation requires a Rust toolchain and may fail if dependencies are incompatible or unavailable; the library at the repository root is the primary implementation, while Python and R versions support reading only and may not reflect write behavior.
- Null-marked m/z reconstruction relies on fitted spacing models that may introduce small numerical errors for sparse or irregularly-spaced peaks; evaluation must allow for these tolerances.

## Evidence

- [other] Clone or obtain the HUPO-PSI/mzPeak repository at the root directory containing the Rust library source code. Compile the Rust library using Cargo, targeting the read/write API for mzPeak files. Load a sample mzPeak input file using the Rust library's read functionality. Write the loaded data back to disk as a new mzPeak file using the library's write functionality. Verify round-trip integrity by comparing the original and round-tripped files for structural and data equivalence.: "Clone or obtain the HUPO-PSI/mzPeak repository at the root directory containing the Rust library source code. Compile the Rust library using Cargo, targeting the read/write API for mzPeak files. Load"
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [intro] The Python and R implementations support reading mzPeak files only, not writing: "The Python and R implementations support reading mzPeak files only, not writing"
- [readme] This is a **work in progress**, no stability is guaranteed at this point: "This is a **work in progress**, no stability is guaranteed at this point"
- [readme] Because the non-zero m/z points remain unchanged, the reconstructed signal's peak apex or centroid should be unaffected.: "Because the non-zero m/z points remain unchanged, the reconstructed signal's peak apex or centroid should be unaffected."
