---
name: dda-fragmentation-strategy-parameterization
description: Use when you have a virtual chemical mixture (MS1 peaks) and need to prototype a new DDA acquisition strategy before testing on real instrumentation. Use this skill when you want to compare how different parameter combinations (e.g., TopN=3 vs TopN=5, isolation_width=0.5 Da vs 1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - ViMMS
  - OpenMS
  - IAPI (Thermo Fisher Tribrid/Exactive)
  techniques:
  - LC-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
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

# dda-fragmentation-strategy-parameterization

## Summary

Configure and validate data-dependent acquisition (DDA) fragmentation strategies by setting isolation window, m/z tolerance, retention-time tolerance, intensity thresholds, and fragment count constraints, then execute the parameterized strategy in a virtual mass spectrometry environment to generate MS1/MS2 scan data.

## When to use

You have a virtual chemical mixture (MS1 peaks) and need to prototype a new DDA acquisition strategy before testing on real instrumentation. Use this skill when you want to compare how different parameter combinations (e.g., TopN=3 vs TopN=5, isolation_width=0.5 Da vs 1.0 Da, intensity threshold=5E4 vs 1.75E5) affect scan coverage and fragmentation efficiency in a reproducible simulation.

## When NOT to use

- Input is real LC-MS/MS data already acquired on physical instrumentation—use IAPI or vendor software instead.
- Chemicals are not pre-generated or sampled (e.g., only compound names are available without m/z, intensity, RT)—first apply chemical generation/sampling.
- Target is to optimize parameters using empirical data feedback; use iterative grid search or machine learning models rather than manual single-run parameterization.

## Inputs

- Virtual chemical list (Chemical objects with m/z, intensity, retention time)
- Configured IndependentMassSpectrometer instance (polarity, chemical list)
- Controller configuration parameters (N, isolation_width, m/z tolerance, RT tolerance, intensity threshold)

## Outputs

- mzML file (MS1 and MS2 scans)
- Scans list (in-memory Scan objects)
- Evaluation metrics (fragmentation coverage, spectral matches)

## How to apply

Instantiate a Controller subclass (e.g., TopNController) with discrete parameters: N (number of fragments per survey scan), isolation_width (in Da, typically 0.5–2.0), MS1 m/z tolerance (in ppm, e.g., 10 ppm), retention-time tolerance (in seconds, e.g., 15 s), and minimum MS1 intensity threshold (e.g., 1.75E5 counts). Attach the configured controller to an Environment instance alongside an IndependentMassSpectrometer seeded with virtual chemicals, then invoke env.run() to simulate the acquisition loop. The Environment orchestrates the feedback loop: MS1 scans trigger TopN selection of candidate ions, the controller applies isolation and filtering logic, and MS2 spectra are generated and recorded. Verify non-empty scans list with both MS1 and MS2 records present; export as mzML and evaluate fragmentation coverage using peak-picking and spectral matching (e.g., cosine similarity ≥ 0.7 with reference libraries).

## Related tools

- **ViMMS** (Core simulation framework: instantiates Environment, runs the acquisition loop, applies controller logic, and outputs mzML) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Post-simulation evaluation: processes mzML output to compute fragmentation coverage and peak matching metrics)
- **IAPI (Thermo Fisher Tribrid/Exactive)** (Real hardware integration: deploy validated DDA parameters to physical mass spectrometers (after virtual validation)) — https://github.com/thermofisherlsms/iapi

## Examples

```
from vimms.Common import POSITIVE
from vimms.ChemicalSamplers import UniformMZFormulaSampler, ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import TopNController
from vimms.Environment import Environment

formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
ms = IndependentMassSpectrometer(POSITIVE, chemicals)
controller = TopNController(POSITIVE, N=3, isolation_width=1, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75E5)
env = Environment(ms, controller, min_time=0, max_time=1440)
env.run()
env.write_mzML('output.mzML')
```

## Evaluation signals

- scans list is non-empty and contains both MS1 and MS2 Scan records with correct polarity and m/z ranges
- mzML file is valid and readable; retention times are monotonically increasing; each MS2 scan has a parent_scan_id and isolation window matching configuration
- MS1 intensity filter is correctly applied: all selected ions exceed minimum threshold (e.g., 1.75E5); TopN constraint is honored (≤N MS2 scans per survey cycle)
- Spectral matching against reference libraries (GNPS-NIST14, HMDB) yields cosine similarity ≥ 0.7 and ≥ 3 matching peaks with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm
- Fragmentation coverage (number of unique precursor m/z values with MS2 spectra divided by total MS1 peaks) matches or exceeds baseline for equivalent intensity threshold and TopN setting

## Limitations

- Simulation assumes perfect chromatographic peak shape and constant ionization efficiency; does not model peak broadening, ion suppression, or time-varying detector response.
- Controller logic is deterministic; stochastic variation in precursor selection (e.g., dynamic exclusion jitter, Poisson noise on intensity) is not modeled.
- Real DDA hardware may apply additional gating, multiplexing, or calibration steps not captured by the virtual environment.
- Validation requires reference spectral libraries (HMDB, GNPS-NIST14) and peak-picking parameters (MZMine thresholds); results are sensitive to library coverage and peak-picking accuracy.

## Evidence

- [other] The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a fragmentation strategy Controller: "The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a"
- [other] Configure a TopNController with N=3 fragments per survey scan, 1 Da isolation window, 10 ppm m/z tolerance, 15 s retention-time tolerance, and 1.75E5 minimum MS1 intensity threshold: "Configure a TopNController with N=3 fragments per survey scan, 1 Da isolation window, 10 ppm m/z tolerance, 15 s retention-time tolerance, and 1.75E5 minimum MS1 intensity threshold."
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [other] Filter spectra matching with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks: "Filter spectra matching with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks"
