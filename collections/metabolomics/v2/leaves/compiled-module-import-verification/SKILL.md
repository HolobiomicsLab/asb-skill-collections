---
name: compiled-module-import-verification
description: Use when after compiling nanobind-based C++ bindings into a Python extension
  module (e.g., pyOpenMS), or when integrating a newly built native module into a
  Python environment. Apply this skill to confirm that the generated .so/.pyd/.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - nanobind
  - CMake
  - Python interpreter
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

# compiled-module-import-verification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that a compiled Python extension module (generated from C++ bindings via nanobind) loads without errors and exposes the expected API surface. This skill ensures binding completeness and runtime correctness before deployment.

## When to use

After compiling nanobind-based C++ bindings into a Python extension module (e.g., pyOpenMS), or when integrating a newly built native module into a Python environment. Apply this skill to confirm that the generated .so/.pyd/.dylib file is importable, module metadata is present, and at least one representative function or class attribute is callable.

## When NOT to use

- The module source code has not yet been compiled or CMake build has not completed.
- The module is already known to work (e.g., it is a tested release version in production).
- You are performing static analysis of C++ binding declarations rather than runtime validation.

## Inputs

- Compiled Python extension module file (.so on Linux, .pyd on Windows, .dylib on macOS)
- Python environment with compatible runtime and dependencies

## Outputs

- Module import success/failure status
- Proof of binding completeness (successful function call or attribute access)
- Error traceback (if import or invocation fails)

## How to apply

In a Python environment where the compiled extension module is discoverable (via PYTHONPATH or site-packages), import the generated module and execute a simple function call or attribute access on it. Wrap the import and invocation in a try-except block to catch import errors (missing dependencies, ABI mismatches, symbol resolution failures) and attribute errors (missing bindings). Check that the module object exists in sys.modules and that the invoked function or attribute returns without raising an exception. This validates that the binding layer successfully exposed the C++ API and that the compiled code is ABI-compatible with the Python runtime.

## Related tools

- **nanobind** (Generates Python bindings from C++ code; compiled output is the target of import verification)
- **CMake** (Builds the C++ binding files into a Python extension module prior to import testing)
- **Python interpreter** (Runtime environment in which the compiled extension module is imported and tested)

## Evaluation signals

- Module imports without ImportError, AttributeError, or symbol resolution failures.
- Module object is present in sys.modules after successful import.
- Representative function or class attribute from the C++ API is callable and executes without exception.
- Invoked function returns a value or object consistent with C++ API documentation.
- No segmentation faults or ABI incompatibility errors occur during invocation.

## Limitations

- This skill only validates that the module can be imported and a single representative call succeeds; it does not perform exhaustive API coverage testing or verify correctness of all bindings.
- Import success does not guarantee that all exposed functions are correctly bound or that numerical results are accurate.
- Platform-specific ABI mismatches (e.g., glibc version, MSVC runtime) may prevent import even if the binding code is correct.

## Evidence

- [other] Execute the build process to generate the compiled pyOpenMS module. 4. Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors. 5. Execute a simple function call or attribute access on the imported module to confirm binding completeness.: "Execute the build process to generate the compiled pyOpenMS module. 4. Import the generated pyOpenMS module in a Python environment and verify that the module loads without errors. 5. Execute a"
- [readme] With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development.: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
