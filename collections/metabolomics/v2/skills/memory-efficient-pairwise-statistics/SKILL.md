---
name: memory-efficient-pairwise-statistics
description: Use when you have an MSI intensity matrix (msimat object) and an annotated
  mass-difference table (massdiff object with known or hypothesized parent–adduct
  ion pairs) where the number of peak pairs exceeds available RAM.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mass2adduct
  - R
  - Cardinal
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS
  data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into
  memory during an R session.
- corrPairsMSI(d,d.diff.annot)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct_cq
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04720
  all_source_dois:
  - 10.1021/acs.analchem.0c04720
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# memory-efficient-pairwise-statistics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute Pearson correlation statistics across all pairs of mass spectrometry peaks without loading the entire pairwise matrix into memory. This skill splits large ion-pair datasets into sequential chunks, processes each in parallel, and returns correlation coefficients with Bonferroni-corrected significance flags.

## When to use

You have an MSI intensity matrix (msimat object) and an annotated mass-difference table (massdiff object with known or hypothesized parent–adduct ion pairs) where the number of peak pairs exceeds available RAM. Apply this skill when you need to test whether candidate parent and adduct ions co-vary spatially across imaging pixels—a sign of true molecular adduction—but your dataset contains hundreds to thousands of peaks and direct pairwise correlation would exhaust memory.

## When NOT to use

- Your dataset contains fewer than ~100 peak pairs and fits comfortably in available RAM; use corrPairsMSI directly instead.
- You have only a mass list (no pixel intensity values); correlation testing requires spatial co-abundance data across pixels.
- Your mass-difference table contains no annotated matches (no parent–adduct candidates); run adductMatch or topAdducts first to identify candidate pairs.

## Inputs

- msimat object (MSI intensity matrix: pixels × masses)
- massdiff object (parent–adduct candidate pairs with matches column)

## Outputs

- annotated massdiff object with appended columns: Estimate, P.value, Significance

## How to apply

Load the MSI intensity matrix and the annotated massdiff object (containing a 'matches' column linking putative parent–adduct pairs). For datasets that fit in memory, call corrPairsMSI directly with the msimat and massdiff objects, specifying the default two-tailed Pearson correlation method. For larger datasets, invoke corrPairsMSIchunks instead, setting mem.limit (in GB) to a safe fraction of available RAM and ncores for parallel processing of each chunk. The function computes the Pearson correlation coefficient and raw p-value for each pair, then applies Bonferroni multiple-testing correction at α = 0.05 (default) to flag significant correlations. The output is the annotated massdiff object with three appended columns: Estimate (correlation coefficient), P.value (uncorrected), and Significance (boolean). Use this result to filter pairs showing statistically significant co-abundance patterns, which strengthens evidence for parent–adduct identity.

## Related tools

- **mass2adduct** (R package providing corrPairsMSI and corrPairsMSIchunks functions for memory-efficient pairwise correlation testing on MSI data) — https://github.com/kbseah/mass2adduct
- **R** (Runtime environment for invoking corrPairsMSI or corrPairsMSIchunks; parallelization via ncores parameter)
- **Cardinal** (MSI data processing package; MSProcessedImagingExperiment and MSContinuousImagingExperiment objects can be converted to msimat format prior to correlation testing) — http://cardinalmsi.org/

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); # Or for large datasets: d.diff.annot.cor <- corrPairsMSIchunks(d, d.diff.annot, mem.limit=4, ncores=4)
```

## Evaluation signals

- The returned massdiff object has three new numeric columns (Estimate, P.value, Significance) with lengths equal to the number of input peak pairs.
- Correlation coefficients (Estimate) fall in the range [−1, 1]; p-values are non-negative and ≤ 1.0.
- Bonferroni-corrected significance flags (Significance = TRUE) are rare when the number of pairs is large, consistent with stringent multiple-testing correction.
- Pairs with high spatial co-abundance (Significance = TRUE) should show visually consistent spatial distributions when plotted side-by-side on the imaging tissue.
- Re-running the same analysis on the same input data with identical parameters (mem.limit, ncores) yields identical Estimate and P.value columns (chunking should not change numerical results, only memory efficiency).

## Limitations

- Pearson correlation assumes linear relationships between parent and adduct ion intensities; nonlinear co-abundance patterns will not be detected.
- Bonferroni correction is conservative; with many pairs, the corrected significance threshold becomes very stringent, increasing false negatives.
- The msimunging.pl Perl script provided for converting large CSV files to triplet format is memory-limited by available RAM; datasets larger than available RAM may still fail even after conversion.
- Chunked processing (corrPairsMSIchunks) requires careful selection of mem.limit; if set too high, the process will crash; if set too low, speed gains from parallelization diminish due to excessive I/O overhead.

## Evidence

- [other] corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks in the annotated mass-difference object, generating correlation statistics for parent and adduct ion intensity pairs.: "corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks in the annotated mass-difference object, generating correlation statistics for parent and adduct ion"
- [other] For datasets exceeding available memory, invoke corrPairsMSIchunks instead, specifying mem.limit in GB and ncores for parallel processing to chunk the pairwise correlations.: "For datasets exceeding available memory, invoke corrPairsMSIchunks instead, specifying mem.limit in GB and ncores for parallel processing to chunk the pairwise correlations."
- [other] Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction).: "Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction)."
- [readme] Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction.: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [readme] For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function `corrPairsMSIchunks` instead of `corrPairsMSI`.: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function `corrPairsMSIchunks` instead of"
