---
name: vendor-format-abstraction
description: Use when you have mass-spectrometry raw data files from multiple vendors (e.g., Thermo, Waters, Bruker, Sciex) and/or mixed standard formats (mzML, mzXML) that must be processed by a single analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# vendor-format-abstraction

## Summary

Unifies access to mass-spectrometry data files across heterogeneous vendor binary formats, mzML, mzXML, and other formats through a single pluggable API layer that normalizes spectra into a common in-memory representation. This skill is essential when handling proteomics datasets from multiple instrument vendors or format standards, eliminating the need for format-specific parsing logic in downstream analysis.

## When to use

You have mass-spectrometry raw data files from multiple vendors (e.g., Thermo, Waters, Bruker, Sciex) and/or mixed standard formats (mzML, mzXML) that must be processed by a single analysis pipeline. Use this skill when you need to expose heterogeneous input files through a uniform programmatic interface without rewriting parsers for each vendor or format variant.

## When NOT to use

- Input is already a normalized feature table or matrix (e.g., peptide quantification, peak picking already performed)—abstraction operates at the raw spectrum level, not aggregated data.
- You require vendor-specific metadata or features not present in the unified schema (e.g., instrument-proprietary tuning parameters, vendor-specific auxiliary spectra)—abstraction by design discards format-specific details.
- Performance is critical and vendor binary reading on non-Windows platforms is necessary—direct vendor format support is limited to Windows; mzML/mzXML are cross-platform alternatives.

## Inputs

- vendor binary mass-spectrometry raw data files (e.g., .raw, .d, .wiff)
- mzML standard format mass-spectrometry data files
- mzXML standard format mass-spectrometry data files
- file path or stream pointing to any supported mass-spectrometry data format

## Outputs

- normalized in-memory spectrum objects with unified metadata (scan ID, retention time, m/z array, intensity array, precursor m/z, charge state)
- spectrum iterator or random-access interface hiding vendor/format details
- LCMS dataset object with standard chemistry computations pre-applied

## How to apply

Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) invariant across formats. Implement file format detection and routing logic to identify input file type (mzML, mzXML, vendor binary, etc.). Integrate or wrap existing vendor-specific parsers and standard format libraries into a pluggable framework. Normalize parsed spectra into the unified in-memory representation, handling vendor-specific conventions and metadata extraction. Expose the normalized spectra through a single API interface (iterator, random-access getter, or query methods) that hides format-specific implementation details from the caller. Test that spectra read from different formats produce identical normalized outputs for the same underlying instrument run.

## Related tools

- **ProteoWizard Library and Tools** (Provides the reference implementation of the pluggable development framework, vendor parser integrations, and unified spectrum API for reading mass-spectrometry data files across formats) — https://github.com/ProteoWizard/pwiz
- **pwiz** (Core C++ library and command-line tools (e.g., msconvert) that implement the vendor-format abstraction layer and expose spectrum normalization) — https://github.com/ProteoWizard/pwiz

## Evaluation signals

- Spectra read from vendor binary format and equivalent mzML/mzXML produce byte-identical or schema-validated equivalent normalized outputs (scan ID, retention time, m/z, intensity, precursor m/z, charge state all match within floating-point tolerance).
- A single code path successfully reads spectra from files of different formats without conditional branching on format type.
- Downstream analysis tools receive spectrum objects with consistent field types and value ranges regardless of input file format origin.
- File format detection correctly routes input to the appropriate parser without user specification of format type.
- All vendor-specific metadata and parsing errors are gracefully handled; no crashes on unsupported vendor variants or corrupt format-specific headers.

## Limitations

- Direct vendor raw data format support is limited to Windows; cross-platform access requires conversion to mzML or mzXML via msconvert or equivalent offline step.
- Vendor-specific proprietary metadata (e.g., instrument tuning parameters, vendor-specific spectra types) are either discarded or incompletely mapped into the unified schema; custom wrappers may be needed to preserve such data.
- Unified schema supports only the most common spectrum metadata (scan ID, retention time, m/z, intensity, precursor m/z, charge state); less common vendor-specific fields require extension or custom handling.

## Evidence

- [other] Unified data structure design rationale: "Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) and supports multiple vendor and open"
- [other] Format detection and routing mechanism: "Implement file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.)."
- [other] Abstraction API exposure: "Expose the normalized spectra through a single API interface (e.g., iterator, random-access getter, or query methods) that hides format-specific details from the caller."
- [readme] ProteoWizard framework design principle: "provide a robust, pluggable development framework that simplifies and unifies data file access"
- [readme] mzML standard implementation and cross-platform support: "reference implementation of HUPO-PSI mzML standard mass spectrometry data format"
- [readme] Vendor format support scope: "supports reading directly from many vendor raw data formats (on Windows)"
