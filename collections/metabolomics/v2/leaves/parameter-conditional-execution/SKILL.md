---
name: parameter-conditional-execution
description: Use when when a post-processing step (such as dereplication) risks removing
  true positive signals due to overly strict thresholds, and you need the option to
  retain raw or unfiltered output without code branching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
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

# parameter-conditional-execution

## Summary

Conditionally enable or disable a processing step (e.g., feature dereplication) by setting a control parameter to a sentinel value (e.g., negative number). This skill allows users to bypass intermediate transformations when they conflict with downstream analysis goals or when true signal may be lost.

## When to use

When a post-processing step (such as dereplication) risks removing true positive signals due to overly strict thresholds, and you need the option to retain raw or unfiltered output without code branching. Specifically in metabolomics workflows where mzdiff-based dereplication of XCMS CentWave features may incorrectly collapse features with mass differences smaller than the tolerance, sacrificing sensitivity for specificity.

## When NOT to use

- When the processing step is mandatory by design or downstream dependency (e.g., if the consumer tool requires deduplicated input).
- When the parameter should instead control the threshold magnitude rather than enable/disable the step; use conditional execution only for binary on/off decisions.
- When performance or memory constraints make retaining unfiltered data unfeasible; the no-op path should still be lightweight.

## Inputs

- Feature table from XCMS CentWave extraction (m/z values, retention times, feature identifiers, intensities)
- Control parameter value (e.g., mzdiff mass tolerance threshold in Da)

## Outputs

- Feature table, either with dereplication applied (features collapsed by mass and retention time similarity) or with all features retained (when control parameter is negative)

## How to apply

Implement a conditional check on the control parameter value before executing the processing step. If the parameter is set to a sentinel value (e.g., any negative number for mzdiff), skip the transformation and pass input features through unchanged. Otherwise, apply the normal processing logic with the parameter as the threshold. In the Paramounter context, set mzdiff to a negative value to disable dereplication entirely, allowing all XCMS CentWave-extracted features to be retained in the output feature table. Document the sentinel convention clearly so users understand that negative values suppress the step rather than invert its behavior.

## Related tools

- **XCMS CentWave** (Performs peak detection and feature extraction; output features are candidates for dereplication or bypass via this skill)
- **Paramounter** (Implements mzdiff-based dereplication logic with conditional execution; enables users to disable dereplication by setting mzdiff to negative) — github.com/HuanLab/Paramounter

## Evaluation signals

- When mzdiff is set to any negative value, output feature table row count equals input row count (no features removed).
- When mzdiff is set to a positive value, output feature count is ≤ input feature count, with collapsed groups verified by identical or near-identical m/z and retention time pairs.
- Parameter value is correctly read and parsed before the conditional check, with no crashes or silent fallback to default behavior.
- Output schema (column names, data types) is consistent regardless of whether the step was executed or bypassed.
- User-facing documentation clearly explains the sentinel value convention to avoid confusion (e.g., 'set mzdiff < 0 to disable dereplication').

## Limitations

- Disabling dereplication may inflate false positive feature counts, increasing memory and downstream computational burden.
- True positive metabolic features with mass differences smaller than the mzdiff tolerance are at risk of removal even when dereplication is enabled; users must validate that the chosen mzdiff threshold is biologically appropriate.
- Conditional execution via sentinel value is implicit and non-obvious; poor documentation may lead users to believe a negative mzdiff parameter inverts the tolerance or applies different logic rather than disabling the step entirely.

## Evidence

- [readme] mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave"
- [readme] some true positive metabolic features with mass differences smaller than that value may be removed by mistake: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
- [readme] if a user wants to disable the dereplication function, set the mzdiff to be any negative value: "if a user wants to disable the dereplication function, set the mzdiff to be any negative value"
- [other] When mzdiff is set to a negative value, the dereplication function is disabled entirely, allowing users to bypass feature collapsing: "When mzdiff is set to a negative value, the dereplication function is disabled entirely, allowing users to bypass feature collapsing"
