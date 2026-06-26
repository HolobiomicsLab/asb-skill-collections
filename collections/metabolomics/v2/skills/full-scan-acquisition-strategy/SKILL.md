---
name: full-scan-acquisition-strategy
description: Use when you need to assess MS1-level ionization efficiency, peak detection
  sensitivity, and chromatographic separation without the overhead of MS/MS fragmentation.
  Use it to benchmark full-scan detection across chemically diverse samples (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - ViMMS
  - DatabaseFormulaSampler
  - ChemicalMixtureCreator
  - IndependentMassSpectrometer
  - FullScanController
  - HMDB
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
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible
  and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive
  and modular framework for the simulation of fragmentation strategies'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# full-scan-acquisition-strategy

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A mass spectrometry acquisition approach that configures a controller to collect MS1 scans only (without tandem MS/MS fragmentation) across a full retention time window, enabling rapid prototyping and evaluation of chemical ionization and detection strategies in a virtual metabolomics environment.

## When to use

Apply this skill when you need to assess MS1-level ionization efficiency, peak detection sensitivity, and chromatographic separation without the overhead of MS/MS fragmentation. Use it to benchmark full-scan detection across chemically diverse samples (e.g., sampled from HMDB within a target m/z range like 100–1000) before committing to tandem acquisition strategies on real instrumentation.

## When NOT to use

- When fragment ion identification is required—full-scan-only strategies do not generate MS/MS spectra needed for metabolite structure elucidation or spectral library matching.
- When the research question targets low-abundance compound detection in complex matrices where tandem MS provides essential selectivity and noise reduction.
- When you have pre-existing MS/MS data that should be evaluated under different acquisition strategies; use data-dependent or data-independent acquisition replays instead.

## Inputs

- Molecular formula list (HMDB database or user-provided)
- m/z range bounds (e.g., min_mz=100, max_mz=1000)
- Retention time range (e.g., min_rt=0, max_rt=1440)
- Ionization polarity specification (positive or negative)

## Outputs

- LC-MS acquisition simulation (scan-level data)
- mzML format mass spectrometry file
- MS1 peak detection results (m/z, retention time, intensity)

## How to apply

Initialize a DatabaseFormulaSampler to retrieve molecular formulas from HMDB within your desired m/z range (e.g., 100–1000), then use ChemicalMixtureCreator with ms_levels=1 to generate a chemical mixture for MS1-only analysis. Instantiate an IndependentMassSpectrometer with your polarity choice (positive or negative) and configure a FullScanController as the fragmentation strategy—this controller acquires MS1 scans only. Create an Environment instance specifying the mass spectrometer, controller, and retention time bounds (e.g., min_rt=0, max_rt=1440 minutes). Execute env.run() to simulate the LC-MS acquisition, then export results to mzML format using Environment.write_mzML(). Peak picking evaluation can then be applied using MZMine parameters to assess detection quality.

## Related tools

- **ViMMS** (Provides the simulation framework, controllers (FullScanController), mass spectrometer model, and environment execution engine for full-scan LC-MS acquisition strategy prototyping) — https://github.com/glasgowcompbio/vimms
- **DatabaseFormulaSampler** (Samples molecular formulas from HMDB database within specified m/z range to generate chemically diverse test compounds) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureCreator** (Generates virtual chemical mixtures with ms_levels=1 configuration for MS1-only simulation) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Instantiates virtual mass spectrometer with specified polarity and isolation window behavior) — https://github.com/glasgowcompbio/vimms
- **FullScanController** (Acquisition strategy controller that configures the mass spectrometer to acquire MS1 scans only) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Source database for sampling realistic molecular formulas in specified m/z and retention time ranges)

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import FullScanController
from vimms.Environment import Environment
chemicals = ChemicalMixtureCreator.from_hmdb(min_mz=100, max_mz=1000, ms_levels=1)
ms = IndependentMassSpectrometer(chemicals, polarity='positive')
env = Environment(ms, FullScanController(), min_rt=0, max_rt=1440)
env.run()
env.write_mzML('output_fullscan.mzML')
```

## Evaluation signals

- Verify that the output mzML file contains only MS1-level scans (no MS2/MS/MS scans); check mzML header and scan level tags.
- Confirm that the number of sampled formulas matches the stated range (e.g., 73,822 unique formulas for m/z 100–1000 from HMDB in the task example).
- Validate that all detected peaks fall within the specified m/z bounds and retention time window (e.g., min_mz=100, max_mz=1000, start_rt=0, stop_rt=1E5).
- Ensure peak intensities meet the minimum intensity threshold for ROI extraction (e.g., at_least_one_point_above=min_ms1_intensity with default 1.75E5).
- Compare simulated MS1 spectra against reference empirical data or benchmarks for realistic peak height and m/z distribution patterns.

## Limitations

- Full-scan-only strategy cannot provide fragment ion data, limiting metabolite identification to molecular weight and retention time matching alone; spectral library matching (e.g., GNPS-NIST14-MATCHES) requires MS/MS data.
- Simulation depends on the fidelity of the IndependentMassSpectrometer model and does not account for all real-world detector nonlinearities, saturation effects, or space-charge phenomena that arise on actual Thermo Orbitrap Fusion Tribrid or similar instruments.
- Chemical sampling from HMDB may not represent the full diversity of endogenous or exogenous metabolites in real samples; targeted validation on empirical beer or biological samples is recommended before instrument deployment.

## Evidence

- [other] full-scan single-sample simulation from sampled HMDB chemicals: "Reproduce the MS1 full-scan single-sample simulation from sampled HMDB chemicals"
- [other] Can a SimpleMs1Controller generate realistic full-scan MS1 spectra when applied to chemically diverse samples created by sampling molecular formulas from the HMDB database?: "Can a SimpleMs1Controller generate realistic full-scan MS1 spectra when applied to chemically diverse samples created by sampling molecular formulas from the HMDB database?"
- [other] DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000: "A DatabaseFormulaSampler successfully sampled 73,822 unique formulas from the HMDB database within the m/z range 100–1000"
- [other] FullScanController as the fragmentation strategy (which acquires MS1 scans only): "Configure FullScanController as the fragmentation strategy (which acquires MS1 scans only)."
- [readme] Virtual Metabolomics Mass Spectrometer (VIMMS), a flexible and modular framework designed to simulate fragmentation strategies: "Virtual Metabolomics Mass Spectrometer (VIMMS), a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
