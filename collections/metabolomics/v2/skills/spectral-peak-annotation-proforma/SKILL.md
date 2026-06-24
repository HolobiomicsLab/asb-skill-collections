---
name: spectral-peak-annotation-proforma
description: Use when you have an annotated or raw tandem mass spectrometry spectrum
  and need to identify which observed peaks correspond to expected peptide fragment
  ions from a known or predicted peptidoform. Use it before spectrum visualization
  if you want highlighted, labeled fragment matches;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - HUPO-PSI PSI-MOD CV
  techniques:
  - LC-MS
  license_tier: restricted
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

# Spectral Peak Annotation via ProForma 2.0

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Annotate observed m/z peaks in tandem mass spectrometry spectra by matching them against theoretical fragment ions generated from a ProForma 2.0 peptide sequence specification. This enables identification and labeling of fragment types (e.g., a, b, y ions) and their corresponding neutral losses for publication-quality spectrum visualization.

## When to use

Apply this skill when you have an annotated or raw tandem mass spectrometry spectrum and need to identify which observed peaks correspond to expected peptide fragment ions from a known or predicted peptidoform. Use it before spectrum visualization if you want highlighted, labeled fragment matches; or after spectrum preprocessing (noise removal, intensity filtering) if working with real proteomics data.

## When NOT to use

- Input spectrum has no known or hypothesized peptide sequence — use de novo or library search methods instead.
- Spectrum has not been preprocessed for noise and precursor removal — annotation accuracy will be degraded by competing high-intensity noise peaks; preprocess first using filter_intensity() and remove_precursor_peak().
- ProForma syntax is invalid or the peptide string does not conform to ProForma 2.0 specification — annotation will fail or produce unreliable results.

## Inputs

- MsmsSpectrum object (spectrum_utils.spectrum.MsmsSpectrum)
- ProForma 2.0 peptide string (e.g., '[Phospho]-PEPTIDE[Carbamidomethyl]')
- fragment tolerance mass (Da or ppm)
- fragment tolerance mode ('Da' or 'ppm')
- ion types string (e.g., 'aby', 'abcy')

## Outputs

- Annotated MsmsSpectrum with peak-to-fragment mappings stored
- Peak annotations including fragment type, charge, and neutral loss
- List or dictionary of matched peaks with their assigned ion identities

## How to apply

Load or construct an MsmsSpectrum object (e.g., via spectrum_utils.spectrum.MsmsSpectrum.from_usi() for USI-identified spectra). Provide a ProForma 2.0 peptide string representing the target peptidoform, including any post-translational modifications in ProForma syntax. Call spectrum.annotate_proforma() with parameters: the peptide string, fragment_tol_mass (e.g., 10 Da or ppm tolerance), fragment_tol_mode (absolute or relative), and ion_types (e.g., 'aby' for a, b, y fragments). Optionally specify neutral_losses to match ions with water or ammonia loss. The method matches theoretical m/z values for each ion type against observed peaks within the specified mass tolerance, storing matched peak annotations in the spectrum object. Verification is done by inspecting the annotated spectrum object's peak annotations or by visualizing with spectrum_utils.plot.spectrum() to confirm fragments are highlighted correctly.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class and annotate_proforma() method for fragment matching and annotation) — https://github.com/bittremieux/spectrum_utils
- **Python** (Language runtime for executing spectrum_utils code)
- **HUPO-PSI PSI-MOD CV** (Ontology resource for standardized protein modification names used in ProForma syntax) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
spectrum = spectrum_utils.spectrum.MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.annotate_proforma('PEPTIDE', fragment_tol_mass=10, fragment_tol_mode='Da', ion_types='aby')
```

## Evaluation signals

- Annotated spectrum object contains non-empty peak annotation records mapping observed peaks to fragment types (e.g., 'b3', 'y5+1', 'a4-H2O').
- Number of matched peaks and matched ion types are consistent with expected fragmentation pattern for the peptide length and ion types requested (e.g., a b/y ladder coverage).
- Fragment m/z values in annotations fall within the specified fragment_tol_mass of observed peak m/z values.
- Visualization of the annotated spectrum (via spectrum_utils.plot.spectrum()) shows highlighted peaks that align visually with the annotated fragment positions.
- No annotation errors or exceptions raised; ProForma string is successfully parsed and theoretical fragments generated.

## Limitations

- Annotation requires a correct or well-hypothesized peptide sequence; incorrect ProForma input produces incorrect or empty annotations.
- Fragment tolerance (mass and mode) significantly affects sensitivity and false positive rate; too loose a tolerance risks spurious matches; too strict may miss true fragments due to calibration error.
- High-intensity noise or contaminating peaks in unpreprocessed spectra can be erroneously matched if they fall within tolerance of theoretical fragments; preprocessing (noise filtering, precursor removal) is strongly recommended.
- ProForma 2.0 specification support depends on the version of spectrum_utils; complex modifications or edge-case syntax may not be fully supported.
- Neutral loss annotation is optional; specifying incorrect or incomplete neutral loss sets (e.g., omitting phospho-specific losses) will miss real but unlabeled fragment types.

## Evidence

- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] Workflow step from article showing annotation step in practice: "Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string"
- [other] Concrete API call showing annotate_proforma method and parameters: "spectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types="aby")"
- [other] Preprocessing step context showing annotation occurs post-cleanup: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Spectrum loading mechanism for input: "Load a spectrum from an online data resource by its Universal Spectrum Identifier (USI)"
