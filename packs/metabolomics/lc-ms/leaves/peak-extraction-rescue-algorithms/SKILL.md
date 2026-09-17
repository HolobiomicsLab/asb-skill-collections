---
name: peak-extraction-rescue-algorithms
description: Use when traditional peak extraction algorithms have produced a feature
  table that you suspect is incomplete or missing known suspects from your target
  database (e.g., T3DB).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2258
  tools:
  - R Shiny
  - EISA-EXPOSOME
  techniques:
  - LC-MS
  - GC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown
  below
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eisa_exposome_cq
    doi: 10.1021/acs.analchem.3c02697
    title: EISA-EXPOSOME
  dedup_kept_from: coll_eisa_exposome_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c02697
  all_source_dois:
  - 10.1021/acs.analchem.3c02697
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Targeted Peak Extraction Strategy for Rescuing Missed Features

## Summary

A computational strategy that identifies and extracts LC-MS peaks at m/z and retention time positions corresponding to suspect compounds that traditional peak extraction algorithms fail to detect. This technique augments feature tables with recovered chemical features, improving coverage of chemical substance annotation without requiring chemical standards.

## When to use

Apply this skill when traditional peak extraction algorithms have produced a feature table that you suspect is incomplete or missing known suspects from your target database (e.g., T3DB). Specifically, use it when you have: (1) LC-MS raw data or feature/peak data in standard formats, (2) a suspect database with known m/z, retention time, and intensity values (.xlsx or .csv), and (3) evidence or concern that target compounds are not appearing in the initial peak extraction output.

## When NOT to use

- Your input is already a complete, validated feature table and you have no suspicion of missing features — targeted rescue is an augmentation step, not a primary extraction method.
- Your suspect database lacks reliable m/z or retention time information, or contains no standards relevant to your sample — the strategy relies on precise coordinate matching.
- You are working with data types other than LC-MS (e.g., GC-MS without compatible m/z/RT metadata) — the method is designed for LC-MS peak morphology and timing.

## Inputs

- LC-MS raw data or feature/peak data (supported formats: mzML, NetCDF, or equivalent)
- Suspect database file (.xlsx or .csv format with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT)
- Initial feature table from traditional peak extraction

## Outputs

- Augmented feature table with targeted extraction results
- Rescued features flagged with metadata indicating recovery by targeted extraction
- Visualization-filtered subset of results (via R Shiny interface)

## How to apply

Load the LC-MS feature/peak data and your suspect database (with columns NAME, PrecursorMZ, ProductMZ, Intensity, and RT where RT is optional) into the R Shiny EISA-EXPOSOME interface. The algorithm then systematically searches the raw LC-MS data at the exact m/z and retention time coordinates specified in the database to identify peaks that the traditional extraction algorithm missed. These rescued peaks are integrated back into the feature table with a flag indicating they were recovered by targeted extraction. The rationale is that traditional algorithms may fail to detect low-intensity, co-eluting, or noise-adjacent peaks that can be reliably identified when you know precisely where to look. Filter results using the visualization interface to validate that rescued features are genuine and not artifacts.

## Related tools

- **R Shiny** (Interactive interface for loading LC-MS data and suspect database, executing targeted peak extraction, and filtering/visualizing rescued features) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **EISA-EXPOSOME** (Complete platform implementing targeted peak extraction strategy and downstream annotation for suspect chemical screening) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Evaluation signals

- Rescued features have m/z and retention time values matching entries in the suspect database (within expected instrumental tolerance)
- Intensity values of rescued peaks are consistent with the database's reported Intensity column, or show expected signal-to-noise ratios
- The augmented feature table contains a flag or metadata field identifying which features were recovered by targeted extraction versus traditional extraction
- Visual inspection via the R Shiny interface confirms that rescued peaks are genuine chromatographic/mass spectral signals, not noise or artifacts
- The number and diversity of chemical substances annotated increases measurably compared to the original feature table, with gains concentrated in the suspect compound set

## Limitations

- The strategy depends on the accuracy and completeness of the suspect database; incorrect m/z or RT values in the database will cause false negatives or lead to rescue of incorrect peaks.
- Retention time (RT) is listed as 'not essential' in the database schema; recovery accuracy may be lower when RT information is missing, as m/z alone can be ambiguous in crowded mass spectra.
- The method does not reduce dependence on chemical standards for *quantification*; it only aids in *detection* and *annotation*, and still may require orthogonal validation.
- Performance depends on LC-MS data quality; severely noisy or poorly resolved data may yield false rescues or fail to recover genuine low-intensity features.

## Evidence

- [intro] Targeted peak extraction strategy rescues features that cannot be extracted by traditional peak extraction algorithms, improving coverage of chemical substance annotation: "used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation"
- [readme] Database schema specifies required and optional columns for suspect compound definition: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [other] Workflow loads data, applies targeted extraction, integrates results, and outputs augmented feature table: "1. Load LC-MS feature/peak data and the suspect database (e.g., T3DB in .xlsx format) into memory. 2. Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention"
- [readme] Interactive filtering capability allows validation of results via visualization: "you can filter the results according to the visualisation interface"
- [intro] Method reduces dependence on chemical standards in traditional analysis: "can help reduce the dependence on chemical standards in traditional chemical analysis and significantly enhance the chemical coverage"
