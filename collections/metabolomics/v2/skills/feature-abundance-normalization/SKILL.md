---
name: feature-abundance-normalization
description: Use when after peak picking (e.g., via MS-DIAL) and quality control filtering, when you have a raw feature abundance matrix with intensity values across multiple samples and need to make intensities comparable before statistical testing or multivariate analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - margheRita
  - notame
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-abundance-normalization

## Summary

Normalize LC-MS/MS metabolomic feature abundance matrices to remove systematic variation and improve comparability across samples while preserving biological signal. This is a critical preprocessing step that corrects for instrument drift, batch effects, and sample loading differences in untargeted metabolomics workflows.

## When to use

Apply this skill after peak picking (e.g., via MS-DIAL) and quality control filtering, when you have a raw feature abundance matrix with intensity values across multiple samples and need to make intensities comparable before statistical testing or multivariate analysis. Particularly essential when samples were processed across multiple batches or instruments, or when systematic drift in molecular feature intensity is suspected across a run sequence.

## When NOT to use

- Input is already a downstream statistical or annotation table (e.g., p-values, metabolite identifications, pathway scores) — normalization applies only to raw or log-transformed intensity matrices.
- Samples have been acquired using fundamentally different instrumental methods or ionization polarities in a single matrix — normalize each polarity/method separately.
- The study design is single-batch, single-run with negligible instrument drift and no confounding batch effects — normalization may introduce unnecessary noise if systematic variation is minimal.

## Inputs

- Raw peak intensity matrix (text/TSV format) from MS-DIAL with features as rows and samples as columns
- Sample metadata with batch assignment and QC/non-QC sample classification
- QC sample replicate measurements (if drift correction is to be applied)

## Outputs

- Normalized feature abundance matrix with same dimensions as input but with scaled/corrected intensities
- Normalization parameters and drift correction spline coefficients (for reproducibility)
- Summary statistics (e.g., pre- vs. post-normalization intensity distributions, batch effect reduction metrics)

## How to apply

Load the raw feature abundance matrix (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt format) and sample metadata into R via margheRita. The package implements probabilistic quotient normalization (PQN) as a recommended approach for metabolomic profiles; this method normalizes each sample by dividing by the median of the quotient distribution (feature intensity / median intensity across all samples for that feature). For samples containing QC replicates, consider drift correction using cubic spline fitting across the run sequence before normalization. Apply the selected normalization strategy uniformly to all features and samples in the matrix. Output the normalized feature table and verify that the distribution of intensities across samples is now approximately symmetric and comparable, with systematic biases (e.g., time-dependent drift, batch-level shifts) substantially attenuated.

## Related tools

- **margheRita** (Implements probabilistic quotient normalization and drift correction functions for metabolomic feature matrices; provides complete preprocessing workflow including normalization, filtering, and quality control) — https://github.com/emosca-cnr/margheRita
- **notame** (Provides alternative normalization and batch effect correction strategies; supports drift correction via cubic spline and multiple imputation methods for preprocessed LC-MS data) — https://github.com/hanhineva-lab/notame
- **R** (Programming environment for implementing normalization functions and matrix operations)

## Evaluation signals

- Post-normalization feature intensity distributions are approximately centered (median near zero on log scale) and symmetric across samples, with outlier samples no longer showing systematic skew.
- Batch-level intensity offsets are substantially reduced: mean intensity per batch should be approximately equal after normalization (verified via boxplot or ANOVA F-statistic comparison).
- QC sample replicates cluster tightly in post-normalization PCA or hierarchical clustering, indicating reduced technical variation and improved reproducibility.
- Coefficient of variation within QC replicates decreases compared to raw data, indicating improved measurement precision after drift and batch correction.
- Biological signal (e.g., group separation in PCA, effect sizes in differential abundance tests) is preserved or enhanced relative to raw data, demonstrating that normalization does not obscure genuine biological differences.

## Limitations

- Probabilistic quotient normalization assumes that most features do not change between samples; if a large proportion of features are genuinely differentially abundant (>50%), normalization may compress real biological signal.
- Drift correction via cubic spline requires a sufficient number of QC replicates distributed evenly across the run sequence; sparse or unevenly distributed QCs may yield unreliable spline fits.
- Different ionization polarities (RP-NEG, RP-POS, HILIC, etc.) and chromatographic column types must be normalized separately; applying normalization across incompatible acquisition modes will conflate instrumental and biological variation.
- Missing values (imputed or not) can distort the quotient distribution in probabilistic quotient normalization; high missingness (>30% per feature) should be addressed by feature filtering before normalization.

## Evidence

- [readme] margheRita implements probabilistic quotient normalization and drift correction: "filtering by mass defects, filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization"
- [readme] PQN is a recommended method for metabolomic profiles: "a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles"
- [readme] Drift correction via cubic spline is available in notame: "Drift correction: correcting for systematic drift in the intensity of molecular features using cubic spline correction"
- [readme] Full preprocessing workflow includes normalization after peak picking: "After peak picking with the dedicated software, we use R for data preprocessing, quality control, statistical analysis and visualization"
- [readme] margheRita addresses complete workflow for metabolomic profiling: "The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)"
