---
name: transition-list-formatting-for-targeted-analysis
description: Use when you have generated or assembled a lipid spectral library with precursor m/z values, adduct information, and fragmentation patterns, and you need to import those spectra into Skyline for targeted data-independent or parallel-reaction-monitoring (PRM) analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  tools:
  - Excalibur
  - Skyline
  - LSG
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
---

# transition-list-formatting-for-targeted-analysis

## Summary

Serialize lipid spectral library data (precursor m/z, product ion m/z, and transition metadata) into Skyline-compatible CSV format to enable targeted proteomics or metabolomics analysis. This skill bridges computational spectral generation and instrument-ready transition lists for targeted mass spectrometry workflows.

## When to use

You have generated or assembled a lipid spectral library with precursor m/z values, adduct information, and fragmentation patterns, and you need to import those spectra into Skyline for targeted data-independent or parallel-reaction-monitoring (PRM) analysis. The input must be user-selected as Skyline format (not Excalibur or MSP export).

## When NOT to use

- Input spectral library is already in MSP format or only needs MSP export; use MSP serialization instead.
- Target instrument is a Thermo Orbitrap using data-dependent acquisition (DDA); use Excalibur-format precursor list instead.
- Fragmentation patterns or product ions have not been generated or validated against peer-reviewed studies; the transition list will be unreliable without correct ion assignments.

## Inputs

- Lipid spectral library object (in-memory representation containing lipid class, fatty acid composition, adducts, precursor m/z, product ion m/z, fragmentation patterns)
- User format selection parameter (set to 'Skyline')
- Retention time data (optional, if available in library)

## Outputs

- CSV file formatted for Skyline import (with Skyline-required column headers and transition list structure)
- File naming convention reflecting 'Skyline' format selection

## How to apply

Load the generated lipid spectral library containing lipid identities, adducts, m/z values, and fragmentation patterns from the internal representation. Extract precursor m/z, product ion m/z values (fragment ions), and transition-specific metadata (e.g., collision energy, retention time if available). Serialize these fields as CSV rows with Skyline-required column headers (typically precursor m/z, product m/z, transition name, collision energy). Write the formatted CSV to a file with a naming convention that reflects the Skyline format selection. Validate that all rows conform to Skyline's expected column structure and that numeric fields (m/z, collision energy) are properly formatted.

## Related tools

- **Skyline** (Target software that consumes the formatted transition list CSV for targeted MS method design and data analysis)
- **LSG** (Spectral library generation tool that produces the lipid library data (identities, adducts, m/z, fragmentation patterns) fed into this transition-list formatting workflow) — https://github.com/98104781/LSG/releases/tag/v1.3.0

## Evaluation signals

- CSV file opens without parse errors in Skyline and transitions are recognized as valid entries.
- All precursor m/z and product ion m/z values are numeric and within expected mass range for lipid species (e.g., 400–1200 m/z for most lipids).
- Column headers match Skyline's expected schema; no missing or misnamed required fields.
- Row count matches the expected number of transitions (precursor × product ion combinations) generated from the input library.
- Retention time values (if included) are numeric and within typical chromatographic range (0–60 min for typical gradient).

## Limitations

- Fragmentation patterns used to generate the spectral library depend on peer-reviewed studies; if those studies do not cover a particular lipid class or adduct, product ions may be inaccurate or missing.
- User must manually select Skyline format; if Excalibur or MSP is selected by mistake, this skill will not be invoked.
- Retention time information may not be available in all generated libraries, limiting the ability to filter or schedule transitions.
- Skyline transition list format may vary across Skyline versions; compatibility with a specific Skyline release is not explicitly documented.

## Evidence

- [other] For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize as CSV with Skyline-required column headers and transition list structure.: "For Skyline format: extract precursor m/z, product ion m/z values, and transition-specific metadata; serialize as CSV with Skyline-required column headers and transition list structure."
- [readme] Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'.: "Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'."
- [other] Load generated lipid spectral library data (lipid identities, adducts, m/z values, fragmentation patterns) from internal representation.: "Load generated lipid spectral library data (lipid identities, adducts, m/z values, fragmentation patterns) from internal representation."
- [readme] The fragmentation patterns used to generate the spectra are based on peer-reviewed studies.: "The fragmentation patterns used to generate the spectra are based on peer-reviewed studies."
