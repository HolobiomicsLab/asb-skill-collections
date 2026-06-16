---
name: lcms-feature-detection-and-quantification
description: Use when you have raw LC-MS data (mzML or equivalent format) from a metabolomics experiment and need to extract a reproducible, quantified feature table with intensity measurements before conducting metabolite identification or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - MetaboAnalystR
derived_from:
- doi: 10.1038/s41467-024-48009-6
  title: metaboanalystr
evidence_spans:
- 'MetaboAnalystR 4.0: a unified LC-MS workflow for global metabolomics'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboanalystr
    doi: 10.1038/s41467-024-48009-6
    title: metaboanalystr
  dedup_kept_from: coll_metaboanalystr
schema_version: 0.2.0
---

# LC-MS feature detection and quantification

## Summary

Auto-optimized detection and quantification of metabolite features from LC-MS1 spectra, producing a feature table with dimensions (features × samples) and peak intensity statistics. This skill bridges raw mzML/NetCDF data to downstream metabolite annotation and functional analysis.

## When to use

You have raw LC-MS data (mzML or equivalent format) from a metabolomics experiment and need to extract a reproducible, quantified feature table with intensity measurements before conducting metabolite identification or statistical analysis. Use this when you require automated peak picking with parameter optimization rather than manual threshold tuning.

## When NOT to use

- Input is already a processed feature table or quantification matrix
- Data is from targeted MS assays with predefined compound lists (use targeted quantification instead)
- Raw spectra lack sufficient chromatographic resolution or signal-to-noise for reliable peak detection

## Inputs

- Raw LC-MS spectral data in mzML or NetCDF format
- Sample metadata (optional, for batch annotation)

## Outputs

- Feature table (features × samples matrix)
- Peak intensity values and summary statistics (mean, median, std dev, min, max)
- Feature metadata including m/z and retention time

## How to apply

Load raw LC-MS data (mzML/NetCDF format) into MetaboAnalystR 4.0 and execute the unified LC-MS workflow, which applies auto-optimized feature detection via ultra-fast parameter optimization for peak picking. The workflow generates a feature table by assigning detected peaks to features and computing peak intensity values across all samples. Extract table dimensions (number of features as rows, number of samples as columns) and compute summary statistics on intensity distributions (mean, median, standard deviation, min, max). The auto-optimization approach improves quantification accuracy and detection of high-quality MS features compared to fixed-parameter methods.

## Related tools

- **MetaboAnalystR** (Executes auto-optimized LC-MS1 feature detection, quantification, and unified workflow for peak picking and intensity matrix generation) — https://github.com/xia-lab/MetaboAnalystR

## Evaluation signals

- Feature table has non-zero dimensions (number of features > 0, number of samples ≥ 2)
- Intensity values are numeric, positive, and within instrument detection range
- Summary statistics (mean, median, std dev) are internally consistent and match raw peak intensities
- Retention time and m/z values are within expected ranges for LC-MS analysis
- Results match or exceed reference benchmark: >10% more high-quality features detected compared to legacy methods

## Limitations

- Auto-optimization performance depends on data quality; low signal-to-noise or poor chromatographic resolution reduce feature detection sensitivity
- Parameter optimization assumes adequate chemical diversity in the sample; highly specialized or limited metabolite sets may not optimize effectively
- Feature table does not include compound identities; annotation requires downstream MS/MS deconvolution and spectral matching
- Batch effects or signal drift across runs are not corrected in the feature detection step; separate batch correction workflows are recommended

## Evidence

- [readme] an auto-optimized feature detection and quantification module for LC-MS1 spectra processing: "an auto-optimized feature detection and quantification module for LC-MS1 spectra processing"
- [readme] ultra-fast parameter optimization for peak picking, automated batch effect correction: "ultra-fast parameter optimization for peak picking, automated batch effect correction, and improved pathway activity prediction"
- [readme] MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features: "MetaboAnalystR 4.0 can accurately detect and identify > 10% more high-quality MS and MS/MS features"
- [other] Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max): "Extract feature table dimensions (number of rows as features, number of columns as samples) and compute summary statistics on peak intensity values (mean, median, standard deviation, min, max)"
