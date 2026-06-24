---
name: psm-score-sorting-and-ranking
description: Use when when you have grouped PSMs by spectrum identifier and need to
  (1) establish input candidate PSMs for rescoring by selecting top-ranked PSMs based
  on search engine score, or (2) re-rank PSMs after rescoring completes to select
  final output PSMs for FDR calculation and result writing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS²Rescore
  - psm_utils
  - Mokapot
  - Percolator
  license_tier: open
derived_from:
- doi: 10.1002/pmic.202300336
  title: MS2Rescore (immunopeptidome rescoring)
evidence_spans:
- MS²Rescore is a tool for rescoring peptide-spectrum matches
- Accepted ProForma modification labels in :py:mod:`psm_utils`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2rescore_immunopeptidome_rescoring_cq
    doi: 10.1002/pmic.202300336
    title: MS2Rescore (immunopeptidome rescoring)
  dedup_kept_from: coll_ms2rescore_immunopeptidome_rescoring_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/pmic.202300336
  all_source_dois:
  - 10.1002/pmic.202300336
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# PSM Score Sorting and Ranking

## Summary

Sort peptide-spectrum matches (PSMs) by search engine or rescored metric and assign rank positions per spectrum to enable rank-based filtering and output selection in proteomics rescoring workflows. This skill ensures consistent rank ordering before and after rescoring, and underpins downstream filtering decisions that control FDR.

## When to use

When you have grouped PSMs by spectrum identifier and need to (1) establish input candidate PSMs for rescoring by selecting top-ranked PSMs based on search engine score, or (2) re-rank PSMs after rescoring completes to select final output PSMs for FDR calculation and result writing. Specifically, use this skill before applying max_psm_rank_input filtering (input stage) and after rescoring completes (output stage).

## When NOT to use

- PSM file is already FDR-filtered by the search engine; MS²Rescore requires all target and decoy PSMs without pre-filtering
- Input PSMs are not yet grouped by spectrum identifier; rank sorting assumes spectrum-level grouping
- No valid search engine score or rescored metric is available in the PSM records

## Inputs

- Grouped PSM collection indexed by spectrum identifier
- Search engine PSM scores (input stage) or rescored metric values (output stage)
- lower_score_is_better boolean flag indicating sort direction
- max_psm_rank_input parameter (default 10, for input-stage filtering)
- max_psm_rank_output parameter (default 1, for output-stage filtering)

## Outputs

- Rank-sorted PSM collection per spectrum with assigned rank positions
- Filtered PSM subset containing up to max_psm_rank_input or max_psm_rank_output PSMs per spectrum
- Annotated PSM table with rank column for each PSM

## How to apply

For each spectrum, sort PSMs by their scoring metric—using the search engine score at input stage or the rescored metric at output stage. Determine sort direction by checking the lower_score_is_better flag: if true, sort ascending (lower scores rank higher); if false, sort descending (higher scores rank higher). Assign rank positions starting from 1 for the top-ranked PSM. These ranks are then used to filter PSMs: retain up to max_psm_rank_input PSMs (default 10) for rescoring feature generation, and later filter to up to max_psm_rank_output PSMs (default 1) before FDR calculation. Rank assignment must be stable and reproducible across runs to ensure correct FDR control.

## Related tools

- **MS²Rescore** (Orchestrates PSM rank sorting at input and output stages; applies max_psm_rank_input and max_psm_rank_output filtering based on rank positions) — https://github.com/compomics/ms2rescore
- **psm_utils** (Parses PSM files from diverse search engines and groups PSMs by spectrum identifier before rank sorting) — https://github.com/compomics/psm_utils
- **Mokapot** (Rescoring engine whose output scores are re-sorted per spectrum to assign new rank positions for output filtering)
- **Percolator** (Rescoring engine whose output scores are re-sorted per spectrum to assign new rank positions for output filtering) — https://github.com/percolator/percolator

## Evaluation signals

- Verify that all PSMs within each spectrum are sorted by their metric (ascending if lower_score_is_better=true, descending otherwise) with no ties left unresolved
- Confirm rank positions start at 1 for the top-ranked PSM and increment by 1 for each subsequent PSM within the same spectrum
- Check that the number of retained PSMs per spectrum does not exceed max_psm_rank_input at input stage or max_psm_rank_output at output stage
- Validate that re-sorting after rescoring produces a different rank order than input sorting when rescored scores differ from search engine scores
- Ensure FDR calculation uses only PSMs that passed max_psm_rank_output filtering, confirming correct FDR control after rank-based output filtering

## Limitations

- Rank sorting is local to each spectrum; cross-spectrum score comparisons are not performed and may not be meaningful due to varying PSM quality per spectrum
- If lower_score_is_better flag is incorrectly specified, rank order will be inverted, leading to incorrect candidate selection and FDR miscalibration
- Tied scores within a spectrum (identical metric values) may be arbitrarily ordered by the sorting algorithm, potentially causing non-deterministic rank assignment if ties are common
- max_psm_rank_input and max_psm_rank_output parameters are global and apply uniformly across all spectra; no per-spectrum or per-charge-state customization is supported
- Output rank filtering must occur before FDR calculation to ensure statistical validity; filtering after FDR calculation will invalidate FDR thresholds

## Evidence

- [methods] For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better). Select up to max_psm_rank_input PSMs per spectrum (default 10) as input candidates for downstream rescoring feature generation and model application.: "For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better). Select up to max_psm_rank_input PSMs per spectrum (default 10)"
- [methods] After rescoring completes, re-sort PSMs by rescored metric for each spectrum. Filter output to retain up to max_psm_rank_output PSMs per spectrum (default 1) before final FDR calculation.: "After rescoring completes, re-sort PSMs by rescored metric for each spectrum. Filter output to retain up to max_psm_rank_output PSMs per spectrum (default 1) before final FDR calculation."
- [intro] MS²Rescore requires access to all target and decoy PSMs without FDR-filtering: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation: "To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation"
- [intro] MS²Rescore supports rescoring of multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring: "MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring"
