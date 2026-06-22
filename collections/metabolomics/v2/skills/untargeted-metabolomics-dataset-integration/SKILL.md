---
name: untargeted-metabolomics-dataset-integration
description: Use when you have two LC-MS feature tables (each with m/z, retention time, and intensity columns) from independent untargeted metabolomic experiments or replicates and need to establish one-to-one feature correspondence across them to compare abundances, detect shared metabolites, or merge datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Matlab
  - M2S
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-metabolomics-dataset-integration

## Summary

Match untargeted metabolomic features across two LC-MS datasets by computing pairwise similarity scores on m/z and retention time dimensions, then resolving one-to-one correspondences with confidence filtering. This enables comparative metabolomics workflows where features from independent runs must be aligned before statistical or functional analysis.

## When to use

You have two LC-MS feature tables (each with m/z, retention time, and intensity columns) from independent untargeted metabolomic experiments or replicates and need to establish one-to-one feature correspondence across them to compare abundances, detect shared metabolites, or merge datasets for downstream analysis.

## When NOT to use

- Datasets are from targeted metabolomics with known internal standards and reference compounds — use targeted feature alignment instead.
- Input feature tables are not yet generated from raw LC-MS data — first perform peak picking, deconvolution, and feature table construction.
- Datasets use radically different LC-MS protocols (e.g., positive vs. negative ionization modes, different chromatographic methods) — consider post-hoc ionization or mode conversion before matching.

## Inputs

- LC-MS feature table 1 (columns: m/z, retention time, intensity)
- LC-MS feature table 2 (columns: m/z, retention time, intensity)

## Outputs

- Matched feature pairs table (columns: feature_id_1, feature_id_2, m/z_1, m/z_2, retention_time_1, retention_time_2, match_confidence_score)
- Unmatched features report (features with no confident correspondence)

## How to apply

Load both LC-MS feature tables into Matlab. Apply the M2S matching algorithm to compute pairwise similarity scores across m/z and retention time dimensions. Filter candidate matches by applying mass-to-charge and temporal tolerances (article/README do not specify exact thresholds) to eliminate false positives. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair, avoiding many-to-one or one-to-many assignments. Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores for downstream validation and analysis.

## Related tools

- **Matlab** (Runtime environment for executing M2S pairwise feature matching algorithm on LC-MS feature tables)
- **M2S** (Core package implementing similarity-score-based matching of untargeted metabolomic features across two LC-MS datasets) — https://github.com/rjdossan/M2S

## Evaluation signals

- All matched feature pairs have symmetric one-to-one relationships (no feature appears in multiple pairs).
- Match confidence scores are reported for each pair and fall within a reasonable range (article does not specify exact range); pairs with low confidence can be manually reviewed or filtered.
- Matched m/z and retention time pairs exhibit small deltas relative to user-defined or default tolerances, confirming that only chemically plausible correspondences were retained.
- Output table schema includes original feature identifiers from both input tables, enabling traceability back to raw feature tables and peak properties.
- Unmatched features are documented and quantified; a high proportion of unmatched features may indicate misaligned chromatography or instrument drift requiring investigation.

## Limitations

- M2S is designed for pairwise matching of exactly two datasets; matching three or more datasets requires iterative or custom extensions.
- Matching accuracy depends on chromatographic reproducibility and mass accuracy of the LC-MS instrument; datasets with poor retention time or m/z stability may yield low match confidence.
- No explicit handling of adducts, isotopes, or in-source fragments is mentioned; pre-processing or separate adduct annotation may be required.
- The article provides no information on computational complexity or scalability to large feature tables (thousands of features per dataset).
- GitHub repository shows no changelog; version history and parameter tuning guidance are unavailable.

## Evidence

- [other] M2S is a Matlab package designed to match untargeted metabolomic features of two LC-MS datasets.: "M2S is a Matlab package designed to match untargeted metabolomic features of two LC-MS datasets."
- [other] Load two LC-MS feature tables (each with m/z, retention time, and intensity columns) into Matlab. Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm. Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair. Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores.: "Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm. Filter candidate matches based on mass-to-charge and temporal"
- [intro] Matlab package to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
