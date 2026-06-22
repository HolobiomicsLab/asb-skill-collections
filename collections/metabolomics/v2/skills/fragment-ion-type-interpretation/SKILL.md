---
name: fragment-ion-type-interpretation
description: Use when you have an tandem MS spectrum with unidentified peaks and a known or hypothesized peptide sequence (in ProForma 2.0 format, including post-translational modifications).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - matplotlib
  - ProForma 2.0
  - PSI-MOD CV
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragment-ion-type-interpretation

## Summary

Annotate observed mass spectrometry fragment peaks by matching them to theoretical fragment ions (a, b, y types and neutral losses) derived from a known peptide sequence using ProForma 2.0 notation. This enables visual and quantitative identification of which peaks correspond to expected peptide backbone cleavage products.

## When to use

You have an tandem MS spectrum with unidentified peaks and a known or hypothesized peptide sequence (in ProForma 2.0 format, including post-translational modifications). You want to overlay theoretical fragment ion m/z values onto the observed spectrum to highlight which peaks represent b-ions, y-ions, a-ions, and neutral loss variants, with a user-specified mass tolerance (e.g., 10 ppm or 0.05 Da).

## When NOT to use

- The peptide sequence is unknown or highly uncertain—annotation requires a ground-truth ProForma string.
- The spectrum has already been assigned via database search or other spectral matching and you seek only visualization, not de novo fragment identification.
- Fragment tolerance is not biologically justified or instrument-appropriate for the given mass analyzer (e.g., using 0.01 Da tolerance for a low-resolution ion trap).

## Inputs

- MsmsSpectrum object (spectrum_utils.spectrum.MsmsSpectrum)
- ProForma 2.0 peptide string (e.g., '[Acetyl]-PEPTIDEK[Phospho]')
- Fragment mass tolerance (numeric, in Da or ppm)
- Fragment tolerance mode ('Daltons' or 'ppm')
- Ion types string (e.g., 'aby')

## Outputs

- Annotated MsmsSpectrum object with matched fragments
- Peak-to-ion assignment mapping (visible in annotation field)
- Optional: Publication-quality spectrum plot with annotated peaks highlighted

## How to apply

Load the spectrum as an MsmsSpectrum object (e.g., via Universal Spectrum Identifier). Define a ProForma 2.0 peptide string representing the measured peptidoform, including any modifications. Call spectrum.annotate_proforma() with parameters for fragment_tol_mass, fragment_tol_mode ('Daltons' or 'ppm'), and ion_types (e.g., 'aby' for a-, b-, and y-ions). The method computes all theoretical m/z values for those ion types and matches them to observed peaks within the specified tolerance. Neutral losses (e.g., from serine/threonine phosphorylation) can be included. The result is an annotated spectrum object where matched peaks are labeled with their ion assignment; visualization via spectrum_utils.plot.spectrum() then highlights these annotations in publication-quality figures.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class and annotate_proforma() method for matching observed peaks to theoretical fragment ions) — https://github.com/bittremieux/spectrum_utils
- **matplotlib** (Renders annotated spectra as publication-quality static plots via spectrum_utils.plot.spectrum())
- **ProForma 2.0** (Notation standard for unambiguous representation of peptide sequences with post-translational modifications) — https://www.psidev.info/proforma
- **PSI-MOD CV** (Ontology of protein modifications used to disambiguate modification names in ProForma strings) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
spectrum = spectrum_utils.spectrum.MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475'); spectrum.annotate_proforma('PEPTIDEK', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='aby')
```

## Evaluation signals

- Number and fraction of observed peaks assigned to theoretical fragments (e.g., >40% of intensity explained by matched ions indicates good annotation quality).
- Mass error distribution of matched peaks should be centered near zero and within the specified tolerance (e.g., mean <2 ppm, std <3 ppm for a 10 ppm tolerance).
- Presence of expected diagnostic ions for the peptide (e.g., N-terminal b-ions, C-terminal y-ions) validates that the sequence and tolerance are correct.
- Visual inspection of the plot confirms that highlighted peaks align with observed spectral features (no false matches to noise or non-existent m/z values).
- Reproducibility: re-running annotation with the same parameters and ProForma string yields identical peak assignments.

## Limitations

- Annotation accuracy depends critically on correct ProForma 2.0 specification; missing or misplaced modifications will cause fragment m/z mismatches and false negatives.
- Fragment tolerance must be tuned to the mass analyzer type (e.g., Orbitrap requires tighter tolerance than ion trap); inappropriate tolerance leads to either missed matches or spurious assignments.
- Neutral loss prediction is limited to hard-coded or user-specified loss masses; complex fragmentation pathways (e.g., sequential or rearrangement losses) are not modeled.
- High-intensity background noise or isotopic overlaps can mask or falsely occupy candidate fragment m/z slots.
- No changelog found, so version-to-version changes in annotation algorithm or default parameters are not explicitly documented.

## Evidence

- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string.: "Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string"
- [other] Call spectrum_utils.annotate_proforma() with specified fragment tolerance (mass and mode), ion types, and optionally neutral losses.: "annotate the spectrum with a ProForma 2.0 peptide string using spectrum.annotate_proforma() with specified fragment tolerance (mass and mode), ion types (e.g., 'aby'), and optionally neutral losses."
- [intro] Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting.: "Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting."
- [other] Visualize the spectrum with the annotated peaks highlighted: "Visualize the spectrum with the annotated peaks highlighted"
