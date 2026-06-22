---
name: adduct-form-prediction-and-mass-calculation
description: Use when you have a characterized lipid species (with defined class and fatty acid composition) and need to predict which adduct forms will ionize under your experimental ionization mode (positive or negative ESI), and you require accurate precursor m/z values for DDA method configuration or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0625
  tools:
  - Excalibur
  - LSG (Lipid Spectrum Generator)
  techniques:
  - LC-MS
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

# adduct-form-prediction-and-mass-calculation

## Summary

Enumerate all ionization adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−) for a given lipid species and compute their precursor m/z values to support targeted mass spectrometry experiments. This skill is essential for generating comprehensive precursor lists and spectral libraries for data-dependent acquisition (DDA) on Orbitrap instruments.

## When to use

Apply this skill when you have a characterized lipid species (with defined class and fatty acid composition) and need to predict which adduct forms will ionize under your experimental ionization mode (positive or negative ESI), and you require accurate precursor m/z values for DDA method configuration or spectral library construction. Use it upstream of fragmentation pattern application and spectral library export.

## When NOT to use

- Input already contains experimentally observed precursor m/z values from MS1 scans — use this skill for *in silico* prediction only.
- Your workflow requires only neutral mass or monoisotopic mass without adduct enumeration; this skill adds complexity if adduct prediction is not needed.
- Ionization mode and expected adducts are not yet defined — clarify experimental conditions before applying this skill.

## Inputs

- Lipid species list with neutral mass (or fatty acid composition from which mass can be calculated)
- Lipid class identifier
- Ionization polarity setting (positive or negative ESI)
- Set of expected adduct forms for the experiment (e.g., [M+H]+, [M+Na]+, [M+NH4]+ for positive mode)

## Outputs

- Enumerated adduct forms for each lipid species
- Precursor m/z values (one per adduct per species)
- Species–adduct mapping (preserving lipid class, fatty acid composition, and adduct identity)
- Excalibur-compatible precursor list in CSV format for DDA configuration

## How to apply

For each lipid species in your enumerated list, systematically generate all relevant adduct forms based on the ionization polarity of your experiment (e.g., [M+H]+, [M+Na]+, [M+NH4]+ for positive ESI; [M−H]−, [M+Cl]− for negative ESI). Calculate the exact m/z of each adduct by adding or subtracting the mass of the adduct-forming ion from the neutral lipid mass. Retain the lipid species identifier (name, class, fatty acid composition) alongside each adduct form and its calculated m/z. This enumeration serves as the input to subsequent fragmentation pattern application and enables export as an Excalibur-compatible precursor list (CSV format) for direct import into DDA acquisition methods.

## Related tools

- **LSG (Lipid Spectrum Generator)** (Integrates adduct enumeration and m/z calculation into on-demand spectral library generation; accepts lipid species lists and outputs adduct-annotated precursor lists and MSP spectral libraries.) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Target mass spectrometry instrument control software that imports adduct-enumerated precursor lists in CSV format to configure DDA acquisition methods on Orbitrap instruments.)

## Evaluation signals

- All expected adduct forms for the ionization polarity are present in the output (e.g., [M+H]+, [M+Na]+, [M+NH4]+ for positive ESI).
- Calculated m/z values are chemically valid: for [M+H]+, m/z = (M + 1.008)/z; for [M+Na]+, m/z = (M + 22.990)/z; for [M−H]−, m/z = (M − 1.008)/|z|, where M is neutral mass and z is charge.
- Adduct–species mapping is preserved: each precursor entry retains lipid class, fatty acid composition, and adduct form annotation.
- Precursor list is importable by Excalibur without format errors and generates valid DDA targets on Orbitrap.
- No duplicate adducts for the same species; each species–adduct pair appears exactly once in the enumeration.

## Limitations

- Adduct prediction relies on a pre-defined set of expected adduct forms; unexpected adducts (e.g., rare multimers or solvent-specific adducts) will not be generated unless explicitly specified.
- Calculated m/z assumes accurate input neutral mass; errors in lipid mass or fatty acid composition will propagate to all adduct m/z values.
- Does not account for isotope distribution; output is monoisotopic m/z only.
- Fragmentation patterns are applied separately after adduct enumeration; this skill does not validate whether predicted adduct forms will actually fragment or ionize effectively under experimental conditions.

## Evidence

- [other] For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−).: "For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−)."
- [other] Construct complete mass spectra (precursor m/z, fragment m/z values, and relative intensities) for each lipid–adduct combination.: "Construct complete mass spectra (precursor m/z, fragment m/z values, and relative intensities) for each lipid–adduct combination."
- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [readme] an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'.: "an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported by selecting '.CSV'."
