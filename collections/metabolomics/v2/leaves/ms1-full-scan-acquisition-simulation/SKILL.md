---
name: ms1-full-scan-acquisition-simulation
description: Use when when you need to prototype, test, or benchmark MS1-only acquisition
  strategies on a defined set of metabolites (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Poetry
  - ViMMS
  - OpenMS
  techniques:
  - LC-MS
  license_tier: restricted
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

# MS1 Full-Scan Acquisition Simulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Simulate full-scan MS1 (parent ion) acquisition on known chemical compounds using ViMMS, generating realistic LC-MS chromatograms and MS1 spectra without fragmentation. This skill enables prototyping and optimization of MS acquisition strategies in a virtual environment before testing on real mass spectrometry hardware.

## When to use

When you need to prototype, test, or benchmark MS1-only acquisition strategies on a defined set of metabolites (e.g., sampled from HMDB) without access to real LC-MS equipment, or when you want to generate synthetic full-scan MS1 data for method validation or comparative studies of fragmentation strategies.

## When NOT to use

- When you need MS/MS fragmentation data — use a TopN or data-dependent controller instead of FullScanController.
- When your input is real measured MS data that you wish to replay or re-acquire — use ChemicalMixtureFromMZML to extract chemicals from an existing mzML, then simulate with a different controller.
- When you require instrument-specific hardware simulation (e.g., Thermo Tribrid tuning parameters) — IAPI provides direct hardware control and is outside the scope of ViMMS simulation.

## Inputs

- List of chemical formulas or KnownChemical objects (with retention times, m/z values, intensities)
- HMDB database or local metabolite list (for sampling)
- Acquisition time bounds (min_time, max_time in seconds)
- Ionization polarity setting (positive or negative)

## Outputs

- mzML file containing full-scan MS1 spectra and chromatograms
- Simulation evaluation data (if save_eval=True) for scan-level metrics

## How to apply

First, sample or define a set of chemical compounds with known m/z values (typically 100–1000 m/z range) using ViMMS DatabaseFormulaSampler or ChemicalMixtureCreator. Create KnownChemical objects with retention times and MS1 intensities. Instantiate an IndependentMassSpectrometer with polarity='positive' (or negative) and supply the chemicals list. Configure a FullScanController (or SimpleMs1Controller) with the same polarity to acquire only MS1 scans, disabling any MS/MS fragmentation. Initialize an Environment object with the spectrometer, controller, and set time bounds (e.g., min_time=0, max_time=1200 seconds). Execute env.run() to simulate the full LC-MS acquisition loop, which generates scan-by-scan MS1 data. Finally, export the acquired scans to mzML format using Environment.write_mzML(), which produces a standards-compliant mzML output file suitable for downstream peak picking and analysis.

## Related tools

- **ViMMS** (Core simulation framework; provides SimpleMs1Controller and FullScanController for MS1-only acquisition, IndependentMassSpectrometer for virtual instrument, Environment for run loop, and write_mzML for output export) — https://github.com/glasgowcompbio/vimms
- **Python** (Programming language for instantiating ViMMS classes and executing simulation workflows)
- **Poetry** (Dependency management tool for installing and configuring ViMMS and its dependencies) — https://python-poetry.org/
- **OpenMS** (Post-simulation peak picking and fragmentation coverage analysis on the exported mzML files)

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import FullScanController
from vimms.Environment import Environment
from vimms.Common import POSITIVE
cmc = ChemicalMixtureCreator(formula_sampler, ms_levels=2)
chemicals = cmc.sample(100)
ms = IndependentMassSpectrometer(polarity=POSITIVE, chemicals=chemicals)
controller = FullScanController(polarity=POSITIVE)
env = Environment(ms, controller, min_time=0, max_time=1200, save_eval=True)
env.run()
env.write_mzML('output.mzML')
```

## Evaluation signals

- mzML file is valid and parseable by standard tools (OpenMS, pymzML) without schema errors
- mzML contains MS1 scans only (no MS2 scans), with m/z and intensity arrays matching the input chemical parameters
- Retention time coverage spans the configured time window (min_time to max_time) with scan-level timestamps monotonically increasing
- Peak picking on the mzML (using MZMine parameters or OpenMS) recovers chemical signals at or near input m/z values and retention times within expected tolerance (typically ≤ 1 ppm for m/z, ≤ 30 s for retention time)
- Comparison of simulation output (number of detected peaks, intensity distribution, chromatographic profile) to input chemical list shows expected overlap and absence of artifactual peaks

## Limitations

- ViMMS simulation assumes idealized peak shapes and does not model instrumental noise, calibration errors, or hardware-specific artifacts that occur on real mass spectrometers.
- The DatabaseFormulaSampler relies on HMDB metabolite coverage; m/z ranges outside 100–1000 and rare metabolites may be underrepresented or absent.
- Full-scan MS1-only simulations do not generate fragment ion (MS/MS) data, so they cannot be used to optimize or validate fragmentation-dependent identification strategies.
- Chromatographic overlap and ion suppression effects are not modeled; all sampled chemicals are assumed to ionize with specified intensity regardless of co-eluting compounds.

## Evidence

- [other] The ViMMS framework includes a SimpleMs1Controller that can generate full-scan MS1 data from simulated chemicals, with the Environment class providing write_mzML functionality to export generated scans as mzML files.: "SimpleMs1Controller that can generate full-scan MS1 data from simulated chemicals, with the Environment class providing write_mzML functionality to export generated scans as mzML files"
- [other] Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms using ChemicalMixtureCreator with ms_levels=2.: "Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms"
- [other] Configure FullScanController with polarity='positive' to acquire only MS1 scans without fragmentation. Create an Environment with the mass spectrometer, controller, min_time=0, max_time=1200, and enable save_eval=True. Execute env.run() to simulate the LC-MS acquisition loop.: "Configure FullScanController with polarity='positive' to acquire only MS1 scans without fragmentation. Create an Environment with the mass spectrometer, controller, min_time=0, max_time=1200"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
