---
name: metabolomic-feature-table-interpretation
description: Use when after quality control, filtering, and normalization of an MS-DIAL-derived
  feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt),
  when you have samples assigned to discrete experimental classes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3676
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - margheRita
  - R
  - clusterProfiler
  - ComplexHeatmap
  - notame
  - pcaMethods
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
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

# metabolomic-feature-table-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interprets preprocessed LC-MS/MS metabolomic feature tables through univariate and multivariate statistical testing to identify metabolites with significant abundance differences across experimental groups, followed by pathway analysis to contextualize findings within biological systems.

## When to use

After quality control, filtering, and normalization of an MS-DIAL-derived feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt), when you have samples assigned to discrete experimental classes (e.g., AA, DD, MM phenotypes) and need to identify which metabolic features show statistically significant differences in abundance across those classes and map them to affected biological pathways.

## When NOT to use

- Input feature table has not been normalized or quality-filtered (run preprocessing steps first)
- Samples lack clear experimental class assignments or metadata (univariate testing requires group labels)
- Only exploratory/unsupervised analysis is planned (use PCA or clustering instead)
- Sample size per class is very small (n < 3 per group), reducing statistical power and validity of ANOVA assumptions

## Inputs

- Normalized feature abundance matrix (e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt format)
- Sample metadata table with experimental class assignments (e.g., AA/DD/MM phenotypes)
- margheRita data object (created via load and metadata assignment)

## Outputs

- Univariate statistical results table (Feature_ID, metabolite name, ANOVA F-statistic, p-value, q-value, effect size)
- Filtered significant features list (q-value-thresholded)
- Pathway enrichment results (ORA or MSEA output with pathway names, p-values, and member features)
- Optional: heatmap visualization (via ComplexHeatmap integration) showing significant features across sample classes

## How to apply

Load the normalized feature table and sample metadata into margheRita. Apply the univariate() function to compute ANOVA F-statistics and p-values (or non-parametric alternatives for non-normal data) across all class levels for each metabolite feature; margheRita automatically applies Benjamini–Hochberg FDR correction during this step. Use select_sign_features() to filter significant features at a chosen q-value cutoff (e.g., q < 0.05). Extract a results table containing Feature_ID, metabolite names, ANOVA statistics, p-values, q-values, and effect sizes. Subsequently apply pathway analysis using Over-Representation Analysis (ORA) or Metabolite Set Enrichment Analysis (MSEA) via clusterProfiler integration to assign significant features to metabolic pathways and databases, providing biological context for the statistical findings.

## Related tools

- **margheRita** (Executes univariate ANOVA and non-parametric statistical tests; filters significant features; exports results tables and integrates pathway analysis via clusterProfiler) — https://github.com/emosca-cnr/margheRita
- **clusterProfiler** (Performs Over-Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA) on significant feature lists to assign metabolic pathway membership)
- **ComplexHeatmap** (Generates heatmap visualizations of significant features across sample classes via margheRita's h_map() function)
- **notame** (Alternative/complementary R package for non-targeted LC-MS metabolomic profiling, including feature-wise statistical tests and multivariate models; margheRita can export to notame format via as.metaboset()) — https://github.com/hanhineva-lab/notame
- **pcaMethods** (Provides Principal Component Analysis capability used by margheRita's mR_pca() function for multivariate exploratory analysis alongside univariate testing)

## Examples

```
univariate_results <- margheRita::univariate(mR_data, method='anova'); sig_features <- margheRita::select_sign_features(univariate_results, q_cutoff=0.05); pathway_enrich <- margheRita::pathway_analysis(sig_features, method='ORA', database='kegg')
```

## Evaluation signals

- Results table contains non-null Feature_ID, metabolite names, q-values, and p-values for all tested features; no missing values in critical columns
- Q-values are greater than or equal to corresponding p-values (FDR correction validated); selected features meet the specified q-value threshold (e.g., all q < 0.05 in filtered output)
- Effect sizes or ANOVA F-statistics are reasonable (F > 1 and increasing with effect magnitude); feature counts post-filtering are consistent with statistical expectations for the experiment
- Pathway enrichment results reference recognized metabolic databases (e.g., KEGG, Reactome, BioCyc) and report significant pathways with p-values; member features in each pathway match the significant feature list
- Heatmap visualization (if generated) shows clear differential abundance patterns across experimental classes for significant features, visually confirming statistical results

## Limitations

- ANOVA assumes normality of feature abundances within each class; if violated, non-parametric alternatives (Kruskal–Wallis) should be applied instead, which margheRita supports
- FDR correction (Benjamini–Hochberg) is appropriate for large feature sets but assumes independence of tests; highly correlated metabolites may reduce effective multiple-testing adjustment stringency
- Pathway enrichment depends on database completeness and metabolite annotation accuracy; unannotated or misidentified features will not map to pathways, reducing biological interpretability
- Statistical significance does not imply biological significance; effect sizes and pathway coherence should be examined to prioritize findings for validation
- MS-DIAL processing parameters (peak picking, alignment, m/z tolerance) upstream of normalization influence feature quality; severe artifacts or missing values pre-filtering can bias statistical results

## Evidence

- [other] Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature. Use select_sign_features() to filter significant features based on q-value threshold (Benjamini–Hochberg FDR correction applied during univariate or select_sign_features step).: "Apply univariate() function to compute ANOVA F-statistics and p-values across the three class levels for each metabolite feature. Use select_sign_features() to filter significant features based on"
- [readme] simplified execution of parametric and non-parametric statistical tests over a large number of features; pathway analysis based on ORA and MSEA over various databases: "simplified execution of parametric and non-parametric statistical tests over a large number of features; pathway analysis based on ORA and MSEA over various databases"
- [other] Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes.: "Extract and tabulate the results including feature identifiers, ANOVA statistics, p-values, q-values, and effect sizes"
- [intro] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler: "margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler"
- [intro] The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS).: "The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)"
