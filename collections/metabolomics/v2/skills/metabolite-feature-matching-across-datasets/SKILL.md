---
name: metabolite-feature-matching-across-datasets
description: Use when you have two independent LC-MS untargeted metabolomic feature
  tables (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - M2S
  - Matlab
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c03592
  title: m2s
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_m2s
    doi: 10.1021/acs.analchem.1c03592
    title: m2s
  dedup_kept_from: coll_m2s
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

# metabolite-feature-matching-across-datasets

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match untargeted metabolomic features across two LC-MS datasets by comparing retention time and mass-to-charge ratio signatures using the M2S Matlab package. This skill enables researchers to identify and link corresponding metabolite features between independent LC-MS runs, producing a consolidated feature correspondence table with matching scores.

## When to use

You have two independent LC-MS untargeted metabolomic feature tables (e.g., from different instruments, sample batches, or experimental replicates) and need to establish feature correspondence across them to enable comparative metabolomics analysis, multi-cohort integration, or validation of feature detection across runs.

## When NOT to use

- Input data is already a pre-aligned or single feature table from a unified analysis pipeline (M2S is for cross-dataset matching, not within-dataset feature deconvolution)
- Features lack retention time or m/z information; M2S relies on these two dimensions for similarity computation
- You require targeted metabolite identification rather than untargeted feature correspondence (M2S matches features, not compound IDs or chemical structures)

## Inputs

- LC-MS untargeted metabolomic feature table 1 (tabular: feature ID, retention time, m/z, intensity or abundance)
- LC-MS untargeted metabolomic feature table 2 (tabular: feature ID, retention time, m/z, intensity or abundance)

## Outputs

- Matched feature table (tabular: feature pairs from dataset 1 and 2, matching scores, retention time deltas, m/z deltas)

## How to apply

Load both feature datasets into Matlab, ensuring each contains retention time and mass-to-charge ratio (m/z) information for detected features. Initialize the M2S package with both feature tables as inputs. Execute the M2S matching algorithm, which identifies corresponding features by computing similarity scores based on retention time and m/z alignment (the algorithm uses these two dimensions as the primary matching criteria). The algorithm produces a matched feature table annotated with feature correspondences and matching scores, which can be exported for downstream analysis. Inspect the matching scores to assess confidence in correspondences and filter by a quality threshold appropriate to your analytical tolerance.

## Related tools

- **M2S** (Matlab package that implements the matching algorithm for untargeted metabolomic features across two LC-MS datasets using retention time and m/z similarity) — https://github.com/rjdossan/M2S
- **Matlab** (Runtime and numerical computing environment required to execute M2S package and load/manipulate feature tables)

## Evaluation signals

- Output matched feature table contains all expected columns: feature identifiers from both datasets, retention time and m/z for each feature, and a matching score (0–1 or similar scale)
- Matching scores are symmetric: if feature A from dataset 1 matches feature B from dataset 2 with score S, inspect whether the reverse correspondence is consistent
- No feature from one dataset is matched to multiple features in the other (one-to-one cardinality, or expected one-to-many is documented)
- Retention time and m/z deltas between matched features are within expected instrumental tolerance (e.g., <0.5 min RT, <5 ppm m/z, or user-specified thresholds)
- Matched feature count is non-zero and reasonable relative to total feature count in each input table (e.g., >50% if datasets are expected to be similar)

## Limitations

- M2S matching relies solely on retention time and m/z; features with identical m/z but different chemical identity (isomers, adducts) may produce spurious matches if retention times are similar
- Matching performance depends on the accuracy of retention time calibration and mass calibration across the two LC-MS runs; systematic shifts or drift will reduce correspondence accuracy
- The algorithm and thresholds for retention time and m/z tolerance are not documented in the README; users must either infer defaults or consult source code or original publication
- No explicit handling of one-to-many or many-to-one feature correspondences (e.g., when dataset 2 resolves a single feature in dataset 1 into multiple peaks)

## Evidence

- [other] M2S is a Matlab package designed to match untargeted metabolomic features of two LC-MS datasets: "Matlab package to match untargeted metabolomic features of two LC-MS datasets"
- [other] The workflow involves loading two feature datasets, initializing M2S, executing the matching algorithm based on retention time and m/z similarity, and exporting matched features with scores: "Execute the M2S matching algorithm to identify and link corresponding features across the two datasets based on retention time and mass-to-charge ratio similarity"
- [other] M2S produces a matched feature table as output: "Generate and export the matched feature table containing feature correspondences and matching scores"
