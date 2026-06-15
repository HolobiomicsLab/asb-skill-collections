---
name: chromatin-accessibility-bias-correction
description: Use when you have loaded raw ATAC-seq fragment counts into a SummarizedExperiment object and are preparing to compute motif deviations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0749
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
  - BSgenome
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

# chromatin-accessibility-bias-correction

## Summary

Correct GC content bias in single-cell or bulk ATAC-seq chromatin accessibility counts before computing deviation scores. This preprocessing step ensures that downstream motif deviation analysis is not confounded by the strong relationship between GC content and chromatin accessibility.

## When to use

Apply this skill when you have loaded raw ATAC-seq fragment counts into a SummarizedExperiment object and are preparing to compute motif deviations. GC bias correction must occur early in the workflow, before sample/peak filtering and before computing expectations and deviations, because the bias term becomes part of the statistical model for deviation normalization.

## When NOT to use

- Input counts have already been corrected for GC bias by another method or tool.
- The organism or reference genome is not available as a BSgenome package; addGCBias() requires the genome parameter.
- Your analysis goal is clustering or dimensionality reduction without downstream motif deviation analysis; GC bias correction is specific to the deviation workflow and may not benefit purely unsupervised tasks.

## Inputs

- SummarizedExperiment object containing ATAC-seq fragment counts (assay slot with count matrix)
- BSgenome object (e.g., BSgenome.Hsapiens.UCSC.hg19) specifying the reference genome

## Outputs

- SummarizedExperiment object with updated rowData containing a 'bias' column with GC content bias term for each peak

## How to apply

Load the reference genome (e.g., BSgenome.Hsapiens.UCSC.hg19) as a BSgenome object. Call addGCBias() on your counts SummarizedExperiment, passing the genome object as the 'genome' parameter. This function computes the GC content for each peak region and adds a 'bias' column to the rowData slot. The bias values are then used downstream by computeExpectations() and computeDeviations() to generate GC-matched background peak sets and to normalize deviation scores. The rationale is that chromatin accessibility varies systematically with GC content due to sequencing and technical factors; explicitly modeling this bias allows computeDeviations() to compute residuals that reflect true motif-associated variability rather than GC artifacts.

## Related tools

- **chromVAR** (R package providing addGCBias() function for computing and storing GC bias term in SummarizedExperiment rowData) — https://github.com/GreenleafLab/chromVAR
- **BSgenome** (Bioconductor package providing reference genome sequences required to compute GC content at peak regions)
- **SummarizedExperiment** (Bioconductor package defining the S4 class structure in which bias-corrected counts and metadata are stored)

## Examples

```
example_counts <- addGCBias(example_counts, genome = BSgenome.Hsapiens.UCSC.hg19)
```

## Evaluation signals

- Verify that rowData(counts_object) contains a new 'bias' column with numeric values (GC content bias term) for each peak.
- Check that the bias column has non-zero, non-null values across the peak set; all peaks should have a computed bias.
- Confirm downstream computeExpectations() and computeDeviations() functions run without error, indicating the bias term is correctly formatted and compatible with the statistical model.
- Inspect the deviation scores produced by computeDeviations(); they should show biological signal (differential motif activity across cell types) rather than correlation with peak GC content.
- Compare motif deviation rankings before and after GC bias correction; motifs with high GC-content bias should show reduced spurious deviation signals post-correction.

## Limitations

- addGCBias() requires that the organism and genome build are available as a BSgenome package; custom or rare genomes may not have pre-built packages.
- GC bias modeling assumes a linear or monotonic relationship between GC content and accessibility; deviations from this assumption in highly unusual datasets may require custom bias models.
- The function adds a rowData column but does not modify the actual count matrix; bias correction is applied post-hoc during deviation computation, not by transforming counts directly.

## Evidence

- [intro] GC bias is a confounding factor that must be modeled before deviation computation: "The function `addGCBias` returns an updated SummarizedExperiment with a new rowData column named "bias""
- [readme] addGCBias() integrates the genome reference to extract GC content per peak: "example_counts <- addGCBias(example_counts, genome = BSgenome.Hsapiens.UCSC.hg19)"
- [intro] Bias correction must occur before filtering steps and deviation computation: "Add GC content bias to rowData using addGCBias() with the reference genome. 4. Filter samples using filterSamples()"
