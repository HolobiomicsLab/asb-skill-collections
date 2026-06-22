---
name: hmdb-metabolite-extraction
description: Use when you have downloaded raw HMDB data (hmdb_metabolites.zip or pickle file) and need to generate a representative set of chemical objects for simulating LC-MS/MS acquisition strategies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - VIMMS
  - vimms-data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# HMDB Metabolite Extraction

## Summary

Extract and filter molecular metabolites from the Human Metabolome Database (HMDB) using ViMMS's database utilities, applying m/z range and intensity constraints to create a curated chemical object library for LC-MS/MS simulation and evaluation.

## When to use

You have downloaded raw HMDB data (hmdb_metabolites.zip or pickle file) and need to generate a representative set of chemical objects for simulating LC-MS/MS acquisition strategies. This skill is essential when you want to test fragmentation strategies against real metabolomic composition rather than synthetic formulae, or when you need to validate database filtering parameters against known compound counts (e.g., confirming 73,822 unique formulas in the m/z 100–1000 range).

## When NOT to use

- You already have a curated list of target compounds with known structures and MS/MS spectra — direct spectral library matching is preferable to database sampling.
- Your workflow requires only synthetic chemical generation (uniform m/z coverage, simple formula distributions) — UniformMZFormulaSampler or equivalent is lighter-weight.
- Input data is not HMDB-format or does not contain metabolite molecular formulae — the extractor assumes specific HMDB schema and column names.

## Inputs

- HMDB database file (hmdb_metabolites.zip or .pickle format)
- m/z range specification (min_mz, max_mz as integers or floats)
- Optional: MS1 intensity threshold (numeric, e.g., 5000 or 1.75E5)
- Optional: polarity specification (positive/negative)

## Outputs

- Filtered set of unique molecular formulae (count and formulae objects)
- Chemical objects suitable for ViMMS Environment simulation
- Count validation report (e.g., 73,822 formulas for m/z 100–1000)

## How to apply

Load the HMDB data using ViMMS's HMDB data-loading utilities (e.g., via pickle or zip extraction from the vimms-data repository). Instantiate a DatabaseFormulaSampler with the loaded HMDB database, specifying m/z range constraints (e.g., min_mz=100, max_mz=1000). Execute the sampler's internal filtering logic to produce the set of unique molecular formulas meeting all criteria. Apply optional secondary intensity thresholds (e.g., min_ms1_intensity=5000 or 1.75E5) if filtering to a specific ionization regime. Count the resulting unique formulas and cross-validate against expected database statistics. Convert the filtered formulae to chemical objects using ChemicalMixtureCreator or equivalent ViMMS class for downstream MS/MS simulation.

## Related tools

- **VIMMS** (Primary framework providing DatabaseFormulaSampler class, HMDB data-loading utilities, ChemicalMixtureCreator, and Environment for MS/MS simulation) — https://github.com/glasgowcompbio/vimms
- **vimms-data** (Repository hosting HMDB database downloads (hmdb_metabolites.zip, hmdb_compounds.p pickle files) and example datasets) — https://github.com/glasgowcompbio/vimms-data
- **Python** (Runtime environment for executing ViMMS HMDB loading and DatabaseFormulaSampler instantiation)

## Examples

```
from vimms.ChemicalCreation import ChemicalMixtureCreator, DatabaseFormulaSampler; sampler = DatabaseFormulaSampler(hmdb_data, min_mz=100, max_mz=1000); cmc = ChemicalMixtureCreator(sampler); chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- Returned unique formula count matches expected HMDB statistics (e.g., 73,822 for m/z 100–1000 range).
- All filtered formulae fall within specified m/z bounds (min_mz ≤ observed m/z ≤ max_mz); no boundary violations.
- If intensity threshold applied, all extracted metabolites meet the specified min_ms1_intensity criterion.
- Chemical objects can be instantiated and passed to ViMMS ChemicalMixtureCreator without schema errors.
- Downstream Environment.run() executes without errors on chemical objects extracted from filtered formulae.

## Limitations

- HMDB database schema must match ViMMS's expected column names and structure; incompatible HMDB versions may require custom loaders.
- Formula filtering is deterministic but may exclude valid metabolites if m/z range or intensity thresholds are too restrictive.
- Count validation (e.g., 73,822) is specific to a particular HMDB release and ViMMS version; future updates to HMDB or the sampler may alter reported counts.
- No changelog or versioning information provided for HMDB data or DatabaseFormulaSampler; reproducibility may require explicit ViMMS version pinning.
- Secondary intensity thresholds (e.g., min_ms1_intensity) filter at the extraction layer but do not account for MS instrument detection limits or ionization efficiency variations.

## Evidence

- [other] Download the HMDB database file (hmdb_metabolites.zip or equivalent pickle file) from the vimms-data repository.: "Download the HMDB database and extract metabolites"
- [results] Load the HMDB data using ViMMS's HMDB data-loading utilities.: "Load the HMDB data using ViMMS's HMDB data-loading utilities"
- [results] Instantiate a DatabaseFormulaSampler with the loaded HMDB database and apply formula-filtering constraints (e.g., m/z range 100–1000).: "DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000)"
- [other] The DatabaseFormulaSampler successfully filters the HMDB database and reports 73,822 unique formulas when applied to chemical formulae in the m/z range 100–1000.: "The DatabaseFormulaSampler successfully filters the HMDB database and reports 73,822 unique formulas when applied to chemical formulae in the m/z range 100–1000"
- [results] Chemical objects are generated by sampling from metabolites in the HMDB database.: "chemical objects are generated by sampling from metabolites in the HMDB database"
- [readme] ViMMS is a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics.: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
