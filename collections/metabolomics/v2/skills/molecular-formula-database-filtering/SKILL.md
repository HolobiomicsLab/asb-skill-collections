---
name: molecular-formula-database-filtering
description: Use when when you need to constrain a large metabolite database to a specific instrumental range (e.g., m/z 100–1000) before generating virtual chemical mixtures for LC-MS/MS simulation, or when you need to verify that a reported filtered database count can be reproduced from raw database files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - ViMMS
  - HMDB database
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

# molecular-formula-database-filtering

## Summary

Filter a molecular formula database (e.g., HMDB) by physicochemical constraints such as m/z range to obtain a subset of unique chemical formulae suitable for virtual mass spectrometry simulation or targeted metabolomics analysis.

## When to use

When you need to constrain a large metabolite database to a specific instrumental range (e.g., m/z 100–1000) before generating virtual chemical mixtures for LC-MS/MS simulation, or when you need to verify that a reported filtered database count can be reproduced from raw database files.

## When NOT to use

- Input is already a pre-filtered formula list or chemical mixture object—use this skill only on raw, unfiltered database files.
- You are filtering by tandem MS fragmentation patterns or spectral similarity rather than by molecular formula and m/z range.
- The database is not HMDB or a similar structure-preserving metabolite compendium (e.g., if working with raw peak lists or already-processed mzML scans).

## Inputs

- HMDB database file (hmdb_metabolites.zip or pickle format)
- m/z range constraints (min_mz, max_mz)
- Optional: additional physicochemical filter parameters

## Outputs

- Filtered set of unique molecular formulae
- Count of unique formulae meeting filter criteria
- Optionally: chemical objects with assigned m/z and formula annotations

## How to apply

Load the raw HMDB database file (e.g., hmdb_metabolites.zip or pickle format) using ViMMS's HMDB data-loading utilities. Instantiate a DatabaseFormulaSampler class with the loaded HMDB data and specify filtering constraints—typically an m/z range (e.g., min_mz=100, max_mz=1000). Execute the sampler's internal filtering logic to produce the set of unique molecular formulae that pass all criteria. Count the total number of unique formulae in the filtered result and compare against any reported or expected counts to verify reproducibility. The filtering is deterministic and does not involve randomization, so the count should be stable across runs.

## Related tools

- **ViMMS** (Python framework providing DatabaseFormulaSampler class and HMDB data-loading utilities for filtering and instantiating chemical objects from the HMDB database) — https://github.com/glasgowcompbio/vimms
- **HMDB database** (Source metabolite database containing chemical formulae and m/z values to be filtered) — https://github.com/glasgowcompbio/vimms-data
- **Python** (Programming language in which ViMMS and the DatabaseFormulaSampler filtering logic are implemented)

## Examples

```
from vimms import DatabaseFormulaSampler; sampler = DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000); filtered_formulas = sampler.sample(); print(len(filtered_formulas))
```

## Evaluation signals

- The reported filtered formula count (e.g., 73,822 unique formulae in m/z range 100–1000) is reproduced exactly when running the sampler on the same raw database file.
- All returned molecular formulae fall within the specified m/z range (min_mz ≤ observed m/z ≤ max_mz).
- The filtered formula set contains no duplicates; uniqueness constraint is enforced by the sampler's internal logic.
- Running the sampler multiple times on the same database and constraints yields identical formula counts and membership.
- The sampler output is compatible with downstream ViMMS classes (e.g., ChemicalMixtureCreator can successfully ingest the filtered formula set to generate chemical objects).

## Limitations

- The filtering operates only on molecular formula and m/z range; it does not filter by spectroscopic properties, ionization efficiency, or likelihood of detection in real MS runs.
- HMDB coverage is limited to annotated metabolites; novel or rare compounds outside HMDB will not be captured.
- The reported filter count depends on the exact version and completeness of the downloaded HMDB database file; updates to HMDB may yield slightly different counts.
- Filtering assumes m/z is computed from molecular formula using a standard mass calculation (typically [M+H]+ for positive mode); different ionization adducts or charge states are not explicitly handled in the basic sampler.

## Evidence

- [other] task_004 research_question: "Can the reported count of 73,822 unique formulas in the HMDB database (filtered for m/z 100–1000) be reproduced by running DatabaseFormulaSampler on the downloaded raw HMDB data?"
- [other] task_004 finding: "The DatabaseFormulaSampler successfully filters the HMDB database and reports 73,822 unique formulas when applied to chemical formulae in the m/z range 100–1000."
- [other] task_004 workflow step 1: "Download the HMDB database file (hmdb_metabolites.zip or equivalent pickle file) from the vimms-data repository."
- [other] task_004 workflow step 3: "Instantiate a DatabaseFormulaSampler with the loaded HMDB database and apply formula-filtering constraints (e.g., m/z range 100–1000 if specified)."
- [readme] README workflow step: "DatabaseFormulaSampler(hmdb, min_mz=100, max_mz=1000)"
- [other] Article workflow: generate chemicals: "chemical objects are generated by sampling from metabolites in the HMDB database"
