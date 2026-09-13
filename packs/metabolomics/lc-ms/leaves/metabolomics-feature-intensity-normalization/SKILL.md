---
name: metabolomics-feature-intensity-normalization
description: Use when after peak detection and feature table construction (rows =
  features, columns = samples with intensity values) and before applying intensity-based
  filters (e.g., fold-change, phenotype score) or when preparing data for dashboard
  visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pytest
  - fermo_core
  - FERMO dashboard
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-024-50111-8
  title: FERMO
evidence_spans:
- No discussion section present in document
- See our organization-level document on [CONTRIBUTING]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fermo_2_cq
    doi: 10.1038/s41467-024-50111-8
    title: FERMO
  dedup_kept_from: coll_fermo_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-50111-8
  all_source_dois:
  - 10.1038/s41467-024-50111-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-feature-intensity-normalization

## Summary

Normalize LC-MS(/MS) metabolomics feature intensities across samples to correct for instrumental drift, varying sample loads, and batch effects before multivariate analysis or filtering. This is a preprocessing step that ensures fold-change comparisons and phenotype associations are not confounded by intensity scaling artifacts.

## When to use

Apply this skill after peak detection and feature table construction (rows = features, columns = samples with intensity values) and before applying intensity-based filters (e.g., fold-change, phenotype score) or when preparing data for dashboard visualization. Normalization is required when samples or batches show systematic differences in total ion current, sample concentration, or instrument sensitivity that are not biologically meaningful.

## When NOT to use

- Input is already a statistically normalized or log-transformed feature table — applying normalization twice risks removing biological signal
- Intensity values are already relative abundances (0–1 or percentages) — normalization would be redundant
- Analysis goal is solely qualitative (presence/absence of features) rather than quantitative (relative or absolute intensity comparison)

## Inputs

- Peak intensity table (CSV): rows = feature IDs, columns = sample identifiers, values = LC-MS intensity (or abundance) measurements
- Sample metadata (optional): group assignments, batch information, or other covariates that may inform normalization strategy

## Outputs

- Normalized peak intensity table (CSV): same dimensions as input, with intensities scaled to remove systematic technical variation
- Normalization report or parameters (e.g., scaling factors applied per sample or feature)

## How to apply

FERMO's fermo_core library integrates metabolomics data with orthogonal sample metadata. Normalization should be applied to the peak intensity table (CSV format with feature IDs as rows and sample abundances as columns) to bring all intensities to a common scale before fold-change calculation or group-wise comparisons. The normalized feature table then becomes the input to downstream filtering operations (e.g., fold-change filters that compare feature intensities across specified group sets). Validate that normalized intensities remain non-negative, that relative ranking of features within samples is preserved, and that the distribution of intensities post-normalization does not introduce artificial clustering or artifact patterns in dashboard visualizations.

## Related tools

- **fermo_core** (Metabolomics data integration and preprocessing library; performs fold-change calculations and intensity comparisons after normalization) — https://github.com/fermo-metabolomics/fermo_core
- **FERMO dashboard** (GUI for loading normalized peak tables, applying intensity-based filters (fold-change, phenotype score), and visualizing normalized feature abundances) — https://github.com/fermo-metabolomics/FERMO
- **pytest** (Unit testing framework to validate normalization correctness (e.g., verify intensity distributions, check for negative values, confirm group comparability))

## Evaluation signals

- Normalized intensities are non-negative and span a reasonable numeric range (no NaN or infinite values)
- Relative ranking of features within each sample is preserved (high-intensity features remain high-intensity after normalization)
- Mean intensity or distribution metrics across sample groups are comparable post-normalization, reducing systematic batch/technical bias
- Downstream fold-change calculations on normalized data are reproducible and do not show spurious group separation driven by intensity scaling alone
- Visual inspection of normalized data in the FERMO dashboard shows balanced intensity distributions across samples without artificial clustering or outliers introduced by normalization

## Limitations

- Normalization method choice (e.g., quantile, median, total ion current, internal standard) can influence downstream filter results; no single best method is mentioned in the README or task description
- If sample groups have genuinely different total ion currents due to biological differences (e.g., differing metabolite abundance), aggressive normalization may obscure these differences
- Very sparse feature tables (many zeros) may not normalize well with some methods; method robustness to sparsity is not discussed in the provided context

## Evidence

- [readme] FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization.: "FERMO integrates metabolomics data with orthogonal data such as phenotype information for rapid, biochemometric, hypothesis-driven prioritization."
- [readme] As minimal requirement, FERMO takes LC-MS(/MS) metabolomics data, which it can integrate with a range of optional orthogonal data formats.: "As minimal requirement, FERMO takes LC-MS(/MS) metabolomics data, which it can integrate with a range of optional orthogonal data formats."
- [other] Implement the fold-change calculation logic comparing feature intensities across specified groups.: "Implement the fold-change calculation logic comparing feature intensities across specified groups."
