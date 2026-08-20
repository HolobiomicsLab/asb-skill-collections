---
name: chemical-formula-extraction-and-filtering
description: Use when when you have a loaded metabolite database (e.g., hmdb_compounds.p pickle file) and need to constrain the chemical space to a specific instrumental m/z range (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
  tools:
  - ViMMS
  - ViMMS (Virtual Metabolomics Mass Spectrometer)
  - Python pickle
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

# chemical-formula-extraction-and-filtering

## Summary

Extract and filter chemical molecular formulas from a metabolite database (HMDB) by applying mass-to-charge ratio (m/z) range and MS level constraints, then deduplicate to obtain a curated set of unique formulas suitable for metabolomics simulation or sampling.

## When to use

When you have a loaded metabolite database (e.g., hmdb_compounds.p pickle file) and need to constrain the chemical space to a specific instrumental m/z range (e.g., 100–1000 Da) and MS acquisition level before running virtual mass spectrometry simulations or designing data-dependent acquisition strategies.

## When NOT to use

- Input database is already formatted as a deduplicated feature table or matrix; use direct indexing instead.
- m/z range is instrument-independent (e.g., you are performing untargeted discovery across all accessible masses); applying a fixed range will discard relevant chemistry.
- Database records lack explicit ms_levels field or are not in pickle format; verify schema compatibility first.

## Inputs

- HMDB compounds database (Python pickle file: hmdb_compounds.p)
- m/z range bounds (min_mz, max_mz as floats or integers)
- MS level filter specification (ms_levels integer or list)

## Outputs

- Filtered, deduplicated set of unique molecular formulas
- Count of unique molecular formulas
- Summary report (e.g., JSON, CSV, or log file with filter statistics)

## How to apply

Load the HMDB compounds database using Python pickle deserialization. Apply a minimum m/z filter (min_mz=100) and maximum m/z filter (max_mz=1000) to retain only formulas whose monoisotopic mass falls within the instrumental range. Filter to retain only MS level 1 (MS1) compounds by selecting records with ms_levels=1, eliminating fragmentation-only entries. Deduplicate the filtered result set to obtain unique molecular formula entries. Count the total unique formulas and record in a summary report. The rationale is to ensure the virtual environment samples only from chemically plausible, instrument-accessible molecules.

## Related tools

- **ViMMS (Virtual Metabolomics Mass Spectrometer)** (Framework that uses the DatabaseFormulaSampler to load and filter HMDB formulas for chemical sampling in tandem MS simulation and DDA strategy prototyping) — https://github.com/glasgowcompbio/vimms
- **Python pickle** (Standard library for deserializing the hmdb_compounds.p database file into Python objects)

## Examples

```
from vimms.ChemicalSamplers import DatabaseFormulaSampler; import pickle; db = pickle.load(open('hmdb_compounds.p', 'rb')); sampler = DatabaseFormulaSampler(db, min_mz=100, max_mz=1000, ms_level=1); unique_formulas = set(sampler.formulas); print(f'Unique formulas: {len(unique_formulas)}')
```

## Evaluation signals

- Returned count of unique formulas matches expected cardinality for the m/z range (e.g., 73,822 for m/z 100–1000 in HMDB); verify against a manually spot-checked subset or prior runs.
- No duplicate formulas in the deduplicated output; perform set cardinality check: len(unique_formulas) == len(set(unique_formulas)).
- All retained formulas have m/z values strictly within [min_mz, max_mz] bounds; sample formulas and verify min(mz_values) >= 100 and max(mz_values) <= 1000.
- All retained formulas have ms_levels == 1; verify that any formula with ms_levels > 1 or ms_levels == 0 was filtered out.
- Summary report contains filter step metadata (input record count, pre-filter count, post-filter count, deduplication count, final count) to audit data loss at each stage.

## Limitations

- HMDB pickle format is version-dependent; schema changes between HMDB releases may require field name updates (e.g., ms_levels vs. msn_level).
- The m/z filter assumes monoisotopic mass; isotope-resolved or adduct-specific m/z (e.g., [M+H]+, [M+Na]+) is not explicitly handled in this workflow and may require post-filtering.
- Deduplication is performed on the formula string only, not on the full chemical structure; isomers with identical molecular formula will collapse to a single entry.
- Performance scales linearly with database size; for very large databases (> 1M compounds), consider chunking or lazy loading to avoid memory exhaustion.

## Evidence

- [other] When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas.: "When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas."
- [other] 1. Load the HMDB compounds database (hmdb_compounds.p) using Python pickle. 2. Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range. 3. Filter to retain only MS level 1 compounds by selecting those with ms_levels=1. 4. De-duplicate the filtered formula set to obtain unique molecular formula entries. 5. Count the total number of unique formulas and record in a summary report.: "Load the HMDB compounds database (hmdb_compounds.p) using Python pickle. Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range."
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
- [intro] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
