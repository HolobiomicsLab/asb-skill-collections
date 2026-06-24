---
name: retention-time-mass-correspondence-resolution
description: Use when you have two LC-MS untargeted metabolomic feature tables (each
  containing m/z, retention time, and intensity columns) and need to establish which
  features in dataset A correspond to which features in dataset B, typically for comparative
  metabolomics, batch effect correction, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
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

# retention-time-mass-correspondence-resolution

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match untargeted metabolomic features across two LC-MS datasets by resolving one-to-one correspondences based on m/z and retention time similarity. This skill enables cross-dataset feature alignment by computing pairwise similarity scores and selecting highest-confidence matches within specified mass and temporal tolerances.

## When to use

You have two LC-MS untargeted metabolomic feature tables (each containing m/z, retention time, and intensity columns) and need to establish which features in dataset A correspond to which features in dataset B, typically for comparative metabolomics, batch effect correction, or multi-cohort feature integration.

## When NOT to use

- Input datasets are targeted metabolomics (with known metabolite identities) rather than untargeted feature discovery.
- Features are already aligned (e.g., from a single LC-MS run or pre-processed common feature space).
- One or both input tables lack retention time information or have poor m/z calibration.

## Inputs

- LC-MS feature table 1 (with m/z, retention time, intensity columns)
- LC-MS feature table 2 (with m/z, retention time, intensity columns)

## Outputs

- Matched feature pair table (original identifiers, m/z, retention times, confidence scores)
- Feature correspondence matrix

## How to apply

Load both LC-MS feature tables into Matlab, then apply the M2S matching algorithm to compute pairwise similarity scores across m/z and retention time dimensions. Define mass-to-charge and temporal tolerances to filter candidate matches and eliminate false positives. Resolve the bipartite matching problem by selecting the highest-confidence match for each feature pair, ensuring a one-to-one correspondence. Output a structured table mapping original feature identifiers, m/z values, retention times, and match confidence scores for downstream validation and reuse.

## Related tools

- **M2S** (Matlab package implementing pairwise feature matching and one-to-one correspondence resolution via m/z and retention time similarity scoring) — https://github.com/rjdossan/M2S

## Evaluation signals

- All matched pairs have m/z and retention time differences within user-specified tolerances (e.g., ±5 ppm for mass, ±0.5 min for retention time).
- Each feature in the smaller dataset is matched to at most one feature in the larger dataset (one-to-one correspondence enforced).
- Match confidence scores are monotonically ranked; the highest-scoring match is selected for each feature pair.
- Output table schema is complete: every matched pair includes original identifiers, m/z values, retention times, and confidence metrics.
- No matched pairs violate the pairwise similarity metric (e.g., Euclidean distance in normalized m/z–RT space).

## Limitations

- M2S is designed for untargeted LC-MS feature matching; performance may degrade if features are poorly resolved or if m/z calibration differs significantly between datasets.
- One-to-one matching assumes no feature duplication or isobaric co-elution; overlapping or ambiguous matches may lead to arbitrary resolution.
- Sensitivity to mass and temporal tolerance thresholds; overly strict tolerances risk missing true matches, while loose tolerances risk false positives.
- No changelog or version control information was found, limiting reproducibility and compatibility tracking.

## Evidence

- [readme] Matlab package to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm.: "Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm"
- [other] Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives.: "Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives"
- [other] Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair.: "Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair"
- [other] Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores.: "Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores"
