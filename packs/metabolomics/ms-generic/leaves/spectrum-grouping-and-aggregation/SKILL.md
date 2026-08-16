---
name: spectrum-grouping-and-aggregation
description: Use when you have loaded raw PSM search results from a proteomics search engine (e.g., MaxQuant, MSGFPlus, Sage) and need to prepare them for multi-rank rescoring in MS²Rescore.
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

# spectrum-grouping-and-aggregation

## Summary

Group peptide-spectrum matches (PSMs) by their spectrum identifier, then sort and filter candidate PSMs per spectrum according to search engine score and rank thresholds (max_psm_rank_input and max_psm_rank_output). This enables rank-controlled rescoring input selection and output filtering to preserve FDR validity across multiple candidate identifications per spectrum.

## When to use

Apply this skill when you have loaded raw PSM search results from a proteomics search engine (e.g., MaxQuant, MSGFPlus, Sage) and need to prepare them for multi-rank rescoring in MS²Rescore. Use it specifically when: (1) you want to retain and rescore multiple candidate PSMs per spectrum (not just the top-1 hit), (2) you need to control how many candidates feed into rescoring (via max_psm_rank_input) and how many are output before FDR calculation (via max_psm_rank_output), or (3) you are handling chimeric spectra or want to evaluate lower-ranking PSMs that may improve after rescoring.

## When NOT to use

- Input PSM file has already been FDR-filtered or top-1 truncated by the search engine or a prior workflow step; MS²Rescore requires access to all target and decoy PSMs without FDR-filtering.
- Spectrum identifiers in the PSM file cannot be mapped to spectrum files using the provided spectrum_id_pattern or spectrum ID extraction regex; grouping will fail or produce misaligned groups.
- You only care about top-1 hits per spectrum and do not need to rescore multiple candidates; simpler rank-1 filtering suffices.

## Inputs

- PSM file (search engine output in psm_utils-supported format: .mzid, .tsv, .csv, .xml, or .msf)
- Spectrum file (mzML or mgf) for optional per-spectrum metadata
- Configuration parameters: max_psm_rank_input, max_psm_rank_output, spectrum_id_pattern or id_decoy_pattern

## Outputs

- Grouped and sorted PSM table with rank assignments per spectrum
- Filtered PSM subset (up to max_psm_rank_input) ready for rescoring feature generation
- Final output TSV with up to max_psm_rank_output PSMs per spectrum with preserved ranks and rescored metrics

## How to apply

Load all target and decoy PSM entries from the search engine output file using psm_utils, preserving FDR-unfiltered results. Group PSMs by spectrum identifier (extracted via a regex pattern or direct PSM field). Within each spectrum group, sort PSMs by search engine score using the lower_score_is_better flag (or its inverse) to establish a rank order. Select up to max_psm_rank_input PSMs per spectrum (default 10) as candidates for downstream rescoring feature generation and model input. After rescoring completes, re-sort each spectrum's PSMs by the new rescored metric. Finally, filter output to retain only up to max_psm_rank_output PSMs per spectrum (default 1) before applying FDR calculation, ensuring that lower-ranking PSMs do not bias FDR estimates while still allowing chimeric or multi-hit spectra to be represented.

## Related tools

- **MS²Rescore** (Main platform orchestrating PSM grouping, rescoring, and output filtering; implements rank-based filtering logic using max_psm_rank_input and max_psm_rank_output parameters) — https://github.com/compomics/ms2rescore
- **psm_utils** (Library for parsing and grouping PSMs from multiple search engine formats (MaxQuant, MSGFPlus, Sage, etc.) into unified PSM objects keyed by spectrum identifier)
- **Mokapot** (Optional rescoring engine that accepts grouped PSM candidates and produces rescored metrics for re-ranking within spectrum groups)
- **Percolator** (Optional rescoring engine that accepts grouped PSM candidates and produces rescored metrics for re-ranking within spectrum groups) — https://github.com/percolator/percolator/releases/latest

## Evaluation signals

- All PSMs are grouped by spectrum identifier with no orphaned PSMs or missing spectrum assignments.
- Within each spectrum group, PSMs are ranked consistently by search engine score (ascending if lower_score_is_better=true, descending otherwise); confirm via spot-check of top-3 PSMs per spectrum.
- Exactly min(max_psm_rank_input, number_of_candidates_per_spectrum) PSMs are selected per spectrum for rescoring input; count histogram shows no spectrum with more than max_psm_rank_input candidates.
- After rescoring, PSMs are re-ranked by rescored metric and filtered to exactly min(max_psm_rank_output, surviving_candidates) per spectrum in output TSV; verify by inspecting rank column distribution.
- All target and decoy PSMs are preserved during grouping (not pre-filtered); confirm by comparing input file record count to grouped PSM total before and after filtering steps.

## Limitations

- Grouping relies on accurate spectrum_id_pattern regex; if spectrum IDs in the PSM file do not match the pattern, PSMs will not group correctly or will be orphaned.
- The max_psm_rank_output parameter must be chosen to preserve sufficient decoy PSMs for reliable FDR calculation; setting it too low may underestimate FDR due to loss of decoy statistics.
- Performance may degrade with very large PSM files (millions of PSMs) or spectra with unusually high candidate counts (>100 PSMs per spectrum); grouping and sorting are O(N log N) per spectrum.
- Chimeric spectra with multiple unrelated peptides require manual review; the filtering step may suppress lower-ranking correct hits if they fall below max_psm_rank_output, leading to missed identifications.

## Evidence

- [other] MS²Rescore implements rank-based filtering using two configuration parameters: max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring (e.g., top 5 PSMs), while max_psm_rank_output filters lower-ranking PSMs before final FDR calculation and output writing to ensure correct FDR control: "MS²Rescore implements rank-based filtering using two configuration parameters: max_psm_rank_input controls how many candidate PSMs per spectrum are included for rescoring (e.g., top 5 PSMs), while"
- [other] Load PSM file and parse all target and decoy PSM entries using psm_utils, grouping by spectrum identifier. For each spectrum, sort PSMs by search engine score (lower is better if lower_score_is_better flag is true, otherwise higher is better). Select up to max_psm_rank_input PSMs per spectrum (default 10) as input candidates for downstream rescoring feature generation and model application.: "Load PSM file and parse all target and decoy PSM entries using psm_utils, grouping by spectrum identifier. For each spectrum, sort PSMs by search engine score (lower is better if"
- [intro] MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**: "MS²Rescore always needs access to **all target and decoy PSMs, without any FDR-filtering**"
- [intro] MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring: "MS²Rescore can rescore multiple candidate PSMs per spectrum. This allows for lower-ranking candidate PSMs to become the top-ranked PSM after rescoring"
- [intro] To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation: "To ensure a correct FDR control after rescoring, MS²Rescore filters out lower-ranking PSMs before final FDR calculation"
