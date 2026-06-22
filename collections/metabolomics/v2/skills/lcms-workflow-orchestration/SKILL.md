---
name: lcms-workflow-orchestration
description: Use when starting from raw LC-MS spectral files (mzML or mzXML format) in a global metabolomics study and you need to produce a complete, validated feature table with m/z, retention time, and intensity values across all samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
---

# lcms-workflow-orchestration

## Summary

Orchestrate a unified LC-MS data processing pipeline that combines peak detection, retention-time and m/z-based alignment, feature table consolidation, and quality assessment to transform raw LC-MS spectra (mzML/mzXML) into validated quantitative metabolite feature matrices. This skill implements the auto-optimized feature detection and quantification workflow that MetaboAnalystR 4.0 provides for global metabolomics.

## When to use

Apply this skill when starting from raw LC-MS spectral files (mzML or mzXML format) in a global metabolomics study and you need to produce a complete, validated feature table with m/z, retention time, and intensity values across all samples. Trigger conditions include: (1) receipt of untransformed mass spectrometry data from an instrument; (2) requirement for standardized, reproducible peak detection and alignment across a cohort; (3) need to leverage community best practices for LC-MS1 spectra processing with automated parameter optimization.

## When NOT to use

- Input data is already in feature-table format (CSV/TSV with pre-aligned m/z and RT)—skip to downstream analysis.
- Study requires targeted analysis of known compounds with predefined inclusion lists, not global untargeted metabolomics.
- Data are from data-dependent (DDA) or data-independent (DIA) MS/MS spectra requiring compound deconvolution and annotation—use the separate MS/MS spectra module instead.

## Inputs

- raw LC-MS spectral files (mzML format)
- raw LC-MS spectral files (mzXML format)
- sample metadata (sample IDs, class labels, batch information)

## Outputs

- consolidated quantitative feature table (m/z, retention time, intensity per feature per sample)
- feature quality metrics and validation report
- aligned peak list with retention time corrections
- peak detection and alignment parameter log

## How to apply

Load raw LC-MS spectral data (mzML or mzXML format) into the MetaboAnalystR environment after installing package dependencies and initializing the xia-lab/MetaboAnalystR repository. Execute peak detection on raw spectra using MetaboAnalystR's auto-optimized feature detection module, which automatically optimizes parameters to improve quantification accuracy and detection coverage. Perform retention-time and m/z-based alignment of detected peaks across all samples using the alignment function—the README reports this accelerates the workflow while maintaining accuracy. Consolidate aligned peaks into a quantitative feature table with m/z, retention time, and intensity columns for each detected feature across all samples. Finally, validate the feature table using MetaboAnalystR's quality assessment module, which checks completeness, missing value patterns, and applies quality metrics; the README benchmark shows MetaboAnalystR 4.0 can accurately detect and identify >10% more high-quality MS features than prior approaches.

## Related tools

- **MetaboAnalystR** (primary platform for unified LC-MS workflow orchestration, peak detection, retention-time and m/z-based alignment, feature table consolidation, and quality assessment) — https://github.com/xia-lab/MetaboAnalystR

## Examples

```
devtools::install_github("xia-lab/MetaboAnalystR", build = TRUE, build_vignettes = FALSE); library(MetaboAnalystR); # Load and process LC-MS data (mzML format) as per vignette workflow
```

## Evaluation signals

- Feature table is non-empty with valid m/z values (typically 50–1200 Da for small-molecule metabolomics), retention times, and intensity counts; no NaN or Inf entries in quantitative columns.
- Alignment quality: peak cluster size distribution shows majority of features detected in ≥50% of samples (missing value rate <50% per feature) after alignment, indicating successful cross-sample matching.
- Quality metrics from MetaboAnalystR validation module report: coefficient of variation (CV) for technical replicates <30%; blank intensity levels significantly lower than sample intensity (blank/sample ratio <0.1 or user-defined threshold).
- Peak detection sensitivity: benchmarked against known metabolite standards, >10% improvement in high-quality MS feature detection relative to prior-version baselines.
- Alignment accuracy: m/z error <5 ppm and retention-time tolerance met for replicate samples; visual inspection of extracted ion chromatograms (XICs) for key features shows consistent peak positions across samples.

## Limitations

- Auto-optimization of peak detection parameters may fail or require manual tuning for unusual matrix compositions, very high ion suppression, or non-standard sample preparations not represented in training data.
- Missing values in the consolidated feature table are not imputed by default during this workflow stage; separate imputation module must be applied downstream if needed.
- Workflow assumes mzML or mzXML input; other vendor-specific raw formats (e.g., .raw, .d) must be converted first, which may introduce processing artifacts.
- Quality assessment checks completeness and missing-value patterns but does not evaluate biological relevance or statistical significance; false-positive features (noise, contaminants, isotopologues) are not automatically flagged and require downstream statistical filtering.
- Performance and memory requirements scale with sample number and spectral complexity; very large cohorts (>1000 samples) or high-resolution data may require parameter adjustment or computational resources.

## Evidence

- [other] MetaboAnalystR 4.0 implements a unified LC-MS workflow for global metabolomics, as indicated by the software title and README.: "MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics"
- [other] The workflow steps as reconstructed from the task card.: "Clone and initialize the xia-lab/MetaboAnalystR repository and load raw LC-MS spectral data (mzML or mzXML format) into the MetaboAnalystR environment. Execute peak detection on raw spectra using the"
- [readme] Core feature of MetaboAnalystR 4.0: auto-optimized feature detection and quantification module.: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] Benchmark performance demonstrating the improved quantification and identification accuracy.: "MetaboAnalystR 4.0 can significantly improve the quantification accuracy and identification coverage of the metabolome. Serial dilutions demonstrate that MetaboAnalystR 4.0 can accurately detect and"
- [readme] Rationale for using this workflow in global metabolomics.: "By leveraging the best practices established by the community, MetaboAnalyst R 4.0 offers three key features"
- [readme] Raw data processing workflow and acceleration statement.: "The raw data processing workflow has been accelerated and gradually mature."
