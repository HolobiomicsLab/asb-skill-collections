---
name: virtual-chemical-mixture-generation
description: Use when you need to create a synthetic chemical population for testing data-dependent acquisition (DDA) strategies in a simulation environment before committing to real mass spectrometry analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - ViMMS
  - HMDB
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
---

# virtual-chemical-mixture-generation

## Summary

Generate realistic virtual chemical mixtures by sampling molecular formulas across a specified m/z range and MS levels using ViMMS samplers and mixture creators. This skill enables simulation-based development of LC-MS/MS fragmentation strategies without requiring real chemical standards or instrument time.

## When to use

Use this skill when you need to create a synthetic chemical population for testing data-dependent acquisition (DDA) strategies in a simulation environment before committing to real mass spectrometry analysis. Apply it when you want deterministic, reproducible chemical sets for comparing multiple fragmentation controllers, or when you need to prototype new MS/MS methods without access to real metabolomics data.

## When NOT to use

- Input chemicals are already empirically measured or extracted from real mzML files (use ChemicalMixtureFromMZML instead)
- You require exact isotope patterns or advanced fragmentation libraries not built into the sampler
- The simulation goal is to replay a specific previous LC-MS/MS analysis (use real peak-picked data with explicit m/z and intensity values)

## Inputs

- Formula sampler configuration (min_mz, max_mz, sampler type)
- Number of compounds to generate (integer)
- MS levels specification (e.g., ms_levels=2 for MS1+MS2)

## Outputs

- Chemical list (list of Chemical objects with m/z, intensity, fragmentation data)
- Metadata: sampler parameters, formula distribution statistics

## How to apply

Select an appropriate formula sampler (e.g., UniformMZFormulaSampler for synthetic chemicals, or DatabaseFormulaSampler for HMDB-derived compounds) and define the m/z range (e.g., 100–500 Da for small molecules). Instantiate a ChemicalMixtureCreator with the sampler and call sample() specifying the desired number of compounds (e.g., 100) and ms_levels (typically 2 for MS1 and MS2 tandem workflows). The resulting chemical list carries intensity profiles and m/z values that respect the sampler's distribution. Pass this list directly to an IndependentMassSpectrometer constructor in the next orchestration step. Verify the output contains non-empty Chemical objects with both MS1 and MS2 records and m/z values within the requested bounds.

## Related tools

- **ViMMS** (Provides UniformMZFormulaSampler, DatabaseFormulaSampler, and ChemicalMixtureCreator for generating virtual chemical mixtures with configurable m/z ranges and MS levels) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Source database for metabolite formulas when using DatabaseFormulaSampler to generate chemicals sampled from real metabolite pools)
- **Python** (Execution environment for instantiating samplers and calling sample() methods)

## Examples

```
from vimms.ChemicalMixtureCreator import UniformMZFormulaSampler, ChemicalMixtureCreator
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- Verify the returned chemical list is non-empty and contains the requested number of compounds
- Confirm all Chemical objects have m/z values strictly within [min_mz, max_mz] bounds (e.g., 100–500 Da)
- Check that ms_levels=2 chemicals contain both MS1 (intact molecule) and MS2 (fragment ion) records
- Validate intensity values are non-negative and reasonable for MS1 peaks (e.g., match sampler intensity model)
- Ensure no duplicate m/z values exist at the precision needed for isolation window control (typically 1 Da or finer)

## Limitations

- UniformMZFormulaSampler generates synthetic m/z distributions that may not reflect real metabolome sparsity or isotope clustering
- DatabaseFormulaSampler requires access to HMDB or similar database file; licensing or download may be needed
- Generated chemicals lack context-specific fragmentation patterns unless paired with a fragmentation library or empirical spectrum matching
- No support for post-translational modifications, adducts, or multimeric species without manual Chemical object annotation

## Evidence

- [other] Generate 100 virtual chemicals by sampling m/z uniformly between 100–500 Da using UniformMZFormulaSampler and ChemicalMixtureCreator, requesting both MS1 and MS2 levels.: "Generate 100 virtual chemicals by sampling m/z uniformly between 100–500 Da using UniformMZFormulaSampler and ChemicalMixtureCreator, requesting both MS1 and MS2 levels"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] Generate chemicals using formula samplers with parameters min_mz=100, max_mz=600 and sample(100, ms_levels=2): "formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)"
- [results] chemical objects are generated by sampling from metabolites in the HMDB database: "chemical objects are generated by sampling from metabolites in the HMDB database"
- [other] They can be sampled from databases such as HMDB: "They can be sampled from databases such as HMDB"
