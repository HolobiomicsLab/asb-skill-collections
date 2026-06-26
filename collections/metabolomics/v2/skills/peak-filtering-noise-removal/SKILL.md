---
name: peak-filtering-noise-removal
description: Use when you have raw MS/MS spectra (in formats like mzML, json, mgf,
  msp, mzxml) that contain background noise or numerous low-intensity peaks before
  running MS2Query library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3216
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2Query
  - MZMine
  - matchms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-37446-4
  title: ms2query
evidence_spans:
- MS2Query - Reliable and fast MS/MS spectral-based analogue search
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2query
    doi: 10.1038/s41467-023-37446-4
    title: ms2query
  dedup_kept_from: coll_ms2query
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-37446-4
  all_source_dois:
  - 10.1038/s41467-023-37446-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-filtering-noise-removal

## Summary

Remove noise and low-intensity peaks from raw MS/MS spectra to produce cleaned spectral data suitable for library matching. This preprocessing step eliminates spurious signals that would otherwise degrade spectral similarity scoring and analogue/exact-match search accuracy.

## When to use

Apply this skill when you have raw MS/MS spectra (in formats like mzML, json, mgf, msp, mzxml) that contain background noise or numerous low-intensity peaks before running MS2Query library matching. Use it especially when spectra originate from instruments with high baseline noise or when your MS2 data contains many low-abundance ion signals unrelated to the target compound.

## When NOT to use

- Do not apply peak filtering if your spectra have already been preprocessed (e.g., by MZMine or similar tools) and clustered to a single representative spectrum per feature.
- Do not use this skill in isolation; filtering must be combined with normalization and other preprocessing steps before library matching.
- Do not apply aggressive filtering thresholds that remove legitimate low-abundance fragment ions critical for compound identification.

## Inputs

- raw MS/MS spectra (mgf, mzML, msp, mzxml, json formats)
- intensity threshold or peak-retention parameter
- raw query spectral data objects

## Outputs

- filtered/cleaned spectra with low-intensity peaks and noise removed
- spectral data in format suitable for MS2Deepscore embedding and library matching

## How to apply

Implement filtering logic to remove low-intensity peaks from raw query spectra by setting an intensity threshold or by retaining only the highest-abundance peaks. The filtering should be applied sequentially as part of a complete preprocessing pipeline, together with spectrum normalization, before library matching. According to MS2Query documentation, preprocessing steps like clustering or feature selection via tools such as MZMine are advised to reduce the number of MS2 spectra per feature, and filtering can be applied as part of that workflow. After filtering, validate that cleaned spectra meet expected format and quality criteria — for example, check that peak lists retain sufficient structural information and that the resulting spectrum is not over-sparse.

## Related tools

- **MS2Query** (MS/MS library matching tool that consumes preprocessed and filtered spectra for analogue and exact-match search) — https://github.com/iomega/ms2query
- **MZMine** (Tool for preprocessing, peak picking, and clustering MS2 spectra; can be used upstream of filtering to reduce spectral redundancy) — https://mzmine.github.io/mzmine_documentation/index.html
- **matchms** (Python library for spectrum object handling and preprocessing operations including filtering)

## Examples

```
# Python snippet for filtering within a preprocessing pipeline
from matchms.filtering import normalize_spectra, remove_peaks_below_threshold
# After loading spectra, apply threshold-based filtering followed by normalization
filtered_spectra = [remove_peaks_below_threshold(spec, minimum_intensity=10) for spec in raw_spectra]
normalized_spectra = [normalize_spectra(spec) for spec in filtered_spectra]
# Then pass to MS2Query: ms2query --spectra ./preprocessed_spectra --library ./library_folder --ionmode positive
```

## Evaluation signals

- Verify that the filtered spectrum retains 5–100 peaks (typical range) and does not become sparse or empty.
- Check that peak intensity distribution in the cleaned spectrum is reasonable — no unexpectedly flat or artificially truncated distributions.
- Confirm that the filtered spectrum still represents the target compound's diagnostic fragments (e.g., key product ions).
- Validate that MS2Query model prediction scores on filtered spectra are higher and more reliable than on unfiltered spectra (ideally > 0.7 for true analogues/exact matches).
- Inspect a sample of filtered spectra visually to ensure that structural information has not been lost and that the cleaning process was appropriate.

## Limitations

- No explicit specification in the MS2Query documentation of optimal intensity thresholds or filtering algorithms; threshold selection may require empirical tuning for different instrument types and ionization modes.
- Aggressive filtering can remove genuine low-abundance fragment ions that are diagnostic for certain compound classes, potentially reducing recall for structural variants.
- MS2Query itself does not perform internal peak picking or noise filtering — preprocessing must be done upstream (e.g., with MZMine), so users bear responsibility for appropriate filtering parameter selection.
- Filtering effectiveness is highly dependent on the quality and baseline characteristics of the input raw spectra; poorly calibrated instruments or highly noisy data may require more sophisticated preprocessing than simple intensity-based filtering.

## Evidence

- [readme] MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or feature selection.: "MS2Query does not do any peak picking or clustering of similar MS2 spectra. If your files contain many MS2 spectra per feature it is advised to first reduce the number of MS2 spectra by clustering or"
- [other] Implement filtering logic to remove noise and low-intensity peaks from raw query spectra: "Implement filtering logic to remove noise and low-intensity peaks from raw query spectra."
- [other] Apply the complete pre-processing pipeline sequentially to raw query spectra to produce cleaned spectrum outputs: "Apply the complete pre-processing pipeline sequentially to raw query spectra to produce cleaned spectrum outputs."
- [readme] One reliable method is using MZMine for preprocessing, https://mzmine.github.io/mzmine_documentation/index.html. As input for MS2Query you can use the MGF file of the FBMN output of MZMine: "One reliable method is using MZMine for preprocessing. As input for MS2Query you can use the MGF file of the FBMN output of MZMine"
