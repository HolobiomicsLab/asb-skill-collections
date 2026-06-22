---
name: mass-difference-transformation-pair-derivation
description: Use when you have a formula-assigned DOM dataset from FT-ICR MS (or other mass spectrometry with compound annotations) and need to characterize how molecular transformations occur across the sample—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - MoleTrans
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

# mass-difference-transformation-pair-derivation

## Summary

Derive transformation pairs and characterize molecular transformations by computing pairwise mass differences between formula-assigned DOM features and clustering them into transformation groups based on known mass-shift patterns. This reactomics-based approach enables identification of molecular modification networks in complex organic mixtures analyzed by FT-ICR MS.

## When to use

Apply this skill when you have a formula-assigned DOM dataset from FT-ICR MS (or other mass spectrometry with compound annotations) and need to characterize how molecular transformations occur across the sample—e.g., to understand DOM reactivity in fermentation, persulfate pretreatment, or other environmental processes. Use it specifically when you want to move beyond individual molecular formula composition to network-level understanding of functional group gains/losses and metabolic modifications.

## When NOT to use

- Input is already a pre-computed transformation network or reactomics matrix—this skill derives transformation pairs de novo and is redundant if that step is complete.
- Formula assignment is unreliable or absent; mass-difference-based clustering requires confident molecular formula identity for each feature.
- You require single-feature level annotation (e.g., functional group predictions for isolated compounds) rather than network-level transformation characterization.

## Inputs

- Formula-assigned DOM dataset from FT-ICR MS with molecular formulas assigned to each mass feature
- Optional: compound-annotated results from alternative mass spectrometry approaches
- Known mass-shift pattern definitions (transformation classes and their expected m/z shifts)

## Outputs

- Transformation network table with mass differences, associated formula pairs, transformation types, and frequency counts
- Filtered transformation pair set (spurious differences removed via occurrence threshold)
- Reactomics transformation matrix for network visualization and analysis

## How to apply

Load the formula-assigned DOM dataset with each mass feature linked to its molecular formula. Compute all pairwise mass differences between assigned formulas across the entire dataset. Identify and cluster these mass differences into transformation groups using known mass-shift patterns (e.g., gains/losses of H₂, CH₂, O, N, or other common functional group modifications). Count the frequency and co-occurrence of each transformation pair within the sample. Filter transformation pairs by a minimum occurrence threshold to remove spurious mass differences and retain only biologically or chemically plausible transformations. Export the final transformation network as a structured table annotated with mass differences, associated formula pairs, transformation types, and frequency counts for downstream visualization and interpretation.

## Related tools

- **MoleTrans** (Browser-based webtool for post-analysis and data mining on formula-assigned datasets; provides calculation functions and algorithms for transformation-pair derivation, clustering, and export; supports FT-ICR MS and alternative mass spectrometry compound-annotated results.) — https://github.com/JibaoLiu/MoleTrans

## Evaluation signals

- All pairwise mass differences are computed without gaps (completeness check: number of pairs ≈ n×(n−1)/2 for n formulas, accounting for symmetry or duplicate removal logic).
- Transformation clusters align with known biochemical and analytical mass-shift patterns (e.g., H₂ ≈ 2.0157, CH₂ ≈ 14.0157, O ≈ 15.9949 Da with <5 ppm tolerance typical for FT-ICR MS).
- Frequency distribution of transformation pairs is reasonable (no single transformation class dominates >80% unless biological justification is strong; filtered set is substantially smaller than unfiltered, indicating effective spurious-difference removal).
- Transformation network is acyclic or contains only expected cycles (e.g., bidirectional transformations between pairs); large cycles suggest clustering errors.
- Output table schema matches specification (columns: mass_difference, formula_pair, transformation_type, frequency_count, co-occurrence_metrics); no null entries in required fields after filtering.

## Limitations

- Mass-difference approach assumes mass resolution sufficient to distinguish intended transformations from random noise; FT-ICR MS is required for complex mixtures; lower-resolution instruments may produce unreliable transformation calls.
- Spurious mass differences can arise from unrelated formula pairs sharing coincidental m/z shifts; minimum occurrence threshold must be calibrated per study (no universal cutoff provided in source material).
- Known mass-shift pattern library must be curated and up-to-date; missed or incorrectly classified transformations will bias network structure and biological interpretation.
- Reactomics analysis assumes transformation pairs reflect true molecular modifications; alternative explanations (e.g., instrumental artifacts, isomeric variation, sample mixing) are not distinguished by mass difference alone.
- Partial support for non-FT-ICR MS data (e.g., other mass spectrometry with compound annotations) may reduce reliability due to lower mass accuracy and resolution.

## Evidence

- [other] Compute all pairwise mass differences between assigned formulas across the dataset: "Compute all pairwise mass differences between assigned formulas across the dataset. 3. Identify and cluster mass differences into transformation groups based on known mass-shift patterns"
- [other] Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences: "Filter transformation pairs by minimum occurrence threshold to remove spurious mass differences. 6. Export the final transformation network as a table"
- [other] MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based analysis of molecular transformations in complex organic mixtures: "MoleTrans provides source code for main calculation functions and algorithms that enable post-analysis and data mining on formula-assigned datasets from FT-ICR MS, which supports reactomics-based"
- [readme] MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated results based on other mass spectrometry: "MoleTrans is a webtool for post analysis and data mining on the formula assigned datasets from FT-ICR MS. Alternatively, it can partialy support the combined analysis on the compound annotated"
- [other] gains/losses of common functional groups or metabolic modifications: "Identify and cluster mass differences into transformation groups based on known mass-shift patterns (e.g., gains/losses of common functional groups or metabolic modifications)"
