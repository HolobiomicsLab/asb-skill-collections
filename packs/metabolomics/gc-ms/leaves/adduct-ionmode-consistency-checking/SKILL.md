---
name: adduct-ionmode-consistency-checking
description: Use when parsing, standardizing, or filtering MS spectra from mixed or
  heterogeneous databases where adduct assignment may be manually entered, auto-inferred,
  or missing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Python 3.12
  - spectra-hash (SPLASH)
  - FragHub
  techniques:
  - GC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: eMetaboHUB/FragHub
  license_tier: noncommercial
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-ionmode-consistency-checking

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Validates that adduct polarity matches ionization mode in mass spectra, removing spectra with contradictory adduct–ionmode pairs (e.g., negative adducts in positive ionmode or positive adducts in negative ionmode). This ensures chemical plausibility and data integrity in standardized spectral libraries.

## When to use

Apply this skill when parsing, standardizing, or filtering MS spectra from mixed or heterogeneous databases where adduct assignment may be manually entered, auto-inferred, or missing. It is essential before ontologic enrichment, spectral matching, or library export to catch metadata inconsistencies that would produce chemically impossible ions.

## When NOT to use

- Input spectra have no adduct field or ionmode field (skip this filter; prioritize other metadata validation)
- Spectra are from GC–MS or other methods where ionmode may not apply or adduct assignment is instrumentally determined and already validated upstream
- Input is already a curated, literature-validated spectral library with manually reviewed adduct assignments

## Inputs

- parsed mass spectra with ionmode field (pos/neg) and adduct field populated
- adduct dictionary mapping adduct strings to charge polarity
- spectrum metadata records (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY)

## Outputs

- filtered spectrum list with adduct–ionmode-inconsistent entries removed
- DELETION_REASONS log file with spectrum identifiers and reason strings (e.g., 'negative adduct in positive ionmode')

## How to apply

For each spectrum in the input set, extract the ionmode field (pos/neg) and the adduct field (e.g., [M+H]+, [M-H]-, [M+Na]+). Apply conditional logic: if ionmode is 'pos', flag any negative adduct (e.g., [M-H]-, [M-Cl]-) as invalid; if ionmode is 'neg', flag any positive adduct (e.g., [M+H]+, [M+Na]+) as invalid. Delete the entire spectrum and log the reason (e.g., 'negative adduct in positive ionmode') to a DELETION_REASONS subdirectory for audit. Spectra with valid ionmode–adduct pairs proceed to downstream filters. This check is typically applied after peak validation but before duplicate removal and structural identifier standardization.

## Related tools

- **Python 3.12** (implementation language for adduct–ionmode validation logic, line-by-line spectrum parsing, and deletion logging)
- **spectra-hash (SPLASH)** (used downstream after consistency checking to assign unique spectral identifiers for duplicate removal and database indexing) — github.com/berlinguyinca/spectra-hash
- **FragHub** (parent application that orchestrates adduct–ionmode consistency checking as a filter step during MSP/.mgf/.json/.csv file parsing and standardization) — github.com/eMetaboHUB/FragHub

## Examples

```
# Pseudocode reflecting the workflow in task_004:
for spectrum in parsed_spectra:
  ionmode = spectrum.get('IONMODE')  # e.g., 'pos' or 'neg'
  adduct = spectrum.get('ADDUCT')    # e.g., '[M+H]+' or '[M-H]-'
  adduct_polarity = adduct_dict[adduct]  # lookup charge from dictionary
  if (ionmode == 'pos' and adduct_polarity < 0) or (ionmode == 'neg' and adduct_polarity > 0):
    log_deletion(spectrum_id, 'ionmode-adduct mismatch', 'DELETION_REASONS/')
    delete(spectrum)
  else:
    keep(spectrum)
```

## Evaluation signals

- All remaining spectra have ionmode–adduct pairs that respect polarity rules: positive ionmode contains only positive adducts; negative ionmode contains only negative adducts
- DELETION_REASONS log contains one entry per deleted spectrum with unique identifier and explicit reason ('negative adduct in positive ionmode' or 'positive adduct in negative ionmode')
- Spectrum count in output is ≤ input count; no spectra are duplicated or lost during deletion
- Spot-check: for a sample of deleted spectra in DELETION_REASONS, manually confirm that the flagged ionmode–adduct pair is indeed contradictory (e.g., ionmode='pos' with adduct='[M-H]-')
- Downstream spectral matching or feature detection shows no systematic bias toward false-positive matches due to implausible ionization states

## Limitations

- The filter assumes ionmode and adduct fields are present and populated; missing or null values must be handled by prior validation steps or a separate auto-assignment skill (e.g., auto-addition of [M+H]+ for in-silico spectra with missing adduct)
- Adduct dictionary must be comprehensive and correctly map adduct strings to polarity; if custom or non-standard adducts are present, they must be added to the dictionary or the spectrum will not be recognized as invalid
- GC–MS spectra may require exception handling: standard ionmode/adduct rules may not apply to electron ionization (EI) or other GC-specific ionization modes, requiring separate validation logic
- No automatic repair or correction is performed; all inconsistent spectra are deleted. If adduct is simply mis-entered, this approach sacrifices data rather than correcting it

## Evidence

- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [other] Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode.: "Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode."
- [discussion] improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [discussion] modifiy adduct ionmode check with "pos", "neg" in adduct dico.: "modifiy adduct ionmode check with "pos", "neg" in adduct dico."
