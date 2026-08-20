---
name: psm-spectrum-identifier-regex-extraction
description: Use when when you have PSM identifications from a search engine (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- MS²Rescore is a tool for rescoring peptide-spectrum matches
- Accepted ProForma modification labels in :py:mod:`psm_utils`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2rescore_immunopeptidome_rescoring_cq
    doi: 10.1002/pmic.202300336
    title: MS2Rescore (immunopeptidome rescoring)
  dedup_kept_from: coll_ms2rescore_immunopeptidome_rescoring_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/pmic.202300336
  all_source_dois:
  - 10.1002/pmic.202300336
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PSM-spectrum identifier regex extraction

## Summary

Extract common spectrum identifiers from PSM file spectrum_id fields and spectrum file titles using regex capture groups, then match them to link PSMs to their corresponding spectra. This is essential for MS²Rescore to correctly map peptide identifications to their experimental spectra before rescoring.

## When to use

When you have PSM identifications from a search engine (e.g., MaxQuant, MSGFPlus, Mascot) and spectrum files (mzML or mgf format) that use different naming schemes or formats for their spectrum identifiers, and you need to establish a one-to-one mapping between PSMs and spectra before rescoring. Typical triggers: spectrum file titles contain scan numbers or indices in a format different from the PSM file's spectrum_id field, or both files use custom identifier patterns that must be extracted and normalized.

## When NOT to use

- PSM and spectrum identifiers already match directly by string equality without requiring regex extraction or normalization
- Spectrum files are not available or are not in supported mzML/mgf formats
- The PSM file has already been FDR-filtered or contains only a subset of identifications, as MS²Rescore requires all target and decoy PSMs

## Inputs

- PSM file from search engine (supported formats: MS Amanda .csv, Sage .sage.tsv, PeptideShaker .mzid, ProteomeDiscoverer .msf, MSGFPlus .mzid, Mascot .mzid, MaxQuant msms.txt, X!Tandem .xml, PEAKS .mzid)
- Spectrum file in mzML or mgf format
- Regex pattern for spectrum ID extraction (spectrum_id_pattern)
- Regex pattern for PSM ID extraction (psm_id_pattern)

## Outputs

- PSM-to-spectrum mapping table (data structure linking each PSM to its matched spectrum)
- List of unmatched PSMs (for error reporting)

## How to apply

Define two regex patterns with at least one capturing group each: `spectrum_id_pattern` to extract identifiers from spectrum file titles (e.g., mzML spectrum IDs or MGF titles), and `psm_id_pattern` to extract identifiers from the PSM file's spectrum_id field. Load the PSM file and apply psm_id_pattern to each PSM's spectrum_id field, capturing the scan number or index. Load the spectrum file and apply spectrum_id_pattern to each spectrum's title or identifier field. Match the extracted identifiers using string equality to establish the PSM-to-spectrum mapping. Return a mapping table linking each PSM to its matched spectrum, and flag any unmatched PSMs for error reporting. Both regex patterns must match the entire identifier string and return the same extracted identifier for successful linking.

## Related tools

- **MS²Rescore** (Platform that performs PSM-spectrum mapping and rescoring; orchestrates the entire workflow including regex-based identifier linking) — https://github.com/compomics/ms2rescore
- **psm_utils** (Library for parsing and manipulating PSM files from multiple search engines; provides standardized access to PSM data including spectrum_id fields) — https://github.com/compomics/psm_utils

## Evaluation signals

- All PSMs in the input file are successfully matched to exactly one spectrum (no duplicates or orphaned PSMs after mapping)
- Unmatched PSMs are minimal and identifiable: only those with spectrum identifiers that do not exist in the spectrum file
- The extracted identifiers from both patterns are identical in format and value for matched PSM-spectrum pairs (string equality check passes)
- The regex patterns correctly handle edge cases such as multiple capture groups in the pattern; only the first capture group is used for matching
- The generated mapping table contains no null or empty spectrum assignments for PSMs that should have been matched

## Limitations

- Regex patterns must be manually defined and validated for each combination of search engine output and spectrum file format; incorrect patterns result in no or partial matching
- If PSM or spectrum files use inconsistent identifier formats (e.g., some scan numbers zero-padded, others not), the regex patterns must account for this normalization or matching will fail
- Search engines that do not report spectrum identifiers in their output files, or spectrum files with corrupted or missing identifier fields, will produce unmatched PSMs
- The mapping requires exact string equality after regex extraction; if spectrum identifiers are present but in a format not captured by the pattern, PSMs will be orphaned

## Evidence

- [other] MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file spectrum_id fields—that must match the entire string and return the same identifier to link PSMs to spectra.: "MS²Rescore uses two regex patterns with single capture groups—``spectrum_id_pattern`` to extract identifiers from spectrum file titles and ``psm_id_pattern`` to extract identifiers from PSM file"
- [intro] Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra...two options are available to map PSMs to spectra: ``spectrum_id_pattern`` and: "Essential for MS²Rescore to function correctly is linking the search engine PSMs to the original spectra"
- [intro] Both ``mzML`` and ``mgf`` formats are supported: "Both ``mzML`` and ``mgf`` formats are supported"
- [other] 1. Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index. 2. Load spectrum file (mzML or MGF format) and extract spectrum identifiers from spectrum titles using the spectrum_id_pattern regex with at least one capturing group. 3. Match extracted PSM identifiers to spectrum identifiers using string equality to establish the PSM-to-spectrum mapping.: "Load PSM file and extract spectrum identifiers using the psm_id_pattern regex with at least one capturing group to isolate the scan number or index"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
