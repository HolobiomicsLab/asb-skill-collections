---
name: mass-tolerance-window-filtering
description: Use when after calculating neutral mass from observed m/z and adduct type, and before ranking candidates by chemical plausibility. Use it whenever querying a formula database (KEGG, PubChem, or custom) to retrieve all molecular formulae within a specified mass tolerance window of each neutral mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3664
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - MetaboShiny
  - R
  - KEGG
  - PubChem
  techniques:
  - mass-spectrometry
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

# mass-tolerance-window-filtering

## Summary

Filter candidate molecular formulae by mass error tolerance when matching observed m/z values to database entries. This skill constrains formula lookup results to a user-defined ppm or Da window around the neutral mass, reducing false positives and focusing candidate lists on chemically plausible assignments.

## When to use

Apply this skill after calculating neutral mass from observed m/z and adduct type, and before ranking candidates by chemical plausibility. Use it whenever querying a formula database (KEGG, PubChem, or custom) to retrieve all molecular formulae within a specified mass tolerance window of each neutral mass. It is essential when the database is large and you need to reduce the candidate set to interpretable size.

## When NOT to use

- Input is already a feature table (annotation/compound assignment is done; use this skill earlier in the workflow)
- Mass tolerance window is unknown or unavailable from the instrument (cannot proceed without specifying ppm or Da threshold)
- Formula database is empty, unavailable, or not built in MetaboShiny (build or import database first)

## Inputs

- observed m/z peak list (numeric vector or peaklist file)
- configured adduct definitions (e.g., [M+H]+, [M+Na]+, [M-H]−)
- mass tolerance threshold (numeric, in ppm or Da)
- formula database (KEGG, PubChem, or user-supplied CSV)

## Outputs

- filtered candidate formula table (rows = peaks, columns = formula, observed m/z, theoretical m/z, mass error, adduct type)
- candidate ranking by mass error
- tabulated results with per-peak formula assignments and mass error metrics

## How to apply

For each m/z peak in your input list, first apply the inverse of the configured adduct transformation (e.g., subtract 1.007825 for [M+H]+, subtract 22.989220 for [M+Na]+) to calculate the neutral mass. Then query the formula database with a mass tolerance window defined in parts per million (ppm) or Daltons (Da). The tolerance window is typically set during MetaboShiny project initialization (e.g., 5 ppm for high-resolution instruments). Return all candidate formulae whose theoretical m/z values fall within ±tolerance of the neutral mass. This filtering step greatly reduces computational load and prevents unlikely formulae from propagating to downstream plausibility scoring.

## Related tools

- **MetaboShiny** (Provides configurable adduct settings, formula database integration, and mass-tolerance-filtered candidate lookup within a unified workflow UI) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Underlying language for mass-error calculation, database querying, and candidate filtering logic)
- **KEGG** (Formula database source for molecular formula candidates)
- **PubChem** (Formula database source for molecular formula candidates)

## Evaluation signals

- Candidate formulae returned have mass error (observed m/z − theoretical m/z) within the specified tolerance window (e.g., ≤5 ppm)
- No candidate formulae are returned with mass error exceeding the tolerance threshold
- Candidate count per peak is reduced by >90% relative to unfiltered database size, indicating effective filtering
- Mass error distribution is centered near zero with minimal outliers, suggesting correct neutral mass calculation and adduct inversion
- Downstream chemical plausibility scoring (element ratios, hydrogen deficiency) confirms candidates are chemically reasonable

## Limitations

- Filtering is only as good as the accuracy of the mass spectrometer and the configured mass tolerance; underestimating tolerance may exclude true positives, while overestimating may re-introduce false positives.
- The skill assumes adduct definitions are correct and complete; misconfigured adduct rules will propagate incorrect neutral masses to the tolerance filter.
- Formula databases (KEGG, PubChem) may have gaps, outdated records, or biases toward certain compound classes; custom databases must be manually curated and formatted.
- When multiple adducts are configured for the same peak, tolerance filtering produces separate candidate lists per adduct; ambiguity resolution requires downstream ranking or manual curation.

## Evidence

- [other] For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−).: "For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−)."
- [other] Query the formula database (KEGG, PubChem, or user-supplied) to retrieve all molecular formulae within the configured mass tolerance window (in ppm or Da) of each neutral mass.: "Query the formula database (KEGG, PubChem, or user-supplied) to retrieve all molecular formulae within the configured mass tolerance window (in ppm or Da) of each neutral mass."
- [readme] Set the error margin of your mass spectrometer in parts per million (ppm).: "Set the error margin of your mass spectrometer in parts per million (ppm)."
- [other] Rank candidate formulae by mass error and chemical plausibility rules (e.g., element ratios, hydrogen deficiency).: "Rank candidate formulae by mass error and chemical plausibility rules (e.g., element ratios, hydrogen deficiency)."
- [other] Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak.: "Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak."
