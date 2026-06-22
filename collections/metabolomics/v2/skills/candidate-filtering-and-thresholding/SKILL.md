---
name: candidate-filtering-and-thresholding
description: Use when after generating candidate molecular formula and adduct pairs for detected m/z features, when you have observed isotopic patterns from feature detection and need to reduce annotation ambiguity by eliminating candidates with poor isotopic fit.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MetaboShiny
  - R
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# candidate-filtering-and-thresholding

## Summary

Filter and rank molecular formula and adduct annotation candidates by isotopic pattern matching quality and user-defined thresholds. This skill removes low-confidence candidates and prioritizes high-confidence molecular assignments by comparing observed isotopic distributions to theoretical predictions.

## When to use

After generating candidate molecular formula and adduct pairs for detected m/z features, when you have observed isotopic patterns from feature detection and need to reduce annotation ambiguity by eliminating candidates with poor isotopic fit. Apply this skill before final compound identification to focus downstream analysis on high-confidence molecular hypotheses.

## When NOT to use

- When no observed isotopic pattern data is available from feature detection (i.e., single m/z peaks without isotope envelope information).
- When input candidates lack explicit molecular formula or adduct assignment.
- When isotope scoring configuration has not been set or validated in the MetaboShiny Settings section.

## Inputs

- candidate formula/adduct pairs
- observed m/z isotopic patterns (from feature detection output)
- isotope scoring configuration (method, intensity imprecision threshold)

## Outputs

- ranked annotation table with isotope scores
- filtered candidate set (above-threshold candidates only)
- isotope score per candidate

## How to apply

Load candidate formula/adduct pairs alongside their corresponding observed m/z isotopic patterns from the feature detection output. For each candidate, calculate the theoretical isotopic pattern using the molecular formula and specified adduct. Compute an isotope score by measuring similarity between observed and theoretical patterns (e.g., cosine similarity or intensity correlation). Apply isotope scoring threshold filters as configured in the Isotope scoring settings, typically using an intensity imprecision default of 2%. Rank all candidates by isotope score in descending order and output a ranked annotation table with scores. Candidates below the threshold are removed; those above are retained and sorted by score magnitude.

## Related tools

- **MetaboShiny** (Provides Isotope scoring configuration UI and ranking/filtering pipeline for candidate annotations based on isotopic pattern similarity) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Computational backend for isotope pattern calculation, similarity scoring, and ranking operations)

## Evaluation signals

- Ranked candidates are sorted in descending order by isotope score; verify ordering is monotonic.
- All retained candidates have isotope scores ≥ the configured threshold (default intensity imprecision 2%); spot-check threshold compliance.
- Candidates filtered out have isotope scores below threshold; verify they were removed from the output table.
- Isotope scores reflect similarity metric used (e.g., cosine similarity or intensity correlation); values should fall within expected metric range (e.g., 0–1 for normalized similarity).
- Theoretical isotopic pattern calculation matches the selected adduct and molecular formula; re-compute one candidate manually as a spot check.

## Limitations

- Isotope scoring depends on high-quality, well-resolved isotopic patterns in observed data; noisy or poorly resolved isotope envelopes may yield unreliable scores.
- Only M-score isotope scoring method is currently available in MetaboShiny; alternative similarity metrics are not yet supported.
- Intensity imprecision threshold (default 2%) is global and uniform across all candidates; heterogeneous noise levels or instrumental variability may require case-specific tuning.
- Filtering is sensitive to correct molecular formula and adduct specification; errors in formula generation or adduct table will propagate into meaningless scores.

## Evidence

- [other] For each candidate, calculate the theoretical isotopic pattern using the molecular formula and specified adduct. Compute isotope score by measuring the similarity between observed and theoretical patterns (e.g., cosine similarity or intensity correlation).: "For each candidate, calculate the theoretical isotopic pattern using the molecular formula and specified adduct. Compute isotope score by measuring the similarity between observed and theoretical"
- [other] Apply isotope scoring threshold filters as configured in the Isotope scoring settings. Rank all candidates by isotope score in descending order and output the ranked annotation table with scores.: "Apply isotope scoring threshold filters as configured in the Isotope scoring settings. Rank all candidates by isotope score in descending order and output the ranked annotation table with scores."
- [other] MetaboShiny includes an Isotope scoring configuration setting as part of its pre-analysis workflow, located within the Settings section alongside Global, Project, Search, Adducts, and Formula prediction parameters.: "MetaboShiny includes an Isotope scoring configuration setting as part of its pre-analysis workflow, located within the Settings section alongside Global, Project, Search, Adducts, and Formula"
- [readme] Select the method to use to score compounds that have the same weight (currently only M-score available). Set the intensity imprecision (default: 2%).: "Select the method to use to score compounds that have the same weight (currently only M-score available). Set the intensity imprecision (default: 2%)."
