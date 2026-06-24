---
name: spectral-match-score-interpretation
description: 'Use when when you have GC-MS output with Match.Factor values or structural
  similarity scores from categorate() and need to decide which identified compounds
  are reliable enough to carry forward. Specifically: (1) after running GC-MS and
  receiving a Match.Factor column;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - ChemmineR
  - fmcsR
  - webchem
  - R
  - uafR
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pone.0306202
  title: uafr
evidence_spans:
- To perform the chemical structure matches and summarize atomic features, uafR taps
  into an amazing set of cheminformatics packages -- [ChemmineR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html),
  [fmcsR]
- uafR taps into an amazing set of cheminformatics packages -- [ChemmineR](https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html),
  [fmcsR](https://bioconductor.org/packages/release/bioc
- '[fmcsR](https://bioconductor.org/packages/release/bioc/html/fmcsR.html), [webchem](https://cran.r-project.org/web/packages/webchem/index.html)'
- Modern programming languages allow even complex workflows to be automated
- Modern programming languages allow even complex workflows to be automated.
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

# spectral-match-score-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpreting and applying Match.Factor thresholds and structural match scores (>0.95) to filter and validate chemical identifications in GC-MS and cheminformatics workflows. This skill bridges mass spectrometry confidence metrics with structural matching results to establish compound identity with quantifiable confidence.

## When to use

When you have GC-MS output with Match.Factor values or structural similarity scores from categorate() and need to decide which identified compounds are reliable enough to carry forward. Specifically: (1) after running GC-MS and receiving a Match.Factor column; (2) after calling categorate() on query chemicals and receiving best-match tables with structural match scores; (3) when you need to subset compounds for downstream analysis and must choose a confidence threshold that balances specificity (avoiding false positives) with sensitivity (retaining true signals).

## When NOT to use

- Input is already a pre-validated, peer-reviewed compound library or reference standard with certified identities; re-scoring adds no value.
- Match.Factor column is missing or populated with non-numeric values; threshold filtering will fail or produce meaningless results.
- Structural match score is not computed (e.g., categorate() output lacks a numeric score column); you cannot assess confidence and should investigate data preparation.

## Inputs

- GC-MS data frame with required columns: 'Compound.Name', 'Match.Factor', 'Component.RT', 'Base.Peak.MZ', 'Component.Area', 'File.Name'
- Query chemical name list (character vector)
- Chemical library data frame (wide or long format with chemical compound groups)
- Structural similarity threshold (numeric, typically >0.95)

## Outputs

- Filtered query chemical name vector (subset passing Match.Factor or match score threshold)
- Best-match table from categorate() with columns: query chemical name, matched type/group, compound identifier (e.g., 'CMP1', 'CMP2'), match score
- Subset suitable for downstream exactoThese() or mzExacto() calls

## How to apply

Match.Factor thresholds are applied as a pre-filter to narrow search space before categorate() or mzExacto() calls. In the uafR workflow, users first subset input_dat by Match.Factor ≥ a chosen cutoff (e.g., 70 or 80) to extract high-confidence compound names, then pass those names to categorate(). For structural matching, categorate() internally uses fmcsR and ChemmineR to compute match scores against the provided chemical library; scores >0.95 indicate high-confidence best matches (e.g., ethyl hexanoate correctly matched to CMP2). Decisions on threshold depend on the downstream use case: stricter thresholds (≥80) reduce noise but may miss weak signals; looser thresholds (≥70) retain more candidates but increase ambiguity. Extract match scores from the categorate() output table and validate that the best-match compound identifier and match score both meet your confidence criterion before accepting the classification.

## Related tools

- **ChemmineR** (Performs structural matching and fingerprint-based similarity calculations within categorate() to compute match scores for chemical library comparisons) — https://www.bioconductor.org/packages/release/bioc/html/ChemmineR.html
- **fmcsR** (Computes flexible maximum common substructure (FMCS) matches and molecular descriptors (MW, rings, groups, atoms, charges) used by categorate() and exactoThese() for structural scoring) — https://bioconductor.org/packages/release/bioc/html/fmcsR.html
- **webchem** (Accesses external chemical databases (PubChem, KEGG, FEMA, FDA/SPL) to enrich categorate() output with cross-referenced compound metadata and categorical assignments) — https://cran.r-project.org/web/packages/webchem/index.html
- **uafR** (R package that implements spreadOut(), mzExacto(), categorate(), and exactoThese() functions to orchestrate Match.Factor filtering and structural matching workflows) — https://github.com/castratton/uafR

## Examples

```
query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]; query_categorated = categorate(query_chemicals, chem_library, input_format = "wide")
```

## Evaluation signals

- Verify that filtered query_chemicals subset contains only compounds with Match.Factor ≥ threshold AND that the unfiltered set is larger (confirming filtering occurred).
- Check categorate() output table: every row should have a non-empty match score column; rows with scores >0.95 should have a non-null compound identifier (e.g., 'CMP1', 'CMP2'); rows with scores ≤0.95 or no match should have 'No' or NA.
- Spot-check 2–3 best matches: manually verify that the matched compound identifier (e.g., CMP2 for ethyl hexanoate) aligns with chemical structure or known reference data from the library.
- Confirm that downstream exactoThese() or mzExacto() calls execute without errors when passed the filtered output, and that the resulting chemical subset is non-empty and expected size.
- Compare Match.Factor distribution before and after filtering (e.g., histogram or quantile summary) to confirm that the threshold cut produced the expected subset reduction.

## Limitations

- Match.Factor is instrument- and method-dependent; a threshold of 70 may be appropriate for one GC-MS platform but over-permissive for another. Cross-validation with standards is recommended.
- Structural match scores >0.95 assume that the chemical library is well-curated and contains true reference compounds; if library entries are mislabeled or incomplete, high scores may be misleading.
- The categorate() function's match score depends on the quality and coverage of the restricted chemical library; if a query compound has no close structural analog in the library, all matches may score <0.95 even if the compound is present in the sample.
- Match.Factor and structural match score address different dimensions of confidence (instrument peak matching vs. chemical structure similarity); both should be evaluated but high Match.Factor does not guarantee structural accuracy and vice versa.

## Evidence

- [methods] a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()` is to first subset by match factor: "a useful approach for narrowing the search chemicals for `categorate()` and/or `mzExacto()` is to first subset by match factor: `query_chems = standard_dat$Compound.Name[standard_dat$Match.Factor >="
- [other] The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g., CMP2 for ethyl hexanoate).: "The categorate() function, when applied under structural-matching conditions restricted to 4 chemical type sets, produces a best-match table that correctly identifies compound classifications (e.g.,"
- [other] Call categorate() on the query chemicals, passing the restricted library to access structural match data via ChemmineR, fmcsR, and webchem. Extract the best-match results, which identify the highest-scoring structural match (match score >0.95) within each type set for each query chemical.: "Call categorate() on the query chemicals, passing the restricted library to access structural match data via ChemmineR, fmcsR, and webchem. Extract the best-match results, which identify the"
- [methods] `categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals.: "`categorate()` is an overpowered function that accesses a broad array of categorical data for searched chemicals."
- [readme] query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]: "query_chemicals = input_dat$Compound.Name[input_dat$Match.Factor > 80]"
