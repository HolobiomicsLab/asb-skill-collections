---
name: fdr-aware-psm-retention-strategy
description: 'Use when rescoring PSMs with machine learning or statistical models
  where: (1) you want to consider multiple candidate PSMs per spectrum (e.'
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
  techniques:
  - mass-spectrometry
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

# FDR-aware PSM retention strategy

## Summary

A rank-based filtering strategy that retains multiple candidate PSMs per spectrum during rescoring input but selectively removes lower-ranking PSMs before final FDR calculation to preserve statistical validity. This approach enables consideration of chimeric spectra and lower-ranking candidates during feature generation while ensuring correct FDR control in the final output.

## When to use

Apply this skill when rescoring PSMs with machine learning or statistical models where: (1) you want to consider multiple candidate PSMs per spectrum (e.g., chimeric spectra with overlapping peptide signals), (2) you need to maintain FDR control at PSM, peptide, or protein level after rescoring, and (3) lower-ranking PSMs may become top-ranked after rescoring and should not artificially inflate false discovery rates. Specifically use when configuring MS²Rescore or similar rescoring pipelines with max_psm_rank_input > max_psm_rank_output.

## When NOT to use

- Input is already FDR-filtered or contains only top-ranked PSMs per spectrum—MS²Rescore requires all target and decoy PSMs without FDR-filtering to enable proper rescoring.
- Single PSM per spectrum only or no multi-rank candidate pool exists—the strategy requires multiple candidates per spectrum to provide benefit; use standard single-rank filtering instead.
- You do not need to maintain FDR control (e.g., exploratory analysis only)—the added complexity of dual-threshold filtering is unnecessary if statistical rigor is not a requirement.

## Inputs

- All target and decoy PSM identifications from search engine (ungrouped, unsorted, no prior FDR filtering)
- Spectrum identifiers used to group PSMs
- Search engine scores for each PSM
- Spectrum files (mzML or mgf format) for some feature generators
- Rescored metric or score for each PSM after model application

## Outputs

- Filtered PSM table (TSV) with up to max_psm_rank_output PSMs retained per spectrum
- PSM rank assignments per spectrum
- FDR-corrected PSM, peptide, and protein-level statistics

## How to apply

Configure two rank thresholds: max_psm_rank_input (e.g., top 5–10 PSMs per spectrum) to include candidate PSMs for rescoring feature generation, and max_psm_rank_output (e.g., 1) to filter the output before FDR calculation. Load all target and decoy PSMs without FDR-filtering, group by spectrum identifier, and sort by search engine score. Select up to max_psm_rank_input PSMs as input to downstream rescoring. After rescoring, re-sort PSMs by the new rescored metric, then retain only up to max_psm_rank_output PSMs per spectrum before FDR calculation and TSV output. This two-stage filtering ensures lower-ranking PSMs are considered during machine learning feature generation (where they may improve model calibration) but removed before FDR correction (where they would otherwise be misclassified as true discoveries).

## Related tools

- **MS²Rescore** (Modular rescoring platform that implements dual-threshold PSM filtering (max_psm_rank_input and max_psm_rank_output) and FDR control) — https://github.com/compomics/ms2rescore
- **psm_utils** (Python library for parsing PSM files from diverse search engines and grouping by spectrum identifier) — https://github.com/compomics/ms2rescore
- **Mokapot** (Machine learning rescoring engine supported by MS²Rescore; operates on input PSMs and produces rescored metrics)
- **Percolator** (Statistical rescoring engine supported by MS²Rescore; alternative to Mokapot for PSM re-ranking) — https://github.com/percolator/percolator

## Examples

```
ms2rescore --config config.toml --psm_file search_results.mzid --spectrum_file data.mzML --max_psm_rank_input 10 --max_psm_rank_output 1
```

## Evaluation signals

- Verify max_psm_rank_input is ≥ max_psm_rank_output: input threshold must be equal to or larger than output threshold to enable meaningful filtering.
- Confirm output TSV contains ≤ max_psm_rank_output PSMs per spectrum; count distinct PSMs grouped by spectrum ID and verify no spectrum exceeds the threshold.
- Check that FDR control is preserved: compare PSM-, peptide-, and protein-level FDR estimates in output to independent FDR calculation (e.g., via Mokapot or Percolator) on the same filtered PSM set; results should match within rounding error.
- Validate that lower-ranking PSMs improved after rescoring: spot-check a sample of PSMs that were rank 2–max_psm_rank_input in search engine output but dropped below max_psm_rank_output after rescoring; confirm their rescored scores are genuinely worse than retained PSMs.
- Audit input completeness: verify input PSM file contained all target and decoy PSMs from search engine (no pre-filtering); count total PSMs before and after filtering to ensure no unexpected loss at intermediate steps.

## Limitations

- Requires access to all unfiltered target and decoy PSM identifications; if the PSM file is already FDR-filtered or truncated, correct FDR control cannot be guaranteed downstream.
- Performance depends on quality of rescoring model: if the rescoring engine produces poorly calibrated scores, lower-ranking PSMs may not be properly re-ranked, and the dual-threshold strategy will not recover true discoveries.
- Chimeric spectra with overlapping peptide signals may still be mishandled if max_psm_rank_input is too small or if the rescoring model does not adequately penalize spurious matches; tuning these parameters requires empirical validation on data with known ground truth.
- Decoy identification must be accurate: if decoy PSMs are incorrectly labeled (using id_decoy_pattern or protein name prefix), FDR estimates will be biased regardless of filtering strategy applied.

## Evidence

- [other] max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring (e.g., top 5 PSMs), while max_psm_rank_output filters lower-ranking PSMs before final FDR calculation: "max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring (e.g., top 5 PSMs), while max_psm_rank_output filters lower-ranking PSMs before final FDR calculation and"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [other] Select up to max_psm_rank_input PSMs per spectrum as input candidates for downstream rescoring feature generation and model application. After rescoring completes, re-sort PSMs by rescored metric for each spectrum. Filter output to retain up to max_psm_rank_output PSMs per spectrum before final FDR calculation.: "Select up to max_psm_rank_input PSMs per spectrum (default 10) as input candidates for downstream rescoring feature generation and model application. After rescoring completes, re-sort PSMs by"
- [intro] To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation: "To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation"
- [intro] MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring: "MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring"
