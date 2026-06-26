---
name: mzml-format-output-validation
description: Use when after executing smiter.synthetic_mzml.write_mzml to generate
  synthetic LC-MS/MS runs from nucleoside or peptide fragmentation models.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - SMITER
  - pyQms
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# mzML Format Output Validation

## Summary

Validate that synthetic LC-MS/MS simulation outputs conform to the mzML file format standard, ensuring correct encoding of mass spectrometry data (m/z, intensity, retention time, fragmentation parameters) for downstream computational analysis. This skill is essential when SMITER or similar synthetic spectrum generators produce mzML files that must be compatible with MS data processing pipelines.

## When to use

After executing smiter.synthetic_mzml.write_mzml to generate synthetic LC-MS/MS runs from nucleoside or peptide fragmentation models. Validation is required when the resulting mzML file will be imported into computational mass spectrometry workflows, MS data analysis algorithms, or gold-standard benchmark datasets where file integrity and schema compliance directly affect algorithm performance and reproducibility.

## When NOT to use

- Input is not an mzML file (e.g., raw vendor formats like .raw, .d, or other serialized spectra formats) — use format-specific validators instead.
- Objective is to validate experimental (real) mass spectrometry data quality, not synthetic output — use real MS QA workflows (e.g., MzQC) instead.
- The mzML file has already been validated by the tool that generated it and you are only checking downstream analysis compatibility with a specific algorithm (use algorithm-specific input checkers).

## Inputs

- mzML file (output from smiter.synthetic_mzml.write_mzml)
- Original peak properties dictionary or input CSV (for ground-truth comparison)
- Simulation configuration parameters (gradient_length, fragmentor type, noise model)

## Outputs

- Validation report (pass/fail per mzML structural and semantic checks)
- XML schema compliance status
- Spectrum count and array data integrity summary
- Flagged anomalies (e.g., out-of-range m/z, intensity saturation, missing metadata)

## How to apply

Validate the mzML output file by checking: (1) XML schema compliance and well-formedness using an XML validator; (2) presence and correctness of required mzML elements (spectrum metadata, m/z and intensity arrays, precursor information, fragmentation parameters); (3) consistency between declared array lengths and actual binary-encoded m/z/intensity data; (4) retention time values align with the specified gradient_length parameter from the simulation configuration; (5) mass-to-charge (m/z) values are physically plausible (typically 50–3000 m/z range for LC-MS/MS); (6) intensity values are non-negative and within expected dynamic range. Ground truth validation can compare known input peak properties (from the input CSV converted via csv_to_peak_properties) against reconstructed peaks in the mzML to verify fragmentation model output was correctly serialized.

## Related tools

- **SMITER** (Generates synthetic mzML files from chemical formulas and fragmentation models; output is the target of validation) — https://github.com/LeidelLab/SMITER
- **pyQms** (Supplies isotopic pattern calculations used by SMITER; validates chemical formula-to-spectrum consistency) — https://github.com/pyQms/pyqms

## Examples

```
# After running SMITER simulation:
# python -c "import xml.etree.ElementTree as ET; tree = ET.parse('synthetic_run.mzML'); root = tree.getroot(); spectra = root.findall('.//{http://psi.hupo.org/ms/mzml}spectrum'); print(f'Spectra count: {len(spectra)}'); print(f'First spectrum: {spectra[0].attrib}' if spectra else 'No spectra found')"
```

## Evaluation signals

- mzML file parses without XML schema errors and all required elements (indexedmzML, run, spectrumList, spectrum) are present and non-empty.
- Spectrum count matches expected number of peaks generated from the input CSV via csv_to_peak_properties.
- All m/z and intensity arrays have declared length matching the actual binary-encoded data length (no truncation or padding).
- Retention time values (scanStartTime) monotonically increase and span the range [0, gradient_length] as specified in simulation parameters.
- Ground-truth check: reconstructed precursor m/z and fragment m/z from mzML match the predicted values ±5 ppm (or tool-specific tolerance) from the input peak properties and fragmentation model.
- Intensity values are non-negative, with at least one base peak near 100 % relative abundance per spectrum.

## Limitations

- mzML validation confirms schema compliance but does NOT verify biological plausibility of fragment assignments — chemical accuracy depends on the underlying fragmentation model (NucleosideFragmentor or PeptideFragmentor) and noise injector configuration.
- Validation cannot detect systematic errors in the fragmentation model's mass calculation rules (e.g., incorrect neutral loss masses); ground-truth comparison with external MS databases or manual expert review may be needed.
- Very large mzML files (>10 GB) may require streaming XML validators to avoid memory exhaustion; standard off-the-shelf validators may not scale to multi-hour LC-MS/MS simulations.
- The mzML standard allows vendor-specific extensions and software-specific metadata; validation against the core schema may pass but still lose fidelity when imported into older or incompatible MS software.

## Evidence

- [readme] SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs.: "SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs."
- [other] Run the simulation and write the resulting synthetic LC-MS/MS run to mzML format using smiter.synthetic_mzml.write_mzml, passing the nucleoside fragmentor, noise injector, peak properties, and gradient parameters.: "Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`"
- [readme] It enables the simulation of any biomolecule since all calculations are based on the chemical formulas.: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas."
- [readme] As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] Such gold standards, where the ground truth is known, are required in computational mass spectrometry to test new algorithms and to improve parameters for existing ones.: "Such gold standards, where the ground truth is known, are required in computational mass spectrometry to test new algorithms"
