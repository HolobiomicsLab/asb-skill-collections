---
name: inadequate-spectral-processing
description: Use when you have raw INADEQUATE NMR spectrum files (e.g., in standard
  NMR formats) that require initial processing before metabolite annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
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

# inadequate-spectral-processing

## Summary

This skill encompasses the loading, referencing, and peak-picking of INADEQUATE NMR spectra using PyINETA. It is the foundational step in metabolite identification workflows that prepares raw spectral data for downstream network clustering and database matching.

## When to use

Apply this skill when you have raw INADEQUATE NMR spectrum files (e.g., in standard NMR formats) that require initial processing before metabolite annotation. Use it as the entry point to the pyINETA pipeline when you need to detect and localize peaks across 2D INADEQUATE spectra prior to network filtering and metabolite matching.

## When NOT to use

- Input is already a pre-processed, peak-picked coordinate table — skip directly to clustering or network filtering.
- Spectrum does not contain INADEQUATE data (e.g., 1D ¹H or ¹³C NMR) — use appropriate single-dimension peak-picking tools instead.
- Peaks have already been filtered and clustered into networks — this skill addresses raw spectral input, not network refinement.

## Inputs

- INADEQUATE NMR spectrum file (raw spectral data in standard format)
- Referencing parameters (e.g., chemical shift offset for calibration)

## Outputs

- Picked peaks list (structured table or list with chemical shift coordinates and intensity values)
- Peak intensity matrix or coordinate set suitable for downstream clustering

## How to apply

Load the INADEQUATE NMR spectrum file using PyINETA's input reader module. Apply basic referencing via chemical shift adjustment (shifting) to align the spectrum to a known standard. Then invoke the pyineta.picking module to detect local maxima and apply intensity thresholds across the 2D spectrum to identify candidate peaks. The module outputs a structured list of detected peaks with associated chemical shift coordinates (typically in ppm) and intensity values. These peak coordinates form the input to subsequent network clustering and metabolite matching steps.

## Related tools

- **PyINETA** (Primary package providing spectrum I/O, referencing, and peak-picking modules (pyineta.picking)) — https://github.com/edisonomics/PyINETA
- **Python** (Runtime environment for executing PyINETA pipeline scripts)

## Examples

```
python /path/to/PyINETA/run_pyineta.py -c config.ini -s pick -o output_dir
```

## Evaluation signals

- Peak coordinate list is non-empty and contains valid chemical shift values (typically 0–200 ppm range for INADEQUATE) and positive intensities.
- Peaks are distributed across the expected 2D spectral space with no clustering artifacts at spectrum boundaries or processing boundaries.
- Output can be successfully loaded by downstream pyINETA modules (clustering, network finding) without format or schema errors.
- Peaks correspond to known metabolite signals when visually compared to the original spectrum or reference database.
- No duplicate or near-duplicate peaks (within noise tolerance) appear in the output list.

## Limitations

- Peak-picking uses basic intensity threshold logic and may miss weak or overlapping signals in crowded spectral regions.
- Referencing is performed via basic chemical shift adjustment; no advanced calibration against internal standards is integrated at this stage.
- Peak-picking does not distinguish between true metabolite signals and noise or artifacts — filtering and network-based validation occur in subsequent steps.
- No changelog is available in the repository, limiting visibility into changes to peak-picking algorithm behavior across versions.

## Evidence

- [readme] Load and reference INADEQUATE spectra, then pick peaks: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [other] Peak-picking produces chemical shift and intensity output: "Apply peak-picking algorithm via pyineta.picking module to detect local maxima and intensity thresholds across the spectrum. 3. Output the detected peaks as a structured list or table containing"
- [readme] Peaks are input to downstream network filtering: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [readme] Primary execution via command-line with config file: "python <path_to_pyineta_repo>/run_pyineta.py -c config.ini <other options>"
