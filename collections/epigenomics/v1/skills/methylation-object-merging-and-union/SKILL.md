---
name: methylation-object-merging-and-union
description: Use when you have loaded individual methylation call files as methylRawList objects from bisulfite sequencing experiments (via methRead()) and need to perform base-level comparative analysis across two or more samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3367
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - R
  - methylKit
  - Bismark
  - MethylDackel
derived_from:
- doi: 10.1186/gb-2012-13-10-r87
  title: methylkit
evidence_spans:
- packageVersion('methylKit')
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_methylkit
    doi: 10.1186/gb-2012-13-10-r87
    title: methylkit
  dedup_kept_from: coll_methylkit
schema_version: 0.2.0
---

# methylation-object-merging-and-union

## Summary

Merge methylation call objects across multiple bisulfite sequencing samples to create a unified methylBase object containing only bases with coverage in all samples. This is a prerequisite for comparative differential methylation analysis, ensuring consistent base-pair resolution across the sample cohort.

## When to use

You have loaded individual methylation call files as methylRawList objects from bisulfite sequencing experiments (via methRead()) and need to perform base-level comparative analysis across two or more samples. The goal is to identify a common set of covered loci before calculating differential methylation statistics.

## When NOT to use

- Input is already a methylBase object; merging is not needed.
- You wish to perform single-sample methylation statistics or visualization without cross-sample comparison.
- Coverage is highly uneven across samples and you prefer to use coverage-weighted or missing-data-imputation strategies instead of complete-case deletion.

## Inputs

- methylRawList object (collection of methylRaw objects, one per sample, from methRead())
- Methylation call files in text format with per-base cytosine calls

## Outputs

- methylBase object (merged methylation matrix with bases covered in all samples)

## How to apply

Apply the unite() function to a methylRawList object to merge all samples and retain only those base-pair locations covered in every sample in the cohort. The resulting methylBase object contains a consistent set of bases suitable for downstream statistical testing via calculateDiffMeth(). This union operation is essential because differential methylation analysis requires paired observations across all samples; bases missing in even one sample are excluded. The merger also standardizes the coverage landscape, reducing heterogeneity that would inflate false positives in Fisher's exact test or logistic regression.

## Related tools

- **methylKit** (R package providing methRead() and unite() functions for loading and merging methylation call objects) — https://github.com/al2na/methylKit
- **Bismark** (Bisulfite alignment and methylation calling tool producing input call files for methRead()) — https://github.com/FelixKrueger/Bismark
- **MethylDackel** (Alternative tool for extracting per-base methylation metrics from BAM/CRAM files, producing input-compatible call files) — https://github.com/dpryan79/MethylDackel

## Examples

```
myMethBaseObj <- unite(myMethRawList, destrand=FALSE)
```

## Evaluation signals

- Output methylBase object contains only bases with non-zero coverage across all samples in the input methylRawList.
- Total row count of methylBase is ≤ the row count of any individual methylRaw input (due to union operation).
- Column count equals the number of samples in the input methylRawList (one coverage and one methylation percentage column per sample).
- No missing values (NA) appear in the coverage or methylation percentage columns of the output methylBase.
- Subsequent calculateDiffMeth() produces a methylDiff object with valid q-values and percent methylation differences for all rows.

## Limitations

- The union operation (bases covered in ALL samples) can substantially reduce statistical power if samples have highly divergent coverage profiles or sequencing depths, as rare or low-coverage regions are discarded.
- Bases with coverage below the default threshold (10 reads per base, set during methRead()) are already filtered prior to merging; subsequent filtering cannot recover these loci.
- No imputation or interpolation is performed; missing coverage in any sample results in complete exclusion of that base from the merged object.
- Large cohorts with heterogeneous library sizes may lose >50% of individual base calls due to the complete-case requirement.

## Evidence

- [intro] In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all: "In order to do further analysis, we will need to get the bases covered in all samples. The following function will merge all samples to one object for base-pair locations that are covered in all"
- [intro] We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object: "We start by reading in the methylation call data from bisulfite sequencing with methRead function. Reading in the data this way will return a methylRawList object"
- [other] Merge samples across all bases with unite() function to create a methylBase object containing only bases covered in all samples.: "Merge samples across all bases with unite() function to create a methylBase object containing only bases covered in all samples"
