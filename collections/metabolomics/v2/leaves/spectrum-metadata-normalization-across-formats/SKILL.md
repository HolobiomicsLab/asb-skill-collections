---
name: spectrum-metadata-normalization-across-formats
description: Use when you have mass-spectrometry data files in mixed formats (e.
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

# spectrum-metadata-normalization-across-formats

## Summary

Unify mass-spectrometry spectrum data across vendor-specific and open file formats (mzML, mzXML, vendor binary) into a single normalized in-memory representation with standardized metadata fields. This skill enables tool developers and analysts to read and process heterogeneous MS data through a single API without format-specific branching logic.

## When to use

You have mass-spectrometry data files in mixed formats (e.g., vendor raw files on Windows, mzML exports, mzXML conversions) and need a single code path to extract and compare essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) without re-implementing format-specific parsers for each tool.

## When NOT to use

- Input data are already in a single, standardized format and no cross-format comparison or tool reuse is required.
- Vendor-specific metadata or binary header information critical to your analysis cannot be represented in a common schema without loss of fidelity.
- You need real-time streaming access to spectra and the overhead of format detection and normalization is prohibitive.

## Inputs

- mass-spectrometry raw data file (vendor binary format)
- mzML-formatted spectrum file
- mzXML-formatted spectrum file
- file path or stream with unknown MS data format

## Outputs

- normalized in-memory spectrum object with standardized metadata fields
- unified spectrum iterator or random-access collection
- common spectrum metadata (scan ID, retention time, m/z array, intensity array, precursor m/z, charge state)

## How to apply

Design a unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) spanning all target formats. Implement file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.). Integrate or wrap existing parsers (e.g., ProteoWizard or format-specific libraries) to read raw spectra from the chosen format. Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions and metadata extraction. Finally, expose the normalized spectra through a single API interface (iterator, random-access getter, or query methods) that hides format-specific details from the caller. Verify correctness by spot-checking that m/z and intensity arrays, retention times, and charge states are identical across the same sample loaded from different input formats.

## Related tools

- **ProteoWizard Library and Tools** (provides robust, pluggable framework for unified data file access and implements reference implementation of HUPO-PSI mzML standard) — github.com/ProteoWizard/pwiz
- **pwiz** (modular open-source cross-platform library and tools for reading and normalizing vendor and open MS data formats) — github.com/ProteoWizard/pwiz

## Evaluation signals

- Spot-check that m/z arrays, intensity arrays, retention times, and charge states are identical when the same sample is loaded from two different input formats (e.g., vendor binary vs. mzML export).
- Verify that all required metadata fields (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state) are present and non-null in the normalized spectrum object.
- Confirm that the API successfully hides format-specific details: client code should not contain format-conditional branches or vendor-specific metadata access.
- Validate that format detection correctly routes to the appropriate parser (check routing logic against file headers or file extensions).
- Ensure that normalized metadata conform to the HUPO-PSI mzML standard schema where applicable and that no precision or semantic loss occurs during normalization.

## Limitations

- Vendor raw data file reading is supported directly on Windows only; Linux and macOS users must convert to mzML or mzXML first via external tools.
- Vendor-specific metadata or proprietary fields not represented in the unified schema will be lost during normalization.
- Charge state inference or correction may differ between vendor formats; explicit charge assignments should be validated after normalization.
- Real-time or streaming access to spectra incurs overhead from format detection and normalization at each read step.

## Evidence

- [other] unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state): "unified spectrum data structure that captures essential metadata (scan ID, retention time, m/z values, intensity values, precursor m/z, charge state)"
- [other] file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.): "file format detection and routing logic to identify the input file type (mzML, mzXML, vendor binary, etc.)"
- [other] Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions: "Normalize parsed spectra into the unified in-memory representation, handling format-specific conventions"
- [intro] provide a robust, pluggable development framework that simplifies and unifies data file access: "provide a robust, pluggable development framework that simplifies and unifies data file access"
- [readme] supports reading directly from many vendor raw data formats (on Windows): "supports reading directly from many vendor raw data formats (on Windows)"
- [readme] reference implementation of HUPO-PSI mzML standard mass spectrometry data format: "reference implementation of HUPO-PSI mzML standard mass spectrometry data format"
