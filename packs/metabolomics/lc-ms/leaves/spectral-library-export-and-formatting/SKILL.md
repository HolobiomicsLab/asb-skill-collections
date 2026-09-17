---
name: spectral-library-export-and-formatting
description: Use when after theoretical spectra have been generated for lipid–adduct
  combinations with enumerated fragment masses and intensities, and you need to deploy
  them for downstream MS/MS analysis on Orbitrap (DDA via Excalibur) or SkyLine (targeted/PRM)
  workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - Excalibur
  - LSG (Lipid Spectrum Generator)
  - Skyline
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# spectral-library-export-and-formatting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Export computationally generated lipid mass spectra into standardized formats (MSP, CSV) compatible with targeted and data-dependent acquisition workflows on Orbitrap instruments. This skill bridges in-memory spectral libraries to instrument-ready precursor lists and transition libraries.

## When to use

After theoretical spectra have been generated for lipid–adduct combinations with enumerated fragment masses and intensities, and you need to deploy them for downstream MS/MS analysis on Orbitrap (DDA via Excalibur) or SkyLine (targeted/PRM) workflows. Use this skill when spectral output must transition from the generative tool (LSG) to instrument control or analysis software.

## When NOT to use

- Spectra have not yet been generated or fragmentation patterns have not been applied—use spectrum generation skill first.
- Input is a raw mass spectrometry data file (mzML, RAW, d) rather than theoretical spectra—use data acquisition or centroiding workflows instead.
- Targeted analysis requires custom transition selection or collision energy optimization beyond the default peer-reviewed fragmentation patterns—export to CSV and manually curate in Skyline or vendor software.

## Inputs

- Enumerated lipid species list (species name, lipid class, fatty acid composition)
- Generated mass spectra with adduct-specific precursor m/z, fragment m/z, and relative intensities

## Outputs

- MSP format spectral library (.MSP file)
- Excalibur-compatible precursor list (CSV) for DDA/Orbitrap
- Skyline-compatible transition list (CSV)

## How to apply

After spectrum generation completes with precursor m/z, fragment m/z values, and relative intensities for each lipid–adduct combination, select the desired export format: (1) MSP format for spectral library databases compatible with NIST and open-source search engines; (2) CSV format as an Excalibur-compatible precursor list for DDA acquisition on Orbitrap, which includes precursor m/z, charge state, and fragmentation energy; or (3) Skyline-compatible transition list (CSV) for targeted parallel reaction monitoring (PRM). The selection determines both file structure and metadata inclusion. Validate that exported precursor m/z values match the enumerated adduct masses and that fragment intensities are normalized (typically 0–999 or 0–100% scale). Export format choice should align with the intended MS instrument control software and the downstream search/analysis engine.

## Related tools

- **LSG (Lipid Spectrum Generator)** (Generates theoretical spectra with adduct enumeration and peer-reviewed fragmentation patterns; produces in-memory or intermediate spectral data that is exported by this skill) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Orbitrap instrument control and DDA acquisition software; consumes CSV precursor lists exported by this skill for targeted MS/MS triggering)
- **Skyline** (Targeted proteomics and metabolomics analysis platform; imports CSV transition lists exported by this skill for PRM or SRM workflows)

## Evaluation signals

- MSP file contains valid header entries (name, precursor m/z, adduct notation) and peaks block with fragment m/z and intensity pairs for every exported spectrum.
- CSV precursor list rows correspond 1:1 to enumerated lipid–adduct combinations with no missing or duplicate precursor m/z values.
- Exported precursor m/z matches the theoretical mass calculated for the lipid molecular weight + adduct mass offset (e.g., [M+H]+ = MW+1.0078, [M+Na]+ = MW+22.9898, [M−H]− = MW−1.0078).
- Fragment m/z values in exported spectra fall within expected mass windows for the lipid class and adduct type (e.g., no fragments heavier than the precursor).
- File format conforms to MSP specification (NIST-style headers and peaks) or CSV schema expected by Excalibur (columns: precursor m/z, charge, NCE/normalized collision energy, optional transition list) and can be imported without format errors.

## Limitations

- Export is limited to three predefined formats (MSP, Excalibur CSV, Skyline CSV); custom instrumental formats or vendor-specific extensions require post-export translation.
- Relative intensity values are normalized by LSG according to peer-reviewed fragmentation patterns but may require re-normalization or collision energy re-optimization after instrument import for optimal signal-to-noise ratio.
- No validation that exported spectra will produce confident identifications in the target MS experiment; downstream MS/MS performance depends on instrument tuning, sample ionization, and actual fragment ion abundances, which may deviate from theoretical predictions.

## Evidence

- [readme] Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'.: "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
- [other] Construct complete mass spectra (precursor m/z, fragment m/z values, and relative intensities) for each lipid–adduct combination. Export the spectral library in MSP format or as an Excalibur-compatible precursor list (CSV) for DDA analysis on Orbitrap instruments.: "Construct complete mass spectra (precursor m/z, fragment m/z values, and relative intensities) for each lipid–adduct combination. Export the spectral library in MSP format or as an"
- [readme] This program is intended to enable the user to generate on-demand (mass)spectral libraries for the identification of lipid species.: "This program is intended to enable the user to generate on-demand (mass)spectral libraries for the identification of lipid species."
