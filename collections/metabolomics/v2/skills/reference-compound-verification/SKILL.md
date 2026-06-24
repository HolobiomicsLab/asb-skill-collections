---
name: reference-compound-verification
description: Use when after formatting raw mass spectrometry transition data into
  the EISA-EXPOSOME schema (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID columns),
  and before exporting the final database file.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0157
  - http://edamontology.org/topic_3373
  tools:
  - R Shiny
  - EISA-EXPOSOME
  techniques:
  - mass-spectrometry
  license_tier: open
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

# reference-compound-verification

## Summary

Validate database schema conformance and data integrity by checking that reference compounds (e.g., Methamidophos) are present, correctly formatted, and exhibit expected mass spectrometry transitions. This quality-control step ensures a database file is compatible with EISA-EXPOSOME suspect screening before deployment.

## When to use

After formatting raw mass spectrometry transition data into the EISA-EXPOSOME schema (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID columns), and before exporting the final database file. Use this skill to detect schema violations, missing reference entries, or data type mismatches that would break downstream suspect screening.

## When NOT to use

- Input is a raw instrument data file (mzML, mzXML, or NetCDF) that has not yet been converted to tabular transition format.
- The database file is already in production use; reference verification should occur during initial curation, not retrospectively on live data.
- No reference compounds or ground-truth standards are available for the specific chemical class or application domain.

## Inputs

- Raw or candidate database file (.xlsx or .csv format)
- Compiled T3DB reference database file (.xlsx format)
- Mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound ID)

## Outputs

- Validation report (presence/absence and correctness of reference compounds)
- Schema conformance confirmation (column names, data types, required vs. optional fields)
- Integrity flag (pass/fail) for export decision

## How to apply

Load the candidate database file (.xlsx or .csv) and cross-reference it against the compiled T3DB reference database provided by EISA-EXPOSOME. Verify that at least one well-characterized reference compound (e.g., Methamidophos with PrecursorMZ 142.0086, ProductMZ 94.0046, Intensity 100, RT 2.182, ID 1) is present with correct numeric precision and column alignment. Check that all required columns (NAME, PrecursorMZ, ProductMZ, Intensity, ID) are present; RT is optional. Confirm that numeric fields (m/z, intensity, retention time) have consistent precision and no missing or malformed entries. Use the R Shiny interface to visualize and filter results, examining whether reference compounds and their transitions render correctly in the visualization layer. If any reference entry fails validation, halt export and revise the data source or transformation logic.

## Related tools

- **R Shiny** (Interactive interface for visualizing, filtering, and validating database entries; displays reference compounds and their transitions for manual inspection and QC confirmation.) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **EISA-EXPOSOME** (Host platform that defines the required database schema and provides the reference T3DB file for cross-validation.) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Evaluation signals

- Reference compound (Methamidophos) is present in the candidate database with exact matching PrecursorMZ (142.0086), ProductMZ (94.0046), Intensity (100), and RT (2.182) values.
- All six required/optional columns (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID) are present with correct names and no data type mismatches.
- Numeric fields (m/z values, intensity, RT) have consistent decimal precision (e.g., 4 decimal places for m/z) and no null or NaN entries in required columns.
- Reference compound entries render without error in the R Shiny visualization interface and can be filtered and viewed interactively.
- Row count and schema alignment match expectations from the T3DB template; no orphaned or malformed records in reference entries.

## Limitations

- Verification relies on pre-defined reference compounds (Methamidophos); if a database does not include expected standards, this skill cannot validate completeness.
- RT (retention time) is optional; databases lacking RT values will still pass schema validation but may have reduced utility for peak extraction and annotation if RT filtering is downstream.
- Reference verification checks structural conformance but does not validate the accuracy of m/z or intensity values against independent mass spectrometry standards or literature values.
- The R Shiny interface requires a running instance and manual inspection; fully automated validation scripts are not documented in the provided README.

## Evidence

- [readme] Schema requirement: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential"
- [readme] Reference compound exemplar: "|Methamidophos|142.0086|94.0046|100|2.182|1|"
- [other] Workflow integration: "Cross-reference entries against the compiled T3DB database file (provided in .xlsx format) to ensure column alignment and data consistency. Validate presence and correct formatting of Methamidophos"
- [readme] Visualization tool: "We provide a Rshiny program for EISA-EXPOSOME, which runs with the interface shown below, and you can filter the results according to the visualisation interface"
- [other] Export validation: "Export the validated database as .xlsx or .csv format and verify file integrity."
