---
name: suspect-database-matching
description: Use when you have LC-MS peak/feature data, a curated suspect compound database with known m/z, retention time, and fragment ion coordinates, and you observe that traditional peak extraction algorithms have failed to detect ions corresponding to suspected contaminants or chemicals of interest.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# Suspect Database Matching via Targeted Peak Extraction

## Summary

A mass spectrometry feature recovery skill that uses a targeted peak extraction strategy to rescue chemical features at known m/z and retention time coordinates from LC-MS data that traditional peak detection algorithms fail to identify. It integrates a suspect compound database (e.g., T3DB) to improve chemical annotation coverage without reliance on authentic standards.

## When to use

Apply this skill when you have LC-MS peak/feature data, a curated suspect compound database with known m/z, retention time, and fragment ion coordinates, and you observe that traditional peak extraction algorithms have failed to detect ions corresponding to suspected contaminants or chemicals of interest. This is particularly valuable in exposome and untargeted screening workflows where chemical coverage is limited by detection sensitivity.

## When NOT to use

- Input is already a validated, complete feature table from a high-sensitivity targeted method (e.g., MRM quantification)—targeted extraction adds redundancy rather than recovery.
- Suspect database contains incorrect or non-existent m/z values—false coordinates will generate spurious peak calls.
- Raw MS data lacks sufficient signal-to-noise ratio at target m/z positions—no peak will exist to rescue, and the method cannot recover completely absent signals.

## Inputs

- LC-MS raw peak/feature data (mzML, NetCDF, or vendor format importable to R)
- Suspect compound database file (.xlsx or .csv format with columns: NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID)
- Optional: Retention time tolerance window and m/z accuracy threshold (typically ppm-level)

## Outputs

- Augmented feature table with targeted extraction results
- Flagged recovered features (metadata indicating source as targeted extraction)
- Visualization dashboard showing filtered suspect matches and peak chromatograms

## How to apply

Load raw LC-MS feature or peak data and a suspect database file (.xlsx or .csv format containing NAME, PrecursorMZ, ProductMZ, Intensity, and RT columns) into the EISA-EXPOSOME R Shiny interface. For each suspect compound, the algorithm performs targeted extraction by searching the raw data at the specific m/z and retention time positions defined in the database. Peaks are extracted at these targeted coordinates even if they fell below the detection threshold of standard algorithms. Recovered features are flagged as rescued and integrated into the existing feature table. Use the Shiny visualization interface to filter and validate results, checking that rescued peaks are plausible (above noise floor, consistent with expected fragmentation patterns) before downstream analysis.

## Related tools

- **R Shiny** (Interactive interface for loading data, executing targeted peak extraction, filtering results, and visualizing chromatograms and suspect matches) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **EISA-EXPOSOME** (Core computational platform implementing targeted peak extraction strategy and database matching for high-throughput suspect chemical screening) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **T3DB** (Curated suspect compound database provided in .xlsx format with m/z, retention time, and fragment ion annotations)

## Evaluation signals

- Recovered feature count and percent increase over traditional peak extraction baseline
- Schema validation: all rescued features have NAME, PrecursorMZ, ProductMZ, RT, and ID matching the input database exactly
- Peak intensity and signal-to-noise ratio of rescued features are above the noise floor and consistent with fragmentation patterns
- Visualization filters show no false positives or chromatographic artifacts (e.g., scattered noise or column bleed)
- Reproducibility: re-running the same database against the same raw data yields identical recovered feature sets

## Limitations

- Depends critically on database accuracy—incorrect m/z or RT coordinates in the suspect database will yield false or missed recoveries.
- Cannot recover signals absent entirely from raw data; only rescues peaks that exist but fell below traditional algorithm thresholds.
- Retention time (RT) column is optional in the database, reducing specificity if RT is unavailable and only m/z is used for targeting.
- Performance and accuracy are constrained by instrumental mass accuracy and chromatographic stability; poor instrument calibration or retention time drift can cause misalignment.
- The method does not perform de novo compound identification; it requires pre-existing suspect compound entries in the database.

## Evidence

- [readme] used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation: "used a targeted peak extraction strategy to rescue features that cannot be extracted by traditional peak extraction algorithms, improving the coverage of chemica substance annotation"
- [other] Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention time positions corresponding to suspect compounds: "Apply the targeted peak extraction strategy to identify and extract peaks at m/z and retention time positions corresponding to suspect compounds that were missed by traditional peak extraction"
- [readme] Database format requirements including columns NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID, with RT marked as optional: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential"
- [readme] R Shiny program interface and filtering capability: "We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below, and you can filter the results according to the visualisation interface"
- [readme] Core finding on chemical coverage enhancement and standard reduction: "can help reduce the dependence on chemical standards in traditional chemical analysis and significantly enhance the chemical coverage"
