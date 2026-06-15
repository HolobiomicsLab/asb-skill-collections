---
name: variability-score-comparison-across-parameter-sets
description: Use when when you have computed deviation and variability scores using chromVAR for two or more discrete parameter configurations (e.g., 6-mer vs 7-mer kmers, or different motif databases) and need to determine which parameter set produces stronger or more discriminative variability signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3169
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
- library(motifmatchr)
- library(SummarizedExperiment)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chromvar
    doi: 10.1038/nmeth.4401
    title: chromvar
  dedup_kept_from: coll_chromvar
schema_version: 0.2.0
---

# variability-score-comparison-across-parameter-sets

## Summary

Compare chromatin accessibility variability scores computed across different kmer sizes (or other discrete parameter choices) to determine which configuration yields higher magnitude deviations. This skill enables quantitative assessment of how annotation granularity affects deviation signal strength in chromVAR workflows.

## When to use

When you have computed deviation and variability scores using chromVAR for two or more discrete parameter configurations (e.g., 6-mer vs 7-mer kmers, or different motif databases) and need to determine which parameter set produces stronger or more discriminative variability signals. Use this skill to move beyond single-configuration analysis to empirically justify parameter choice.

## When NOT to use

- You have only one parameter configuration and no comparison set; this skill requires ≥2 parameter sets.
- Your variability scores have already been normalized or transformed in a way that makes raw magnitude comparison invalid.
- The input counts have not been filtered for sufficient depth (min_depth) and peak representation (min_in_peaks) — filtering must precede kmer annotation and deviation computation.

## Inputs

- SummarizedExperiment object with GC-bias-corrected and filtered counts (output from filterPeaks)
- Kmer annotation indices from matchKmers() for two or more kmer sizes (e.g., 6-mer and 7-mer)
- Deviation objects computed via computeDeviations() for each kmer size

## Outputs

- Tabulated summary statistics (mean, median, standard deviation) of variability scores per kmer size
- Comparative distribution summary enabling ranking of parameter sets by variability magnitude

## How to apply

After computing deviations and variability scores independently for each parameter set using computeDeviations() and computeVariability(), extract the variability score distributions from each resulting object. Tabulate summary statistics (mean, median, standard deviation) for each kmer size or annotation set. Compare distributions using these descriptive statistics; higher mean or median variability scores indicate that the parameter set captures more pronounced accessibility differences. The rationale is that kmer size affects annotation density and specificity: larger kmers (e.g., 7-mer vs 6-mer) may concentrate deviation signal on fewer, more specific sequence motifs, yielding higher per-motif variability. Organize results in a table to enable side-by-side comparison and visual inspection of the distributions.

## Related tools

- **chromVAR** (Core package providing computeDeviations(), computeVariability(), and matchKmers() functions for kmer annotation and deviation scoring) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Provides matchKmers() function to generate kmer annotation matrices from genome sequences)
- **BSgenome.Hsapiens.UCSC.hg19** (Supplies reference genome sequence required by matchKmers() for kmer matching)
- **BiocParallel** (Enables efficient parallelization of computeDeviations() and computeVariability() across large kmer annotation sets)
- **R** (Language and environment for running chromVAR functions and computing summary statistics)

## Examples

```
# After filtering counts and computing deviations for 6-mer and 7-mer:
kmer_6_stats <- data.frame(
  kmer_size = 6,
  mean_var = mean(variability(dev_6mer)),
  median_var = median(variability(dev_6mer)),
  sd_var = sd(variability(dev_6mer))
)
kmer_7_stats <- data.frame(
  kmer_size = 7,
  mean_var = mean(variability(dev_7mer)),
  median_var = median(variability(dev_7mer)),
  sd_var = sd(variability(dev_7mer))
)
comparison_table <- rbind(kmer_6_stats, kmer_7_stats)
print(comparison_table)
```

## Evaluation signals

- Both kmer size configurations produce non-null, finite variability scores with no missing values in the summary statistics table.
- The 7-mer variability distribution shows a measurably higher mean or median than the 6-mer distribution, supporting the hypothesis that larger kmers concentrate signal on fewer motifs.
- Standard deviation and range (min/max) of variability scores are reported for each kmer set, enabling assessment of distribution shape and spread.
- No negative or unexpectedly small (near-zero) variability values appear in the summary, indicating successful deviation computation.
- The tabulated results can be visualized (e.g., via box plot or histogram) to confirm that distributions are visually distinct and the comparison is interpretable.

## Limitations

- Comparison validity depends on identical filtering steps (filterSamples, filterPeaks) applied to the same input counts before separate kmer annotation; any difference in pre-processing confounds the comparison.
- Variability score magnitude is sensitive to GC bias correction (addGCBias); results are specific to the chosen genome reference and bias model.
- SnapATAC has been reported to outperform chromVAR for clustering tasks; this skill validates kmer utility for deviation annotation, not clustering performance.
- Summary statistics (mean, median, SD) may not fully capture distribution shape differences; visual or formal statistical tests (e.g., Kolmogorov–Smirnov) may be needed for rigorous comparison.
- Kmer matching is computationally expensive for larger kmers; practical comparison is typically limited to nearby sizes (e.g., 6 vs 7) rather than widely divergent choices.

## Evidence

- [other] research_question: "Does kmer size (6-mer vs 7-mer) affect the magnitude of chromatin accessibility variability scores computed by chromVAR?"
- [other] finding_confirmation: "Extract and tabulate mean, median, and standard deviation of variability scores for both kmer sets, then compare distributions to confirm 7-mers yield higher variability than 6-mers."
- [readme] tool_role: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [readme] kmer_rationale: "Using kmers + PCA appears to be the best variant of chromVAR for clustering"
- [readme] workflow_step: "Generate 6-mer kmer annotation matrix using matchKmers(6, counts_filtered, genome=BSgenome.Hsapiens.UCSC.hg19), then compute deviations with computeDeviations(counts_filtered, kmer_ix_6mer)."
