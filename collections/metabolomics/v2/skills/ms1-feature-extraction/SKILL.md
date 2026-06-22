---
name: ms1-feature-extraction
description: Use when when you have an LC-HRMS feature table (with m/z values, retention times, and isotopic signatures) and a suspect compound database (with reference m/z, expected retention time windows, isotope ratios, and neutral loss fragments), and you need to rapidly prioritize which features are most.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Scannotation
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.est.3c04764
  title: Scannotation
evidence_spans:
- Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scannotation_cq
    doi: 10.1021/acs.est.3c04764
    title: Scannotation
  dedup_kept_from: coll_scannotation_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.3c04764
  all_source_dois:
  - 10.1021/acs.est.3c04764
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms1-feature-extraction

## Summary

Extract and integrate multiple MS1 chemical predictors (m/z, retention times, isotopic patterns, neutral loss patterns) from LC-HRMS features to compute unified proximity scores between detected features and suspect compounds. This enables rapid prioritization of compound candidates during suspect screening workflows.

## When to use

When you have an LC-HRMS feature table (with m/z values, retention times, and isotopic signatures) and a suspect compound database (with reference m/z, expected retention time windows, isotope ratios, and neutral loss fragments), and you need to rapidly prioritize which features are most likely to correspond to which suspects before MS/MS annotation or manual review.

## When NOT to use

- Input is already a manually validated or MS/MS-confirmed compound assignment — use this skill for pre-annotation only, not to second-guess confirmed identities.
- You lack reference isotopic or neutral loss patterns for your suspect compounds — the scoring will be incomplete and reliability will degrade.
- Your feature table does not include retention time data — RT proximity scoring will be unavailable, reducing discriminatory power.

## Inputs

- LC-HRMS feature table (m/z values, retention times, isotopic pattern signatures)
- Suspect compound database (reference m/z, expected retention time windows, isotope ratios, neutral loss fragments)
- Mass error tolerance (ppm or absolute Da)
- Retention time deviation window (minutes)
- Component weights for ensemble scoring

## Outputs

- Feature–suspect proximity scores (per feature–suspect pair)
- Ranked candidate compound list (sorted by proximity score)
- Filtered prioritized compound assignments (above score threshold)

## How to apply

Load the feature table and suspect compound database into Scannotation. For each feature–suspect pair, compute four component scores: (1) m/z distance using absolute or relative mass error tolerance (typically ppm-based); (2) retention time proximity by comparing observed vs. predicted RT within an acceptable deviation window; (3) isotopic pattern match by comparing observed isotope abundance ratios to theoretical patterns for the suspect; (4) neutral loss pattern match by identifying common loss fragments (H₂O, CO₂, CH₄) in the observed feature fragmentation profile relative to the suspect's expected structure. Combine these four scores via weighted ensemble (default: weighted sum) to produce a final feature–suspect proximity score. Rank all candidates by this score and apply a threshold filter to generate a prioritized compound list for downstream validation.

## Related tools

- **Scannotation** (Automated suspect screening tool that implements the MS1 predictor combiner scoring pipeline to compute feature–suspect proximity scores and prioritize compound candidates for LC-HRMS pre-annotation.) — https://github.com/scannotation/Scannotation_software

## Evaluation signals

- Proximity scores are computed for all feature–suspect pairs without missing values; check that output table has dimensions = (n_features × n_suspects).
- Component scores (m/z, RT, isotope, neutral loss) fall within their expected ranges (typically 0–1 or 0–100 depending on normalization); verify no NaN, Inf, or out-of-bound values.
- Ranked output is sorted in descending order by proximity score; spot-check that top-ranked candidates have higher scores than lower-ranked ones.
- Filtered output respects the applied threshold: all remaining feature–suspect pairs have proximity score ≥ threshold; all removed pairs have score < threshold.
- For known positive control feature–suspect pairs, verify that the assigned proximity score is among the top-ranked (e.g., top 5%) for that feature, confirming the scoring mechanism is not inverting or randomizing ranks.

## Limitations

- Scoring accuracy depends critically on the quality and completeness of reference data in the suspect compound database (isotope ratios, neutral loss fragments). Missing or incorrect reference patterns will degrade ranking.
- Retention time prediction quality varies across chromatographic methods and column chemistries; RT-based scoring may be unreliable if predicted RT windows are poorly calibrated or method-specific.
- The weighted ensemble method for combining component scores is heuristic; optimal weights may vary by chemical class or sample matrix, requiring method-specific tuning.
- Scannotation was developed and tested on Windows 10 and Mac (in Windows virtual machine); cross-platform compatibility on native Linux or other OS is not documented.

## Evidence

- [readme] Scannotation combines MS1 chemical predictors and scores proximity for feature-suspect prioritization.: "This software combines several MS1 chemical predictors: m/z, retention times, isotopic patterns and neutral loss patterns, to score the proximity between features and suspects, thus efficiently"
- [other] The workflow involves loading data, computing four component scores, and combining them via ensemble method.: "Load feature table (m/z values, retention times, isotopic pattern signatures) and suspect compound database (reference m/z, expected retention time windows, isotope ratios, neutral loss fragments)."
- [readme] Scannotation enables rapid pre-annotation of LC-HRMS datasets through automated suspect screening.: "Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets."
- [readme] Development and testing platform details.: "Scannotation was developed on Windows 10 and tested on both Windows and on a Mac computer in a Windows virtual machine."
