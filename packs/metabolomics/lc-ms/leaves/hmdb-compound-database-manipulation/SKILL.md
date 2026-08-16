---
name: hmdb-compound-database-manipulation
description: Use when when you need to establish a reproducible inventory of compounds for LC-MS/MS simulation studies, particularly to determine how many unique molecular formulas fall within a target m/z window (e.g., 100–1000 Da) and MS1 detection level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - ViMMS
  - Python pickle module
  - DatabaseFormulaSampler
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hmdb-compound-database-manipulation

## Summary

Load, filter, and deduplicate the HMDB compounds database by m/z range and MS level to obtain counts and inventories of unique molecular formulas for virtual metabolomics simulation. This skill enables reproducible quantification of the chemical search space available for fragmentation strategy development.

## When to use

When you need to establish a reproducible inventory of compounds for LC-MS/MS simulation studies, particularly to determine how many unique molecular formulas fall within a target m/z window (e.g., 100–1000 Da) and MS1 detection level. Use this skill before generating virtual chemical populations or validating acquisition strategy performance against a known compound set.

## When NOT to use

- Input is already a pre-filtered formula list or feature table — skip deduplication and recount only.
- MS/MS fragmentation data (MS2 spectra) are required — this skill addresses only MS1 chemical inventory, not spectral libraries.
- You need real experimental compound detection; ViMMS produces simulated data, so use actual LC-MS/MS runs for validation.

## Inputs

- HMDB pickle database file (hmdb_compounds.p)
- m/z range parameters (min_mz, max_mz as floats)
- MS level filter (integer, typically 1)

## Outputs

- Deduplicated set of unique molecular formulas (Python set or list)
- Count of unique formulas (integer)
- Summary report (text or JSON)

## How to apply

Load the HMDB compounds database (hmdb_compounds.p) using Python pickle, then apply a two-stage filter: first, retain only formulas with m/z between the specified minimum and maximum bounds (typically min_mz=100, max_mz=1000); second, select only MS level 1 compounds (ms_levels=1) to match the instrument's capability. Deduplicate the filtered set by molecular formula to remove redundancy, then count and record the total unique formulas. This approach ensures that simulation studies use a consistent, documented chemical search space and that reported findings (e.g., '73,822 unique molecular formulas') are reproducible by peers.

## Related tools

- **ViMMS** (Framework that uses the filtered HMDB database to generate virtual LC-MS/MS data and evaluate acquisition strategies) — https://github.com/glasgowcompbio/vimms
- **Python pickle module** (Deserialize the HMDB compounds database from binary format)
- **DatabaseFormulaSampler** (ViMMS component that applies m/z and MS level filters to the HMDB database) — https://github.com/glasgowcompbio/vimms

## Examples

```
import pickle; db = pickle.load(open('hmdb_compounds.p', 'rb')); filtered = [f for f in db if 100 <= f.mz <= 1000 and f.ms_levels == 1]; unique_formulas = len(set(f.formula for f in filtered)); print(f'Unique formulas: {unique_formulas}')
```

## Evaluation signals

- Reported unique formula count (e.g., 73,822) is reproducible by independent execution of the same pickle file with identical filter parameters.
- Deduplicated formula set size equals count of unique entries; no duplicate formulas remain.
- All formulas in output satisfy min_mz ≤ formula_mz ≤ max_mz and ms_levels=1 constraints; spot-check ≥5 boundary and interior samples.
- Summary report documents filter parameters, input database filename, timestamp, and row counts before/after deduplication to enable audit trail.
- Output formulas are valid molecular formula strings (e.g., 'C6H12O6') parseable by metabolomics libraries.

## Limitations

- HMDB database snapshot is time-dependent; different versions yield different counts and formulas, so results must cite the HMDB release date.
- MS level filtering (ms_levels=1) excludes higher-order MS data; if MS/MS or MSn spectra are present, they are discarded.
- m/z filtering is applied to nominal or monoisotopic mass; very high-resolution or isotope-labeling workflows may require mass-dependent tolerance adjustments not captured by simple min/max bounds.
- Deduplication assumes formula strings are exact matches; formatting or tautomeric variants (e.g., 'C6H12O6' vs. 'C₆H₁₂O₆') could artificially inflate counts if inconsistently represented.

## Evidence

- [other] When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas.: "When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas."
- [other] Load the HMDB compounds database (hmdb_compounds.p) using Python pickle. Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range. Filter to retain only MS level 1 compounds by selecting those with ms_levels=1. De-duplicate the filtered formula set to obtain unique molecular formula entries.: "Load the HMDB compounds database (hmdb_compounds.p) using Python pickle. Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range. Filter to retain only MS"
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
- [readme] A flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics.: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
