---
name: mzml-format-export-from-simulator
description: Use when after running an Environment simulation in ViMMS that has generated MS1 and/or MS/MS scans from a virtual mass spectrometer and controller pair. Use this skill when you need to preserve the generated scans in a standard format compatible with existing metabolomics software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Poetry
  - VIMMS
  - OpenMS
  - MZmine
  techniques:
  - LC-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzML-format export from simulator

## Summary

Export simulated LC-MS/MS scan data from ViMMS to mzML format for downstream analysis and comparison with real acquisition data. This enables validation of simulated fragmentation strategies and integration with standard metabolomics processing pipelines.

## When to use

After running an Environment simulation in ViMMS that has generated MS1 and/or MS/MS scans from a virtual mass spectrometer and controller pair. Use this skill when you need to preserve the generated scans in a standard format compatible with existing metabolomics software (e.g., OpenMS, MZmine), or when comparing simulated acquisition strategies against real LC-MS/MS data.

## When NOT to use

- If the simulation has not been executed (env.run() has not completed), the Environment will have no scans to export.
- If only evaluation metrics or controller decisions are needed without persistent data storage.
- If the target analysis pipeline requires a different format (e.g., mgf, netCDF) — use format-specific export methods instead.

## Inputs

- Environment object (configured with mass spectrometer, controller, min_time, max_time, save_eval=True)
- Completed simulation state (post env.run())

## Outputs

- mzML file (containing MS1 and MS/MS scans)
- Text-based mass spectrometry data in mzML XML schema

## How to apply

After instantiating an Environment with a mass spectrometer, controller, time bounds, and the save_eval flag enabled, execute env.run() to complete the LC-MS simulation loop. Once the simulation is complete, call Environment.write_mzML() to serialize all generated scans (both MS1 and fragmentation spectra) to an mzML file. The mzML output can then be processed by external tools like OpenMS to compute fragmentation coverage or peak picking metrics. Ensure that the simulation has completed successfully and scans have been accumulated in the Environment's internal data structures before attempting export.

## Related tools

- **VIMMS** (Provides Environment class with write_mzML() method for exporting simulated scans to mzML format.) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Downstream tool for processing mzML output from a simulation to compute fragmentation coverage and validate acquisition strategy performance.)
- **MZmine** (Standard peak-picking and feature detection software compatible with mzML input for post-simulation analysis.)

## Examples

```
from vimms.MassSpec import IndependentMassSpectrometer
from vimms.Controller import FullScanController
from vimms.Environment import Environment
ms = IndependentMassSpectrometer(polarity='positive', chemicals=chemicals)
controller = FullScanController(polarity='positive')
env = Environment(ms, controller, min_time=0, max_time=1200, save_eval=True)
env.run()
env.write_mzML('output_simulation.mzML')
```

## Evaluation signals

- mzML file is generated at the specified output path without errors.
- mzML file is valid XML and conforms to the mzML schema (can be parsed by OpenMS or mzML validators).
- mzML file contains the expected number of scans matching the simulation time interval and controller strategy (e.g., MS1 scans + MS/MS scans for TopN controller).
- mzML scan headers include correct m/z ranges, retention times, intensity arrays, and polarity information from the simulated mass spectrometer.
- External tools (OpenMS, MZmine) can ingest the mzML file without parsing errors and extract chemical features consistent with the input chemical list.

## Limitations

- mzML export requires that save_eval=True was set on the Environment; scans are not retained if this flag is False.
- The write_mzML() method writes to a single output file; multiple simulations or control conditions require separate export calls and file management.
- mzML export does not include all internal ViMMS simulation metadata (e.g., controller state transitions, ROI exclusion decisions); detailed evaluation data may require separate access to evaluation helpers.
- Peak picking in downstream analysis relies on MZMine parameters defined in PeakPicking.py and may vary depending on chemical complexity and intensity ranges in the simulated data.

## Evidence

- [other] The `Environment` class provides `write_mzML` to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
- [other] Create an Environment with the mass spectrometer, controller, min_time=0, max_time=1200, and enable save_eval=True. Execute env.run() to simulate the LC-MS acquisition loop. Write the generated scans to mzML output using Environment.write_mzML().: "Create an Environment with the mass spectrometer, controller, min_time=0, max_time=1200, and enable save_eval=True. Execute env.run() to simulate the LC-MS acquisition loop. Write the generated scans"
- [other] Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
- [other] When running an `Environment` you can enable the `save_eval` flag: "When running an `Environment` you can enable the `save_eval` flag"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
