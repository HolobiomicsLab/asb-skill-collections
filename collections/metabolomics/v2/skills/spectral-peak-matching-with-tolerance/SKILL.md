---
name: spectral-peak-matching-with-tolerance
description: Use when when comparing a query MS/MS spectrum (e.g., from an unknown metabolite) against a library spectrum to establish correspondence between peaks. Use this skill before calculating similarity scores (cosine, entropy, Bhattacharyya) or when applying penalty factors to unmatched peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - cosine.py
  - entropy.py
  - bhattacharya1.py
derived_from:
- doi: 10.1021/acs.analchem.5c02047
  title: Reverse Spectral Search
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_reverse_spectral_search_cq
    doi: 10.1021/acs.analchem.5c02047
    title: Reverse Spectral Search
  dedup_kept_from: coll_reverse_spectral_search_cq
schema_version: 0.2.0
---

# spectral-peak-matching-with-tolerance

## Summary

Identify and match peaks between query and library MS/MS spectra within a specified m/z tolerance threshold, forming the foundation for similarity scoring in spectral searching. This step is critical for discriminating true spectral matches from noise and controlling false positives in chimeric spectra.

## When to use

When comparing a query MS/MS spectrum (e.g., from an unknown metabolite) against a library spectrum to establish correspondence between peaks. Use this skill before calculating similarity scores (cosine, entropy, Bhattacharyya) or when applying penalty factors to unmatched peaks. Particularly valuable when the input spectra may contain chimeric fragments and you need to control match stringency via tolerance.

## When NOT to use

- Input spectra are already aligned or pre-processed into common m/z grids; use direct element-wise comparison instead.
- Tolerance threshold is unknown or data quality is too poor to justify tolerance-based matching (e.g., uncalibrated instruments with >1 Da mass error).
- You are performing de novo sequencing or spectral deconvolution where peak correspondence is not the bottleneck.

## Inputs

- query MS/MS spectrum (array of m/z–intensity pairs)
- library MS/MS spectrum (array of m/z–intensity pairs)
- m/z tolerance threshold (scalar, in Da or ppm)

## Outputs

- list of matched peak pairs (query m/z, library m/z, query intensity, library intensity)
- list of unmatched query peaks (m/z, intensity)

## How to apply

Load both the query MS/MS spectrum (m/z and intensity pairs) and the library MS/MS spectrum. Iterate through each peak in the query spectrum and find all library peaks whose m/z values fall within the specified tolerance threshold (typically 0.01–0.1 Da or ppm-based). For each query peak with a match, record the pair; peaks outside tolerance are marked as unmatched. The m/z tolerance acts as the primary control: tighter tolerances reduce spurious matches but may miss true signals; looser tolerances increase sensitivity but risk including noise. Store matched peak pairs for downstream scoring calculations, and separately track unmatched query peaks for potential penalty application in reverse spectral search workflows.

## Related tools

- **cosine.py** (Calculates cosine similarity on matched peaks to produce symmetric and reverse spectral search scores) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/cosine.py
- **entropy.py** (Computes entropy-based similarity metric on matched peak sets) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/entropy.py
- **bhattacharya1.py** (Calculates Bhattacharyya angle similarity on matched peaks) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/bhattacharya1.py

## Evaluation signals

- Matched peak list contains only pairs where library m/z − query m/z ≤ tolerance; no out-of-tolerance pairs are included.
- Unmatched query peaks list contains exactly those query peaks for which no library peak exists within tolerance.
- Total matched + unmatched query peaks equals total query peaks (completeness check).
- When tolerance is tightened, number of matched pairs decreases or remains constant; when loosened, it increases or remains constant (monotonicity).
- Manual inspection of a few matched pairs confirms biological plausibility (e.g., expected fragment ions from known precursor m/z and ionization mode).

## Limitations

- Performance degrades with high spectral density (many peaks close together) if tolerance is not calibrated to instrument resolution.
- Tolerance must be consistent with mass calibration quality; poorly calibrated spectra will cause mismatches even with appropriate tolerance.
- Peak matching is agnostic to intensity; two peaks may match by m/z alone even if intensity patterns suggest they are unrelated, leading to inflated or spurious similarity scores.
- No consideration of isotope patterns, adducts, or neutral losses; simple m/z-based matching may conflate related but distinct species.

## Evidence

- [other] Identify matched peaks between query and library using a specified m/z tolerance threshold.: "Identify matched peaks between query and library using a specified m/z tolerance threshold."
- [readme] Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation.: "Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation."
- [readme] enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control.: "enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control."
- [other] Load the query MS/MS spectrum (m/z and intensity pairs) and the library MS/MS spectrum.: "Load the query MS/MS spectrum (m/z and intensity pairs) and the library MS/MS spectrum."
