---
name: theoretical-spectrum-generation
description: Use when you have a defined set of lipid species (identified by class
  and fatty acid composition) and need to create a high-throughput spectral library
  for mass spectrometry-based lipid identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0675
  - http://edamontology.org/topic_3375
  tools:
  - LSG (Lipid Spectrum Generator)
  - Excalibur
  - Skyline
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- https://github.com/98104781/LSG/releases/tag/v1.3.0
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

# theoretical-spectrum-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate theoretical mass spectra for enumerated lipid species by applying peer-reviewed, adduct-specific fragmentation patterns. This skill produces precursor m/z, fragment m/z values, and relative intensities that can be exported as spectral libraries (MSP format) or instrument-compatible precursor lists (CSV for Orbitrap DDA or Skyline).

## When to use

Apply this skill when you have a defined set of lipid species (identified by class and fatty acid composition) and need to create a high-throughput spectral library for mass spectrometry-based lipid identification. Specifically, use it before DDA (data-dependent acquisition) on an Orbitrap instrument or targeted analysis in Skyline when peer-reviewed fragmentation rules exist for your lipid classes of interest.

## When NOT to use

- Your lipid species lack well-defined fatty acid composition or class annotation — fragmentation patterns are class- and composition-dependent.
- No peer-reviewed fragmentation data exist for your target lipid classes — the tool relies on published fragmentation rules and cannot infer novel patterns.
- Your analysis goal is to identify fragments in existing experimental spectra rather than to plan acquisition — use spectral matching or database search instead.

## Inputs

- Lipid species list (name, class, fatty acid composition)
- Ionization mode specification (positive/negative)
- Adduct definitions (e.g., [M+H]⁺, [M+Na]⁺, [M−H]⁻)

## Outputs

- Theoretical mass spectra (precursor m/z, fragment m/z, relative intensities)
- Spectral library in MSP format
- Excalibur-compatible precursor list (CSV) for DDA on Orbitrap
- Skyline-compatible transition list (CSV)

## How to apply

Start by loading a lipid species list annotated with class and fatty acid composition. For each species, enumerate all relevant adduct forms (e.g., [M+H]⁺, [M+Na]⁺, [M−H]⁻) based on your ionization mode. Apply class- and adduct-specific fragmentation patterns derived from peer-reviewed studies to compute theoretical fragment masses and their relative intensities. Assemble complete mass spectra (precursor m/z + fragment m/z array + intensity array) for each lipid–adduct combination. Finally, export the resulting spectral library in MSP format for general use or as an Excalibur-compatible CSV precursor list if targeting Orbitrap DDA analysis.

## Related tools

- **LSG (Lipid Spectrum Generator)** (Primary tool for enumeration of lipid species and generation of theoretical spectra by applying peer-reviewed fragmentation patterns.) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Instrument control and DDA acquisition software; accepts LSG-generated precursor lists (CSV) for automated precursor selection on Orbitrap instruments.)
- **Skyline** (Targeted proteomics/lipidomics software; accepts LSG-generated transition lists (CSV) for method configuration and peak detection.)

## Evaluation signals

- Precursor m/z values match the calculated monoisotopic mass of each lipid–adduct combination (within instrumental mass accuracy, typically ≤5 ppm for Orbitrap).
- Fragment masses correspond to known loss patterns and cleavage sites documented in peer-reviewed lipid fragmentation literature for the specified class and adduct type.
- Relative intensities follow expected fragmentation hierarchy (base peak typically < 100%, smaller peaks > 1% depending on adduct stability).
- Exported CSV files parse correctly in Excalibur or Skyline without schema errors (correct column headers, numeric fields, valid adduct notation).
- MSP format output contains valid entries for each lipid–adduct pair: NAME, PRECURSORMZ, FORMULA, SMILES (if available), and PEAKS array with m/z–intensity pairs.

## Limitations

- Fragmentation patterns are fixed by peer-reviewed literature and do not adapt to instrument-specific or matrix-dependent variations in actual spectra.
- Relative intensities are theoretical and may not match real experimental ratios due to ionization efficiency, in-source fragmentation, and instrument tuning effects.
- The skill requires complete fatty acid composition data; partial or ambiguous lipid annotations may lead to incomplete or inaccurate enumeration.
- Lipid class coverage is limited to those with published fragmentation studies; novel lipid classes or unusual adducts may not be supported.

## Evidence

- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [readme] The fragmentation patterns used to generate the spectra are based on peer-reviewed studies: "The fragmentation patterns used to generate the spectra are based on peer-reviewed studies."
- [other] For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−): "For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−)."
- [other] Apply peer-reviewed fragmentation patterns specific to the lipid class and adduct type to generate theoretical fragment masses and intensities: "Apply peer-reviewed fragmentation patterns specific to the lipid class and adduct type to generate theoretical fragment masses and intensities."
- [readme] Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV': "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
