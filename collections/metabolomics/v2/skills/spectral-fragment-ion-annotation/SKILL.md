---
name: spectral-fragment-ion-annotation
description: Use when you have an MS/MS spectrum (m/z and intensity arrays) and a known or hypothesized peptide sequence (optionally with post-translational modifications in ProForma 2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - HUPO-PSI/psi-mod-CV
  - NumPy
  - Numba
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
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
---

# spectral-fragment-ion-annotation

## Summary

Annotate observed MS/MS spectrum peaks against theoretical fragment ions (a, b, y, and other ion types) derived from a ProForma 2.0 peptidoform specification, using tolerance-based matching to link experimental m/z values to predicted fragment masses and charge states. This enables identification and visualization of peptide fragmentation patterns in tandem mass spectrometry data.

## When to use

You have an MS/MS spectrum (m/z and intensity arrays) and a known or hypothesized peptide sequence (optionally with post-translational modifications in ProForma 2.0 format), and you need to identify which observed peaks correspond to specific fragment ion types (b-ions, y-ions, a-ions, immonium ions, internal fragments, etc.) to validate the peptide identification, diagnose fragmentation behavior, or prepare publication-quality annotated spectra.

## When NOT to use

- The input spectrum is not MS/MS (tandem) data — this skill requires fragmentation peaks from collision-induced dissociation or similar activation; a single MS1 spectrum has no fragment ions to annotate.
- The peptide sequence is unknown or ambiguous — annotation requires a ground-truth ProForma 2.0 string; use only for validation or targeted re-analysis of suspected sequences, not for de novo sequencing.
- The fragment tolerance window is too narrow or the mass calibration is poor — mismatches will lead to few or no annotations; verify instrument mass accuracy (typically ≤ 5–10 ppm for high-resolution MS) before annotation.

## Inputs

- MsmsSpectrum object (m/z array, intensity array, precursor m/z, precursor charge, retention time)
- ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or MOD:-style notation)
- Fragment mass tolerance value (float, e.g., 10.0)
- Fragment tolerance mode (string: 'ppm' or 'Da')
- Ion types specification (string, e.g., 'aby' or 'by')
- Optional: neutral losses dictionary (dict of {loss_name: mass_delta})

## Outputs

- Annotated MsmsSpectrum object with FragmentAnnotation records
- FragmentAnnotation list entries (each containing: observed m/z, theoretical m/z, ion type, charge state, neutral loss label, isotope state, peak intensity)
- Visualizable spectrum object with highlighted/labeled fragment peaks

## How to apply

Load or construct an MsmsSpectrum object with precursor m/z, charge, and observed peak m/z and intensity arrays. Parse the peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK') using spectrum_utils.proforma to extract the amino acid sequence and position-specific modifications. Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment mass tolerance (typically 10–20 ppm or 0.05–0.1 Da), tolerance mode ('ppm' or 'Da'), and desired ion_types (default 'by' for b and y ions; can include 'abc' for a/b/c primary fragments, 'xyz' for x/y/z fragments, 'I' for immonium, 'm' for internal). Optionally specify a neutral_losses dictionary (e.g., {'NH3': -17.026549, 'H2O': -18.010565}) to model common loss ions. The annotation engine computes all theoretical fragment m/z values for the specified ion types and charge states (1+, 2+, etc.), then performs tolerance-based matching against observed peaks. Verify success by inspecting the returned FragmentAnnotation records linked to peaks (include ion type, charge, neutral loss label, isotope state, and matched intensity) and visually confirming the annotated spectrum shows peaks at expected positions.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum class, annotate_proforma() method, fragment_annotation module, and ProForma 2.0 parsing) — https://github.com/bittremieuxlab/spectrum_utils
- **HUPO-PSI/psi-mod-CV** (Protein Modifications Ontology providing standardized PSI-MOD accessions for modification names (MOD:* notation) used in ProForma strings) — https://github.com/HUPO-PSI/psi-mod-CV
- **NumPy** (Computational backend optimizing fragment m/z array operations and tolerance-based matching for large peak lists)
- **Numba** (JIT compiler accelerating inner loops of fragment matching algorithms for computational efficiency)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; spectrum = MsmsSpectrum(mz=observed_mz, intensity=observed_intensity, precursor_mz=precursor_mz, precursor_charge=2, retention_time=rt); spectrum.annotate_proforma('EM[Oxidation]EVEES[Phospho]PEK', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby')
```

## Evaluation signals

- All returned FragmentAnnotation records have observed m/z within the specified fragment tolerance (ppm or Da) of their theoretical m/z; verify by checking |observed_mz - theoretical_mz| ≤ tolerance_threshold.
- Charge states of annotated fragments are valid (typically 1+, 2+, or higher for singly/multiply charged ions); check that all annotation.charge ≥ 1.
- Ion type labels (a, b, y, etc.) follow the peptidoform specification and match the sequence length; e.g., a b-ion at position i should correspond to residues 1..i.
- Annotated peaks correspond to intense features in the spectrum (not noise); verify that annotated peaks have intensity ≥ 5% of base peak intensity if noise filtering was applied.
- Visual inspection of the annotated spectrum shows fragment peaks at expected positions (e.g., b and y ions forming a ladder pattern); compare against reference spectra or literature fragmentation patterns for the peptide.

## Limitations

- Annotation assumes the input peptidoform string is correct; sequence mis-assignments or incorrect modification assignments will produce spurious or incomplete annotations.
- Fragment tolerance must be empirically tuned to the mass spectrometer's actual accuracy; overly tight tolerances miss real fragments, overly loose tolerances produce false matches.
- Neutral loss models (e.g., H2O, NH3) are manually specified; the algorithm will not discover unexpected or instrument-specific neutral losses.
- Low-abundance fragments or isotopic variants may be missed if they fall below the intensity threshold or lie at spectrum edges; preprocessing steps (noise removal, m/z range filtering) affect annotation completeness.
- Modifications not present in the ProForma string or PSI-MOD ontology cannot be represented; custom or novel PTMs require manual workaround or extension of the modification vocabulary.

## Evidence

- [other] MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal), and optional neutral losses dictionary: "Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for"
- [other] The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using fragment_annotation module.: "The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using"
- [other] Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity.: "Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms"
- [readme] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization"
