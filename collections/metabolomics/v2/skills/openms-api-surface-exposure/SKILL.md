---
name: openms-api-surface-exposure
description: Use when when you need to make OpenMS C++ classes, functions, or data structures callable from Python code, or when verifying that a newly bound C++ component can be imported and instantiated without errors in a Python environment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0339
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - nanobind
  - CMake
  - OpenMS C++ library
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
---

# openms-api-surface-exposure

## Summary

Expose and verify OpenMS C++ API surface through nanobind-based Python bindings, enabling downstream Python code to access mass spectrometry data structures and algorithms. This skill bridges compiled C++ library functionality into importable Python modules for rapid prototyping and algorithm development.

## When to use

When you need to make OpenMS C++ classes, functions, or data structures callable from Python code, or when verifying that a newly bound C++ component can be imported and instantiated without errors in a Python environment. Triggers: adding new C++ bindings to src/pyOpenMS/bindings/, building the pyOpenMS extension module from source, or testing binding completeness after CMake compilation.

## When NOT to use

- Input is already a pre-built binary wheel (.whl) or conda package; use package installation instead.
- No C++ source changes are needed and only existing Python APIs are being called.
- The goal is to use OpenMS algorithms without rebuilding the extension module (use existing pyOpenMS installation from bioconda or conda-forge).

## Inputs

- C++ source files in src/pyOpenMS/bindings/ with nanobind binding declarations
- CMakeLists.txt with nanobind compilation rules
- OpenMS C++ library headers and compiled object files

## Outputs

- Compiled pyOpenMS Python extension module (.so on Linux, .pyd on Windows, .dylib on macOS)
- Importable Python module with bound C++ classes and functions
- Module load verification and runtime function call test results

## How to apply

Navigate to src/pyOpenMS/bindings/ and review or create nanobind binding specifications according to the wrapping instructions in CLAUDE.md. Configure the CMake build system to compile the nanobind binding files into a Python extension module (.so/.pyd). Execute the CMake build process to generate the compiled pyOpenMS module. Import the generated pyOpenMS module in a Python environment (e.g., `import pyOpenMS`) and verify that the module loads without ImportError or missing symbol errors. Execute a simple function call or attribute access on a bound C++ class (e.g., instantiate a spectrum object, call a peak-finding method) to confirm that the binding is complete and functional. Check for runtime type errors, segmentation faults, or attribute access failures that would indicate incomplete or incorrect binding specifications.

## Related tools

- **nanobind** (Binding code generator and C++/Python interop framework used to specify and compile OpenMS C++ classes into importable Python extension modules)
- **CMake** (Build system configuration tool that orchestrates nanobind compilation, linking, and extension module generation)
- **OpenMS C++ library** (Upstream C++ API being exposed through nanobind bindings) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- pyOpenMS module imports without ImportError, ModuleNotFoundError, or unresolved symbol errors.
- A bound C++ class can be instantiated from Python (e.g., `spectrum = pyOpenMS.MSSpectrum()`).
- Methods and attributes on bound objects are callable and return expected types without segmentation faults.
- No AttributeError or TypeError when accessing bound functions with correct argument types.
- CMake build log shows zero compilation warnings or errors in nanobind binding code.

## Limitations

- The provided document fragment does not contain the full technical specification of binding file structure or module import verification process, limiting detailed guidance on binding specification syntax.
- Nanobind binding completeness depends on manual specification of each C++ class/function to expose; not all OpenMS C++ API is automatically bound.
- Platform-specific compilation issues may occur on Windows, macOS, and Linux due to different C++ toolchains and nanobind ABI requirements.
- Binding layer may introduce performance overhead compared to native C++ for computationally intensive workflows.

## Evidence

- [other] Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications according to CLAUDE.md wrapping instructions.: "Navigate to the src/pyOpenMS/bindings/ directory and review nanobind binding specifications according to CLAUDE.md wrapping instructions."
- [other] Configure the build system (CMake) to compile nanobind binding files into a Python extension module.: "Configure the build system (CMake) to compile nanobind binding files into a Python extension module."
- [other] Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors.: "Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors."
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
- [other] Execute a simple function call or attribute access on the imported module to confirm binding completeness.: "Execute a simple function call or attribute access on the imported module to confirm binding completeness."
