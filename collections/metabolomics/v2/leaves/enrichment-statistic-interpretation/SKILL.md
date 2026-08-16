---
name: enrichment-statistic-interpretation
description: Use when after performing two-group or multi-group differential analysis
  on a lipidomics dataset and obtaining log fold-change (logFC) values for individual
  lipid molecules, use this skill to determine whether specific lipid classes, chain
  lengths, or unsaturation patterns are systematically up- or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
  tools:
  - lipidr
  - R
  - limma
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# enrichment-statistic-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret lipid set enrichment analysis (LSEA) results ranked by log fold-change to identify significantly enriched or depleted lipid classes and chain properties in differential lipidomics experiments. This skill extracts and visualizes enrichment statistics to reveal preferential regulation patterns across lipid molecular features.

## When to use

After performing two-group or multi-group differential analysis on a lipidomics dataset and obtaining log fold-change (logFC) values for individual lipid molecules, use this skill to determine whether specific lipid classes, chain lengths, or unsaturation patterns are systematically up- or down-regulated rather than occurring by chance.

## When NOT to use

- Input lipid abundance data has not been log-transformed or normalized — LSEA assumes properly preprocessed data
- No valid de_analysis result object exists; differential analysis must be completed first with logFC values computed
- Sample size is very small (n < 3 per group) — enrichment statistics lack power and may be unreliable

## Inputs

- LipidomicsExperiment object with log-transformed, normalized lipid abundance data
- de_analysis result object containing logFC values and p-values from two-group or multi-group differential analysis

## Outputs

- significant_lipidsets table with enrichment scores, adjusted p-values, and lipid set identities (lipid classes, chain features, unsaturation patterns)
- Visualization plots showing enriched lipid sets ranked by enrichment score

## How to apply

Call the lsea() function with rank.by='logFC' parameter on a de_analysis result object containing logFC values from your differential comparison (e.g., benign vs. cancer or cancer vs. metastasis). The function ranks lipid molecules by their logFC values and computes enrichment statistics for predefined lipid sets (classes, chain-length features, unsaturation patterns). Extract the significant_lipidsets table from the lsea output and filter for lipid sets meeting your significance threshold (typically adjusted p-value < 0.05). Visualize the enriched lipid sets alongside their enrichment scores and adjusted p-values to interpret which lipid molecular features show preferential regulation in your biological comparison.

## Related tools

- **lipidr** (Implements lsea() function for ranking lipids by logFC and computing enrichment statistics for predefined lipid sets (classes, chain properties, unsaturation)) — https://github.com/ahmohamed/lipidr
- **limma** (Required dependency for differential analysis (de_analysis) that produces the logFC values input to LSEA)

## Examples

```
lsea_result <- lsea(de_analysis_object, rank.by='logFC'); significant_sets <- lsea_result$significant_lipidsets; plot(lsea_result)
```

## Evaluation signals

- Significant lipid sets (adjusted p-value < 0.05) are identifiable and biologically coherent (e.g., a lipid class or chain-length feature, not individual lipids)
- Enrichment scores and direction (positive/negative) align with the biological hypothesis — e.g., if PCs/PGs are upregulated in cancer vs. benign, LSEA should highlight PC and PG classes with positive enrichment scores
- The significant_lipidsets table contains both enriched (high logFC rank) and depleted (low logFC rank) lipid sets, reflecting actual differential regulation patterns
- Visualizations clearly distinguish significant from non-significant lipid sets and rank them by enrichment magnitude
- Results are reproducible when re-running lsea() on the same de_analysis object with identical rank.by='logFC' parameter

## Limitations

- LSEA depends on the quality and completeness of the predefined lipid sets; if a lipid class or feature is poorly represented or mislabeled, enrichment may be missed or miscalculated
- Enrichment interpretation assumes that the logFC ranking is biologically meaningful; if differential analysis results are confounded by batch effects or unmeasured covariates, enrichment statistics may reflect artifacts
- No enrichment signal will be detected if all lipids in a set have similar logFC values; the method requires sufficient variability across the ranked list
- Multiple testing correction (e.g., Benjamini–Hochberg FDR) is applied; highly correlated lipid sets may reduce power if enrichment is spread across multiple related sets

## Evidence

- [other] Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid classes and chain unsaturations.: "Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid"
- [other] Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets.: "Call lsea() function with rank.by='logFC' parameter to rank lipid molecules by log fold-change and compute enrichment statistics for predefined lipid sets."
- [other] Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold.: "Extract the significant_lipidsets table from lsea output, filtering for lipid classes and chain-length features meeting the significance threshold."
- [readme] A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns.: "A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns."
- [intro] A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues.: "A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues."
