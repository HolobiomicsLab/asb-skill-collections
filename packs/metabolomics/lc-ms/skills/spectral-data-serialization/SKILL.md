---
name: spectral-data-serialization
description: Use when after completing MS/MS spectra detection and peak recognition on tandem MS breath samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - BreathXplorer
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/jasms.4c00152
  title: BreathXplorer
evidence_spans:
- '[![PyPI](https://img.shields.io/pypi/pyversions/breathXplorer)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_breathxplorer_cq
    doi: 10.1021/jasms.4c00152
    title: BreathXplorer
  dedup_kept_from: coll_breathxplorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00152
  all_source_dois:
  - 10.1021/jasms.4c00152
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-serialization

## Summary

Export detected MS/MS spectra from feature extraction and peak recognition pipelines to MGF (Mascot Generic Format) files for downstream spectral analysis and compound identification. This skill encodes precursor m/z, charge state, retention time, and fragment ion peaks into a standardized text format suitable for spectral library matching and metabolomics workflows.

## When to use

Apply this skill after completing MS/MS spectra detection and peak recognition on tandem MS breath samples. Use when you have FeatureSet or Sample objects from BreathXplorer's find_feature() or merge_result() pipelines and need to export spectral data in a portable, standards-compliant format compatible with spectral matching tools and databases.

## When NOT to use

- Input contains only MS1 feature data without tandem MS/MS spectra — MGF format requires MS2-level spectral data.
- Output destination is a database or binary format — MGF is text-based and designed for file exchange, not for in-memory or database serialization.
- Spectral data is already in another standardized format (e.g., mzML, mzXML) and no format conversion or filtering is needed.

## Inputs

- FeatureSet object (from find_feature) with tandem MS/MS spectral data attached
- Sample object (from merge_result) with aligned features and associated spectra
- mzML or mzXML file path containing raw MS/MS acquisitions

## Outputs

- MGF file (Mascot Generic Format) with formatted MS/MS spectra
- Text file with BEGIN IONS / END IONS sections, PEPMASS, MSLEVEL, and m/z–intensity pairs

## How to apply

Call the to_mgf() function on a FeatureSet or Sample object, passing a path to the output MGF file. The function iterates over detected MS/MS spectra, formats each spectrum with required MGF fields (precursor m/z as PEPMASS, MS level as MSLEVEL=2, and fragment ion m/z–intensity pairs), wraps each spectrum in BEGIN IONS / END IONS delimiters, and writes all entries to a single text file. Validate the output by verifying that: (1) every BEGIN IONS block has a matching END IONS block; (2) every spectrum contains at least one PEPMASS field and one fragment peak pair; (3) m/z and intensity values are numeric and non-negative; (4) the file parses without syntax errors in downstream spectral matching software.

## Related tools

- **BreathXplorer** (Python package providing to_mgf() function to serialize MS/MS spectra and retrieve_tandem() to load tandem MS data) — https://github.com/wykswr/breathXplorer
- **Python** (Runtime environment for executing BreathXplorer's to_mgf() utility and file I/O operations)

## Examples

```
from breathXplorer import retrieve_tandem; retrieve_tandem("sample.mzML").to_mgf("spectra.mgf")
```

## Evaluation signals

- Output file is valid MGF syntax: every BEGIN IONS has a matching END IONS, no malformed delimiters or unclosed sections.
- Every spectrum record contains a PEPMASS field with a numeric m/z value and MSLEVEL=2 marker.
- Fragment ion pairs (m/z intensity) are present for each spectrum and consist of two numeric values per line.
- All m/z and intensity values are non-negative floats; no NaN, Inf, or missing values in peak lists.
- File can be successfully parsed by downstream spectral matching tools (e.g., MASCOT, X!Tandem, or open-source MGF parsers).

## Limitations

- MGF format does not preserve retention time metadata in a standardized field; retention time may be lost or stored in custom annotations depending on the exporting tool and downstream parser expectations.
- Charge state is not explicitly encoded in the MGF standard; precursor charge inference must be handled by downstream spectral matching software.
- Large datasets with many spectra may produce very large MGF files with poor random-access performance; alternative binary formats (mzML, HDF5) are better suited for high-volume data.
- MGF does not support metadata about sample origin, instrument configuration, or quality metrics; these must be tracked separately in documentation or metadata files.

## Evidence

- [readme] If you're using tandem MS, you can also export the MS/MS spectra as mgf file using the `to_mgf` function: "If you're using tandem MS, you can also export the MS/MS spectra as mgf file using the `to_mgf` function"
- [readme] The file contains the MS/MS spectra of the features, each feature has a PEPMASS (precursor mass) and MSLEVEL field, and the following pairs are the m/z and intensity of the MS/MS spectra.: "The file contains the MS/MS spectra of the features, each feature has a PEPMASS (precursor mass) and MSLEVEL field, and the following pairs are the m/z and intensity of the MS/MS spectra."
- [other] Format each spectrum entry with required MGF fields: precursor m/z, precursor charge, retention time, and fragment ion peaks (m/z and intensity pairs).: "Format each spectrum entry with required MGF fields: precursor m/z, precursor charge, retention time, and fragment ion peaks (m/z and intensity pairs)."
- [other] Write all formatted spectra to a single MGF file with proper header and section delimiters.: "Write all formatted spectra to a single MGF file with proper header and section delimiters."
- [other] Validate MGF syntax and verify all spectra contain required fields.: "Validate MGF syntax and verify all spectra contain required fields."
