---
name: ms1-spectrum-simulation
description: Use when when you need to generate synthetic LC-MS/MS data to test fragmentation strategies, validate acquisition controllers, or benchmark peak-picking and spectral matching algorithms before deployment on real mass spectrometers.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - ViMMS
  - DatabaseFormulaSampler
  - ChemicalMixtureCreator
  - IndependentMassSpectrometer
  - FullScanController
  - MZMine
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

# ms1-spectrum-simulation

## Summary

Simulate realistic full-scan MS1 spectra from chemically diverse samples by applying a mass spectrometer controller to a virtual LC-MS environment. This skill enables prototyping and evaluation of MS acquisition strategies without access to real instrumentation.

## When to use

When you need to generate synthetic LC-MS/MS data to test fragmentation strategies, validate acquisition controllers, or benchmark peak-picking and spectral matching algorithms before deployment on real mass spectrometers. Use this skill when you have a defined set of chemical formulas or mixtures and want to see how they ionize and fragment under specified polarity and scan modes.

## When NOT to use

- You already have real LC-MS/MS data and want to replay it with different fragmentation strategies (use replay/re-acquisition workflows instead).
- You need tandem MS/MS fragmentation spectra; this skill generates MS1 only (set ms_levels > 1 and use a tandem controller for MS/MS).
- Your chemical set is very small (< 10 compounds) and you need microsecond-level scan-timing fidelity; virtual simulation trades hardware realism for flexibility.

## Inputs

- Chemical formula list or HMDB database connection
- Polarity specification (positive or negative)
- Retention time range (min_rt, max_rt in minutes)
- m/z range for chemical sampling (e.g., 100–1000)

## Outputs

- mzML format LC-MS/MS data file
- Simulated MS1 scan collection with m/z, intensity, and retention time
- Peak-picked features table (optional, via MZMine integration)

## How to apply

Initialize a DatabaseFormulaSampler to retrieve chemical formulas (e.g., from HMDB within m/z 100–1000); create a ChemicalMixtureCreator with ms_levels=1 to specify MS1-only acquisition. Configure an IndependentMassSpectrometer with your selected polarity (positive or negative) and attach a FullScanController to define the fragmentation strategy. Instantiate an Environment with the mass spectrometer, controller, and retention time range (e.g., min_rt=0, max_rt=1440). Execute env.run() to simulate the full LC-MS acquisition, then export the scans to mzML format using Environment.write_mzML(). Verify the output contains realistic peak intensities and isotope patterns by examining peak-picking results against MZMine parameters.

## Related tools

- **ViMMS** (Core simulation framework providing virtual mass spectrometer, controller, and environment for LC-MS/MS scan-level acquisition prototyping) — https://github.com/glasgowcompbio/vimms
- **DatabaseFormulaSampler** (Retrieves and samples chemical formulas from HMDB or other databases within specified m/z ranges to generate realistic chemical mixtures) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureCreator** (Constructs chemical mixtures and specifies MS levels (MS1 only vs tandem MS/MS) for simulation) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Instantiates a virtual mass spectrometer with specified polarity and ionization parameters) — https://github.com/glasgowcompbio/vimms
- **FullScanController** (Defines the fragmentation strategy and acquisition mode (MS1-only full-scan in this skill)) — https://github.com/glasgowcompbio/vimms
- **MZMine** (Performs peak picking and feature detection on simulated mzML output using defined intensity thresholds and m/z ranges)

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import FullScanController
from vimms.Environment import Environment
from vimms.Sampler import DatabaseFormulaSampler
mix = DatabaseFormulaSampler().sample(100, 1000)
ms = IndependentMassSpectrometer(ms_mode='positive', chemicals=mix.chemicals)
env = Environment(ms, FullScanController(), min_rt=0, max_rt=1440)
env.run()
env.write_mzML('output.mzML')
```

## Evaluation signals

- The output mzML file contains valid scans with non-zero intensity arrays and retention time metadata.
- Peak-picked features match the input chemical set size (73,822 unique formulas → ~73k peaks, allowing for ionization efficiency and dynamic range losses).
- Minimum intensity threshold (at_least_one_point_above=1.75E5) is satisfied for detected ROIs in the output.
- m/z range of detected peaks falls within the specified m/z window (e.g., 100–1000); no peaks outside this window.
- Isotope patterns and relative intensities are realistic (e.g., 13C isotopomer ~1% relative intensity for singly charged ions).

## Limitations

- Simulation assumes independent ionization of chemicals; does not model ion suppression or competitive ionization in complex mixtures.
- Virtual MS1 spectra depend on the underlying chemical database and ionization model; HMDB coverage is limited to known metabolites and does not include novel or modified compounds.
- Retention time prediction uses a simple model (linear or fixed rt per chemical); real LC chromatography is more complex and compound-dependent.
- No simulation of instrument artifacts (e.g., electronic noise, detector saturation, or scan-to-scan jitter) unless explicitly implemented in the IndependentMassSpectrometer.
- Peak matching to spectral libraries (e.g., GNPS-NIST14) requires additional matching threshold filtering (0.0–1.0 cosine similarity) outside this skill.

## Evidence

- [other] A DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000, enabling generation of realistic chemical mixtures for MS1-only simulation.: "DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000"
- [other] Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only). Instantiate IndependentMassSpectrometer with the generated chemicals in positive or negative polarity. Configure FullScanController as the fragmentation strategy.: "Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only). Instantiate IndependentMassSpectrometer with the generated chemicals in positive or negative polarity. Configure"
- [other] Create an Environment instance with the mass spectrometer, controller, and retention time range (e.g., min_rt=0, max_rt=1440). Execute env.run() to simulate the LC-MS acquisition process. Write the resulting scans to mzML format.: "Create an Environment instance with the mass spectrometer, controller, and retention time range (e.g., min_rt=0, max_rt=1440). Execute env.run() to simulate the LC-MS acquisition process. Write the"
- [readme] ViMMS, a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics.: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in PeakPicking.py. Minimum intensity threshold for ROI extraction at_least_one_point_above=min_ms1_intensity with default value 1.75E5.: "The evaluation helpers rely on peak picking using MZMine parameters. at_least_one_point_above=min_ms1_intensity with default value 1.75E5"
