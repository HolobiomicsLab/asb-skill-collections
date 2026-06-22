---
name: lipid-spectral-data-export
description: Use when after generating a complete lipid spectral library with adduct-specific fragmentation patterns and retention time metadata, when you need to deploy the library for targeted or data-dependent acquisition on specific mass spectrometry instruments—either Excalibur-controlled orbitrap.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - Excalibur
  - Skyline
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_lipid_spectrum_generator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04518
  all_source_dois:
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-spectral-data-export

## Summary

Conditional serialization of in-memory lipid spectral library data into format-specific CSV export schemas compatible with downstream mass spectrometry analysis platforms (Excalibur for DDA orbitrap or Skyline for targeted analysis). This skill bridges generated spectral metadata to instrument-ready precursor or transition lists.

## When to use

After generating a complete lipid spectral library with adduct-specific fragmentation patterns and retention time metadata, when you need to deploy the library for targeted or data-dependent acquisition on specific mass spectrometry instruments—either Excalibur-controlled orbitrap instruments for DDA analysis or Skyline-based targeted workflows.

## When NOT to use

- Input spectral library has not yet been generated or is in external MSP format only—use this skill after internal library synthesis is complete.
- Target instrument is neither Excalibur-based orbitrap nor Skyline-compatible; format mapping logic is specific to these two platforms.
- Export goal is to produce a universal spectral library (MSP format) rather than instrument-specific precursor/transition lists—use MSP export instead.

## Inputs

- in-memory lipid spectral library object (lipid class, fatty acid compositions, adducts, m/z, fragmentation patterns, retention times)
- format selection parameter (Excalibur or Skyline)
- output file path or naming template

## Outputs

- CSV file with Excalibur precursor list schema (precursor m/z, charge, retention time, lipid identity columns)
- CSV file with Skyline transition list schema (precursor m/z, product m/z, transition metadata columns)

## How to apply

Accept a user-selected export format parameter (Excalibur or Skyline) at the start of the export routine. Load the in-memory lipid spectral library containing lipid identities, adduct assignments, m/z values, and fragmentation patterns. For Excalibur format: extract precursor m/z, charge state, and retention time; construct CSV rows with Excalibur-required column headers and DDA-compatible structure. For Skyline format: extract precursor m/z, product ion m/z values (fragment masses), and transition-specific metadata; construct CSV rows with Skyline-required headers and transition-per-row structure. Validate that all required columns are populated and m/z values are numeric and positive. Write the formatted CSV to disk with a naming convention that reflects the selected format and source lipid parameters.

## Related tools

- **Excalibur** (Target DDA acquisition platform for which precursor list CSV is serialized (orbitrap-compatible format with charge state and retention time metadata))
- **Skyline** (Target targeted analysis platform for which transition list CSV is serialized (product ion m/z and transition structure))

## Evaluation signals

- Verify CSV headers match the target platform's specification (Excalibur or Skyline) as documented in each tool's import requirements.
- Confirm all m/z values (precursor and product ions) are numeric, positive, and within the expected mass range for lipids (e.g., 400–2000 m/z).
- Check that precursor m/z and charge state pairs produce valid monoisotopic masses for the declared lipid identity and adduct.
- Validate row count and lipid coverage matches the generated library (no silent truncation or filtering during export).
- Open the exported CSV in the target application (Excalibur or Skyline) and confirm successful import without parsing or schema errors.

## Limitations

- Export format is limited to Excalibur and Skyline; other mass spectrometry software platforms require separate custom mapping logic.
- Retention time metadata is only populated if the spectral library generation step included RT prediction or assignment; exported RT values are only as accurate as their source.
- Fragmentation pattern accuracy depends on the peer-reviewed literature and adduct-specific fragmentation rules used during library synthesis; unusual lipid modifications or non-standard adducts may not be represented.
- CSV export does not preserve high-resolution spectral intensity arrays; only nominal m/z and metadata are exported—full spectrum recovery requires MSP or binary format.

## Evidence

- [other] LSG implements a conditional CSV export mechanism that generates either an Excalibur-compatible precursor list for DDA analysis via orbitrap or a Skyline-compatible transition list, selected by the user.: "LSG implements a conditional CSV export mechanism that generates either an Excalibur-compatible precursor list for DDA analysis via orbitrap or a Skyline-compatible transition list"
- [other] Load generated lipid spectral library data (lipid identities, adducts, m/z values, fragmentation patterns) from internal representation.: "Load generated lipid spectral library data (lipid identities, adducts, m/z values, fragmentation patterns) from internal representation"
- [other] For Excalibur format: extract precursor m/z, charge state, and retention time; serialize as CSV with Excalibur-required column headers and row structure.: "For Excalibur format: extract precursor m/z, charge state, and retention time; serialize as CSV with Excalibur-required column headers and row structure"
- [other] For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize as CSV with Skyline-required column headers and transition list structure.: "For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize as CSV with Skyline-required column headers and transition list structure"
- [readme] Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'.: "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
