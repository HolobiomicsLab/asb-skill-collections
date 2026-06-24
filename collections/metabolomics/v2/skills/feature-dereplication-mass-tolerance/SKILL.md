---
name: feature-dereplication-mass-tolerance
description: Use when you have a raw XCMS CentWave feature extraction table with m/z
  values, retention times, and intensities, and you observe that multiple features
  cluster around the same nominal mass and retention window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - XCMS CentWave
  - Paramounter
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c04758
  title: Paramounter
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_paramounter_cq
    doi: 10.1021/acs.analchem.1c04758
    title: Paramounter
  dedup_kept_from: coll_paramounter_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c04758
  all_source_dois:
  - 10.1021/acs.analchem.1c04758
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-dereplication-mass-tolerance

## Summary

Collapse redundant metabolomic features extracted by XCMS CentWave by grouping peaks with similar m/z values and retention times within a user-defined mass tolerance threshold (mzdiff), then retaining only a single representative feature per group. This post-extraction step reduces feature table size and removes spurious duplicates while risking loss of true metabolic features with small mass differences.

## When to use

Apply this skill when you have a raw XCMS CentWave feature extraction table with m/z values, retention times, and intensities, and you observe that multiple features cluster around the same nominal mass and retention window. This is especially critical when peak height optimization is enabled (which increases false positive rate) or when you want to enforce a consistent mass resolution threshold across your feature set.

## When NOT to use

- Input is already a deduplicated or curated feature table from a previous dereplication step.
- You are analyzing targeted metabolomics data where each m/z represents a validated biochemical standard; dereplication may incorrectly merge distinct chemical entities.
- Retention time information is unavailable or unreliable, undermining the retention time similarity criterion used by dereplication.

## Inputs

- XCMS CentWave feature extraction table (tab-delimited or CSV with columns: feature ID, m/z, retention time, intensity)
- Mass tolerance parameter (mzdiff, in Da units)

## Outputs

- Deduplicated feature table with collapsed redundant features
- Feature count reduction report (original vs. deduplicated count)

## How to apply

Load the XCMS CentWave feature table containing m/z, retention time, and feature identifiers. Group features by retention time window and apply mass tolerance filtering: collapse all features within mzdiff mass units (default 0.001–0.01 m/z) of each other into a single representative feature, using a deterministic selection criterion such as highest intensity or earliest retention time. If you suspect true positives are being removed (e.g., isotopologues or constitutional isomers with small mass differences), disable dereplication by setting mzdiff to any negative value. The choice of mzdiff directly trades off between reducing artifacts (lower mzdiff) and preserving genuine chemical diversity (higher mzdiff or disabled). Output a deduplicated feature table with feature counts reduced and duplicate m/z entries consolidated.

## Related tools

- **XCMS CentWave** (Peak detection and feature extraction algorithm; produces the raw feature table that is deduplicated by this skill)
- **Paramounter** (Metabolomics processing pipeline that implements post-extraction dereplication using mzdiff mass tolerance and optimized peak height tuning) — github.com/HuanLab/Paramounter

## Evaluation signals

- Feature count is reduced relative to the input table; verify the reduction is proportional to the mzdiff threshold applied.
- No feature in the output table has an m/z value within mzdiff of another feature's m/z in the same retention time window (verify by pairwise distance check).
- Representative features are consistently selected (e.g., all are highest intensity or earliest retention time within each collapsed group).
- When mzdiff is set to a negative value, the output feature table is identical to the input (dereplication disabled as expected).
- Manual spot-check: inspect merged features to ensure that m/z and retention time differences are indeed smaller than the mzdiff threshold, confirming correct grouping logic.

## Limitations

- True positive metabolic features with mass differences smaller than the mzdiff tolerance threshold may be removed by mistake, particularly for isotopologues, in-source fragments, or constitutional isomers.
- The choice of mzdiff is empirical and dataset-dependent; overly stringent (low) values risk losing genuine chemical diversity, while permissive (high) values retain artifacts.
- Dereplication assumes retention time is a reliable proxy for chemical identity; co-eluting isomers or structural variants will be incorrectly collapsed.
- Peak height optimization (another Paramounter feature) can increase the false positive rate, making dereplication both necessary and potentially less effective at distinguishing true from spurious features.

## Evidence

- [readme] mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave"
- [readme] some true positive metabolic features with mass differences smaller than that value may be removed by mistake: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
- [readme] if a user wants to disable the dereplication function, set the mzdiff to be any negative value: "if a user wants to disable the dereplication function, set the mzdiff to be any negative value"
- [readme] Suggested default value: 0.001 or 0.01: "Suggested default value: 0.001 or 0.01"
- [readme] Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features: "Paramounter tunes an optimized peak height to maximize the number of true positive features. A drawback of that optimized value is the higher rate of false positive features"
