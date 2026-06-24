---
name: proteomics-data-structure-design
description: Use when when building a mass-spectrometry analysis pipeline that must
  support multiple vendor and open formats (mzML, mzXML, Thermo, Agilent, Bruker,
  etc.) and you need to shield downstream tools from format-specific parsing logic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ProteoWizard Library and Tools
  - pwiz
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.9b00640
  title: Skyline (small molecules)
evidence_spans:
- The ProteoWizard Library and Tools are a set of modular and extensible open-source,
  cross-platform tools and software libraries
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# proteomics-data-structure-design

## Summary

Design and implement a unified, vendor-agnostic spectrum data structure that normalizes mass-spectrometry data from heterogeneous file formats (mzML, mzXML, vendor binary) into a single in-memory representation. This skill enables a single API to transparently read and expose normalized spectra regardless of input format.

## When to use

When building a mass-spectrometry analysis pipeline that must support multiple vendor and open formats (mzML, mzXML, Thermo, Agilent, Bruker, etc.) and you need to shield downstream tools from format-specific parsing logic. Specifically when you have raw or vendor-specific mass-spec files and must expose them through a uniform data interface.

## When NOT to use

- Input is already in a standardized format (mzML) and downstream tools natively support it without needing a unified layer.
- You require format-specific features or vendor-proprietary metadata that would be lost during normalization.
- Performance is critical and the overhead of abstraction and normalization exceeds the benefit of format transparency.

## Inputs

- Raw mass-spectrometry data files (mzML, mzXML, vendor binary formats)
- Format metadata and schema definitions
- Format-specific parser libraries or bindings

## Outputs

- Unified spectrum data structure (in-memory representation)
- Normalized spectrum metadata (scan ID, retention time, m/z, intensity, precursor m/z, charge state)
- Single API interface for spectrum access (iterator or query methods)

## How to apply

First, design a unified spectrum data structure schema that captures essential metadata: scan ID, retention time, m/z array, intensity array, precursor m/z, and charge state. Implement file format detection and routing logic to identify the input file type. Integrate or wrap existing format-specific parsers (e.g., ProteoWizard libraries or vendor-provided readers) to read raw spectra. Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction rules. Finally, expose normalized spectra through a single API interface (iterator, random-access getter, or query methods) that hides format details from the caller. Use the pluggable framework approach to allow new format support without modifying core normalization logic.

## Related tools

- **ProteoWizard Library and Tools** (Provides robust, pluggable development framework and format-specific parsers for unifying mass-spec data file access) — https://github.com/ProteoWizard/pwiz
- **pwiz** (Core library implementing reference implementation of HUPO-PSI mzML standard and vendor format support) — https://github.com/ProteoWizard/pwiz

## Evaluation signals

- All input spectra from different formats (mzML, mzXML, vendor binary) can be read and produce identical normalized output when the same raw data is used.
- Unified data structure contains all required fields (scan ID, retention time, m/z array, intensity array, precursor m/z, charge state) with no null or missing values for valid spectra.
- Single API interface successfully returns spectra without caller needing to know or specify the input format.
- Format-specific metadata is correctly preserved or mapped into the normalized schema without loss of essential information.
- Performance overhead of normalization layer is acceptable relative to the benefit of format abstraction (typically < 10–20% overhead).

## Limitations

- Vendor binary format support on Windows only; cross-platform pipelines may be limited to mzML/mzXML or require format conversion on non-Windows systems.
- Normalization may lose vendor-specific or proprietary metadata that is not part of the HUPO-PSI mzML standard.
- Pluggable framework requires maintenance when vendor formats change or new formats are introduced.
- No changelog or versioning information is available for tracking API or schema changes over time.

## Evidence

- [other] Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) and supports multiple vendor and open formats.: "Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) and supports multiple vendor and open"
- [other] Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction.: "Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction."
- [other] Expose the normalized spectra through a single API interface (e.g., iterator, random-access getter, or query methods) that hides format-specific details from the caller.: "Expose the normalized spectra through a single API interface (e.g., iterator, random-access getter, or query methods) that hides format-specific details from the caller."
- [readme] The libraries provide a robust, pluggable development framework that simplifies and unifies data file access: "provide a robust, pluggable development framework that simplifies and unifies data file access"
- [readme] supports reading directly from many vendor raw data formats (on Windows): "supports reading directly from many vendor raw data formats (on Windows)"
