---
name: spectral-peak-intensity-normalization
description: Use when after loading raw m/z peak data (in MetaboAnalyst, MetaboShiny native, or Metabolights format) and merging it with sample metadata (batch IDs, concentration values, experimental group labels).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaboShiny
  - R
  - XCMS
  - Docker
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-intensity-normalization

## Summary

Normalize m/z peak intensities across LC-MS/MS samples to account for batch effects, sample concentration differences, and technical variation, enabling valid cross-sample and cross-batch comparison. This is a prerequisite for downstream statistical analysis and compound identification in metabolomics workflows.

## When to use

After loading raw m/z peak data (in MetaboAnalyst, MetaboShiny native, or Metabolights format) and merging it with sample metadata (batch IDs, concentration values, experimental group labels). Apply this skill when samples span multiple analytical batches, when samples have different concentrations or loading amounts, or when peak intensity distributions are skewed or heteroscedastic across samples.

## When NOT to use

- Input is already a pre-normalized or intensity-corrected feature table from upstream processing (e.g., XCMS with quantile normalization already applied).
- Metadata does not contain batch information and all samples are known to be from a single analytical run with uniform sample loading.
- Raw, unnormalized m/z peak data has not yet been merged with metadata (proceed with file import and merging first).

## Inputs

- m/z peak table (MetaboAnalyst, MetaboShiny native, or Metabolights format)
- sample metadata file (with 'sample', 'individual', batch ID column, and optionally concentration column)
- batch identifiers (if applicable)
- sample concentration or loading amount values (if applicable)

## Outputs

- batch-corrected and concentration-normalized feature table
- filtered feature table (low-intensity m/z removed)
- normalized peak intensity matrix (intensity distribution plots for validation)

## How to apply

Execute normalization in two sequential stages: (1) Batch and concentration correction — if metadata contains batch IDs and/or sample concentration values, select these variables to correct for systematic batch-to-batch variation and concentration-dependent intensity scaling. (2) Filtering and normalization — apply a filtering method (e.g., interquartile range, median absolute deviation, or relative standard deviation) to remove low-intensity m/z features below detection limits, then select one normalization type (median, quantile, sum, by reference feature, or by sample-specific factor), optionally apply data transformation (log or cubic root), scaling (autoscale, Pareto, range, or mean-center), and imputation for missing values (KNN, BPCA, SVD, random forest, or median). Inspect pre- and post-normalization peak intensity distributions for a random subset of m/z and samples to verify that the selected parameters reduce skewness and equalize variance across samples without introducing artifacts.

## Related tools

- **MetaboShiny** (Primary interactive platform for batch correction, filtering, normalization, transformation, scaling, and missing value imputation in m/z peak tables) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Programming environment for running MetaboShiny and custom normalization workflows)
- **XCMS** (Upstream peak detection and alignment tool; output can be exported in MetaboAnalyst format for import into MetaboShiny)
- **Docker** (Container platform for deploying MetaboShiny without manual R/Java dependency installation)

## Examples

```
library(MetaboShiny); start_metshi(inBrowser=T); # In GUI: load project → Data normalization tab → 'Get options' → select batch/concentration variables → select Filtering (e.g. Interquartile range), Normalization type (e.g. Median), Transformation (e.g. Log transform), Scaling (e.g. Autoscale), Missing values (e.g. KNN imputation) → click 'Go' → verify pre/post distribution plots → save data
```

## Evaluation signals

- Pre- and post-normalization peak intensity distribution plots show reduced skewness and more uniform variance across samples.
- Batch-corrected intensities no longer exhibit systematic differences between batch groups (visual inspection of batch effect removal).
- Concentration-normalized intensities show no spurious correlation with sample concentration or loading amount.
- Missing value imputation (if applied) produces plausible intensity estimates consistent with the distribution of observed values for that m/z feature.
- Feature retention is appropriate: low-intensity m/z features below the specified detection threshold have been removed, but the majority of high-quality features are retained.

## Limitations

- Normalization efficacy depends on appropriate selection of filtering, transformation, scaling, and imputation methods; the README notes 'The best selection will depend on each user's data' and recommends exploring multiple methods and parameter combinations.
- If metadata does not contain batch IDs or concentration values, batch and concentration correction steps cannot be applied; single-batch, uniform-loading datasets should skip this stage.
- Outlier detection and exclusion is optional; users must decide whether to enable outlier filtering based on their data and analysis goals.
- Metadata must minimally contain a 'sample' column (matching peak table sample identifiers), an 'individual' column, and at least one experimental group or category column; incomplete or misaligned metadata will cause merge failures.

## Evidence

- [readme] The data needs to be normalized in order to compare m/z peak values between samples and batches.: "The data needs to be normalized in order to compare m/z peak values between samples and batches."
- [other] MetaboShiny provides data normalization functionality organized into two components: one for handling batches and concentration, and a separate module for filtering and normalization operations on loaded m/z peak data.: "data normalization functionality organized into two components: one for handling batches and concentration, and a separate module for filtering and normalization operations"
- [readme] After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples, so the user can see how the data distribution has changed with the normalization and adjust their parameters if needed.: "After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples, so the user can see how the data distribution has"
- [readme] Select one of each of the options for the following normalization features: Filtering options (Interquartile range, Mean, Median absolute deviation, Median, Non-parametric relative standard deviation, Relative standard deviation, Standard deviation, None), Normalization type (By reference compound, By reference feature, By sample-specific factor, Median, Quantile normalization, Sum, None), Data transformation (Cubic root transform, Log transform, None), Scaling (Autoscale/Z-transform, Mean-center, Pareto scaling, Range scaling, None), Missing values (Half feature minimum, Half sample minimum, Total minimum, Random forest, KNN imputation, SVD imputation, BPCA imputation, PPCA imputation, Median, Mean, Leave them out, Leave them alone), and Outliers (Exclude outliers toggle).: "Filtering options, Normalization type, Data transformation, Scaling, Missing values, Outliers. The user can choose whether to exclude outliers from the data analysis by toggling the 'Exclude"
- [other] Apply batch correction to account for systematic variations across sample batches. Normalize peak intensities by concentration to account for differences in sample loading.: "Apply batch correction to account for systematic variations across sample batches. Normalize peak intensities by concentration to account for differences in sample loading."
