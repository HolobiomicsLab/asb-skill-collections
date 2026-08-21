---
name: candidate-psm-cardinality-control
description: Use when when rescoring PSMs from a search engine with MS²Rescore and
  you need to (1) constrain computational cost by reducing the number of candidates
  fed to feature generators and rescoring engines, (2) control false discovery rate
  correctly by removing lower-ranking PSMs before final statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  tools:
  - MS²Rescore
  - psm_utils
  - Mokapot
  - Percolator
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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

# Candidate PSM Cardinality Control

## Summary

Apply rank-based filtering to limit the number of candidate peptide-spectrum matches (PSMs) per spectrum at two distinct stages: input (for rescoring feature generation) and output (before FDR calculation). This dual-stage filtering ensures efficient rescoring while maintaining correct false discovery rate control.

## When to use

When rescoring PSMs from a search engine with MS²Rescore and you need to (1) constrain computational cost by reducing the number of candidates fed to feature generators and rescoring engines, (2) control false discovery rate correctly by removing lower-ranking PSMs before final statistical calculations, or (3) handle chimeric spectra where multiple valid peptide identifications exist per spectrum but only top-ranked results should be reported.

## When NOT to use

- Input PSM file is already FDR-filtered; MS²Rescore requires access to all target and decoy PSMs without any FDR-filtering applied beforehand.
- You have no need to rescore PSMs; cardinality control is specific to the rescoring workflow and adds complexity without benefit in search-only pipelines.
- Spectrum files are unavailable or unlinked to PSM entries; feature generation for rescoring requires valid spectrum ID mapping.

## Inputs

- PSM file from proteomics search engine (e.g., MaxQuant msms.txt, MSGFPlus .mzid, Mascot .mzid, MS Amanda .csv)
- Spectrum file (mzML or mgf format) — required for feature generation
- Configuration parameters: max_psm_rank_input, max_psm_rank_output, lower_score_is_better flag, decoy identification pattern (id_decoy_pattern or protein name prefix)

## Outputs

- Filtered PSM table (TSV format) with all retained PSMs and their ranks, grouped by spectrum
- Rank assignments per PSM (1, 2, 3, ...) within each spectrum
- Subset of PSMs meeting cardinality constraints for FDR calculation

## How to apply

Load all target and decoy PSM entries from the search engine output (without prior FDR filtering) using psm_utils, grouping by spectrum identifier. For each spectrum, sort PSMs by the search engine score (applying the lower_score_is_better flag if necessary). Filter to retain up to max_psm_rank_input PSMs per spectrum (default 10) as candidates for downstream feature generation and model rescoring. After rescoring completes, re-sort PSMs by the rescored metric for each spectrum, then filter to retain up to max_psm_rank_output PSMs per spectrum (default 1) before applying FDR calculation. The rationale is that input filtering reduces computational burden without affecting FDR control, while output filtering ensures that lower-ranking PSMs (which may have been boosted by rescoring in chimeric spectra) do not violate FDR assumptions during statistical tests.

## Related tools

- **MS²Rescore** (Primary rescoring platform that implements rank-based filtering at input and output stages) — https://github.com/compomics/ms2rescore
- **psm_utils** (PSM file parser and grouper; used to load, parse, and organize target and decoy PSM entries by spectrum identifier) — https://github.com/compomics/psm_utils
- **Mokapot** (Rescoring engine supported by MS²Rescore; receives rank-filtered input PSMs and produces rescored metrics)
- **Percolator** (Rescoring engine supported by MS²Rescore; receives rank-filtered input PSMs and produces rescored metrics) — https://github.com/percolator/percolator/releases/latest

## Examples

```
ms2rescore config.json --max_psm_rank_input 10 --max_psm_rank_output 1
```

## Evaluation signals

- Each spectrum in the output PSM table contains ≤ max_psm_rank_output PSMs, verified by counting rows per spectrum identifier.
- PSMs are sorted by rescored metric within each spectrum and assigned consecutive ranks (1, 2, 3, ...) in rank column.
- Input feature generation received ≤ max_psm_rank_input PSMs per spectrum; downstream rescoring engines processed this constrained set.
- FDR calculation results remain statistically valid; lower-ranking PSMs removed before statistical tests do not inflate false positive rates.
- Chimeric spectra with multiple valid peptides retain their top-1 ranked PSM (if max_psm_rank_output=1) while lower-ranking candidates are excluded from final output.

## Limitations

- Setting max_psm_rank_input too low (e.g., 1–2) may exclude valid alternative PSMs and reduce rescoring benefit, especially for chimeric or ambiguous spectra.
- Setting max_psm_rank_output to 1 enforces single-PSM reporting per spectrum, which may discard valid co-identifications for spectra with genuinely ambiguous peptide assignments.
- The lower_score_is_better flag must be set correctly for each search engine; incorrect orientation can lead to inverted ranking and removal of top-scoring candidates.
- Decoy identification pattern (id_decoy_pattern or protein name prefix) must match the search engine's decoy labeling scheme; mismatched patterns cause decoy PSMs to be treated as targets or vice versa, violating FDR control.

## Evidence

- [other] max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring: "max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring (e.g., top 5 PSMs)"
- [other] max_psm_rank_output filters lower-ranking PSMs before final FDR calculation: "max_psm_rank_output filters lower-ranking PSMs before final FDR calculation and output writing to ensure correct FDR control"
- [intro] MS²Rescore requires access to all target and decoy PSMs without FDR-filtering: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] MS²Rescore supports rescoring of multiple candidate PSMs per spectrum, allowing lower-ranking candidates to become top-ranked after rescoring: "MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring"
- [other] Two-stage rank filtering: input candidates sorted by search engine score, output candidates sorted by rescored metric: "For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better). Select up to max_psm_rank_input PSMs per spectrum (default 10)"
- [other] PSM grouping by spectrum identifier using psm_utils: "Load PSM file and parse all target and decoy PSM entries using psm_utils, grouping by spectrum identifier"
- [intro] FDR control rationale for output filtering: "To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation"
