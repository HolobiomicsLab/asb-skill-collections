---
name: nmr-spectrum-peak-detection
description: Use when you have a loaded INADEQUATE NMR spectrum file (after referencing via basic shifting) and need to identify individual peak positions and intensities as input to downstream peak network clustering or metabolite matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyINETA
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.4c03966
  title: PyINETA
evidence_spans:
- pyINETA is a Python package
- python run_pyineta.py <options>
- This is the documentation for the PyINETA package version 2.0.0.
- '.. automodule:: pyineta.finding :members:'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pyineta_cq
    doi: 10.1021/acs.analchem.4c03966
    title: PyINETA
  dedup_kept_from: coll_pyineta_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c03966
  all_source_dois:
  - 10.1021/acs.analchem.4c03966
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# nmr-spectrum-peak-detection

## Summary

Automated detection of local intensity maxima in INADEQUATE NMR spectra to generate a structured list of picked peaks with chemical shift coordinates and intensity values. This is the foundational step in INADEQUATE metabolite identification workflows.

## When to use

Apply this skill when you have a loaded INADEQUATE NMR spectrum file (after referencing via basic shifting) and need to identify individual peak positions and intensities as input to downstream peak network clustering or metabolite matching. Use when the goal is to transition from continuous spectral intensity data to discrete peak coordinates.

## When NOT to use

- Input spectrum has not been loaded or referencing has not been applied — apply referencing first.
- Goal is direct metabolite identification without clustering peaks into networks — peak-picking alone cannot resolve which peaks belong to the same compound.
- Spectrum is dominated by noise or extremely low signal-to-noise ratio — peak detection will produce high false-positive rates.

## Inputs

- INADEQUATE NMR spectrum file (referencing-corrected via basic chemical shift shifting)
- Intensity threshold parameter(s) for local maxima detection
- Chemical shift range or spectral region of interest (optional)

## Outputs

- Structured list or table of picked peaks
- Peak records with chemical shift coordinates (ppm)
- Peak intensity values for each detected maximum

## How to apply

Load the INADEQUATE NMR spectrum file using PyINETA's input reader, then apply the peak-picking algorithm via the pyineta.picking module to detect local maxima across the spectrum intensity landscape. The module scans for peaks that exceed specified intensity thresholds and marks their chemical shift coordinates. Output peaks are structured as a list or table containing both chemical shift coordinates and corresponding intensity values. Success is judged by verifying that detected peaks correspond to actual spectral features (high signal-to-noise ratio) and that no peaks are missed in high-intensity regions.

## Related tools

- **PyINETA** (Primary package containing the pyineta.picking module for automated local maxima detection and intensity-threshold-based peak identification) — https://github.com/edisonomics/PyINETA
- **Python** (Programming language and runtime environment for executing PyINETA peak-picking algorithms)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s pick -o output_dir
```

## Evaluation signals

- All detected peaks have non-zero intensity values and lie within the chemical shift range of the loaded spectrum.
- Picked peaks cluster visually on the original spectrum as local maxima, with no peaks called in low-intensity baseline regions.
- Peak list is reproducible: running the same picking step on the same referencing-corrected spectrum produces identical results.
- Downstream clustering step (pyineta.clustering) successfully groups picked peaks into networks without excessive fragmentation or over-merging.
- Comparison against manual peak annotation (if available) shows sensitivity and specificity consistent with the intensity threshold chosen.

## Limitations

- Peak picking relies on intensity thresholds; setting thresholds too low introduces noise artifacts, while too high may miss weaker legitimate peaks.
- Adjacent peaks that are closer than the spectral resolution cannot be separated; resolution is hardware-dependent and not addressed by the picking step alone.
- Basic chemical shift referencing (via simple shifting) may leave residual referencing errors that alter picked peak coordinates slightly.
- No changelog available in the repository, making it difficult to track changes in peak-picking algorithm behavior across versions.

## Evidence

- [other] The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output.: "The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output."
- [readme] pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [other] Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum.: "Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum."
- [other] Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values.: "Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values."
- [readme] It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
