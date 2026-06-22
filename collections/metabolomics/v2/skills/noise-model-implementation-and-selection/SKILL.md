---
name: noise-model-implementation-and-selection
description: Use when when constructing synthetic LC-MS/MS runs in SMITER, you must choose a noise model before calling write_mzml.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SMITER
  - pyQms
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smiter_cq
    doi: 10.3390/genes12030396
    title: SMITER
  dedup_kept_from: coll_smiter_cq
schema_version: 0.2.0
---

# noise-model-implementation-and-selection

## Summary

Select and instantiate a noise model (uniform or intensity-dependent) to inject realistic instrument noise into synthetic LC-MS/MS data during mzML generation. This skill is essential for creating gold-standard datasets where noise characteristics match real MS instrumentation.

## When to use

When constructing synthetic LC-MS/MS runs in SMITER, you must choose a noise model before calling write_mzml. Use this skill if your synthetic dataset needs to reflect realistic m/z and intensity noise patterns that occur in actual mass spectrometry instruments, or if you are comparing algorithm performance across datasets with different noise profiles.

## When NOT to use

- If you need deterministic, noise-free synthetic spectra for algorithm validation that requires ground-truth peak positions; use a zero-noise or pass-through noise model instead.
- If your input data already contains experimental noise from real instrument runs; noise injection is only appropriate for synthetic data generation.
- If you are simulating a specialized instrument with documented, non-standard noise characteristics that neither the default model nor available custom implementations support.

## Inputs

- Noise model class or instance (e.g., UniformNoiseInjector or custom implementation)
- Peak properties dictionary (mass, intensity, retention-time information)
- Fragmentor object (e.g., PeptideFragmentor)
- General simulation parameters (gradient_length, instrument configuration)

## Outputs

- Noise-injected synthetic mzML file
- MS1 and MS2 spectra with realistic m/z and intensity noise

## How to apply

First, decide whether to use the default established noise model or a custom implementation. SMITER offers two primary noise injection strategies: uniform noise (simple, constant magnitude injection) or an intensity-dependent noise model that combines general baseline noise with intensity-specific noise. Instantiate the selected noise generator (e.g., smiter.noise_functions.UniformNoiseInjector) and pass it to write_mzml along with your peak properties, fragmentor, and general simulation parameters. The modular design allows you to implement or adapt noise models if the defaults do not match your experimental conditions. Verify that noise parameters are reasonable for your target instrument by comparing synthetic spectra against published baseline noise levels for that instrument class.

## Related tools

- **SMITER** (Framework providing modular noise injector classes and write_mzml integration for noise application during synthetic mzML generation) — https://github.com/LeidelLab/SMITER
- **pyQms** (Dependency enabling highly-accurate isotopic pattern calculation that informs noise injection on realistic feature shapes) — https://github.com/pyQms/pyqms

## Examples

```
from smiter.noise_functions import UniformNoiseInjector
from smiter.synthetic_mzml import write_mzml
noise_injector = UniformNoiseInjector()
write_mzml(peak_properties, noise_injector, fragmentor, general_params, output_file='synthetic.mzML')
```

## Evaluation signals

- Output mzML file is valid and parseable by standard tools (e.g., mzML schema compliance, no malformed XML).
- Noise statistics in synthetic spectra (baseline m/z and intensity noise distributions) match the chosen noise model parameters within expected tolerance.
- Peak signal-to-noise ratios in synthetic spectra are consistent with the noise injection strategy used (lower SNR for uniform noise, variable SNR for intensity-dependent noise).
- Comparison of synthetic and real spectra from the target instrument class shows similar noise profiles (visual inspection or quantitative metrics like noise floor level, intensity variance).
- The same peak properties + fragmentor with different noise models produce different spectra, confirming noise model is actually being applied.

## Limitations

- The default noise model may not accurately reflect noise characteristics of all MS instruments; custom model development and validation against real data are required for specialized instruments.
- Uniform noise injection assumes constant noise magnitude across all m/z and intensity ranges, which may not capture intensity-dependent or m/z-dependent noise in real instruments.
- Noise model selection and parameterization require prior knowledge of target instrument noise characteristics; poor parameter choices can produce unrealistic synthetic data.
- No changelog is available to track changes in noise model implementations across SMITER versions, potentially affecting reproducibility if model behavior changes silently.

## Evidence

- [other] SMITER's write_mzml function accepts peak properties, noise injector, fragmentor, and general parameters to generate synthetic LC-MS/MS data: "Call smiter.synthetic_mzml.write_mzml with the peak properties, noise injector, fragmentor, and general parameters to execute the simulation and write the output mzML file."
- [abstract] SMITER provides modular noise model design supporting both default and custom implementations: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] Two primary noise injection strategies are available: uniform and intensity-dependent: "m/z-and intensity noise injection ( uniform noise or a noise model that combines general noise with intensity-specific noise)"
- [abstract] Default noise model is established and tested; users can select from it or create custom alternatives: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
- [other] Noise model is one of the three key instantiation steps before simulation: "3. Choose a Noise generator (e.g. smiter.noise_functions.UniformNoiseInjector)"
