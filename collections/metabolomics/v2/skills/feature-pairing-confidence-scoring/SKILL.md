---
name: feature-pairing-confidence-scoring
description: Use when you have two LC-MS feature tables (each with m/z, retention
  time, and intensity columns) and need to establish reliable correspondence between
  features across datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Matlab
  - M2S
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c03592
  title: m2s
evidence_spans:
- Matlab package to match untargeted metabolomic features
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s_cq
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  dedup_kept_from: coll_m2s_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03592
  all_source_dois:
  - 10.1021/acs.analchem.1c03592
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-pairing-confidence-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute and assign confidence scores to candidate feature pairs from two LC-MS metabolomic datasets by evaluating similarity across m/z and retention time dimensions, then resolve one-to-one correspondences by selecting highest-confidence matches. This skill is essential for confidently aligning untargeted metabolomic features across replicate or comparative LC-MS runs.

## When to use

You have two LC-MS feature tables (each with m/z, retention time, and intensity columns) and need to establish reliable correspondence between features across datasets. Specifically, apply this skill when: (1) you have computed initial pairwise similarity scores across m/z and retention time dimensions, (2) you have candidate feature pairs that may contain false positives, and (3) your analysis goal requires unambiguous one-to-one feature mappings rather than ambiguous many-to-many associations.

## When NOT to use

- Input datasets are already manually curated or contain pre-validated feature correspondences; scoring is redundant.
- You require many-to-many feature associations or fuzzy matching rather than strict one-to-one correspondence.
- LC-MS datasets are from fundamentally different analytical methods (e.g., different ionization, column chemistry) where m/z and retention time alone are insufficient predictors of true correspondence.

## Inputs

- LC-MS feature table 1 (with m/z, retention time, and intensity columns)
- LC-MS feature table 2 (with m/z, retention time, and intensity columns)
- mass-to-charge tolerance (in ppm or Da)
- retention time tolerance (in seconds or minutes)

## Outputs

- Matched feature pairs table (original feature identifiers, m/z values, retention times, match confidence scores)
- Confidence score matrix (pairwise similarity scores)

## How to apply

Load both LC-MS feature tables into Matlab and apply pairwise feature matching by computing similarity scores using the M2S matching algorithm, which evaluates both m/z and retention time dimensions simultaneously. Filter candidate matches by imposing mass-to-charge and temporal tolerances to eliminate false positives—these tolerances should reflect your instrument's typical m/z accuracy and retention time stability. Resolve competing one-to-one feature correspondences by selecting the highest-confidence match for each feature pair; this ensures each input feature maps to at most one output feature and vice versa, avoiding redundant or contradictory assignments. Compile matched pairs into a structured output table that preserves original feature identifiers, m/z values, retention times, and match confidence scores for downstream interpretation and troubleshooting.

## Related tools

- **M2S** (Matlab package that implements pairwise feature matching and confidence scoring for untargeted metabolomic LC-MS datasets) — https://github.com/rjdossan/M2S

## Evaluation signals

- Matched feature pairs preserve one-to-one cardinality: each input feature from dataset 1 pairs to exactly one feature in dataset 2 and vice versa (no unmapped or multiply-assigned features).
- Confidence scores are monotonically correlated with match accuracy: true-positive pairs should exhibit higher scores than false-positive pairs, validated by independent verification (e.g., standards, replicate analysis, or orthogonal methods).
- Output table is non-empty and contains all required columns (original feature identifiers, m/z, retention time, confidence scores) with no NaN or missing values in scored pairs.
- m/z and retention time differences between matched pairs fall within the imposed tolerances; pairs violating tolerance thresholds should be filtered or flagged.
- Confidence score distribution shows clear separation between high-confidence matches and filtered-out candidates, indicating effective discrimination between true and false correspondences.

## Limitations

- Performance depends critically on the choice of mass-to-charge and retention time tolerances; overly loose tolerances yield false positives, overly strict tolerances yield false negatives. Tolerances should be instrument- and method-specific.
- M2S was developed for untargeted metabolomic datasets and may not generalize to targeted methods, data-dependent acquisition, or fundamentally different analytical workflows.
- No changelog or version history is documented, limiting ability to assess reproducibility across package updates or to understand which algorithm variants have been tested.
- Confidence scoring relies only on m/z and retention time similarity; it does not incorporate intensity, spectral fragmentation, or chemical structure information, which may improve resolution of ambiguous pairs.

## Evidence

- [other] Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm.: "Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm."
- [other] Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives.: "Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives."
- [other] Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair.: "Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair."
- [readme] Matlab package to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores.: "Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores."
