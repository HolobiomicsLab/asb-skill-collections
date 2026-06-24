---
name: precursor-list-formatting-for-dda
description: Use when you have generated a lipid spectral library (lipid identities,
  adducts, m/z values, fragmentation patterns) and your downstream analysis requires
  DDA acquisition on an Orbitrap instrument using Excalibur software.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3750
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0591
  tools:
  - Excalibur
  - LSG
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-list-formatting-for-dda

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert a generated lipid spectral library into an Excalibur-compatible precursor list CSV format suitable for data-dependent acquisition (DDA) analysis on an Orbitrap mass spectrometer. This skill conditionally serializes precursor m/z, charge state, and retention time metadata into the column structure and row format required by Excalibur.

## When to use

Apply this skill when you have generated a lipid spectral library (lipid identities, adducts, m/z values, fragmentation patterns) and your downstream analysis requires DDA acquisition on an Orbitrap instrument using Excalibur software. Use this instead of MSP export when you need a precursor inclusion list rather than a full spectral library.

## When NOT to use

- Input is an MSP format spectral library — export MSP directly instead of converting to precursor list.
- Downstream analysis uses targeted MRM or SRM on a triple-quadrupole instrument — use Skyline-compatible transition list format instead.
- User requires full fragmentation spectra rather than precursor targeting — use MSP export.

## Inputs

- Generated lipid spectral library data (in-memory representation: lipid identities, adducts, precursor m/z, charge states, retention times, fragmentation patterns)
- User format selection parameter (string: 'Excalibur' or 'Skyline')

## Outputs

- Excalibur-compatible precursor list CSV file (with Excalibur-required column headers, one precursor per row)

## How to apply

Accept a user-facing format selection parameter (Excalibur vs. Skyline) and route to the Excalibur branch. Load the generated lipid spectral library data, extracting precursor m/z values, charge states, and retention time metadata for each lipid–adduct combination. Serialize these fields into a CSV file with Excalibur-required column headers and row structure (as defined by Excalibur's precursor list schema). Write the formatted CSV to disk with a naming convention reflecting the selected format. The rationale is that Orbitrap DDA relies on precursor inclusion lists to target specific m/z and charge combinations; Excalibur's format specification ensures the instrument and software can parse and apply these targets correctly.

## Related tools

- **Excalibur** (Target mass spectrometer and acquisition software for which the precursor list CSV is formatted; interprets the serialized precursor m/z, charge, and RT to configure DDA inclusion lists on Orbitrap instruments)
- **LSG** (Upstream tool that generates the lipid spectral library data and provides the conditional CSV export mechanism (including the Excalibur branch)) — https://github.com/98104781/LSG

## Evaluation signals

- CSV file is valid and parseable (no malformed rows, consistent column count per row)
- CSV column headers match Excalibur's required schema (e.g., precursor m/z, charge state, retention time fields are present and named correctly)
- All precursor m/z values are numeric, positive, and within the expected range for lipids (typically 300–1200 m/z)
- Charge states are positive integers (typically +1, +2, +3, or +4 for lipid adducts)
- File naming convention reflects 'Excalibur' format selection (e.g., includes 'Excalibur' or '.csv' extension)

## Limitations

- Fragmentation patterns are not included in the precursor list CSV; if fragment masses are needed for method development, export MSP format instead.
- Retention time values depend on prior annotation or prediction in the spectral library generation step; missing or inaccurate RTs will reduce targeting precision.
- Excalibur format is specific to Orbitrap instruments; users with different mass spectrometer platforms should select the appropriate export format.
- User must manually select the correct format (Excalibur vs. Skyline); no automatic detection of downstream instrument type.

## Evidence

- [other] For Excalibur format: extract precursor m/z, charge state, and retention time; serialize as CSV with Excalibur-required column headers and row structure.: "For Excalibur format: extract precursor m/z, charge state, and retention time; serialize as CSV with Excalibur-required column headers and row structure."
- [other] LSG implements a conditional CSV export mechanism that generates either an Excalibur-compatible precursor list for DDA analysis via orbitrap or a Skyline-compatible transition list, selected by the user.: "LSG implements a conditional CSV export mechanism that generates either an Excalibur-compatible precursor list for DDA analysis via orbitrap or a Skyline-compatible transition list, selected by the"
- [readme] Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'.: "Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'."
- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [other] Accept user format selection (Excalibur or Skyline) as input parameter.: "Accept user format selection (Excalibur or Skyline) as input parameter."
