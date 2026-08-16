---
name: compound-internal-standard-ratio-calculation
description: Use when immediately after loading metabolomics measurements into a SummarizedExperiment
  object, before any batch correction or quality filtering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  - R base
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-internal-standard-ratio-calculation

## Summary

Compute the ratio of compound peak area to internal standard peak area for each sample, a fundamental normalization step in metabolomics that accounts for instrument variability and sample preparation differences. This ratio serves as the basis for downstream quality control, batch correction, and absolute concentration estimation.

## When to use

Apply this skill immediately after loading metabolomics measurements into a SummarizedExperiment object, before any batch correction or quality filtering. Use it when you have paired measurements of compound area and assigned internal standard area in the same sample, and need a normalized metric that is independent of injection volume or extraction efficiency variation.

## When NOT to use

- Samples lack internal standard measurements or internal standard area is zero (will produce NaN or Inf values)
- Internal standard assignment is unknown or ambiguous for a compound
- Input is already a ratio matrix; re-computation would create spurious values

## Inputs

- SummarizedExperiment object with primaryAssay slot (compound area values)
- SummarizedExperiment object with secondaryAssay slot (internal standard area values)
- rowData metadata containing internal standard assignment per compound

## Outputs

- SummarizedExperiment assay slot named 'ratio' containing compound/IS area ratios
- Numeric matrix of dimensions [compounds × samples] with ratio values

## How to apply

Within the mzQuality workflow, the buildExperiment function automatically calculates the compound/internal standard ratio for each sample by dividing the primaryAssay (compound area) by the secondaryAssay (internal standard area). The ratio is stored as a computed assay slot in the SummarizedExperiment object. Ensure that each compound has a designated internal standard recorded in the object's metadata (rowData), and that both area measurements are present and non-zero for all samples. The calculated ratio is then used in subsequent steps: quality control filtering (via Rosner outlier tests on QC sample ratios), batch correction (ratio_corrected assay), background signal estimation, and concentration prediction via linear regression against known calibration standards.

## Related tools

- **mzQuality** (Performs ratio calculation via buildExperiment and doAnalysis; stores ratio in assay slot) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Container object that stores assay matrices (primaryAssay, secondaryAssay, ratio) and rowData/colData metadata)
- **R base** (Arithmetic division operation (primaryAssay / secondaryAssay))

## Examples

```
path <- system.file("extdata", "example.tsv", package = "mzQuality"); exp <- buildExperiment(readData(path)); assay(exp, "ratio")
```

## Evaluation signals

- Verify that the 'ratio' assay is present in the SummarizedExperiment object and has dimensions [number of compounds × number of samples]
- Check that all ratio values are finite positive numbers (no NaN, Inf, or negative values unless intentional masking is applied)
- Confirm that ratio values are used downstream in batch correction (ratio_corrected assay) and QC filtering (Rosner outlier detection on QC ratios)
- Inspect compoundPlot(exp, assay='ratio') to visually verify that QC sample ratios cluster tightly (low intra-group variance) before batch correction
- For samples with known concentrations, verify that ratio values exhibit linear correlation with concentration in concentrationPlot output

## Limitations

- Assumes internal standard area is non-zero for all samples; samples with zero or missing internal standard values will produce invalid ratios (NaN or Inf)
- Ratio calculation alone does not account for matrix effects or batch-related drift; downstream batch correction using ratio_corrected is required
- Internal standard must be chosen appropriately and assigned consistently across all compounds; poor internal standard selection (high RSD in QC samples) will propagate to unreliable ratios
- Assumes that compound and internal standard are measured in the same injection and sample preparation; cross-sample or cross-batch internal standard substitution may violate this assumption

## Evidence

- [other] buildExperiment uses primaryAssay and secondaryAssay as compound and Internal Standard areas respectively, and automatically calculates the compound/Internal Standard ratio for each sample: "buildExperiment deduces rowData and colData slots from compoundColumn and aliquotColumn, uses primaryAssay and secondaryAssay as compound and Internal Standard areas respectively, and automatically"
- [other] The ratio is the foundation for calibration-line concentration estimation via linear regression: "The Concentration Plot is a scatter plot with a linear model added, based on the calculated `ratio` and known `concentration`."
- [readme] Ratio is stored in the SummarizedExperiment assay slot for downstream analysis: "Calculate the ratio between the compounds and assigned internal standards"
- [readme] QC sample ratios are tested for outliers to detect instrument or sample preparation failures: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio"
- [intro] mzQuality recommends internal standards based on RSD of batch-corrected ratios in QC samples: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's"
