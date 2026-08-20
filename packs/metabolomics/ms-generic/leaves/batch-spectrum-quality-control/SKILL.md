---
name: batch-spectrum-quality-control
description: Use when when ingesting spectra from multiple open mass spectrometry libraries (OMSLs) in .mgf, .msp, .json, or .csv format and you observe mixed experimental protocols, inconsistent adduct annotations, or partial metadata.
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
  - mass-spectrometry
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

# Batch Spectrum Quality Control

## Summary

Remove mass spectra that violate ionmode–adduct polarity consistency, lack chemical identifiers, or fail quality thresholds during bulk standardization of open mass spectrometry libraries. This skill detects and logs mismatched adducts, missing annotations, and low-entropy spectra to ensure only high-quality, annotated spectra are retained.

## When to use

When ingesting spectra from multiple open mass spectrometry libraries (OMSLs) in .mgf, .msp, .json, or .csv format and you observe mixed experimental protocols, inconsistent adduct annotations, or partial metadata. Apply this skill before standardization pipelines to eliminate spectra that would fail downstream analysis in MSdial, MZmine, or Flash Entropy Search.

## When NOT to use

- Input spectra are already pre-filtered and curated by a single, trusted source with known consistent ionmode–adduct pairing.
- Spectra lack adduct annotations by experimental design (e.g., neutral loss or rearrangement spectra where adduct is undefined).
- You require retention of all spectral data including outliers for meta-analysis or sensitivity studies; QC filtering will remove potentially valuable edge cases.

## Inputs

- Mass spectrum records with ionmode field ('pos' or 'neg')
- Adduct annotations (e.g., '[M+H]+', '[M-H]−')
- Chemical identifiers (SMILES, InChI, InChIKey)
- Peak arrays with m/z and intensity values
- Entropy score (calculated during processing)

## Outputs

- Filtered spectrum dataset (spectra passing all QC checks)
- DELETION_REASONS subfolder with per-spectrum deletion justifications
- Standardized .mgf, .msp, .json, or .csv output files with valid spectra only

## How to apply

Load the spectrum dataset and parse ionmode ('pos' or 'neg') and adduct fields from each record. For each spectrum, validate that adducts are compatible with ionmode using regex pattern matching: positive adducts (e.g., [M+H]+, [M+Na]+) must appear only in positive-mode spectra; negative adducts (e.g., [M-H]−) only in negative-mode spectra. Flag and delete spectra with ionmode–adduct mismatches, missing or null adduct fields, or malformed adduct strings that fail regex validation. Additionally, remove spectra lacking SMILES, InChI, *and* InChIKey simultaneously, and those below a minimum entropy threshold. Log the detailed deletion reason (e.g., 'ionmode-adduct mismatch', 'missing adduct', 'bad adduct format', 'missing identifiers', 'low entropy score') for each removed spectrum to a DELETION_REASONS subfolder for traceability and audit.

## Related tools

- **Python 3.12** (Primary runtime for parsing spectrum records, regex validation of adduct strings, and logging deletion reasons)
- **spectra-hash (SPLASH)** (Generates spectral identifiers for duplicate detection and traceability; integrated into FragHub for cross-batch consistency checks) — github.com/berlinguyinca/spectra-hash
- **FragHub** (End-to-end framework implementing batch spectrum QC including ionmode–adduct validation, entropy scoring, and deletion logging) — github.com/eMetaboHUB/FragHub

## Evaluation signals

- Deletion log reports zero spectra with valid ionmode–adduct pairs mismatched (e.g., [M-H]− in positive-mode spectra).
- All retained spectra contain non-null, non-empty adduct fields that match their ionmode polarity via regex.
- No retained spectrum lacks all three of SMILES, InChI, and InChIKey simultaneously.
- Entropy scores of all retained spectra are above or equal to the configured minimum threshold.
- DELETION_REASONS subfolder contains one log entry per deleted spectrum with a specific reason category and count matches total deletions.

## Limitations

- Adduct regex patterns must be carefully maintained; incorrect or incomplete patterns will silently pass malformed adducts or reject valid ones. FragHub documentation does not specify the exact regex syntax or coverage of all adduct types.
- Entropy score calculation and threshold are not explicitly defined in the README; no reference to standard entropy metrics (Shannon, Rényi) is provided, making reproducibility difficult.
- GC spectra exception handling is mentioned but not fully specified: which instruments trigger 'GC mode' and bypass precursor m/z checks is not documented.
- The skill assumes ionmode is reliably recorded in source spectra; if ionmode is missing or ambiguous, the filter cannot validate adduct polarity.
- Offline RDkit and PubChem data used for chemical identifier recalculation may become stale; no versioning or update strategy is documented.

## Evidence

- [other] FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct annotations.: "FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct"
- [other] For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg mode), using adduct regex pattern matching.: "For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg"
- [other] Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder.: "Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [other] Now deleting spectrum with no SMILES no InChI **AND no inchikey**.: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [readme] remove_spectrum_under_entropy_score(score): The entropy score of the spectrum is calculated during processing. If a spectrum has an entropy score lower than the minimum required, it is deleted.: "The entropy score of the spectrum is calculated during processing. If a spectrum has an entropy score lower than the minimum required, it is deleted."
