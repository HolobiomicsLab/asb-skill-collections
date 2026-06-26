---
name: mass-spectrometry-file-format-conversion
description: Use when you have raw MS data files in vendor-native format (.raw, .d,
  .ms) from CE-MS or LC-MS instruments and need to process them through AriumMS or
  other open-source metabolomics pipelines that require standardized XML-based interchange
  formats.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3649
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - msconvert
  - ProteoWizard
  - AriumMS
  - IsoFusion
  - MSConvert
  - Excalibur
  - LSG
  - Skyline
  techniques:
  - LC-MS
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s00216-023-04715-6
  title: AriumMS
- doi: 10.26599/bdma.2024.9020059
  title: ''
- doi: 10.1021/acs.analchem.2c04518
  title: ''
evidence_spans:
- For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed
  with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project
- msconvert, distributed with the ProteoWizard Project http://proteowizard.sourceforge.net/download.html
- github.com__xfcui__IsoFusion
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
- https://github.com/98104781/LSG/releases/tag/v1.3.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ariumms_cq
    doi: 10.1007/s00216-023-04715-6
    title: AriumMS
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_ariumms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-023-04715-6
  all_source_dois:
  - 10.1007/s00216-023-04715-6
  - 10.26599/bdma.2024.9020059
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-file-format-conversion

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert raw mass spectrometry data from vendor-native formats (.raw, .d, .ms) to open, standardized .mzXML or .mzML formats using msconvert, enabling downstream processing by untargeted metabolomics workflows such as AriumMS. This conversion is a mandatory prerequisite for multi-platform CE-MS and LC-MS data integration.

## When to use

You have raw MS data files in vendor-native format (.raw, .d, .ms) from CE-MS or LC-MS instruments and need to process them through AriumMS or other open-source metabolomics pipelines that require standardized XML-based interchange formats. The conversion must occur before ROI extraction, preprocessing, or data augmentation steps.

## When NOT to use

- Your MS data is already in .mzXML or .mzML format — conversion is redundant.
- Your downstream workflow accepts vendor-native formats directly (rare; most open-source tools require standardized formats).
- You lack the ProteoWizard suite installation or permission to run msconvert on your system.

## Inputs

- Raw mass spectrometry data file (vendor-native format: .raw, .d, .ms)
- CE-MS or LC-MS instrument output

## Outputs

- .mzXML file
- .mzML file

## How to apply

Run msconvert (distributed with ProteoWizard) with the output format flag set to either .mzXML or .mzML, applying default centroiding and compression settings appropriate for your data type (CE-MS or LC-MS). After conversion, validate that output files are well-formed XML, contain expected metadata fields (scan count, mass range, retention time range), and match the input file count. The choice between .mzXML and .mzML is determined by your downstream tool's requirements; both are valid open formats. Centroiding reduces file size and noise while preserving peak information necessary for region-of-interest detection.

## Related tools

- **msconvert** (Primary tool for converting raw MS data to standardized .mzXML or .mzML formats with configurable centroiding and compression) — http://proteowizard.sourceforge.net/download.html
- **ProteoWizard** (Suite containing msconvert; distributes the conversion tool) — http://proteowizard.sourceforge.net/download.html
- **AriumMS** (Downstream untargeted metabolomics workflow that consumes converted .mzXML or .mzML files for ROI extraction and data augmentation) — https://github.com/AdrianHaun/AriumMS

## Examples

```
msconvert input_raw_file.raw --mzML --zlib --filter "peakPicking vendor msLevel=1-"  # Converts .raw to .mzML with zlib compression and vendor centroiding
```

## Evaluation signals

- Output files are well-formed XML and parse without schema validation errors.
- Output .mzXML or .mzML files contain non-empty metadata fields: scan count > 0, mass range min and max are numerically sensible for the instrument and analysis, retention time range reflects expected chromatographic window.
- File conversion completes without error messages or warnings from msconvert.
- Number of output files matches number of input files (1:1 conversion).
- File size of converted .mzXML or .mzML is smaller than raw input (compression applied) but contains all scans and peaks.

## Limitations

- Vendor-specific metadata embedded in raw files may be lost or degraded during conversion to open formats; check that critical instrument parameters (ionization mode, analyzer type, resolution settings) are preserved in the converted file.
- msconvert requires the ProteoWizard suite to be installed and may not support all vendor formats; consult ProteoWizard documentation for supported input types.
- Centroiding settings (default vs. user-specified) affect downstream peak detection sensitivity and should be documented for reproducibility.
- Large raw files (>1 GB) may require extended conversion time; batch processing should use appropriate parallelization or scheduling.

## Evidence

- [other] Raw MS data must be converted to .mzXML or .mzML file format using msconvert: "For MS Data conversion to .mzXML or .mzML file format use msconvert, distributed with the ProteoWizard Project"
- [other] Workflow step: obtain raw MS data in vendor-native format: "Obtain raw MS data files in vendor-native format (e.g., .raw, .d, .ms) from CE-MS or LC-MS instruments."
- [other] Workflow step: run msconvert with output format and centroiding settings: "Run msconvert (ProteoWizard) with output format set to .mzXML or .mzML, applying default centroiding and compression settings as appropriate for the data type."
- [other] Validation step: verify converted files contain expected metadata: "Verify converted files are valid .mzXML or .mzML and contain expected metadata (scan count, mass range, retention time range)."
- [readme] AriumMS requires converted .mzXML or .mzML as input: "All in one tool for untargeted Metabolomics by ROI and augmentation of multiple Data sets."
