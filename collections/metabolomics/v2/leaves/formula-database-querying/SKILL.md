---
name: formula-database-querying
description: Use when you have calibrated m/z peak lists, configured adduct transformations
  (e.g., [M+H]+, [M+Na]+, [M-H]−), and need to annotate peaks with molecular formulae
  from KEGG, PubChem, or custom databases.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - MetaboShiny
  - R
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-database-querying

## Summary

Query molecular formula databases to retrieve candidate formulae for observed m/z values after adduct-corrected neutral mass calculation. This skill maps mass spectrometry peaks to chemical structures by systematically matching theoretical formula masses within a configurable mass tolerance window (ppm or Da).

## When to use

Apply this skill when you have calibrated m/z peak lists, configured adduct transformations (e.g., [M+H]+, [M+Na]+, [M-H]−), and need to annotate peaks with molecular formulae from KEGG, PubChem, or custom databases. Use it as the intermediate step after adduct configuration and before isotope pattern scoring in metabolomics annotation pipelines.

## When NOT to use

- Input is already fully annotated with verified molecular structures (formula prediction is redundant).
- Mass spectrometry data lacks reliable m/z calibration or adduct information (will produce unreliable neutral mass estimates).
- Working with intact protein or large polymer data where formula prediction is less meaningful than sequence matching.

## Inputs

- m/z peak list (numeric values with intensities)
- adduct configuration table (adduct name, mass shift, charge)
- molecular formula database (CSV with formula, monoisotopic mass, optional metadata)
- mass tolerance threshold (ppm or Da)

## Outputs

- ranked candidate formula table (columns: m/z, neutral mass, molecular formula, adduct type, theoretical m/z, mass error in ppm, plausibility score)
- filtered peak-to-formula assignments (top candidate per peak or top-N candidates)

## How to apply

For each m/z value in your peak list, calculate the neutral mass by applying the inverse of each configured adduct transformation. Query the selected formula database (KEGG, PubChem, or user-supplied CSV) to retrieve all molecular formulae whose theoretical monoisotopic masses fall within the configured mass tolerance window (typically 5–10 ppm or equivalent Da threshold). Rank returned candidates by mass error and apply chemical plausibility filters (e.g., element ratio rules, hydrogen deficiency thresholds). Return and tabulate the top-ranked formula candidates with their observed m/z, theoretical m/z, calculated mass error (in ppm), assigned adduct type, and neutral mass for each peak.

## Related tools

- **MetaboShiny** (Primary application encapsulating formula prediction and lookup; orchestrates adduct configuration, database querying, ranking, and tabulation of candidate formulae) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Underlying computation language for formula database operations and mass calculation logic)

## Evaluation signals

- Mass error for top-ranked candidates falls within the configured tolerance window (ppm or Da); verify no candidate exceeds threshold.
- Neutral mass calculations are consistent: neutral_mass = observed_m/z × |charge| − adduct_mass_shift (for positive mode [M+H]+ example: neutral = (m/z × 1) − 1.007825).
- Returned formulae pass chemical plausibility rules: hydrogen deficiency ≥ 0, element ratios within expected bounds (e.g., O/C < 2, N/C < 1.5).
- Tabulated output contains non-empty rows only for peaks with at least one formula candidate within tolerance; peaks with zero matches are explicitly marked or excluded per user settings.
- Comparison of mass error distribution: observed ppm errors should be centered near zero with SD matching instrument calibration; outliers suggest incorrect adduct assignment or database mismatch.

## Limitations

- Formula prediction accuracy is limited by database completeness; rare or novel metabolites absent from KEGG, PubChem, or custom database will not be retrieved.
- Mass tolerance window (ppm) must be carefully chosen: too narrow may exclude correct formulae due to calibration drift; too wide introduces false positives.
- Isotope patterns and adduct multiplicities (e.g., [M+2H]2+, [2M+H]+) are not distinguished during formula lookup and must be filtered in downstream isotope scoring or manual review.
- Chemical plausibility rules (element ratios, hydrogen deficiency) are heuristic and may reject valid metabolite formulae outside typical ranges.
- Multiple formulae can have nearly identical masses, especially for large molecules; mass error alone may not resolve ambiguity without additional scoring (e.g., isotope patterns, MS/MS fragmentation).

## Evidence

- [other] For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−).: "For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−)."
- [other] Query the formula database (KEGG, PubChem, or user-supplied) to retrieve all molecular formulae within the configured mass tolerance window (in ppm or Da) of each neutral mass.: "Query the formula database (KEGG, PubChem, or user-supplied) to retrieve all molecular formulae within the configured mass tolerance window (in ppm or Da) of each neutral mass."
- [other] Rank candidate formulae by mass error and chemical plausibility rules (e.g., element ratios, hydrogen deficiency).: "Rank candidate formulae by mass error and chemical plausibility rules (e.g., element ratios, hydrogen deficiency)."
- [other] Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak.: "Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak."
- [readme] Here you can set the parameters and rules to use when predicting chemical formulas.: "Here you can set the parameters and rules to use when predicting chemical formulas."
