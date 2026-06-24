---
name: library-spectrum-database-format-parsing
description: Use when you have experimental MS/MS spectra (from mzML, mzXML, or raw
  instrument formats) and wish to match them against a reference spectral library
  provided in MSP or CSV format. The skill is required as the first step before similarity
  scoring and candidate ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - TandemMatch
  - IonToolPack
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.4c00146
  title: PeakQC
evidence_spans:
- 'TandemMatch: MS/MS spectral library matching with support for MSP and CSV library
  formats.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakqc_cq
    doi: 10.1021/jasms.4c00146
    title: PeakQC
  dedup_kept_from: coll_peakqc_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00146
  all_source_dois:
  - 10.1021/jasms.4c00146
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# library-spectrum-database-format-parsing

## Summary

Parse and extract spectral reference data from MSP and CSV library formats to enable MS/MS spectral library matching. This skill transforms raw library files into structured peak and metadata records suitable for cosine similarity or dot-product scoring against experimental spectra.

## When to use

Apply this skill when you have experimental MS/MS spectra (from mzML, mzXML, or raw instrument formats) and wish to match them against a reference spectral library provided in MSP or CSV format. The skill is required as the first step before similarity scoring and candidate ranking.

## When NOT to use

- Library data is already in a proprietary database or binary format not explicitly listed as MSP or CSV
- Experimental spectra lack precursor m/z or retention time information needed for matching
- Input spectra are MS1-only (no MS/MS fragmentation data available)

## Inputs

- MSP library file (text format with spectrum metadata and peak lists)
- CSV library file (tabular format with spectrum identifiers and fragment ions)
- Experimental MS/MS spectral data (mzML, mzXML, or raw instrument format)

## Outputs

- Parsed spectral library records (reference spectrum identities, fragment m/z, intensities)
- Matched library spectra ranked by similarity score
- Results file (CSV or JSON) with spectrum metadata, library accession, match score, and fragment ion assignments

## How to apply

Load the spectral library file in either MSP or CSV format and parse it to extract reference spectrum identities, fragment m/z values, and intensities for each library entry. MSP files typically contain spectrum metadata headers followed by peak lists; CSV files contain tabular rows of spectrum accessions and fragment ion data. Store the parsed library entries in memory or indexed structure. The TandemMatch module implements this parsing and subsequent matching workflow: after loading the reference library, it applies cosine similarity or dot-product scoring to each experimental MS/MS spectrum against all library entries, filters candidates using a similarity threshold and precursor m/z mass tolerance window, ranks matches by score, and outputs results with spectrum metadata, library accession, match score, and fragment ion assignments.

## Related tools

- **TandemMatch** (Implements MS/MS spectral library matching with MSP and CSV library format parsing, scoring, filtering, and ranking of candidate matches) — https://github.com/pnnl/IonToolPack
- **IonToolPack** (Software suite housing TandemMatch and providing omics-agnostic MS data processing with GUI interface) — https://github.com/pnnl/IonToolPack

## Evaluation signals

- All library entries are successfully parsed without errors or dropped records; verify by comparing input file line count (for CSV) or spectrum count (for MSP) against parsed record count
- Fragment m/z values and intensities are correctly extracted and fall within expected ranges for the instrument and ionization mode
- Precursor m/z values parsed from library metadata match expected mass ranges and are consistent with chemical composition of reference compounds
- Matched results include non-empty library accession, match score, and fragment ion assignment fields; check that match score is within [0, 1] range for normalized similarity metrics
- Output file schema matches expected structure (CSV or JSON) with all required columns or fields populated for each match

## Limitations

- No changelog found in repository documentation, limiting visibility into format compatibility and parser version history
- MSP and CSV format specifications and strictness of parsing (e.g., handling malformed headers, missing fields, or non-standard delimiters) are not detailed
- Library matching performance and scalability with very large libraries (millions of spectra) are not characterized
- Support for proprietary or vendor-specific library formats (e.g., NIST .msp dialects, instrument-specific formats) is not discussed

## Evidence

- [other] Load spectral library from MSP or CSV format, extracting reference spectrum identities, fragment m/z values, and intensities.: "Load spectral library from MSP or CSV format, extracting reference spectrum identities, fragment m/z values, and intensities."
- [readme] TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats.: "TandemMatch: MS/MS spectral library matching with support for MSP and CSV library formats."
- [other] Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries.: "Apply cosine similarity or dot-product scoring to compare each experimental MS/MS spectrum against all library entries."
- [other] Filter candidate matches using a similarity threshold and mass tolerance window on precursor m/z.: "Filter candidate matches using a similarity threshold and mass tolerance window on precursor m/z."
- [other] Rank matched library spectra by score and output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to a structured results file (CSV or JSON).: "Rank matched library spectra by score and output matched records with spectrum metadata, library accession, match score, and fragment ion assignments to a structured results file (CSV or JSON)."
