---
name: bias-corrected-z-score-interpretation
description: Use when after computeDeviations has generated a SummarizedExperiment object with z-score assays reflecting bias-corrected deviations of observed vs. expected accessibility at motif or kmer sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0749
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

# bias-corrected-z-score-interpretation

## Summary

Interpret deviation z-scores computed by chromVAR as bias-corrected measures of individual or sample-level deviations from expected chromatin accessibility patterns at annotated genomic features (motifs or kmers). This skill enables ranking and differential testing of annotations by their variability across cells or samples.

## When to use

After computeDeviations has generated a SummarizedExperiment object with z-score assays reflecting bias-corrected deviations of observed vs. expected accessibility at motif or kmer sites. Use this skill when you need to (1) rank annotations by their across-sample/cell variability, (2) identify which annotations show statistically significant differential usage between cell types or conditions, or (3) understand which individual samples/cells deviate most from the accessibility baseline at a given annotation.

## When NOT to use

- Input counts have not been filtered for GC bias using addGCBias — bias correction requires explicit bias annotation in the input object
- Raw count matrix is the input; z-scores must first be computed via computeDeviations before interpretation
- Analyzing bulk ATAC-seq without single-cell resolution, where sample-level deviation interpretation differs fundamentally from cell-level interpretation

## Inputs

- chromVARDeviations object (SummarizedExperiment with z-score assays from computeDeviations)
- Cell or sample metadata (colData) including grouping variables (e.g., cell_type, sample_id)
- Optionally: pre-defined grouping variable name for differential testing (e.g., 'Cell_Type')

## Outputs

- Variability scores per annotation (standard deviation of z-scores across samples)
- Bootstrap confidence intervals around variability estimates
- Ranked list of annotations sorted by variability
- Differential deviation test results (p-values, effect sizes, adjusted p-values per annotation and group pair)
- Visualization of ranked annotations (via plotVariability)

## How to apply

The deviation z-scores returned by chromVAR's computeDeviations function account for GC bias in the input ATAC/DNAse-seq counts, allowing fair comparison across genomic regions with different nucleotide composition. To interpret: (1) Extract the z-score assay from the deviation object; high absolute z-scores indicate samples/cells with higher or lower accessibility at that annotation than the genome-wide expectation. (2) Apply computeVariability to compute the standard deviation of z-scores across samples for each annotation, yielding a variability ranking; annotations with higher variance indicate those whose chromatin state varies most across the population. (3) For differential testing across cell types, use differentialDeviations to test whether the mean or distribution of z-scores differs significantly between groups (e.g., GM vs. H1 cell lines); this controls for the bias correction already embedded in the z-scores. (4) Evaluate results using bootstrap confidence intervals (generated during computeVariability) and hypothesis tests against null variability thresholds to assess statistical significance.

## Related tools

- **chromVAR** (Computes bias-corrected z-score deviations and variability metrics; provides computeDeviations, computeVariability, and differentialDeviations functions) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Generates motif-to-peak annotation matrices (input to computeDeviations) prior to z-score derivation) — https://github.com/GreenleafLab/motifmatchr
- **SummarizedExperiment** (Container class for deviation object with z-score assays and colData metadata)
- **BiocParallel** (Enables parallelized variability and differential deviation computation)

## Examples

```
dev <- computeDeviations(counts_filtered, motif_ix); variability <- computeVariability(dev); diff_dev <- differentialDeviations(dev, "Cell_Type")
```

## Evaluation signals

- Variability scores (standard deviations) are positive, finite, and rank-ordered; confidence intervals are non-zero and contain point estimates
- Z-scores in deviation assay have mean ≈ 0 and standard deviation ≈ 1 per annotation after bias correction (check via summary statistics)
- Differential deviation test p-values follow expected distribution under null (uniform on [0, 1]); significant findings (adjusted p < 0.05) show reproducible effect sizes across independent samples
- plotVariability output shows visually distinct rank separation between high and low variability annotations; no annotations with undefined or infinite scores
- Z-scores correlate inversely with GC content bias when compared to raw deviation before correction (bias correction should reduce spurious GC-driven signals)

## Limitations

- Z-score interpretation assumes approximately normal distribution of deviations; extreme outlier samples may inflate variability estimates and require robust variance methods
- Differential deviation testing requires sufficient sample size per group (>2–3 samples recommended) and balanced group designs for reliable effect size estimation
- Bootstrap confidence intervals can be wide when sample size is small or annotations occur in few peaks; results should be interpreted with uncertainty quantification
- Newer methods such as SnapATAC outperform chromVAR for clustering tasks; bias-corrected z-scores are best used for annotation ranking and motif discovery rather than dimensionality reduction or cell clustering

## Evidence

- [intro] ChromVAR identifies motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples: "aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [readme] The computeDeviations function returns a SummarizedExperiment with z-score assays reflecting bias-corrected deviations: "The function `computeDeviations` returns a SummarizedExperiment with two "assays""
- [other] ComputeVariability computes standard deviation of z-scores and generates bootstrap confidence intervals for hypothesis testing: "Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests"
- [other] DifferentialDeviations tests for significant differences in bias-corrected deviations between cell type groups using colData annotations: "Call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between GM and H1 cell groups using the colData cell-type annotation."
- [readme] Additive GC bias correction is required before deviation interpretation to ensure fair comparison across regions: "The function `addGCBias` returns an updated SummarizedExperiment with a new rowData column named "bias""
