---
name: methylation-hyper-hypo-classification
description: Use when after calculating differential methylation across samples using calculateDiffMeth(), when you need to separately enumerate and extract hyper-methylated (increased methylation) versus hypo-methylated (decreased methylation) bases that meet both statistical significance (q-value < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - R
  - methylKit
  - Bismark
  - genomation
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

# methylation-hyper-hypo-classification

## Summary

Classify differentially methylated bases into hyper-methylated and hypo-methylated subsets using getMethylDiff() with statistical and effect-size cutoffs. This skill extracts and counts methylation changes between sample groups to identify loci where methylation is significantly elevated or reduced.

## When to use

After calculating differential methylation across samples using calculateDiffMeth(), when you need to separately enumerate and extract hyper-methylated (increased methylation) versus hypo-methylated (decreased methylation) bases that meet both statistical significance (q-value < 0.01) and biological relevance (≥25% methylation difference) thresholds.

## When NOT to use

- Methylation data has not yet been merged across all samples using unite() or does not contain coverage in all replicates.
- You are working with non-CpG cytosine methylation (e.g., CHG or CHH contexts in plants) without verifying that your q-value and effect-size thresholds remain appropriate.
- Input methylation percentages are binary (fully methylated or unmethylated) rather than continuous; the q-value calculation and effect-size filtering assume heterogeneous methylation percentages.

## Inputs

- methylDiff object (output from calculateDiffMeth())

## Outputs

- methylDiff object filtered for hyper-methylated bases (type='hyper')
- methylDiff object filtered for hypo-methylated bases (type='hypo')
- Integer counts of hyper-methylated and hypo-methylated bases

## How to apply

Apply getMethylDiff() to a methylDiff object produced by calculateDiffMeth(), specifying q-value = 0.01 and percent methylation difference = 25% as joint filtering thresholds. The function automatically selects the appropriate statistical test (Fisher's exact test for small sample sizes, logistic regression for larger cohorts) based on sample count. Extract hyper-methylated bases by setting type='hyper' and hypo-methylated bases with type='hypo', producing separate methylDiff objects. Validate results by confirming that returned base counts align with expected methylation directionality from your experimental design (e.g., treatment vs. control groups).

## Related tools

- **methylKit** (Provides calculateDiffMeth() to perform statistical test selection and p-value calculation, and getMethylDiff() to filter and subset methylation changes by significance and effect size.) — https://github.com/al2na/methylKit
- **Bismark** (Generates initial methylation call files (input to methRead()) that are later processed through calculateDiffMeth() and getMethylDiff() for hyper/hypo classification.) — https://github.com/FelixKrueger/Bismark
- **genomation** (Annotates the resulting hyper-methylated and hypo-methylated base sets with gene features (promoters, introns, exons, intergenic regions) for downstream functional interpretation.)

## Examples

```
hyper <- getMethylDiff(methylDiffObject, difference=25, qvalue=0.01, type='hyper'); hypo <- getMethylDiff(methylDiffObject, difference=25, qvalue=0.01, type='hypo')
```

## Evaluation signals

- Hyper-methylated and hypo-methylated base counts are both non-zero, indicating bidirectional methylation changes.
- Returned bases have q-value ≤ 0.01 and absolute percent methylation difference ≥ 25%.
- Base counts for each direction (hyper/hypo) match the vignette-reported or literature-expected values for the same reference dataset.
- The sum of hyper-methylated and hypo-methylated base counts does not exceed the total number of bases in the methylDiff object (no double-counting).
- Hyper-methylated bases show higher methylation percentage in the treatment/case group; hypo-methylated bases show lower methylation percentage in the treatment/case group relative to control.

## Limitations

- The q-value < 0.01 and 25% methylation difference thresholds are dataset-dependent; adjusted thresholds may be required for tissues or organisms with naturally lower methylation heterogeneity.
- Classification accuracy depends on adequate coverage (≥10 reads per base by default in methRead()) and balanced sample sizes; Fisher's exact test is used for small groups and logistic regression for larger cohorts, leading to different statistical power.
- Non-CpG methylation contexts (CHG, CHH) are not explicitly handled by the core workflow; users analyzing embryonic stem cells or plant tissues with non-CpG methylation must ensure appropriate context filtering before or after getMethylDiff().
- Overlapping or proximal differentially methylated bases are not automatically merged into regions; bases are classified individually, which may inflate counts if clustering is desired.

## Evidence

- [intro] After q-value calculation, we can select the differentially methylated regions/bases based on q-value and percent methylation difference cutoffs: "After q-value calculation, we can select the differentially methylated regions/bases based on q-value and percent methylation difference cutoffs"
- [intro] Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%: "Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%"
- [intro] The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression: "The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression"
- [intro] Traditionally, hypo-methylation is associated with gene transcription (if it is on a regulatory region such as promoters) and hyper-methylation is associated with gene repression: "Traditionally, hypo-methylation is associated with gene transcription (if it is on a regulatory region such as promoters) and hyper-methylation is associated with gene repression"
- [other] Using getMethylDiff() with q-value < 0.01 and 25% methylation difference cutoffs on example methylKit data yields separate hyper-methylated and hypo-methylated base objects, which can be extracted by specifying type="hyper" or type="hypo" parameters: "Using getMethylDiff() with q-value < 0.01 and 25% methylation difference cutoffs on example methylKit data yields separate hyper-methylated and hypo-methylated base objects, which can be extracted by"
