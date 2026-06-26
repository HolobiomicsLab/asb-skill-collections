---
name: y-ion-signal-detection-and-noise-assessment
description: Use when you have extracted a centroided MS/MS spectrum from a Thermo
  Orbitrap raw file (via rawrr::readSpectrum or equivalent) and need to verify that
  the observed y-ion fragments for a known peptide precursor exhibit signal-to-noise
  ratios consistent with high-quality fragmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3636
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - Spectra
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime,
  in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read
  back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# y-ion signal detection and noise assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detects and validates y-ion fragment signals in centroided tandem MS spectra by comparing peak intensities to local baseline noise, ensuring peptide fragmentation quality meets analytical thresholds. Applied to high-resolution Orbitrap data to verify that observed ion signals are tens to hundreds of times above the noise floor.

## When to use

You have extracted a centroided MS/MS spectrum from a Thermo Orbitrap raw file (via rawrr::readSpectrum or equivalent) and need to verify that the observed y-ion fragments for a known peptide precursor exhibit signal-to-noise ratios consistent with high-quality fragmentation. Use this skill when evaluating spectral quality, validating peptide identification confidence, or assessing whether an LC-MS run meets performance benchmarks for a targeted peptide.

## When NOT to use

- Input spectrum is profile-mode (not centroided); baseline noise estimation and peak matching will be unreliable without centroiding preprocessing.
- Peptide sequence is unknown or ambiguous; theoretical y-fragment m/z calculation depends on accurate sequence annotation.
- Raw file is from a non-Orbitrap or non-high-resolution instrument where baseline noise characteristics differ substantially from Orbitrap noise profiles.

## Inputs

- centroided MS/MS spectrum (m/z and intensity arrays) from rawrr::readSpectrum or equivalent
- peptide sequence (e.g., LGGNEQVTR)
- precursor m/z and charge state
- instrument metadata (resolving power, AGC target, injection time)
- mass tolerance threshold (e.g., 10 ppm)

## Outputs

- identified y-ion peak positions and intensities
- signal-to-noise ratios for each y-ion
- local baseline noise estimates
- spectral quality assessment (pass/fail based on S/N thresholds)
- AGC injection efficiency metric (actual / maximum injection time %)

## How to apply

Extract the m/z and intensity arrays from the centroided spectrum object returned by rawrr::readSpectrum. Calculate theoretical y-fragment m/z values for the peptide sequence (e.g., LGGNEQVTR as doubly charged 487.2567 m/z). Identify observed y-ion signals by matching experimental m/z to theoretical m/z with appropriate tolerance (e.g., 10 ppm for Orbitrap resolving power 30,000 at 200 m/z). For each y-ion peak, measure the signal intensity and estimate local baseline noise from adjacent spectral regions. Calculate the signal-to-noise ratio as peak intensity divided by local noise floor. Verify that all y-ions exceed tens to hundreds counts above the noise level to confirm high spectral quality. Document the AGC injection time (e.g., 2.8 ms of 55 ms maximum) as a metric of ion accumulation efficiency.

## Related tools

- **rawrr** (extracts centroided m/z and intensity arrays from Thermo Orbitrap .raw files via readSpectrum() and provides instrument metadata (resolving power, AGC injection time)) — https://github.com/fgcz/rawrr
- **RawFileReader** (underlying .NET assembly wrapped by rawrr; provides direct access to binary Orbitrap spectral data and instrument parameters) — https://github.com/thermofisherlsms/RawFileReader
- **Spectra** (Bioconductor package that can be used with MsBackendRawFileReader to access raw Orbitrap data via standardized accessor functions) — https://bioconductor.org/packages/Spectra/

## Examples

```
S <- rawrr::readSpectrum(rawfile = '20181113_010_autoQC01.raw', scan = 9594); y_ions <- c(175.119, 288.203, 403.230); observed_mz <- S[[1]]$mz; observed_int <- S[[1]]$intensity; sapply(y_ions, function(y) min(abs(observed_mz - y)) < 0.01)
```

## Evaluation signals

- All identified y-ions have signal intensity ≥ tens to hundreds counts above measured local baseline noise (quantitative S/N assessment).
- Observed y-ion m/z values match theoretical m/z within specified tolerance (e.g., 10 ppm) and fragment ladder is continuous or mostly continuous.
- AGC injection time is ≤ 55 ms maximum for Orbitrap and represents typical efficiency (e.g., ~5% in the example indicates rapid ion accumulation).
- Absence of unexplained gaps in the y-ion series; missing y-ions are rare or attributable to known loss patterns (e.g., loss of ammonia or water).
- Baseline noise floor is stable across the m/z range and does not show artifacts (e.g., electronic noise spikes) that would inflate apparent S/N.

## Limitations

- Noise estimation depends on the definition of 'local baseline'; adjacent spectral regions must be carefully selected to avoid contamination from nearby peaks or spectral artifacts.
- Signal-to-noise assessment assumes centroided data; profile-mode spectra require peak-picking preprocessing and may yield different noise estimates.
- Theoretical y-fragment m/z calculation assumes the peptide sequence is correct and charge state is known; sequence ambiguity or charge miscalculation will cause false negatives.
- Windows systems require decimal symbol configured as '.' for proper rawrr data extraction; misconfiguration will cause data parsing failures.
- The skill does not account for variable ionization efficiency across different y-ion m/z ranges; hydrophobic or highly charged fragments may show anomalously low or high intensities independent of instrumental performance.

## Evidence

- [other] Identify y-ion signals by matching observed m/z values to theoretical y-fragment m/z of the precursor peptide (LGGNEQVTR/2). Calculate signal-to-noise ratio for each y-ion by comparing peak intensity to local baseline noise and verify all y-ions exceed tens to hundreds counts above noise floor.: "Identify y-ion signals by matching observed m/z values to theoretical y-fragment m/z of the precursor peptide (LGGNEQVTR/2). Calculate signal-to-noise ratio for each y-ion by comparing peak intensity"
- [other] all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality.: "all y-ion signals for LGGNEQVTR++ peptide are several tens to hundreds of times above the noise level, demonstrating high spectral quality."
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "invoke compiled `C#` wrapper methods using a system call"
- [results] the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~`r format((2.8/55)*100, digits = 1)`% of the maximum injection time of 55 ms: "the C-trap managed to collect the defined 100,000 charges within 2.8 ms, corresponding to only ~5% of the maximum injection time of 55 ms"
- [methods] The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF: "Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
