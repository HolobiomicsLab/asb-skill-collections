---
name: formula-based-network-construction
description: Use when you have a formula-assigned dataset from FT-ICR MS (or other
  compound-annotated mass spectrometry) and you want to characterize molecular transformations
  and their co-occurrence patterns—particularly in studies of DOM reactivity, fermentation,
  or oxidative treatment of organic mixtures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3762
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MoleTrans
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned
  datasets from FT-ICR MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moletrans_cq
    doi: 10.1021/acs.estlett.5c00284
    title: MoleTrans
  dedup_kept_from: coll_moletrans_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.estlett.5c00284
  all_source_dois:
  - 10.1021/acs.estlett.5c00284
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# formula-based-network-construction

## Summary

Construct molecular transformation networks from formula-assigned mass spectrometry datasets by computing pairwise mass differences, clustering them into known transformation types, and filtering by occurrence frequency to reveal the reactivity architecture of complex organic mixtures. This skill enables reactomics-based analysis of DOM and other environmental organic systems.

## When to use

You have a formula-assigned dataset from FT-ICR MS (or other compound-annotated mass spectrometry) and you want to characterize molecular transformations and their co-occurrence patterns—particularly in studies of DOM reactivity, fermentation, or oxidative treatment of organic mixtures where mass-shift patterns reflect functional group modifications or metabolic processes.

## When NOT to use

- Input is unannotated or unassigned mass features without molecular formula assignments.
- Analysis goal is compound-level identification rather than transformation characterization; use targeted MS/MS fragmentation instead.
- Dataset contains only singly abundant formulas with no repeated or overlapping transformations; network construction requires sufficient transformation co-occurrence to be meaningful.

## Inputs

- formula-assigned FT-ICR MS dataset (mass features with assigned molecular formulas)
- optional: compound-annotated results from alternative mass spectrometry approaches
- transformation pattern dictionary (known mass-shift groups and their chemical meanings)

## Outputs

- transformation network table (mass differences, formula pairs, transformation types, frequency counts)
- clustered transformation groups (annotated by functional group or metabolic modification)
- co-occurrence matrix or edge-weighted network representation

## How to apply

Load the formula-assigned DOM dataset with molecular formulas assigned to each mass feature. Compute all pairwise mass differences between assigned formulas across the sample. Identify and cluster mass differences into transformation groups by matching observed mass shifts against known transformation patterns (e.g., gains/losses of H₂O, CO₂, or other functional groups characteristic of the process). Count frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by a minimum occurrence threshold (article does not specify exact threshold; choose based on data sparsity and noise) to remove spurious mass differences. Export the final transformation network as a table containing mass differences, associated formula pairs, transformation types, and frequency counts for downstream network analysis or visualization.

## Related tools

- **MoleTrans** (Browser-based webtool for post-analysis and data mining on formula-assigned FT-ICR MS datasets; provides source code for main calculation functions and algorithms that compute pairwise mass differences, cluster transformations, and construct transformation networks.) — https://github.com/JibaoLiu/MoleTrans

## Evaluation signals

- Transformation pairs are reproducible when recomputed from the same formula-assigned dataset; no stochastic variability in clustering or filtering steps.
- Mass differences in the output table correspond exactly to known mass shifts of expected functional group modifications (e.g., ±18.01056 for H₂O, ±43.98983 for CO₂); validate against literature or internal standards.
- Frequency counts per transformation type show expected patterns relative to the underlying chemical process (e.g., oxidative treatment should enrich oxygen-adding transformations).
- Network connectivity and degree distributions are consistent with the chemical complexity of the sample and the applied treatment; sparse networks may indicate incomplete formula assignment or insufficient transformation overlap.
- Filtered transformation table is smaller than the unfiltered set; comparison confirms that spurious mass differences (below occurrence threshold) have been successfully removed.

## Limitations

- MoleTrans can only partially support combined analysis on compound-annotated results from mass spectrometry approaches other than FT-ICR MS; tool is optimized for FT-ICR MS formula-assigned data.
- Accuracy of transformation clustering depends critically on the completeness and accuracy of the input transformation pattern dictionary; missing or misnamed mass-shift patterns will lead to false negatives or misclustering.
- Article does not specify the minimum occurrence threshold for filtering; practitioners must choose empirically based on data sparsity, noise characteristics, and downstream application (e.g., network visualization may require higher thresholds to reduce visual clutter).
- No explicit handling of isomeric or isobaric formulas in the provided workflow; ambiguous formula assignments may inflate transformation pair counts.

## Evidence

- [other] MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based analysis of molecular transformations in complex organic mixtures.: "MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based"
- [other] Compute all pairwise mass differences between assigned formulas across the dataset. Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g., gains/losses of common functional groups or metabolic modifications).: "Compute all pairwise mass differences between assigned formulas across the dataset. Identify and cluster mass differences into transformation groups based on known mass-shift patterns"
- [other] Count frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences.: "Count frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results"
- [other] Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts.: "Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts"
