---
name: molecular-identifier-completeness-verification
description: Use when during MSP, MGF, JSON, or CSV file parsing when standardizing mass spectra from heterogeneous open mass spectral libraries (OMSLs).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0118
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - Python 3.12
  - RDkit
  - spectra-hash (SPLASH)
  - FragHub
  techniques:
  - GC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02219
  all_source_dois:
  - 10.1021/acs.analchem.4c02219
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-identifier-completeness-verification

## Summary

Verify that mass spectra possess all required chemical identifiers (SMILES, InChI, InChIKey) and consistent adduct–ionmode pairs before inclusion in a standardized spectral library. This skill ensures data completeness and chemical consistency, preventing analysis with ambiguous or contradictory molecular information.

## When to use

Apply this skill during MSP, MGF, JSON, or CSV file parsing when standardizing mass spectra from heterogeneous open mass spectral libraries (OMSLs). Trigger verification after metadata extraction and before final spectrum list serialization, especially when spectra originate from multiple databases with varying annotation completeness or when chemical identifiers have been recalculated or normalized from SMILES/InChI sources.

## When NOT to use

- Input spectra have already been manually curated and verified for identifier completeness by a domain expert; re-verification may introduce false negatives.
- Spectra are from a single, internally consistent database (e.g., MassBank or NIST) with a known annotation standard; additional filtering may remove valid entries that use alternative identifier conventions.
- Analysis goal requires retention of spectra with partial identifiers (e.g., SMILES-only or InChIKey-only) for exploratory data mining or comparative method development; this skill enforces strict completeness and may exclude relevant data.

## Inputs

- MSP file (line-by-line parsed spectrum metadata and peak blocks)
- MGF file (precursor m/z, charge, SMILES/InChI/InChIKey fields, and peak lists)
- JSON file (ISO/IEC 20802-2:2016 or non-standard JSON spectrum records)
- CSV file (semicolon- or tab-separated; requires 'peaks' column and chemical identifier columns)
- Parsed spectrum object (metadata dict: NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY; peak_array: list of m/z–intensity pairs)

## Outputs

- Filtered spectrum list (non-deleted entries only)
- DELETION_REASONS subdirectory (text files, one per deleted spectrum, recording reason: missing identifiers, adduct–ionmode mismatch, or bad adduct format)
- Serialized output file (MSP, MGF, JSON, or CSV format, depending on configuration)

## How to apply

After parsing spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) and m/z–intensity peak pairs, apply three sequential filters: (1) Delete spectrum if it lacks SMILES AND InChI AND InChIKey (i.e., no chemical structure identifier is present). (2) Delete spectrum if the adduct–ionmode pairing is inconsistent: remove spectra with negative adduct in positive ionmode or positive adduct in negative ionmode. (3) Delete spectrum if no ADDUCT field is present or contains invalid/malformed values. Log all deletions to a DELETION_REASONS subdirectory with detailed reason strings. The rationale is that incomplete or contradictory identifiers render spectra unsuitable for spectral matching, chemical classification (via RDkit/PubChem/ClassyFire), or downstream analysis tools (MSdial, MZmine). Spectra passing all three checks are retained and serialized to the output file.

## Related tools

- **Python 3.12** (File I/O, line-by-line MSP/MGF/CSV parsing, metadata extraction, adduct regex validation, and logging of deletion reasons.)
- **RDkit** (Recalculation and normalization of SMILES and InChI identifiers to validate their correctness before completeness check.)
- **spectra-hash (SPLASH)** (Duplicate removal by SPLASH key matching; ensures that only unique spectra (by SPLASH hash) are retained after identifier verification.) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (End-to-end MS data standardization pipeline that integrates molecular-identifier-completeness-verification as a core filtering step during spectrum processing.) — https://github.com/eMetaboHUB/FragHub

## Examples

```
# Python 3.12 snippet within FragHub pipeline:
if not (spectrum.get('SMILES') or spectrum.get('INCHI') or spectrum.get('INCHIKEY')):
    deletion_log.append({'spectrum_id': spectrum['NAME'], 'reason': 'missing_all_identifiers'})
    continue
if spectrum['IONMODE'] == 'pos' and is_negative_adduct(spectrum['ADDUCT']):
    deletion_log.append({'spectrum_id': spectrum['NAME'], 'reason': 'negative_adduct_in_positive_ionmode'})
    continue
retained_spectra.append(spectrum)
```

## Evaluation signals

- Verify that no output spectrum lacks all three identifiers (SMILES, InChI, InChIKey); sample random output records and confirm at least one identifier is present in each.
- Check DELETION_REASONS logs: confirm that all deleted spectra have documented reason strings (e.g., 'missing_all_identifiers', 'negative_adduct_in_positive_ionmode', 'bad_adduct_format'). Count of deleted spectra should match total reason log entries.
- Validate adduct–ionmode consistency in retained spectra: spot-check that positive ionmode spectra contain only positive adducts ([M+H]+, [M+Na]+, etc.) and negative ionmode spectra contain only negative adducts ([M-H]-, [M+Cl]-, etc.). No spectrum should have adduct sign opposite to ionmode polarity.
- Compare input and output spectrum counts; reduction should be proportional to data quality. If reduction is unexpectedly high (>50%), inspect DELETION_REASONS for systematic issues (e.g., misconfigured adduct regex, missing InChIKey field in entire input batch).
- Perform schema validation: confirm output file complies with declared format (MSP header fields, MGF spectrum blocks, JSON record structure, CSV column headers). No malformed or truncated spectrum entries should be present.

## Limitations

- Adduct regex pattern correctness depends on accurate upstream field extraction; malformed ADDUCT field values may bypass validation if regex does not account for variant formats (e.g. spacing, parentheses, case). FragHub documentation notes 'fix adduct regex pattern' as a recent correction, implying prior false negatives/positives.
- Identifier normalization (SMILES canonicalization, InChI recalculation via RDkit) must complete before completeness check; if RDkit or PubChem offline data is stale or corrupted, normalized identifiers may be invalid or missing, causing spurious deletions.
- Duplicate removal by SPLASH key (post-completeness check) may identify spectra as duplicates that differ slightly in metadata (e.g., same peaks but different instrument name or collision energy); current implementation does not preserve metadata variants, so one record is lost.
- No explicit handling of edge cases in GC spectra: the skill applies precursor m/z and adduct checks to all GC spectra uniformly, but GC-MS typically does not record precursor m/z (molecular ion may be absent or weak). Manual annotation with '_GC' suffix is required to flag GC-only files, but this convention is not enforced during parsing.
- The skill requires prior specification of valid ionmode values ('pos', 'neg'); ionmode field values outside this set will not trigger adduct–ionmode validation, potentially allowing inconsistent records to pass through.

## Evidence

- [discussion] Delete spectrum if no SMILES AND no InChI AND no InChIKey: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [discussion] Adduct–ionmode consistency rule for positive/negative ionmode: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [discussion] Bad adduct filtering: "removing no or bad adduct spectrum"
- [discussion] Deletion logging for traceability: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [readme] Rationale for completeness checks in FragHub standardization workflow: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [other] Metadata field extraction during MSP parsing: "Parse spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification, handling missing or malformed entries."
