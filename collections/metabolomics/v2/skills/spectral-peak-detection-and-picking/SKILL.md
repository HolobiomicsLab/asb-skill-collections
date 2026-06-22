---
name: spectral-peak-detection-and-picking
description: Use when you have raw INADEQUATE NMR spectra files and need to transition from continuous spectral data to discrete peak coordinates. Use it as the first signal-processing step before clustering peaks into networks or matching against metabolite databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyINETA
  - PyINETA Clustering module
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

# spectral-peak-detection-and-picking

## Summary

Automated detection and extraction of spectral peaks from INADEQUATE NMR spectra using the PyINETA picking module. This is a foundational preprocessing step that identifies individual peak positions and intensities from raw spectra, enabling downstream clustering and metabolite identification.

## When to use

Apply this skill when you have raw INADEQUATE NMR spectra files and need to transition from continuous spectral data to discrete peak coordinates. Use it as the first signal-processing step before clustering peaks into networks or matching against metabolite databases. Essential when working with noisy or complex spectra where manual peak annotation is infeasible.

## When NOT to use

- Input is already a processed peak list or peak network table—skip directly to clustering or matching.
- Spectra have already been baseline-corrected and peak-picked by external NMR software—re-picking may introduce artifacts or duplicate processing.
- You only need to visualize raw spectra without extracting discrete peaks for further analysis.

## Inputs

- Raw INADEQUATE NMR spectra files (referenced via config.ini input path)
- Configuration file (config.ini) with spectra directory and picking parameters
- Spectral data with defined chemical shift axes

## Outputs

- Detected peak coordinates (chemical shift positions in two dimensions)
- Peak intensity values
- Peak network lists (preliminary groupings of codetected peaks)
- Picking visualization figures (if -f yes option enabled)

## How to apply

Invoke the PyINETA picking module via run_pyineta.py with the -s pick or -s pick+ option, specifying a configuration file (config.ini) that contains input spectra paths and picking parameters. The picking module reads and references INADEQUATE spectra using basic shifting to normalize chemical shift references. The algorithm detects individual peaks across the spectral dimensions, outputting peak coordinates (chemical shifts) and intensities. Choose the picking step when starting from raw spectra; use pick+ to automatically run clustering, finding, and matching on the detected peaks. Validate by inspecting the generated peak list and figures to ensure peaks correspond to actual spectral features, not noise.

## Related tools

- **PyINETA** (Python package containing the picking module for automated peak detection from INADEQUATE spectra) — https://github.com/edisonomics/PyINETA
- **PyINETA Clustering module** (Downstream step to group detected peaks by compound identity after picking) — https://github.com/edisonomics/PyINETA

## Examples

```
python run_pyineta.py -c config.ini -o output_dir -s pick -f yes
```

## Evaluation signals

- Peak list is non-empty and contains coordinates within expected chemical shift ranges for INADEQUATE spectra (typically 0–200 ppm for both dimensions).
- Number of detected peaks correlates with spectral complexity; simpler spectra should yield fewer peaks than complex mixture spectra.
- Visualization plots show detected peaks overlaid on or near actual spectral features, confirming peaks are not noise artifacts.
- Peaks can be successfully clustered into networks in the downstream clustering step, indicating peaks are of sufficient quality.
- Matched metabolites in the final output align with expected metabolites in the query sample, validating pick quality indirectly.

## Limitations

- Peak picking uses basic shifting for spectral referencing, which may be insufficient for spectra with severe baseline distortions or poor shimming.
- Algorithm performance depends on picking parameter tuning in config.ini; no automatic optimization is documented.
- Overlapping or closely spaced peaks in high-complexity spectra may be merged into single peaks or missed entirely.
- No changelog is provided in the repository, limiting visibility into algorithm changes or known issues across versions.

## Evidence

- [intro] Peak picking is a foundational step in the PyINETA pipeline: "pyINETA can perform basic tasks such as reading and referencing (using basic shifting) the INADEQUATE spectra and peak picking"
- [methods] Picking module is one of the core pipeline components: "Picking
-------
.. automodule:: pyineta.picking"
- [intro] Picked peaks are filtered downstream to identify networks from the same compound: "It is designed to filter these picked peaks to identify networks of peaks (ideally) coming from the same compound"
- [readme] Concrete invocation showing the picking step: "optional arguments:
  -s STEPS, --steps STEPS
                        Optional: Specify which steps you want to run. Can be
                        one of {all,load,pick,cluster,find,match,plot"
- [intro] Spectral referencing method used in picking: "reading and referencing (using basic shifting) the INADEQUATE spectra"
