---
name: mass-spectrometry-fragmentation-modeling
description: Use when you are generating synthetic LC-MS/MS data for method validation,
  algorithm benchmarking, or co-fragmentation analysis, and need to model how specific
  biomolecules (peptides, nucleosides, or other chemical formulas) fragment under
  collision-induced dissociation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SMITER
  - pyQms
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate
  LC-MS/MS runs.
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/genes12030396
  all_source_dois:
  - 10.3390/genes12030396
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-fragmentation-modeling

## Summary

Model MS/MS fragmentation patterns for biomolecules by selecting and configuring a fragmentor object that encodes molecule-specific cleavage rules, then integrating it into synthetic mzML generation to produce realistic tandem mass spectra. This skill enables creation of gold-standard LC-MS/MS datasets where fragmentation behavior is known and reproducible.

## When to use

You are generating synthetic LC-MS/MS data for method validation, algorithm benchmarking, or co-fragmentation analysis, and need to model how specific biomolecules (peptides, nucleosides, or other chemical formulas) fragment under collision-induced dissociation. Use this skill when you require deterministic, repeatable MS/MS spectra with known fragmentation patterns to establish ground truth.

## When NOT to use

- You are analyzing experimental (non-synthetic) LC-MS/MS data—use fragment annotation or database search instead.
- Your biomolecule type is not covered by SMITER's default models (peptides, nucleosides) and you lack the expertise or documentation to implement a custom fragmentor.
- You need real-time or probabilistic fragmentation (e.g., with inherent randomness per acquisition)—SMITER generates deterministic synthetic spectra.

## Inputs

- Peak properties dictionary (mass, intensity, retention time for analytes)
- Fragmentor object (PeptideFragmentor, nucleoside fragmentor, or custom class)
- Noise injector (e.g., UniformNoiseInjector)
- General simulation parameters (gradient_length, instrument settings)

## Outputs

- Synthetic mzML file with MS1 and MS2 spectra
- Fragment ion peak lists with m/z and intensity values
- Fragmentation pattern records for each parent ion

## How to apply

Instantiate a fragmentor object appropriate to your biomolecule class—SMITER provides PeptideFragmentor for peptides and two nucleoside fragmentation models. The fragmentor encodes molecule-specific cleavage rules based on chemical structure. Pass the fragmentor to the write_mzml function along with peak-property definitions (mass, intensity, retention time), a noise model, and simulation parameters (gradient length, instrument configuration). The modular design allows custom fragmentor implementations if default models do not match your analyte chemistry. Verify that the resulting mzML file contains populated MS/MS spectra with fragment ion m/z and intensity values consistent with the chosen fragmentation model's rules.

## Related tools

- **SMITER** (Synthetic mzML writer and modular fragmentation/noise integration engine) — https://github.com/LeidelLab/SMITER
- **pyQms** (Provides highly-accurate isotopic pattern calculations for realistic peak simulation) — https://github.com/pyQms/pyqms

## Examples

```
from smiter import synthetic_mzml, fragmentation_functions, noise_functions
fragmentor = fragmentation_functions.PeptideFragmentor()
noise_injector = noise_functions.UniformNoiseInjector()
synthetic_mzml.write_mzml(peak_properties=peak_dict, noise_injector=noise_injector, fragmentor=fragmentor, gradient_length=30, output_file='synthetic.mzML')
```

## Evaluation signals

- Output mzML file is valid and readable by standard mass spectrometry tools (e.g., contains proper mzML schema structure).
- MS/MS spectra contain fragment ion peaks consistent with the fragmentor's cleavage rules (e.g., peptide b- and y-ions for PeptideFragmentor).
- Fragment m/z values match expected neutral losses and residue compositions for the input sequence/formula.
- Peak intensities scale smoothly across the gradient and respond predictably to the noise model.
- The fragmentation pattern is deterministic and reproducible across multiple runs with identical inputs.

## Limitations

- SMITER's fragmentation models are currently limited to peptides and modified nucleosides; other biomolecule classes require custom fragmentor implementation.
- Fragmentation patterns are rule-based and deterministic; they do not capture stochastic aspects of real MS/MS such as variable branching or instrument-specific bias.
- Peak distributions use standard statistical shapes (Gaussian, gamma, exponentially-modified Gaussian) and may not replicate unusual empirical peak tailing or asymmetry.
- Retention time prediction requires external modules; SMITER itself does not include retention time models in the core library.

## Evidence

- [other] SMITER's write_mzml function integrates peak-property definitions along with selectable noise and fragmentation models: "SMITER's write_mzml function executes the final simulation step by accepting peak-property definitions along with selectable noise and fragmentation models, which are integrated through a modular"
- [other] Instantiate a fragmentor object such as PeptideFragmentor to define fragmentation rules: "Instantiate a fragmentor object (e.g., fragmentation_functions.PeptideFragmentor or nucleoside fragmentation model) to define fragmentation rules."
- [readme] SMITER offers several methods for peptide fragmentation and two models for nucleoside fragmentation by default: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
- [readme] SMITER features a modular design allowing noise and fragmentation models to be easily implemented or adapted: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] Gold-standard datasets enable evaluation of co-elution and co-fragmentation challenges before conducting actual MS experiments: "a comprehensive simulation can identify and thus prevent such difficulties before performing actual MS experiments. SMITER allows to create such datasets easily, fast and efficiently"
