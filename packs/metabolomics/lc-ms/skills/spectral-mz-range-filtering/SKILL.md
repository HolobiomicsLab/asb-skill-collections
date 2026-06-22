---
name: spectral-mz-range-filtering
description: Use when you have loaded an MsmsSpectrum object from a proteomics or metabolomics dataset and need to focus the analysis window on a specific m/z range relevant to your experiment (e.g., 100–1400 m/z for typical tryptic peptides).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
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

# spectral-mz-range-filtering

## Summary

Restrict mass-to-charge (m/z) range of tandem MS spectra to a defined window to eliminate out-of-range noise and focus analysis on biologically relevant ion signals. This preprocessing step is applied early in the spectrum processing pipeline to improve downstream peak matching and reduce computational overhead.

## When to use

Apply this skill when you have loaded an MsmsSpectrum object from a proteomics or metabolomics dataset and need to focus the analysis window on a specific m/z range relevant to your experiment (e.g., 100–1400 m/z for typical tryptic peptides). Use it before intensity filtering or peak annotation to eliminate spectral artifacts outside your region of interest.

## When NOT to use

- Spectrum has already been m/z-filtered by an upstream process or is already restricted to your target range.
- Your analysis requires full spectral information across all m/z values (e.g., for neutral loss or imager analysis outside standard peptide range).
- Input is not an MsmsSpectrum object but a different spectrum representation (e.g., raw binary mzML data stream).

## Inputs

- MsmsSpectrum object (loaded e.g., via MsmsSpectrum.from_usi())

## Outputs

- MsmsSpectrum object with m/z and intensity arrays restricted to the specified range

## How to apply

Call set_mz_range() on the MsmsSpectrum object with min_mz and max_mz parameters defining your desired window (e.g., min_mz=100, max_mz=1400 for peptide analysis). The method modifies the spectrum's m/z and intensity arrays in place, retaining only peaks whose m/z values fall within [min_mz, max_mz]. Choose your boundaries based on the expected mass range of fragment ions from your analyte class and instrument capabilities. Verify the result by confirming that the returned spectrum's minimum and maximum m/z values respect your specified range, and that no peaks outside this window remain in the m/z array.

## Related tools

- **spectrum_utils** (Provides MsmsSpectrum class and set_mz_range() method for m/z window restriction) — https://github.com/bittremieux/spectrum_utils/

## Examples

```
spectrum = MsmsSpectrum.from_usi('mzspec:MSV000082283:f07074:scan:5475')
spectrum.set_mz_range(min_mz=100, max_mz=1400)
```

## Evaluation signals

- Verify that spectrum.mz.min() >= min_mz and spectrum.mz.max() <= max_mz after filtering.
- Confirm that the length of the intensity array matches the length of the m/z array after filtering.
- Check that no peaks remain outside the [min_mz, max_mz] window in the output spectrum.
- Validate that peaks within the range are preserved with identical m/z and intensity values.
- Ensure the modification preserves the pairing between m/z and intensity arrays (no index misalignment).

## Limitations

- set_mz_range() performs hard cutoff at boundary values; peaks exactly at min_mz or max_mz may be included or excluded depending on implementation detail.
- No interpolation or smoothing is applied; edge effects near boundaries are not mitigated.
- The method does not account for instrument mass calibration drift or systematic m/z offset; pre-calibration is assumed.

## Evidence

- [other] set_mz_range method: "spectrum.set_mz_range(min_mz=100, max_mz=1400)"
- [intro] filter rationale: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] workflow context: "Apply set_mz_range with min_mz=100 and max_mz=1400 to restrict the m/z window."
- [intro] tool description: "spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization."
