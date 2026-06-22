---
name: biomolecule-filtering-by-abundance-threshold
description: Use when after data transformation (e.g., log2 normalization) but before statistical analysis, when you have an expression matrix with missing values or high variance across samples and you need to remove unreliable biomolecules.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - pmartR
  - R
  - PMart ShinyApp
  - Shiny
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
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

# biomolecule-filtering-by-abundance-threshold

## Summary

Filter biomolecules from omics expression matrices using minimum non-missing value thresholds and coefficient of variation (CV) cutoffs to retain only reliably quantified features. This two-stage filtering removes low-abundance or highly variable biomolecules before downstream statistical analysis.

## When to use

Apply this skill after data transformation (e.g., log2 normalization) but before statistical analysis, when you have an expression matrix with missing values or high variance across samples and you need to remove unreliable biomolecules. Use this skill when your analysis goal requires high-confidence abundance measurements—e.g., when identifying biomarkers or when downstream statistical power is sensitive to noise-driven biomolecules. Concrete trigger: if your expression matrix has >20% missing values per biomolecule, or if visual inspection of CV distributions shows a long tail of high-variance features, filtering is warranted.

## When NOT to use

- Input is already a pre-filtered feature table or a consensus set of validated analytes—re-filtering risks loss of known biomarkers.
- Analysis goal is to detect rare or low-abundance biomolecules (e.g., biomarkers with sparse quantification); aggressive non-missing thresholds will eliminate them.
- Biomolecules have biological reasons for high CV (e.g., biomarkers with treatment-dependent variability); filtering by CV alone may remove signal.

## Inputs

- expression data matrix (biomolecules × samples, with missing values encoded as NA or 0)
- sample metadata (phenotypes, treatment groups, covariates)
- biomolecule metadata (identifiers, annotations)

## Outputs

- filtered expression matrix (reduced set of reliable biomolecules)
- filtering summary report (number retained and removed per threshold step)
- quality control metrics (non-missing value counts, CV values per biomolecule)

## How to apply

Load the expression data matrix (rows=biomolecules, columns=samples), sample metadata, and biomolecule metadata into pmartR. Calculate the count of non-missing (observed) values for each biomolecule across all samples, then apply a user-defined minimum non-missing threshold (e.g., retain biomolecules present in ≥80% of samples). For biomolecules passing the first threshold, compute the coefficient of variation (CV = standard deviation / mean) and apply a maximum CV cutoff (typical range: 20–50% depending on instrument and analyte class). Retain only biomolecules satisfying both criteria. Export the filtered expression matrix and a summary report documenting the number of biomolecules removed at each stage. The rationale: non-missing value thresholds remove unreliably quantified features due to instrumental or biological dropout; CV thresholds remove intrinsically noisy biomolecules whose high variability may obscure true biological signal.

## Related tools

- **pmartR** (core backend R package providing filtering functions (non-missing value and CV calculation and thresholding)) — https://github.com/pmartR
- **PMart ShinyApp** (web-based GUI wrapping pmartR filtering module; allows interactive threshold selection and real-time filtering preview) — https://github.com/pmartR/PMart_ShinyApp
- **Shiny** (R web framework enabling interactive threshold tuning and visualization of filtering results)
- **R** (statistical computing environment for programmatic filtering workflow and threshold calculation)

## Evaluation signals

- Non-missing value counts per biomolecule after filtering match the specified threshold (e.g., if threshold=80%, all retained biomolecules have ≥80% non-missing samples).
- Coefficient of variation for all retained biomolecules is ≤ the specified CV threshold; no retained biomolecule exceeds the cutoff.
- Filtering summary report shows decreasing biomolecule counts at each threshold stage with no anomalous spikes (e.g., stage 1 removes N biomolecules, stage 2 removes M, cumulative total matches original count minus retained count).
- Filtered expression matrix has no NaN or Inf values introduced; dimensions and rownames/colnames are preserved or explicitly mapped.
- CV and non-missing value distributions before and after filtering show expected left-shift (removal of low-abundance and high-variance features).

## Limitations

- CV thresholds assume normally or log-normally distributed abundance; highly skewed or multimodal distributions may yield uninformative CV values.
- Non-missing value thresholds are arbitrary and dataset-specific; no universal standard. Setting too high eliminates rare valid biomolecules; too low retains noise.
- Filtering based solely on global CV ignores biomolecule-by-treatment interactions; high CV may reflect true biological signal rather than measurement noise.
- The pmartR/Shiny implementation provides no built-in validation against hold-out or independent cohorts; filtered thresholds may not generalize.
- Repository README and article lack reproducibility details (validation protocols, benchmark datasets, performance metrics on independent cohorts).

## Evidence

- [other] The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a filtered result.: "The filtering module removes biomolecules using two primary criteria: minimum non-missing values thresholds and coefficient of variation thresholds, applied to the expression dataset to produce a"
- [other] Calculate the number of non-missing values per biomolecule across all samples. 3. Apply the minimum non-missing value threshold to retain only biomolecules meeting the cutoff. 4. Calculate the coefficient of variation (CV) for each remaining biomolecule. 5. Apply the coefficient-of-variation threshold to filter out biomolecules exceeding the maximum allowable CV.: "Calculate the number of non-missing values per biomolecule across all samples. 3. Apply the minimum non-missing value threshold to retain only biomolecules meeting the cutoff. 4. Calculate the"
- [intro] Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds.: "Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds."
- [readme] Filtering. Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds. Filter samples based on statistical metrics and other exploratory analyses.: "Filtering. Filter biomolecules based on various criteria including minimum non-missing values and coefficient of variation thresholds. Filter samples based on statistical metrics and other"
- [readme] The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself.: "The aim is for the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself."
