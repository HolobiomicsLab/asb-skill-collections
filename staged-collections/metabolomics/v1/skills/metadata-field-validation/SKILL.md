---
name: metadata-field-validation
description: Systematic validation of metadata field presence, data types, and values in mass spectral library records against expected schemas and plausibility thresholds. This skill ensures that essential annotation fields (SMILES, InChI, InChIKey, adduct, precursor m/z, parent mass) are correctly populated and logically consistent before downstream analysis.
when_to_use_negative:
- Input spectra lack any structural annotation (SMILES, InChI, or compound name); metadata-field-validation requires at least one annotation source to derive or repair fields.
- Analysis goal is to filter unannotated experimental MS/MS data without structure assignment; use peak filtering and intensity normalization instead.
- Metadata fields are already validated and locked (e.g., curated reference libraries from a downstream consumer); validation is redundant.
edam_operation: http://edamontology.org/operation_3436
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3407
- http://edamontology.org/topic_3314
tools:
- name: matchms
  role: Provides metadata filters ('Require valid annotation', 'Repair adduct and parent mass based on SMILES', 'Repair not matching annotation') that implement field validation logic and repair workflows; orchestrates the full pipeline
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Loads and compares SMILES, InChI, and InChIKey to verify structural annotation consistency; detects mismatches in 2D structure
- name: PubChem
  role: Reference database from which canonical SMILES, InChI, and InChIKey are derived during metadata repair
  repo: https://pubchem.ncbi.nlm.nih.gov/
- name: Python
  role: Programming language for parsing spectrum records, orchestrating validation logic, and aggregating statistics
provenance:
  source_task_ids:
  - task_007
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/metadata-field-validation@sha256:f611450550fb9d339ee24832b80272652341749e18cf19f0268725f6dbf1bcf7
---

# metadata-field-validation

## Summary

Systematic validation of metadata field presence, data types, and values in mass spectral library records against expected schemas and plausibility thresholds. This skill ensures that essential annotation fields (SMILES, InChI, InChIKey, adduct, precursor m/z, parent mass) are correctly populated and logically consistent before downstream analysis.

## When to use

Apply this skill when ingesting or curating annotated mass spectral library records (e.g., GNPS, MoNA, Massbank, NIST) where metadata completeness and correctness directly affect structure annotation validation. Validate field presence and coherence after repairs have been applied (e.g., after deriving SMILES from compound names or repairing adduct/parent mass fields) to confirm that the repair succeeded and introduced no new inconsistencies.

## When NOT to use

- Input spectra lack any structural annotation (SMILES, InChI, or compound name); metadata-field-validation requires at least one annotation source to derive or repair fields.
- Analysis goal is to filter unannotated experimental MS/MS data without structure assignment; use peak filtering and intensity normalization instead.
- Metadata fields are already validated and locked (e.g., curated reference libraries from a downstream consumer); validation is redundant.

## Inputs

- annotated mass spectral library records (mzML, JSON, or custom format with metadata fields)
- metadata field schema specification (required fields, data types, ranges)
- structure comparison tool (RDKit) for SMILES/InChI/InChIKey consistency checks
- reference compound database (PubChem) for canonical annotation lookup

## Outputs

- validation report (per-spectrum: pass/fail/repaired status, field-level error details)
- aggregate statistics (total input spectra, count removed, count repaired, count retained)
- cleaned spectrum records with validated/repaired metadata
- error manifest (systematic issues, e.g., % of spectra with missing ionmode, % with inconsistent SMILES/InChI pairs)

## How to apply

Parse metadata fields from each spectrum record and check: (1) field presence — confirm that required fields (ionmode, precursor m/z, SMILES, InChI, InChIKey, adduct, parent mass) are not null or empty; (2) data type correctness — verify numeric fields (precursor m/z, parent mass, collision energy) are valid numbers, not strings; (3) logical consistency — cross-validate related fields, e.g., check that derived SMILES/InChI/InChIKey triples are mutually consistent using structure comparison tools (RDKit), and that adduct type is compatible with the observed precursor m/z and calculated parent mass (monoisotopic mass, not molar mass); (4) plausibility — flag spectra where annotations exist but are chemically implausible given the measured mass. Document validation results per-spectrum and aggregate pass/fail/repair counts (e.g., 31,758 removed vs. 52,084 repaired) to judge repair effectiveness and identify systematic gaps.

## Related tools

- **matchms** (Provides metadata filters ('Require valid annotation', 'Repair adduct and parent mass based on SMILES', 'Repair not matching annotation') that implement field validation logic and repair workflows; orchestrates the full pipeline) — https://github.com/matchms/matchms
- **RDKit** (Loads and compares SMILES, InChI, and InChIKey to verify structural annotation consistency; detects mismatches in 2D structure)
- **PubChem** (Reference database from which canonical SMILES, InChI, and InChIKey are derived during metadata repair) — https://pubchem.ncbi.nlm.nih.gov/
- **Python** (Programming language for parsing spectrum records, orchestrating validation logic, and aggregating statistics)

## Evaluation signals

- Field presence check: 100% of spectra post-validation contain non-null values for ionmode, precursor m/z, and at least one structural annotation (SMILES, InChI, or InChIKey).
- Data type correctness: numeric fields (precursor m/z, parent mass, collision energy) parse without error and fall within plausible ranges (e.g., m/z > 0, parent mass matches monoisotopic mass, not molar mass).
- Structural consistency: SMILES/InChI/InChIKey triples derived or repaired via RDKit comparison show ≥99.97% agreement (per the article's repair adduct filter result: 99.98% of spectra had correct adduct after repair).
- Repair effectiveness: Compare pre-repair and post-repair counts — expect repair functions to reduce removal rate (article reports 31,758 removed vs. 52,084 repaired, demonstrating 40% reduction in discarded spectra).
- Error manifest: Document systematic issues (e.g., article reports 27.6% of spectra could not derive SMILES from compound name; 1.62% of annotated spectra had different 2D structure) to identify which fields or repair functions need strengthening.

## Limitations

- Field validation cannot detect chemically wrong annotations that are consistent with measured precursor m/z and mass; the pipeline lacks fragment-level plausibility checks (e.g., matching observed peaks to fragmentation rules of the annotated structure).
- Repair functions are tied to specific metadata fields (adduct, precursor m/z, SMILES); other fields like instrument type and collision energy are not yet validated or cleaned by the current matchms pipeline.
- Validation depends on external reference databases (PubChem) for canonical annotations; gaps or errors in PubChem will propagate to the cleaned library.
- Repair effectiveness varies by annotation source: compound names with insufficient detail or non-standard nomenclature cannot be reliably converted to SMILES (27.6% failure rate observed in the article).

## Evidence

- [abstract] SMILES, InChI and InChIKey are loaded by RDKit and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Repair not matching annotation resolves conflicts between SMILES/InChI/InChIKey fields: "Repair not matching annotation"
- [abstract] Repair adduct and parent mass based on SMILES validates and corrects adduct assignment: "Repair adduct and parent mass based on SMILES"
- [abstract] 31,758 spectra removed vs. 52,084 repaired demonstrates repair function effectiveness: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [discussion] Current publicly available libraries lack plausibility checks that consider both metadata and measured fragments: "Current publicly available libraries often have incorrect or inaccuracies, they currently still lack plausibility checks that consider both metadata and measured fragments."
