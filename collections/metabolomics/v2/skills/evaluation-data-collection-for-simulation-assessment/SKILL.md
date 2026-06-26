---
name: evaluation-data-collection-for-simulation-assessment
description: Use when you are developing or comparing new data-dependent acquisition
  (DDA) strategies in ViMMS and need to evaluate how well each strategy fragments
  sampled compounds from the HMDB database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0153
  tools:
  - Python
  - Poetry
  - ViMMS
  - OpenMS
  - MZMine
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# Evaluation-Data Collection for Simulation Assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Enable systematic collection of diagnostic metrics during LC-MS/MS simulation runs to assess the performance of fragmentation acquisition strategies without requiring real instrument hardware. This skill bridges virtual metabolomics simulations and downstream evaluation by capturing scan-level data that can be post-processed to compute fragmentation coverage and strategy efficacy.

## When to use

You are developing or comparing new data-dependent acquisition (DDA) strategies in ViMMS and need to evaluate how well each strategy fragments sampled compounds from the HMDB database. Specifically, when you have instantiated an Environment with a mass spectrometer and controller but need to collect ground-truth or intermediate metrics (e.g., which compounds were actually fragmented, at what isolation windows, with what signal intensity) to later measure fragmentation coverage or match against spectral libraries.

## When NOT to use

- You are analyzing real LC-MS/MS instrument data and need to extract peaks or features; use standard peak-picking tools (MZMine, XCMS) instead — evaluation data collection is for simulation-only assessment.
- Your goal is only to generate synthetic mzML files for format validation; you do not need to measure fragmentation efficacy or compare strategies.
- The simulation is set to MS1-only acquisition (e.g., FullScanController with no fragmentation); there is no MS/MS data to evaluate, making coverage metrics meaningless.

## Inputs

- Environment object (configured with IndependentMassSpectrometer, acquisition controller, min_time, max_time)
- List of KnownChemical objects with retention times, m/z values, and intensities
- Acquisition controller configuration (e.g., FullScanController or TopNController with polarity, isolation width, N value)

## Outputs

- Evaluation metrics dictionary (embedded in Environment state or exported via save_eval flag)
- mzML file with scan-level data ready for post-processing
- Fragmentation coverage statistics (computed downstream via OpenMS or ViMMS evaluation helpers)

## How to apply

When instantiating the Environment object that runs the LC-MS/MS acquisition simulation, set the flag `save_eval=True`. This instructs the Environment to collect diagnostic evaluation data during the `env.run()` execution loop. The collected data includes scan-level metadata: which chemicals were selected for fragmentation, their isolation windows, precursor m/z and intensity, and retention time windows. After simulation completes, the mzML output file (written via `Environment.write_mzML()`) can be post-processed using OpenMS or the evaluation helpers in ViMMS (which rely on MZMine peak-picking parameters) to compute fragmentation coverage metrics. These metrics quantify how many of the known sampled chemicals were successfully targeted and fragmented, allowing you to compare strategies before testing on real instruments.

## Related tools

- **ViMMS** (Core simulation framework; provides Environment class with save_eval flag and write_mzML method for collecting and exporting evaluation data) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Post-processes mzML output from simulation to compute fragmentation coverage metrics)
- **MZMine** (Peak-picking engine underlying ViMMS evaluation helpers; parameters defined in PeakPicking.py)
- **Poetry** (Dependency management for ViMMS development environment) — https://python-poetry.org/

## Examples

```
env = Environment(ms, controller, min_time=0, max_time=1200, save_eval=True)
env.run()
env.write_mzML()
```

## Evaluation signals

- The mzML file contains valid scan-level metadata (retention time, precursor m/z, isolation window, intensity) for all fragmented compounds in the input chemical list.
- Fragmentation coverage metric (proportion of known chemicals successfully selected and fragmented) is non-zero and correlates with the controller's selection strategy (e.g., TopN with N=5 should fragment ≤5 compounds per time window).
- Post-processing the mzML with OpenMS and comparing spectral matches against GNPS-NIST14 library returns consistent matching statistics (matching_ms1_tol=1 ppm, matching_ms2_tol=0.05 ppm, matching_min_match_peaks≥3) across replicate simulations with the same controller and chemical set.
- Evaluation metrics show sensitivity to acquisition parameters: changing isolation width or polarity in the controller visibly alters fragmentation coverage or MS/MS spectrum quality.
- The evaluation data dictionary (if exported separately) contains entries for every compound in the chemical mixture, with no missing or malformed fields (e.g., null retention times, NaN intensities).

## Limitations

- Evaluation data collection in ViMMS simulations assumes ideal instrument behavior; real instruments exhibit peak broadening, detector saturation, and ion suppression effects that are not modeled, so metrics computed on virtual mzML may overestimate coverage compared to real acquisition.
- The quality of fragmentation coverage assessment depends downstream on peak-picking parameters (minimum ROI intensity, minimum ROI length, m/z tolerance thresholds) defined in MZMine configuration; poor parameter choice can artificially inflate or deflate coverage metrics even if the simulation collected complete data.
- Evaluation data collection is not supported for all controller types in ViMMS; custom or experimental controllers may not populate the save_eval metrics correctly, requiring manual inspection of mzML files.

## Evidence

- [other] When running an `Environment` you can enable the `save_eval` flag: "When running an `Environment` you can enable the `save_eval` flag"
- [other] The `Environment` class provides `write_mzML` to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
- [other] Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
- [intro] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [intro] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
