---
name: deletion-reason-logging-and-traceability
description: Use when when processing OMSLs (Open Mass Spectra Libraries) with heterogeneous data quality, inconsistent annotations, or mixed ionmode/chromatographic modes (LC/GC), and you need to track which spectra were discarded, why, and potentially recover or reprocess them in future iterations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Python 3.12
  - FragHub
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

# deletion-reason-logging-and-traceability

## Summary

A data quality and provenance practice that systematically logs detailed reasons for every spectrum deletion during mass spectrometry data standardization, enabling traceability and audit trails for downstream validation and reprocessing decisions.

## When to use

When processing OMSLs (Open Mass Spectra Libraries) with heterogeneous data quality, inconsistent annotations, or mixed ionmode/chromatographic modes (LC/GC), and you need to track which spectra were discarded, why, and potentially recover or reprocess them in future iterations. Essential when combining spectra from multiple databases or when supporting incremental processing where only new spectra are added to prior runs.

## When NOT to use

- When processing curated, pre-validated spectra libraries with <1% expected deletion rate; logging overhead may outweigh traceability value.
- When input data is streaming and not persisted; deletion logs require persistent storage to be queryable.
- When strict real-time performance requirements prohibit I/O for every filtered spectrum; batch deletion logging may be an alternative.

## Inputs

- spectrum dataset with ionmode, adduct, SMILES, InChI, InChIKey, precursor m/z, and peak list fields
- filter configuration (minimum peaks, entropy threshold, m/z range, peak intensity normalization parameters)
- spectrum records parsed from .json, .csv, .msp, or .mgf files

## Outputs

- filtered spectrum dataset (spectra passing all validation checks)
- DELETION_REASONS subfolder containing detailed deletion logs (one entry per deleted spectrum)
- deletion summary statistics (count by reason category, source library breakdown)

## How to apply

For each spectrum flagged for deletion during filtering (ionmode-adduct mismatch, missing/malformed adduct annotation, missing structural identifiers, or entropy score below threshold), write a detailed deletion log entry to a DELETION_REASONS subfolder with: (1) the spectrum record identifier, (2) the specific reason category (e.g., 'neg adduct in pos spectrum', 'missing adduct', 'bad adduct format', 'insufficient peaks', 'low entropy score'), (3) the rejected values (ionmode, adduct string, entropy score), and (4) the filtering rule that triggered the removal. Store these logs in a structured, query-able format (e.g., TSV or JSON per spectrum) so that deletion ratios, patterns (e.g., % of spectra failing adduct validation vs. structural identifier checks), and edge cases can be analyzed. This enables retrospective investigation if thresholds are adjusted or if spectra from a particular source library systematically fail.

## Related tools

- **Python 3.12** (Parsing spectrum records, validating adduct regex patterns, writing deletion logs to DELETION_REASONS subfolder)
- **FragHub** (Reference implementation for mass spectrometry data standardization and filtering with structured deletion reason logging) — https://github.com/eMetaboHUB/FragHub

## Evaluation signals

- All deleted spectra have a corresponding deletion log entry in DELETION_REASONS subfolder with non-null reason field.
- Deletion reason categories match the filter rules applied (ionmode-adduct mismatch, missing adduct, bad adduct format, insufficient peaks, entropy score, structural identifier validation).
- Deletion log entries contain spectrum identifier, rejected field values, and the specific rule/threshold that triggered removal.
- Deletion summary counts (by reason category) sum to total spectra removed; no records lost or duplicated.
- Deletion logs are queryable (e.g., can retrieve all spectra failing adduct validation vs. entropy check), enabling root-cause analysis of rejection patterns.

## Limitations

- Storage overhead: one log entry per deleted spectrum can generate large DELETION_REASONS subdirectories for libraries with high rejection rates; may require periodic archival.
- Logging granularity: if a spectrum fails multiple filter rules, only the first encountered deletion reason is typically logged; concurrent failures are not captured.
- Regex pattern fixes (adduct validation) may change between runs; prior deletion logs cannot be reused without re-running filters, limiting incremental processing effectiveness.
- No explicit standard for deletion log schema in FragHub documentation; implementation may vary across tools, hindering interoperability.

## Evidence

- [other] improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [other] Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder.: "Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder."
- [readme] FragHub separates spectra based on different experimental parameters such as polarity (positive/negative), chromatographic mode (LC/GC), and acquisition type (experimental/in silico): "FragHub separates spectra based on different experimental parameters such as polarity (positive/negative), chromatographic mode (LC/GC), and acquisition type (experimental/in silico)"
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [readme] FragHub save the splash keys of previous spectra processed. So that at the next update, only new spectra from the database are processed, and added to previous FragHub processes.: "FragHub save the splash keys of previous spectra processed. So that at the next update, only new spectra from the database are processed, and added to previous FragHub processes."
