---
name: in-silico-spectrum-metadata-curation
description: Use when when processing collections of in-silico mass spectra from OMSLs (Open Mass Spectra Libraries) where the adduct field is absent, null, or not explicitly specified in the source file;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - FragHub
  - spectra-hash
derived_from:
- doi: 10.1021/acs.analchem.4c02219
  title: FragHub
evidence_spans:
- Python-3.12
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fraghub_cq
    doi: 10.1021/acs.analchem.4c02219
    title: FragHub
  dedup_kept_from: coll_fraghub_cq
schema_version: 0.2.0
---

# in-silico-spectrum-metadata-curation

## Summary

Automatic assignment and validation of ionization adducts ([M+H]+ or [M-H]-) to in-silico mass spectra when adduct metadata is missing or inconsistent. This skill ensures that in-silico spectra conform to chemical ionization polarity conventions before standardization and downstream analysis.

## When to use

When processing collections of in-silico mass spectra from OMSLs (Open Mass Spectra Libraries) where the adduct field is absent, null, or not explicitly specified in the source file; particularly when spectra are labeled with ionmode (positive or negative) but lack corresponding adduct annotations. FragHub applies this during the standardization pipeline when ingesting .json, .csv, .msp, or .mgf files containing computational spectra.

## When NOT to use

- Spectra already contain an explicit, non-null adduct field—apply validation, not assignment.
- Spectra have ionmode metadata missing entirely—cannot infer adduct without polarity information.
- Experimental (measured) mass spectra, not in-silico—use instrument-reported adduct values instead.

## Inputs

- in-silico mass spectra records with missing or null adduct fields
- ionmode metadata ('pos' or 'neg') for each spectrum
- spectrum metadata objects from .json, .csv, .msp, or .mgf source files

## Outputs

- in-silico spectra with auto-assigned adducts ([M+H]+ or [M-H]-)
- standardized spectrum records ready for validation and downstream curation
- deletion log for spectra failing adduct-ionmode consistency checks

## How to apply

Load in-silico spectrum records and identify those with missing or null adduct fields. Inspect the ionmode field for each spectrum to determine ionization polarity ('pos' or 'neg'). Apply conditional logic: if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct. Validate that the assigned adduct is consistent with ionmode—reject any spectrum where a negative adduct appears in a positive ionmode spectrum, or vice versa. Write updated spectra records with auto-assigned adducts back to the output database or file. This ensures adduct-ionmode consistency before subsequent filtering and normalization steps.

## Related tools

- **Python** (Scripting language for conditional adduct assignment logic and ionmode validation)
- **FragHub** (Mass spectrometry data standardization pipeline that implements automatic adduct assignment during in-silico spectrum curation) — https://github.com/eMetaboHUB/FragHub
- **spectra-hash** (Spectral identifier generation (SPLASH) used for duplicate detection to ensure curation consistency) — https://github.com/berlinguyinca/spectra-hash

## Evaluation signals

- All in-silico spectra with previously missing adducts now have [M+H]+ or [M-H]- assigned and persisted in the output file.
- No spectrum remains with an adduct-ionmode inconsistency (e.g., [M-H]- in positive ionmode or [M+H]+ in negative ionmode).
- Spectra failing the adduct-ionmode check are logged with detailed reasons in a DELETION_REASONS subfolder.
- Auto-assigned adducts match the ionmode polarity: positive ionmode → [M+H]+; negative ionmode → [M-H]-.
- Output spectra conform to ISO/IEC 20802-2:2016 .json format (or equivalent for other output formats) with populated adduct field.

## Limitations

- Requires ionmode metadata to be present and correctly labeled ('pos' or 'neg')—if ionmode is missing or malformed, adduct assignment cannot proceed.
- Assigns only [M+H]+ and [M-H]- adducts; does not handle other adduct types (e.g., [M+Na]+, [M+NH4]+) commonly seen in experimental spectra.
- Does not validate the chemical plausibility of the in-silico spectrum itself—only checks adduct-ionmode consistency. Spectra may still fail other validation filters (e.g., minimum peak count, entropy threshold, or missing SMILES/InChI).
- In-silico spectra lacking SMILES, InChI, AND InChIKey are removed during processing regardless of successful adduct assignment.

## Evidence

- [other] FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency.: "FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency."
- [other] Apply conditional logic: if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct.: "if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct"
- [other] Validate that the assigned adduct is consistent with the ionmode (no negative adducts in positive ionmode, no positive adducts in negative ionmode).: "Validate that the assigned adduct is consistent with the ionmode (no negative adducts in positive ionmode, no positive adducts in negative ionmode)."
- [discussion] auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing.: "auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing."
- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing"
