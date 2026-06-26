---
name: rust-build-and-compilation
description: Use when when you have Rust source code (such as the mzPeak format implementation
  at the repository root) and need to generate executable binaries or libraries for
  converting mass-spectrometry file formats, validating output files, or reading/writing
  domain-specific formats like mzPeak.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Rust
  - cargo
  - mzPeak
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Rust Build and Compilation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compiling Rust source code into executable binaries and libraries using cargo, the Rust package manager. This skill is essential for constructing command-line tools and libraries for scientific data format conversion and validation.

## When to use

When you have Rust source code (such as the mzPeak format implementation at the repository root) and need to generate executable binaries or libraries for converting mass-spectrometry file formats, validating output files, or reading/writing domain-specific formats like mzPeak.

## When NOT to use

- Input is already a pre-compiled binary or distributed package—skip to execution instead of rebuilding
- Rust toolchain is not installed or target platform lacks required system libraries—install prerequisites first
- You only need to read or inspect source code without execution—use a text editor or code browser instead

## Inputs

- Rust source code repository with Cargo.toml manifest
- Rust version (typically 1.56 or later)
- System libraries and development headers required by dependencies

## Outputs

- Compiled executable binaries in target/debug/ or target/release/
- Static or dynamic libraries (.rlib, .so, .dylib, .dll)
- Intermediate build artifacts in target/ directory

## How to apply

Clone or access the target Rust repository containing the source code and Cargo.toml manifest. Execute `cargo build` (or `cargo build --release` for optimized production binaries) from the repository root to compile all dependencies and source code into an executable. The build process resolves dependencies declared in Cargo.toml, compiles them in the correct order, and produces binaries in the `target/` directory. Verify successful compilation by checking that no errors are reported and that the expected binary exists at `target/debug/` or `target/release/` depending on build mode. For reproducible builds, inspect the Cargo.lock file to ensure dependency versions are pinned.

## Related tools

- **cargo** (Rust package manager and build system used to compile mzPeak implementation) — https://doc.rust-lang.org/cargo/
- **Rust** (Programming language in which the mzPeak library and command-line conversion tools are written) — https://www.rust-lang.org/
- **mzPeak** (Primary Rust implementation being compiled; includes library for reading/writing mzPeak files and CLI tools for format conversion) — https://github.com/HUPO-PSI/mzPeak

## Examples

```
cd /path/to/HUPO-PSI/mzPeak && cargo build --release
```

## Evaluation signals

- Cargo build completes without errors or warnings (or only expected warnings); exit code is 0
- Binary executable or library file exists at expected path in target/debug/ or target/release/ with non-zero file size
- Running the compiled binary with --help or --version produces expected output and does not segfault
- If building a library, verify that generated .rlib or .so file can be linked by downstream code or inspected with cargo metadata
- Timestamps on output binaries are newer than source .rs files, confirming recompilation occurred

## Limitations

- mzPeak implementation is a work in progress with no stability guaranteed; compilation may fail or produce unstable binaries across versions
- Python and R implementations are read-only and do not include full Rust compilation workflow; only the Rust implementation at repository root supports reading and writing
- Compilation requires Rust toolchain to be pre-installed on the system; no pre-built binaries are mentioned in the documentation
- Build times depend on the number and complexity of dependencies; cold builds can be slow on first compilation

## Evidence

- [readme] Build process and expected outputs: "Build the Rust CLI tool using cargo (the Rust package manager). 3. Execute the conversion command-line tool"
- [readme] Primary language and location of implementation: "The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into"
- [readme] Build tool and environment setup: "The simplest path uses [`uv`](https://docs.astral.sh/uv/) and the provided [`Justfile`](Justfile): ```bash just setup     # create .venv and install MkDocs Material just serve     # live-reload"
- [readme] Work-in-progress status affecting stability: "**NOTE**: This is a **work in progress**, no stability is guaranteed at this point"
