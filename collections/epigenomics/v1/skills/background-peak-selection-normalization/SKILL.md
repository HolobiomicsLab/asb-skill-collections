---
name: background-peak-selection-normalization
description: Use when after computing expected accessibility from filtered peak and sample counts, and before computing final deviation scores. Use this skill when working with sparse ATAC-seq or DNase-seq data where GC bias and accessibility depth are known confounders of motif-associated variability.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
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

# background-peak-selection-normalization

## Summary

Select GC content and accessibility-matched background peaks to normalize bias-corrected deviation scores in chromatin accessibility analysis. This normalization step removes technical artifacts and ensures that motif deviation scores reflect true biological variability rather than GC or sequencing depth confounds.

## When to use

After computing expected accessibility from filtered peak and sample counts, and before computing final deviation scores. Use this skill when working with sparse ATAC-seq or DNase-seq data where GC bias and accessibility depth are known confounders of motif-associated variability.

## When NOT to use

- Input peaks are already aggregated or bulk-level; background-peak normalization is designed for single-cell or sample-level sparse data.
- No GC bias annotations are available in rowData; addGCBias() must be applied first.
- You are computing raw accessibility counts rather than motif-associated variability; use filterPeaks and filterSamples alone if the goal is QC, not deviation scoring.

## Inputs

- SummarizedExperiment object with filtered peak counts and rowData containing GC bias annotations
- Pre-computed expected accessibility values (from computeExpectations)
- Matrix of motif-to-peak matches (from matchMotifs)

## Outputs

- chromVARDeviations object (SummarizedExperiment) with two assays: deviations and deviationScores
- Normalized motif deviation scores (rows = motifs, columns = samples/cells)

## How to apply

Generate background peak sets using getBackgroundPeaks() to obtain peaks matched for GC content and accessibility level to each observed peak. These background peaks serve as control annotations for normalization. Pass the background peaks to computeDeviations() along with the motif-peak matches, filtered counts, and pre-computed expectations. The function will compute deviation scores as the difference between observed motif variability and the expected variability estimated from background peaks, thereby correcting for GC bias and sequencing depth effects. Validate that the deviation assay shows a reasonable distribution (e.g., mean near 0, standard deviation around 1) and that results are reproducible across independent background peak selections.

## Related tools

- **chromVAR** (Provides getBackgroundPeaks() and computeDeviations() functions for background-based normalization of motif deviations) — https://github.com/GreenleafLab/chromVAR
- **SummarizedExperiment** (Data structure holding filtered counts, GC bias annotations, and output deviation assays)
- **motifmatchr** (Provides matchMotifs() output (peak-to-motif match matrix) required as input to computeDeviations()) — https://github.com/GreenleafLab/motifmatchr

## Examples

```
dev <- computeDeviations(object = counts_filtered, annotations = motif_ix, background_peaks = bg_peaks)
```

## Evaluation signals

- Deviation assay has correct dimensions (motif count = rows, sample count = columns)
- Deviation scores have mean approximately 0 and standard deviation approximately 1 (normalized distribution)
- deviationScores assay exists and contains z-score or similar standardized values
- Motifs with strong expected deviation from background show higher absolute deviation scores than low-variance motifs
- Re-running with different random background peak selections produces highly correlated deviation scores (robustness check)

## Limitations

- Background peak selection relies on sufficient peak density for robust GC and accessibility matching; sparse peak sets may yield unreliable background pools.
- Assumes that GC content and overall accessibility are the primary technical confounders; other sources of bias (e.g., library complexity, batch effects) are not directly corrected.
- Method is sensitive to the quality of the input expectations and motif-peak matches; errors in filterSamples, filterPeaks, or matchMotifs will propagate to deviation scores.
- No changelog documented for chromVAR; reproducibility across versions may require explicit version pinning.

## Evidence

- [other] Generate background peaks using getBackgroundPeaks() to obtain GC and accessibility-matched peak sets for normalization.: "Generate background peaks using getBackgroundPeaks() to obtain GC and accessibility-matched peak sets for normalization"
- [other] The computeDeviations function returns a SummarizedExperiment object containing deviation scores that quantify motif-associated variability in chromatin accessibility across samples: "The computeDeviations function returns a SummarizedExperiment object containing deviation scores that quantify motif-associated variability in chromatin accessibility across samples"
- [other] Compute bias-corrected deviations using computeDeviations() with filtered counts, motif matches, background peaks, and computed expectations to produce the final chromVARDeviations object.: "Compute bias-corrected deviations using computeDeviations() with filtered counts, motif matches, background peaks, and computed expectations to produce the final chromVARDeviations object"
- [readme] The package aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples: "aims to identify motifs or other genomic annotations associated with variability in chromatin accessibility between individual cells or samples"
- [other] Validate output structure (two assays: deviations and deviationScores), row count (motif count), column count (sample count), and score distributions.: "Validate output structure (two assays: deviations and deviationScores), row count (motif count), column count (sample count), and score distributions"
