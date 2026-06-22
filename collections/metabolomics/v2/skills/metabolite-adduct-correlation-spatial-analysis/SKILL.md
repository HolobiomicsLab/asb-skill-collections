---
name: metabolite-adduct-correlation-spatial-analysis
description: Use when you have annotated mass-difference peaks with known adduct identities (via mass-matching to reference adduct tables) and possess MSI intensity matrices where each peak's abundance is measured across multiple tissue pixels or voxels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3168
  tools:
  - mass2adduct
  - R
  - corrPairsMSI
  - corrPairsMSIchunks
  - msimat
  - massdiff
  - adductMatch
  - pointsAdducts
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into memory during an R session.
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
---

# metabolite-adduct-correlation-spatial-analysis

## Summary

Test spatial co-localization of candidate parent and adduct ion pairs in mass spectrometry imaging data using two-tailed Pearson correlation on pixel-wise intensity profiles. This skill validates putative adduct assignments by testing whether annotated ion pairs exhibit correlated abundance patterns across tissue pixels, a prerequisite for establishing true molecular relationships.

## When to use

You have annotated mass-difference peaks with known adduct identities (via mass-matching to reference adduct tables) and possess MSI intensity matrices where each peak's abundance is measured across multiple tissue pixels or voxels. Apply this skill to discriminate true adduct pairs from spurious mass-difference matches by requiring spatial correlation of intensities; adducts arising from the same parent molecule should co-vary across the imaging field.

## When NOT to use

- MSI data are not available or have been aggregated to bulk spectra; corrPairsMSI requires per-pixel or per-voxel intensity values and cannot work on summed or average spectra.
- Adduct pairs have not been pre-annotated against a reference list; this skill validates existing annotations rather than discovering new adducts de novo.
- Pixel-wise intensities are not independent or are heavily autocorrelated spatially; Pearson correlation assumes independence and will yield inflated false positives if spatial structure is extreme.

## Inputs

- msimat object (MSI intensity matrix with peaks as columns and pixels as rows)
- massdiff object with annotated matches column (output from adductMatch or topAdducts with manual curation)

## Outputs

- annotated massdiff object with appended columns: Estimate (correlation coefficient), P.value (uncorrected p-value), Significance (boolean flag post-Bonferroni correction)
- correlation statistics table suitable for filtering and visualization

## How to apply

Load the MSI intensity matrix (msimat object) and the adduct-annotated mass-difference table (massdiff object with matches column populated by adductMatch or similar) into R. Invoke corrPairsMSI() with both objects and default parameters (two-tailed Pearson correlation); this performs correlation testing on every annotated parent–adduct pair, yielding raw p-values and Bonferroni-corrected significance flags. For datasets exceeding available memory—hundreds or thousands of peaks—use corrPairsMSIchunks() instead, specifying mem.limit in GB and ncores for parallel processing to avoid memory crashes. Extract and interpret the three output columns: Estimate (the correlation coefficient, typically 0 to 1 for co-varying adducts), P.value (raw uncorrected p-value), and Significance (boolean after multiple-testing correction at α=0.05). Annotate the mass spectrum using pointsAdducts() to visualize parent and adduct peaks passing the correlation filter.

## Related tools

- **corrPairsMSI** (Primary function performing two-tailed Pearson correlation test on each annotated parent–adduct ion pair across all pixels in the MSI dataset.) — https://github.com/kbseah/mass2adduct
- **corrPairsMSIchunks** (Memory-efficient variant of corrPairsMSI for large datasets; chunks pairwise correlations serially or in parallel to avoid memory exhaustion.) — https://github.com/kbseah/mass2adduct
- **msimat** (Data structure constructor and I/O function; loads CSV-exported MSI intensity data (from Cardinal, SCiLS, MSiReader) into R as the intensity matrix required by correlation functions.) — https://github.com/kbseah/mass2adduct
- **massdiff** (Data structure and function for representing and computing pairwise mass differences between peaks; must be pre-annotated with adduct matches before correlation testing.) — https://github.com/kbseah/mass2adduct
- **adductMatch** (Matches observed mass differences (from histogram bins) to a reference adduct table, populating the matches column required as input to correlation testing.) — https://github.com/kbseah/mass2adduct
- **pointsAdducts** (Visualization function for annotating mass spectra with parent and adduct ion identities after correlation filtering; highlights significant correlations.) — https://github.com/kbseah/mass2adduct
- **R** (Programming environment and statistical computing platform required to execute mass2adduct functions and Pearson correlation tests.)

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); # or for large datasets: d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot, how='parallel', ncores=4)
```

## Evaluation signals

- Correlation coefficients for true adduct pairs should be significantly > 0 (typically 0.6–1.0) with P.value < 0.05 after Bonferroni correction; pairs failing this criterion should be discarded as false positives.
- Output massdiff object must contain exactly three new columns: Estimate (numeric), P.value (numeric ≥ 0), and Significance (boolean); verify schema and row count matches input.
- Bonferroni correction factor should equal the number of unique parent–adduct pairs tested; verify reported p-value thresholds are consistent with α=0.05 / (number of tests).
- Visualization via pointsAdducts() should show parent and adduct ions (marked in distinct colors, e.g., parent black, adduct red) only for peaks passing correlation significance threshold, confirming filtering was applied.
- For memory-chunked runs (corrPairsMSIchunks), concatenated results should be identical to non-chunked runs on the same input when chunk size and ncores allow full coverage, confirming serialization correctness.

## Limitations

- Pearson correlation assumes linear relationships and bivariate normality; heavily skewed or zero-inflated intensity distributions may yield inaccurate p-values.
- Bonferroni correction is conservative and may mask true correlations when thousands of pairs are tested; consider alternative multiple-testing methods (e.g., FDR) for exploratory analyses.
- No changelog or versioning system documented in the repository, limiting reproducibility tracking and the ability to identify which version of mass2adduct was used in a published workflow.
- corrPairsMSIchunks is available only for Unix-like systems when using parallel processing (how='parallel'); Windows users must use serial chunking or the non-chunked corrPairsMSI function.
- Spatial autocorrelation in tissue imaging can inflate correlation coefficients and p-value significance if pixels are not treated as independent samples; the method does not account for spatial clustering or tissue heterogeneity.

## Evidence

- [other] corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks in the annotated mass-difference object: "corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks in the annotated mass-difference object, generating correlation statistics for parent and adduct ion"
- [other] Call corrPairsMSI function, supplying both the msimat and annotated massdiff objects, specifying two-tailed Pearson correlation method (default).: "Call corrPairsMSI function, supplying both the msimat and annotated massdiff objects, specifying two-tailed Pearson correlation method (default)."
- [other] For datasets exceeding available memory, invoke corrPairsMSIchunks instead, specifying mem.limit in GB and ncores for parallel processing: "For datasets exceeding available memory, invoke corrPairsMSIchunks instead, specifying mem.limit in GB and ncores for parallel processing to chunk the pairwise correlations."
- [other] Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction).: "Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction)."
- [readme] Test for spatial correlations between mass peaks in MS imaging data to see if putative parent- and derivative-ion masses tend to occur together and their abundances are correlated.: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function). For example, we wish to see if what we believe to be pairs of parent- and derivative-ion"
- [readme] By default the cutoff for significance is p=0.05 with Bonferroni correction.: "By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [readme] For large data sets, where the tables would not fit into memory, use the function `corrPairsMSIchunks` instead of `corrPairsMSI`.: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function `corrPairsMSIchunks` instead of"
