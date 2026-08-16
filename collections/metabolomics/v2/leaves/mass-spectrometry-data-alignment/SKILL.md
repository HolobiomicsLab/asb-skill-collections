---
name: mass-spectrometry-data-alignment
description: Use when you have two LC-MS feature tables (each containing m/z, retention
  time, and intensity columns) from the same or related biological samples and need
  to identify which features in dataset A correspond to which features in dataset
  B.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Matlab
  - M2S
  techniques:
  - LC-MS
  - GC-MS
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

# mass-spectrometry-data-alignment

## Summary

Align untargeted metabolomic features across two LC-MS datasets by computing pairwise similarity scores on m/z and retention time dimensions, then resolving one-to-one feature correspondences. This skill enables integration of metabolomic datasets for comparative analysis.

## When to use

You have two LC-MS feature tables (each containing m/z, retention time, and intensity columns) from the same or related biological samples and need to identify which features in dataset A correspond to which features in dataset B. This is essential when combining or comparing untargeted metabolomic experiments that were run separately.

## When NOT to use

- Input datasets have already been aligned or preprocessed with a prior feature-matching step
- You are working with targeted metabolomics (where features are predefined) rather than untargeted discovery
- The two datasets come from fundamentally different analytical platforms (e.g., one GC-MS and one LC-MS)

## Inputs

- LC-MS feature table 1 (with m/z, retention time, intensity columns)
- LC-MS feature table 2 (with m/z, retention time, intensity columns)

## Outputs

- Matched feature pairs table (original identifiers, m/z, retention times, confidence scores)
- Match confidence scores or similarity metrics

## How to apply

Load both LC-MS feature tables into Matlab. Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm. Filter candidate matches using mass-to-charge and temporal tolerances to eliminate false positives—these thresholds control specificity and should reflect your instrument's typical measurement error and expected metabolite stability. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair, ensuring each feature in dataset A maps to at most one feature in dataset B and vice versa. Compile the final matched pairs into a structured output table preserving original feature identifiers, m/z values, retention times, and match confidence scores for downstream validation.

## Related tools

- **M2S** (Matlab package that implements pairwise feature matching and one-to-one correspondence resolution for LC-MS metabolomic datasets) — https://github.com/rjdossan/M2S

## Evaluation signals

- All features in the output table have corresponding entries in both input datasets (referential integrity check)
- Match confidence scores are within the expected range (e.g., 0–1 or 0–100%) and show a clear separation between high-confidence matches and rejected pairs
- Each feature from dataset A appears in at most one matched pair (one-to-one correspondence enforced)
- Matched m/z values between datasets differ by less than the specified mass-to-charge tolerance
- Matched retention times between datasets differ by less than the specified temporal tolerance

## Limitations

- M2S requires manual setting of mass-to-charge and temporal tolerances; inappropriate thresholds can cause false positives or false negatives
- The algorithm is designed for pairwise matching only and cannot directly align >2 datasets simultaneously
- Performance and parameter sensitivity depend on the complexity of metabolomic profiles and the overlap between datasets

## Evidence

- [other] Load two LC-MS feature tables (each with m/z, retention time, and intensity columns) into Matlab. Apply pairwise feature matching by computing similarity scores across m/z and retention time dimensions using the M2S matching algorithm.: "Load two LC-MS feature tables (each with m/z, retention time, and intensity columns) into Matlab. Apply pairwise feature matching by computing similarity scores across m/z and retention time"
- [other] Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each feature pair.: "Filter candidate matches based on mass-to-charge and temporal tolerances to eliminate false positives. Resolve one-to-one feature correspondences by selecting the highest-confidence match for each"
- [other] Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores.: "Compile matched pairs into a structured output table with original feature identifiers, m/z values, retention times, and match confidence scores."
- [readme] Matlab package to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
