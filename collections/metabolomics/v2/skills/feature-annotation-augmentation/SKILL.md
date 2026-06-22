---
name: feature-annotation-augmentation
description: Use when when a traditional peak extraction pipeline (e.g., XCMS) has generated a feature table from LC-MS data but fails to detect known or suspected compounds present in your sample. Specifically, when you have a suspect database (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3634
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R Shiny
  - EISA-EXPOSOME
  - T3DB
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c02697
  title: EISA-EXPOSOME
evidence_spans:
- We provide a Rshiny program for EISA-EXPOSOME
- We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Targeted Peak Extraction for Feature Annotation Augmentation

## Summary

A computational strategy that rescues LC-MS chemical features missed by traditional peak extraction algorithms by performing targeted extraction at m/z and retention time coordinates of suspect compounds from a reference database. This augments feature tables with previously undetected chemical annotations, improving exposome coverage without requiring additional chemical standards.

## When to use

When a traditional peak extraction pipeline (e.g., XCMS) has generated a feature table from LC-MS data but fails to detect known or suspected compounds present in your sample. Specifically, when you have a suspect database (e.g., T3DB) with precise m/z, retention time, and fragmentation parameters for target analytes, and you observe chemical coverage gaps despite adequate signal intensity at expected chromatographic positions.

## When NOT to use

- Input is already a comprehensively annotated feature table with no known chemical coverage gaps.
- No reference suspect database is available or the database lacks accurate m/z and retention time parameters for your analytes of interest.
- The original peak extraction algorithm detected all compounds above the noise threshold; targeted extraction is redundant if no features were actually missed.

## Inputs

- LC-MS feature/peak data (raw or feature table format)
- Suspect compound database (.xlsx or .csv with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID)

## Outputs

- Augmented feature table with rescued features flagged as recovered by targeted extraction
- Filtered annotation results (via Shiny visualization interface)

## How to apply

Load the LC-MS raw data (or feature/peak matrix) and a suspect compound database (.xlsx or .csv format with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID) into the R Shiny interface. For each suspect compound, the algorithm queries the raw LC-MS data at the specified precursor m/z and retention time window, extracting peaks that fall below the sensitivity or statistical threshold of the original peak picker. Rescued peaks are integrated into the existing feature table with an annotation flag indicating recovery via targeted extraction. Apply post-hoc filtering through the Shiny visualization interface to assess annotation confidence and remove false positives. Success is measured by increased chemical coverage (number of annotated compounds) and reduced false-negative rate in downstream suspect screening workflows.

## Related tools

- **R Shiny** (Interactive interface for targeted peak extraction, result filtering, and visualization of augmented feature tables) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **EISA-EXPOSOME** (Complete computational platform implementing targeted peak extraction and suspect screening with database lookup) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **T3DB** (Compiled suspect compound database in .xlsx format containing m/z, retention time, and fragmentation parameters)

## Evaluation signals

- Number of chemical features in the augmented table exceeds the original table; check for increased annotation coverage.
- Rescued features have retention time and m/z values matching within instrumental tolerance (typically ±5 ppm for m/z) to suspect database entries.
- Flagged rescued features display product ion intensities consistent with expected fragmentation patterns from the suspect database.
- Comparison of the augmented table to an orthogonal or validated chemical standard reference shows improved sensitivity (lower false negatives) for known compounds.
- Visualization filtering produces interpretable, non-redundant results; inspect for duplicate annotations or artifacts introduced by the targeted extraction.

## Limitations

- Accuracy depends critically on the completeness and accuracy of the suspect database; missing or mis-specified m/z or RT values will cause rescue failures.
- Retention time (RT) parameter is not essential in the database format but strongly recommended; targeted extraction without RT windows may yield false positives or cross-contamination from co-eluting compounds.
- The algorithm does not reduce dependence on chemical standards for quantification, only for chemical coverage in detection; quantitative validation still requires reference materials.
- Rescued features flagged as recovered may require orthogonal confirmation (e.g., MS/MS fragmentation verification) to distinguish true positives from instrumental noise or matrix interferences.

## Evidence

- [readme] used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation: "used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation"
- [readme] can help reduce the dependence on chemical standards in traditional chemical analysis and significantly enhance the chemical coverage: "can help reduce the dependence on chemical standards in traditional chemical analysis and significantly enhance the chemical coverage"
- [other] Load LC-MS feature/peak data and the suspect database (e.g., T3DB in .xlsx format) into memory. Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention time positions corresponding to suspect compounds that were missed by traditional peak extraction.: "Load LC-MS feature/peak data and the suspect database (e.g., T3DB in .xlsx format) into memory. Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention time"
- [other] Integrate rescued features into the existing feature table, flagging them as recovered by targeted extraction.: "Integrate rescued features into the existing feature table, flagging them as recovered by targeted extraction."
- [readme] your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential.: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [intro] you can filter the results according to the visualisation interface: "you can filter the results according to the visualisation interface"
