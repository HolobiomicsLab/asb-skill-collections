---
name: json-spectral-data-processing
description: Use when you have raw or semi-curated mass spectrometry spectral data
  in JSON, CSV, MSP, or MGF format from multiple open mass spectra libraries (OMSLs)
  and need to standardize field names, validate chemical identifiers (SMILES, InChI,
  InChIKey), remove duplicates, filter by quality criteria.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - spectra-hash
  - FragHub
  - Python 3.12
  - RDkit
  - PubChem
  - Classyfire
  - NPclassifier
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

# JSON Spectral Data Processing

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Standardize and organize mass spectrometry spectral data from open libraries by loading FragHub JSON format spectra, applying quality filters, recalculating chemical identifiers, and deduplicating via SPLASH keys. This skill ensures data consistency, removes inconsistent records, and produces analysis-ready spectra compatible with MSdial, MZmine, and other metabolomics software.

## When to use

You have raw or semi-curated mass spectrometry spectral data in JSON, CSV, MSP, or MGF format from multiple open mass spectra libraries (OMSLs) and need to standardize field names, validate chemical identifiers (SMILES, InChI, InChIKey), remove duplicates, filter by quality criteria (precursor m/z, adduct consistency, ionization mode), and organize spectra by experimental parameters (LC/GC, positive/negative polarity, experimental vs. in-silico) before downstream analysis or database integration.

## When NOT to use

- Input spectra already possess validated, non-redundant SPLASH keys and verified chemical identifiers; re-processing would be redundant.
- Analysis requires preservation of all raw spectral records including those with missing or invalid chemical identifiers; this skill removes such records by design.
- Input data is from a single, already-curated mass spectrometry database with internally enforced consistency; the standardization and deduplication overhead may not be justified.

## Inputs

- Spectral data files in FragHub JSON format
- Mass spectrometry spectral records in CSV, MSP, or MGF format
- Chemical structure identifiers (SMILES, InChI, InChIKey)
- Precursor m/z values
- Adduct annotations with ionization mode labels

## Outputs

- Standardized and deduplicated spectral dataset in FragHub JSON format
- Organized spectra separated by experimental parameters (LC/GC, polarity, experimental/in-silico)
- Spectral records in user-selected output formats (JSON, CSV, MSP, MGF)
- Deletion log with reasons for removed spectra
- SPLASH keys assigned to each retained spectrum

## How to apply

Load spectral data files (JSON, CSV, MSP, MGF) using Python 3.12 into FragHub's standardization pipeline. Normalize field names and chemical identifiers (SMILES, InChI, InChIKey) by recalculation using RDkit and PubChem offline data; verify adduct information consistency with ionization mode (reject negative adducts in positive-mode spectra and vice versa). Compute or retrieve SPLASH keys for each spectrum using the spectra-hash tool, then group spectra by identical SPLASH key and retain only the first occurrence to remove duplicates. Apply peak-list filtering to streamline m/z–intensity pairs. Filter out spectra lacking SMILES AND InChI AND InChIKey simultaneously, or missing precursor m/z or valid adduct information. Separate deduplicated spectra by experimental parameters (LC vs. GC, polarity, experimental vs. in-silico) into organized subdirectories, write outputs in user-selected formats (JSON, CSV, MSP, MGF), and log all deleted spectra with deletion reasons in a DELETION_REASONS subfolder for traceability.

## Related tools

- **spectra-hash** (Computes or retrieves SPLASH keys (SPectraL hASH) for each spectrum to enable systematic duplicate identification and removal) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (Main standardization and organization pipeline that integrates spectra-hash, applies quality filters, normalizes chemical identifiers, and orchestrates spectral separation by experimental parameters) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (Execution environment and primary language for loading spectral datasets, computing identifiers, grouping spectra, and writing deduplicated output)
- **RDkit** (Recalculates and normalizes chemical structure identifiers (SMILES, InChI, InChIKey) for consistency)
- **PubChem** (Offline data source for completing chemical names and descriptors, and ontologic information lookup by InChIKey)
- **Classyfire** (Local data source for chemical compound classification, integrated into standardization workflow)
- **NPclassifier** (Local data source for natural product classification, integrated into standardization workflow)

## Evaluation signals

- All retained spectra possess valid, consistent SPLASH keys with no duplicate SPLASH values remaining in the output.
- Zero spectra in the final dataset lack SMILES or InChI or InChIKey (all three must be present; missing any one triggers removal).
- No retained spectrum has a negative adduct in positive-mode ionization, or a positive adduct in negative-mode ionization; adduct–ionmode consistency is 100%.
- All deleted spectra are logged in the DELETION_REASONS subfolder with explicit, detailed reasons (e.g., 'no SMILES, InChI, and InChIKey', 'negative adduct in positive ionmode', 'missing precursor m/z').
- Output spectral records conform to the FragHub JSON format and are successfully parsed by downstream tools (MSdial, MZmine, Flash Entropy Search).

## Limitations

- Spectra deemed inconsistent—those lacking SMILES AND InChI AND InChIKey simultaneously, or missing precursor m/z or valid adduct information—are irreversibly removed; recovery of raw records requires backups.
- SPLASH-based deduplication retains only the first occurrence of duplicate spectra; other duplicate variants (differing in metadata, annotations, or provenance) are discarded without hierarchical merging.
- RDkit and PubChem offline data updates are not automated; stale local data may yield inconsistent or incorrect chemical identifier recalculations; reproducibility of Classyfire and NPclassifier local data sources is not documented.
- Automatic chunk-size calculation for multi-threading performance is mentioned but comparative benchmarking against fixed chunk sizes is not provided; actual performance improvement is unvalidated.
- macOS and Linux support has been removed as of version 1.4.1; tool is Windows-only.

## Evidence

- [discussion] Refactoring duplicatas removal, now by sames SPLASH key.: "Refactoring duplicatas removal, now by sames SPLASH key."
- [readme] FragHub standardizes field names and values of MS spectra from various databases, ensuring data consistency and compatibility.: "FragHub standardizes field names and values of MS spectra from various databases, ensuring data consistency and compatibility."
- [other] Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal.: "Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [discussion] Now deleting spectrum with no SMILES no InChI **AND no inchikey**.: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [readme] Standardized spectra produced by FragHub are compatible with multiple analysis software, including MSdial, MZmine, and Flash Entropy Search, providing users with maximum flexibility in choosing analysis tools.: "Standardized spectra produced by FragHub are compatible with multiple analysis software, including MSdial, MZmine, and Flash Entropy Search, providing users with maximum flexibility in choosing"
- [discussion] direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub.: "direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub."
- [discussion] Now completing NAMES and descriptor from RDkit and PubChem datas (offline).: "Now completing NAMES and descriptor from RDkit and PubChem datas (offline)."
- [discussion] improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
