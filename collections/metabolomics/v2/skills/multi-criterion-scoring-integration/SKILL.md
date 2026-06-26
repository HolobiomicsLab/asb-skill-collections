---
name: multi-criterion-scoring-integration
description: Use when you have an LC-HRMS feature table (m/z, retention time, isotope
  ratios, fragmentation patterns) and a suspect compound database with reference properties
  (m/z, expected RT windows, theoretical isotope ratios, characteristic neutral losses),
  and you need to rank which features most likely.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Scannotation
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.est.3c04764
  title: Scannotation
evidence_spans:
- Scannotation is an automated and user-friendly suspect screening tool for the rapid
  pre-annotation of LC-HRMS datasets.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-criterion-scoring-integration

## Summary

Integrates multiple orthogonal MS1 chemical predictors (m/z, retention time, isotopic pattern, neutral loss) into a unified proximity score to rank feature-suspect pairs for LC-HRMS suspect screening. This skill enables rapid, automated prioritization of candidate compounds by combining weak individual signals into a robust ensemble score.

## When to use

Apply this skill when you have an LC-HRMS feature table (m/z, retention time, isotope ratios, fragmentation patterns) and a suspect compound database with reference properties (m/z, expected RT windows, theoretical isotope ratios, characteristic neutral losses), and you need to rank which features most likely correspond to which suspects without running MS2 fragmentation on all candidates.

## When NOT to use

- Feature table is already assigned to confirmed standards with authentic MS2 spectra — use MS2 library matching instead.
- Suspect database lacks theoretical retention time or isotope ratio predictions — scoring will be incomplete and reliability reduced.
- Sample contains only a single dominant compound or is already pre-filtered to high confidence candidates — overhead of multi-criterion integration is not justified.

## Inputs

- LC-HRMS feature table (m/z values, retention times, observed isotopic pattern abundances, observed fragmentation neutral losses)
- Suspect compound database (reference m/z, expected retention time windows, theoretical isotope ratios, known neutral loss fragments for each suspect)

## Outputs

- Ranked feature-suspect proximity scores (scalar score per pair)
- Prioritized compound candidate list (features ranked by proximity to suspects, filtered above decision threshold)
- Scoring component breakdown (m/z distance, RT proximity, isotope match, neutral loss match per pair for interpretability)

## How to apply

Load the observed feature table and suspect compound database. For each feature-suspect pair, compute four independent proximity metrics: (1) m/z distance as absolute or relative mass error within your tolerance window (e.g. 5 ppm); (2) retention time proximity as deviation from predicted RT within an acceptable window; (3) isotopic pattern match as correlation or χ² between observed and theoretical isotope abundance ratios; (4) neutral loss pattern match as presence of common loss fragments (e.g., H₂O, CO₂, CH₄) in the observed feature profile. Combine the four component scores via weighted sum, normalized ensemble, or other aggregation method—Scannotation's implementation uses a unified scoring mechanism but the exact weighting scheme should be tuned to your analytical platform and compound class. Rank all feature-suspect pairs by final score and apply a decision threshold to produce a prioritized candidate list for confirmatory MS2 analysis or targeted acquisition.

## Related tools

- **Scannotation** (implements multi-criterion scoring module integrating m/z, retention time, isotopic pattern, and neutral loss predictors for automated suspect screening and feature-suspect proximity ranking) — https://github.com/scannotation/Scannotation_software

## Evaluation signals

- All four component scores (m/z, RT, isotope, neutral loss) are computed and present in output for each feature-suspect pair; no missing or NaN values where predictors are defined.
- Final proximity scores are bounded in a consistent range (e.g., 0–1 or 0–100) and monotonically rank candidates such that higher-scoring pairs receive higher priority.
- Feature-suspect pairs known to be true positives (from standards or confirmed annotations) rank significantly higher than decoy or negative-control pairs in the same feature set.
- Threshold-filtered candidate list is smaller than the full feature table by a meaningful margin (e.g., 5–50% of original features retained), indicating effective prioritization.
- Component score contributions are independently interpretable: e.g., a high-scoring pair can be traced to strong m/z and isotope matches even if RT or neutral loss scores are weak, demonstrating that the ensemble does not mask individual signals.

## Limitations

- Accuracy depends on accuracy and completeness of suspect database predictions (reference m/z, RT windows, isotope ratios, neutral losses); missing or incorrect reference data will produce misleading proximity scores.
- Relative weighting of the four component scores (m/z, RT, isotope, neutral loss) is not data-driven in the article; manual tuning may be required for optimal performance on different compound classes or LC-MS platforms.
- Retention time prediction model is not detailed; if RT windows are too broad or narrow, the RT component will either add noise or provide false confidence.
- Neutral loss component requires detailed knowledge of suspect chemistry; for complex or unfamiliar compounds, predicted neutral loss patterns may be incomplete or incorrect.
- Does not address cases where multiple features map to the same suspect or multiple suspects map to the same feature; post-processing or conflict resolution rules are not specified.

## Evidence

- [readme] Scannotation combines MS1 chemical predictors and scores proximity between features and suspects: "This software combines several MS1 chemical predictors: m/z, retention times, isotopic patterns and neutral loss patterns, to score the proximity between features and suspects"
- [intro] Four component scores are integrated into a unified scoring mechanism: "Scannotation implements a scoring module that integrates four MS1 chemical predictors—m/z, retention times, isotopic patterns, and neutral loss patterns—to compute a proximity score between detected"
- [other] Workflow combines component scores via weighted sum or ensemble method: "Combine the four component scores (m/z, RT, isotope, neutral loss) via weighted sum or other ensemble method to produce final feature-suspect proximity score"
- [readme] Scoring enables rapid pre-annotation and compound prioritization: "Scannotation is an automated and user-friendly suspect screening tool for the rapid pre-annotation of LC-HRMS datasets."
- [other] Final ranking and threshold filtering produce prioritized candidate list: "Rank candidates by proximity score and filter by threshold to produce prioritized compound list"
