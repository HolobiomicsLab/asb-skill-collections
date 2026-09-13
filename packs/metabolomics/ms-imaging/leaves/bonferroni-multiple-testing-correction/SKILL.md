---
name: bonferroni-multiple-testing-correction
description: Use when when you have performed many pairwise correlation tests between
  candidate parent and adduct ion intensity pairs in MSI data and need to identify
  statistically significant relationships while controlling for multiple-comparison
  bias.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3673
  tools:
  - mass2adduct
  - R
  - corrPairsMSI
  - corrPairsMSIchunks
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# bonferroni-multiple-testing-correction

## Summary

Apply Bonferroni multiple-testing correction to control family-wise error rate when performing many pairwise statistical tests (e.g., correlation tests) on mass spectrometry imaging data. This corrects raw p-values by dividing the significance threshold by the number of tests performed, reducing false positives in high-dimensional adduct discovery.

## When to use

When you have performed many pairwise correlation tests between candidate parent and adduct ion intensity pairs in MSI data and need to identify statistically significant relationships while controlling for multiple-comparison bias. Specifically, when corrPairsMSI or corrPairsMSIchunks outputs raw uncorrected p-values and you must flag which ion pairs show genuinely significant spatial co-occurrence after multiple-testing adjustment.

## When NOT to use

- When the number of pairwise tests is very small (< 10–20 pairs); Bonferroni becomes overly conservative and may fail to flag any pair as significant, especially if individual correlations are modest.
- When you have prior biological knowledge that restricts the hypothesis space (e.g., testing only 5 pre-specified adduct forms); use a less stringent correction method such as Benjamini–Hochberg FDR control instead.
- When raw p-values have not been computed yet; correction requires the full set of uncorrected test results to determine the multiple-comparison threshold.

## Inputs

- msimat object (MSI intensity matrix with spatial pixel coordinates and peak intensities)
- massdiff object with matches column (annotated mass-difference table identifying candidate parent–adduct pairs)
- raw p-values from pairwise Pearson correlation test (one per ion pair)

## Outputs

- Bonferroni-corrected significance flags (boolean: TRUE if raw p-value < α/n_tests, FALSE otherwise)
- Annotated massdiff object with appended Significance column marking statistically robust parent–adduct pairs

## How to apply

After performing Pearson correlation tests on all ion pairs in the massdiff object using corrPairsMSI, apply Bonferroni correction by dividing the significance threshold (default α=0.05) by the total number of pairwise tests performed. The corrPairsMSI function automatically computes a boolean Significance column that marks ion pairs where the raw p-value falls below the Bonferroni-adjusted threshold. Extract and retain only those pairs where Significance == TRUE, as these represent correlations unlikely to arise by chance alone across the large number of comparisons. The rationale is that with hundreds or thousands of peaks, many spurious correlations will appear significant at α=0.05 without correction; Bonferroni adjustment ensures that the reported adduct-parent pairs have controlled family-wise error rate.

## Related tools

- **corrPairsMSI** (Performs two-tailed Pearson correlation tests on each parent–adduct ion pair and returns raw p-values; Bonferroni correction is applied internally to flag Significance column) — https://github.com/kbseah/mass2adduct
- **corrPairsMSIchunks** (Memory-efficient variant of corrPairsMSI for large datasets; chunks pairwise correlations and applies Bonferroni correction within each chunk for parallel processing) — https://github.com/kbseah/mass2adduct
- **R** (Statistical computing environment in which Bonferroni correction is implemented (native statistical functions); mass2adduct package runs in R)

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); d.sig <- d.diff.annot.cor[d.diff.annot.cor$Significance==TRUE, ]
```

## Evaluation signals

- Significance column in output massdiff object contains only boolean TRUE/FALSE values; no NA or numerical values.
- The number of ion pairs flagged as significant (Significance==TRUE) is substantially smaller than the raw count of pairs with p < 0.05, confirming that correction has been applied.
- For any pair marked Significance==TRUE, verify that raw p-value < (0.05 / total_number_of_pairs_tested); spot-check a few rows to ensure correction threshold was correctly computed.
- When visualizing adduct ions with pointsAdducts(..., signif=TRUE), only ion pairs with Bonferroni-corrected significance are highlighted, and their number is reduced compared to an uncorrected plot.
- Downstream biological interpretation: retained adduct pairs should show high spatial correlation (r > 0.5 or similar) and biological plausibility (e.g., mass difference matches a known matrix or salt ion).

## Limitations

- Bonferroni correction is conservative, especially with thousands of peaks; in MSI data with hundreds of detected m/z values, many true adduct relationships may be rejected due to low statistical power. Consider FDR control as an alternative if you prioritize sensitivity.
- The correction assumes all pairwise tests are independent, which may not hold if ion intensities are spatially or biologically correlated. The README and article do not address dependence structure.
- No built-in threshold adjustment for different hypothesis classes (e.g., separate α for known versus novel adducts); a single α=0.05 is applied uniformly across all tests.

## Evidence

- [other] raw uncorrected p-value and Significance (boolean flag after Bonferroni multiple-testing correction): "Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction)."
- [other] Bonferroni p-value adjustment is the default in corrPairsMSI: "This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object."
- [other] corrPairsMSI output includes Bonferroni-corrected significance flags: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [other] Application of Bonferroni correction to MSI adduct correlation testing: "Call corrPairsMSI function, supplying both the msimat and annotated massdiff objects, specifying two-tailed Pearson correlation method (default)."
