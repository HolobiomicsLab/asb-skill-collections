---
name: simulation-evaluation-data-capture
description: Use when when you have simulated DDA (data-dependent acquisition) scans from a ViMMS Environment and need to (1) quantify how well the simulated acquisition matched real or reference data (via evaluation metrics), and (2) export the results as standards-compliant mzML files for comparison with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0157
  tools:
  - ViMMS
  - ChemicalMixtureFromMZML
  - TopNController
  - IndependentMassSpectrometer
  - Environment
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive and modular framework for the simulation of fragmentation strategies'
- Existing mzML files can be converted into chemical lists using `ChemicalMixtureFromMZML`.
- '`TopNController` – standard Top‑N data dependent acquisition.'
- Mass Spectrometer – either an in silico model (`IndependentMassSpectrometer`) or a real instrument.
- Environment – orchestrates interaction between the mass spectrometer and the controller.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms_cq
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms_cq
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

# simulation-evaluation-data-capture

## Summary

Capture evaluation metrics and write simulated MS/MS scans to mzML format during a virtual mass spectrometry acquisition loop. This skill bridges in-silico fragmentation strategy prototyping with downstream comparative analysis by preserving both scan results and performance metadata.

## When to use

When you have simulated DDA (data-dependent acquisition) scans from a ViMMS Environment and need to (1) quantify how well the simulated acquisition matched real or reference data (via evaluation metrics), and (2) export the results as standards-compliant mzML files for comparison with empirical LC-MS/MS data or alternative fragmentation strategies.

## When NOT to use

- Input is only a single chemical spectrum or a static database query—this skill requires a full time-resolved acquisition loop through an Environment.
- No reference or comparison target exists—evaluation metrics are most valuable when contrasted against real or alternative strategy results.
- mzML export is not supported by your ViMMS build or you lack write permissions to the output path.

## Inputs

- Environment object with configured mass spectrometer and controller
- Simulated scan list (generated during env.run())
- Controller fragmentation strategy parameters (N for TopN, isolation window m/z, intensity thresholds)

## Outputs

- mzML file containing simulated MS1 and MS/MS scans
- Evaluation metrics object (scan counts, chemical coverage, intensity statistics)
- Downstream comparison data for strategy validation

## How to apply

During Environment instantiation, set save_eval=True to enable automatic capture of evaluation metrics (e.g., scan count, chemical coverage, intensity distribution statistics) as the acquisition loop runs. After env.run() completes, invoke Environment.write_mzML() to serialize the simulated scan list to mzML format. The evaluation metrics are computed scan-by-scan as the TopNController or other controller makes acquisition decisions, allowing you to assess strategy efficacy (e.g., how many of the top-intensity chemicals were selected, retention time accuracy) without manual post-processing. Export the resulting mzML alongside evaluation summaries to enable blind or side-by-side comparison with reference data, such as real Beer1pos mzML samples.

## Related tools

- **ViMMS** (Framework providing Environment class, scan simulation loop, and write_mzML() method for metric capture and file export) — https://github.com/glasgowcompbio/vimms
- **TopNController** (Fragmentation strategy controller that determines which precursor ions are selected for MS/MS; its decisions are tracked in evaluation metrics) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Virtual mass spectrometer that generates MS1 and MS/MS scans fed into the evaluation loop) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureFromMZML** (Extracts regions of interest (ROIs) from empirical mzML data as UnknownChemical objects for use as input to the virtual spectrometer and evaluation baseline) — https://github.com/glasgowcompbio/vimms

## Examples

```
env = Environment(mass_spectrometer=ms, controller=TopNController(N=10, isolation_width=1.0), retention_time_range=(0, 1E5), save_eval=True); env.run(); env.write_mzML('simulated_dda.mzML')
```

## Evaluation signals

- mzML file is valid and parseable by standard MS data tools (e.g., Proteowizard, mzmine); check file header and scan index integrity.
- Evaluation metrics are non-null and contain reasonable scan counts (>0) and intensity ranges matching the input chemical mixture.
- Number of MS/MS scans generated equals or is less than the TopN parameter × number of MS1 scans, reflecting correct acquisition logic.
- Retention time values in output mzML span the specified acquisition window (start_rt to stop_rt); no scans outside this range.
- Simulated mzML scan statistics (e.g., median precursor m/z, median intensity) are comparable in order of magnitude to the reference Beer1pos data.

## Limitations

- Evaluation metrics depend on correct peak picking via MZMine parameters in PeakPicking.py; suboptimal or mismatched peak detection settings will distort coverage and intensity statistics.
- mzML export does not preserve all ViMMS internal metadata (e.g., controller decision history, intermediate chemical states); downstream tools may need custom parsing for full audit trails.
- Real-time evaluation during env.run() can add computational overhead; very large chemical mixtures (>10,000 compounds) or long RT windows may slow metric collection.
- Evaluation is relative to the input chemical list; if the chemical extraction (via ChemicalMixtureFromMZML) misses low-abundance species or has poor ROI filtering, evaluation metrics may underestimate true strategy performance.

## Evidence

- [methods] Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics.: "Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics."
- [methods] Execute env.run() to simulate the DDA acquisition loop.: "Execute env.run() to simulate the DDA acquisition loop."
- [methods] Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison.: "Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison."
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] You can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files.: "You can evaluate diverse fragmentation strategies using real data, and extract the scan results as mzML files."
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py.: "The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py."
