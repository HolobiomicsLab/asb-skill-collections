---
name: adduct-regex-pattern-matching
description: Use when ingesting mass spectrometry spectra from heterogeneous databases or libraries where adduct annotations may be incomplete, incorrectly formatted, or inconsistent with the ionization mode. Use it before downstream analysis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - Python 3.12
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

# adduct-regex-pattern-matching

## Summary

Validate and enforce ionmode–adduct consistency in mass spectrometry spectra by applying regex pattern matching to detect and flag spectra with mismatched or malformed adduct annotations. This skill removes spectra where negative adducts appear in positive-mode ionization (or vice versa) and filters out spectra with missing or syntactically invalid adduct strings.

## When to use

Apply this skill when ingesting mass spectrometry spectra from heterogeneous databases or libraries where adduct annotations may be incomplete, incorrectly formatted, or inconsistent with the ionization mode. Use it before downstream analysis (e.g., fragmentation prediction, spectral matching) to ensure data integrity and prevent false or uninformative comparisons.

## When NOT to use

- Input spectra already have validated, curated adduct annotations from a trusted single source (e.g., direct instrumental output with no aggregation risk).
- The analysis workflow is agnostic to ionmode or adduct identity and does not require strict consistency (e.g., generic mass spectral clustering that ignores ionization context).
- Spectra are from a single, well-controlled LC-MS/MS experiment where all adducts are known a priori to be correct and complete.

## Inputs

- Spectrum dataset (JSON, CSV, MSP, or MGF format) with ionmode and adduct fields parsed
- Adduct regex pattern specification (e.g., matching '[M+H]+', '[M-H]-', and other standard adducts)
- Ionization mode values ('pos' or 'neg') per spectrum

## Outputs

- Filtered spectrum dataset (valid spectra only)
- Deletion log with detailed reasons (ionmode–adduct mismatch, missing adduct, malformed adduct) per removed spectrum
- DELETION_REASONS folder containing detailed deletion metadata

## How to apply

Load the spectrum dataset and parse the ionmode field ('pos' or 'neg') and adduct field (e.g., '[M+H]+', '[M-H]-') from each spectrum record. For each spectrum, check ionmode–adduct compatibility using regex pattern matching: positive adducts (containing '+' and typically '+' in the adduct string) must only appear in 'pos' mode, and negative adducts (containing '−' and typically '−' in the adduct string) must only appear in 'neg' mode. Flag and delete spectra that violate this rule, have null/missing adduct fields, or have malformed adduct strings that fail regex validation. Log the deletion reason (ionmode–adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder for audit and quality control. Retain only spectra with valid, syntactically correct adduct annotations consistent with their ionmode.

## Related tools

- **Python 3.12** (Runtime environment for parsing spectra, executing regex matching, and logging deletion reasons)
- **FragHub** (Mass spectrometry data standardization pipeline that integrates adduct regex pattern matching as a core filtering step) — https://github.com/eMetaboHUB/FragHub
- **spectra-hash** (Spectral identifier generation (SPLASH); integrated into FragHub for duplicate detection and spectrum tracking) — https://github.com/berlinguyinca/spectra-hash

## Examples

```
for each spectrum in dataset: if spectrum.ionmode == 'pos' and re.search(r'\[M-[^+]*\]-', spectrum.adduct): flag_for_deletion(spectrum, 'neg_adduct_in_pos_mode'); elif spectrum.ionmode == 'neg' and re.search(r'\[M\+[^-]*\]\+', spectrum.adduct): flag_for_deletion(spectrum, 'pos_adduct_in_neg_mode'); elif not spectrum.adduct or not re.match(r'^\[[^\]]+\][+-]$', spectrum.adduct): flag_for_deletion(spectrum, 'missing_or_malformed_adduct')
```

## Evaluation signals

- All remaining spectra have adduct annotations that match their ionmode: positive adducts only in 'pos' mode, negative adducts only in 'neg' mode.
- No remaining spectrum has a null, empty, or malformed adduct field (all adducts pass regex validation).
- Deletion log is complete and accounts for all removed spectra, with each entry citing the specific deletion reason (ionmode–adduct mismatch, missing adduct, or bad format).
- Spectrum count reduction is tracked and documented; downstream spectral matching and fragmentation prediction tools run without adduct-related errors.
- Regex pattern correctly identifies standard adduct forms (e.g., '[M+H]+', '[M-H]-', '[M+Na]+', '[M+Cl]-') and rejects malformed variants (e.g., 'M+H', '[M+H', 'M+2H').

## Limitations

- Regex pattern correctness depends on accurate specification of adduct nomenclature; regional or instrument-specific adduct naming conventions may not be captured by a single pattern.
- Missing or null adduct fields result in spectrum deletion, which may discard otherwise valid spectra if adduct information was optional or inferred from other metadata.
- No automatic inference or correction of adducts; if an adduct is malformed but interpretable (e.g., 'M+H' instead of '[M+H]+'), the spectrum is deleted rather than repaired.
- The skill does not validate whether an adduct is chemically reasonable for a given molecule or ionization method; only syntax and ionmode consistency are checked.
- Multi-threaded or chunked processing may complicate sequential logging; chunk size auto-calculation is mentioned but not detailed, risking incomplete or duplicated deletion logs.

## Evidence

- [other] FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct annotations.: "filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct annotations"
- [other] For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg mode), using adduct regex pattern matching.: "check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg mode), using adduct"
- [other] Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation.: "Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation"
- [other] Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder.: "Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder"
- [readme] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [readme] removing no or bad adduct spectrum: "removing no or bad adduct spectrum"
- [readme] fix adduct regex pattern: "fix adduct regex pattern"
- [readme] modifiy adduct ionmode check with "pos", "neg" in adduct dico: "modifiy adduct ionmode check with "pos", "neg" in adduct dico"
