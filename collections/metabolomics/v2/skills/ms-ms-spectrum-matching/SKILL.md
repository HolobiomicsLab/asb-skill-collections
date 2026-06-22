---
name: ms-ms-spectrum-matching
description: Use when you have a cleaned and clustered set of LC-MS features (m/z, retention time, MS/MS spectra) from MS-CleanR output and need to assign putative compound identities by matching observed MS/MS fragmentation patterns against reference spectral libraries using HRR-based scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3094
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MS-CleanR
  - MS-FINDER
  - MS-DIAL
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS spectrum matching

## Summary

Export filtered LC-MS features to MS-FINDER for in silico annotation using hydrogen rearrangement rules (HRR) scoring and multi-database querying to assign compound identities to detected metabolites. This skill bridges MS-CleanR's feature curation with MS-FINDER's spectral library matching to produce annotated compound tables.

## When to use

You have a cleaned and clustered set of LC-MS features (m/z, retention time, MS/MS spectra) from MS-CleanR output and need to assign putative compound identities by matching observed MS/MS fragmentation patterns against reference spectral libraries using HRR-based scoring. Apply this when your data contain MS/MS spectra (DDA or DIA mode) and you want structure-informed predictions ranked by database match confidence.

## When NOT to use

- Input contains only MS1 spectra with no MS/MS fragmentation data—MS-FINDER requires MS/MS for annotation and will crash
- Data were acquired in MS1-only mode without data-dependent or data-independent MS/MS collection
- Feature table already contains validated compound identities from orthogonal methods; re-annotation may introduce conflicting annotations

## Inputs

- MS-CleanR-filtered and clustered feature table (CSV or R data frame with m/z, retention time, MS/MS spectra)
- MS/MS spectral data in MS-FINDER compatible format (.msp or vendor-specific formats)
- MS-FINDER configuration file specifying HRR scoring parameters and database selections

## Outputs

- MS-FINDER annotation results (per-feature compound IDs, HRR scores, database source, structural class predictions)
- Merged annotation table (filtered peak list enriched with compound annotations, prioritized by database and score)
- Optional .msp file for mass spectral similarity networking

## How to apply

Load the cleaned feature set from MS-CleanR (output of prior filtering and clustering steps). Format feature data (m/z, retention time, MS/MS spectra) into MS-FINDER compatible input format. Configure MS-FINDER annotation parameters, enabling the hydrogen rearrangement rules (HRR) scoring system and selecting multiple database targets (e.g., NIST, MassBank, custom databases). Execute MS-FINDER in silico annotation on the exported features. Parse MS-FINDER results and consolidate per-feature annotations (compound ID, HRR score, database match, structural predictions) into a unified annotation table, prioritizing database matches by user-defined criteria.

## Related tools

- **MS-FINDER** (Performs in silico spectral library matching using hydrogen rearrangement rules (HRR) scoring system and queries multiple databases to assign compound identities to MS/MS spectra) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Upstream tool that filters and clusters LC-MS features and exports them in MS-FINDER-compatible format for annotation) — https://github.com/eMetaboHUB/MS-CleanR
- **MS-DIAL** (Generates initial peak lists from LC-MS raw data (DDA or DIA mode) that serve as input to MS-CleanR filtering, which then feeds MS-FINDER annotation) — http://prime.psc.riken.jp/compms/index.html

## Evaluation signals

- All selected features from MS-CleanR are successfully exported to MS-FINDER and produce at least one annotation per feature (no null or missing compound IDs)
- HRR scores and database match source are recorded for each annotation, enabling prioritization and confidence assessment
- Merged annotation table contains no duplicate compound assignments to the same feature unless explicitly retained for alternate matches
- Annotations are consistent with expected m/z and fragmentation patterns (spot-check a subset against known standards or chemical databases)
- Optional .msp export file is valid and can be imported into mass spectral networking tools without format errors

## Limitations

- MS-FINDER requires MS/MS spectra; features without MS/MS fragmentation will be discarded during the first MS-CleanR step and cannot be annotated
- Annotation quality depends on spectral library coverage and database currency; rare or novel metabolites may not match any reference
- Hydrogen rearrangement rules (HRR) scoring is empirical and may rank false-positive matches highly if libraries contain noisy spectra
- MS-CleanR versions after active development (README states tool is no longer maintained since MS-DIAL 5.x integration) may not be compatible with newer MS-FINDER releases
- Known R version incompatibility: 'Error: the condition has length > 1' encountered during database annotation merging if using R > 4.2

## Evidence

- [readme] all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried: "all selected features are exported to MS-FINDER program for in silico-based annotation using hydrogen rearrangement rules (HRR) scoring system. At this step, multiple databases can be queried"
- [readme] MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis (DDA) or data independent analysis (DIA): "MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis (DDA) or data independent analysis (DIA)"
- [other] Format feature data (m/z, retention time, MS/MS spectra) into MS-FINDER compatible input format. Configure MS-FINDER annotation parameters including hydrogen rearrangement rules (HRR) scoring system and select multiple database targets for querying. Execute MS-FINDER in silico annotation on the exported features.: "Format feature data (m/z, retention time, MS/MS spectra) into MS-FINDER compatible input format. Configure MS-FINDER annotation parameters including hydrogen rearrangement rules (HRR) scoring system"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher): "Needs MS-DIAL (v4.00 or higher) and MS-FINDER (3.30 or higher)"
