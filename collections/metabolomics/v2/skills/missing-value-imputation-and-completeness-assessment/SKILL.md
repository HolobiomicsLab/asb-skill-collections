---
name: missing-value-imputation-and-completeness-assessment
description: Use when after loading raw omics expression data (protein, peptide, metabolite
  abundances) with inherent missing values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - PMart Shiny GUI
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

# missing-value-imputation-and-completeness-assessment

## Summary

Assess and filter omics biomolecules based on missing-value patterns and coefficient of variation, then optionally impute missing values to retain molecules meeting completeness thresholds. This skill is essential for deciding which biomolecules to retain before downstream statistical analysis, balancing data completeness against noise.

## When to use

After loading raw omics expression data (protein, peptide, metabolite abundances) with inherent missing values. Apply this skill when you need to (1) identify biomolecules with insufficient data density to support reliable statistical inference, (2) filter out high-variance or sparse molecules that may introduce noise, or (3) impute missing values in retained molecules to enable downstream analyses that require complete data matrices (e.g., ANOVA, correlation heatmaps, normalization).

## When NOT to use

- Input is already a filtered feature table with no missing values; re-filtering may remove valid signal.
- The analysis goal does not require complete data matrices (e.g., if using missing-value-aware statistical tests that explicitly model missingness).
- Missingness is known to be non-random (e.g., left-censored by instrument detection limits); imputation without accounting for the censoring mechanism may introduce bias.

## Inputs

- Expression data matrix (samples × biomolecules, with missing values represented as NA or NaN)
- Sample metadata (sample identifiers, grouping variables)
- Biomolecule metadata (identifiers, annotations)
- Minimum non-missing-value threshold (integer or percentage)
- Maximum coefficient-of-variation threshold (numeric, e.g., 0.5 for 50%)

## Outputs

- Filtered expression matrix (reduced set of biomolecules meeting completeness and CV thresholds)
- Imputed expression matrix (same biomolecules, with missing values replaced)
- Filtering summary report (number of biomolecules removed at each step, reasons for removal)
- Missing-value pattern visualizations (e.g., missing-variable plots)

## How to apply

First, calculate the number of non-missing values (completeness count) per biomolecule across all samples. Apply a minimum non-missing-value threshold to retain only biomolecules meeting the cutoff; this is a hard filter that removes sparse molecules before imputation. Next, calculate the coefficient of variation (CV) for each remaining biomolecule and apply a maximum CV threshold to exclude high-variance molecules that may reflect biological or technical noise. For biomolecules passing both thresholds, impute missing values using an appropriate method (e.g., k-nearest neighbors, mean/median substitution, or probabilistic approaches supported by pmartR). Export the filtered expression matrix, the imputed values matrix, and a summary report showing the number of biomolecules retained and removed at each filtering step. The rationale is that these dual thresholds—completeness and variability—ensure that retained data is sufficiently dense and sufficiently low-noise to support robust downstream analysis.

## Related tools

- **pmartR** (Backend R package providing functions to calculate non-missing-value counts, coefficient of variation, apply filtering thresholds, and perform imputation on omics data objects) — https://github.com/pmartR/pmartR
- **PMart Shiny GUI** (Interactive web interface wrapping pmartR filtering and imputation functions, allowing users to set non-missing-value and CV thresholds, visualize missing-value patterns, and export filtered/imputed matrices without R coding) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Execution environment for pmartR and statistical computation)

## Evaluation signals

- Filtered biomolecule count matches the number of molecules with ≥ (threshold) non-missing values across all samples before CV filtering is applied.
- CV values for all retained biomolecules are ≤ the specified maximum CV threshold; check summary statistics on the filtered matrix.
- Imputed expression matrix has no remaining NA/NaN values in the retained biomolecule rows, and imputed values fall within the observed range for that biomolecule (or within a plausible range defined by the imputation method).
- Missing-variable plot or summary shows a clear reduction in biomolecule count from raw to filtered, with documented loss at each threshold step.
- Downstream analyses (PCA, ANOVA, heatmaps) run without error on the filtered/imputed matrix, indicating data completeness requirements are satisfied.

## Limitations

- Non-missing-value thresholds are user-defined and data-dependent; no universal default exists. Choice affects bias-variance tradeoff: stricter thresholds retain fewer biomolecules but higher-confidence data.
- CV threshold may bias toward low-abundance, invariant molecules and may remove legitimate high-variance biomarkers; domain knowledge is required to set appropriate cutoffs.
- Imputation methods (mean, KNN, probabilistic) introduce artificial correlations or reduce variance; imputed values are not observed and may inflate false-positive associations in downstream tests.
- The pmartR-Shiny GUI does not document all imputation algorithms or their default parameters in the provided README; users should consult pmartR documentation for method selection.
- Missing-value patterns are assumed to be independent of biomolecule identity for filtering purposes; if missingness correlates with sample group or biomolecule class, filtering may introduce batch effects or bias.

## Evidence

- [other] The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a filtered result.: "The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds"
- [intro] Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds.: "Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds"
- [other] Calculate the number of non-missing values per biomolecule across all samples. 3. Apply the minimum non-missing value threshold to retain only biomolecules meeting the cutoff. 4. Calculate the coefficient of variation (CV) for each remaining biomolecule. 5. Apply the coefficient-of-variation threshold to filter out biomolecules exceeding the maximum allowable CV.: "Calculate the number of non-missing values per biomolecule across all samples. Apply the minimum non-missing value threshold to retain only biomolecules meeting the cutoff. Calculate the coefficient"
- [intro] Exploratory data analysis. PCA, missing-variable plots, correlation heatmaps, and more.: "Exploratory data analysis. PCA, missing-variable plots, correlation heatmaps, and more."
- [readme] The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself.: "The bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself"
