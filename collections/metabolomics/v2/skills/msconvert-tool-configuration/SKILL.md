---
name: msconvert-tool-configuration
description: Use when you have vendor-specific raw mass spectrometry data files (e.g., from Orbitrap, Q-TOF, or other MS instruments) and need to feed them into IsoFusion or other tools that require MS1 format as input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSConvert
  - IsoFusion
  techniques:
  - CE-MS
derived_from:
- doi: 10.26599/bdma.2024.9020059
  title: IsoFusion
evidence_spans:
- The conversion tool can use MSConvert, which you need to download and install yourself.
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

# MSConvert tool configuration

## Summary

Configure and execute MSConvert to convert raw mass spectrometry files into MS1 format, a prerequisite input format for downstream peptide feature detection tools like IsoFusion. This skill bridges vendor-specific raw formats and standardized MS1 text-based spectra.

## When to use

You have vendor-specific raw mass spectrometry data files (e.g., from Orbitrap, Q-TOF, or other MS instruments) and need to feed them into IsoFusion or other tools that require MS1 format as input. MS1 is the required format when you plan to use end-to-end deep learning models for peptide charge, isotope count, and retention time prediction.

## When NOT to use

- Your mass spectrometry data is already in MS1 or another supported text format (mzML, mzXML); conversion is redundant.
- You are using a tool that accepts raw format natively; check tool documentation before assuming MSConvert conversion is required.
- Your raw files are corrupted or from an instrument not supported by MSConvert; validation of raw file integrity is a prerequisite.

## Inputs

- vendor-specific raw mass spectrometry file (e.g., .raw, .d, .wiff)

## Outputs

- MS1 format text file (peak list with m/z, intensity, and scan metadata)

## How to apply

Download and install MSConvert independently (it is not bundled with downstream analysis tools). Configure MSConvert output settings to produce MS1 format—a text-based peak list format. Execute MSConvert on your raw mass spectrometry file, specifying the input raw file path and requesting MS1 as the output format. Verify that the resulting MS1 file is valid and non-empty before proceeding to downstream analysis (e.g., IsoFusion). The conversion step is mandatory because tools like IsoFusion expect pre-converted MS1 input and do not perform raw-format conversion internally.

## Related tools

- **MSConvert** (standalone command-line and GUI tool for format conversion from vendor-specific raw MS files to standardized MS1 text output)
- **IsoFusion** (downstream deep learning tool that consumes MS1-format input for end-to-end peptide feature detection) — https://github.com/xfcui/IsoFusion

## Examples

```
MSConvert is typically run via command line or GUI after independent installation; a representative invocation following conversion would be: `./run_IsoFusion.py --file ~/dataset/ms1/converted_file.ms1 --process_num 8 --gpu 0 --batch_size 256`
```

## Evaluation signals

- Output MS1 file exists, is non-empty, and contains valid peak list entries with m/z, intensity, and scan headers.
- MS1 file can be successfully parsed by downstream tools (e.g., IsoFusion) without format errors.
- Peak count and mass range in MS1 output are consistent with expectations from the raw file's instrument and acquisition method.
- No truncation, corruption, or data loss is evident when comparing scan count and total ion current (TIC) summaries between raw and MS1 formats.

## Limitations

- MSConvert must be downloaded and installed independently; it is not included with analysis tools and requires manual setup.
- Not all vendor raw formats are supported by MSConvert; compatibility depends on vendor libraries and ProteoWizard updates.
- MS1 format discards some metadata (e.g., instrument-specific tuning parameters); reproducibility of downstream predictions may depend on consistent MS1 configuration across datasets.

## Evidence

- [readme] You will need to convert your raw mass spectrometry files to MS1 format.: "You will need to convert your raw mass spectrometry files to MS1 format."
- [readme] The conversion tool can use MSConvert, which you need to download and install yourself.: "The conversion tool can use MSConvert, which you need to download and install yourself."
- [intro] Raw mass spectrometry files must be converted to MS1 format using MSConvert, which users must download and install independently before proceeding with IsoFusion analysis.: "Raw mass spectrometry files must be converted to MS1 format using MSConvert, which users must download and install independently before proceeding with IsoFusion analysis."
- [readme] our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum: "our model is an end-to-end model that can predict charge, number of isotopes and retention time directly from the mass spectrum"
