---
name: psm-rank-filtering-input-selection
description: Use when you have a PSM file from a proteomics search engine containing
  multiple candidate identifications per spectrum and need to prepare input for rescoring
  with MS²Rescore. Use it when computational resources are limited or when you want
  to focus rescoring on high-confidence candidates (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
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

# PSM Rank Filtering for Rescoring Input Selection

## Summary

Select a subset of top-ranked candidate PSMs per spectrum for rescoring feature generation and model application, controlled by the max_psm_rank_input parameter. This filtering ensures computationally efficient rescoring while preserving the diversity of candidate identifications needed for accurate FDR control.

## When to use

Apply this skill when you have a PSM file from a proteomics search engine containing multiple candidate identifications per spectrum and need to prepare input for rescoring with MS²Rescore. Use it when computational resources are limited or when you want to focus rescoring on high-confidence candidates (e.g., top 5–10 PSMs per spectrum) while preserving lower-ranking candidates for downstream FDR calculation.

## When NOT to use

- Input PSM file has already been FDR-filtered or pre-filtered at a fixed threshold; MS²Rescore requires all target and decoy PSMs without prior FDR-filtering
- You need to retain all lower-ranking candidate PSMs for direct output (use max_psm_rank_output filtering instead, applied after rescoring)
- Search engine score ordering is unknown or inconsistent across search engines in the input file

## Inputs

- PSM file from search engine (any format supported by psm_utils: MaxQuant, MSGFPlus, Sage, X!Tandem, etc.)
- Spectrum identifier mapping rules or configuration
- max_psm_rank_input parameter value (integer; default 10)
- Search engine score ordering flag (lower_score_is_better: true/false)

## Outputs

- Filtered PSM set grouped by spectrum
- Subset of candidate PSMs per spectrum (up to max_psm_rank_input)
- Rank assignments for retained PSMs within each spectrum

## How to apply

Load the PSM file using psm_utils and group all target and decoy PSMs by spectrum identifier. For each spectrum, sort PSMs by the search engine score (ascending if lower_score_is_better=true, otherwise descending). Retain only the top max_psm_rank_input PSMs (default 10) per spectrum as candidates for downstream rescoring feature generation and model application. Discard lower-ranking PSMs at this stage. This filtered set becomes the input to the rescoring engine (e.g., Mokapot or Percolator). The rationale is to reduce computational cost while ensuring that the best candidate PSMs are rescored; lower-ranking PSMs are re-evaluated post-rescoring using the separate max_psm_rank_output parameter before final FDR calculation.

## Related tools

- **psm_utils** (Parse PSM files from multiple search engines and group by spectrum identifier)
- **MS²Rescore** (Orchestrate PSM filtering, feature generation, and rescoring; apply max_psm_rank_input parameter) — https://github.com/compomics/ms2rescore
- **Mokapot** (Rescoring engine that processes the filtered candidate PSM set)
- **Percolator** (Alternative rescoring engine that processes the filtered candidate PSM set) — https://github.com/percolator/percolator

## Evaluation signals

- Verify that each spectrum retains exactly min(total_psms_for_spectrum, max_psm_rank_input) PSMs after filtering
- Confirm that retained PSMs are the top-ranked according to search engine score (accounting for score direction)
- Check that all retained PSMs have rank ≤ max_psm_rank_input within their spectrum group
- Validate that the filtered PSM set includes both target and decoy PSMs in the correct proportion before passing to rescoring
- Ensure that rank assignments are consistent with the sort order applied (e.g., rank 1 = highest score)

## Limitations

- Setting max_psm_rank_input too low (e.g., 1) may discard genuine alternative identifications and reduce rescoring sensitivity; recommended minimum is 5
- Search engine score direction must be correctly specified (lower_score_is_better flag); if reversed, ranking order will be inverted and incorrect PSMs will be selected
- PSMs with identical scores may be sorted arbitrarily depending on sort stability; tie-breaking behavior should be documented for reproducibility
- Spectrum identifier mapping must be accurate and consistent between PSM file and spectrum file; mismatches result in loss of PSMs or orphaned identifications

## Evidence

- [other] Select up to max_psm_rank_input PSMs per spectrum (default 10) as input candidates for downstream rescoring feature generation and model application.: "Select up to max_psm_rank_input PSMs per spectrum (default 10) as input candidates for downstream rescoring feature generation and model application."
- [other] For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better).: "For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better)."
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring: "MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring"
- [other] Load PSM file and parse all target and decoy PSM entries using psm_utils, grouping by spectrum identifier.: "Load PSM file and parse all target and decoy PSM entries using psm_utils, grouping by spectrum identifier."
