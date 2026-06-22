---
name: numeric-array-round-trip-validation
description: Use when after implementing or modifying a numerical compression codec (such as MSNumpressCoder for m/z and intensity arrays in mass-spectrometry workflows) to verify that round-trip encode–decode cycles preserve numerical values within expected tolerance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - KNIME
  - MSNumpressCoder
  - OpenMS unit test suite
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numeric-array-round-trip-validation

## Summary

Validate numerical compression and decompression by encoding test arrays, decoding the result, and comparing decoded values against originals for equality within machine precision. This skill ensures fidelity of lossy or lossless compression codecs used in mass-spectrometry data pipelines.

## When to use

Apply this skill after implementing or modifying a numerical compression codec (such as MSNumpressCoder for m/z and intensity arrays in mass-spectrometry workflows) to verify that round-trip encode–decode cycles preserve numerical values within expected tolerance. Use it as a gate before integration into production data processing pipelines.

## When NOT to use

- Input data is already pre-validated by an upstream tool and integration test coverage is already sufficient.
- Codec specification is still in design phase and encoding/decoding functions are not yet implemented.
- Round-trip validation is not applicable because the compression format is append-only or single-pass (no decode stage).

## Inputs

- floating-point array of m/z values or intensity measurements
- compression codec implementation (class or function)
- unit test fixture suite

## Outputs

- comparison report of original vs. decoded values
- pass/fail status for each test vector
- unit test execution log with success count

## How to apply

Construct a test array of known floating-point values representing either m/z ratios or intensity measurements. Invoke the encoder on the test array to produce a compressed byte stream. Immediately decode the byte stream using the corresponding decoder. Compare each decoded value against the original input array element-wise, checking that differences fall within machine epsilon or a domain-specific tolerance (e.g., parts-per-million for mass accuracy). Document pass/fail for each test vector and any deviations. Run the full codec unit test suite to verify all test fixtures in the OpenMS test directory (e.g., MSNumpressCoder_test.cpp) pass without failure.

## Related tools

- **MSNumpressCoder** (Encoder/decoder class for m/z and intensity numeric array compression in OpenMS; implements the Numpress compression algorithm for mass-spectrometry data.) — https://github.com/OpenMS/OpenMS
- **OpenMS unit test suite** (Test fixture collection (MSNumpressCoder_test.cpp) that exercises codec round-trip validation and ensures all test vectors pass.) — https://github.com/OpenMS/OpenMS/blob/develop/src/tests/class_tests/openms/source/MSNumpressCoder_test.cpp
- **KNIME** (Workflow orchestration tool for integrating OpenMS components (including MSNumpressCoder) into data-processing pipelines.)

## Evaluation signals

- Decoded array has identical length and dimensionality as original input array.
- Each decoded value matches the original value within machine precision or domain-specific tolerance (e.g., < 5 ppm for m/z values).
- All unit test fixtures in MSNumpressCoder_test.cpp execute without assertion failures or exceptions.
- Round-trip error (max absolute or relative difference across all array elements) is zero or below a documented threshold.
- Byte-stream is non-empty and has expected size relative to input array dimensionality and compression ratio.

## Limitations

- Round-trip validation assumes both encoder and decoder implementations are available and correct; it does not detect bugs present in both simultaneously.
- Validation depends on choice of tolerance threshold; values below machine epsilon may fail spuriously due to floating-point rounding.
- MSNumpressCoder specifically targets m/z and intensity arrays; validation method may not transfer to other data types or compression schemes without modification.
- No changelog documented in OpenMS repository, so codec changes between versions may not be tracked explicitly.

## Evidence

- [other] MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays: "MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays, with validation performed through test fixtures located in the OpenMS test suite."
- [other] Implement the MSNumpressCoder encoder to compress m/z and intensity arrays using the Numpress compression algorithm; Implement the MSNumpressCoder decoder to decompress Numpress-encoded byte streams back into floating-point m/z and intensity arrays: "Implement the MSNumpressCoder encoder to compress m/z and intensity arrays using the Numpress compression algorithm. 3. Implement the MSNumpressCoder decoder to decompress Numpress-encoded byte"
- [other] Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision: "Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision."
- [other] Run the full OpenMS MSNumpressCoder unit test suite to verify all test fixtures pass, documenting any deviations or failures: "Run the full OpenMS MSNumpressCoder unit test suite to verify all test fixtures pass, documenting any deviations or failures."
- [readme] OpenMS is free software available under the three-clause BSD license and runs under Windows, macOS, and Linux: "OpenMS is free software available under the three-clause BSD license and runs under Windows, macOS, and Linux."
