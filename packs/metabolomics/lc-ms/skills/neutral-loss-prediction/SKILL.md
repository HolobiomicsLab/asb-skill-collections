---
name: neutral-loss-prediction
description: Use when you have LC-HRMS features with fragmentation data (observed m/z shifts, mass deficits, or tandem MS spectra) and a suspect compound database with known or predictable neutral loss fragments (e.g., H₂O, CO₂, CH₄, or structure-specific losses).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - Scannotation
  techniques:
  - LC-MS
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

# neutral-loss-prediction

## Summary

Predict and score neutral loss fragment patterns from LC-HRMS features to match against suspect compound structures, enabling probabilistic compound prioritization in suspect screening workflows. This skill bridges observed fragmentation profiles and theoretical structural losses to improve feature-to-compound assignment accuracy.

## When to use

Apply this skill when you have LC-HRMS features with fragmentation data (observed m/z shifts, mass deficits, or tandem MS spectra) and a suspect compound database with known or predictable neutral loss fragments (e.g., H₂O, CO₂, CH₄, or structure-specific losses). Use it as part of a multi-predictor scoring pipeline when m/z, retention time, and isotopic pattern alone are insufficient to confidently prioritize candidates.

## When NOT to use

- Input features lack fragmentation data or tandem MS spectra (neutral loss scoring requires observed mass shifts or fragment m/z values).
- Suspect database contains no structural or empirical neutral loss annotations (prediction requires at least reference fragmentation profiles or reaction rules).
- Analysis goal is exploratory feature clustering or de novo compound discovery, not targeted suspect matching (neutral loss scoring is most effective with a curated suspect list).

## Inputs

- LC-HRMS feature table (m/z values, retention times, fragmentation spectra or mass shifts)
- Suspect compound database (chemical structures, expected retention times, theoretical or empirical neutral loss patterns)
- Mass error tolerance threshold (ppm or Da)
- Neutral loss database or fragmentation prediction model

## Outputs

- Neutral loss match scores (per feature–suspect pair)
- Ranked list of suspect compounds prioritized by multi-predictor proximity score
- Feature-suspect assignments with confidence annotations

## How to apply

For each observed LC-HRMS feature, identify common neutral loss fragments (e.g., water loss = −18 Da, CO₂ loss = −44 Da) in the mass spectrum or inferred from retention time and m/z transitions. For each suspect compound in the database, predict or retrieve known neutral loss patterns based on its chemical structure or empirical fragmentation rules. Compare observed and predicted neutral loss m/z shifts using absolute or relative mass error tolerance (typically 5–10 ppm for HRMS). Score the match by counting concordant losses or computing a similarity metric (e.g., fraction of expected losses observed). Combine the neutral loss score with m/z, retention time, and isotopic pattern scores via weighted sum or ensemble method to produce a final feature-suspect proximity score. Rank and filter by score threshold to prioritize candidates for confirmation.

## Related tools

- **Scannotation** (Automated suspect screening platform that integrates neutral loss pattern scoring with m/z, retention time, and isotopic pattern predictors into a unified feature-suspect proximity scoring module) — https://github.com/scannotation/Scannotation_software

## Evaluation signals

- Neutral loss scores are computed and ranked for all feature–suspect pairs without missing or NaN values (completeness check).
- Observed neutral loss m/z deltas fall within the specified mass error tolerance (5–10 ppm) of predicted losses for high-scoring matches.
- Features with known fragmentation patterns (e.g., from reference standards) show elevated neutral loss scores when matched against the corresponding suspect compound.
- Final multi-predictor proximity scores correlate positively with validation outcomes (e.g., confirmed identifications by orthogonal methods).
- Neutral loss score component has non-zero variance and contributes measurably to ranking when combined with other MS1 predictors (no redundancy or collapse to uniform scores).

## Limitations

- Neutral loss prediction accuracy depends on availability of experimental fragmentation data or validated structure–fragmentation rules; insufficient training data or incorrect structural annotations reduce scoring reliability.
- Common neutral losses (H₂O, CO₂) may occur in multiple structural isomers, reducing discriminative power when used alone; neutral loss scoring is most effective as part of an ensemble with m/z, RT, and isotopic pattern predictors.
- Observed neutral losses in low-resolution or noisy MS data may be missed or misassigned, especially for small or isobaric fragments; HRMS and clean spectral preprocessing are assumed.
- No formal validation of Scannotation's neutral loss weighting scheme or threshold tuning procedure is documented in the available README; parameter sensitivity and generalization to new chemical classes are unknown.

## Evidence

- [readme] Scannotation combines several MS1 chemical predictors: m/z, retention times, isotopic patterns and neutral loss patterns, to score the proximity between features and suspects, thus efficiently prioritizing compounds of interest: "combines several MS1 chemical predictors: m/z, retention times, isotopic patterns and neutral loss patterns, to score the proximity between features and suspects"
- [other] Score neutral loss pattern match by identifying common loss fragments (e.g., H₂O, CO₂, CH₄) in the observed feature fragmentation profile relative to suspect structure: "Score neutral loss pattern match by identifying common loss fragments (e.g., H₂O, CO₂, CH₄) in the observed feature fragmentation profile relative to suspect structure"
- [other] Combine the four component scores (m/z, RT, isotope, neutral loss) via weighted sum or other ensemble method to produce final feature-suspect proximity score: "Combine the four component scores (m/z, RT, isotope, neutral loss) via weighted sum or other ensemble method to produce final feature-suspect proximity score"
- [readme] Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets: "automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets"
