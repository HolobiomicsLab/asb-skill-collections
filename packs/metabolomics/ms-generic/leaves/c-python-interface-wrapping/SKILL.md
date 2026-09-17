---
name: c-python-interface-wrapping
description: Use when you have a mature C++ library (like OpenMS) with stable APIs
  that you want to make accessible from Python environments, and you need to preserve
  performance-critical C++ execution while supporting rapid prototyping or integration
  into Python-based data pipelines (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
  tools:
  - nanobind
  - CMake
  - OpenMS C++ library
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
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

# C++-Python-Interface-Wrapping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert a compiled C++ library into importable Python modules using binding generators (e.g. nanobind, SWIG) so that Python code can call C++ functions and classes directly. This skill is essential when you need to expose computationally intensive or legacy C++ code to Python workflows without rewriting the core logic.

## When to use

Apply this skill when you have a mature C++ library (like OpenMS) with stable APIs that you want to make accessible from Python environments, and you need to preserve performance-critical C++ execution while supporting rapid prototyping or integration into Python-based data pipelines (e.g., KNIME, Jupyter, or workflow engines).

## When NOT to use

- The C++ library is still under active development with unstable or frequently changing APIs—interface wrapping is brittle to C++ signature changes.
- Performance requirements can be met entirely in pure Python or via existing wheel packages—wrapping adds build complexity without proportional benefit.
- The C++ code is tightly coupled to platform-specific features or low-level system APIs that are difficult to expose safely through a language boundary.

## Inputs

- C++ header files (.h, .hpp) defining classes and functions to expose
- Binding specification files (nanobind .pyi or SWIG .i files)
- CMakeLists.txt or build configuration linking C++ sources and binding files
- Compiled C++ library or object files (.a, .lib, .so)

## Outputs

- Compiled Python extension module (.so on Linux, .pyd on Windows, .dylib on macOS)
- Importable Python module (e.g., `import pyOpenMS`)
- Python package with C++ class and function bindings accessible via Python syntax

## How to apply

Identify the C++ headers and classes to expose in the binding specification files (e.g., nanobind .pyi definitions in src/pyOpenMS/bindings/). Configure the build system (CMake) to invoke the binding generator on these specifications, compiling the resulting bindings into a Python extension module (.so on Linux, .pyd on Windows). Execute the build to generate the compiled module. Import the module in a Python environment using standard import syntax. Verify successful wrapping by calling a simple C++ function or accessing a class attribute through the Python interface, confirming that the binding preserves the expected method signatures and return types.

## Related tools

- **nanobind** (Binding generator that converts C++ classes and functions into importable Python modules with minimal boilerplate)
- **CMake** (Build system that orchestrates compilation of C++ sources, invokes the binding generator, and links the resulting extension module) — https://github.com/OpenMS/OpenMS
- **OpenMS C++ library** (Source C++ codebase (mass spectrometry algorithms and data structures) to be wrapped) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- The compiled extension module exists in the expected output directory and has the correct platform-specific file extension (.so, .pyd, .dylib).
- The module can be imported without C++ linker or runtime errors: `import pyOpenMS` succeeds.
- A simple C++ function or class method is callable from Python and returns data with the correct type and structure (e.g., `pyOpenMS.MSExperiment()` instantiates a Python object wrapping the C++ class).
- Signature inspection in Python matches the C++ API: `help(pyOpenMS.MSExperiment)` or `dir(pyOpenMS)` lists expected methods and attributes.
- Round-trip data conversion works: passing Python data structures to C++ functions and receiving results back preserves semantics (e.g., numeric precision, list ordering, object identity).

## Limitations

- Binding specification files must be maintained in sync with C++ API changes; breaking C++ API changes require updates to binding files and rebuild.
- Complex C++ features (template metaprogramming, operator overloading edge cases, multiple inheritance) may require explicit binding code or workarounds in the binding generator configuration.
- Performance of bound code depends on copy/move semantics across the C++–Python boundary; frequent small data transfers can negate the speed advantage of C++ execution.
- The generated Python module is binary-platform-specific; wheels must be built separately for each OS and Python version combination.
- Debugging stack traces may be difficult to interpret when errors originate in C++ code beneath the binding layer.

## Evidence

- [other] The provided document fragment does not contain sufficient technical description of the binding generation mechanism, binding file structure, or module import verification process to extract a bounded finding.: "The provided document fragment does not contain sufficient technical description of the binding generation mechanism"
- [other] Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications according to CLAUDE.md wrapping instructions. Configure the build system (CMake) to compile nanobind binding files into a Python extension module. Execute the build process to generate the compiled pyOpenMS module. Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors. Execute a simple function call or attribute access on the imported module to confirm binding completeness.: "Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications... Import the generated pyOpenMS module in a Python environment and verify that the module loads without"
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
- [readme] It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS"
- [readme] Documentation for the Python bindings pyOpenMS can be found on the pyOpenMS online documentation: "Documentation for the Python bindings pyOpenMS can be found on the pyOpenMS online documentation"
