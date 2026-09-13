---
name: precursor-mass-difference-calculation
description: Use when when comparing two MS/MS spectra using modified cosine similarity
  and the precursor m/z values differ, indicating potential neutral losses, adduct
  variations, or analogs with different substituents.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - cosine_neutral_loss repository
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/jasms.2c00153
  title: Neutral-loss similarity
- doi: 10.1016/1044-0305
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_neutral_loss_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.2c00153
  all_source_dois:
  - 10.1021/jasms.2c00153
  - 10.1016/1044-0305
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-mass-difference-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate the mass offset between precursor ions of two MS/MS spectra to enable alignment of peaks under the modified cosine similarity measure. This step is essential for detecting structurally related molecules that differ in mass.

## When to use

When comparing two MS/MS spectra using modified cosine similarity and the precursor m/z values differ, indicating potential neutral losses, adduct variations, or analogs with different substituents. You need this calculation before attempting to align peaks across spectra with non-zero mass offsets.

## When NOT to use

- Input spectra have identical or negligibly different precursor m/z values (use standard cosine similarity instead)
- Comparing spectra where mass differences are artifacts of measurement error rather than chemical modification (apply mass calibration first)
- Neutral loss similarity is being used instead of modified cosine similarity, as it does not require this offset calculation

## Inputs

- MS/MS spectrum (query) with precursor_mz field
- MS/MS spectrum (reference) with precursor_mz field

## Outputs

- precursor mass difference (float, in Da)
- mass offset parameter for peak alignment

## How to apply

Extract the precursor m/z value from both the query spectrum and the reference spectrum. Subtract the reference precursor m/z from the query precursor m/z to obtain the mass difference (in Da). This offset is then used during peak matching: peaks are considered aligned if m/z_query matches m/z_reference + mass_difference within the specified tolerance. The mass difference accommodates the shift in the m/z axis caused by different precursor masses, allowing the modified cosine algorithm to score aligned peak intensities correctly. Typically this tolerance is 0.1 Da or specified by the instrument calibration.

## Related tools

- **spectrum_utils** (Load and parse MS/MS spectra with precursor_mz annotation; extract precursor charge and m/z fields)
- **cosine_neutral_loss repository** (Reference implementation of modified cosine similarity scoring that uses the precursor mass difference for peak alignment) — https://github.com/bittremieux/cosine_neutral_loss

## Examples

```
import spectrum_utils.spectrum as sus; spectrum1 = sus.MsmsSpectrum.from_usi(usi1); spectrum2 = sus.MsmsSpectrum.from_usi(usi2); mass_diff = spectrum1.precursor_mz - spectrum2.precursor_mz; print(f'Precursor mass difference: {mass_diff} Da')
```

## Evaluation signals

- Precursor mass difference is a scalar float, typically in range ±500 Da for MS/MS comparisons
- When mass difference is applied as offset during peak matching, the number of matched peaks should increase relative to standard (non-offset) cosine similarity for true analogs
- Peak alignment consistency: verify that m/z_query == m/z_reference + mass_difference holds for matched peak pairs within specified tolerance
- Modified cosine score should be higher for mass-offset analogs compared to standard cosine score computed without offset
- Mass difference should be reproducible and stable across repeated calculations for the same spectrum pair

## Limitations

- Precursor mass difference assumes both spectra originate from the same ionization method and charge state; different charge states require normalization first
- Very large mass differences (>1000 Da) may indicate data quality issues or misidentified precursor ions rather than true analogs
- The calculation does not account for measurement uncertainty; alignment tolerance must be set appropriately for instrument resolution
- Modified cosine similarity with mass offset is designed for discovery of structurally related molecules; it may produce spuriously high scores for unrelated spectra with coincidental mass differences

## Evidence

- [other] Extract precursor m/z values from both spectra. 3. Calculate the precursor mass difference between the two spectra. 4. Match peaks between spectra allowing for the precursor mass offset (modified cosine: peaks at m/z_query and m/z_reference + mass_difference are considered aligned).: "Extract precursor m/z values from both spectra. 3. Calculate the precursor mass difference between the two spectra. 4. Match peaks between spectra allowing for the precursor mass offset"
- [other] Modified cosine similarity is a spectrum similarity measure implemented in the repository alongside cosine similarity and neutral loss similarity for comparing MS/MS spectra in the discovery of structurally related molecules.: "Modified cosine similarity is a spectrum similarity measure implemented in the repository alongside cosine similarity and neutral loss similarity for comparing MS/MS spectra in the discovery of"
- [readme] Modified cosine similarity <br/>   Watrous, J. _et al_. Mass spectral molecular networking of living microbial colonies. _Proceedings of the National Academy of Sciences_ **109**, E1743–E1752 (2012).: "Modified cosine similarity ... Mass spectral molecular networking of living microbial colonies"
- [readme] spectrum1.precursor_charge = 1
    spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz): "spectrum1.precursor_charge = 1; spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz)"
