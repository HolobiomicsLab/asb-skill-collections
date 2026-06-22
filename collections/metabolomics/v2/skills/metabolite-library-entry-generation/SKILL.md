---
name: metabolite-library-entry-generation
description: Use when you have an experimental MS/MS spectrum (from MassBank or your own acquisition) and need to create a standardized library entry with ranked fragment ions for use in MetaboAnnotatoR or other fragment-based annotation pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - R
  - MassBank
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
---

# metabolite-library-entry-generation

## Summary

Convert experimental MS/MS spectra into annotated metabolite library entries by applying peak detection thresholds, noise filtering, and fragment ion scoring. This skill is essential for building custom fragment databases that enable downstream metabolite annotation of LC–MS All-ion fragmentation datasets.

## When to use

You have an experimental MS/MS spectrum (from MassBank or your own acquisition) and need to create a standardized library entry with ranked fragment ions for use in MetaboAnnotatoR or other fragment-based annotation pipelines. Specifically, use this skill when you want to curate high-confidence metabolite identities with explicit fragment peak annotations and scoring.

## When NOT to use

- Input spectrum is already in profile mode (not centroid); genFragEntry requires centroid-mode data.
- You have a pre-existing, validated library (e.g., LipidPos) and only need to annotate features; use annotateRC instead.
- MS/MS spectrum has very low signal-to-noise ratio or insufficient fragmentation; the resulting library entry will contain few confident peaks.

## Inputs

- Centroid-mode MS/MS spectrum (raw or from MassBank accession, e.g. MSBNK-RIKEN-PR100295)
- Metabolite name (string)
- Adduct type (string, e.g. '[M+H]+')
- Accurate adduct m/z (numeric)
- Output filename (string, CSV format)

## Outputs

- Metabolite library entry file (CSV format with columns: metabolite identifier, accurate mass, fragment m/z, occurrence score, and adduct annotation)
- Peak detection and scoring summary (included in exported CSV)

## How to apply

Load the centroid-mode MS/MS spectrum into R and invoke the genFragEntry function with explicit metabolite metadata (name, adduct type, accurate adduct m/z) and default peak-picking parameters: noise=0.005 (absolute intensity floor), mpeaksThres=0.1 (relative intensity threshold as fraction of base peak), mpeaksScore=0.9 (confidence score for peaks above threshold), and mzTol=0.01 (m/z tolerance in Da for peak grouping). The function attributes occurrence scores to peaks exceeding the mpeaksThres threshold and noise level, then exports a CSV file containing metabolite identifier, accurate mass, and annotated fragment m/z values with their scores. Verify the output by inspecting the CSV schema (must include metabolite name, adduct, m/z, and fragment annotations) and confirming that the number of detected fragments and their m/z values are consistent with known fragmentation pathways for the target metabolite.

## Related tools

- **MetaboAnnotatoR** (R package containing genFragEntry function for converting MS/MS spectra to library entries and annotateRC for downstream feature annotation) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment (version 4.5.0 or higher) required to execute genFragEntry)
- **MassBank** (Public repository for retrieving reference MS/MS spectra (e.g., accession MSBNK-RIKEN-PR100295 for D-Pantothenic Acid [M+H]+))

## Examples

```
genFragEntry(spectrum_data, metabolite_name='D-Pantothenic Acid', adduct_name='[M+H]+', accurate_mz=220.1205, noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01, output_file='pantothenic_acid_library.csv')
```

## Evaluation signals

- CSV output file is generated and contains all required columns: metabolite name, accurate m/z, fragment m/z values, and occurrence scores.
- Number of detected fragments and their m/z values match expected fragmentation pathways for the target metabolite (manual inspection or literature comparison).
- All peaks in the output exceed the noise threshold (0.005) and mpeaksThres threshold (0.1 relative intensity).
- Occurrence scores assigned to fragments fall within expected range (0–1 or 0–0.9 depending on mpeaksScore parameter); peaks below threshold receive no score.
- m/z values are reported to consistent precision (typically ≥4 decimal places) and fall within the biological m/z range (50–2000 Da typical for small metabolites).

## Limitations

- Function requires strictly centroid-mode spectra; profile-mode input will produce erroneous peak detection.
- Default parameters (noise=0.005, mpeaksThres=0.1, mzTol=0.01) may require tuning for non-standard acquisition methods or instrument calibration drift.
- Library entries generated from a single spectrum lack redundancy; multiple replicates are recommended for robust annotation performance.
- Output CSV is a single-metabolite entry; batch processing of many spectra requires external iteration logic in R.
- The function does not automatically assign chemical structures or reaction mechanisms to fragments; annotation of fragment origins requires manual curation or external databases.

## Evidence

- [other] genFragEntry converts MS/MS spectra to library entries: "The genFragEntry function converts MS/MS spectra into library entries by attributing occurrence scores to peaks above the mpeaksThres threshold and noise level"
- [other] Default parameters for peak detection and scoring: "using default parameters: noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1, and mzTol=0.01, with metabolite name, adduct name, accurate adduct m/z, and output filename explicitly specified"
- [other] Example workflow: retrieve spectrum, load into R, invoke genFragEntry, export CSV: "Retrieve the D-Pantothenic Acid [M+H]+ fragmentation spectrum from MassBank (accession MSBNK-RIKEN-PR100295). Load the spectrum data into R and invoke the genFragEntry function with default"
- [readme] Centroid-mode requirement in README: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [readme] Vignette describes library entry generation from spectra: "Generation of Metabolite fragment database entry from MS/MS experimental spectra."
