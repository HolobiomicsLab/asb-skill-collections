---
name: spectral-intensity-thresholding
description: Use when you have loaded raw INADEQUATE NMR spectrum data and need to distinguish true molecular peaks from noise and instrumental artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2275
  tools:
  - Python
  - PyINETA
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

# spectral-intensity-thresholding

## Summary

Applies intensity-based filtering to INADEQUATE NMR spectra to identify and extract genuine spectral peaks above noise and background levels. This step is essential for reducing false positives and focusing subsequent analysis on meaningful molecular signals.

## When to use

Use this skill when you have loaded raw INADEQUATE NMR spectrum data and need to distinguish true molecular peaks from noise and instrumental artifacts. It is required before peak clustering or network identification, especially when spectra contain variable baseline noise or low-intensity background signals that would otherwise clutter downstream metabolite matching.

## When NOT to use

- Input is already a curated or pre-filtered peak list with intensity filtering already applied.
- Spectrum contains only very weak signals where aggressive thresholding would eliminate all peaks of interest.
- Analysis goal requires preservation of all detected maxima, including low-intensity features, for subsequent statistical ranking rather than binary filtering.

## Inputs

- INADEQUATE NMR spectrum file (raw or processed format supported by PyINETA)
- Intensity threshold parameter (user-configurable cutoff value)

## Outputs

- Filtered peak list (structured list or table)
- Peak coordinates (chemical shift values in ppm)
- Peak intensity values (above-threshold signal magnitudes)

## How to apply

Load the INADEQUATE spectrum using PyINETA's input reader. Apply the peak-picking algorithm via pyineta.picking module to detect local maxima across the spectrum and filter them against an intensity threshold. The threshold value acts as a gate to eliminate peaks below the specified intensity level, retaining only those peaks likely to represent true molecular signals. Peaks passing the threshold are retained in a structured output list with their chemical shift coordinates and intensity values preserved for subsequent clustering and matching steps.

## Related tools

- **PyINETA** (Provides the peak-picking module (pyineta.picking) that detects local maxima and applies intensity thresholding to INADEQUATE spectra) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment and scripting language for executing PyINETA workflows)

## Examples

```
python <path_to_pyineta_repo>/run_pyineta.py -c config.ini -s pick -o output_folder
```

## Evaluation signals

- Output peak list contains only peaks with intensity values above the specified threshold; no peak in output has intensity below cutoff.
- Peak coordinates are expressed in consistent chemical shift units (ppm) and match input spectrum dimensionality.
- Comparison of output peak count and intensity distribution before/after thresholding shows reasonable signal-to-noise improvement (e.g., >50% reduction in spurious peaks for typical NMR noise levels).
- Retained peaks align visually with prominent features in the input spectrum when plotted.
- Downstream clustering step (pyineta.clustering) produces coherent peak networks without fragmenting true molecular signals into disconnected clusters.

## Limitations

- Threshold value is user-configurable and requires empirical optimization; inappropriate threshold may eliminate weak but genuine metabolite signals or retain noise peaks.
- Basic intensity thresholding does not account for spectral baseline drift, phase distortion, or other instrumental artifacts that may affect peak intensity estimation.
- No adaptive or dynamic thresholding based on local noise estimation; same threshold is applied uniformly across the entire spectrum regardless of regional noise variation.

## Evidence

- [other] Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum.: "Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum."
- [other] The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output.: "The peak-picking mechanism reads INADEQUATE spectra, applies referencing via basic shifting, and produces a list of picked peaks as output."
- [readme] pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [other] Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values.: "Output the detected peaks as a structured list or table containing chemical shift coordinates and intensity values."
