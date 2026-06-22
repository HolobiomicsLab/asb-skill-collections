---
name: mass-range-filtering-for-metabolomics
description: Use when when preparing a chemical database for virtual or real MS/MS acquisition, and you need to focus on a specific m/z window (e.g., 100–1000) that matches your instrument's scan range or your metabolomics study's analytical scope.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - ViMMS
  - Python pickle
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

# mass-range-filtering-for-metabolomics

## Summary

Filter a metabolite database by m/z range to retain only compounds within a target mass spectrometry analysis window. This preprocessing step isolates chemically relevant formulas before acquisition strategy simulation or spectral library construction.

## When to use

When preparing a chemical database for virtual or real MS/MS acquisition, and you need to focus on a specific m/z window (e.g., 100–1000) that matches your instrument's scan range or your metabolomics study's analytical scope. Triggered by the need to reduce database size while maintaining chemical relevance and avoiding analysis of compounds outside the detectable mass range.

## When NOT to use

- Input is already a subset database or spectral library pre-filtered by m/z — reapplying range filtering may discard valid compounds or create redundant work.
- Analysis requires compounds outside the specified m/z window (e.g., studying very large lipids >1000 or very small metabolites <100) — the filter will exclude them systematically.
- Database lacks reliable neutral mass or molecular formula annotation — filtering cannot proceed without this metadata.

## Inputs

- Full metabolite database (pickle format, e.g., hmdb_compounds.p)
- Min m/z threshold (numeric, e.g., 100)
- Max m/z threshold (numeric, e.g., 1000)
- Optional MS level specification (e.g., ms_levels=1)

## Outputs

- Filtered and deduplicated set of molecular formulas
- Count of unique formulas passing filters (e.g., 73822 for HMDB m/z 100–1000)
- Summary report documenting filter parameters and retention statistics

## How to apply

Load the full metabolite database (e.g., HMDB pickle file) into memory. Apply a dual-threshold m/z filter by retaining only molecular formulas with neutral mass ≥ min_mz and ≤ max_mz (e.g., min_mz=100, max_mz=1000). Optionally filter by MS level (e.g., ms_levels=1 for intact precursors only). De-duplicate the filtered formula set to obtain unique molecular entries. Count and log the resulting formula count as a quality metric. This approach ensures only compounds theoretically ionizable within your instrument's operating window are used downstream in simulation or matching workflows.

## Related tools

- **ViMMS** (Virtual MS/MS simulation framework that consumes filtered chemical databases (e.g., via DatabaseFormulaSampler) to generate or replay LC-MS/MS acquisitions within the specified m/z window) — https://github.com/glasgowcompbio/vimms
- **Python pickle** (Serialization format for loading and parsing the HMDB database file in memory)

## Examples

```
# Python snippet for filtering HMDB database by m/z range
import pickle
with open('hmdb_compounds.p', 'rb') as f:
    compounds = pickle.load(f)
filtered = {c['formula']: c for c in compounds if 100 <= c['mz'] <= 1000 and c.get('ms_levels') == 1}
print(f'Unique formulas: {len(set(filtered.keys()))}')
```

## Evaluation signals

- Verify output formula count matches expected cardinality for the database and m/z window (e.g., 73822 for HMDB 100–1000).
- Confirm all formulas in the output have neutral mass within [min_mz, max_mz] via spot-check sampling.
- Validate deduplification: output formula set size ≤ input size, with no duplicate entries.
- Check that MS level filtering (if applied) correctly retained only compounds matching the specified level(s).
- Ensure summary report documents parameters (min_mz, max_mz, ms_levels) and result count for reproducibility and auditability.

## Limitations

- Filtering discards all compounds outside the m/z range; if the range is too narrow, valid metabolites relevant to the study will be lost. Selection of min/max thresholds requires prior knowledge of the instrument and study scope.
- Filter assumes accurate neutral mass calculation from molecular formula; errors in formula annotation propagate through the filter.
- De-duplication removes only exact formula matches; structural isomers with identical formulas will be collapsed to one entry, potentially losing isomeric diversity.

## Evidence

- [other] When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas.: "When the DatabaseFormulaSampler filters the HMDB database for formulas with m/z between 100 and 1000, it yields 73822 unique molecular formulas."
- [other] Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range.: "Apply m/z range filter (min_mz=100, max_mz=1000) to retain only formulas within the specified range."
- [other] Filter to retain only MS level 1 compounds by selecting those with ms_levels=1.: "Filter to retain only MS level 1 compounds by selecting those with ms_levels=1."
- [other] De-duplicate the filtered formula set to obtain unique molecular formula entries.: "De-duplicate the filtered formula set to obtain unique molecular formula entries."
- [other] Chemicals can be sampled from databases such as HMDB or from specific distributions: "Chemicals can be sampled from databases such as HMDB or from specific distributions"
