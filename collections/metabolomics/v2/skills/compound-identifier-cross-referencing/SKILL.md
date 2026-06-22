---
name: compound-identifier-cross-referencing
description: 'Use when when you have prepared raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound identifiers) and need to verify it conforms to EISA-EXPOSOME''s required schema before database import. Specifically: you are building or validating a custom .xlsx/.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R Shiny
  - T3DB compiled database
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

# compound-identifier-cross-referencing

## Summary

Validate mass spectrometry transition data against a curated reference database (e.g. T3DB) by aligning compound identifiers, precursor/product m/z values, and retention times to ensure column structure and data consistency before importing into EISA-EXPOSOME for suspect screening.

## When to use

When you have prepared raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound identifiers) and need to verify it conforms to EISA-EXPOSOME's required schema before database import. Specifically: you are building or validating a custom .xlsx/.csv database file and need confidence that entries match expected reference transitions and naming conventions.

## When NOT to use

- Your database file already matches the EISA-EXPOSOME schema and has been validated against a trusted reference—proceed directly to import.
- You are performing de novo compound identification without a curated reference database available—use spectral library matching or in silico prediction instead.
- Your transition data is already in a different standardized format (e.g., ProteoWizard mzML) that will be automatically converted by the pipeline.

## Inputs

- raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, compound identifiers)
- reference database file in .xlsx or .csv format (e.g., compiled T3DB)
- compound name/identifier list

## Outputs

- validated database file (.xlsx or .csv) with correct column structure (NAME, PrecursorMZ, ProductMZ, Intensity, RT, ID)
- cross-reference validation report documenting matched and unmatched entries
- file integrity confirmation

## How to apply

Load your prepared tabular transition data and the reference database file (e.g., compiled T3DB in .xlsx format) into a comparison workflow. Cross-reference each compound entry by NAME and ID against the reference to verify PrecursorMZ, ProductMZ, Intensity, and RT (if applicable) values match expected transitions. Use a reference compound check—e.g., validate Methamidophos entries (PrecursorMZ 142.0086, ProductMZ 94.0046, Intensity 100, RT 2.182, ID 1) as a known positive control. Document any mismatches or missing columns (NAME, PrecursorMZ, ProductMZ, Intensity, ID are required; RT is optional). Export the validated dataset as .xlsx or .csv and verify file integrity before loading into EISA-EXPOSOME.

## Related tools

- **R Shiny** (interactive interface for filtering, validating, and reviewing cross-referenced database entries within EISA-EXPOSOME) — https://github.com/Lab-XUE/EISA-EXPOSOME
- **T3DB compiled database** (reference dataset for cross-referencing pesticide and compound identifiers, m/z values, and retention times) — https://github.com/Lab-XUE/EISA-EXPOSOME

## Evaluation signals

- All compound NAME entries in your database match entries in the reference database (T3DB or equivalent) by ID and NAME.
- PrecursorMZ, ProductMZ, and Intensity values for each transition align with reference values within acceptable measurement error (±0.01 m/z or instrument tolerance).
- Retention time (RT) values, where provided, are consistent with reference RT or clearly documented if measured under different conditions.
- Required columns (NAME, PrecursorMZ, ProductMZ, Intensity, ID) are present; optional RT column is either populated consistently or explicitly omitted.
- Reference compound check passes: Methamidophos entries display both transitions (PrecursorMZ 142.0086 → 94.0046 and 142.0086 → 124.9816) with correct Intensity and RT values.
- File exports without corruption and can be loaded into EISA-EXPOSOME without schema errors.

## Limitations

- Cross-referencing is only as reliable as the reference database; incomplete or outdated reference data (e.g., missing transitions or incorrect m/z values) will propagate validation errors.
- RT values are optional and may differ between instruments, labs, or chromatographic methods; comparison requires documented harmonization or exclusion from validation.
- The workflow does not resolve compound name ambiguities (e.g., synonyms, isomers, or metabolites with identical m/z); manual curation may be needed for entries with multiple reference matches.
- Large database files or many-to-many matching scenarios may require computational optimization; no performance benchmarks are provided.

## Evidence

- [readme] column structure and data format requirement: "your file (.xlsx /.csv) must contain the following columns:|NAME|PrecursorMZ|ProductMZ|Intensity|RT|ID|, **RT** is not essential."
- [readme] T3DB reference format and example: "We also provide the compiled T3DB database file in .xlsx format. |Methamidophos|142.0086|94.0046|100|2.182|1|"
- [other] cross-reference validation workflow step: "Cross-reference entries against the compiled T3DB database file (provided in .xlsx format) to ensure column alignment and data consistency."
- [other] reference compound check: "Validate presence and correct formatting of Methamidophos entries as a reference compound check."
- [other] data input sources: "Obtain or prepare raw mass spectrometry transition data (precursor m/z, product m/z, intensity, retention time, and compound identifiers)."
