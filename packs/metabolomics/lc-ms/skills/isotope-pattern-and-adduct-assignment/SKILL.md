---
name: isotope-pattern-and-adduct-assignment
description: Use when after feature detection has produced a TSV feature table (from Asari or equivalent) containing m/z, retention time, and intensity columns, and before MS1 or MS2 annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - ThermoRawFileParser
  - khipu
  - Python
  - Asari
  - mass2chem
  techniques:
  - LC-MS
derived_from:
- doi: 10.1371/journal.pcbi.1011912
  title: pcpfm
evidence_spans:
- convert Thermo .raw to mzML (ThermoRawFileParser)
- pre-annotation to group featues to empirical compounds (khipu)
- Python-Centric Pipeline for Metabolomics
- The Python-Centric Pipeline for Metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pcpfm
    doi: 10.1371/journal.pcbi.1011912
    title: pcpfm
  dedup_kept_from: coll_pcpfm
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1011912
  all_source_dois:
  - 10.1371/journal.pcbi.1011912
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Isotope Pattern and Adduct Assignment

## Summary

Cluster LC-MS features into empirical compounds by matching isotope and adduct signatures using configurable m/z and retention time tolerances, producing annotated feature groups that represent putative metabolites. This skill bridges individual feature detection and compound-level annotation.

## When to use

Apply this skill after feature detection has produced a TSV feature table (from Asari or equivalent) containing m/z, retention time, and intensity columns, and before MS1 or MS2 annotation. Use when you need to group multiply-charged or isotope-bearing features into single metabolite entities, or when your ionization mode produces known adduct families (e.g., [M+H]+, [M+Na]+, [M+NH4]+ in positive mode) that you want to collapse into empirical compounds.

## When NOT to use

- Input feature table is already grouped or pre-annotated at the compound level
- Sample ionization mode or adduct families are unknown and cannot be specified
- m/z or retention time calibration is poor (ppm error >10 ppm) — recalibrate before grouping

## Inputs

- feature table (TSV format) with columns: m/z, retention time, intensity
- ionization mode specification (positive or negative)
- adduct definitions (e.g., [M+H]+, [M+Na]+, [M+NH4]+)

## Outputs

- empirical compound JSON file (empCpd.json)
- feature groupings with isotope and adduct annotations
- median m/z and retention time per compound

## How to apply

Load the preferred feature table (TSV format) from the Asari results directory. Invoke khipu's build_empCpds command, specifying ionization mode (positive or negative) and m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds). Khipu clusters features within these mass and time windows, assigning isotopologue and adduct annotations based on observed mass differences (e.g., 1.003 Da for +1 charge difference) and charge state patterns. The algorithm outputs a JSON file where each empirical compound contains a list_of_features, median m/z, median retention time, and pre-annotation fields. Validate that all required JSON fields are populated and that feature clustering is consistent with expected adduct mass shifts for the chosen ionization mode.

## Related tools

- **khipu** (Clusters features into empirical compounds by matching isotopes and adducts within configurable m/z and retention time windows; performs mass-difference-based annotation of charge states and adduct types.) — https://github.com/shuzhao-li-lab/khipu
- **Asari** (Produces the upstream feature table (TSV format) that serves as input to isotope and adduct assignment.) — https://github.com/shuzhao-li/asari
- **mass2chem** (Provides utilities for interpreting mass differences and adduct definitions during annotation.) — https://github.com/shuzhao-li-lab/mass2chem

## Evaluation signals

- JSON schema validation: all empirical compounds contain required fields (list_of_features, median_mz, median_rt, pre_annotation)
- Mass difference consistency: isotope shifts match expected values (e.g., 1.003 Da for [M]+ vs [M+1]+; 0.502 Da for doubly-charged vs singly-charged)
- Retention time clustering: grouped features lie within the specified retention time tolerance (default 2 seconds)
- m/z clustering: grouped features lie within the specified m/z tolerance (default 5 ppm)
- Adduct annotation plausibility: assigned adducts match the ionization mode (e.g., [M+H]+ and [M+Na]+ in positive mode, [M-H]- in negative mode)

## Limitations

- Clustering accuracy depends critically on accurate m/z and retention time calibration; poorly calibrated data will produce fragmented or over-merged empirical compounds.
- Fixed default tolerances (5 ppm m/z, 2 seconds RT) may not be optimal for all instruments or chromatography methods; method optimization may require empirical adjustment.
- Does not resolve structural isomers or in-source fragments; isotope and adduct annotation is purely mass-based and cannot distinguish metabolites with identical m/z and retention time.
- Performance on very large feature tables (>10,000 features) has not been extensively benchmarked; computational scaling is not discussed in the paper.

## Evidence

- [other] The build_empCpds command groups features into empirical compounds by matching isotopes and adducts with configurable mz tolerance (default 5 ppm) and rt tolerance (default 2 seconds), producing a JSON file containing grouped features with their mz and rt values.: "build_empCpds command constructs empirical compound groups from a feature table using khipu with configurable mz and retention time tolerances"
- [other] Construct feature groups by clustering features within the specified m/z and rt windows, assigning isotopologue and adduct annotations based on observed mass differences and charge state patterns.: "Construct feature groups by clustering features within the specified m/z and rt windows, assigning isotopologue and adduct annotations based on observed mass differences and charge state patterns"
- [readme] pre-annotation to group featues to empirical compounds (khipu): "pre-annotation to group featues to empirical compounds (khipu)"
- [readme] empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards.: "empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards"
- [other] Load the preferred feature table (TSV format) from the asari_results subdirectory. Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time tolerance (default 2 seconds), specifying ionization mode and adduct definitions for the detected polarity.: "Load the preferred feature table (TSV format) from the asari_results subdirectory. Invoke khipu via the build_empCpds command with configurable m/z tolerance (default 5 ppm) and retention time"
