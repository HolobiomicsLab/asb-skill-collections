---
name: ion-type-classification-and-filtering
description: Use when you have an MS/MS spectrum and a ProForma 2.0 peptidoform specification,
  and you need to identify which observed peaks correspond to specific fragment ion
  types (e.g., only b and y ions for backbone fragmentation, or immonium ions for
  amino acid identification).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - PSI-MOD (HUPO-PSI Protein Modifications Ontology)
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

# ion-type-classification-and-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Selectively annotate and visualize peptide fragment ions of specified types (a, b, y, immonium, internal, etc.) from tandem mass spectrometry spectra. This skill enables targeted interpretation of observed peaks by restricting annotation to biologically or analytically relevant fragment ion series, improving spectrum clarity and reducing false-positive peak assignments.

## When to use

Apply this skill when you have an MS/MS spectrum and a ProForma 2.0 peptidoform specification, and you need to identify which observed peaks correspond to specific fragment ion types (e.g., only b and y ions for backbone fragmentation, or immonium ions for amino acid identification). Use it to focus annotation on ion types relevant to your research question—e.g., excluding internal fragments if they complicate interpretation, or including immonium ions when identifying modified residues.

## When NOT to use

- Ion type is unknown or ambiguous—spectrum_utils annotation requires explicit ion_types specification; do not use if you cannot decide a priori which fragments are relevant.
- Spectrum is already fully interpreted or you need de novo fragment ion discovery without a reference peptide—ion-type classification assumes a known peptidoform.
- Fragment mass tolerance is extremely large (>100 ppm or >1 Da)—the tolerance-based matching will produce too many false matches across ion types to be disambiguated by type label alone.

## Inputs

- MsmsSpectrum object (with m/z, intensity, precursor m/z, charge, retention time)
- ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK')
- fragment tolerance parameters (mass value and mode: 'ppm' or 'Da')

## Outputs

- Annotated MsmsSpectrum object with FragmentAnnotation records linked to peaks
- Peak annotations including ion type, charge state, neutral loss label, isotope state, and matched intensity

## How to apply

After loading an MsmsSpectrum object and parsing the ProForma 2.0 peptidoform string, call MsmsSpectrum.annotate_proforma() with the ion_types parameter set to your desired combination: 'by' (default: b and y ions), 'abc' (a, b, c primary fragments), 'xyz' (x, y, z complementary fragments), 'I' (immonium ions for side chains), or 'm' (internal fragments). The annotation engine computes theoretical m/z values for only the specified ion types and charge states, then performs tolerance-based matching against observed peaks using fragment_tol_mass and fragment_tol_mode ('ppm' or 'Da'). The resulting annotated spectrum links FragmentAnnotation records to peaks, each tagged with its ion type label. Choose ion_types based on your fragmentation model: backbone-only analyses use 'by'; comprehensive characterization includes 'abcxyz'; diagnostic amino acid identification includes 'I'. Visualization of the annotated spectrum with ion-type-specific highlighting confirms correct classification.

## Related tools

- **spectrum_utils** (Core library providing MsmsSpectrum class, annotate_proforma() method, and FragmentAnnotation record generation; handles ion-type specification and tolerance-based peak matching.) — https://github.com/bittremieux/spectrum_utils
- **PSI-MOD (HUPO-PSI Protein Modifications Ontology)** (Provides standardized modification vocabulary (via MOD: prefix) and human-readable names (e.g., Oxidation, Phospho) used in ProForma 2.0 peptidoform strings for ion-type-specific annotation.) — https://github.com/HUPO-PSI/psi-mod-CV

## Examples

```
spectrum.annotate_proforma('EM[Oxidation]EVEES[Phospho]PEK', fragment_tol_mass=20, fragment_tol_mode='ppm', ion_types='aby')
```

## Evaluation signals

- Returned FragmentAnnotation records have non-empty ion_type field matching one of the requested types (e.g., 'b', 'y', 'I'); no annotations exist for ion types not specified in ion_types parameter.
- Matched peak m/z values fall within the fragment_tol_mass window (in ppm or Da units) of the theoretical m/z for their annotated ion and charge state.
- Spectrum visualization highlights annotated peaks grouped by ion type, showing no overlap or spurious assignments across incompatible fragment series.
- Peak count and intensity distribution per ion type are consistent with known fragmentation patterns for the peptide sequence and modification state.
- Exclusion of an ion type (e.g., removing 'I' from 'abcI') reduces the total number of annotations by roughly the proportion of immonium ions expected in the mass range.

## Limitations

- Ion-type classification is deterministic only after peaks are matched: ambiguous or overlapping theoretical m/z values (especially for high-charge fragments or heavily modified peptides) may cause incorrect ion-type assignment if peaks fall within tolerance of multiple fragment types.
- Neutral loss annotation (e.g., NH3, H2O) is optional and provided as a user-supplied dictionary; if not specified, neutral-loss variants are not distinguished, reducing granularity of ion characterization.
- The method assumes the input ProForma 2.0 string is correctly formatted and unambiguous; malformed or overly ambiguous modification specifications will cause parsing errors or silently incorrect annotations.
- Internal fragments ('m' ion type) and immonium ions ('I') are less commonly used in standard peptide identification workflows; their annotation may be less well-validated than b and y ions, especially for non-standard modifications.

## Evidence

- [other] Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal), and optional neutral losses dictionary.: "Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for"
- [other] The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using fragment_annotation module.: "The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using"
- [other] Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity.: "Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity."
- [other] Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string: "Annotate peaks corresponding to a, b, and y peptide fragments in the spectrum based on a ProForma 2.0 peptide string"
- [readme] spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
