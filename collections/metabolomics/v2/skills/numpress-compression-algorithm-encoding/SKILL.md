---
name: numpress-compression-algorithm-encoding
description: Use when you have raw floating-point m/z and intensity arrays extracted from mass-spectrometry experiments (e.g., from mzML or mzXML files) and need to compress them for storage or transmission.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - KNIME
  - OpenMS
  - pyOpenMS
  techniques:
  - LC-MS
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

# numpress-compression-algorithm-encoding

## Summary

Encodes m/z and intensity numeric arrays from mass-spectrometry data using the Numpress compression algorithm to produce byte-level compressed representations. This skill is essential for reducing file size and transmission bandwidth of LC-MS datasets while preserving numerical precision within machine epsilon.

## When to use

Apply this skill when you have raw floating-point m/z and intensity arrays extracted from mass-spectrometry experiments (e.g., from mzML or mzXML files) and need to compress them for storage or transmission. Use it as part of a data pipeline where space efficiency and round-trip numerical fidelity are both required — for example, before archiving LC-MS raw data or preparing mass-spectrometry data for integration into workflow engines like KNIME or Galaxy.

## When NOT to use

- Input data is already Numpress-encoded or in a pre-compressed format (e.g., mzML with embedded compressed spectra)
- Numerical precision loss is unacceptable or the application requires lossless bit-for-bit recovery (note: Numpress is lossy compression with controlled precision, not bit-level)
- Mass-spectrometry data arrays are very small (< 10 m/z–intensity pairs), where compression overhead exceeds savings

## Inputs

- floating-point numeric array (m/z values)
- floating-point numeric array (intensity values)
- mass-spectrometry raw data in mzML or mzXML format

## Outputs

- compressed byte stream (Numpress-encoded m/z array)
- compressed byte stream (Numpress-encoded intensity array)
- validation report (round-trip comparison results)

## How to apply

Instantiate the MSNumpressCoder encoder from the OpenMS library with the input floating-point array (m/z or intensity values). The encoder applies the Numpress compression algorithm, which exploits the typical properties of mass-spectrometry data (small differences between consecutive m/z values, intensity distributions). Pass the raw array to the encoder method, which returns a compressed byte stream. Validate the encoding by immediately performing a round-trip: decode the byte stream back into floating-point values and compare the result against the original array element-wise, confirming that all values match within machine precision (typically ≤ 1e-6 relative error for 32-bit floats). This round-trip test ensures both encoder and decoder correctness before committing compressed data to downstream storage or transmission.

## Related tools

- **OpenMS** (C++ library providing MSNumpressCoder encoder and decoder classes for Numpress compression of mass-spectrometry numeric arrays) — https://github.com/OpenMS/OpenMS
- **KNIME** (Workflow engine for integrating OpenMS tools, including Numpress-encoded data, into reproducible analysis pipelines)
- **pyOpenMS** (Python bindings to OpenMS C++ API, enabling Numpress encoding/decoding in Python-based mass-spectrometry workflows) — https://github.com/OpenMS/OpenMS

## Evaluation signals

- Round-trip validation: decoded array values are identical to the original m/z or intensity array within floating-point machine precision (≤ 1e-6 relative tolerance for 32-bit floats)
- Byte stream is non-empty and smaller than the original uncompressed array (typical compression ratio 3–5× for m/z arrays with close spacing)
- All unit test fixtures from OpenMS MSNumpressCoder_test.cpp pass without errors
- Encoded data can be successfully decoded by the corresponding MSNumpressCoder decoder without exceptions or data corruption
- Compression is deterministic: encoding the same input array twice produces byte-identical output

## Limitations

- Numpress compression is lossy; original floating-point values cannot be recovered bit-for-bit, though precision loss is typically << 1 ppm (suitable for most MS applications)
- Compression ratio depends on input data characteristics (e.g., regularly spaced m/z values compress better than irregular ones); sparse or highly variable intensity arrays may compress poorly
- Performance scales linearly with array size; very large spectra (>100k peaks per spectrum) may introduce latency in real-time workflows
- Decoder output precision is limited by the original bit depth and Numpress algorithm design; users should not expect sub-ppm accuracy for m/z values unless the input data was originally acquired at that precision

## Evidence

- [other] MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays: "MSNumpressCoder is a component in OpenMS that handles encoding and decoding of m/z and intensity numeric arrays, with validation performed through test fixtures located in the OpenMS test suite."
- [other] Implement the MSNumpressCoder encoder to compress m/z and intensity arrays using the Numpress compression algorithm: "Implement the MSNumpressCoder encoder to compress m/z and intensity arrays using the Numpress compression algorithm."
- [other] Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision: "Execute round-trip validation: encode a test array, then decode the result and compare the decoded values against the original input array for numerical equality within machine precision."
- [readme] OpenMS is free software available under the three-clause BSD license and offers integration into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept: "It supports easy integration of OpenMS built tools into workflow engines like nextflow, KNIME, Galaxy, and TOPPAS via the TOPPTools concept"
- [readme] OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development: "With pyOpenMS, OpenMS offers Python bindings to a large part of the OpenMS API to enable rapid algorithm development."
