---
name: json-spectral-format-parsing
description: Use when when you have raw mass spectrometry spectral data in JSON format
  from open mass spectra libraries (OMSLs) or other sources and need to validate structural
  completeness, check for required metadata fields (SMILES, InChI, InChIKey, precursor
  m/z, adduct), and separate spectra by acquisition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Python 3.12
  - RDkit
  - FragHub
  techniques:
  - mass-spectrometry
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

# json-spectral-format-parsing

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Parse and validate mass spectrometry spectral data from JSON files conforming to ISO/IEC 20802-2:2016 and non-standard formats, extracting spectrum records with structural identifiers (SMILES, InChI, InChIKey), precursor m/z, adduct information, and peak lists. This skill enables standardized ingestion of spectral datasets into downstream processing pipelines.

## When to use

When you have raw mass spectrometry spectral data in JSON format from open mass spectra libraries (OMSLs) or other sources and need to validate structural completeness, check for required metadata fields (SMILES, InChI, InChIKey, precursor m/z, adduct), and separate spectra by acquisition type (experimental vs. in silico) and ionization mode (positive/negative) for subsequent filtering or analysis.

## When NOT to use

- If your input is already in a standardized, pre-validated format (e.g., already processed FragHub output) and requires no structural identifier checking or adduct validation.
- If you need to merge spectra across multiple ionmodes or combine datasets with intentionally inconsistent adduct annotations—parsing will filter these out as invalid.
- If your JSON file uses a proprietary, undocumented schema that does not map to the ISO/IEC 20802-2:2016 or common OMSL conventions—custom parsing logic will be required.

## Inputs

- JSON-formatted spectral data file (ISO/IEC 20802-2:2016 or non-standard compatible)
- Spectral records with fields: SMILES, InChI, InChIKey, precursor m/z, adduct, ionmode, peak array

## Outputs

- Validated JSON spectral dataset with retained spectra (at least one structural identifier present)
- DELETION_REASONS log directory with detailed rationale for each filtered spectrum

## How to apply

Load the input JSON spectral data file, which may conform to the ISO/IEC 20802-2:2016 standard or non-standard formats. Iterate through each spectrum record and extract required fields: structural identifiers (SMILES, InChI, InChIKey), precursor m/z value, adduct information, and peak list arrays. Check for presence and non-emptiness of these fields; spectra lacking all three structural identifiers simultaneously (no SMILES AND no InChI AND no InChIKey) are flagged for deletion. Verify adduct ionmode consistency—remove spectra with negative adducts in positive ionmode or positive adducts in negative ionmode. Write valid spectra to output JSON file in the same format, and log deletion reasons (e.g., missing structural identifiers, adduct mismatch) to a DELETION_REASONS subdirectory with detailed rationale for traceability.

## Related tools

- **Python 3.12** (Primary runtime for JSON parsing, field extraction, and validation logic)
- **RDkit** (Validation and normalization of SMILES and InChI structural identifiers)
- **FragHub** (Complete pipeline tool that integrates JSON parsing with downstream filtering, standardization, and spectral organization) — https://github.com/eMetaboHUB/FragHub

## Evaluation signals

- All retained spectra contain at least one of SMILES, InChI, or InChIKey (none are completely absent).
- Adduct ionmode consistency: no spectrum in positive ionmode contains negative adducts (e.g., [M-H]-), and vice versa.
- Precursor m/z field is present and non-empty for all retained spectra.
- Peak array field contains at least the minimum number of peaks required (configurable; FragHub default is implied by filter checks).
- DELETION_REASONS log entries match the count and rationale of spectra filtered out (e.g., 'no SMILES AND no InChI AND no InChIKey', 'negative adduct in positive ionmode').

## Limitations

- Parser strictly enforces AND logic for structural identifier deletion: spectra are removed only if ALL three (SMILES, InChI, InChIKey) are absent simultaneously. If even one identifier is present, the spectrum is retained—no validation of identifier quality or mutual consistency is performed at this stage.
- Adduct validation occurs only if the adduct field is populated; spectra with missing adduct information are not automatically rejected by this parsing step (they may be rejected by later filtering stages or auto-populated with [M+H]+ or [M-H]- in in-silico workflows).
- Non-standard JSON formats may require custom field mapping before parsing; the ISO/IEC 20802-2:2016 standard field names are assumed by default.
- No explicit validation of InChIKey or SMILES chemical validity; presence is checked, but RDkit or PubChem normalization occurs in downstream steps (e.g., FragHub's descriptor completion).

## Evidence

- [other] Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats). Iterate through each spectrum record and check for the presence of SMILES, InChI, and InChIKey fields.: "Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats). Iterate through each spectrum record and check for the presence of SMILES, InChI, and"
- [other] a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at least one of these identifiers.: "a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at least one of these identifiers."
- [other] Write retained spectra to the output file in the same JSON format. Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale.: "Write retained spectra to the output file in the same JSON format. Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale."
- [readme] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [readme] Refactoring .json reader for standard ISO/IEC 20802-2:2016 .json and non-standard formats.: "Refactoring .json reader for standard ISO/IEC 20802-2:2016 .json and non-standard formats."
