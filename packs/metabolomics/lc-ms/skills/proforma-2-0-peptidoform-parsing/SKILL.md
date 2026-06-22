---
name: proforma-2-0-peptidoform-parsing
description: Use when you have a ProForma 2.0 peptidoform string (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - ProForma 2.0
  - Unimod
  - spectrum_utils
  - PSI-MOD
  - XL-MOD
  - Glycan Naming Ontology
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
- Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/)
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification
- 'Specify modifications by their name: `EM[Oxidation]EVEES[Phospho]PEK`'
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

# ProForma 2.0 Peptidoform Parsing

## Summary

Parse ProForma 2.0 notation strings to extract peptide sequences, modification positions, and ion types for fragment annotation in mass spectrometry. This skill enables standardized representation of modified peptidoforms and supports downstream ion annotation workflows.

## When to use

Use this skill when you have a ProForma 2.0 peptidoform string (e.g., 'DLTDYLM[Oxidation]K') and need to extract the underlying peptide sequence, identify modification sites and types (from Unimod or PSI-MOD vocabularies), and prepare the peptidoform for theoretical fragment ion calculation and spectrum annotation.

## When NOT to use

- Input is unmodified peptide sequence with no modifications—direct string parsing is sufficient; ProForma parsing adds unnecessary complexity.
- Modifications use non-standard or proprietary notation not covered by Unimod, PSI-MOD, XL-MOD, or Glycan Naming Ontology—parser will fail or return unrecognized modification errors.
- Fragment annotation is not needed (e.g., if the task is only to calculate precursor m/z or report modification composition)—skip to direct mass lookup.

## Inputs

- ProForma 2.0 peptidoform string (e.g., 'DLTDYLM[Oxidation]K')
- Peptide sequence (20–100 amino acids typical)
- Modification vocabulary source (Unimod ID or PSI-MOD accession)
- Fragment tolerance parameters (mass value, 'Da' or 'ppm' mode)

## Outputs

- Parsed peptide sequence (unmodified backbone)
- Modification site map (position → modification name and mass shift)
- Theoretical fragment m/z values (b and y ions with charge states)
- Annotated spectrum peaks (peak m/z, assigned ion type, charge, mass error)

## How to apply

Call spectrum_utils.proforma to parse the ProForma 2.0 string, which extracts the sequence and maps modification positions using controlled vocabularies (Unimod, PSI-MOD, XL-MOD, or Glycan Naming Ontology). The parser resolves bracketed modification syntax (e.g., '[Oxidation]', '[Phospho]') to standard CV terms. Pass the parsed peptidoform to MsmsSpectrum.annotate_proforma() along with fragment tolerance parameters (fragment_tol_mass, fragment_tol_mode) and desired ion types (e.g., 'by' for b and y ions) to compute theoretical m/z values. Validate that all modifications are recognized by the selected CV and that charge states are handled correctly during ion calculation.

## Related tools

- **spectrum_utils** (Core library providing spectrum_utils.proforma parser and MsmsSpectrum.annotate_proforma() method for ProForma 2.0 parsing and fragment annotation) — https://github.com/bittremieux/spectrum_utils
- **Unimod** (Controlled vocabulary for post-translational modifications; referenced by ProForma parser to resolve modification IDs and mass shifts) — https://www.unimod.org/
- **PSI-MOD** (Alternative controlled vocabulary for protein modifications; supported by spectrum_utils parser for modification term lookup) — https://github.com/HUPO-PSI/psi-mod-CV/
- **XL-MOD** (Controlled vocabulary for cross-linking modifications; supported by ProForma parser for cross-linked peptidoform notation)
- **Glycan Naming Ontology** (Controlled vocabulary for glycan modifications; supported by ProForma parser for glycosylated peptidoform notation) — https://gnome.glyomics.org/
- **Python** (Programming language in which spectrum_utils and ProForma parsing are implemented)

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372')
spectrum.annotate_proforma('DLTDYLM[Oxidation]K', fragment_tol_mass=0.05, fragment_tol_mode='Da', ion_types='by')
```

## Evaluation signals

- All modification brackets in input string are successfully resolved to valid CV terms (Unimod ID or PSI-MOD accession); no 'unrecognized modification' errors are raised.
- Parsed sequence matches input string after removal of brackets and modification annotations (e.g., 'DLTDYLM[Oxidation]K' → sequence 'DLTDYLMK').
- Modification position map correctly maps each modification to its 1-indexed amino acid position; mass shifts match CV values (e.g., Oxidation = +15.9949 Da).
- Annotated spectrum peaks show mass errors within the specified fragment tolerance (e.g., ±0.05 Da or ±10 ppm) for matched b and y ions.
- Ion charge states are consistent with precursor charge and fragment mass range (e.g., singly and doubly charged ions present in m/z 100–1400 window).

## Limitations

- Parser requires exact Unimod or PSI-MOD terminology; typos or non-standard abbreviations (e.g., 'Ox' instead of 'Oxidation') will cause parse failure.
- ProForma 2.0 syntax supports a limited set of modification notations; complex or ambiguous modifications (e.g., isobaric variants with identical mass) may not disambiguate correctly without additional context.
- Fragment annotation depends on accurate fragment tolerance parameters; too-loose tolerances (e.g., >100 ppm) will cause false-positive peak assignments; too-strict tolerances will miss valid ions due to calibration drift or instrument resolution limits.
- Glycosylated and cross-linked peptidoforms introduce additional complexity in theoretical m/z calculation; validation against public spectra is essential to ensure correctness.

## Evidence

- [intro] fragment_annotation_proforma: "fragment ions can be annotated based on the ProForma 2.0 specification"
- [other] proforma_parsing_step: "Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions."
- [other] annotate_proforma_method: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the"
- [other] modification_vocabularies: "Modifications are defined by controlled vocabularies (CVs), including Unimod, PSI-MOD"
- [other] cv_support_crosslink_glycan: "support for modifications from cross-linking (using XL-MOD) ... glycans (using the Glycan Naming Ontology)"
