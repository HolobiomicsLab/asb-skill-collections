---
name: formula-deduplication-and-counting
description: Use when when you have loaded a chemical database (e.g., HMDB pickle file) and need to understand how many distinct molecular formulas remain after filtering for a specific m/z range (e.g., 100–1000) and MS acquisition level (typically MS level 1).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - ViMMS
  - Python pickle
  - pandas
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
---

# formula-deduplication-and-counting

## Summary

Deduplicate and count unique molecular formulas from a filtered chemical database after applying m/z range and MS level constraints. This skill quantifies the diversity of ionizable species available in a virtual metabolomics acquisition simulation.

## When to use

When you have loaded a chemical database (e.g., HMDB pickle file) and need to understand how many distinct molecular formulas remain after filtering for a specific m/z range (e.g., 100–1000) and MS acquisition level (typically MS level 1). This is essential before running virtual mass spectrometry experiments to ensure the chemical space is correctly scoped.

## When NOT to use

- If the input database is already in a feature table or has been pre-deduplicated and you only need to query the count without re-filtering.
- If you need to preserve or analyze duplicate formula entries (e.g., to study isotopologues or different adducts of the same formula).
- If your workflow requires formula-level metadata (e.g., retention time, intensity, or adduct annotation) — this skill only counts unique formulas.

## Inputs

- HMDB compounds database (pickled Python object, .p file)
- m/z range specification (min_mz, max_mz)
- MS level filter parameter (e.g., ms_levels=1)

## Outputs

- Deduplicated molecular formula list (set or pandas Series)
- Count of unique molecular formulas (integer)
- Summary report with formula count and filter parameters

## How to apply

Load the HMDB compounds database using Python pickle deserialization. Apply a minimum and maximum m/z filter (e.g., min_mz=100, max_mz=1000) to retain only formulas within the instrument's observable range. Further filter to retain only compounds with ms_levels=1 to match the target acquisition mode. Deduplicate the filtered formula set by converting to a set or using pandas drop_duplicates() to remove duplicate entries. Count the total number of unique formulas and record in a summary report or return as a scalar for downstream validation or comparisons.

## Related tools

- **ViMMS** (Framework within which the formula sampling and filtering occurs; DatabaseFormulaSampler applies the m/z and MS level filters before deduplication) — https://github.com/glasgowcompbio/vimms
- **Python pickle** (Deserializes the HMDB compounds database (.p file) into memory for filtering)
- **pandas** (Optional utility for efficient deduplication and counting of formulas)

## Examples

```
import pickle
with open('hmdb_compounds.p', 'rb') as f:
    hmdb = pickle.load(f)
filtered = [f for f in hmdb if 100 <= f.mass <= 1000 and f.ms_levels == 1]
unique_formulas = set(f.formula for f in filtered)
print(len(unique_formulas))
```

## Evaluation signals

- The count of unique formulas equals the cardinality of the deduplicated set (no duplicates remain).
- The reported count (73,822 for HMDB with m/z 100–1000, MS level 1) is reproducible across multiple runs with identical filter parameters.
- All returned formulas have m/z values within the specified range (100–1000) when calculated from their neutral masses.
- Formulas excluded by the m/z or MS level filter are not present in the final deduplicated set.
- The count is ≥ 1 and ≤ the total number of formulas in the original database (sanity bounds check).

## Limitations

- The skill depends on the completeness and accuracy of the input HMDB database file; corrupt or incomplete .p files will yield incorrect counts.
- M/z calculations assume a specific ionization mode (implied but not explicitly stated in the workflow); switching ionization modes (positive vs. negative) may change the effective m/z range and thus the count.
- Deduplication is formula-level only; structurally different compounds with identical molecular formulas are not distinguished and will not be double-counted.
- The skill does not validate or flag ambiguous or unusual formulas; implausible elemental compositions will still be counted.

## Evidence

- [other] When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas.: "When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas."
- [other] Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range. Filter to retain only MS level 1 compounds by selecting those with ms_levels=1. De-duplicate the filtered formula set to obtain unique molecular formula entries.: "Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range. 3. Filter to retain only MS level 1 compounds by selecting those with ms_levels=1. 4. De-duplicate"
- [other] Load the HMDB compounds database (hmdb_compounds.p) using Python pickle.: "Load the HMDB compounds database (hmdb_compounds.p) using Python pickle."
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
