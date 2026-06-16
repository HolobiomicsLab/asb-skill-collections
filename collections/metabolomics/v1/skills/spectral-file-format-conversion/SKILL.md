---
name: spectral-file-format-conversion
description: Use when when importing raw mass spectrometry data from instrument vendors or public repositories in one format (e.g., mzML, mzXML) and needing to export it in another format (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - pytest
  - Python
derived_from:
- doi: 10.21105/joss.02411
  title: matchms
evidence_spans:
- Matchms offers an array of tools for metadata cleaning and validation
- Matchms is a versatile open-source Python package developed for importing, processing, cleaning, and comparing mass spectrometry data
- make sure the existing tests still work by running ``pytest``
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms
    doi: 10.21105/joss.02411
    title: matchms
  dedup_kept_from: coll_matchms
schema_version: 0.2.0
---

# spectral-file-format-conversion

## Summary

Convert mass spectrometry spectral data between multiple file formats (mzML, mzXML, msp, MGF, JSON, metabolomics-USI) to enable interoperability across analysis pipelines and ensure compatibility with downstream processing tools.

## When to use

When importing raw mass spectrometry data from instrument vendors or public repositories in one format (e.g., mzML, mzXML) and needing to export it in another format (e.g., MGF, JSON) for compatibility with subsequent matchms processing, similarity comparisons, or external tools that require a specific spectral data format.

## When NOT to use

- When source and target formats are already compatible with your downstream tools—conversion adds unnecessary computation and risk of data loss.
- When working exclusively within the matchms ecosystem and all tools accept the native Spectrum object format—in-memory processing is preferable to round-trip file conversions.
- When the source data is already in a vendor-proprietary format with complex instrument-specific metadata that may not be fully captured by matchms's supported schemas—consult vendor documentation first.

## Inputs

- Mass spectrometry spectral data in one of: mzML, mzXML, msp, metabolomics-USI, or MGF format
- Spectrum objects loaded into matchms after optional preprocessing

## Outputs

- Mass spectrometry spectral data exported to target format (MGF, JSON, or other supported format)
- Converted spectral file ready for downstream analysis or tool integration

## How to apply

Use matchms's built-in spectrum import and export functions to read spectral data from a source format and write it to a target format. Matchms natively supports reading from mzML, mzXML, msp, metabolomics-USI, and MGF formats and can export to MGF and JSON. The conversion is applied after spectral data is loaded into matchms Spectrum objects, optionally after metadata cleaning and peak filtering steps. Verify format conversion integrity by confirming that key metadata fields (precursor m/z, retention time, instrument type) and peak intensity arrays are preserved across the conversion. Choose the target format based on downstream analysis needs: MGF and JSON are recommended for general matchms workflows, while mzML/mzXML preserve raw instrument data.

## Related tools

- **matchms** (Provides import/export functions for spectral file format conversion; supports reading from mzML, mzXML, msp, metabolomics-USI, MGF and exporting to MGF, JSON formats) — https://github.com/matchms/matchms
- **Python** (Programming language used to call matchms import/export APIs)

## Examples

```
from matchms.importing import load_from_mgf; from matchms.exporting import save_as_json; spectra = load_from_mgf('input.mgf'); save_as_json(spectra, 'output.json')
```

## Evaluation signals

- Verify that the output file is created in the target format and is readable by downstream tools or validators.
- Check that key metadata fields (precursor m/z, retention time, instrument type, scan number) are present and have expected values in the converted file—compare against the source file using spot checks.
- Confirm that peak intensity arrays and m/z values are numerically preserved (within floating-point precision) across the conversion.
- Run spectral validation on the output file to ensure no required metadata is missing and all spectra conform to the target format schema.
- Perform a round-trip conversion (A → B → A) and compare the final result to the original to detect lossy conversions or format-specific artifacts.

## Limitations

- Conversion may lose instrument-specific metadata not captured in the target format's schema; mzML and mzXML preserve more raw instrument data than MGF or JSON.
- Not all metadata fields in the source format may have direct equivalents in the target format; some fields may be dropped or truncated during export.
- Sparse or inconsistent metadata in the source file may cause validation errors or warnings during export; metadata cleaning and validation should be applied before conversion.
- Performance scales with file size; conversion of very large spectral datasets (hundreds of thousands of spectra) may require memory optimization or batch processing.

## Evidence

- [readme] The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON.: "The software supports a range of popular spectral data formats, including mzML, mzXML, msp, metabolomics-USI, MGF, and JSON"
- [readme] Matchms facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data.: "It facilitates the implementation of straightforward, reproducible workflows, transforming raw data from common mass spectra file formats into pre- and post-processed spectral data"
- [other] Raw spectral data can be imported from public MGF or MSP files and exported after processing to MGF or JSON format.: "Import spectral data from a public MGF or MSP file using matchms Python package...Export the cleaned spectrum collection to an output file (MGF or JSON format)"
