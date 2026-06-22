---
name: molecular-database-loading-and-parsing
description: Use when when setting up a ViMMS chemical sampling environment and you need to restrict the chemical search space to a specific m/z range (e.g., 100–1000) and MS level (e.g., MS1 only) before generating virtual LC-MS/MS data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - ViMMS
  - Python pickle
  techniques:
  - LC-MS
  - ion-mobility-MS
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-database-loading-and-parsing

## Summary

Load and parse serialized molecular structure databases (e.g., HMDB compounds in pickle format) into memory, then apply m/z range and MS level filters to extract a curated set of unique molecular formulas for chemical sampling in virtual metabolomics simulations.

## When to use

When setting up a ViMMS chemical sampling environment and you need to restrict the chemical search space to a specific m/z range (e.g., 100–1000) and MS level (e.g., MS1 only) before generating virtual LC-MS/MS data. Use this skill before initializing a DatabaseFormulaSampler or equivalent chemical generator.

## When NOT to use

- Database is already in memory and pre-filtered — skip loading and filtering steps and pass the formula set directly to the sampler.
- You need to preserve all formulas including adducts and isotopologues — this skill removes duplicates and MS level variants.
- Target m/z range extends outside the database's native coverage — verify database m/z distribution before setting thresholds.

## Inputs

- Serialized molecule database file (pickle format, e.g., hmdb_compounds.p)
- m/z range parameters (min_mz, max_mz as floats)
- MS level filter criterion (ms_levels as integer)

## Outputs

- Filtered set of unique molecular formulas (Python list or set)
- De-duplicated formula count (integer)
- Summary report documenting filter criteria and result count

## How to apply

Load the HMDB compounds database (hmdb_compounds.p) using Python pickle deserialization. Apply a minimum and maximum m/z boundary filter (e.g., min_mz=100, max_mz=1000) to retain only molecular formulas within the instrument's operating range. Filter further to retain only MS level 1 compounds (ms_levels=1) to focus on parent ion-level chemistry. De-duplicate the filtered formula set to obtain a canonical list of unique molecular formulas. Count and record the total number of unique formulas in a summary report; this count (e.g., 73822 formulas for HMDB with m/z 100–1000) documents the effective search space for the simulation.

## Related tools

- **ViMMS** (Simulation framework that consumes the filtered formula set via DatabaseFormulaSampler to generate virtual chemical samples for LC-MS/MS acquisition simulation) — https://github.com/glasgowcompbio/vimms
- **Python pickle** (Standard library module for deserializing the HMDB database from binary pickle format into Python objects)

## Examples

```
import pickle
db = pickle.load(open('hmdb_compounds.p', 'rb'))
filtered = [c for c in db if 100 <= c.get('mz', 0) <= 1000 and c.get('ms_levels') == 1]
unique_formulas = list(set(c['formula'] for c in filtered))
print(f'Unique formulas: {len(unique_formulas)}')
```

## Evaluation signals

- Pickle deserialization succeeds without corruption or version mismatch errors; database object structure matches expected schema (e.g., list of compound dicts with 'formula', 'mz', 'ms_levels' keys).
- m/z filter: verify min_mz ≤ all retained formulas' m/z ≤ max_mz; confirm count of out-of-range formulas are excluded.
- MS level filter: spot-check a random sample of retained formulas to confirm ms_levels == 1; verify count of filtered-out multi-level entries.
- De-duplication check: compare filtered count to count after applying `set()` on formula strings; counts must be equal.
- Reported unique formula count (e.g., 73822 for HMDB m/z 100–1000) is reproducible across multiple runs with identical parameters; log the count and filter parameters for audit trail.

## Limitations

- Database file format (pickle) is Python-specific and not human-readable; validation requires unpickling. If file is corrupted or from an incompatible Python/library version, deserialization will fail.
- m/z filtering assumes formula molecular weight correlates linearly with m/z; adducts, charge states, and post-ionization modifications are not accounted for in this step.
- De-duplication is string-based (e.g., 'C6H12O6' == 'C6H12O6'); isomers with identical molecular formula are collapsed into one, potentially losing chemical diversity.
- MS level filtering to 1 only excludes doubly-charged, multiply-ionized, and fragmented species; may not suit high-resolution or ion-mobility workflows.

## Evidence

- [other] Load the HMDB compounds database (hmdb_compounds.p) using Python pickle: "1. Load the HMDB compounds database (hmdb_compounds.p) using Python pickle."
- [other] Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range: "2. Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range."
- [other] Filter to retain only MS level 1 compounds by selecting those with ms_levels=1: "3. Filter to retain only MS level 1 compounds by selecting those with ms_levels=1."
- [other] De-duplicate the filtered formula set to obtain unique molecular formula entries: "4. De-duplicate the filtered formula set to obtain unique molecular formula entries."
- [other] When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas: "When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas."
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
