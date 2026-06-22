---
name: spectral-data-preprocessing
description: Use when you have raw or processed MS spectrum data (mz/intensity pairs) from direct-injection MS (DI-MS), ASAP-MS, or other ambient ionization instruments (AI-MS, LDI-MS), and you need to identify peaks of interest, assign confidence scores, and prepare the data for database matching or species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-data-preprocessing

## Summary

Spectral data preprocessing transforms raw or processed mass spectrometry spectra (m/z and intensity pairs) into cleaned, annotated datasets suitable for downstream analysis. This skill integrates loading, peak detection, labeling, and result aggregation into a structured output table for species authentication and metabolite identification workflows.

## When to use

Apply this skill when you have raw or processed MS spectrum data (mz/intensity pairs) from direct-injection MS (DI-MS), ASAP-MS, or other ambient ionization instruments (AI-MS, LDI-MS), and you need to identify peaks of interest, assign confidence scores, and prepare the data for database matching or species discrimination without manual peak curation.

## When NOT to use

- Input data are already processed into a peak feature table with confidence annotations — skip to database matching.
- The analysis goal is exploratory visualization only and does not require quantitative peak identification or scoring.
- Data originate from instruments or file formats not supported by RapidMass (e.g., proprietary formats without a documented converter).

## Inputs

- raw MS spectrum data (m/z and intensity pairs)
- processed MS spectrum data
- input files from DI-MS, ASAP-MS, AI-MS, or LDI-MS instruments

## Outputs

- structured peak table with peak identifiers, m/z values, intensities, and confidence scores
- annotated MS spectrum
- preprocessed data ready for database matching

## How to apply

Load the raw or processed MS spectrum data as m/z and intensity pairs from an input file format compatible with RapidMass. Apply the RapidMass automatic peak detection algorithm to identify peaks of interest across the full mass range, using intensity ranking and m/z value thresholds as the basis for selection. Assign labels and annotations to detected peaks, incorporating confidence scores derived from the detection algorithm. Aggregate the results into a structured output table containing peak identifiers, m/z values, intensities, and confidence scores. This preprocessing prepares the spectrum for downstream database search algorithms and visual discrimination workflows.

## Related tools

- **RapidMass** (Primary tool for automatic peak detection, annotation, and preprocessing workflow integration) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct-injection mass spectrometry instrument supported for raw data acquisition)
- **ASAP-MS** (Ambient sampling atmospheric pressure mass spectrometry instrument supported for raw data acquisition)

## Evaluation signals

- All detected peaks have assigned m/z values, intensity measurements, and confidence scores with no missing values in the output table.
- Peak identifiers are unique and consistently indexed; no duplicate peak entries exist in the aggregate result.
- Confidence scores fall within a defined range (e.g., 0–1 or 0–100) and correlate positively with peak intensity ranking.
- The output table schema matches the documented RapidMass format (peak ID, m/z, intensity, confidence); metadata such as source file and preprocessing timestamp are preserved.
- Visual inspection of annotated peaks aligns with expected metabolite or authentication markers for the sample type (e.g., plant species markers in botanical authentication workflows).

## Limitations

- Performance depends on spectrum quality and signal-to-noise ratio; low-intensity peaks may be missed if noise thresholds are not tuned to the instrument and sample type.
- Automatic peak detection may produce false positives in crowded m/z regions or false negatives for closely spaced isotope clusters; manual review is recommended for high-stakes applications.
- The skill assumes input files are in a format compatible with RapidMass; unsupported instrument formats or corrupted data will cause preprocessing to fail.
- No changelog is available for RapidMass, limiting reproducibility and traceability of algorithm updates across software versions.
- Performance validation reported in the literature used easily confused plant materials; applicability to other sample types (e.g., synthetic compounds, environmental mixtures) is not explicitly confirmed.

## Evidence

- [other] Load raw or processed MS spectrum data (mz/intensity pairs) from input file. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. Assign labels and annotations to detected peaks based on intensity ranking and m/z values. Aggregate results into a structured output table with peak identifiers, m/z, intensity, and confidence scores.: "1. Load raw or processed MS spectrum data (mz/intensity pairs) from input file. 2. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. 3. Assign labels"
- [intro] integrates data pre-processing, analysis, and evaluation: "integrates data pre-processing, analysis, and evaluation"
- [readme] software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS: "the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS"
- [readme] Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be tried with this software.: "Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be"
- [readme] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
