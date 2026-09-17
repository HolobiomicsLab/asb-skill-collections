---
name: vendor-data-standardization
description: Use when you have raw MS data files directly from a vendor instrument
  (Thermo .raw, Agilent .d, Waters .ms, etc.) and need to process them through AriumMS
  or any other metabolomics pipeline that accepts only .mzXML or .mzML formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3643
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - msconvert
  - ProteoWizard
  - AriumMS
  techniques:
  - LC-MS
  - CE-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
evidence_spans:
- For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed
  with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project http://proteowizard.sourceforge.net/download.html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ariumms_cq
    doi: 10.1007/s00216-023-04715-6
    title: AriumMS
  dedup_kept_from: coll_ariumms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-04715-6
  all_source_dois:
  - 10.1007/s00216-023-04715-6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# vendor-data-standardization

## Summary

Convert raw mass spectrometry data from vendor-native binary formats (.raw, .d, .ms) to open, XML-based standards (.mzXML or .mzML) to enable interoperable downstream metabolomics processing. This standardization is a mandatory prerequisite for untargeted metabolomics workflows that require platform-agnostic data handling across CE-MS and LC-MS instruments.

## When to use

Apply this skill when you have raw MS data files directly from a vendor instrument (Thermo .raw, Agilent .d, Waters .ms, etc.) and need to process them through AriumMS or any other metabolomics pipeline that accepts only .mzXML or .mzML formats. This is the first step before any ROI detection, preprocessing, or data augmentation in untargeted metabolomics analyses.

## When NOT to use

- Input data is already in .mzXML or .mzML format — conversion is redundant.
- Your downstream tool natively supports vendor formats or has its own internal converter — use that instead to avoid transcoding artifacts.
- You require preservation of vendor-specific metadata (e.g., Thermo tune file, calibration constants) not exported by msconvert — consider archiving the original alongside the standard format.

## Inputs

- Raw MS data in vendor-native binary formats (.raw, .d, .ms, or equivalent from CE-MS or LC-MS instruments)

## Outputs

- .mzXML or .mzML files with centroided data, metadata tags, and compression applied

## How to apply

Run msconvert (ProteoWizard) on each raw vendor-format file, specifying .mzXML or .mzML as the output format and applying default centroiding and compression settings appropriate to your data type (e.g., profile vs. centroid mode). After conversion, validate that each output file contains expected metadata: scan count matching the source file, mass-to-charge range consistent with your instrument and method, and retention time range aligned with your chromatographic gradient. Verify file integrity by confirming the .mzXML or .mzML structure is well-formed (schema-compliant) before proceeding to AriumMS or downstream analysis.

## Related tools

- **msconvert** (Command-line tool that performs the actual conversion from vendor-native MS formats to .mzXML/.mzML, with control over centroiding, compression, and output metadata.) — http://proteowizard.sourceforge.net/download.html
- **ProteoWizard** (Software suite that distributes msconvert and provides the underlying library for multi-format MS file I/O and standardization.) — http://proteowizard.sourceforge.net/download.html
- **AriumMS** (Downstream untargeted metabolomics tool that requires .mzXML or .mzML input; serves as the primary consumer of the standardized format produced by this skill.) — https://github.com/AdrianHaun/AriumMS

## Examples

```
msconvert input.raw --mzML --zlib --filter "peakPicking true 1-" --output output.mzML
```

## Evaluation signals

- Output file is valid .mzXML or .mzML (XML well-formedness check via xmllint or Python xml.etree parser succeeds without parse errors).
- Scan count in the converted file matches the scan count reported by the vendor software for the original raw file.
- Mass-to-charge range (min m/z, max m/z) in the .mzML/XML header is consistent with instrument mass range and the method configuration.
- Retention time range spans the expected chromatographic window (e.g., 0–30 min for a 30 min LC method).
- AriumMS successfully reads the converted file and initiates ROI search without file format errors.

## Limitations

- msconvert does not preserve all vendor-proprietary metadata (e.g., instrument tune files, source-specific calibration constants); if such metadata is critical, archive the original vendor file alongside the standard format.
- Centroiding and compression settings in msconvert affect data fidelity; default parameters may not be optimal for all MS methods (e.g., high-resolution vs. low-resolution, profile vs. centroid acquisition). Review and test settings for your specific instrument and analyte class.
- Not all vendor formats are equally well supported by ProteoWizard; rare or new instrument formats may have incomplete converters or require custom build steps. Consult ProteoWizard documentation for your instrument vendor.
- File size can increase or decrease depending on compression codec chosen; verify storage capacity and I/O performance before batch-converting large cohorts.

## Evidence

- [other] Raw MS data must be converted to .mzXML or .mzML file format using msconvert, a tool distributed with the ProteoWizard Project, as a prerequisite for AriumMS processing.: "Raw MS data must be converted to .mzXML or .mzML file format using msconvert, a tool distributed with the ProteoWizard Project, as a prerequisite for AriumMS processing."
- [other] Obtain raw MS data files in vendor-native format (e.g., .raw, .d, .ms) from CE-MS or LC-MS instruments. Run msconvert (ProteoWizard) with output format set to .mzXML or .mzML, applying default centroiding and compression settings as appropriate for the data type.: "Obtain raw MS data files in vendor-native format (e.g., .raw, .d, .ms) from CE-MS or LC-MS instruments. Run msconvert (ProteoWizard) with output format set to .mzXML or .mzML, applying default"
- [other] Verify converted files are valid .mzXML or .mzML and contain expected metadata (scan count, mass range, retention time range).: "Verify converted files are valid .mzXML or .mzML and contain expected metadata (scan count, mass range, retention time range)."
- [readme] For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
