---
name: isotope-and-adduct-pattern-recognition
description: Use when when processing MS1 mass tracks from a single sample and you have already constructed per-bin mass tracks with consensus m/z and intensity vectors.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3520
  tools:
  - pymzml
  - Python
  - khipu
  - mass2chem
  - asari
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- The default method uses `pymzml` to parse mzML files.
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-and-adduct-pattern-recognition

## Summary

Identifies and groups related mass tracks by recognizing characteristic m/z differences corresponding to 13C/12C isotopes, sodium/hydrogen (Na/H) adducts, and other mass-pattern relationships. This anchors mass tracks to a common neutral mass, reducing redundancy and improving feature annotation in high-resolution LC-MS metabolomics.

## When to use

When processing MS1 mass tracks from a single sample and you have already constructed per-bin mass tracks with consensus m/z and intensity vectors. Apply this skill to annotate groups of co-eluting ions that share the same or closely-related retention time profile but differ in m/z by known isotope ratios (13C offset ≈ 1.003 amu) or adduct mass shifts (Na vs H ≈ 22 amu). This is essential when feature redundancy from isotopologues or multiply-charged/adducted species would otherwise inflate the final feature table.

## When NOT to use

- Input is already a deduplicated feature table; this skill operates on raw mass tracks before final feature selection.
- MS/MS data or ion-pairing databases are not available and you require higher confidence in adduct assignment; pattern recognition alone may be ambiguous.
- Sample retention time is so short or instrument resolution so low that isotope/adduct clusters cannot be resolved; operate at lower mass resolution (< 50k FWHM) or very high scan-rate scenarios.

## Inputs

- per-sample mass tracks (list of (consensus_mz, intensity_vector, retention_time_range) tuples)
- instrument mass accuracy specification (ppm tolerance, e.g., 5 ppm)
- reference adduct/isotope mass-shift library (13C offset, Na/H difference, etc.)

## Outputs

- isotope/adduct-annotated mass tracks (with relationship tags and inferred neutral mass)
- reduced feature set (anchor tracks only, with secondary tracks labeled)
- mass pattern validation metrics (observed vs. expected abundance ratios, mass error in ppm)

## How to apply

After mass track construction, compute pairwise m/z differences between all tracks co-eluting in the same retention-time window. Screen these differences against a library of known mass shifts: 13C/12C isotope patterns (1.003355 amu per carbon, typically seen as +1.003 in singly-charged species), Na–H substitution (+21.982 amu), and other common adducts. For each observed m/z difference within instrument mass accuracy (typically ≤ 5 ppm for Orbitrap), cluster tracks into isotopic families or adduct families. Use intensity ratios and expected natural abundance patterns (e.g., ~1.1% per 12C for a single 13C substitution) to validate suspected 13C peaks. Establish a primary (lightest, or most intense) track as the anchor and tag secondary tracks with their relationship type (e.g., '[M+Na]+', '[M+13C]+'). This reduces downstream redundancy and aids structural annotation by inferring neutral mass from the anchor track.

## Related tools

- **pymzml** (Parses mzML files to retrieve MS1 spectra and reconstruct mass track m/z values)
- **khipu** (Pre-annotation tool to group ions (including isotopologues and adducts) into empirical compounds and infer neutral mass) — https://github.com/shuzhao-li-lab/khipu
- **mass2chem** (Provides utility functions for adduct calculation and libraries of mass patterns for isotopologues and in-source fragments) — https://github.com/shuzhao-li/mass2chem
- **asari** (Orchestrates mass track construction and supplies filter/evaluation functions; isotope/adduct anchor identification is a built-in feature) — https://github.com/shuzhao-li/asari

## Examples

```
from asari.chromatograms import extract_massTracks_; from mass2chem import adduct_calc; mass_tracks = extract_massTracks_(sample_data); anchored_tracks = identify_anchor_mass_tracks(mass_tracks, mass_shift_library={'13C': 1.003355, 'Na_H': 21.982}, ppm_tol=5)
```

## Evaluation signals

- Isotope-cluster abundance ratios match theoretical natural-abundance expectations (e.g., 13C at ~1.1% of 12C for singly-charged peaks).
- All anchor tracks are assigned and secondary tracks are correctly tagged with their relationship type (13C, Na/H, etc.) and retain m/z differences within instrument tolerance (≤ 5 ppm).
- Co-elution of anchors and secondaries is verified: retention-time ranges overlap or differ by < 1 scan at typical LC timescales.
- No duplicate features in the final feature table for the same neutral mass; feature count is reduced relative to pre-grouping mass track count.
- Neutral mass inferred from anchor tracks is consistent with database queries (e.g., HMDB lookup succeeds) and MS/MS annotation (if available).

## Limitations

- Ambiguity when m/z differences from different mass shifts (e.g., 13C vs. a different adduct) occupy overlapping windows; requires intensity ratio and chromatographic context to disambiguate.
- Low-abundance isotopologues or multiply-charged species may fall below the detection threshold and not be recognized; depends on minimum intensity threshold.
- In regions of very high peak density (e.g., lipid-rich samples with many isobaric species), clustering can merge unrelated mass tracks if retention times are close; user may need to adjust m/z or RT window tolerances.
- Performance depends on accurate prior construction of individual mass tracks; errors in consensus m/z or intensity vector propagate into adduct/isotope grouping.

## Evidence

- [other] Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotopes or Na/H adducts.: "Establish anchor mass tracks by identifying m/z differences matching 13C/12C isotopes or Na/H adducts."
- [readme] Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass.: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass."
- [readme] provides functions on handling chemical formulas, formula based adduct calculation, indexing and search functions on mass spec data, libraries of common metabolites, contaminants, mass differences: "provides functions on handling chemical formulas, formula based adduct calculation, indexing and search functions on mass spec data, libraries of common metabolites, contaminants, mass differences"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
