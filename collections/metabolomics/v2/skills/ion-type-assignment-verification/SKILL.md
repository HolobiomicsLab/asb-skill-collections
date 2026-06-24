---
name: ion-type-assignment-verification
description: Use when after calling MsmsSpectrum.annotate_proforma() to assign fragment
  ions to a mass spectrum, verify that each annotated peak has the correct ion_type
  ('b' or 'y'), charge state, and m/z deviation from the theoretical mass computed
  for that peptidoform.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Unimod
  - spectrum_utils
  - ProForma 2.0
  - PSI-MOD
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
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

# ion-type-assignment-verification

## Summary

Validate that observed mass spectrum peaks are correctly annotated with their ion types (b, y, or other fragment series), charge states, and theoretical mass deviations when matched against a ProForma 2.0 peptidoform string. This skill ensures the integrity of fragment ion assignments before downstream analysis.

## When to use

After calling MsmsSpectrum.annotate_proforma() to assign fragment ions to a mass spectrum, verify that each annotated peak has the correct ion_type ('b' or 'y'), charge state, and m/z deviation from the theoretical mass computed for that peptidoform. Use this skill to catch annotation errors before proceeding to spectral matching or peptide identification workflows.

## When NOT to use

- Input spectrum has already been manually validated and ion assignments confirmed by expert review in a previous step.
- Peptidoform contains non-standard modifications not defined in Unimod or PSI-MOD controlled vocabularies, preventing accurate theoretical m/z computation.
- Fragment mass tolerance is set so wide (e.g., >500 ppm) that multiple ion types could plausibly match the same peak, making verification ambiguous.

## Inputs

- MsmsSpectrum object with observed peak list (m/z, intensity pairs)
- ProForma 2.0 peptidoform string (e.g., DLTDYLM[Oxidation]K)
- Fragment mass tolerance (Da or ppm)
- Tolerance mode (absolute or relative)

## Outputs

- Validated annotation table with peak m/z, ion_type, charge, theoretical m/z, and mass error
- List of correctly annotated peaks per ion series
- List of unmatched or mis-annotated peaks (if any)
- Summary statistics (number of b ions, y ions, total annotated peaks)

## How to apply

Iterate through the annotated peaks returned by spectrum_utils.MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by'). For each peak, extract its assigned ion_type, charge state, and observed m/z. Compare the observed m/z against the theoretical m/z computed from the ProForma 2.0 peptidoform and verify that the deviation falls within the specified fragment_tol_mass (in Da) or fragment_tol_mode (ppm). Confirm that ion_type assignments follow chemical logic—b ions increase in mass sequentially from the N terminus, y ions from the C terminus—and that no peak is misassigned to a physically impossible ion series for the given peptide length and charge state. Document any peaks that fail these checks as unmatched or incorrectly annotated.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum.annotate_proforma() method to compute theoretical b and y ion m/z values and match them to observed peaks; provides ProForma parser to extract sequence and modification positions.) — https://github.com/bittremieux/spectrum_utils
- **ProForma 2.0** (Standard notation for specifying peptidoforms with modifications; enables unambiguous definition of theoretical fragment ions.) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary of protein modifications used to resolve modification names in ProForma strings and compute accurate mass shifts.) — https://www.unimod.org/
- **PSI-MOD** (Controlled vocabulary providing alternative standardized identifiers for protein modifications.) — https://github.com/HUPO-PSI/psi-mod-CV/

## Examples

```
from spectrum_utils.spectrum import MsmsSpectrum; usi = 'mzspec:MSV000079960:DY_HS_Exp7-Ad1:scan:30372'; spectrum = MsmsSpectrum.from_usi(usi); peptide = 'DLTDYLM[Oxidation]K'; annotated = spectrum.annotate_proforma(peptide, fragment_tol_mass=0.05, fragment_tol_mode='Da', ion_types='by'); [print(f"{peak.mz:.4f} {peak.ion_type} +{peak.charge} error={peak.mz_error:.6f} Da") for peak in annotated if peak.ion_type in ['b', 'y']]
```

## Evaluation signals

- All annotated peaks have an assigned ion_type ('b' or 'y'), charge state (≥1), and m/z value.
- Observed m/z of each annotated peak deviates from its theoretical m/z by ≤ fragment_tol_mass (Da) or fragment_tol_mode (ppm), as specified.
- Ion type assignments respect chemical constraints: b-ion m/z values increase monotonically along the peptide sequence; y-ion m/z values follow expected mass ladder.
- No peak is assigned to a charge state inconsistent with its observed m/z (e.g., charge +3 assigned to a singly-charged ion m/z that would be physically impossible).
- Annotation coverage (number of annotated peaks / total peaks in spectrum) is consistent with prior observations for the given peptide mass and fragmentation method.

## Limitations

- Verification assumes the ProForma 2.0 string and modification definitions in Unimod are correct; errors in the input peptidoform will propagate to theoretical m/z calculations and cause false failures.
- Internal fragment ions, neutral loss products, and non-protease cleavage patterns are not verified by this skill; only canonical b and y ions are annotated by the default ion_types='by' setting.
- High mass accuracy requirements (<5 ppm) may result in false negatives if the mass spectrometer calibration drifts during acquisition.
- Ambiguous assignments (two or more valid ion types within tolerance of the same observed peak) are not flagged as a concern by this skill; a secondary scoring or consensus step may be needed.

## Evidence

- [other] Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the specified tolerance.: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks"
- [other] Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input parameters.: "Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent"
- [other] spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation.: "spectrum_utils provides functionality to annotate observed spectrum fragments using the ProForma 2.0 specification for modified peptidoforms, enabling ion type annotation"
- [other] Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions.: "Parse the ProForma 2.0 peptidoform string (e.g. DLTDYLM[Oxidation]K) using spectrum_utils.proforma to extract the peptide sequence and modification positions"
- [other] Modifications are defined by controlled vocabularies (CVs), including Unimod, PSI-MOD, and support for modifications from cross-linking (using XL-MOD) and glycans (using the Glycan Naming Ontology).: "Modifications are defined by controlled vocabularies (CVs), including Unimod, PSI-MOD"
