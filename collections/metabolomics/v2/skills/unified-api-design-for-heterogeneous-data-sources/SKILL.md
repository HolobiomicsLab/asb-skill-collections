---
name: unified-api-design-for-heterogeneous-data-sources
description: Use when your analysis pipeline must ingest mass-spectrometry data from mixed vendor sources (e.g., Thermo RAW, Agilent .d, Waters .raw, and open mzML) without writing separate parser logic for each format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ProteoWizard Library and Tools
  - pwiz
derived_from:
- doi: 10.1021/acs.jproteome.9b00640
  title: Skyline (small molecules)
evidence_spans:
- The ProteoWizard Library and Tools are a set of modular and extensible open-source, cross-platform tools and software libraries
- github.com__ProteoWizard__pwiz
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_skyline_small_molecules_cq
    doi: 10.1021/acs.jproteome.9b00640
    title: Skyline (small molecules)
  dedup_kept_from: coll_skyline_small_molecules_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.9b00640
  all_source_dois:
  - 10.1021/acs.jproteome.9b00640
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unified-api-design-for-heterogeneous-data-sources

## Summary

Design and implement a single, vendor-agnostic API layer that normalizes access to mass-spectrometry data files across multiple proprietary and open formats (mzML, mzXML, vendor binary). This skill unifies spectrum metadata and intensity representation so downstream tools interact with one canonical interface rather than format-specific readers.

## When to use

Your analysis pipeline must ingest mass-spectrometry data from mixed vendor sources (e.g., Thermo RAW, Agilent .d, Waters .raw, and open mzML) without writing separate parser logic for each format. Use this skill when you want to hide format-specific conventions (scan ID naming, retention-time units, charge-state encoding, precursor m/z lookup) from application code and expose a uniform in-memory spectrum object with consistent fields (scan ID, retention time, m/z array, intensity array, precursor m/z, charge state).

## When NOT to use

- Input data is already a normalized, vendor-independent format (mzML, mzXML) and no legacy vendor formats are present—apply this skill only if you must support multiple heterogeneous sources.
- Your analysis pipeline is vendor-locked or designed exclusively for a single instrument type (e.g., only Thermo Orbitrap) and does not need cross-platform compatibility.
- You are working with non-mass-spectrometry data (e.g., genomics, image, tabular data) where format unification strategies differ fundamentally.

## Inputs

- Mass-spectrometry data file (vendor binary format: Thermo RAW, Agilent .d, Waters .raw, or open format: mzML, mzXML)
- File path or file descriptor to raw data file

## Outputs

- Unified spectrum iterator or query interface exposing normalized spectrum objects
- In-memory spectrum representation with canonical fields (scan ID, retention time, m/z array, intensity array, precursor m/z, charge state)

## How to apply

First, design a canonical spectrum data structure that captures essential metadata: scan ID, retention time, m/z values, intensity values, precursor m/z, and charge state. Second, implement file-format detection logic (by file extension or magic bytes) to route the input to the appropriate parser. Third, integrate or wrap existing parsers (ProteoWizard libraries, format-specific vendor SDKs, or community libraries like mzML parsers) to read raw spectra from the chosen format. Fourth, normalize each parsed spectrum into your unified representation, handling vendor-specific conventions (e.g., Thermo's scan numbering, Waters' drift-time fields). Finally, expose the normalized spectra through a single API interface—such as an iterator, random-access getter, or query method—that hides format-specific details from the caller. The key rationale is that a robust, pluggable development framework simplifies and unifies data file access, enabling rapid tool creation on top of the normalized layer.

## Related tools

- **ProteoWizard Library and Tools** (Provides modular C++ libraries, pluggable parsers, and reference implementations (mzML, mzIdentML) that unify vendor format ingestion and normalize spectra into canonical in-memory representation) — https://github.com/ProteoWizard/pwiz
- **pwiz** (Core open-source library and command-line tool suite (e.g., msconvert) that implements format detection, vendor SDK wrapping, and normalized spectrum API) — https://github.com/ProteoWizard/pwiz

## Evaluation signals

- All input spectra, regardless of source format, are parsed successfully into the canonical spectrum object with no missing or malformed fields (scan ID, retention time, m/z, intensity, precursor m/z, charge state).
- API calls to the unified interface return equivalent spectrum data and metadata for the same physical scan across different input formats (e.g., scan #100 from Thermo RAW and mzML should have identical m/z arrays and intensity arrays, within expected rounding).
- Downstream analysis tools can iterate or query spectra using the unified API without conditional logic or format-specific branching; same tool code handles all supported input formats.
- Format-specific metadata normalization is verifiable: vendor-specific retention-time units are converted to a canonical unit (e.g., seconds or minutes); charge state is consistently encoded; precursor m/z lookups follow a uniform rule across formats.
- Performance and memory usage are consistent across formats for equivalent spectral complexity (e.g., iteration speed and RAM footprint for a 100 MB dataset should not vary >20% based on input format).

## Limitations

- Vendor binary format support (e.g., Thermo RAW, Waters .raw) on Windows may require vendor-specific SDKs or restricted libraries; cross-platform support may be limited to open formats (mzML, mzXML).
- Some vendor-specific metadata (e.g., drift time in ion-mobility spectrometry, or custom instrument parameters) may not map cleanly to the canonical schema and may be lost or truncated during normalization.
- File-format detection by extension or magic bytes can be ambiguous or fragile if input filenames are non-standard or corrupted; a fallback or manual format hint mechanism is recommended.
- Large vendor binary files may require buffering or streaming strategies to avoid memory overload; the unified API design must account for scalability to multi-gigabyte datasets.

## Evidence

- [other] Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) and supports multiple vendor and open formats.: "Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) and supports multiple vendor and open"
- [other] Implement file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.).: "Implement file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.)."
- [other] Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction.: "Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction."
- [other] Expose the normalized spectra through a single API interface (e.g., iterator, random-access getter, or query methods) that hides format-specific details from the caller.: "Expose the normalized spectra through a single API interface (e.g., iterator, random-access getter, or query methods) that hides format-specific details from the caller."
- [readme] The libraries provide a robust, pluggable development framework that simplifies and unifies data file access: "provide a robust, pluggable development framework that simplifies and unifies data file access"
- [readme] supports reading directly from many vendor raw data formats (on Windows): "supports reading directly from many vendor raw data formats (on Windows)"
- [readme] reference implementation of HUPO-PSI mzML standard mass spectrometry data format: "reference implementation of HUPO-PSI mzML standard mass spectrometry data format"
