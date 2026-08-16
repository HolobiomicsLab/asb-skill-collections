---
name: multi-database-structure-querying
description: Use when after cleaning and clustering LC-MS features in MS-CleanR, when you need to assign putative compound identities to a feature set with MS/MS spectra, and when candidate compounds may exist across multiple specialized databases (e.g., natural products, pharmaceuticals, contaminants).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_2258
  tools:
  - MS-CleanR
  - MS-FINDER
  - MS-DIAL
  techniques:
  - LC-MS
  - NMR
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-database-structure-querying

## Summary

Query multiple metabolite structure databases simultaneously via MS-FINDER to annotate LC-MS features using hydrogen rearrangement rules (HRR) scoring. This skill enables parallel, database-agnostic compound identification from cleaned and clustered MS-DIAL peak lists, with consolidation of per-feature annotations into a unified table ranked by user-defined database priority.

## When to use

After cleaning and clustering LC-MS features in MS-CleanR, when you need to assign putative compound identities to a feature set with MS/MS spectra, and when candidate compounds may exist across multiple specialized databases (e.g., natural products, pharmaceuticals, contaminants). Use this skill when you want to leverage HRR-based scoring to rank structural candidates and compare results across databases rather than querying a single database sequentially.

## When NOT to use

- Input features lack MS/MS spectra — MS-CleanR will discard all features without MS/MS during the first filtering step, and MS-FINDER requires fragmentation data for in silico annotation.
- Data were acquired in MS1-only mode (no tandem MS) — the HRR scoring system and database querying depend on fragmentation patterns.
- You have already committed to a single reference database and do not need candidate ranking or cross-database comparison.

## Inputs

- MS-CleanR-filtered and clustered LC-MS feature set with m/z, retention time, and MS/MS spectra
- MS-FINDER–compatible input format (feature table with spectral data)
- Configuration file or parameters specifying target databases and HRR scoring settings

## Outputs

- Unified annotation table per feature (compound ID, HRR score, database source, structural predictions)
- Merged feature table with annotations prioritized by user-defined database rank
- Optional .msp file for mass spectral networking

## How to apply

Export the selected feature set (m/z, retention time, MS/MS spectra) from MS-CleanR in MS-FINDER–compatible format. Configure MS-FINDER annotation parameters to enable the hydrogen rearrangement rules (HRR) scoring system and specify multiple target databases for querying in a single batch run. Execute MS-FINDER in silico annotation on the exported features. Parse and consolidate all per-feature annotation results (compound ID, HRR score, database match, structural predictions) into a unified annotation table. Merge annotation results back to the filtered peak list by prioritizing database hits according to user-defined ranking criteria (e.g., highest HRR score, preferred database order). Optionally export consolidated results as .msp file for mass spectral similarity networking.

## Related tools

- **MS-FINDER** (Executes in silico annotation using HRR scoring and queries multiple metabolite structure databases; version 3.30 or higher required) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Generates filtered and clustered feature set as input; exports feature data to MS-FINDER–compatible format and consolidates annotation results post-querying) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Upstream peak detection and MS/MS spectral extraction; version 4.00 or higher required; generates peak lists consumed by MS-CleanR) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- Every feature in the input set receives at least one HRR-scored annotation with a database source label; no features are silently dropped.
- Per-feature annotation records include compound ID, HRR score, database source, and structural predictions; no field is missing or null for matched features.
- Database prioritization ranking is consistently applied across all features (e.g., a user-specified database always ranks first when present, or highest HRR score always wins ties).
- Merged feature table row count matches input feature count (or documents any intentional exclusions, e.g., unmatched features).
- Optional .msp export file parses without syntax errors and contains spectral entries matching the consolidated annotation count.

## Limitations

- Requires at least MS-DIAL v4.00 and MS-FINDER v3.30 or higher; newer MS-DIAL 5.x integration may supersede this workflow as MS-CleanR is no longer actively maintained.
- All features without MS/MS spectra are discarded in the first MS-CleanR filtering step; MS1-only data will cause a crash.
- At least 3 blank and 3 QC samples must be identified in the MS-DIAL sample list for proper blank ratio analysis during feature cleaning.
- Sample and class names must not contain spaces, hyphens, or single-letter class identifiers, or the workflow will fail.
- Known bug in R > 4.2: 'Error: the condition has length > 1' encountered during database annotation merging; workaround or R version downgrade required.
- HRR scoring provides in silico predictions; annotations are not validated against experimental standards and should be confirmed by orthogonal methods (e.g., high-resolution MS, authentic standards, NMR).

## Evidence

- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried"
- [readme] The final step will merge annotation results to the filtered peak list by prioritizing database annotation depending on user choice.: "The final step will merge annotation results to the filtered peak list by prioritizing database annotation depending on user choice."
- [other] MS-CleanR exports selected features to MS-FINDER for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system, with capability to query multiple databases at this step.: "MS-CleanR exports selected features to MS-FINDER for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system, with capability to query multiple databases at this step."
- [other] Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table.: "Parse MS-FINDER results and consolidate per-feature annotations (compound ID, score, database match, structural predictions) into a unified annotation table."
- [readme] All these options are tunable by the user.: "All these options are tunable by the user."
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Optionally, all results can be exported as .msp file for mass spectral similarity networking purpose.: "Optionally, all results can be exported as .msp file for mass spectral similarity networking purpose."
