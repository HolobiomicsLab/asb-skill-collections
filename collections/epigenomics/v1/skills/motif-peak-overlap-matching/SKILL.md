---
name: motif-peak-overlap-matching
description: Use when you have a filtered set of non-overlapping peaks from ATAC-seq data and a collection of motifs (typically from JASPAR or similar databases), and you need to identify which peaks contain matches to which motifs as a prerequisite for computing motif-based deviation scores across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0239
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3169
  - http://edamontology.org/topic_0654
  tools:
  - chromVAR
  - R
  - motifmatchr
  - SummarizedExperiment
  - BiocParallel
  - BSgenome.Hsapiens.UCSC.hg19
  - JASPAR
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

# motif-peak-overlap-matching

## Summary

Match transcription factor motifs to chromatin accessibility peaks to identify which peaks contain which DNA binding motifs. This is an essential preprocessing step that links motif occurrence to peak regions before computing deviation scores in chromatin accessibility analysis.

## When to use

Apply this skill when you have a filtered set of non-overlapping peaks from ATAC-seq data and a collection of motifs (typically from JASPAR or similar databases), and you need to identify which peaks contain matches to which motifs as a prerequisite for computing motif-based deviation scores across samples.

## When NOT to use

- You already have pre-computed motif-peak matches from another tool or database and do not need to re-match.
- Your peaks have not been filtered for quality or overlaps, as matching on unfiltered peak sets may produce spurious or redundant motif calls.
- Your reference genome does not match your peak coordinate system (e.g., peaks are from hg38 but you provide hg19).

## Inputs

- motif collection (e.g., JASPAR motifs as PWMatrix or PWMatrixList)
- filtered peaks (GenomicRanges object)
- reference genome (BSgenome object, e.g., BSgenome.Hsapiens.UCSC.hg19)

## Outputs

- motif-peak index object (sparse binary matrix or similar structure indicating which peaks contain which motifs)

## How to apply

Use the matchMotifs function from the motifmatchr package, providing the motif collection, the filtered peak set as a GenomicRanges object, and a reference genome (e.g., BSgenome.Hsapiens.UCSC.hg19). The function performs sequence matching to determine peak-motif overlaps. The resulting motif-to-peak index object stores which peaks contain which motifs, and this becomes the 'annotations' argument for downstream computeDeviations. The matching is genome-aware: it retrieves sequences from the reference genome corresponding to each peak region and scans for motif matches using position weight matrices, enabling accurate identification of potential transcription factor binding sites.

## Related tools

- **motifmatchr** (Performs sequence matching of motifs to peak regions; returns peak-to-motif index used as annotations argument for computeDeviations) — https://github.com/GreenleafLab/motifmatchr
- **chromVAR** (Parent package that uses motif-peak matches to compute deviation scores; matchMotifs output is passed directly to computeDeviations) — https://github.com/GreenleafLab/chromVAR
- **BSgenome.Hsapiens.UCSC.hg19** (Provides reference genome sequence required by matchMotifs to retrieve peak sequences and perform motif scanning)
- **JASPAR** (Source database for motif position weight matrices; accessed via getJasparMotifs to obtain motif collection for matching)

## Examples

```
motif_ix <- matchMotifs(motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19)
```

## Evaluation signals

- Output object is non-empty and has same number of rows as input motifs and same number of columns as input peaks
- Motif-peak matches are sparse (not all motifs match all peaks), reflecting biological selectivity
- Spot-check: verify that peaks containing known TFBS sequences for a query motif are present in the match output
- No errors or warnings indicating genome coordinate mismatches or missing sequences during matching
- Downstream computeDeviations step completes successfully using the motif-peak index, producing a valid SummarizedExperiment with non-NaN deviation scores

## Limitations

- Matching quality depends on motif position weight matrix accuracy and completeness; weak or degenerate motifs may produce false positives.
- Results are sensitive to genome version and peak coordinate system; mismatches cause sequence lookup failures or spurious matches.
- Motif matching does not account for in vivo chromatin state, DNA methylation, or nucleosome positioning; matches represent potential binding sites, not confirmed occupancy.
- Computational cost scales with peak count and motif collection size; very large peak sets (>1M) may require parallel processing or memory optimization.
- Single-bp resolution matching may miss composite binding sites or cooperative TF interactions that require multi-motif analysis.

## Evidence

- [other] The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs: "The function `matchMotifs` from the motifmatchr package finds which peaks contain which motifs"
- [other] Match motifs to filtered peaks using matchMotifs() from motifmatchr package with the reference genome: "Match motifs to filtered peaks using matchMotifs() from motifmatchr package with the reference genome"
- [other] Compute bias-corrected deviations using computeDeviations() with filtered counts, motif matches, background peaks, and computed expectations to produce the final chromVARDeviations object: "motif matches, background peaks, and computed expectations to produce the final chromVARDeviations object"
- [readme] motif_ix := matchMotifs(motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19): "motif_ix := matchMotifs(motifs, counts_filtered, genome = BSgenome.Hsapiens.UCSC.hg19)"
