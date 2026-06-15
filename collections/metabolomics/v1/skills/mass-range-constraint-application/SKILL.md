---
name: mass-range-constraint-application
description: Use when when generating a virtual chemical mixture for LC-MS/MS simulation, or when sampling molecular formulas from a metabolite database (such as HMDB), you need to restrict the sample to a specific m/z window that matches your instrument's acquisition range or your analytical focus.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - VIMMS
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
schema_version: 0.2.0
---

# mass-range-constraint-application

## Summary

Apply mass-to-charge (m/z) range constraints to filter chemical formulas or compounds from metabolomics databases or samplers. This skill ensures that only molecules within a specified mass window are considered for simulation or analysis, which is essential for focusing acquisition strategies on the target mass range of the instrument.

## When to use

When generating a virtual chemical mixture for LC-MS/MS simulation, or when sampling molecular formulas from a metabolite database (such as HMDB), you need to restrict the sample to a specific m/z window that matches your instrument's acquisition range or your analytical focus. This is particularly important before instantiating a formula sampler or creating chemical objects to avoid processing irrelevant out-of-range molecules.

## When NOT to use

- Input is already a pre-filtered chemical mixture or mzML file with specific m/z data — re-filtering may lose or corrupt existing intensity/RT metadata.
- The analytical goal requires exploring the full mass range or comparing across multiple non-overlapping windows — applying a single fixed range would exclude relevant molecules.
- Database or formula sampler does not expose m/z filtering parameters — use alternative filtering steps (e.g., post-hoc filtering on computed m/z values) instead.

## Inputs

- HMDB database (pickle or zip file with metabolite records)
- Formula sampler configuration (min_mz, max_mz parameters)
- Raw molecular formula collection or metabolite list

## Outputs

- Filtered set of unique molecular formulas within the m/z range
- Count or metadata of molecules passing the mass constraint
- Chemical objects or mixture ready for downstream simulation

## How to apply

Specify the `min_mz` and `max_mz` parameters when instantiating a formula sampler (e.g., `DatabaseFormulaSampler` or `UniformMZFormulaSampler`) or when loading chemical mixtures. For example, set `min_mz=100` and `max_mz=1000` to restrict to that window. The sampler's internal filtering logic will apply these bounds and return only unique molecular formulas that fall within the specified m/z range. After instantiation, execute the sampler and count or validate the filtered result to confirm the expected number of molecules pass the constraint (as in task_004, which verified 73,822 unique formulas in the 100–1000 m/z range for HMDB).

## Related tools

- **VIMMS** (Hosts and executes DatabaseFormulaSampler and UniformMZFormulaSampler classes that accept and apply m/z range constraints during chemical mixture generation) — https://github.com/glasgowcompbio/vimms
- **HMDB** (Source metabolite database that is loaded and filtered by m/z range constraints to generate virtual chemical objects)
- **Python** (Programming environment in which m/z constraint parameters are specified and sampler methods are invoked)

## Examples

```
from vimms.ChemicalMixtureCreator import ChemicalMixtureCreator
from vimms.VimsController import DatabaseFormulaSampler
sampler = DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000)
cmc = ChemicalMixtureCreator(sampler)
chemicals = cmc.sample(100, ms_levels=2)
```

## Evaluation signals

- The count of unique filtered formulas matches the expected or reported count (e.g., 73,822 for HMDB at m/z 100–1000).
- All formulas in the filtered output have m/z values strictly within [min_mz, max_mz]; spot-check by computing or inspecting representative formula monoisotopic masses.
- No out-of-range formulas appear in the sampled chemical objects when displayed or logged during instantiation.
- Downstream simulation (e.g., Environment.run()) processes only chemicals within the constrained range, verifiable via scan metadata or ms1_mz fields.
- Reducing min_mz or max_mz yields proportionally fewer filtered molecules; expanding the range yields more (monotonic behavior).

## Limitations

- The m/z filtering is performed at instantiation time; changing the range requires re-instantiation of the sampler.
- Database accuracy depends on the underlying chemical formula accuracy in HMDB or other source — incorrect or missing formulas in the database will not be corrected by this filter.
- Very tight m/z windows (e.g., <100 Da) may yield very few or no molecules, limiting statistical power in downstream simulation.
- The filter applies to neutral mass formulas; actual observed m/z depends on ionization mode (positive/negative) and adducts, which are not accounted for by the range constraint alone.

## Evidence

- [results] DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000): "Create database formula sampler with m/z range 100-1000"
- [other] The DatabaseFormulaSampler successfully filters the HMDB database and reports 73,822 unique formulas when applied to chemical formulae in the m/z range 100–1000.: "finding from task_004 demonstrating validation of m/z-constrained filtering"
- [other] formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600): "# 1. Generate chemicals
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)"
- [intro] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "VIMMS provides a framework to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [results] chemical objects are generated by sampling from metabolites in the HMDB database: "Generate chemical objects by sampling from metabolites in HMDB database"
