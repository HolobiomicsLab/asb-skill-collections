---
name: metabolomics-chemical-mixture-generation-from-hmdb
description: Use when you need to create realistic, diverse chemical populations for simulating LC-MS/MS acquisition strategies in a virtual environment. It is essential when you lack real metabolomics data but want to prototype and compare fragmentation strategies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - Poetry
  - VIMMS
  - HMDB
  techniques:
  - LC-MS
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

# metabolomics-chemical-mixture-generation-from-hmdb

## Summary

Generate synthetic chemical mixtures by sampling molecular formulas from the HMDB database within a specified m/z range, then create KnownChemical objects with realistic retention times, intensities, and chromatographic profiles for LC-MS simulation. This skill enables in-silico prototyping of fragmentation strategies before real instrument testing.

## When to use

Use this skill when you need to create realistic, diverse chemical populations for simulating LC-MS/MS acquisition strategies in a virtual environment. It is essential when you lack real metabolomics data but want to prototype and compare fragmentation strategies (e.g., data-dependent acquisition, top-N controllers, or custom acquisition logic) before deployment on real mass spectrometers. Apply it when your goal is to evaluate acquisition performance metrics (e.g., fragmentation coverage, peak detection rate) across known chemical standards.

## When NOT to use

- You already have real experimental LC-MS data and aim to replay or validate acquisition strategies against measured ground truth; use ChemicalMixtureFromMZML instead to extract chemicals directly from mzML files.
- Your goal is to model species-specific or tissue-specific metabolite abundance distributions; HMDB sampling provides only chemical presence/absence, not biological context.
- You need to include custom adducts or non-standard ionization modes not represented in HMDB; the sampler generates [M+H]+ by default in positive polarity.

## Inputs

- HMDB metabolite database (pickle or flat file)
- m/z range specification (min_mz, max_mz in Da)
- number of chemicals to sample (integer N, typically 50–500)
- LC gradient time bounds (min_time, max_time in seconds, e.g., 0–1200 s)

## Outputs

- list of KnownChemical objects with attributes: molecular formula, exact m/z, retention time, MS1 intensity profile, isotope pattern, and chromatographic shape
- metadata table: formula, [M+H]+ m/z, RT, peak intensity, peak width

## How to apply

First, instantiate a DatabaseFormulaSampler (e.g., UniformMZFormulaSampler or DatabaseFormulaSampler) with a desired m/z range, typically 100–1000 Da for untargeted metabolomics. Load the HMDB metabolite database (available from glasgowcompbio/vimms-data). Sample N chemical formulas uniformly (commonly 100–200 compounds) from HMDB using the sampler. For each formula, use ChemicalMixtureCreator with ms_levels=2 to generate KnownChemical objects, which automatically assign retention times (drawn from a uniform or empirical distribution across the LC gradient), realistic MS1 intensities, and isotope patterns. The creator generates synthetic chromatographic profiles (e.g., Gaussian peaks) for each chemical. Store the resulting list of KnownChemical objects as input to the virtual mass spectrometer (IndependentMassSpectrometer). Verify that generated chemicals span the target m/z and retention-time space without clustering or gaps.

## Related tools

- **VIMMS** (Framework providing ChemicalMixtureCreator, DatabaseFormulaSampler, and IndependentMassSpectrometer classes for in-silico chemical generation and LC-MS simulation) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Metabolite database source for sampling chemical formulas and properties (e.g., exact mass, known structures))
- **Python** (Language for executing ChemicalMixtureCreator and sampler classes)
- **Poetry** (Dependency manager for VIMMS installation and reproducible environments) — https://python-poetry.org/

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator, DatabaseFormulaSampler; import pickle; hmdb = pickle.load(open('hmdb_compounds.p', 'rb')); sampler = DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000); cmc = ChemicalMixtureCreator(sampler); chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- Chemical count matches requested sample size N; no duplicate formulas in output list.
- All sampled m/z values fall within [min_mz, max_mz]; median m/z distribution is uniform or matches expected density.
- All retention times lie within [min_time, max_time]; temporal spread is reasonable relative to LC method (e.g., no clustering at start or end).
- Each KnownChemical has non-zero, realistic MS1 intensity (e.g., 1E4–1E8 intensity units); peak shapes are Gaussian or expected chromatographic form.
- When fed to IndependentMassSpectrometer + FullScanController + Environment.run(), the resulting mzML contains scans for all sampled chemicals with expected m/z and retention-time coordinates.

## Limitations

- HMDB sampling reflects only published metabolites; rare or novel compounds will not be represented.
- ChemicalMixtureCreator assigns retention times independently of chemical structure or hydrophobicity; real retention-time predictions require calibration or machine learning.
- Default ionization is [M+H]+ in positive polarity; neutral loss, in-source fragmentation, and adduct heterogeneity are not modeled.
- Intensity profiles are synthetic (e.g., Gaussian peaks); they do not capture real peak shape artifacts, tailing, or signal suppression from coeluting compounds.
- No automatic handling of isomeric ambiguity; multiple HMDB entries with the same m/z may be sampled as distinct chemicals.

## Evidence

- [other] Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms using ChemicalMixtureCreator with ms_levels=2.: "Sample 100 chemical formulas from HMDB database within m/z range 100–1000 using DatabaseFormulaSampler. Generate KnownChemical objects with retention times, intensities, and MS1 chromatograms using"
- [other] They can be sampled from databases such as HMDB: "They can be sampled from databases such as HMDB"
- [other] Generate chemicals using formula samplers: "Generate chemicals using formula samplers"
- [results] chemical objects are generated by sampling from metabolites in the HMDB database: "chemical objects are generated by sampling from metabolites in the HMDB database"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
