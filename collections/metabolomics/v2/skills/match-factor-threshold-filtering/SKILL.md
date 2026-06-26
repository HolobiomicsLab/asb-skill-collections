---
name: match-factor-threshold-filtering
description: Use when you have a GC-MS dataset with Match.Factor scores for each detected
  compound (output from Agilent Unknowns Analysis or equivalent), and you want to
  reduce the number of query chemicals passed to computationally intensive cheminformatics
  functions (categorate, mzExacto, or exactoThese).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - R
  - spreadOut()
  - mzExacto()
  - uafR
  - Agilent Unknowns Analysis
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
- The first step in the process is to convert the raw input to a format that downstream
  functions can work with. `spreadOut()` prepares the read in .CSV for intelligent
  ***sorting*** (using retention
- '`mzExacto()` collects the same information for a set of query chemicals and uses
  it to precisely search the advanced dictionary for samples that have those chemicals.'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_uafr_cq
    doi: 10.1371/journal.pone.0306202
    title: uafr
  dedup_kept_from: coll_uafr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pone.0306202
  all_source_dois:
  - 10.1371/journal.pone.0306202
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# match-factor-threshold-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Subset gas chromatography–mass spectrometry (GC-MS) compound identifications by Match.Factor score to reduce computational burden and focus downstream cheminformatics analysis on high-confidence hits. This filtering step narrows the search space before expensive operations like categorate() or mzExacto() are applied.

## When to use

You have a GC-MS dataset with Match.Factor scores for each detected compound (output from Agilent Unknowns Analysis or equivalent), and you want to reduce the number of query chemicals passed to computationally intensive cheminformatics functions (categorate, mzExacto, or exactoThese). Apply this filter when you have >10 compounds or when you want to focus on only high-confidence identifications (typically Match.Factor ≥ 70–89).

## When NOT to use

- Input data is already curated or hand-selected; filtering by score is redundant.
- Your analysis requires all detected compounds, including low-confidence hits, for downstream statistical power or completeness.
- The GC-MS dataset does not include a Match.Factor column or lacks standardized scoring (use other validation criteria first).

## Inputs

- GC-MS dataset as .CSV with required columns: 'Match.Factor', 'Compound.Name', 'Component.RT', 'Component.Area', 'Base.Peak.MZ', 'File.Name'
- Numeric threshold value (e.g., 70, 80, or 89)

## Outputs

- Filtered character vector of Compound.Name values (query_chemicals)
- Optionally, a filtered data frame retaining only rows meeting the Match.Factor threshold

## How to apply

After loading your GC-MS .CSV file (which must contain the 'Match.Factor' and 'Compound.Name' columns), use logical subsetting to retain only rows where Match.Factor exceeds your chosen threshold. The task card and README examples demonstrate thresholds of >70, >80, and >89, depending on confidence requirements and false-positive tolerance. Extract the filtered Compound.Name vector as your query_chemicals list. Pass this reduced set to downstream functions (mzExacto, categorate, exactoThese) to avoid processing low-confidence identifications that may introduce noise. The choice of threshold should reflect the specificity demands of your analysis: use ≥89 for explicit query validation (as in the task), ≥80 for exploratory enrichment, and ≥70 for broad screening.

## Related tools

- **uafR** (R package providing mzExacto(), categorate(), and exactoThese() functions that consume filtered query_chemicals; the Match.Factor threshold filter is a prerequisite step to narrow input to these functions.) — https://github.com/castratton/uafR
- **Agilent Unknowns Analysis** (Generates the GC-MS .CSV file with Match.Factor scores for all detected compounds; output format is the input to this filtering skill.) — https://www.agilent.com/cs/library/usermanuals/public/G3335-901

## Examples

```
query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 89]; input_exacto = mzExacto(input_spread, query_chemicals)
```

## Evaluation signals

- The resulting query_chemicals vector contains only compound names whose Match.Factor values exceed your stated threshold (e.g., all values ≥89 for explicit validation).
- The cardinality of query_chemicals is smaller than the original Compound.Name column, confirming subsetting occurred.
- Downstream functions (mzExacto, categorate, exactoThese) complete without errors and produce results only for the filtered compounds.
- Visual inspection of the filtered dataset confirms removal of expected low-confidence hits (e.g., Match.Factor 62.6, 68.8 in the README example are excluded when threshold is ≥70).
- Reported Match.Factor values in final mzExacto output (e.g., Octanal: 99.32, Methyl salicylate: 98.16) all meet or exceed the chosen threshold.

## Limitations

- Match.Factor is instrument and method-dependent; thresholds that work for one GC-MS platform may not generalize. Validate threshold choice against your instrument's historical false-positive rate.
- Filtering may discard true positives with marginally lower scores (e.g., 89.5 if threshold is exactly 90); use domain knowledge or ROC analysis to set thresholds conservatively.
- Does not account for compound-specific match quality factors (e.g., spectral library coverage, isomer ambiguity); a uniform threshold may over-filter rare compounds or under-filter common contaminants.

## Evidence

- [methods] The filter step and its parameters as described in the article extraction.: "a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()` is to first subset by match factor: `query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >=`"
- [readme] README example showing ≥80 threshold for exploratory filtering.: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]"
- [readme] README example showing ≥70 threshold for broader screening.: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 70]"
- [other] Task card specifying ≥89 threshold for high-confidence validation.: "reported best-match factors (Octanal: 99.32, Ethyl hexanoate: 99.35, Methyl salicylate: 98.16, Undecane: 98.68)"
- [methods] Purpose of filtering: reduce downstream computational burden.: "a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()`"
