---
name: formula-sampler-configuration
description: Use when you need to generate a set of candidate chemical formulas for LC-MS/MS simulation—specifically when you want to populate a virtual mass spectrometer with realistic chemical structures drawn from a reference database (HMDB) or a uniform m/z distribution, and you need to apply m/z filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - ViMMS
  - HMDB
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

# formula-sampler-configuration

## Summary

Configure and instantiate a formula sampler (e.g., DatabaseFormulaSampler or UniformMZFormulaSampler) to generate a population of chemical formulas within specified m/z bounds for virtual metabolomics simulation. This skill bridges database/distribution selection and chemical population creation in the ViMMS framework.

## When to use

Use this skill when you need to generate a set of candidate chemical formulas for LC-MS/MS simulation—specifically when you want to populate a virtual mass spectrometer with realistic chemical structures drawn from a reference database (HMDB) or a uniform m/z distribution, and you need to apply m/z filtering (e.g., 100–1000 Da range) to match your intended analytical window.

## When NOT to use

- You already have a pre-computed list of chemical formulas or a ChemicalMixture object; skip sampler configuration and pass it directly to the virtual MS.
- Your analysis requires only a small number of hand-curated target compounds rather than a population-level sample from a database.
- The m/z range you need falls entirely outside the bounds of your reference database or is incompatible with the sampler's design.

## Inputs

- HMDB database file (pickle or zipped format, e.g., hmdb_compounds.p or hmdb_metabolites.zip)
- min_mz and max_mz parameters (integers or floats; e.g., 100, 1000)
- Sampler type selection (string: 'UniformMZFormulaSampler' or 'DatabaseFormulaSampler')

## Outputs

- Instantiated formula sampler object (DatabaseFormulaSampler or UniformMZFormulaSampler)
- Set of filtered unique molecular formulas within m/z range
- Chemical objects suitable for input to virtual mass spectrometer (via ChemicalMixtureCreator)

## How to apply

Select a formula sampler class appropriate to your chemical source: use UniformMZFormulaSampler if you want formulas uniformly distributed across an m/z range, or DatabaseFormulaSampler if you want to sample from a curated metabolite database (e.g., HMDB). Instantiate the sampler with min_mz and max_mz parameters (e.g., min_mz=100, max_mz=1000) to constrain the m/z range. Load the HMDB database using ViMMS's data-loading utilities if using DatabaseFormulaSampler. Pass the configured sampler to a ChemicalMixtureCreator to generate chemical objects, which can then be provided to the virtual mass spectrometer. Verify the filtering logic by counting unique formulas in the output and confirming the count matches expected values (e.g., 73,822 for HMDB m/z 100–1000).

## Related tools

- **ViMMS** (Core framework providing DatabaseFormulaSampler, UniformMZFormulaSampler, and ChemicalMixtureCreator classes for formula sampling and chemical population generation.) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Reference metabolite database providing chemical formulas and m/z values for sampling; downloaded as pickle or zipped file.) — https://github.com/glasgowcompbio/vimms-data
- **Python** (Programming environment for instantiating sampler objects and executing filtering logic.)

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator
from vimms.formula_sampler import DatabaseFormulaSampler
import pickle
with open('hmdb_compounds.p', 'rb') as f:
    hmdb = pickle.load(f)
sampler = DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000)
cmc = ChemicalMixtureCreator(sampler)
chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- Sampler instantiation succeeds without errors and the object is of the correct type (DatabaseFormulaSampler or UniformMZFormulaSampler).
- Count of unique formulas in the filtered output matches the expected value for the given database and m/z range (e.g., 73,822 for HMDB m/z 100–1000).
- All formulas in the output fall within the specified m/z bounds (no formulas < min_mz or > max_mz).
- ChemicalMixtureCreator successfully consumes the sampler and generates chemical objects without throwing exceptions.
- Generated chemical objects can be passed to IndependentMassSpectrometer and Environment without type errors.

## Limitations

- DatabaseFormulaSampler filtering accuracy depends on the completeness and correctness of the reference HMDB database; missing or corrupted entries may affect the final formula count.
- The sampler applies hard m/z bounds but does not validate chemical plausibility or filter by other molecular properties (e.g., charge state, adduct type) unless explicitly configured downstream.
- Sampling from very large databases (e.g., full HMDB) may require significant memory; performance will vary with database size and machine specifications.
- UniformMZFormulaSampler generates formulas uniformly across m/z but may not reflect the natural distribution of metabolites in real samples.

## Evidence

- [other] Can the reported count of 73,822 unique formulas in the HMDB database (filtered for m/z 100–1000) be reproduced by running DatabaseFormulaSampler on the downloaded raw HMDB data?: "The DatabaseFormulaSampler successfully filters the HMDB database and reports 73,822 unique formulas when applied to chemical formulae in the m/z range 100–1000."
- [other] Instantiation and parameterization workflow: "# 1. Generate chemicals
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)"
- [results] Database sampler with m/z filtering: "DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000)"
- [results] Workflow step for loading HMDB: "Download the HMDB database and extract metabolites."
- [intro] ViMMS framework purpose: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
