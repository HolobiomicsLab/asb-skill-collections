---
name: python-binding-generation-with-nanobind
description: Use when when you have a C++ library (such as OpenMS) with nanobind binding specifications in a designated bindings directory and need to create a Python module that exposes C++ classes, functions, and data types to Python code.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3365
  tools:
  - nanobind
  - CMake
  - OpenMS
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- nanobind binding files are in `src/pyOpenMS/bindings/`
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
---

# python-binding-generation-with-nanobind

## Summary

Generate importable Python modules from C++ source code using nanobind binding specifications and CMake compilation. This skill bridges OpenMS C++ API functionality into Python environments by converting binding declarations into compiled extension modules.

## When to use

When you have a C++ library (such as OpenMS) with nanobind binding specifications in a designated bindings directory and need to create a Python module that exposes C++ classes, functions, and data types to Python code. Use this skill when preparing a library for Python-first development workflows or when testing whether the full C++ API surface is accessible from Python.

## When NOT to use

- Input is already a compiled Python wheel or conda package — skip to installation instead of rebuilding.
- Binding specification files are incomplete or missing for the C++ API surface you need to expose.
- Target C++ library cannot be compiled on the platform where you want to build the Python bindings (e.g., missing platform-specific toolchain or incompatible dependencies).

## Inputs

- nanobind binding specification files (C++ source with nb::module declarations)
- CMakeLists.txt with nanobind build targets
- OpenMS C++ library headers and compiled object files
- Python development headers and interpreter (version matching the target binding)

## Outputs

- Compiled Python extension module (.so on Linux, .pyd on Windows, .dylib on macOS)
- Importable pyOpenMS module accessible from Python sys.modules
- Verified binding completeness attestation (successful import + callable C++ functions/classes)

## How to apply

First, review the nanobind binding specification files (typically in src/pyOpenMS/bindings/ for OpenMS) to understand which C++ types and functions are exposed. Configure the CMake build system to compile these bindings into a Python extension module by specifying nanobind as a build dependency and ensuring the binding files are included in the compilation targets. Execute the CMake configuration and build process to generate the compiled .so/.pyd/.dylib extension module. Import the resulting module in a Python interpreter using standard import syntax (e.g., `import pyOpenMS`), and verify module loading completes without ImportError or symbol resolution failures. Finally, execute a simple function call or attribute access on an exposed C++ class or function to confirm that the binding layer correctly translates between Python and C++ calling conventions.

## Related tools

- **nanobind** (Python binding framework used to define and generate C++-to-Python conversion layer from binding specifications)
- **CMake** (Build system that configures compilation of nanobind binding sources into a linkable Python extension module)
- **OpenMS** (C++ mass spectrometry library being exposed to Python through pyOpenMS bindings) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- Module imports without raising ImportError, ModuleNotFoundError, or unresolved symbol errors when executed in a Python interpreter.
- Calling a bound C++ function or instantiating a bound class (e.g., `obj = pyOpenMS.SomeClass()`) succeeds and returns a Python object with expected attributes/methods.
- No segmentation faults or memory access violations occur during simple function calls or method invocations on bound C++ objects.
- Introspection on imported module reveals expected classes, functions, and type signatures matching the binding declarations (e.g., `dir(pyOpenMS)` and `help(pyOpenMS.SomeClass)` show expected items).
- CMake build log confirms all nanobind binding source files were compiled and linked without errors or warnings.

## Limitations

- The provided document fragment lacks sufficient technical detail on binding file structure, module organization, and symbol export strategies; practitioners may need to consult nanobind official documentation and OpenMS-specific binding conventions beyond this skill description.
- Platform-specific toolchain compatibility (C++ compiler, Python development headers version match) is a hard prerequisite; binding generation will fail silently or with cryptic linker errors if toolchain versions are mismatched.
- Only C++ API surface for which binding specifications have been explicitly written will be accessible from Python; unbound C++ functionality remains inaccessible, even if present in the C++ library.

## Evidence

- [other] Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications according to CLAUDE.md wrapping instructions.: "Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications according to CLAUDE.md wrapping instructions."
- [other] Configure the build system (CMake) to compile nanobind binding files into a Python extension module.: "Configure the build system (CMake) to compile nanobind binding files into a Python extension module."
- [other] Execute the build process to generate the compiled pyOpenMS module.: "Execute the build process to generate the compiled pyOpenMS module."
- [other] Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors.: "Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors."
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
