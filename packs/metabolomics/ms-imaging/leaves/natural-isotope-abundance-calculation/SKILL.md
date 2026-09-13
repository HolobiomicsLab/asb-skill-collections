---
name: natural-isotope-abundance-calculation
description: Use when when processing mass spectrometry imaging (MSI) data in positive
  ion mode where both [M+H]+ and [M+Na]+ adducts are present for the same lipid species,
  and you observe intensity overlap in [M+H]+ ion images caused by the isotopic fine
  structure of [M+Na]+ adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - LipidQMap
  - Cardinal
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org)
  conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-isotope-abundance-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate the fractional contribution of sodium adducts ([M+Na]+) to protonated ions ([M+H]+) based on natural isotope abundance ratios, used to correct for isotopic overlap in mass spectrometry imaging. This calculation is the quantitative foundation for Type II isotopic correction in lipidomics.

## When to use

When processing mass spectrometry imaging (MSI) data in positive ion mode where both [M+H]+ and [M+Na]+ adducts are present for the same lipid species, and you observe intensity overlap in [M+H]+ ion images caused by the isotopic fine structure of [M+Na]+ adducts. This is particularly critical in lipidomics workflows where accurate quantitation of lipid species requires removal of sodium-induced isotopic artifacts.

## When NOT to use

- Input data contains only [M+H]+ adducts with no corresponding [M+Na]+ features — the correction will have no effect and is unnecessary.
- Negative ion mode MSI data — the ~22 Da sodium mass shift and isotopic overlap pattern are specific to positive ion mode [M+H]+ vs [M+Na]+ competition.
- Low-resolution or unit-resolution mass spectrometry where [M+H]+ and [M+Na]+ isotopic envelopes cannot be resolved and paired — the assumption that isotopic patterns can be calculated and matched breaks down.

## Inputs

- Feature-by-pixel intensity matrix (float32, shape n_features × n_pixels)
- Feature metadata with neutral lipid identifiers and m/z values
- Paired feature assignments linking [M+H]+ and [M+Na]+ features
- Elemental composition or natural isotope abundance lookup table

## Outputs

- Fractional isotopic contribution factors (one scalar per [M+Na]+/[M+H]+ pair)
- Corrected [M+H]+ intensity matrix (float32, same shape as input)

## How to apply

After identifying paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and confirming the ~22 Da m/z difference (mass difference between Na and H substitution), calculate the fractional isotopic contribution of each [M+Na]+ feature to its paired [M+H]+ feature using natural isotope abundance ratios specific to the lipid's elemental composition. This fractional value is then used as a scaling factor to subtract the [M+Na]+ intensity from the [M+H]+ intensity across all pixels. The calculation is grounded in the abundance of heavy isotopes (primarily 13C) naturally present in both the sodium and protonated forms; the Type II correction model assumes that the isotopic pattern of [M+Na]+ overlaps predictably with [M+H]+ based on these natural abundances. Apply the correction pixel-by-pixel, clamping negative corrected values to zero to preserve physical intensity constraints.

## Related tools

- **LipidQMap** (Implements Type II isotopic correction by calculating natural isotope abundance ratios and subtracting scaled [M+Na]+ intensities from [M+H]+ intensities across all pixels in ion images) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Provides HDF5 data container format and conventions for storing feature-by-pixel intensity matrices and metadata required for isotopic correction workflows) — https://cardinalmsi.org

## Evaluation signals

- Calculated fractional contributions are physically valid (0 ≤ fraction ≤ 1) and reflect expected natural 13C/12C and other isotope ratios for the lipid composition.
- After correction, [M+H]+ intensities are equal to or lower than before (no negative values after clamping); intensity decreases are largest at pixels where [M+Na]+ signal is highest.
- Paired [M+Na]+ and [M+H]+ features are correctly matched by neutral lipid ID and m/z difference of ~22 Da (within mass tolerance, typically ≤ 5 ppm for TOF instruments).
- The corrected intensity matrix preserves the HDF5 layout (spectraData/intensity dataset, dimension scales, pixelData and featureData groups unchanged) and output dimensions remain n_features × n_pixels.
- Visual inspection: toggling between raw and isotope-corrected ion images shows reduction of [M+H]+ image intensity in spatial regions where [M+Na]+ signal is prominent, with smoother distribution and reduced edge artifacts.

## Limitations

- Calculation assumes that natural isotope abundance ratios are constant across all lipid species and do not vary with elemental composition; in practice, the 13C contribution may vary slightly with chain length and unsaturation.
- The fractional contribution model assumes that [M+Na]+ isotopic pattern overlaps linearly with [M+H]+ fine structure; this breaks down if the mass difference leads to non-overlapping isotopic envelopes or if resolution is insufficient to resolve individual isotopomers.
- Correction is only valid when [M+H]+ and [M+Na]+ features are correctly paired; misidentification due to m/z tolerance being too loose or neutral formula mismatch will propagate incorrect fractional values.
- Clamping negative values to zero introduces a small bias in corrected intensities for pixels where [M+Na]+ contribution is estimated to exceed [M+H]+ signal; this typically occurs at low signal-to-noise pixels.
- No changelog or version history provided in the LipidQMap repository, making it unclear whether the natural isotope abundance model has been validated or updated across releases.

## Evidence

- [other] LipidQMap performs Type II isotopic correction by correcting [M+H]+ adducts for isotopic overlap contributed by [M+Na]+ adducts in ion images.: "LipidQMap performs Type II isotopic correction by correcting [M+H]+ adducts for isotopic overlap contributed by [M+Na]+ adducts in ion images."
- [other] For each [M+Na]+ feature, calculate its fractional contribution to the corresponding [M+H]+ feature based on natural isotope abundance ratios (Type II correction model).: "For each [M+Na]+ feature, calculate its fractional contribution to the corresponding [M+H]+ feature based on natural isotope abundance ratios (Type II correction model)."
- [other] Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution).: "Identify paired [M+H]+ and [M+Na]+ features by matching neutral lipid identifiers and comparing their m/z values (accounting for mass difference of ~22 Da for Na vs H substitution)."
- [other] Subtract the scaled [M+Na]+ intensities from the [M+H]+ intensities across all pixels, clamping negative values to zero.: "Subtract the scaled [M+Na]+ intensities from the [M+H]+ intensities across all pixels, clamping negative values to zero."
- [readme] Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts.: "Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts."
