---
name: coefficient-of-variation-calculation-and-filtering
description: Use when after loading and applying minimum non-missing-value thresholds
  to an omics expression dataset (proteomics, metabolomics, or other panomics data).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - PMart Shiny App
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# coefficient-of-variation-calculation-and-filtering

## Summary

Calculate coefficient of variation (CV) for each biomolecule in an omics expression matrix and apply a maximum CV threshold to remove high-variance biomolecules that may represent noise or technical artifacts. This filtering step is typically applied after minimum non-missing-value filtering to produce a final clean dataset suitable for downstream statistical analysis.

## When to use

After loading and applying minimum non-missing-value thresholds to an omics expression dataset (proteomics, metabolomics, or other panomics data). Use this skill when you need to exclude biomolecules with excessively high relative variability across replicates, which may indicate unreliable or noisy measurements that could confound downstream statistical inference.

## When NOT to use

- Input expression data has not yet been log2-transformed or normalized; CV filtering should follow transformation and normalization steps.
- Dataset contains only a small number of replicates per group (n<3), making CV estimates unstable; consider robust variance metrics or skip CV filtering.
- Biomolecules have already undergone abundance-dependent filtering (e.g., by intensity rank); combining multiple intensity-based filters can bias feature selection.

## Inputs

- Expression data matrix (rows=biomolecules, columns=samples, values=log2-transformed abundance)
- Biomolecule metadata table (identifiers, annotations)
- Sample metadata table (group assignments, covariates)
- Maximum CV threshold (numeric, e.g., 0.3 for 30%)

## Outputs

- Filtered expression matrix (subset of original biomolecules)
- Summary report with counts of biomolecules retained and removed at CV filtering step
- Filtered biomolecule metadata table

## How to apply

For each biomolecule remaining after non-missing-value filtering, compute the coefficient of variation as the ratio of standard deviation to mean abundance across all samples. Compare each biomolecule's CV value against a user-defined or data-driven maximum CV threshold. Retain only biomolecules whose CV is below the cutoff, and generate a summary report documenting the number of biomolecules retained and removed at this filtering step. The threshold choice should be justified by exploratory analysis (e.g., distributional inspection of CV values) and the analytical goal—stricter thresholds (lower CV) yield fewer but more reproducible features.

## Related tools

- **pmartR** (R package implementing CV calculation and CV-based filtering via Shiny GUI; backend for filtering module) — https://github.com/pmartR
- **PMart Shiny App** (Interactive web GUI wrapping pmartR; applies CV thresholds via filtering module without requiring R coding) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Host language for pmartR; used for manual CV computation and filtering if not using GUI)

## Evaluation signals

- Biomolecules retained in the filtered matrix all have CV values ≤ the specified threshold; biomolecules removed all have CV > threshold.
- Summary report shows monotonic decrease in biomolecule count from pre-filter to post-filter; number removed = number exceeding threshold.
- Distribution of CV values in the filtered matrix is visibly left-skewed or concentrated below the threshold compared to pre-filter distribution.
- Downstream statistical tests (e.g., ANOVA, G-test) on filtered data show improved p-value distributions and reduced false-discovery rate relative to unfiltered data.
- Reproducibility check: re-running the filter on the same input with identical threshold re-produces identical output biomolecule set.

## Limitations

- CV threshold is user-defined and context-dependent; no universally optimal cutoff exists. Overly permissive thresholds (high CV) retain noise; overly strict thresholds (low CV) discard potentially valid low-abundance or condition-specific features.
- CV calculation assumes mean abundance is non-zero and well-estimated; biomolecules with very low or near-zero mean values may have artificially inflated CV due to division by small denominators.
- CV filtering is most effective on log-transformed data; applying CV to raw (untransformed) abundance data may bias filtering toward high-abundance biomolecules.
- Sequential application of non-missing-value and CV filters can interact; the set of biomolecules passing CV filtering depends on which biomolecules survived the upstream non-missing-value filter.

## Evidence

- [other] Apply the coefficient-of-variation threshold to filter out biomolecules exceeding the maximum allowable CV.: "Apply the coefficient-of-variation threshold to filter out biomolecules exceeding the maximum allowable CV."
- [intro] Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds.: "Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds."
- [other] Calculate the coefficient of variation (CV) for each remaining biomolecule.: "Calculate the coefficient of variation (CV) for each remaining biomolecule."
- [other] The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a filtered result.: "The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a"
