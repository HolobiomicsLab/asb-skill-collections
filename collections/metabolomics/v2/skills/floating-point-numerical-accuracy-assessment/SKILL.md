---
name: floating-point-numerical-accuracy-assessment
description: 'Use when when implementing or validating a lossy numeric codec for mass-spectrometry data (e.g., MSNumpressCoder in OpenMS). Specifically: after implementing both encoder and decoder, before shipping to production, or when comparing alternative compression schemes.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3564
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - KNIME
  - MSNumpressCoder
  - OpenMS
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

# floating-point-numerical-accuracy-assessment

## Summary

Validate that lossy numeric compression and decompression algorithms (e.g., Numpress) preserve floating-point m/z and intensity values within machine precision tolerances. This skill assesses whether round-trip encoding–decoding cycles introduce unacceptable numerical drift in mass-spectrometry data arrays.

## When to use

When implementing or validating a lossy numeric codec for mass-spectrometry data (e.g., MSNumpressCoder in OpenMS). Specifically: after implementing both encoder and decoder, before shipping to production, or when comparing alternative compression schemes. Triggered by the need to ensure decoded m/z and intensity arrays match original input arrays to within floating-point rounding error, not larger systematic deviations.

## When NOT to use

- Input data is already losslessly compressed or integer-only (no floating-point precision to assess).
- Validation is performed only on a single representative sample; edge cases and diverse array magnitudes are not tested.
- No baseline or reference unit test suite exists to confirm expected numerical tolerances for the domain.

## Inputs

- floating-point numeric array (m/z values, intensity values, or similar mass-spectrometry peak data in single or double precision)
- lossy numeric encoder function (e.g., MSNumpressCoder.encodeFixedPoint)
- lossy numeric decoder function (e.g., MSNumpressCoder.decodeFixedPoint)

## Outputs

- round-trip validation report (per-element error statistics: max absolute error, max relative error, mean error)
- pass/fail verdict for each test vector (decoded array vs. original within tolerance)
- identification of failure modes or edge cases (e.g., subnormal floats, large magnitude jumps)

## How to apply

Execute a round-trip validation workflow: (1) encode a representative test array of m/z or intensity floating-point values using the codec's encoder (e.g., MSNumpressCoder.encodeFixedPoint or encodePic); (2) decode the resulting byte stream using the decoder; (3) element-wise compare the decoded floating-point array against the original input array; (4) compute per-element relative error and absolute error, checking that both remain within acceptable bounds (typically machine epsilon × magnitude, or <1e-6 relative error for mass spectrometry); (5) repeat across diverse input arrays (sparse peaks, dense clusters, extreme ranges) to detect edge-case failures. Use the unit test suite (e.g., MSNumpressCoder_test.cpp from OpenMS) as the validation harness and baseline.

## Related tools

- **MSNumpressCoder** (C++ class implementing Numpress encode/decode for m/z and intensity arrays in mass-spectrometry workflows) — https://github.com/OpenMS/OpenMS
- **OpenMS** (Open-source C++ library providing infrastructure for LC-MS data management and test harness for MSNumpressCoder validation) — https://github.com/OpenMS/OpenMS
- **KNIME** (Workflow orchestration tool for integrating OpenMS tools (including MSNumpressCoder) into automated analysis pipelines)

## Evaluation signals

- Round-trip encoded–decoded array bit-wise or numerically matches original input within machine epsilon or domain-specific tolerance (e.g., <1 ppm for m/z, <1% relative for intensity).
- Per-element absolute and relative errors remain below configurable thresholds across all test vectors, including edge cases (very small, very large, clustered, sparse arrays).
- Unit test suite (MSNumpressCoder_test.cpp) executes without assertion failures and reports zero failed test fixtures.
- Comparative analysis: if multiple codec candidates exist, round-trip error metrics are computed and ranked to guide codec selection.
- No systematic bias or drift is observed when encoding then decoding repeatedly in series (chained compression does not accumulate error beyond single round-trip tolerance).

## Limitations

- Numpress and similar lossy codecs accept precision loss by design; acceptable error thresholds must be empirically set for each mass-spectrometry application (e.g., 0.01 Da for m/z, 5% for intensity).
- Machine floating-point rounding introduces platform-dependent and compiler-dependent variability; test fixtures must account for different architectures (x86_64, ARM) and precision modes (float32, float64).
- Edge cases like subnormal floats, infinity, and NaN may exhibit platform-specific codec behavior; comprehensive test coverage requires explicit handling.
- Validation is performed only on synthetic or reference test arrays; real-world mass-spectrometry data may exhibit different statistical properties (e.g., bimodal intensity distributions) that could reveal additional codec artifacts.

## Evidence

- [other] MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays: "MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays, with validation performed through test fixtures located in the OpenMS test suite."
- [other] Execute round-trip validation by encoding test array, then decoding result and comparing against original for numerical equality within machine precision.: "Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision."
- [other] Retrieve test cases from OpenMS repository and run full unit test suite to verify all test fixtures pass: "Retrieve the MSNumpressCoder class specification and reference test cases from the OpenMS GitHub repository (github.com/OpenMS/OpenMS/src/tests/class_tests/openms/source/MSNumpressCoder_test.cpp)."
- [readme] OpenMS is an open-source software C++ library for LC-MS data management and analyses offering infrastructure for rapid development of mass spectrometry-related software.: "OpenMS is an open-source software C++ library for LC-MS data management and analyses. It offers an infrastructure for rapid development of mass spectrometry-related software."
- [readme] OpenMS supports integration into workflow engines like KNIME via the TOPPTools concept and unified parameter handling.: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept and a unified parameter handling via a 'common tool"
