---
name: chromatogram-and-ionization-intensity-modeling
description: 'Use when when you need to simulate LC-MS/MS data for fragmentation strategy development and do not have (or wish to augment) real experimental chromatograms. Specifically: (1) you have a list of known or sampled chemical compounds with molecular formulae;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - Poetry
  - OpenMS
  - VIMMS
  - HMDB
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- ViMMS dependencies are managed with [Poetry](https://python-poetry.org/)
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

# chromatogram-and-ionization-intensity-modeling

## Summary

Generate realistic liquid chromatography retention times, peak shapes, and ionization intensities for chemical compounds within a virtual mass spectrometry simulation. This skill enables creation of synthetic LC-MS/MS datasets that mimic empirical acquisition characteristics, supporting fragmentation strategy prototyping before physical instrument testing.

## When to use

When you need to simulate LC-MS/MS data for fragmentation strategy development and do not have (or wish to augment) real experimental chromatograms. Specifically: (1) you have a list of known or sampled chemical compounds with molecular formulae; (2) you wish to assign realistic retention times and intensity profiles that reflect ionization efficiency and peak shape; (3) you plan to feed this synthetic chemical population into a virtual mass spectrometer controller to test Top-N, DDA, or other acquisition strategies. This is essential before running comparisons against real data (e.g., beer or urine mzML).

## When NOT to use

- Input data is already a set of real LC-MS/MS mzML files from which you wish only to extract chemical metadata without modifying chromatograms or intensities.
- You are comparing simulated results against experimental data and have already extracted empirical retention times and ionization profiles from that real data using ChemicalMixtureFromMZML; regenerating synthetic chromatograms would break the alignment.
- Your workflow requires isotope-resolved chromatographic fine structure or in-source fragmentation patterns not supported by the KnownChemical intensity model.

## Inputs

- Formula sampler configuration (UniformMZFormulaSampler or DatabaseFormulaSampler with m/z range)
- Optional: HMDB database or chemical metadata for known compound list
- ms_levels parameter (typically 2 for MS1 + MS/MS)
- Optional: intensity threshold parameters (min_ms1_intensity, min_roi_intensity, min_roi_length)

## Outputs

- List of KnownChemical objects with assigned retention times, MS1 intensities, and chromatographic peak profiles
- Chemical population ready for input to IndependentMassSpectrometer

## How to apply

Instantiate a ChemicalMixtureCreator with a formula sampler (e.g., UniformMZFormulaSampler or DatabaseFormulaSampler configured for the target m/z range, typically 100–1000 for small-molecule metabolomics). Call the creator's sample() method with ms_levels=2 to generate KnownChemical objects that automatically assign retention times, MS1 intensities, and chromatographic peak profiles. Optionally configure intensity thresholds (e.g., min_ms1_intensity = 5000 or 1.75E5) and ROI builder parameters (min_roi_intensity=0, min_roi_length=3) to filter chemically realistic population. Pass the resulting chemical list to IndependentMassSpectrometer; the simulator will use these intensity and retention-time models during the environment.run() loop, generating MS1 and MS/MS scans with profiles that respect the assigned chromatographic shape and ionization behavior.

## Related tools

- **VIMMS** (Framework hosting ChemicalMixtureCreator, KnownChemical, formula samplers, and IndependentMassSpectrometer for simulating LC-MS/MS with modeled chromatograms and ionization intensities.) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Source database from which chemical formulae and metabolite metadata are sampled to initialize the chemical population with realistic m/z distribution.)
- **Python** (Language in which ChemicalMixtureCreator and related ViMMS classes are implemented and invoked.)

## Examples

```
from vimms.ChemicalSamplers import UniformMZFormulaSampler
from vimms.MixtureCreator import ChemicalMixtureCreator
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=1000)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- Verify that the returned KnownChemical list has non-zero length and each object contains a numeric retention_time > 0 and intensity > min_ms1_intensity threshold.
- Check that m/z values of sampled chemicals fall within the specified sampler range (e.g., 100–1000).
- After passing chemicals to IndependentMassSpectrometer and running env.run(), confirm that generated mzML scans contain MS1 peaks at the assigned retention times with intensities matching the KnownChemical profiles (within expected peak shape variability).
- Verify that ROI (region of interest) count and temporal distribution in the output mzML reflect the number of sampled chemicals and their assigned retention times.
- Compare fragmentation coverage (number of precursor ions fragmented in MS/MS) against a known target strategy (e.g., Top-N) to confirm chemicals are being detected and selected at expected intensity thresholds.

## Limitations

- KnownChemical intensity and retention-time models are synthetic and may not capture compound-specific adduct formation, pH-dependent ionization, or time-dependent ion-suppression effects seen in real LC-MS/MS.
- The chromatographic peak shape is uniformly modeled; complex peak splitting, tailing, or fronting due to column interactions is not simulated.
- Assignment of retention times and intensities is independent of actual chemical properties (lipophilicity, functional groups); realistic prediction would require additional QSAR or empirical regression models.
- Isotope patterns and natural abundance fine structure are not modeled within KnownChemical intensity profiles.

## Evidence

- [other] Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. 2. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms using ChemicalMixtureCreator with ms_levels=2.: "Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. 2. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms"
- [other] # 1. Generate chemicals
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2): "formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)"
- [results] Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class: "Extract chemicals from the previously downloaded beer mzML files using `ChemicalMixtureFromMZML` class"
- [results] chemical objects are generated by sampling from metabolites in the HMDB database: "chemical objects are generated by sampling from metabolites in the HMDB database"
- [results] RoiBuilderParams(min_roi_intensity=0, min_roi_length=3): "RoiBuilderParams(min_roi_intensity=0, min_roi_length=3)"
