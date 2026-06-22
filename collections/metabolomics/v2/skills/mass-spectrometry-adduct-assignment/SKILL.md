---
name: mass-spectrometry-adduct-assignment
description: Use when when processing in-silico or experimental MS spectra records from databases with incomplete metadata, specifically when the adduct field is null or absent but the ionmode field (positive/negative polarity) is present.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0580
  tools:
  - Python
  - FragHub
  - Python 3.12
  - RDkit
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

# mass-spectrometry-adduct-assignment

## Summary

Automatically assign ionization adducts ([M+H]+ or [M-H]-) to mass spectra with missing adduct annotations by inferring the appropriate adduct from the ionization mode (positive or negative). This standardization step ensures consistency and prevents downstream analysis errors caused by missing or inconsistent adduct information.

## When to use

When processing in-silico or experimental MS spectra records from databases with incomplete metadata, specifically when the adduct field is null or absent but the ionmode field (positive/negative polarity) is present. This is essential during MS data standardization workflows where consistent adduct annotation is required for spectral matching, molecular formula annotation, or compatibility with analysis software like MSdial or MZmine.

## When NOT to use

- Input spectra already have explicit adduct annotations — assignment would overwrite existing metadata without validation.
- Ionmode field is missing or ambiguous — conditional logic cannot reliably infer the correct adduct.
- Spectrum uses non-standard ionization (e.g., [M+Na]+, [M+NH4]+, [M-H2O]-) — the binary pos/neg mapping is insufficient.

## Inputs

- Mass spectra records with null or missing adduct field
- Ionmode field (pos/neg) indicating ionization polarity
- Spectrum metadata from database or flat file (.mgf, .msp, .json, .csv)

## Outputs

- Spectra records with assigned [M+H]+ or [M-H]- adduct annotation
- Updated database records or output spectral files with standardized adduct field

## How to apply

Load spectrum records from the database and filter for entries with missing or null adduct fields. Inspect the ionmode field to determine ionization polarity ('pos' or 'neg'). Apply conditional logic: assign [M+H]+ adduct when ionmode is 'pos', and [M-H]- adduct when ionmode is 'neg'. Validate that the assigned adduct is consistent with ionmode (reject negative adducts in positive ionmode, positive adducts in negative ionmode) to catch data inconsistencies. Write updated records with auto-assigned adducts back to the database or output file.

## Related tools

- **FragHub** (Implements automatic adduct assignment for in-silico spectra; validates adduct-ionmode consistency and filters inconsistent spectra) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (Execution environment for conditional logic and database I/O operations)
- **RDkit** (Optional downstream tool for molecular descriptor calculation on standardized spectra)

## Evaluation signals

- All spectra with null adduct field and valid ionmode now have assigned adduct annotation matching ionmode polarity ([M+H]+ for pos, [M-H]- for neg).
- No spectrum contains a positive adduct ([M+H]+) in negative ionmode, or negative adduct ([M-H]-) in positive ionmode — cross-field consistency check passes.
- Output file schema validation: adduct field is no longer null; all records conform to standardized adduct format (e.g., '[M+H]+', '[M-H]-').
- Record count before and after assignment: spectra with inconsistent adduct-ionmode pairs are deleted or flagged, reducing total record count predictably.
- Downstream spectral matching or formula annotation tasks report improved consistency or reduced error rates compared to unprocessed data.

## Limitations

- Binary ionmode mapping (pos → [M+H]+, neg → [M-H]-) assumes protonation as the default adduct; non-standard ionization (e.g., [M+Na]+, [M+NH4]+) cannot be inferred and will be missed.
- Spectra with missing or ambiguous ionmode field cannot be processed — assignment is skipped for these records.
- The workflow does not validate whether the inferred adduct is chemically plausible for the precursor m/z and molecular weight; chemical sanity checks require additional steps (e.g., RDkit mass calculation).
- Duplicate spectra (identical m/z, peaks, but assigned different adducts) are not de-duplicated by this step alone — separate SPLASH-based deduplication or multi-field checks are required.

## Evidence

- [other] FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency.: "FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency."
- [other] Load in-silico spectra records from the FragHub database, filtering for entries with missing or null adduct fields. Inspect the ionmode field for each spectrum to determine ionization polarity (pos/neg). Apply conditional logic: if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct.: "Apply conditional logic: if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct."
- [other] Validate that the assigned adduct is consistent with the ionmode (no negative adducts in positive ionmode, no positive adducts in negative ionmode).: "Validate that the assigned adduct is consistent with the ionmode (no negative adducts in positive ionmode, no positive adducts in negative ionmode)."
- [discussion] auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing.: "auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing."
- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
