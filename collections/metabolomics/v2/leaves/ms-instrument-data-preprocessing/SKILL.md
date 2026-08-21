---
name: ms-instrument-data-preprocessing
description: Use when you have raw mass spectrometry data files from a mass spectrometer
  instrument and need to feed them into a peptide feature detection pipeline (e.g.,
  IsoFusion) that accepts only MS1 format input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSConvert
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.26599/bdma.2024.9020059
  title: IsoFusion
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isofusion_cq
    doi: 10.26599/bdma.2024.9020059
    title: IsoFusion
  dedup_kept_from: coll_isofusion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.26599/bdma.2024.9020059
  all_source_dois:
  - 10.26599/bdma.2024.9020059
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-instrument-data-preprocessing

## Summary

Convert raw mass spectrometry instrument output files to standardized MS1 format as a mandatory preprocessing step before peptide feature detection or mass spectrum analysis. This skill ensures compatibility with downstream deep learning models and feature prediction pipelines.

## When to use

You have raw mass spectrometry data files from a mass spectrometer instrument and need to feed them into a peptide feature detection pipeline (e.g., IsoFusion) that accepts only MS1 format input. This conversion is required before any downstream analysis of charge, isotope patterns, or retention time prediction.

## When NOT to use

- Your input data is already in MS1 or mzML format — the conversion step is redundant.
- You are working with downstream analysis outputs (e.g., feature tables, peptide identifications) — this skill applies only to raw instrument data.
- Your analysis pipeline accepts vendor-native raw formats directly — check tool documentation first.

## Inputs

- raw mass spectrometry data files (vendor-specific formats: .raw, .d, etc.)

## Outputs

- MS1 format mass spectrum file (centroided peak list)

## How to apply

Download and install MSConvert independently from the vendor's distribution. Configure MSConvert to output MS1 format (the centroided peak list representation). Execute MSConvert on your raw mass spectrometry file, specifying MS1 as the output format. Verify the resulting MS1 file is valid and contains expected scan data before proceeding to feature detection. The conversion process standardizes proprietary vendor formats (e.g., .raw, .d directories) into the portable, text-based MS1 format that downstream tools like IsoFusion expect as input.

## Related tools

- **MSConvert** (standalone format converter from vendor raw formats to MS1 centroided peak lists; must be downloaded and installed independently before use)

## Examples

```
# Assume MSConvert is installed and a raw file exists at ~/dataset/sample.raw
# (Note: exact invocation syntax varies by MSConvert version and platform; consult MSConvert documentation for your installation)
```

## Evaluation signals

- The output MS1 file is non-empty and contains valid scan headers and peak data.
- MS1 file structure conforms to the MS1 text format specification (scan number, precursor m/z, charge state, peak lists).
- The MS1 file can be successfully ingested by the downstream tool (e.g., IsoFusion) without parse errors.
- The number of scans in the output MS1 file is consistent with the input raw file's scan count.
- Peak intensities and m/z values are within physically reasonable ranges for the mass spectrometer used.

## Limitations

- MSConvert must be downloaded and installed separately by the user; it is not bundled with analysis tools.
- Conversion success depends on MSConvert's support for the specific vendor raw format and instrument type.
- MS1 format is lossy compared to vendor-native formats; metadata such as instrument settings or raw signal profiles may not be retained.

## Evidence

- [readme] You will need to convert your raw mass spectrometry files to MS1 format.: "You will need to convert your raw mass spectrometry files to MS1 format."
- [readme] The conversion tool can use MSConvert, which you need to download and install yourself.: "The conversion tool can use MSConvert, which you need to download and install yourself."
- [intro] Raw mass spectrometry files must be converted to MS1 format using MSConvert, which users must download and install independently before proceeding with IsoFusion analysis.: "Raw mass spectrometry files must be converted to MS1 format using MSConvert, which users must download and install independently"
- [intro] Execute MSConvert on the raw mass spectrometry file to convert it to MS1 format. Verify the output MS1 file is valid and ready for IsoFusion processing.: "Execute MSConvert on the raw mass spectrometry file to convert it to MS1 format. Verify the output MS1 file is valid"
