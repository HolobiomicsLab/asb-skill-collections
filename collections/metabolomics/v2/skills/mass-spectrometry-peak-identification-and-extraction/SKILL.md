---
name: mass-spectrometry-peak-identification-and-extraction
description: Use when when you have raw mass spectrometry data from direct-infusion (DI-MS) or ambient surface analysis probe (ASAP-MS) instruments and need to identify which m/z peaks are biologically or chemically informative for sample classification, rather than processing the entire spectrum including.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
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

# mass-spectrometry-peak-identification-and-extraction

## Summary

Automated identification and extraction of relevant mass-to-charge peaks from high-throughput mass spectrometry data (DI-MS, ASAP-MS) to reduce dimensionality and prepare data for species classification. This step filters raw MS spectra to feature sets suitable for downstream database searching and sample discrimination.

## When to use

When you have raw mass spectrometry data from direct-infusion (DI-MS) or ambient surface analysis probe (ASAP-MS) instruments and need to identify which m/z peaks are biologically or chemically informative for sample classification, rather than processing the entire spectrum including noise and instrument artifacts.

## When NOT to use

- Input data is already a pre-processed feature table or peak list without raw m/z spectra
- Your MS instrument uses non-standard formats not supported by DI-MS, ASAP-MS, AI-MS, or LDI-MS data loaders in RapidMass

## Inputs

- Raw mass spectrometry data in DI-MS format
- Raw mass spectrometry data in ASAP-MS format
- Mass spectrometry data from ambient ionization MS (AI-MS) or laser desorption/ionization MS (LDI-MS)

## Outputs

- Extracted set of interested MS peaks (m/z values and intensities)
- Peak feature matrix suitable for database search and classification

## How to apply

Load DI-MS or ASAP-MS format mass spectrometry data into RapidMass. The software automatically identifies interested MS peaks using built-in algorithms that distinguish signal from noise across the full m/z range. The extracted peaks are ranked or scored by relevance; these become the feature set for downstream database search and scoring algorithms. The rationale is that automatic peak identification reduces manual curation burden and ensures consistent, reproducible feature extraction across large batches of plant or biological samples, enabling direct discrimination of unknown species against reference databases.

## Related tools

- **RapidMass** (Graphical application that integrates automatic MS peak identification, data pre-processing, and visual peak extraction for species discrimination workflows) — https://github.com/Katherine00689/RapidMass

## Evaluation signals

- Extracted peak set is non-empty and contains m/z values within the expected range for the instrument and sample type
- Number of identified peaks is consistent across replicate samples of the same species, indicating reproducible feature extraction
- Downstream database search algorithm successfully scores and classifies unknown samples against reference species using only the extracted peaks
- Visual output (e.g., score heatmap, classification plot) shows clear separation between different plant species, confirming peaks are informative for discrimination
- Classification accuracy against ground-truth species labels meets the performance threshold documented in validation studies (e.g., >90% for easily confused plant materials)

## Limitations

- Automatic peak identification algorithm parameters and sensitivity thresholds are not fully documented in the README; results may vary depending on instrument calibration and sample ionization conditions
- Peak extraction performance was validated only on easily confused plant materials; generalization to other biological or chemical sample types is not discussed
- No changelog is available to track changes in the peak identification algorithm across software versions

## Evidence

- [readme] Automatic peak identification algorithm ensures consistent feature extraction: "the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS"
- [intro] Peak extraction is part of integrated data pre-processing workflow: "integrates data pre-processing, analysis, and evaluation"
- [intro] Extracted peaks enable downstream species discrimination and classification: "enabling direct discrimination of unknown sample species with intuitive visual outputs"
- [readme] Validation demonstrates peak extraction success on botanical samples: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results"
