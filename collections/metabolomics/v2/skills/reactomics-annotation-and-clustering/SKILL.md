---
name: reactomics-annotation-and-clustering
description: Use when you have a formula-assigned dataset from FT-ICR MS or other mass spectrometry with molecular formulas assigned to each mass feature, and you want to identify and quantify the molecular transformations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MoleTrans
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.estlett.5c00284
  title: MoleTrans
evidence_spans:
- MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reactomics-annotation-and-clustering

## Summary

Derive molecular transformation networks from formula-assigned mass spectrometry datasets by computing pairwise mass differences, clustering them into transformation groups, and filtering by occurrence frequency. This skill enables characterization of molecular reactivity and chemodiversity in complex organic mixtures such as dissolved organic matter (DOM).

## When to use

You have a formula-assigned dataset from FT-ICR MS or other mass spectrometry with molecular formulas assigned to each mass feature, and you want to identify and quantify the molecular transformations (e.g., gains/losses of functional groups, metabolic modifications) that occur within a sample or across conditions. Apply this skill when your analysis goal is to build a transformation network that reveals reaction pathways or DOM reactivity patterns rather than to annotate individual compounds.

## When NOT to use

- Input is already a feature table without molecular formula assignments — this skill requires formula-assigned datasets.
- The analysis goal is compound identification or annotation rather than characterization of molecular transformations and reaction pathways.
- Dataset contains only a single mass feature or too few features to compute meaningful pairwise differences.

## Inputs

- Formula-assigned dataset from FT-ICR MS analysis (each mass feature linked to a molecular formula)
- Optional: compound-annotated results from other mass spectrometry approaches (partial support)

## Outputs

- Transformation network table with mass differences, associated formula pairs, transformation types, and occurrence frequencies
- Clustered transformation groups (categorized by functional group modifications or metabolic changes)

## How to apply

Load the formula-assigned dataset (molecular formulas with associated mass features) into MoleTrans or a compatible post-processing framework. Compute all pairwise mass differences between assigned formulas across the dataset. Identify and cluster mass differences into transformation groups by matching observed mass shifts against known patterns (e.g., losses of H₂O, CO₂, or gains of O, S). Count frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by a minimum occurrence threshold (article does not specify a default; threshold is user-configurable) to remove spurious mass differences arising from noise or random variation. Export the final transformation network as a table annotated with mass differences, associated formulas, transformation types, and frequency counts, suitable for downstream visualization or network analysis.

## Related tools

- **MoleTrans** (Browser-based webtool for post-analysis and data mining on formula-assigned FT-ICR MS datasets; implements core calculation functions for mass difference computation, transformation clustering, and frequency-based filtering.) — github.com/JibaoLiu/MoleTrans

## Evaluation signals

- All pairwise mass differences are computed and clustered consistently; no duplicate transformation pairs are reported.
- Transformation groups match known mass-shift patterns (e.g., common functional group losses/gains documented in the output); transformation types are correctly labeled.
- Frequency counts for each transformation pair are non-negative integers; the minimum occurrence threshold is applied uniformly across all pairs, and pairs below threshold are excluded.
- Export table schema includes mass differences, associated formula pairs, transformation types, and frequency counts; no critical columns are missing or NaN.
- Spurious mass differences (one-off occurrences or noise-driven pairs) are successfully removed; network complexity is reduced relative to raw pairwise differences.

## Limitations

- MoleTrans can only partially support combined analysis on compound-annotated results from mass spectrometry approaches other than FT-ICR MS; full integration with other platforms is not guaranteed.
- The skill depends on accurate and complete formula assignment in the input dataset; systematic errors or missing formulas in the source data will propagate to the transformation network.
- Minimum occurrence threshold is user-configurable and not standardized; different thresholds may yield substantially different transformation networks, complicating cross-study comparisons.
- The method identifies mass-shift patterns but does not mechanistically explain the underlying chemical reactions; interpretation of transformation types requires domain knowledge and external chemical reference data.

## Evidence

- [other] MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based analysis of molecular transformations in complex organic mixtures.: "MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based"
- [other] Compute all pairwise mass differences between assigned formulas across the dataset. Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g., gains/losses of common functional groups or metabolic modifications). Count frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences.: "Compute all pairwise mass differences between assigned formulas across the dataset. Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g.,"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry.: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated"
- [other] Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts.: "Export the final transformation network as a table with mass differences, associated formulas, transformation types, and frequency counts."
