---
name: ionization-mode-annotation
description: Use when when converting MS/MS spectra from .msp format library files (e.g., MassBank) into a custom fragment library for metabolite annotation, and the source spectra are tagged with ionization mode information (positive or negative).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MetaboAnnotatoR
  - R
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
---

# ionization-mode-annotation

## Summary

Annotate MS/MS spectra library entries with positive or negative ionization mode suffixes during conversion from .msp files to individual CSV library entries. This facilitates organization and retrieval of metabolite fragment libraries for LC-MS All-ion fragmentation (AIF) annotation workflows.

## When to use

When converting MS/MS spectra from .msp format library files (e.g., MassBank) into a custom fragment library for metabolite annotation, and the source spectra are tagged with ionization mode information (positive or negative). Use this skill to preserve mode specificity in library file organization, ensuring that downstream annotation matching does not conflate spectra from different ionization modes.

## When NOT to use

- Source .msp file lacks ionization mode metadata or mode designation is ambiguous for some spectra.
- Library entries are already in CSV format or custom binary format — the mspToLib function is designed specifically for .msp input.
- Downstream annotation workflow does not require mode-specific matching or uses a single global ionization mode across all features.

## Inputs

- .msp library file containing MS/MS spectra with ionization mode metadata (e.g., MassBank_example.msp from MetaboAnnotatoR package)
- peak-picking parameters (noise, mpeaksScore, mpeaksThres)
- target output directory path

## Outputs

- Individual CSV library entries, one per spectrum, with mode-specific file name suffixes (e.g., spectrum_001_positive.csv, spectrum_002_negative.csv)
- Per-spectrum CSV records containing m/z, intensity, and occurrence scores for peaks above noise and marker peak thresholds

## How to apply

During .msp to CSV library conversion using the mspToLib function, apply default peak-picking parameters (noise threshold 0.005, marker peaks score 0.9, marker peaks threshold 0.1) to filter peaks above noise and assign occurrence scores to marker peaks. For each spectrum record, append a mode-specific suffix ('positive' or 'negative') to the output CSV file name. This suffix encoding allows the annotation engine to later match experimental features to mode-appropriate library spectra. Verify that all output CSV files carry the correct mode designation and that spectral annotations (m/z, intensity, occurrence scores) are complete and meet the threshold criteria.

## Related tools

- **MetaboAnnotatoR** (R package containing the mspToLib function for conversion of .msp spectral libraries to mode-annotated CSV entries) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment; requires version 4.5.0 or higher to execute mspToLib)

## Examples

```
library(MetaboAnnotatoR); mspToLib(mspFile='MassBank_example.msp', libDir='./custom_lib', noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)
```

## Evaluation signals

- All output CSV file names contain either '_positive' or '_negative' suffix matching the source spectrum ionization mode metadata.
- Each CSV record includes m/z and intensity columns with occurrence scores assigned only to peaks above noise threshold (0.005) and marker peak threshold (0.1).
- Count of output CSV files equals count of spectrum records in input .msp file (no records dropped or duplicated).
- Spot-check: compare m/z values and intensities in 2–3 randomly selected CSV entries against the corresponding records in the source .msp file to confirm accurate transcription.
- Verify that marker peaks with occurrence scores ≥ mpeaksScore threshold (0.9) are present and that low-intensity peaks below mpeaksThres (0.1) are filtered out or marked as non-marker.

## Limitations

- The mspToLib function requires .msp input in a specific format; malformed or non-standard .msp files may fail to parse or produce incomplete CSV output.
- Mode suffix assignment relies on explicit ionization mode metadata in the .msp file; spectra without mode designation will not receive a suffix, potentially breaking downstream mode-aware matching.
- No automated validation or changelog is provided in the package; version history and updates are not documented, making it difficult to track changes or known issues across releases.
- The default peak-picking thresholds (noise=0.005, mpeaksThres=0.1) may not be optimal for all instrument types or mass ranges; threshold tuning may be necessary for non-standard datasets.

## Evidence

- [other] The mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file name: "The mspToLib function reads and converts spectra records from .msp files into CSV library entries stored in a user-defined directory, with a 'positive' or 'negative' mode suffix added to each file"
- [other] occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters: "occurrence scores are attributed to peaks above mpeaksThres threshold and noise level using default parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1)"
- [readme] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [readme] Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format): "Generation of Metabolite fragment database entry from MS/MS spectra from public databases (in .msp format)"
