---
name: cross-instrument-data-harmonization
description: Use when you have mass spectrometry spectral data from multiple instrument types (e.g., direct infusion MS, ambient ionization MS, laser desorption/ionization MS) and need to perform unified species discrimination or database scoring across all samples regardless of their source instrument.
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
  - LDI-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
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

# cross-instrument-data-harmonization

## Summary

Enable unified analysis of mass spectrometry data across heterogeneous instrument platforms (DI-MS, ASAP-MS, LDI-MS, AI-MS) by standardizing file parsing, pre-processing, and peak detection workflows. This skill bridges instrumental differences to allow consistent species authentication and database searching without instrument-specific recalibration.

## When to use

You have mass spectrometry spectral data from multiple instrument types (e.g., direct infusion MS, ambient ionization MS, laser desorption/ionization MS) and need to perform unified species discrimination or database scoring across all samples regardless of their source instrument. The input files may be in vendor-native formats, mzML, or mzXML, and you want to avoid rebuilding analysis pipelines for each instrument.

## When NOT to use

- Input data has already been instrument-corrected or harmonized by a prior vendor-specific pipeline and you only need to apply final species classification.
- You require instrument-specific calibration or mass calibration workflows that depend on proprietary instrument metadata not present in standard file formats.
- The samples come from a single instrument type and reproducibility across instruments is not a study objective.

## Inputs

- Mass spectrometry spectral data files in mzML, mzXML, or native vendor formats from DI-MS, ASAP-MS, LDI-MS, or AI-MS instruments
- Ground-truth species labels or reference dataset for validation
- RapidMass database (user-created or built-in) for unknown sample scoring

## Outputs

- Harmonized peak detection results across all instruments
- Species authentication results and visual outputs for all samples
- Accuracy metrics and performance comparison across instrument types
- Database search scores for unknown samples regardless of source instrument

## How to apply

First, extend the file parser to recognize and load spectral formats from all target instruments (mzML, mzXML, or native vendor formats). Apply RapidMass's standard data pre-processing pipeline uniformly across all inputs: noise filtering and baseline correction to remove instrument-specific artifacts, followed by automatic peak detection using the shared peak detection algorithm. Then execute database search using RapidMass's available database search algorithms to score all samples on a common reference basis. Finally, compare authentication accuracy and peak patterns across instruments against a ground-truth reference dataset to validate that harmonization has not introduced systematic bias or loss of discriminatory power. The rationale is that standardizing pre-processing and peak detection parameters allows cross-instrument comparisons while preserving the chemical information needed for species identification.

## Related tools

- **RapidMass** (Primary software platform that integrates file parsing, data pre-processing, peak detection, database search, and cross-instrument harmonization for mass spectrometry species authentication) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry instrument type supported for harmonized data import and analysis)
- **ASAP-MS** (Ambient solid analysis probe mass spectrometry instrument type supported for harmonized data import and analysis)
- **LDI-MS** (Laser desorption/ionization mass spectrometry instrument type supported for harmonized data import and analysis)

## Evaluation signals

- All input files from different instruments are successfully parsed and loaded without format-specific errors.
- Pre-processed spectra show consistent noise floor and baseline levels across instruments after standard filtering and correction.
- Peak detection identifies the same discriminatory mass-to-charge ratios in replicate samples from different instruments with consistent peak intensity rankings.
- Database search scores for the same unknown sample are comparable or ranked consistently regardless of which instrument type generated the data.
- Accuracy metrics (e.g., species identification rate, cosine similarity to reference spectra) show no statistically significant degradation compared to instrument-specific baseline validation.

## Limitations

- Cross-instrument harmonization assumes that the underlying biochemical signatures are preserved across instrumental platforms; mass shift artifacts or resolution differences between instruments may still affect peak matching fidelity.
- User must provide or construct a reference database that is compatible with all target instruments; databases built exclusively from one instrument type may not generalize equally well to all others.
- Performance validation requires ground-truth labels or a reference dataset; without adequate reference diversity, harmonization may mask true inter-instrument differences or systematic biases.
- The README states that other high-throughput mass spectrometry methodologies 'can also be tried' with RapidMass, indicating that formal validation and support for emerging instrument types may be limited.

## Evidence

- [intro] supports data from multiple instruments, including DI-MS and ASAP-MS: "supports data from multiple instruments, including DI-MS and ASAP-MS"
- [other] LDI-MS data import capability by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats): "Integrate LDI-MS data import capability into RapidMass by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats)"
- [other] Pre-process LDI-MS spectra through RapidMass's standard data pre-processing pipeline (noise filtering, baseline correction, peak detection): "Pre-process LDI-MS spectra through RapidMass's standard data pre-processing pipeline (noise filtering, baseline correction, peak detection)"
- [other] Execute database search using RapidMass's available database search algorithms to score unknown LDI-MS samples: "Execute database search using RapidMass's available database search algorithms to score unknown LDI-MS samples"
- [readme] Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be tried with this software: "Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be"
- [other] Evaluate LDI-MS authentication performance against a reference dataset or ground-truth species labels and compare accuracy metrics to the established DI-MS/ASAP-MS validation baseline: "Evaluate LDI-MS authentication performance against a reference dataset or ground-truth species labels and compare accuracy metrics to the established DI-MS/ASAP-MS validation baseline"
