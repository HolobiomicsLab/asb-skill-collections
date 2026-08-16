---
name: metabolite-pathway-annotation-mapping
description: Use when after peak detection and statistical association or classification analysis has identified a set of significant peaks, use this skill when you need to move from individual feature-level results (peak intensities, p-values, importance scores) to functional biological interpretation via.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - SMART
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-pathway-annotation-mapping

## Summary

Maps detected metabolite peaks to known metabolite identities and then associates them with biochemical pathways to compute pathway enrichment scores and significance. This enables interpretation of metabolomics results at the systems level by linking individual features to metabolic processes.

## When to use

After peak detection and statistical association or classification analysis has identified a set of significant peaks, use this skill when you need to move from individual feature-level results (peak intensities, p-values, importance scores) to functional biological interpretation via pathway enrichment. Specifically apply it when you have: (1) a peak table with detected m/z and retention time values, (2) statistically significant peak identifiers from ANCOVA, PLS/PLS-DA, or other association tests, and (3) access to a metabolite/pathway database to enable peak-to-metabolite and metabolite-to-pathway mapping.

## When NOT to use

- Peak annotation is unavailable or unreliable (e.g., low MS/MS spectral match scores, high mass error >10 ppm). Pathway mapping requires confident peak-to-metabolite identity assignments; poor annotation propagates uncertainty into pathway statistics.
- No appropriate metabolite-pathway database is accessible for the organism or tissue type under study. IOPA relies on curated pathway knowledge; absence of domain-specific pathway annotations limits interpretability.
- The analysis goal is exploratory feature selection or classification performance optimization rather than biological mechanism discovery. Pathway enrichment adds interpretive value but increases computational complexity; omit it if the endpoint is a predictive model rather than pathway identification.

## Inputs

- preprocessed peak table (feature matrix: samples × peaks with m/z, retention time, and intensity values)
- peak identifiers from prior statistical analysis (significant peaks with p-values, effect sizes, or importance scores)
- peak annotation/identity assignments (m/z-to-metabolite mappings)
- metabolite-to-pathway association database or reference

## Outputs

- pathway enrichment results table (pathway identifiers, member metabolites, aggregated statistics, enrichment score, p-value or significance threshold)
- ranked pathway list ordered by enrichment significance or effect size
- annotated peak-to-pathway mapping (traceability of individual peaks to pathways)

## How to apply

First, map each detected peak to a known metabolite identity using m/z matching, retention time alignment, and/or MS/MS fragmentation data against a reference database (e.g. HMDB, KEGG). Second, for each identified metabolite, retrieve its associated biochemical pathways from a pathway knowledge base. Third, for each pathway, aggregate statistical evidence (p-values, effect sizes, or feature importance scores) from all mapped metabolites within that pathway. Fourth, compute pathway-level enrichment scores and significance (e.g., via hypergeometric test, Fisher's exact test, or pathway impact analysis) to rank pathways by their association with the experimental condition or classification outcome. The rationale is that peaks with similar biological roles (co-mapping to the same pathway) provide stronger evidence of pathway dysregulation than individual features alone, and that systems-level interpretation requires linking features to their functional context.

## Related tools

- **SMART** (Implements the IOPA (Integrative Omics Pathway Analysis) module to dispatch metabolite-pathway mapping, pathway enrichment scoring, and significance computation within an integrated metabolomics pipeline.) — https://github.com/YuJenL/SMART
- **R** (Execution environment for SMART; used to load peak tables, parse peak-to-metabolite mappings, construct metabolite-pathway associations, and compute pathway enrichment statistics.)

## Evaluation signals

- All significant peaks from the prior statistical analysis are mapped to at least one metabolite identity (100% traceability; peaks without annotation are flagged separately).
- Pathway enrichment scores are correctly computed and aggregate statistics from all member metabolites; verify by spot-checking one pathway's manual computation against the reported score.
- Pathway significance (p-values) are monotonically related to enrichment magnitude: pathways with larger effect sizes or more significant member peaks have lower p-values.
- Pathway results are internally consistent (e.g., a peak mapped to multiple pathways contributes to all relevant pathways; total metabolite count sums correctly).
- Output includes a peak-to-pathway traceability table showing which detected peaks map to which pathways, enabling validation against domain knowledge or published pathway databases.

## Limitations

- Pathway enrichment accuracy depends on the completeness and accuracy of the reference metabolite-pathway database; missing or incorrect pathway annotations introduce false negatives or positives.
- Peak annotation (m/z-to-metabolite mapping) is often ambiguous, especially for low-mass or isobaric metabolites; multiple annotations per peak can confound pathway assignments unless handled via probability weighting or consensus methods.
- Pathway analysis assumes independence among pathways; in reality, metabolic networks are interconnected and share substrates or cofactors, potentially inflating shared pathway significance.
- Small sample sizes or low statistical power in the prior association analysis can propagate to weak pathway signals even if individual peaks are nominally significant; pathway-level evidence is only as strong as the underlying peak statistics.

## Evidence

- [other] For IOPA: map peaks to metabolite identities, construct metabolite-pathway associations, and compute pathway enrichment scores and significance.: "For IOPA: map peaks to metabolite identities, construct metabolite-pathway associations, and compute pathway enrichment scores and significance."
- [intro] Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA): "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
- [intro] SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis"
- [intro] Post-analysis: Execute peak identification and concentration calibration: "Post-analysis: Execute peak identification and concentration calibration"
