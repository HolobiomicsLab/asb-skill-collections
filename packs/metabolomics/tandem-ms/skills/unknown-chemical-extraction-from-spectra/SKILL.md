---
name: unknown-chemical-extraction-from-spectra
description: Use when when you have an existing real mzML file from a metabolomics LC-MS/MS acquisition (e.g., beer or urine samples) and need to populate a virtual mass spectrometer with the actual chemicals that were measured, so that you can replay the acquisition with alternative fragmentation strategies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - OpenMS
  - VIMMS
  - vimms-data
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
- Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS
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

# unknown-chemical-extraction-from-spectra

## Summary

Extract a list of unknown chemical compounds with retention times and m/z values directly from real LC-MS/MS mzML acquisition data, enabling in silico validation of fragmentation strategies against empirical metabolite populations without prior annotation.

## When to use

When you have an existing real mzML file from a metabolomics LC-MS/MS acquisition (e.g., beer or urine samples) and need to populate a virtual mass spectrometer with the actual chemicals that were measured, so that you can replay the acquisition with alternative fragmentation strategies (e.g., different Top-N parameters) and compare simulated versus original fragmentation coverage.

## When NOT to use

- Input mzML is already peak-picked and de-noised to the point where MS1 feature detection is unreliable or spectrum quality is degraded.
- You aim to simulate acquisition on a completely novel chemical mixture not present in the experimental data; use formula samplers or HMDB database samplers instead.
- The mzML file lacks proper MS1 scan metadata (retention time, m/z calibration) required for accurate chemical reconstruction.

## Inputs

- Real mzML file from LC-MS/MS acquisition (e.g., Beer1pos.mzML)
- Polarity specification (positive or negative ionization mode)

## Outputs

- Chemical mixture object (list of Chemical objects with m/z, retention time, intensity)
- IndependentMassSpectrometer instance seeded with extracted chemicals

## How to apply

Load the real mzML file and use the ViMMS ChemicalMixtureFromMZML class to automatically extract chemical objects (with m/z, retention time, and MS1 intensity information) from the acquired spectra. This creates a chemical list representing the true composition of the sample as observed in the original experiment. The extraction preserves the temporal and intensity profile of each detected chemical, which is essential for accurate simulation replay. The extracted chemicals are then passed to an IndependentMassSpectrometer configured in the same polarity (positive/negative) as the original acquisition. This approach bridges empirical data and simulation by ensuring that the virtual environment operates on the same chemical population as the real instrument, enabling direct comparison of fragmentation outcomes across different controller strategies.

## Related tools

- **VIMMS** (Provides ChemicalMixtureFromMZML class to parse mzML files and extract chemical objects; hosts IndependentMassSpectrometer to host extracted chemicals in simulation environment) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Underlying library used to parse and process mzML files for peak detection and spectrum reading)
- **vimms-data** (Repository hosting example mzML files (Beer1pos, Beer2pos, etc.) used for extraction workflow) — https://github.com/glasgowcompbio/vimms-data

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureFromMZML; chemicals = ChemicalMixtureFromMZML('Beer1pos.mzML').get_chemicals()
```

## Evaluation signals

- Extracted chemical list contains non-empty m/z, retention time, and intensity values for each chemical; no NaN or out-of-range m/z values (e.g., < 50 or > 2000 for typical metabolomics).
- Number of extracted chemicals is consistent with expected sample complexity (e.g., beer sample should yield 50–200+ chemicals); compare against manual inspection or alternative extraction methods.
- Fragmentation coverage metrics (e.g., number of precursor ions matched, MS2 spectrum count) from simulation seeded with extracted chemicals are statistically correlated with original mzML metrics (e.g., Pearson r > 0.7).
- Retention time distribution of extracted chemicals matches the temporal range of the original acquisition (e.g., min_time=0, max_time matches the real experiment).
- Chemical intensity distribution (histogram) extracted from simulation environment is reproducible and stable across independent simulation runs with identical controller parameters.

## Limitations

- Extraction depends on quality of MS1 peak detection and m/z calibration in the original mzML; poor baseline or miscalibration will propagate into extracted chemicals.
- Unknown chemicals are detected and represented by their empirical m/z and retention time, but chemical identity (structure, formula, or annotation) is NOT recovered by extraction; if identity is required, post-hoc library matching (e.g., GNPS) must be performed separately.
- Extraction assumes single ionization state per chemical; multiply-charged ions or adducts are not explicitly resolved and may be treated as distinct chemicals.
- Extraction is applied post-hoc to a fixed mzML snapshot; it does not adapt to or learn from iterative simulations—each extracted chemical list is static for a given input file.

## Evidence

- [other] Extract unknown chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values.: "Extract unknown chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values."
- [results] Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class: "Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies."
- [results] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
