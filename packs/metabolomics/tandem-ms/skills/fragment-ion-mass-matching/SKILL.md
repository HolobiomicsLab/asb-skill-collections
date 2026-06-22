---
name: fragment-ion-mass-matching
description: Use when you have a tandem mass spectrum (MSMS) of a known or hypothesized peptide, along with its ProForma 2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - matplotlib
  - Unimod
  - spectrum_utils
  - ProForma 2.0
  - PSI-MOD
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

# fragment-ion-mass-matching

## Summary

Match observed mass spectrometry peaks to theoretical fragment ions (b and y type) of a known peptidoform by computing theoretical m/z values and matching them within a specified mass tolerance. This skill enables ion type annotation and validation of peptide identifications.

## When to use

You have a tandem mass spectrum (MSMS) of a known or hypothesized peptide, along with its ProForma 2.0 peptidoform notation (including any post-translational modifications), and you need to annotate which observed peaks correspond to which fragment ion types (b, y, or other) to validate the peptide sequence and characterize its fragmentation pattern.

## When NOT to use

- The peptidoform notation is ambiguous or not provided; fragment-ion-mass-matching requires exact knowledge of the expected peptide sequence and modifications.
- The fragment mass tolerance is extremely loose (>>10 ppm) or extremely stringent (<<1 ppm), as this will either match nothing or create false assignments.
- The spectrum contains primarily neutral loss or internal fragment ions rather than b and y ions; this skill is designed for standard proteolytic fragmentation patterns.

## Inputs

- Universal Spectrum Identifier (USI) string (e.g., mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372)
- ProForma 2.0 peptidoform notation string (e.g., DLTDYLM[Oxidation]K)
- Fragment mass tolerance (absolute or ppm)
- Fragment tolerance mode (ppm or Da)

## Outputs

- Annotated spectrum object with assigned ion types for matched peaks
- Peak annotations including ion_type, charge state, and m/z deviation
- Validation report of ion assignment correctness

## How to apply

Load the spectrum from an online resource using its Universal Spectrum Identifier (USI) via MsmsSpectrum.from_usi(). Parse the ProForma 2.0 peptidoform string to extract sequence and modification positions. Call the annotate_proforma() method, specifying ion_types='by' to compute theoretical b and y ion m/z values, fragment_tol_mass and fragment_tol_mode parameters (e.g., 10 ppm tolerance), and then iterate through annotated peaks to validate that each peak's assigned ion type, charge state, and m/z deviation from theoretical mass are correct. The matching succeeds when observed peaks fall within the specified mass tolerance window of their theoretical counterparts.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum.from_usi() for spectrum retrieval, annotate_proforma() method for theoretical ion generation and peak matching, and ProForma parsing) — https://github.com/bittremieux/spectrum_utils
- **ProForma 2.0** (Standard notation for representing peptidoforms with post-translational modifications; used to parse and encode input peptide specifications) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary for protein modifications referenced in ProForma strings) — https://www.unimod.org/
- **PSI-MOD** (Complementary controlled vocabulary for protein modifications) — https://github.com/HUPO-PSI/psi-mod-CV/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372')
spectrum.annotate_proforma('DLTDYLM[Oxidation]K', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='by')
for peak in spectrum.annotated_peaks:
    print(f'{peak.mz} -> {peak.ion_type}{peak.ion_number}+{peak.charge}, Δ={peak.mz_deviation:.4f} ppm')
```

## Evaluation signals

- All annotated peaks have assigned ion_type ('b' or 'y') and non-null charge state values.
- For each matched peak, the m/z deviation from theoretical mass is strictly less than the specified fragment tolerance (e.g., |observed_mz - theoretical_mz| < 10 ppm).
- Ion series continuity: consecutive b or y ions are observed in the annotation, without inexplicable gaps (unless explained by neutral losses or low intensity).
- Mass accuracy validation: recompute theoretical m/z values independently and verify that matched ions fall within tolerance; mismatch indicates configuration error.
- Charge state consistency: observed charge states for b and y ions match expected fragmentation patterns (typically +1 for singly charged peptides, may include +2 for larger peptides).

## Limitations

- Fragment-ion-mass-matching requires accurate ProForma 2.0 notation; incomplete or incorrect modification specification will lead to poor ion matching.
- The skill assumes standard protease digestion (trypsin, pepsin, etc.) producing b and y ions; other fragmentation modes (ETD, ECD, neutral loss dominant spectra) may not be well-captured by this workflow.
- No changelog found for spectrum_utils, so compatibility between versions and changes to the annotate_proforma() API are not explicitly documented.
- The USI mechanism depends on availability and stability of online proteomics repositories (GNPS, MassIVE, ProteomeXchange); offline or disconnected environments cannot retrieve spectra via USI.

## Evidence

- [other] Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the specified tolerance.: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the"
- [other] Retrieve the mass spectrum from a public proteomics data repository using its Universal Spectrum Identifier (USI), e.g. mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372.: "Retrieve the mass spectrum from a public proteomics data repository using its Universal Spectrum Identifier (USI), e.g. mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372."
- [other] Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions.: "Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions."
- [other] Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input parameters.: "Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input"
- [intro] spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation.: "spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation."
