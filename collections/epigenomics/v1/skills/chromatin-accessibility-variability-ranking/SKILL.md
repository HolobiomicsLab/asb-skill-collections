---
name: chromatin-accessibility-variability-ranking
description: Use when you have sparse, single-cell or bulk ATAC/DNAse-seq data from multiple cell types or conditions (e.g., GM vs H1 cell lines), pre-filtered and GC-bias-corrected, with motif-to-peak matches already computed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3672
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - chromVAR
  - R
  - SummarizedExperiment
  - motifmatchr
  - BSgenome.Hsapiens.UCSC.hg19
  - BiocParallel
  - SnapATAC
derived_from:
- doi: 10.1038/nmeth.4401
  title: chromvar
evidence_spans:
- chromVAR is an R package for the analysis of sparse chromatin accessibility
- computeVariability(dev)
- An R package for the analysis of sparse chromatin accessibility
- library(chromVAR)
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

# chromatin-accessibility-variability-ranking

## Summary

Rank transcription factor motifs by their contribution to variability in chromatin accessibility across cell populations, and identify motifs showing statistically significant differential deviation between distinct cell types. This enables discovery of cell-type-specific regulatory patterns driving heterogeneity in chromatin state.

## When to use

You have sparse, single-cell or bulk ATAC/DNAse-seq data from multiple cell types or conditions (e.g., GM vs H1 cell lines), pre-filtered and GC-bias-corrected, with motif-to-peak matches already computed. You want to discover which transcription factor motifs contribute most to observed accessibility variation within and between populations, and to test whether motif usage differs significantly by cell type.

## When NOT to use

- Input counts have not been filtered for sample depth (min_depth), peak overlap, or GC bias correction — use filterSamples, filterPeaks, and addGCBias first.
- Motifs have not yet been matched to peaks — use matchMotifs and computeDeviations before this skill.
- You seek to cluster cells or perform dimensionality reduction based on chromatin patterns — use SnapATAC or k-mer + PCA approaches instead, as chromVAR has been superseded for that task.

## Inputs

- chromVARDeviations object (SummarizedExperiment) with pre-computed deviations from filtered example_counts and matched JASPAR motifs

## Outputs

- Ranked motif variability table (standard deviations, bootstrap confidence intervals, hypothesis test p-values)
- Differential deviations test results table (p-values, effect sizes, bias-corrected deviation differences per motif by cell type)
- Variability rank plot (plotVariability output)

## How to apply

Load a pre-computed chromVARDeviations object (obtained via computeDeviations on bias-corrected, filtered counts and motif annotations). Call computeVariability() to compute the standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests against a null variability of 1. Rank motifs by their variability score and visualize using plotVariability(). Then call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between the two cell groups using the colData cell-type annotation. Export both the ranked variability results and differential-deviation test results (p-values and effect sizes per motif) as structured tables for downstream interpretation.

## Related tools

- **chromVAR** (Core package for computing motif deviations, variability scores, and differential deviation tests on chromatin accessibility data) — https://github.com/GreenleafLab/chromVAR
- **motifmatchr** (Matches motif positions within peaks using the matchMotifs function; required input preparation step) — https://github.com/GreenleafLab/motifmatchr
- **SummarizedExperiment** (Data structure for storing deviations, metadata, and colData annotations (cell type labels) needed for differential testing)
- **BSgenome.Hsapiens.UCSC.hg19** (Reference genome required for GC bias computation and motif matching in human datasets)
- **BiocParallel** (Enables parallel computation of variability and differential deviation tests across many motifs)
- **SnapATAC** (Alternative or complementary tool for single-cell ATAC analysis; outperforms chromVAR for clustering but chromVAR is preferred for annotating motif usage patterns) — https://github.com/r3fang/SnapATAC

## Examples

```
computeVariability(dev); differentialDeviations(dev, "Cell_Type")
```

## Evaluation signals

- Variability ranks are non-negative and sorted in descending order; bootstrap confidence intervals do not include zero for high-variability motifs, confirming non-trivial deviation.
- Hypothesis test p-values against null variability of 1 are properly calibrated (distribution skewed toward small p-values for top-ranked motifs); differentialDeviations p-values are well-behaved and accompany effect size estimates.
- Differential deviation results show consistent effect direction within each cell type group; motifs with small p-values exhibit substantial fold-change differences in mean deviation between GM and H1 cell populations.
- Plotted rank-sorted motifs show monotonic decrease in variability; no missing or NaN values in output tables; motif counts match the input JASPAR set after any filtering.
- Results are interpretable as biological signals (e.g., known GM or H1 lineage-specific TFs rank high in differential tests) and consistent with independent validation (e.g., prior literature on cell-type-specific regulatory networks).

## Limitations

- Newer single-cell clustering methods such as SnapATAC outperform chromVAR for the clustering task, though chromVAR remains a useful complementary tool for motif annotation rather than cell identification.
- The method is sensitive to sparse data and low sequencing depth; filtered samples must meet minimum read depth and peak coverage thresholds or results become unreliable.
- Variability and differential deviation scores depend critically on accurate GC bias correction and prior removal of overlapping peaks; biased or incomplete preprocessing propagates into ranking and test statistics.
- Bootstrap confidence intervals and p-values assume resampling preserves the underlying distribution; results may be unstable if the number of cells/samples is very small or imbalanced between cell types.

## Evidence

- [other] chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples, enabling ranking and differential analysis of motif usage.: "chromVAR is designed to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [other] Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests against null variability of 1.: "Call computeVariability(dev) to compute standard deviation of z-scores across samples for each motif, generate bootstrap confidence intervals by resampling cells/samples, and perform hypothesis tests"
- [other] Call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between GM and H1 cell groups using the colData cell-type annotation.: "Call differentialDeviations(dev, "Cell_Type") to test for significant differences in bias-corrected deviations between GM and H1 cell groups using the colData cell-type annotation"
- [readme] chromVAR may be complementary to some other methods, as a way of annotating TF motif usage in cells & clusters rather than cluster identification or embedding.: "chromVAR may be complementary to some other methods, as a way of annotating TF motif usage in cells & clusters rather than cluster identification or embedding"
- [readme] newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper: "newer methods such as SnapATAC outperform chromVAR for the clustering tasks evaluated in the paper"
