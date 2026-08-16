---
name: cmake-build-configuration-for-extensions
description: Use when when you have C++ source code that needs to be wrapped as a
  Python extension module (e.g., pyOpenMS nanobind bindings), and you need to automate
  the build process via CMake to handle compilation, linking, and module artifact
  generation across multiple platforms (Windows, macOS, Linux).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0227
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3673
  tools:
  - CMake
  - nanobind
  - Python development headers
  license_tier: restricted
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_openms_2_cq
    doi: 10.1038/nmeth.3959
    title: OpenMS
  dedup_kept_from: coll_openms_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/nmeth.3959
  all_source_dois:
  - 10.1038/nmeth.3959
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cmake-build-configuration-for-extensions

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and compile C++ extension modules (such as nanobind Python bindings) using CMake build system integration. This skill enables conversion of compiled C++ libraries into importable Python extension modules by managing build flags, dependency resolution, and module output location.

## When to use

When you have C++ source code that needs to be wrapped as a Python extension module (e.g., pyOpenMS nanobind bindings), and you need to automate the build process via CMake to handle compilation, linking, and module artifact generation across multiple platforms (Windows, macOS, Linux).

## When NOT to use

- Input is a pre-compiled binary wheel or sdist package — use pip/conda install instead
- No CMakeLists.txt or build configuration exists — use setuptools/Poetry or other Python-native build tools
- Target is pure Python code with no C++ dependencies — use standard Python packaging tools

## Inputs

- CMakeLists.txt file with nanobind module configuration
- C++ source files in src/pyOpenMS/bindings/ directory
- Header files and OpenMS C++ API declarations
- Python development headers

## Outputs

- Compiled Python extension module (.pyd on Windows, .so on Linux/macOS)
- Importable pyOpenMS Python module
- Build artifacts in cmake build directory

## How to apply

Navigate to the root CMakeLists.txt or the extension-specific subdirectory (e.g., src/pyOpenMS/bindings/) and review the nanobind binding specifications and CMake configuration directives. Configure the build system by running `cmake` with appropriate flags to specify compiler, build type, and output paths. Execute `cmake --build .` (or `make`) to compile binding files into a shared library or .so/.pyd extension module. Verify that the compiled module is placed in the expected output directory (typically the Python site-packages equivalent or a build artifact folder). The rationale is that CMake abstracts platform-specific compilation details, allowing a single configuration to generate correct binaries for Windows (.pyd), macOS (.so), and Linux (.so) without manual intervention.

## Related tools

- **CMake** (Build configuration and compilation orchestration for C++ extension modules)
- **nanobind** (C++ binding generator that translates OpenMS C++ API into Python-callable code) — https://github.com/OpenMS/OpenMS
- **Python development headers** (Required include files and libraries for linking compiled extension module to Python runtime)

## Examples

```
cd /path/to/OpenMS && mkdir -p build && cd build && cmake .. -DPYTHON_EXECUTABLE=$(python3 -c 'import sys; print(sys.executable)') && cmake --build . --config Release
```

## Evaluation signals

- CMake configuration phase completes without errors and identifies all required dependencies (nanobind, Python headers, OpenMS library)
- Build phase produces a .so/.pyd/.dylib file in the expected output directory with non-zero file size
- Compiled module can be imported in Python without ImportError or symbol resolution failures: `import pyOpenMS`
- Module attributes and functions are accessible and callable: e.g. `dir(pyOpenMS)` returns non-empty list, function calls execute without segmentation fault
- No unresolved linker symbols when running `ldd` (Linux) or `nm` (macOS) on the compiled module artifact

## Limitations

- CMake configuration is platform-specific; cross-compilation may require toolchain file specification
- Nanobind binding completeness depends on manual wrapping of C++ methods — not all OpenMS API is automatically exposed
- Changes to OpenMS C++ headers or method signatures require re-running CMake and rebuild; no incremental binding update
- Python version mismatch between development headers and runtime target will cause import failures

## Evidence

- [other] Configure the build system (CMake) to compile nanobind binding files into a Python extension module.: "Configure the build system (CMake) to compile nanobind binding files into a Python extension module."
- [readme] OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "OpenMS offers Python bindings to a large part of the OpenMS API"
- [other] Execute the build process to generate the compiled pyOpenMS module.: "Execute the build process to generate the compiled pyOpenMS module."
- [other] Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors.: "Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors."
- [readme] OpenMS runs under Windows, macOS, and Linux.: "OpenMS is free software available under the three-clause BSD license and runs under Windows, macOS, and Linux."
