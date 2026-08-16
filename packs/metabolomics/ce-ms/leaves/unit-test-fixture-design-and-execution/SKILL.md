---
name: unit-test-fixture-design-and-execution
description: Use when when implementing or modifying a numerical compression/decompression component (e.g., Numpress for mass-spectrometry m/z and intensity arrays) and you need to verify that round-trip encoding and decoding preserves numerical fidelity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0234
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - KNIME
  - OpenMS
  techniques:
  - CE-MS
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- how you installed OpenMS (e.g., from within KNIME, binary installers, self compiled)
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

# unit-test-fixture-design-and-execution

## Summary

Design and execute unit test fixtures to validate encoder/decoder round-trip correctness for numerical data compression algorithms. This skill ensures that encoded data can be faithfully decoded back to the original input within machine precision tolerances.

## When to use

When implementing or modifying a numerical compression/decompression component (e.g., Numpress for mass-spectrometry m/z and intensity arrays) and you need to verify that round-trip encoding and decoding preserves numerical fidelity. Apply this skill after the encoder and decoder implementations are complete but before integration testing.

## When NOT to use

- When the encoder/decoder implementations are not yet complete or not yet compiled into a runnable form.
- When test fixtures do not exist in the repository and you are uncertain about expected output ranges or precision requirements.
- When integration tests with real mass-spectrometry file formats (mzML, mzXML) are the primary validation goal; unit fixtures are more appropriate for isolated component testing.

## Inputs

- source code of encoder and decoder implementations (C++ classes or equivalent)
- reference test fixture files from the project repository
- arrays of floating-point test data (m/z and intensity values in appropriate ranges)
- project build configuration and test runner setup

## Outputs

- test execution results (pass/fail status for each fixture)
- numerical comparison logs (decoded vs. original values and their deltas)
- round-trip validation report documenting precision loss, if any
- failure logs for any deviating test cases

## How to apply

Retrieve reference test fixtures from the project's test suite (e.g., MSNumpressCoder_test.cpp from the OpenMS GitHub repository). Design test cases that encode a known array of floating-point values (m/z or intensity arrays), then immediately decode the result and compare decoded values against the original input for numerical equality within machine precision. Execute the full unit test suite to verify all fixtures pass. Document any numerical deviations or test failures, paying special attention to boundary cases (very small/large values, repeated elements) and encoding-specific parameters. Use a testing framework integrated with the project (e.g., C++ CppUnit or similar) to automate fixture validation.

## Related tools

- **OpenMS** (C++ library providing MSNumpressCoder component and reference test fixtures for numerical compression validation) — https://github.com/OpenMS/OpenMS
- **KNIME** (optional workflow integration platform for executing OpenMS tools including compression/decompression validation)

## Evaluation signals

- All test fixtures in the project's test suite pass without error (e.g., MSNumpressCoder_test.cpp runs to completion with 0 failures).
- Numerical comparison of decoded arrays against original input arrays shows zero or machine-epsilon-level differences (typically < 1e-6 relative error for float32, < 1e-15 for float64).
- Round-trip encoding and decoding of boundary-case arrays (very small positive/negative values, repeated elements, max/min representable floats) succeeds without overflow, underflow, or NaN generation.
- Test logs contain no warnings or assertions about precision loss beyond documented tolerances for the specific compression algorithm (e.g., Numpress loss-less vs. lossy modes).
- Execution time and memory usage for fixture validation remain within expected bounds for the test suite, with no memory leaks or resource exhaustion detected.

## Limitations

- Unit test fixtures validate only the encoder/decoder in isolation; they do not confirm correct integration with upstream file readers or downstream analysis tools.
- Machine precision and rounding behavior may vary across platforms (x86, ARM, different compilers); fixtures should be run on all target platforms to catch platform-specific numerical issues.
- Test fixtures may not exercise all edge cases (e.g., extremely sparse arrays, pathological compression ratios) present in real mass-spectrometry data; additional stress testing or property-based testing may be necessary.
- Lossy compression algorithms (e.g., Numpress lossy mode) by design introduce controlled error; unit fixtures must clearly distinguish acceptable loss from true codec failures.

## Evidence

- [other] Retrieve the MSNumpressCoder class specification and reference test cases from the OpenMS GitHub repository (github.com/OpenMS/OpenMS/src/tests/class_tests/openms/source/MSNumpressCoder_test.cpp).: "Retrieve the MSNumpressCoder class specification and reference test cases from the OpenMS GitHub repository"
- [other] Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision.: "Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision."
- [other] Run the full OpenMS MSNumpressCoder unit test suite to verify all test fixtures pass, documenting any deviations or failures.: "Run the full OpenMS MSNumpressCoder unit test suite to verify all test fixtures pass, documenting any deviations or failures."
- [other] MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays, with validation performed through test fixtures located in the OpenMS test suite.: "MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays, with validation performed through test fixtures"
