---
name: qc-sample-filtering-multi-step-criteria
description: Use when after feature extraction from XCMS, MS-Dial, or similar tools
  (producing a feature intensity matrix with samples in rows and compounds in columns),
  and after sample type annotation (blank, curve, qc, unknown).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GetFeatistics
  - XCMS
  - MS-Dial
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
- devtools::install_github("FrigerioGianfranco/GetFeatistics", dependencies = TRUE)
- The **GetFeatistics** (GF) package provides several functions useful for the elaboration
  of metabolomics data
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# QC-Sample Filtering with Multi-Step Criteria

## Summary

A four-step sequential filtering workflow that removes non-reproducible and contaminated features from untargeted metabolomics feature intensity matrices using QC sample statistics: CV%, detection frequency, blank contribution ratio, and dilution series consistency. Applied within GetFeatistics to harmonize feature tables before downstream statistical analysis.

## When to use

After feature extraction from XCMS, MS-Dial, or similar tools (producing a feature intensity matrix with samples in rows and compounds in columns), and after sample type annotation (blank, curve, qc, unknown). Use this skill when QC samples are present and reproducibility and contaminant removal are priorities—particularly in untargeted metabolomics where feature quality varies widely and blanks are available for contamination assessment.

## When NOT to use

- Input is already a curated, manually validated feature table with known reproducibility.
- QC samples are absent or too few (< 3) to reliably estimate CV% or blank contribution.
- Blank samples are not available and contamination assessment cannot be performed.
- Feature intensity data are not in matrix form (samples × compounds) or contain non-numeric values.

## Inputs

- Feature intensity matrix (samples × compounds, numeric)
- Sample type legend with classifications (blank, curve, qc, unknown)
- Step cutoff parameters (step1_cutoff: CV% threshold; step2_cutoff: min QC % presence; step3_cutoff: max blank/QC ratio; step4_cutoff: QC_half % range)

## Outputs

- QC-filtered feature intensity matrix (subset of columns, same sample rows)
- List of retained feature IDs passing all four steps
- Filtering summary (counts and percentages removed per step)

## How to apply

Load the feature intensity matrix (df_example_feat_intensities) and sample legend (df_example_qc_sampletype) into R. Execute QCs_process sequentially: Step 1 removes features with CV% above step1_cutoff in QC samples (default filtering for reproducibility); Step 2 excludes features absent in at least step2_cutoff % of QC samples (minimum detection frequency); Step 3 filters features whose blank contribution ratio (mean blank intensity / mean QC intensity) exceeds step3_cutoff (contamination control); Step 4 removes features whose mean intensity in QC_half (dilution series) samples falls outside the range specified by step4_cutoff % relative to mean QC intensity (dilution linearity check). Process each QC group separately if multiple QC cohorts exist, then merge confirmed features across groups. Output the resulting QC-filtered feature table ready for normalization and statistical analysis.

## Related tools

- **GetFeatistics** (R package implementing QCs_process function with four-step filtering pipeline) — https://github.com/FrigerioGianfranco/GetFeatistics
- **XCMS** (Open source feature extraction tool whose output (feature table) serves as input to this filtering skill)
- **MS-Dial** (Open source feature extraction tool whose output (feature table) serves as input to this filtering skill)
- **R** (Runtime environment (≥ 4.3.1) for executing GetFeatistics functions)

## Examples

```
library(GetFeatistics); result <- QCs_process(df_example_feat_intensities, df_example_qc_sampletype, step1_cutoff=30, step2_cutoff=80, step3_cutoff=0.3, step4_cutoff=c(20,180), separate_QC=TRUE)
```

## Evaluation signals

- Step 1: Verify that all retained features have CV% ≤ step1_cutoff when computed across QC samples.
- Step 2: Confirm that retained features are present (non-NA) in ≥ step2_cutoff % of QC samples.
- Step 3: Check that mean(blank) / mean(QC) ≤ step3_cutoff for all retained features.
- Step 4: Validate that mean(QC_half) falls within [step4_cutoff[1]% × mean(QC), step4_cutoff[2]% × mean(QC)] for retained features.
- Overall: Feature count reduction should be monotonic and traceable per step; merged output should have no duplicate feature IDs and same row dimension as input.

## Limitations

- Filtering is sensitive to cutoff parameter choice; no automated optimization is provided—practitioners must validate cutoffs against domain knowledge.
- Requires sufficient QC replication (≥ 3 recommended) to reliably estimate CV% and statistics; sparse QC designs may be unreliable.
- Step 4 (QC_half dilution check) assumes a dilution series is present in the QC group; if absent or non-linear, step 4 may filter valid features.
- Separate QC group processing can fragment feature retention if QC cohorts have differing reproducibility profiles; merging may lose features present in only one QC group.
- Missing values (NA) in feature intensity matrix are not explicitly handled by the filtering steps; imputation or removal strategy should be applied before QCs_process.

## Evidence

- [intro] step1_cutoff filtering to remove features with CV% above threshold in QC samples: "features with a relative standard deviation (CV%) greater than the value defined in the _step1_cutoff_ will be filtered out"
- [intro] step2_cutoff to exclude features not present in minimum percentage of QC samples: "features not present in at least a percentage of QC samples as defined in _step2_cutoff_ will be filtered out"
- [intro] step3_cutoff to remove features with blank contribution ratio above cutoff: "features with a blank contribution, i.e.: the ratio between mean of blank and mean of QC, greater than the value defined in the _step3_cutoff_ will be filtered out"
- [intro] step4_cutoff to remove features with QC_half mean outside specified percentage range: "features whose mean in "QC_half" samples are not between the percentage range of two values defined in _step4_cutoff_ compared to the mean of QCs will be filtered out"
- [other] Four sequential steps remove non-reproducible and contaminated features: "The QCs_process function filters features through four sequential steps: step1 removes features with CV% above cutoff, step2 removes features absent in minimum QC percentage, step3 removes features"
- [intro] Input data structure and sample legend format: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
- [intro] Sample type classification legend requirements: "the second column should contain the following: "blank", "curve", "qc", or "unknown""
- [readme] GetFeatistics as integrated feature elaboration and QC processing framework: "Getting streamlined elaboration of targeted and non-targeted metabolomics data, including elaboration of feature tables, separate QC processing, advanced statistics such as multiple regression linear"
