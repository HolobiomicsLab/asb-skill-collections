---
name: anova-feature-significance-filtering
description: Use when you have a normalized LC-MS/MS metabolite abundance matrix (e.g., from MS-DIAL preprocessing) with multiple samples across experimental groups (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - clusterProfiler
  - margheRita
  - R
  - ComplexHeatmap
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The function `h_map()` provides heatmaps based on package ComplexHeatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# anova-feature-significance-filtering

## Summary

Apply parametric ANOVA to rank metabolite features by statistical significance, then filter to retain only features meeting a stringent adjusted p-value (q-value) threshold to identify the most confident biomarkers for downstream pathway enrichment analysis.

## When to use

You have a normalized LC-MS/MS metabolite abundance matrix (e.g., from MS-DIAL preprocessing) with multiple samples across experimental groups (e.g., control vs. disease, or multiple phenotypes), and you need to identify the most statistically significant metabolite features to prioritize for mechanistic interpretation or pathway analysis. Use this skill when you want to reduce noise and focus on high-confidence signals before pathway enrichment testing.

## When NOT to use

- Input is already a pre-filtered list of known biomarkers or annotated metabolites; ANOVA is unnecessary if biological signal is already curated.
- Sample size per group is < 3; ANOVA power is compromised with very small group sizes and may yield unstable p-value estimates.
- Data have not been normalized (e.g., raw peak intensities); apply quality control, filtering, and normalization before ANOVA to avoid spurious associations driven by systematic bias.

## Inputs

- Normalized metabolite abundance matrix (rows = metabolite features, columns = samples)
- Experimental group assignments (phenotype labels for each sample)
- Feature metadata including m/z, retention time, and metabolite identifiers (PubChemCIDs if available)

## Outputs

- Filtered feature list with ANOVA p-values and adjusted q-values
- PubChemCIDs or feature identifiers for significant metabolites passing q-value threshold
- Summary statistics: count of features meeting threshold, q-value distribution

## How to apply

Execute parametric one-way ANOVA across all experimental groups for each metabolite feature in the normalized abundance matrix. Compute p-values and adjust them for multiple testing using a method such as Benjamini-Hochberg (yielding q-values). Filter features to retain only those meeting a stringent significance threshold (e.g., q-value < 1e-9 in the Urine dataset example). This threshold is chosen to balance statistical rigor with practical sample size; the margheRita workflow emphasizes that such filtering is a prerequisite for robust pathway analysis, as it ensures only high-confidence metabolite signals are propagated to ORA/MSEA. Document the number of features passing the threshold and compare across experimental polarities (e.g., RP_NEG and RP_POS) if multi-polarity data are available.

## Related tools

- **margheRita** (R package providing simplified execution of parametric and non-parametric statistical tests over a large number of features, including ANOVA for metabolite significance filtering prior to pathway analysis) — https://github.com/emosca-cnr/margheRita
- **R** (Statistical computing language used to implement ANOVA and q-value adjustment)
- **clusterProfiler** (Downstream tool used for Over Representation Analysis (ORA) on the filtered PubChemCIDs output from ANOVA filtering)

## Evaluation signals

- The number of features passing the q-value threshold is substantially smaller than the total feature count, confirming effective filtering and noise reduction.
- Q-value histogram shows a bimodal distribution with a cluster near 0 (true positives) and a plateau approaching 1 (noise), consistent with Benjamini-Hochberg correction.
- Features passing the threshold have reproducible signal across replicate samples within the same group (low coefficient of variation or high fold-change between groups).
- The filtered PubChemCID list can be successfully cross-referenced against metabolic pathway databases (KEGG, Reactome) without lookup failures, confirming feature annotation integrity.
- Downstream ORA on the filtered feature set yields enriched pathways with adjusted p-values substantially lower than when ORA is run on the unfiltered feature set, demonstrating that filtering improves signal-to-noise ratio.

## Limitations

- ANOVA assumes normality of feature abundance within groups; heavily skewed or zero-inflated distributions may require log transformation or non-parametric alternatives (Kruskal-Wallis).
- Multiple testing correction (q-value adjustment) becomes conservative with very large feature counts (> 10,000); borderline true signals may be masked if threshold is set too stringently.
- ANOVA detects differences across groups but does not capture non-linear or interaction effects; may miss metabolites with group-specific dysregulation patterns.
- The choice of q-value threshold (e.g., 1e-9 vs. 0.05) is arbitrary and dataset-dependent; thresholds should be justified by downstream pathway robustness or validated against external reference standards rather than applied universally.
- Polarity-specific filtering (RP_NEG vs. RP_POS) may yield non-overlapping feature sets; interpretation requires care to distinguish true biological differences from instrumental artifacts.

## Evidence

- [other] Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities).: "Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities)."
- [other] Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways represented in a table with pathway descriptions and visualization as a barplot.: "Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways"
- [readme] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler and simplified execution of parametric and non-parametric statistical tests over a large number of features: "simplified execution of parametric and non-parametric statistical tests over a large number of features; pathway analysis based on ORA and MSEA over various databases."
- [readme] The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS).: "The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)."
