---
name: feature-table-quality-control
description: Use when when you have a feature intensity matrix (samples × compounds) from untargeted LC–MS/MS or GC–MS analysis and accompanying sample-type metadata (blank, curve, QC, unknown classifications), and you need to remove features with high measurement variability, low QC detection rates, high blank.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3407
  tools:
  - R
  - GetFeatistics
  - XCMS
  - MS-Dial
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration of metabolomics data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-table-quality-control

## Summary

A multi-step QC-based filtering workflow that removes non-reproducible, contaminated, and unreliable features from untargeted metabolomics feature intensity matrices by applying sequential CV%, detection frequency, blank contribution, and dilution series checks. This ensures downstream analyses use only reproducible and reliable features.

## When to use

When you have a feature intensity matrix (samples × compounds) from untargeted LC–MS/MS or GC–MS analysis and accompanying sample-type metadata (blank, curve, QC, unknown classifications), and you need to remove features with high measurement variability, low QC detection rates, high blank contamination, or abnormal intensity behavior across dilution series before statistical or identification analysis.

## When NOT to use

- Input is already a pre-filtered or vendor-processed feature table with QC filtering already applied.
- No QC or blank samples are present in the dataset; the method requires QC replicates and blank samples to set meaningful thresholds.
- Targeted metabolomics with a small curated list of known compounds, where manual curation or alternative QA/QC strategies are preferred over automated filtering.

## Inputs

- df_example_feat_intensities: feature intensity matrix with samples in rows and compounds (features) in columns
- df_example_qc_sampletype: sample metadata table with sample identifiers and type classifications (blank, curve, qc, unknown)

## Outputs

- QC-filtered feature intensity matrix: subset of input features passing all four QC filtering steps
- Feature retention report: counts and identities of features removed at each step

## How to apply

Execute the QCs_process function with four sequential filtering steps on QC samples separately per QC group, then merge confirmed features. Step 1 removes features with coefficient of variation (CV%) above a defined cutoff (e.g., >30%) in QC samples to eliminate high-variance signals. Step 2 excludes features absent in at least a minimum percentage of QC samples (e.g., <80% presence) to filter out sporadic detections. Step 3 removes features whose blank contribution ratio (mean blank intensity / mean QC intensity) exceeds a threshold (e.g., >0.3) to eliminate contamination-prone signals. Step 4 removes features whose mean intensity in QC_half (dilution series or half-intensity QC) samples falls outside a specified percentage range (e.g., 30–300%) relative to full-strength QC mean intensity, to detect abnormal dilution responses. The filtered feature table is then output with only features passing all four criteria.

## Related tools

- **GetFeatistics** (Implements QCs_process function and provides step1–step4 filtering logic, parameter tuning, and visualization of QC-filtered features.) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Runtime environment (≥ v4.3.1) required to execute GetFeatistics and QCs_process.)
- **XCMS** (Upstream feature extraction and alignment tool; QC filtering is typically applied post-XCMS on the resulting feature table.)
- **MS-Dial** (Alternative upstream feature extraction tool; QC filtering is typically applied post-MS-Dial.)

## Examples

```
library(GetFeatistics); filtered_features <- QCs_process(feat_intensities = df_example_feat_intensities, qc_sampletype = df_example_qc_sampletype, step1_cutoff = 30, step2_cutoff = 80, step3_cutoff = 0.3, step4_cutoff = c(30, 300))
```

## Evaluation signals

- Feature count reduction: Verify that the number of features decreases after each step and the final table retains only features meeting all four criteria.
- CV% distribution: Check that step-1-retained features have CV% below the specified step1_cutoff in QC samples.
- QC detection frequency: Confirm that step-2-retained features are present in at least step2_cutoff percentage of QC samples.
- Blank contamination ratio: Validate that step-3-retained features have blank/QC intensity ratios below step3_cutoff.
- Dilution series integrity: Ensure that step-4-retained features have QC_half mean intensities within the step4_cutoff percentage range (e.g., 30–300%) of full QC mean, indicating normal dose–response behavior.

## Limitations

- Step 1 (CV% filtering) may be overly stringent or lenient depending on instrument stability and QC sample homogeneity; requires empirical optimization of step1_cutoff.
- Step 2 (detection frequency) is sensitive to the number and quality of QC replicates; sparse QC sampling may inflate or deflate the presence threshold.
- Step 3 (blank contamination) assumes blank samples are truly representative of background; contaminated or degraded blanks will bias results.
- Step 4 (dilution series check) requires QC_half samples or a dilution series in the dataset; datasets without this experimental design cannot benefit from this filter.
- Separate QC group processing followed by merging may introduce artifacts if QC groups differ substantially in ionization efficiency or matrix effects; groups should be chemically and analytically similar.

## Evidence

- [other] The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff, step2 removes features absent in minimum QC percentage, step3 removes features with blank contribution ratio above cutoff, and step4 removes features with QC_half mean outside specified percentage range.: "The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff, step2 removes features absent in minimum QC percentage, step3 removes features"
- [intro] features with a relative standard deviation (CV%) greater than the value defined in the _step1_cutoff_ will be filtered out...features not present in at least a percentage of QC samples...features with a blank contribution, i.e.: the ratio between mean of blank and mean of QC, greater than the value defined in the _step3_cutoff_ will be filtered out: "if TRUE, features with a relative standard deviation (CV%) greater than the value defined in the _step1_cutoff_ will be filtered out"
- [intro] features not present in at least a percentage of QC samples as defined in _step2_cutoff_ will be filtered out: "if TRUE, features not present in at least a percentage of QC samples as defined in _step2_cutoff_ will be filtered out"
- [intro] features whose mean in "QC_half" samples are not between the percentage range of two values defined in _step4_cutoff_ compared to the mean of QCs will be filtered out: "if TRUE, features whose mean in "QC_half" samples are not between the percentage range of two values defined in _step4_cutoff_ compared to the mean of QCs will be filtered out"
- [intro] The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] the second column should contain the following: "blank", "curve", "qc", or "unknown". the third column should have the actual known values for "curve" and "qc" samples: "the second column should contain the following: "blank", "curve", "qc", or "unknown""
- [intro] This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial: "This package is supposed to be used after obtaining a feature table using open source tools such as XCMS and MS-Dial"
