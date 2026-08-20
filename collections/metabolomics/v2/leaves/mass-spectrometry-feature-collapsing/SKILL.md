---
name: mass-spectrometry-feature-collapsing
description: Use when after XCMS CentWave feature extraction when your feature table
  contains redundant entries — multiple features with highly similar m/z and retention
  time values that represent the same metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
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

# mass-spectrometry-feature-collapsing

## Summary

Dereplication of redundant mass spectrometry features extracted by XCMS CentWave by collapsing features with similar m/z values and retention times within a user-defined mass tolerance threshold. This skill reduces feature redundancy while balancing the risk of removing true positive metabolites with mass differences smaller than the tolerance.

## When to use

After XCMS CentWave feature extraction when your feature table contains redundant entries — multiple features with highly similar m/z and retention time values that represent the same metabolite. Apply this skill when you need to reduce feature count and collapse near-duplicates, but only if you are willing to accept the trade-off that some true positive metabolites with mass differences smaller than your chosen mzdiff threshold may be inadvertently removed.

## When NOT to use

- Input is already a deduplicated or manually curated feature table — applying dereplication twice may cause unintended feature loss.
- You require all individual signals to remain distinct and traceable (e.g., for isotopologue analysis or high-resolution multiplex detection) — collapsing may obscure signal multiplicity.
- Your mass spectrometry workflow is already equipped with orthogonal dereplication (e.g., in-source or downstream filtering) — redundant application of mzdiff-based collapsing may be unnecessary.

## Inputs

- XCMS CentWave feature extraction output table with m/z values, retention times, and feature identifiers
- mzdiff parameter (mass tolerance threshold in Da, or negative value to disable)

## Outputs

- Deduplicated feature table with collapsed features and reduced feature count

## How to apply

Load the XCMS CentWave feature extraction output table (containing m/z values, retention times, and feature identifiers). Group features by applying an mzdiff mass tolerance threshold (suggested default: 0.001 or 0.01) to identify features with similar m/z and retention time values. For each group, collapse multiple features into a single representative feature using a selection criterion (e.g., highest intensity or earliest retention time). If you want to disable dereplication entirely and retain all extracted features, set mzdiff to any negative value. The rationale is that while dereplication reduces false redundancy, it may remove true positive metabolic features whose mass differences fall below the mzdiff tolerance; conversely, disabling dereplication trades increased feature count for retention of all detected signals.

## Related tools

- **XCMS CentWave** (Feature extraction algorithm that produces the m/z and retention time profiles that are subsequently collapsed by mzdiff-based dereplication)
- **Paramounter** (Implements post-extraction dereplication by using mzdiff as a mass tolerance threshold to collapse XCMS CentWave-extracted features) — github.com/HuanLab/Paramounter

## Evaluation signals

- Feature count is reduced after dereplication; the degree of reduction correlates with the mzdiff threshold — smaller mzdiff values yield fewer collapsed groups.
- No two features in the output table have m/z difference smaller than mzdiff and concurrent retention time similarity; verify by pairwise m/z and RT comparisons on the deduplicated table.
- When mzdiff is set to a negative value, the output feature table is identical to the input (dereplication skipped).
- Representative features selected for each collapsed group match the specified selection criterion (e.g., highest intensity or earliest retention time within the group).
- Output feature table schema is preserved: same columns as input (m/z, retention time, feature ID), with reduced row count.

## Limitations

- True positive metabolic features with mass differences smaller than the mzdiff tolerance value may be removed by mistake during dereplication, particularly when mzdiff is set too high.
- Dereplication does not account for biological or chemical context (e.g., isotopologues, adducts, or multiplexed signals that have legitimately similar m/z and retention times).
- The choice of mzdiff is empirical and may require iterative tuning; no universal default accommodates all instrument mass accuracies or metabolite classes.
- When peak height is simultaneously optimized in Paramounter, higher optimization may increase false positive rate and software crash likelihood, adding orthogonal uncertainty to the dereplication step.

## Evidence

- [readme] mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave: "mzdiff is used as the mass tolerance to dereplicate the features (similar m/z values and retention times) extracted by XCMS CentWave"
- [readme] some true positive metabolic features with mass differences smaller than that value may be removed by mistake: "some true positive metabolic features with mass differences smaller than that value may be removed by mistake"
- [readme] if a user wants to disable the dereplication function, set the mzdiff to be any negative value: "if a user wants to disable the dereplication function, set the mzdiff to be any negative value"
- [readme] Suggested default value: 0.001 or 0.01: "Suggested default value: 0.001 or 0.01"
- [other] Paramounter implements post-extraction dereplication by using mzdiff as a mass tolerance threshold to collapse XCMS CentWave features with similar m/z values and retention times: "Paramounter implements post-extraction dereplication by using mzdiff as a mass tolerance threshold to collapse XCMS CentWave features with similar m/z values and retention times"
