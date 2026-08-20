---
name: metabolomic-feature-matching
description: Use when you have two LC-MS feature tables (each with m/z, retention
  time, and intensity columns) from separate metabolomic experiments or replicates,
  and you need to establish which features in dataset A correspond to which features
  in dataset B to enable comparative or longitudinal analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Matlab
  - M2S
  techniques:
  - LC-MS
  license_tier: open
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

# metabolomic-feature-matching

## Summary

M2S is a Matlab package that matches untargeted metabolomic features across two LC-MS datasets by computing similarity scores on m/z and retention time dimensions and resolving one-to-one feature correspondences. Use this skill when you have two independent LC-MS metabolomic experiments and need to establish which detected features represent the same underlying metabolite across datasets.

## When to use

You have two LC-MS feature tables (each with m/z, retention time, and intensity columns) from separate metabolomic experiments or replicates, and you need to establish which features in dataset A correspond to which features in dataset B to enable comparative or longitudinal analysis.

## When NOT to use

- Input data are already aligned or from targeted metabolomic methods with pre-defined feature lists
- You have only a single LC-MS dataset (no second dataset to match against)
- Features have already been matched using an alternative method and you are validating results

## Inputs

- LC-MS feature table 1 (m/z, retention time, intensity columns)
- LC-MS feature table 2 (m/z, retention time, intensity columns)

## Outputs

- Matched feature pairs table with original identifiers, m/z values, retention times, and confidence scores

## How to apply

Load both LC-MS feature tables into Matlab, each containing m/z, retention time, and intensity columns. Apply the M2S matching algorithm to compute pairwise similarity scores across the m/z and retention time dimensions. Filter candidate matches using mass-to-charge and temporal tolerances to eliminate false positives. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair. Compile the matched pairs into a structured output table preserving original feature identifiers, m/z values, retention times, and match confidence scores.

## Related tools

- **Matlab** (Execution environment for M2S matching algorithm and feature table I/O)
- **M2S** (Core package implementing pairwise feature matching via m/z and retention time similarity scoring) — https://github.com/rjdossan/M2S

## Evaluation signals

- Output table contains exactly one match per feature (one-to-one correspondence enforced)
- All matched feature pairs fall within specified m/z and retention time tolerance windows
- Match confidence scores are ranked and the highest-scoring match is selected for each feature
- Output preserves and correctly maps original feature identifiers from both input tables
- No unmatched features are discarded without documentation of confidence threshold rationale

## Limitations

- M2S is designed for untargeted metabolomics; targeted methods with predefined feature lists may not benefit
- Matching quality depends critically on m/z and retention time tolerance parameters, which must be set appropriately for the LC-MS instrument and experimental conditions
- One-to-one resolution may lose true biological one-to-many relationships (e.g., isobaric metabolites or in-source fragments)
- No changelog is documented for the package, limiting reproducibility across versions

## Evidence

- [readme] Matlab package designed to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] Load two LC-MS feature tables and apply pairwise feature matching: "Load two LC-MS feature tables (each with m/z, retention time, and intensity columns) into Matlab. 2. Apply pairwise feature matching by computing similarity scores"
- [other] Filter using tolerances and resolve one-to-one correspondences: "Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives. 4. Resolve one-to-one feature correspondences by selecting the highest-confidence match"
- [other] Compile output with identifiers and confidence scores: "Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores"
