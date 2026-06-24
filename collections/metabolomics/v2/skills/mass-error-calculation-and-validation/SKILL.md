---
name: mass-error-calculation-and-validation
description: Use when when annotating observed mass spectrometry peaks against theoretical
  fragment ions (b, y, or other ion types) using ProForma 2.0 peptidoforms, compute
  the m/z deviation for each matched peak to verify that the annotation adheres to
  your specified mass tolerance (e.g., ±10 ppm or ±0.
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
  techniques:
  - LC-MS
  license_tier: restricted
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

# mass-error-calculation-and-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate and validate the mass deviation (Δm/z) between theoretical fragment ion m/z values and observed spectrum peaks to assess annotation accuracy and fragment ion assignment correctness. This skill ensures that annotated ions fall within specified mass tolerance thresholds, a prerequisite for reliable peptidoform identification.

## When to use

When annotating observed mass spectrometry peaks against theoretical fragment ions (b, y, or other ion types) using ProForma 2.0 peptidoforms, compute the m/z deviation for each matched peak to verify that the annotation adheres to your specified mass tolerance (e.g., ±10 ppm or ±0.02 Da) and to quantify annotation reliability. Use this skill after calling annotate_proforma() to validate that each peak's assigned ion type, charge state, and m/z are consistent with experimental precision.

## When NOT to use

- The observed spectrum has not been quality-filtered (e.g., precursor peak and low-intensity noise not removed); preprocessing should precede annotation validation.
- Fragment mass tolerance parameters have not been empirically determined for your instrument and data format; validation will be arbitrary if tolerance is misspecified.
- The peptide string is not in ProForma 2.0 format or contains unrecognized modifications not defined in Unimod or PSI-MOD; annotation will fail or produce nonsensical m/z values.

## Inputs

- ProForma 2.0 peptide string (e.g., 'DLTDYLM[Oxidation]K')
- Observed mass spectrum (MsmsSpectrum object with peak m/z and intensity)
- Theoretical fragment ion m/z values (computed from peptide and modification positions)
- Fragment mass tolerance parameters (fragment_tol_mass and fragment_tol_mode)

## Outputs

- Annotated spectrum peaks with ion type, charge state, and m/z deviation
- List of validated (matched) peaks and their mass errors
- Flag indicators for peaks exceeding mass tolerance
- Summary statistics of mass error distribution (mean, std dev, range)

## How to apply

After generating theoretical b and y ion m/z values for a ProForma 2.0 peptide string using spectrum_utils.fragment_annotation, match each observed spectrum peak to its nearest theoretical m/z within the specified fragment_tol_mass and fragment_tol_mode (e.g., 'Da' or 'ppm'). For each matched peak, compute the absolute and relative mass error: absolute error = |observed_mz - theoretical_mz| and relative error (ppm) = (observed_mz - theoretical_mz) / theoretical_mz × 1e6. Validate that all errors remain within the tolerance threshold; peaks exceeding the tolerance should be flagged as potential misassignments. Iterate through the annotated peaks and inspect the m/z deviation to identify systematic biases (e.g., calibration drift) or outliers that may indicate incorrect ion type or charge assignment.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum class and annotate_proforma() method to compute theoretical fragment ions and match them to observed peaks; enables extraction of m/z deviations for validation.) — https://github.com/bittremieux/spectrum_utils/
- **ProForma 2.0** (Standard notation for encoding peptide sequences and post-translational modifications; spectrum_utils uses ProForma to parse peptide strings and retrieve modification masses from Unimod.) — https://www.psidev.info/proforma
- **Unimod** (Controlled vocabulary of protein modifications with accurate masses; spectrum_utils resolves modification names (e.g., 'Oxidation') to masses for theoretical m/z calculation.) — https://www.unimod.org/

## Examples

```
spectrum.annotate_proforma('DLTDYLM[Oxidation]K', fragment_tol_mass=0.02, fragment_tol_mode='Da', ion_types='by'); [print(f"{peak.ion_type}{peak.charge}: {peak.mz:.4f} (Δ={peak.mz - theoretical_mz:.6f} Da)") for peak in spectrum.annotated_peaks]
```

## Evaluation signals

- All annotated peaks have m/z deviations within the specified fragment_tol_mass and fragment_tol_mode (e.g., |Δm/z| < 0.02 Da or < 10 ppm).
- Mass error distribution is centered near zero with no systematic drift; median and mean deviations should be close and symmetric around zero.
- Ion type, charge state, and m/z deviation are internally consistent (e.g., y^2+ ions have lower m/z than y^1+, and higher-charge ions show proportionally tighter errors).
- Peaks flagged as exceeding tolerance represent <5% of total annotated peaks (unless instrument calibration is poor, in which case recalibration is warranted).
- Comparing mass errors across multiple spectra from the same sample shows reproducible patterns, indicating systematic instrument behavior rather than random noise.

## Limitations

- Mass error calculation assumes accurate fragment_tol_mass and fragment_tol_mode parameters; if these are misspecified, validation will incorrectly accept or reject peaks.
- The method does not account for isotope patterns or in-source fragmentation; peaks from 13C isotopologues or loss species will exhibit larger m/z deviations and may be misassigned.
- Peptides with complex or non-canonical modifications not present in Unimod or PSI-MOD cannot be accurately annotated, leading to spurious m/z deviations.
- No changelog or version history is available for spectrum_utils, making it difficult to track changes in mass error calculation logic across releases.

## Evidence

- [other] compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the specified tolerance: "Call MsmsSpectrum.annotate_proforma(peptide, fragment_tol_mass, fragment_tol_mode, ion_types='by') to compute theoretical b and y ion m/z values and match them to observed spectrum peaks within the"
- [other] each peak's assigned ion_type, charge state, and m/z deviation from theoretical mass are correct and consistent: "Iterate through annotated peaks and validate that each peak's assigned ion_type ('b' or 'y'), charge state, and m/z deviation from theoretical mass are correct and consistent with the input"
- [other] annotate_proforma enables ion type annotation based on ProForma 2.0 specification: "Annotating observed spectrum fragments using the ProForma 2.0 specification for (modified) peptidoforms."
- [other] fragment ions can be annotated based on ProForma 2.0 specification: "fragment ions can be annotated based on the ProForma 2.0 specification"
- [other] Modifications are defined by controlled vocabularies including Unimod: "Modifications are defined by controlled vocabularies (CVs), including Unimod"
