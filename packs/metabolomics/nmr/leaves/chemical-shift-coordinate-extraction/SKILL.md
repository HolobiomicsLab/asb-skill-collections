---
name: chemical-shift-coordinate-extraction
description: Use when you have loaded an INADEQUATE NMR spectrum file and need to
  detect individual peaks (local maxima) across the chemical shift dimension with
  associated intensity values. This is the mandatory first processing step before
  filtering peaks into networks or matching against metabolite databases.
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
  license_tier: open
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-shift-coordinate-extraction

## Summary

Extract chemical shift coordinates and intensity values from INADEQUATE NMR spectra using automated peak-picking to identify local maxima and intensity thresholds. This skill produces a structured list of peaks that serves as input for downstream network clustering and metabolite identification.

## When to use

Apply this skill when you have loaded an INADEQUATE NMR spectrum file and need to detect individual peaks (local maxima) across the chemical shift dimension with associated intensity values. This is the mandatory first processing step before filtering peaks into networks or matching against metabolite databases.

## When NOT to use

- Input spectrum is already pre-processed into a peak list or feature table — use direct clustering instead.
- Spectrum quality is too poor (very low signal-to-noise ratio or heavily distorted baseline) — peak-picking will produce high false-positive rates.
- The analysis goal is only to visualize the raw spectrum without quantification — raw plotting is simpler.

## Inputs

- INADEQUATE NMR spectrum file (loaded via PyINETA input reader)
- Referencing parameters (baseline shift values for chemical shift correction)

## Outputs

- Structured list of detected peaks
- Peak table containing chemical shift coordinates and intensity values
- Peak coordinates in chemical shift space (ppm or Hz) with intensities

## How to apply

Load the INADEQUATE NMR spectrum file using PyINETA's input reader, then apply the peak-picking algorithm via the pyineta.picking module to detect local maxima across the spectrum using intensity thresholds. The algorithm scans the spectrum and identifies peaks by their chemical shift position and intensity. Apply basic shifting-based referencing if needed to normalize the chemical shift scale. Output the detected peaks as a structured list or table containing chemical shift coordinates (in ppm or Hz) and corresponding intensity values. The quality of peak-picking depends on threshold tuning and the signal-to-noise ratio of the input spectrum.

## Related tools

- **PyINETA** (Python package providing the peak-picking algorithm via pyineta.picking module; reads INADEQUATE spectra and applies intensity threshold detection) — https://github.com/edisonomics/PyINETA
- **Python** (Execution language for PyINETA and the peak-picking workflow)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s pick -o output_dir
```

## Evaluation signals

- Output peak table is non-empty and contains numerical chemical shift coordinates in expected range (typically 0–200 ppm for INADEQUATE) and positive intensity values.
- Number of detected peaks is consistent with visual inspection of the spectrum and known compound complexity.
- Peak coordinates are stable across small variations in referencing offset (chemical shifts should change smoothly, not jump discontinuously).
- Intensity values span a reasonable dynamic range and are proportional to visual peak heights in the spectrum.
- Output conforms to the structured list/table schema expected by downstream pyineta.clustering and pyineta.finding modules.

## Limitations

- Peak-picking relies on intensity thresholds; setting thresholds too low produces false positives (noise peaks), too high misses weak signals.
- Basic shifting referencing may not account for complex referencing issues (e.g., field inhomogeneity, second-order effects); mis-referencing can shift peaks out of tolerance for downstream database matching.
- Overlapping peaks in the same region may be detected as a single peak or produce multiple artificial peaks depending on peak width and threshold.
- Algorithm performance depends on spectrum quality; poor baseline correction, phase distortions, or artifacts can lead to missed or spurious peaks.

## Evidence

- [other] The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output.: "The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output."
- [readme] PyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking.: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [other] Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum.: "Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum."
- [other] Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values.: "Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values."
