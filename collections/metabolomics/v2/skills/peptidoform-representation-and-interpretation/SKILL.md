---
name: peptidoform-representation-and-interpretation
description: Use when when you have a tandem mass spectrometry spectrum with a known or inferred peptide sequence that may contain post-translational modifications (phosphorylation, glycosylation, cross-links), and you need to annotate which observed m/z peaks correspond to specific fragment ion types (b, y, a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - matplotlib
  - spectrum_utils
  - ProForma 2.0
  - Unimod
  - PSI-MOD
  - XL-MOD
  - Glycan Naming Ontology
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- import matplotlib.pyplot as plt
- fig, ax = plt.subplots(figsize=(12, 6))
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
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

# peptidoform-representation-and-interpretation

## Summary

Represent and interpret modified peptides using the ProForma 2.0 specification to annotate observed mass spectrometry fragments with ion types and modifications. This skill enables systematic labeling of b and y ions with chemical modifications tracked via controlled vocabularies (Unimod, PSI-MOD, XL-MOD, Glycan Naming Ontology), facilitating publication-quality spectrum visualization and fragment validation.

## When to use

When you have a tandem mass spectrometry spectrum with a known or inferred peptide sequence that may contain post-translational modifications (phosphorylation, glycosylation, cross-links), and you need to annotate which observed m/z peaks correspond to specific fragment ion types (b, y, a ions) to validate the peptidoform and visualize it in a publication-ready format.

## When NOT to use

- Spectrum has no prior peptide sequence assignment — annotation requires a known or hypothesized peptidoform to generate theoretical fragments.
- Fragment tolerance is too stringent (< 1 ppm for low-resolution instruments) or too permissive (> 100 ppm), leading to spurious or missed matches.
- Modifications are not represented in any supported controlled vocabulary (Unimod, PSI-MOD, XL-MOD, Glycan Naming Ontology) — custom or rare modifications cannot be reliably encoded.

## Inputs

- MsmsSpectrum object with observed m/z and intensity arrays
- ProForma 2.0 peptide string (unmodified or with modification annotations)
- Fragment tolerance value and tolerance mode (ppm or Da)
- Ion types to annotate (e.g., 'by', 'aby')

## Outputs

- Annotated MsmsSpectrum object with matched fragment peaks labeled by ion type
- Publication-quality spectrum plot (PNG, PDF, or matplotlib Figure) showing annotated peaks
- Fragment annotation metadata (matched m/z, theoretical m/z, ion type, residue position)

## How to apply

Construct a ProForma 2.0-compliant peptide string representing the modified sequence, using controlled modification vocabularies (Unimod, PSI-MOD) to encode known or suspected chemical modifications. Call the spectrum_utils `annotate_proforma()` method, specifying the peptide string, fragment tolerance (e.g., 10 ppm), tolerance mode ('ppm' or 'Da'), and desired ion_types (e.g., 'by' for b and y ions). The method will match observed spectrum peaks to theoretical fragment masses derived from the peptidoform, labeling matches in the spectrum object. Render the annotated spectrum using `spectrum_utils.plot.spectrum()` with customizable grid and spine settings. The annotation output is correct when peak labels match expected ion types and masses fall within the specified fragment tolerance of the theoretical values.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum class, annotate_proforma() method, and plot.spectrum() visualization function) — https://github.com/bittremieux/spectrum_utils/
- **ProForma 2.0** (Standard notation for representing modified peptide sequences with machine-parseable modification syntax) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary for common protein post-translational modifications referenced in ProForma strings) — https://www.unimod.org/
- **PSI-MOD** (Controlled vocabulary for protein modifications complementing Unimod for specialized PTMs) — https://github.com/HUPO-PSI/psi-mod-CV/
- **XL-MOD** (Controlled vocabulary for cross-linking modifications in modified peptides) — https://arxiv.org/abs/2003.00329
- **Glycan Naming Ontology** (Controlled vocabulary for glycan modifications on peptides) — https://gnome.glyomics.org/
- **matplotlib** (Backend graphics library used by spectrum_utils.plot for rendering annotated spectra)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
spectrum.annotate_proforma('PEPT[Phospho]IDE', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='by')
fig, ax = spectrum_utils.plot.spectrum(spectrum, grid=False)
fig.savefig('annotated_spectrum.png', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- Annotated peaks exactly match theoretical fragment m/z values within the specified fragment tolerance (ppm or Da); verify by comparing peak labels to hand-calculated or reference b/y ion masses.
- All expected fragment ions within the m/z range and intensity threshold are labeled; count labeled peaks against predicted number for the given ion_types.
- Output spectrum plot clearly distinguishes annotated peaks (labeled with ion type and position) from unannotated peaks; visual inspection confirms legibility and correct spine/grid settings.
- ProForma string parses without error and modifications are recognized in the supported controlled vocabularies; verify via spectrum_utils internal validation or by querying Unimod/PSI-MOD databases.
- Annotated spectrum is reproducible: re-running with the same peptide, tolerance, and ion_types parameters produces identical peak labels and plot appearance.

## Limitations

- Annotation relies on accurate fragment tolerance specification; mismatches between declared tolerance and instrument resolution will result in false negatives (missed matches) or false positives (incorrect assignments).
- Only modifications explicitly registered in Unimod, PSI-MOD, XL-MOD, or Glycan Naming Ontology can be encoded in ProForma; rare, novel, or custom modifications require either vocabulary extension or manual annotation outside this framework.
- The method assumes the peptide sequence is correct; misidentified or incorrect sequences will produce spurious annotations that appear internally consistent but may not reflect true fragment ions in the spectrum.
- Interactive spectrum visualization (mentioned in the README) is not fully documented; customization options for interactive plots beyond publication-quality static images may require direct library exploration.

## Evidence

- [other] fragment ions can be annotated based on the ProForma 2.0 specification: "fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification"
- [other] Modifications are defined by controlled vocabularies including Unimod, PSI-MOD, and support for cross-linking and glycans: "Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/), [PSI-MOD](https://github.com/HUPO-PSI/psi-mod-CV/), including support for modifications from"
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] spectrum_utils provides capabilities for annotating observed spectrum fragments using ProForma and ProForma peptide string annotation with fragment tolerance: ".annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types="aby")"
- [intro] Publication-quality and interactive spectrum plotting with full customization: "Publication-quality, fully customizable spectrum plotting and interactive spectrum plotting."
