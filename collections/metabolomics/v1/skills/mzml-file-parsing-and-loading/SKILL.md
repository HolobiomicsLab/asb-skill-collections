---
name: mzml-file-parsing-and-loading
description: Use when when you have real LC-MS/MS experimental data in mzML format (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - OpenMS
  - VIMMS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
schema_version: 0.2.0
---

# mzml-file-parsing-and-loading

## Summary

Parse and load mzML mass spectrometry data files to extract metabolite information, retention times, m/z values, and fragmentation spectra for use in MS/MS acquisition simulation and comparison workflows. This skill bridges real experimental data and virtual metabolomics simulation environments.

## When to use

When you have real LC-MS/MS experimental data in mzML format (e.g., from a beer or urine sample acquisition) and need to extract chemical identities, retention times, precursor m/z values, and MS/MS fragmentation patterns to either (1) populate a virtual mass spectrometer for simulation, or (2) compare simulated fragmentation coverage against the original experimental acquisition.

## When NOT to use

- Input mzML file is already preprocessed or has had peaks removed — ChemicalMixtureFromMZML extracts from raw scans, so prior filtering may reduce chemical recovery.
- You only need to simulate a new fragmentation strategy on a synthetic chemical list (not empirical data) — use DatabaseFormulaSampler or ChemicalMixtureCreator instead.
- The mzML file is from a targeted or selected-reaction-monitoring (SRM) acquisition rather than full-scan data-dependent acquisition — extraction will recover only the monitored m/z values, not the full chemical space.

## Inputs

- mzML file (real LC-MS/MS acquisition data)
- Polarity specification (positive or negative)
- Optional: m/z range constraints (e.g., 100–1000 Da)

## Outputs

- ChemicalMixtureFromMZML object (list of Chemical objects with retention times and m/z)
- IndependentMassSpectrometer instance populated with extracted chemicals
- Parsed peak list (m/z, retention time, intensity tuples)

## How to apply

Use the ViMMS ChemicalMixtureFromMZML class to read an mzML file and automatically extract a list of chemical objects containing retention time and m/z information from the real acquisition. This extraction preserves the empirical chromatographic and mass spectral characteristics. Then instantiate an IndependentMassSpectrometer with the extracted chemicals in the appropriate polarity mode (positive or negative). Finally, run the Environment with your chosen fragmentation controller (e.g., TopNController with N=5, isolation_width=1) to simulate acquisition on the same chemical mixture, yielding mzML output that can be directly compared to the original file using peak picking and intensity matching metrics.

## Related tools

- **VIMMS** (Provides ChemicalMixtureFromMZML class for parsing mzML and instantiating IndependentMassSpectrometer with extracted chemical data) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Performs peak picking and feature detection on mzML files to support fragmentation coverage comparison)
- **Python** (Runtime for executing mzML parsing and chemical extraction workflows)

## Examples

```
from vimms.ChemicalMixtureFromMZML import ChemicalMixtureFromMZML; from vimms.MassSpectrometer import IndependentMassSpectrometer; chemicals = ChemicalMixtureFromMZML('beer_1_pos.mzML'); ms = IndependentMassSpectrometer(polarity='positive', chemicals=chemicals)
```

## Evaluation signals

- ChemicalMixtureFromMZML returns a non-empty list of Chemical objects with valid retention times and m/z values matching the input mzML scan data
- IndependentMassSpectrometer is instantiated without errors and can be queried for the number and properties of chemicals
- Extracted m/z values and retention times fall within reasonable ranges (e.g., 100–1000 Da for typical metabolites; retention times match experiment duration)
- Simulated mzML output written from Environment using extracted chemicals shows peaks at the same retention times and similar m/z values as the original experimental mzML
- Peak matching between real and simulated mzML files (using m/z tolerance 1 ppm for MS1, 0.05 ppm for MS2, minimum 3 matching peaks) yields consistent hit rates and intensity correlations

## Limitations

- ChemicalMixtureFromMZML extraction is based on detected peaks in the mzML file; very low-abundance or co-eluting metabolites may be missed or incompletely resolved.
- Extracted retention times are only as accurate as the LC gradient and clock synchronization in the original instrument — retention time drift between real and simulated runs will degrade comparison quality.
- The extraction does not recover molecular formula or chemical identity beyond m/z and retention time; structural annotation requires additional database matching (e.g., HMDB or GNPS).
- mzML parsing performance scales with file size; very large acquisitions (e.g., full metabolomics experiments with thousands of compounds) may require increased memory and runtime.

## Evidence

- [other] Extract unknown chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values.: "Extract chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values"
- [other] Set up an IndependentMassSpectrometer with the extracted chemicals in positive polarity mode.: "Set up an IndependentMassSpectrometer with the extracted chemicals in positive polarity mode"
- [results] Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class: "Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class"
- [other] The `Environment` class provides `write_mzML` to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
- [readme] LC-MS/MS is a prevalent technique for identifying small molecules in untargeted metabolomics: "Liquid-Chromatography (LC) coupled with tandem mass spectrometry (MS/MS) is a prevalent technique for identifying small molecules in untargeted metabolomics"
