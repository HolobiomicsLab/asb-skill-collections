---
name: cpg-base-filtering-by-statistical-threshold
description: Use when after calculateDiffMeth() has been run on a methylBase object and you have a methylDiff object with q-values and methylation difference estimates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0749
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

# CpG base filtering by statistical threshold

## Summary

Filter differentially methylated CpG bases from a methylDiff object using combined q-value and percent methylation difference thresholds to isolate statistically significant and biologically meaningful changes. This skill extracts hyper- and hypo-methylated base sets for downstream annotation and validation.

## When to use

After calculateDiffMeth() has been run on a methylBase object and you have a methylDiff object with q-values and methylation difference estimates. Apply this skill when you need to reduce the set of all tested CpG bases to a high-confidence subset meeting both statistical significance (q-value < 0.01) and minimum effect size (≥25% methylation difference) criteria for validation or annotation.

## When NOT to use

- Input is a raw methylation call file or methylRawList object that has not yet been merged and tested for differential methylation — use unite() and calculateDiffMeth() first.
- You have already applied sample-level filtering (coverage, PCR bias) but have not yet merged samples — call unite() before differential methylation testing.
- The analysis goal requires region-level rather than base-pair-level differential methylation — use regional or tiling window analysis functions instead.

## Inputs

- methylDiff object (output from calculateDiffMeth with q-values and percent methylation differences already computed)

## Outputs

- methylDiff object with hyper-methylated bases (type='hyper')
- methylDiff object with hypo-methylated bases (type='hypo')

## How to apply

Call getMethylDiff() on a methylDiff object with q-value threshold of 0.01 and percent methylation difference cutoff of 25%, specifying type='hyper' or type='hypo' to extract separate base objects for each direction of change. The q-value threshold controls false discovery rate from Fisher's exact test or logistic regression (automatically selected based on sample size in calculateDiffMeth), while the 25% methylation difference threshold ensures only bases with substantial changes in methylation percentage are retained. Extract hyper-methylated bases (increased methylation) and hypo-methylated bases (decreased methylation) as separate methylDiff objects for parallel validation. Validate output by confirming the resulting hyper and hypo base counts match expected values from prior runs or published vignettes.

## Related tools

- **methylKit** (R package providing methRead(), unite(), calculateDiffMeth(), and getMethylDiff() functions for methylation data loading, merging, statistical testing, and threshold-based filtering) — https://github.com/al2na/methylKit
- **Bismark** (Bisulfite mapping and methylation calling tool that generates input methylation call files for methylKit processing) — https://github.com/FelixKrueger/Bismark
- **genomation** (R package used for downstream annotation of filtered differentially methylated bases with gene annotation)

## Examples

```
getMethylDiff(methylDiff_object, difference=25, qvalue=0.01, type="hyper")
```

## Evaluation signals

- Resulting hyper-methylated and hypo-methylated base counts match published vignette or expected values from replicate runs
- All returned bases have q-value ≤ 0.01 when inspected in the output methylDiff object
- All returned bases have absolute percent methylation difference ≥ 25% when inspected in the output methylDiff object
- Hyper-methylated bases show positive percent methylation difference (sample1 > sample2); hypo-methylated bases show negative difference (sample1 < sample2)
- Output methylDiff objects are compatible with downstream genomation annotation functions, confirming proper object structure

## Limitations

- Fisher's exact test or logistic regression p-values are converted to q-values for multiple testing correction, but the method (Fisher vs. logistic) is automatically chosen by calculateDiffMeth based on sample size per group, not user control, potentially affecting statistical power for small sample sizes.
- The 25% methylation difference threshold is arbitrary and may not be biologically meaningful for all tissues or contexts — users should validate thresholds against prior knowledge of expected effect sizes in their system.
- Base-level filtering does not account for spatial clustering of methylated bases; consecutive or clustered changes may be more biologically meaningful than isolated individual bases.
- Heterogeneous samples (different cell types in the same sample) may confound methylation percentage estimates, leading to false positives or negatives in differential methylation calls.

## Evidence

- [intro] q-value and percent methylation difference thresholds for filtering: "Following bit selects the bases that have q-value<0.01 and percent methylation difference larger than 25%"
- [intro] getMethylDiff function returns separate hyper and hypo objects: "Using getMethylDiff() with q-value < 0.01 and 25% methylation difference cutoffs on example methylKit data yields separate hyper-methylated and hypo-methylated base objects, which can be extracted by"
- [intro] Statistical test selection based on sample size: "The calculateDiffMeth() function is the main function to calculate differential methylation. Depending on the sample size per each set it will either use Fisher's exact or logistic regression"
- [intro] Methylation status as percentage reflects sample heterogeneity: "Usually, the methylation status of a base determined by a high-throughput bisulfite sequencing will not be a binary score, but it will be a percentage"
- [intro] Hyper vs hypo methylation association with gene regulation: "Traditionally, hypo-methylation is associated with gene transcription (if it is on a regulatory region such as promoters) and hyper-methylation is associated with gene repression"
