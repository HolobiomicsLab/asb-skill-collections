---
name: peptide-modification-representation-and-handling
description: 'Use when when you have an observed MS/MS spectrum and need to annotate fragment peaks against a known modified peptide sequence. Specifically: (1) you possess a peptide amino acid sequence with known or predicted post-translational modifications at specific positions;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3649
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  - PSI-MOD Protein Modifications Ontology
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

# peptide-modification-representation-and-handling

## Summary

Parse and represent post-translational modifications on peptidoforms using the ProForma 2.0 standard, enabling consistent annotation of modified amino acids in mass spectrometry workflows. This skill bridges modification ontologies (PSI-MOD) with peptide sequence specification for fragment ion matching and spectrum annotation.

## When to use

When you have an observed MS/MS spectrum and need to annotate fragment peaks against a known modified peptide sequence. Specifically: (1) you possess a peptide amino acid sequence with known or predicted post-translational modifications at specific positions; (2) you require programmatic parsing of modification notation (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or MOD accessions like 'EM[MOD:00719]EVEES[MOD:00046]PEK'); and (3) you aim to compute theoretical fragment ion m/z values and match them against observed spectrum peaks to validate or discover modification sites.

## When NOT to use

- Input is an unannotated spectrum with no prior knowledge of the peptide sequence or modifications — use a peptide database search or spectral library matching tool instead.
- Modifications are not represented in ProForma 2.0 or PSI-MOD (e.g., custom synthetic labels not in the standard) — manual mapping or conversion is required first.
- Fragment tolerance is not appropriate for the instrument and ionization mode; check instrument specifications before applying a blanket 5 ppm or 0.05 Da rule.

## Inputs

- ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK')
- MsmsSpectrum object (m/z array, intensity array, precursor m/z, charge state, retention time)
- Fragment tolerance (mass value + tolerance mode: 'ppm' or 'Da')
- Ion types specification (string subset of 'abcxyz', default 'by'; 'I' for immonium, 'm' for internal)
- Optional neutral loss dictionary (mapping label to mass delta)

## Outputs

- Annotated MsmsSpectrum object with FragmentAnnotation records
- Matched fragment peaks with ion type, charge, neutral loss label, and isotope state
- Unmatched observed peaks (no theoretical match within tolerance)

## How to apply

Use the spectrum_utils.proforma module to parse a ProForma 2.0 peptidoform string, extracting the amino acid sequence and position-specific modifications (either by common name or PSI-MOD accession). Represent modifications as a dictionary keyed by position and label (e.g., {'2': 'Oxidation', '8': 'Phospho'}). Pass the peptidoform string and modification dictionary to MsmsSpectrum.annotate_proforma() along with fragment ion tolerance parameters (mass value in Da or ppm) and desired ion types ('a', 'b', 'y', 'c', 'z', or combinations). The engine then computes theoretical m/z for each fragment and charge state, applies neutral loss rules (e.g., NH3 –17.026549 Da, H2O –18.010565 Da), and performs tolerance-based matching to observed peaks. Return annotated spectrum with FragmentAnnotation records linking matched peaks to their ion type, charge, modification state, and intensity.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class, proforma parser, and annotate_proforma() method for parsing ProForma 2.0 peptidoforms and matching theoretical fragments to observed peaks.) — https://github.com/bittremieux/spectrum_utils
- **PSI-MOD Protein Modifications Ontology** (Defines standard modification accessions (MOD:XXXXX) and common names for post-translational modifications; used to validate and normalize modification labels in ProForma strings.) — https://github.com/HUPO-PSI/psi-mod-CV
- **Python** (Runtime environment for executing spectrum_utils and custom ProForma parsing scripts.)
- **NumPy** (Optimizes vectorized computation of theoretical m/z values and tolerance-based peak matching.) — https://www.numpy.org/
- **Numba** (Just-in-time compilation of inner loops for efficient fragment m/z calculation and matching.) — http://numba.pydata.org/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; spectrum.annotate_proforma('EM[Oxidation]EVEES[Phospho]PEK', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='by', neutral_losses={'NH3': -17.026549, 'H2O': -18.010565})
```

## Evaluation signals

- Verify that parsed peptidoform correctly extracts unmodified amino acid sequence and maps all position-specific modifications to their ProForma or PSI-MOD labels.
- Check that theoretical fragment m/z values match known references (e.g., online ProForma calculator or published peptide standards with known modifications).
- Confirm that annotated peaks fall within the specified fragment tolerance (ppm or Da) of theoretical m/z and that no peaks outside tolerance are marked as matching.
- Validate that FragmentAnnotation records include consistent ion types (only those requested), appropriate charge states (≤ precursor charge), and valid neutral loss labels (if applicable).
- Inspect unannotated observed peaks to ensure they are peaks that genuinely have no theoretical counterpart within tolerance, or identify systematic mismatches (e.g., unexpected neutral losses or charge state combinations).

## Limitations

- ProForma 2.0 parser may not handle all custom or proprietary modification representations; only standard PSI-MOD terms or common names (e.g., 'Oxidation', 'Phospho') are guaranteed to parse.
- Fragment tolerance parameters (ppm vs. Da) must be chosen appropriate to the instrument; the article does not provide guidance on selecting optimal tolerance for different MS platforms or ionization modes.
- Neutral loss dictionary must be manually specified or inferred; default set includes only common losses (NH3, H2O); specific modifications may require custom neutral loss entries.
- Annotation does not predict or discover novel or unknown modifications — it only matches observed peaks against user-provided theoretical peptidoforms.
- No built-in handling of isotope patterns or singly- vs. multiply-charged fragments beyond charge state enumeration; complex overlaps may require post-processing.

## Evidence

- [other] Parse the ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK') using spectrum_utils.proforma to extract amino acid sequence and position-specific modifications.: "Parse the ProForma 2.0 peptidoform string (e.g., 'EM[Oxidation]EVEES[Phospho]PEK' or 'EM[MOD:00719]EVEES[MOD:00046]PEK') using spectrum_utils.proforma to extract amino acid sequence and"
- [other] Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for immonium, 'm' for internal), and optional neutral losses dictionary (e.g., {'NH3': -17.026549, 'H2O': -18.010565}).: "Call MsmsSpectrum.annotate_proforma() with the peptidoform, fragment tolerance (mass value + mode: 'ppm' or 'Da'), ion types (default 'by'; can include 'abc' or 'xyz' for primary fragments, 'I' for"
- [other] The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum using fragment_annotation module.: "The annotation engine computes theoretical m/z values for all requested fragment ion types and charge states, then performs tolerance-based matching to observed peaks in the spectrum"
- [other] Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity.: "Return the annotated spectrum object with FragmentAnnotation records linked to matching peaks, including ion type, charge, neutral loss label, isotope state, and intensity."
- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms.: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
