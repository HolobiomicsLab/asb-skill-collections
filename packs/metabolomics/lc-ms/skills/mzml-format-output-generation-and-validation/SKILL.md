---
name: mzml-format-output-generation-and-validation
description: Use when after running a ViMMS simulation loop with a fragmentation controller (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Poetry
  - VIMMS
  - OpenMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- ViMMS dependencies are managed with [Poetry](https://python-poetry.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.03990
  all_source_dois:
  - 10.21105/joss.03990
  - 10.1021/acs.analchem.0c03895
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML-Format Output Generation and Validation

## Summary

Export simulated LC-MS/MS scan data from ViMMS to industry-standard mzML format, enabling downstream analysis, archival, and comparative evaluation against real or baseline acquisition strategies. This skill bridges virtual simulation output to standard proteomics/metabolomics workflows.

## When to use

After running a ViMMS simulation loop with a fragmentation controller (e.g., TopNController, WeightedDEWController) to completion, you need to serialize the in-memory scan list to a portable, standards-compliant file format that can be processed by third-party tools (OpenMS, MZmine) or compared against reference acquisitions.

## When NOT to use

- Input scans have not yet been generated (env.run() has not completed) — wait for simulation loop to finish.
- Output format is required by a tool that demands NetCDF or proprietary binary formats (e.g., vendor-specific .raw files) — mzML is text-based and may be slower to parse for very large datasets.
- Evaluation metrics are needed before mzML export — prioritize EvaluationData pickle capture instead, as mzML is primarily for archival and secondary analysis.

## Inputs

- Environment object (instantiated with IndependentMassSpectrometer, controller instance, and save_eval=True)
- In-memory scan list from completed env.run()
- Specification of output file path (out_file) and directory (out_dir)

## Outputs

- mzML file (XML-formatted mass spectrometry data)
- EvaluationData pickle (optional; contains coverage, intensity, and fragmentation statistics)
- Metadata: scan count, retention time range, m/z range, intensity distribution

## How to apply

Within the ViMMS workflow, after instantiating an Environment with a mass spectrometer and controller and calling env.run() to accumulate scans, invoke env.write_mzML() to serialize the complete scan list to mzML format. Set the save_eval=True flag when creating the Environment to enable simultaneous capture of EvaluationData pickles. The output mzML file contains all MS1 and MS/MS spectra in their acquisition order, preserving scan metadata (retention time, m/z, intensity, isolation windows, fragmentation parameters). Validate the mzML output by opening it in peak-picking tools (e.g., OpenMS) or by loading the parallel EvaluationData pickle to cross-check scan counts, intensity ranges (e.g., cumulative intensity thresholds), and fragmentation coverage metrics against baseline controller results.

## Related tools

- **VIMMS** (Core simulation framework; provides Environment class and write_mzML() method to export scan data) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Processes mzML output from simulation to compute fragmentation coverage metrics and validate file integrity)
- **Python** (Language for executing Environment.write_mzML() and post-hoc mzML parsing)

## Examples

```
from vimms.Env import Environment
from vimms.Controller import TopNController
from vimms.MassSpec import IndependentMassSpectrometer

env = Environment(ms, controller, min_time=0, max_time=1440, save_eval=True, out_file='simulation_output.mzML', out_dir='./results')
env.run()
env.write_mzML()
```

## Evaluation signals

- mzML file exists at specified out_file path and is valid XML (parseable by standard XML tools and mzML validators).
- Scan count in mzML header matches the length of the in-memory scan list from env.run().
- EvaluationData pickle cumulative intensity and times_fragmented_summary values are consistent with MS1 and MS/MS peak intensities in the mzML file.
- Retention time, m/z, and isolation window values in mzML scans match the chemical mixture and controller parameters (e.g., isolation_width=1, rt_tol=15).
- mzML file can be successfully imported by downstream tools (OpenMS, MZmine) without parsing errors; peak picking yields expected coverage metrics (e.g., fragmentation rate within ±10% of baseline TopN controller).

## Limitations

- mzML is a verbose, text-based format; exporting very large simulations (>10,000 scans) may incur significant I/O overhead and disk space.
- mzML export does not perform real-time validation; file correctness depends on the integrity of the Environment's scan list. Corrupted or incomplete simulations will propagate to mzML.
- mzML output lacks vendor-specific metadata (e.g., instrument tuning parameters, calibration curves) present in raw binary formats, limiting comparison to real instrument data beyond basic m/z, intensity, and retention time.
- Peak picking for downstream evaluation relies on external tools (OpenMS, MZmine) with their own parameter sensitivity; mzML alone does not guarantee reproducible coverage metrics without consistent peak-picking configuration.

## Evidence

- [other] The Environment class provides write_mzML to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
- [other] When running an Environment you can enable the save_eval flag: "When running an `Environment` you can enable the `save_eval` flag"
- [readme] ViMMS can extract scan results as mzML files: "extract the scan results as mzML files"
- [other] Call env.write_mzML() to serialize the scan list to mzML format: "Call env.write_mzML() to serialize the scan list to mzML format"
- [other] Processes mzML output from a simulation to compute fragmentation coverage: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
