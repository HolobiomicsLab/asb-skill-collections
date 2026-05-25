---
name: ms-spectra-library-parsing
description: Use when working in the metabolomics domain to parse and load mass spectrometry spectral libraries in MGF format, extracting spectrum metadata, precursor m/z, fragment peaks, and chemical annotations for downstream cleaning and validation.
when_to_use_negative:
- Input is already a SpectrumList or deserialized Python object — skip directly to cleaning pipeline.
- Input is in a non-MGF format (e.g., mzML, NetCDF, JSON) without a format conversion step beforehand.
- Library has already been filtered or curated and you are resuming from an intermediate checkpoint — load from the serialized checkpoint instead of re-parsing the original MGF.
edam_operation: http://edamontology.org/operation_3436
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0625
tools:
- name: matchms
  role: Core library for parsing MGF spectral files and instantiating Spectrum objects with metadata
  repo: https://github.com/matchms/matchms
- name: matchms 0.26.4
  role: Specific version used in reproducible GNPS library cleaning pipeline
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Validates and normalizes SMILES, InChI, and InChIKey metadata fields during and after parsing
  repo: https://github.com/rdkit/rdkit
- name: PubChem
  role: External reference database used to derive missing chemical structure annotations from compound names
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/ms-spectra-library-parsing@sha256:926d52ddd075fc4bbeb438faca19f0e0de2fe9ec5f5319923cc0fe791c1fd6ec
---

# MS/MS Spectra Library Parsing

## Summary

Parse and load mass spectrometry spectral libraries in MGF format into a Python-based spectral object framework, extracting spectrum metadata, precursor m/z, fragment peaks, and chemical annotations for downstream cleaning and validation. This is the essential first step in any reproducible MS/MS library curation pipeline.

## When to use

You have obtained a public or private mass spectral library in MGF format (e.g., GNPS no-propagated snapshot, MoNA, MassBank, NIST) and need to ingest all spectra and their associated metadata fields (compound name, SMILES, InChI, InChIKey, precursor m/z, ionization mode, adduct) into a unified object representation before applying cleaning, filtering, or validation operations.

## When NOT to use

- Input is already a SpectrumList or deserialized Python object — skip directly to cleaning pipeline.
- Input is in a non-MGF format (e.g., mzML, NetCDF, JSON) without a format conversion step beforehand.
- Library has already been filtered or curated and you are resuming from an intermediate checkpoint — load from the serialized checkpoint instead of re-parsing the original MGF.

## Inputs

- MGF file (mass spectral library format with spectra and metadata)
- Library snapshot identifier or file path (e.g., GNPS no-propagated 2023-08-21)
- Optional: YAML configuration file specifying parser options

## Outputs

- SpectrumList object (in-memory or serialized)
- Parsed spectrum count and metadata field inventory
- List of Spectrum objects with peaks and metadata fields populated

## How to apply

Use matchms version 0.26.4 (or later compatible version) to parse the MGF file, which deserializes each spectrum record into a Spectrum object containing peaks (m/z and intensity pairs), metadata fields (ionmode, precursor_mz, compound_name, SMILES, InChI, InChIKey, adduct), and spectrum-level identifiers. The parser automatically loads all metadata present in the MGF headers. Verify that the total spectrum count matches the expected input size (e.g., 500,569 for GNPS no-propagated as of 2023-08-21). Store the parsed SpectrumList in memory or serialize to an intermediate format for subsequent pipeline steps (metadata harmonization, filtering, annotation repair). No filtering or modification occurs at this stage; the goal is faithful representation of the input library.

## Related tools

- **matchms** (Core library for parsing MGF spectral files and instantiating Spectrum objects with metadata) — https://github.com/matchms/matchms
- **matchms 0.26.4** (Specific version used in reproducible GNPS library cleaning pipeline) — https://github.com/matchms/matchms
- **RDKit** (Validates and normalizes SMILES, InChI, and InChIKey metadata fields during and after parsing) — https://github.com/rdkit/rdkit
- **PubChem** (External reference database used to derive missing chemical structure annotations from compound names)

## Evaluation signals

- Parsed spectrum count equals or closely matches the known input size for the library snapshot (e.g., 500,569 for GNPS no-propagated 2023-08-21); investigate discrepancies in MGF file integrity.
- All mandatory metadata fields (ionmode, precursor_mz, compound_name) are present in ≥95% of parsed spectra; document percentage of spectra missing each field.
- Peak lists (m/z, intensity pairs) are non-empty for ≥98% of spectra; identify and log spectra with zero or malformed peaks.
- Chemical structure fields (SMILES, InChI, InChIKey) parse without RDKit exceptions in ≥95% of spectra; log any invalid SMILES or InChI that cause deserialization failures.
- Random sample of 100+ parsed Spectrum objects can be manually inspected to confirm metadata fidelity and peak intensity ranges (e.g., intensities ≥0, m/z > 0).

## Limitations

- The parsing step is format-specific to MGF; other mass spectrometry file formats (mzML, NetCDF) require alternative parsers or format conversion beforehand.
- Parsing does not perform any validation or cleaning; metadata quality issues (missing fields, malformed SMILES, inconsistent adducts) are preserved in the parsed output and must be addressed by subsequent filters.
- Large libraries (≥500,000 spectra) may exhaust available memory if held entirely in SpectrumList; consider streaming or batch-processing approaches for extremely large datasets.
- The parser relies on correct MGF header syntax; non-standard or corrupted MGF files may result in silent data loss or parsing errors.
- Chemical annotations are parsed as-is from the MGF file; no external validation against PubChem or other reference databases occurs during parsing itself.

## Evidence

- [abstract] we here introduce a comprehensive pipeline for library cleaning within the matchms framework: "we here introduce a comprehensive pipeline for library cleaning within the matchms framework"
- [abstract] Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra: "Before cleaning, the GNPS library contained 500,569 spectra...The final cleaned GNPS public mass spectral library contains 448.485 curated mass spectra"
- [abstract] metadata cleaning, peak filtering, intensity normalization, and structure annotation validation: "metadata cleaning, peak filtering, intensity normalization, and structure annotation validation"
- [abstract] Matchms is easily installable through pip or Conda and uses Git for systematic version control: "Matchms is easily installable through pip or Conda and uses Git for systematic version control"
- [abstract] Matchms version 0.26.4 was used to run these pipelines: "Matchms version 0.26.4 was used to run these pipelines"
- [abstract] Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min: "Running the machms pipeline with the filters given in Supplementary Table S1 on the GNPS library of 500,569 spectra took 6 h and 45 min"
