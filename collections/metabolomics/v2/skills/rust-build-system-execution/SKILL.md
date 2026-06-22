---
name: rust-build-system-execution
description: Use when you have obtained a Rust source repository (e.g., mzpeak_prototyping) and need to compile it into a working command-line converter tool or library. Use this skill when the source includes a Cargo.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - OpenMS
  - Rust
  - Cargo
  - mzpeak_prototyping
  techniques:
  - mass-spectrometry
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
  - build: coll_mzpeak
    doi: 10.1021/acs.jproteome.5c00435
    title: mzpeak
  dedup_kept_from: coll_mzpeak
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

# rust-build-system-execution

## Summary

Build and compile a Rust project using cargo to produce executable command-line tools or libraries. This skill is essential for preparing prototype bioinformatics software—such as mass spectrometry format converters—from source code into runnable binaries.

## When to use

You have obtained a Rust source repository (e.g., mzpeak_prototyping) and need to compile it into a working command-line converter tool or library. Use this skill when the source includes a Cargo.toml manifest and you need to produce executable binaries that can read, write, or transform scientific data formats (such as converting mzML into mzPeak binary format).

## When NOT to use

- The source code is not Rust; use language-specific build tools (e.g., pip for Python, npm for JavaScript, Maven for Java) instead.
- A pre-compiled binary is already available and no source modification is needed; proceed directly to execution.
- The repository lacks a Cargo.toml file or is incomplete; consult project documentation or clone a complete version first.

## Inputs

- Rust source code directory with Cargo.toml manifest
- Dependency declarations in Cargo.toml and Cargo.lock (if present)
- Source files (*.rs) implementing the converter or library

## Outputs

- Compiled executable binary (e.g., mzpeak_converter in target/debug/ or target/release/)
- Compiled library artifacts (.rlib or .so/.dylib files)
- Build metadata and intermediate object files in target/

## How to apply

Execute `cargo build` at the repository root to compile the Rust project using the Cargo build system, which resolves dependencies, compiles source code, and produces binaries in the `target/` directory. If optimization is required (e.g., for performance-critical converters), use `cargo build --release`. After a successful build, the compiled converter tool is available as an executable in `target/debug/` or `target/release/`. Verify compilation by checking for zero error messages and confirming that the expected binary file exists with executable permissions. The build system will also validate the project's dependency graph and Rust syntax at compile time.

## Related tools

- **Rust** (Programming language and compiler for building the mzPeak converter and library) — https://github.com/rust-lang/rust
- **Cargo** (Rust package manager and build system used to compile the project) — https://github.com/rust-lang/cargo
- **mzpeak_prototyping** (Rust project containing command-line tools and libraries for mzPeak format conversion) — https://github.com/mobiusklein/mzpeak_prototyping

## Examples

```
cd mzpeak_prototyping && cargo build --release && ./target/release/mzpeak_converter input.mzML output.mzpeak
```

## Evaluation signals

- Build completes with zero compiler errors and warnings (or expected warnings only)
- Executable binary exists at target/debug/<tool_name> or target/release/<tool_name> with executable file permissions
- Running the compiled tool without arguments or with --help displays expected command-line interface and usage instructions
- Tool successfully accepts valid input files (e.g., mzML) and produces output files in the expected format (e.g., mzPeak binary with correct structure and metadata)
- Output mzPeak files can be read by other mzPeak implementations (Python, R) without format validation errors

## Limitations

- Project is in work-in-progress status with no stability guarantee; API and binary format may change between builds.
- Build requires Rust toolchain (rustc and cargo) to be installed and accessible on the system; cannot build on systems without Rust.
- Command-line interface and supported input formats are not comprehensively documented; refer to repository source code or inline help.
- The converter tool is a prototype; corner cases, edge cases in mzML input, or vendor-specific quirks may not be handled gracefully.

## Evidence

- [other] Build the command-line converter tool using Rust's cargo build system.: "Build the command-line converter tool using Rust's cargo build system."
- [readme] The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] NOTE: This is a work in progress, no stability is guaranteed at this point.: "NOTE: This is a **work in progress**, no stability is guaranteed at this point."
- [other] Clone or obtain the mzpeak_prototyping Rust repository from github.com/mobiusklein/mzpeak_prototyping at the repository root.: "Clone or obtain the mzpeak_prototyping Rust repository from github.com/mobiusklein/mzpeak_prototyping at the repository root."
