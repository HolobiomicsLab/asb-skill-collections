---
name: spectrum-peak-to-fragment-mapping
description: Use when when you have a tandem mass spectrum (MS/MS) and a ProForma
  2.0 peptidoform string (e.g., DLTDYLM[Oxidation]K) and need to identify which observed
  spectrum peaks correspond to expected b-ion and y-ion fragments, in order to validate
  peptide identification or annotate spectrum quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils
  - Python
  - Unimod
  - ProForma 2.0
  - PSI-MOD
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma)
  specification
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-peak-to-fragment-mapping

## Summary

Map observed mass spectrometry peaks to theoretical fragment ions (b and y ions) for a given peptidoform by matching m/z values within a specified mass tolerance. This enables fragment-level annotation and validation of peptide sequences and their modifications.

## When to use

When you have a tandem mass spectrum (MS/MS) and a ProForma 2.0 peptidoform string (e.g., DLTDYLM[Oxidation]K) and need to identify which observed spectrum peaks correspond to expected b-ion and y-ion fragments, in order to validate peptide identification or annotate spectrum quality.

## When NOT to use

- When the peptide sequence is not known or cannot be reliably inferred from the spectrum.
- When the spectrum is from a non-peptide analyte (e.g., small molecules, metabolites) for which ProForma notation and b/y ion fragmentation do not apply.
- When precursor m/z or charge state is missing or ambiguous, as this is needed to correctly interpret fragment ions.

## Inputs

- ProForma 2.0 peptidoform string (e.g., 'DLTDYLM[Oxidation]K')
- MsmsSpectrum object (observed m/z and intensity pairs)
- Fragment mass tolerance (in Da or ppm)
- Fragment mass tolerance mode (ppm or Da)

## Outputs

- Annotated spectrum with peak assignments (ion type, charge, m/z deviation)
- List of matched fragment ions with their theoretical and observed m/z
- Coverage metrics (number and type of matched ions)

## How to apply

Parse the ProForma 2.0 peptidoform string using spectrum_utils.proforma to extract the sequence and modification positions. Retrieve the spectrum from a public repository (e.g., via Universal Spectrum Identifier) or load it from a local mzML file. Call MsmsSpectrum.annotate_proforma() with the peptide sequence, specifying fragment_tol_mass (e.g., 10 ppm), fragment_tol_mode, and ion_types='by' to compute theoretical b and y ion m/z values. The function matches observed peaks to theoretical m/z within the tolerance window, assigning each matched peak an ion type, charge state, and m/z deviation. Validate annotations by checking that deviations remain within tolerance and that the ion assignments are chemically plausible (e.g., b ions cannot exceed the peptide length).

## Related tools

- **spectrum_utils** (Core library for spectrum loading, ProForma parsing, theoretical fragment m/z calculation, and peak-to-ion matching) — https://github.com/bittremieux/spectrum_utils
- **ProForma 2.0** (Specification standard for encoding peptide sequences and post-translational modifications in peak annotation) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary providing canonical modification definitions and monoisotopic mass shifts used in ProForma parsing) — https://www.unimod.org/
- **PSI-MOD** (Controlled vocabulary for protein modifications, alternative to Unimod for modification definitions) — https://github.com/HUPO-PSI/psi-mod-CV/

## Examples

```
spectrum.annotate_proforma('DLTDYLM[Oxidation]K', fragment_tol_mass=10, fragment_tol_mode='ppm', ion_types='by')
```

## Evaluation signals

- All matched peaks have m/z deviation within the specified fragment_tol_mass threshold (e.g., <10 ppm).
- Ion assignments respect chemical constraints: b-ion mass is strictly less than the full peptide mass; y-ion mass is strictly greater than the mass of the terminal residue.
- The number of matched b and y ions is consistent with peptide length and charge state (longer peptides should yield more potential fragments).
- Matched ion types alternate correctly in m/z space (b ions increase in mass from N-terminus; y ions decrease in mass from C-terminus).
- High-intensity peaks are preferentially matched to theoretical fragments, while low-intensity or noise peaks remain unassigned.

## Limitations

- Annotation accuracy depends on fragment mass tolerance being set appropriately for the instrument and measurement error; too loose a tolerance risks false matches; too strict a tolerance misses true ions.
- ProForma notation requires exact knowledge of modification positions; uncertain or ambiguous PTMs cannot be represented and will produce incorrect fragment masses.
- Complex modifications (e.g., isotopic labeling, cross-links) require extension of the standard ProForma vocabulary (XL-MOD, glycan ontology) which may not be fully supported or readily available.
- The method assumes ideal, complete fragmentation; suppressed or unexpected fragments (e.g., due to sequence context or competing fragmentation pathways) may remain undetected.

## Evidence

- [intro] Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] Call annotate_proforma method with tolerance and ion type specification: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the"
- [other] Validation of matched peaks by ion type and charge: "Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input"
- [other] Fragment ions annotated based on ProForma 2.0 specification: "fragment ions can be annotated based on the [ProForma 2.0](https://www.psidev.info/proforma) specification"
- [other] Use of Unimod modification vocabulary in annotation: "Modifications are defined by controlled vocabularies (CVs), including [Unimod](https://www.unimod.org/)"
