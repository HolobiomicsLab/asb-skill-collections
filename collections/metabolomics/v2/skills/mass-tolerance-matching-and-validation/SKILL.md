---
name: mass-tolerance-matching-and-validation
description: Use when you have an MS/MS spectrum with observed peaks and a peptidoform
  specification (e.g., ProForma 2.0 notation such as 'EM[Oxidation]EVEES[Phospho]PEK'),
  and you need to annotate which observed peaks correspond to known fragment ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - NumPy
  - Numba
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-tolerance-matching-and-validation

## Summary

Matches observed peaks in a mass spectrometry spectrum to theoretical fragment ions within a specified mass tolerance window, validating fragment annotation by comparing observed m/z values against computed theoretical m/z values for peptide fragments (a, b, y, etc.) with configurable tolerance in parts-per-million (ppm) or Daltons (Da).

## When to use

You have an MS/MS spectrum with observed peaks and a peptidoform specification (e.g., ProForma 2.0 notation such as 'EM[Oxidation]EVEES[Phospho]PEK'), and you need to annotate which observed peaks correspond to known fragment ions. Use this skill when you must validate fragment assignments by determining which observed m/z values fall within an acceptable mass error of the theoretical fragment m/z, accounting for different ion types (b, y, a, immonium, internal fragments) and optional neutral losses.

## When NOT to use

- Input spectrum has not been cleaned (precursor peak and noise peaks should be removed before annotation to avoid false matches).
- Peptidoform specification is invalid or incomplete (missing or incorrectly formatted ProForma notation).
- Tolerance window is set too wide (e.g., >50 ppm on a high-resolution instrument), risking spurious matches to unrelated peaks.

## Inputs

- MsmsSpectrum object (m/z array, intensity array, precursor m/z, charge state, retention time)
- ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK')
- Fragment mass tolerance value (numeric)
- Fragment mass tolerance mode ('ppm' or 'Da')
- Ion types to match (string, e.g., 'aby' for a, b, y fragments)

## Outputs

- Annotated MsmsSpectrum object with FragmentAnnotation records
- Peak-to-fragment mappings (ion type, charge, neutral loss, isotope state, matched m/z, intensity)

## How to apply

First, compute theoretical m/z values for all requested fragment ion types and charge states from the peptidoform specification using the ProForma parser. Then perform tolerance-based matching by checking whether each observed peak's m/z lies within the specified fragment tolerance window (e.g., ±10 ppm or ±0.05 Da) of any theoretical fragment m/z. The tolerance mode (ppm vs. Da) is critical: ppm tolerance scales with m/z (suitable for high-resolution instruments), while Da tolerance is absolute (suitable for lower-resolution data). Annotate matching peaks with their ion type, charge state, neutral loss label (if applicable), and isotope state. Finally, evaluate annotation quality by verifying that matched peaks show intensity patterns consistent with fragmentation (e.g., y-ion ladder or b-ion ladder continuity).

## Related tools

- **spectrum_utils** (Provides the annotate_proforma method and fragment_annotation module for tolerance-based peak-to-fragment matching on MsmsSpectrum objects.) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Enables efficient vectorized computation of theoretical m/z values and tolerance range calculations for matching.)
- **Numba** (JIT-compiles the tolerance-based matching loop for computational efficiency on large peak sets.)

## Examples

```
spectrum.annotate_proforma('EM[Oxidation]EVEES[Phospho]PEK', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby')
```

## Evaluation signals

- All returned FragmentAnnotation records have matched observed m/z values within the specified tolerance window of their theoretical m/z.
- Charge states of annotated fragments are consistent with the precursor charge and fragmentation rules (e.g., no charge state higher than precursor).
- Annotated ion sequences (a, b, y, etc.) form expected fragmentation ladders with no gaps indicating missing or misassigned fragments.
- Neutral loss labels (if present) correspond to expected losses (e.g., H₂O = −18.010565 Da, NH₃ = −17.026549 Da) recorded in the provided neutral losses dictionary.
- The number and intensity distribution of matched peaks are consistent with instrument resolution and expected fragmentation intensity profile.

## Limitations

- Tolerance-based matching can produce false positives if the tolerance window is too wide or if the spectrum contains high background noise that was not adequately removed in preprocessing.
- The skill assumes accurate knowledge of the true peptidoform (including all modifications and their positions); incorrect or incomplete ProForma notation will lead to mismatched fragments.
- Neutral loss matching depends on a pre-defined neutral losses dictionary; unexpected or non-standard losses will not be detected.
- The skill does not account for overlapping isobaric peaks or isotopologue patterns; high-resolution mass spectra may require additional isotope-aware post-processing.

## Evidence

- [other] The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using fragment_annotation module.: "computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks"
- [other] Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal), and optional neutral losses dictionary.: "fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal), and optional neutral losses"
- [other] Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity.: "FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity"
- [other] Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string using the annotate_proforma method with parameters for fragment mass tolerance, tolerance mode, and ion types.: "annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string using the annotate_proforma method with parameters for fragment mass tolerance,"
