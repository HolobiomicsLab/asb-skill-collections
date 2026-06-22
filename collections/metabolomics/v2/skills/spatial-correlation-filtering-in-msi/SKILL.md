---
name: spatial-correlation-filtering-in-msi
description: Use when after identifying candidate parent–adduct mass-difference pairs (via massdiff, histogram binning, and adductMatch), apply this skill to discriminate true molecular adducts from coincidental mass matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - Cardinal
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- library(mass2adduct)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04720
  all_source_dois:
  - 10.1021/acs.analchem.0c04720
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spatial-correlation-filtering-in-msi

## Summary

Test spatial correlation between putative parent and adduct ion pairs in mass spectrometry imaging data to validate that candidate adduct assignments reflect true co-localization in tissue. This filters out spurious mass-difference matches by exploiting the spatial dimension of MSI, retaining only ion pairs whose abundance patterns are significantly correlated across pixels.

## When to use

After identifying candidate parent–adduct mass-difference pairs (via massdiff, histogram binning, and adductMatch), apply this skill to discriminate true molecular adducts from coincidental mass matches. The spatial correlation test is essential when working with MSI data where pixel intensity maps are available, because abundance co-localization is strong evidence that two ions are biochemically related rather than random peak pairs.

## When NOT to use

- MSI data without pixel-wise intensity maps (e.g., only mass list, no spatial context).
- When parent and adduct ions are expected to have uncorrelated spatial distributions due to differential ionization efficiency or post-ionization loss.
- For non-imaging mass spectrometry data (e.g., liquid chromatography–MS or direct infusion) where spatial correlation cannot be computed.

## Inputs

- msimat object (preprocessed MSI data matrix with pixel intensities)
- massdiff object (pairwise mass differences, optionally subsetted to specific adduct types)

## Outputs

- data.frame with correlation p-values and Bonferroni-corrected significance flags for each ion pair
- annotated massdiff object with spatial correlation test results (class: massdiff + correlation metadata)

## How to apply

Given an msimat object (preprocessed MSI data matrix with pixel-wise intensity values) and a massdiff object subset to candidate adduct pairs (e.g., from diffGetPeaks or adductMatch), invoke corrPairsMSI() to compute Pearson correlation coefficients and p-values for each ion pair across all pixels. By default, use two-tailed testing with Bonferroni multiple-testing correction and a significance threshold of p < 0.05. Retain only ion pairs meeting this threshold as validated adducts. For very large datasets where all-pairs correlation would exhaust memory, use corrPairsMSIchunks() to process the massdiff object serially in chunks, accumulating p-value results. The output is a filtered data frame annotated with correlation statistics; downstream visualization with pointsAdducts() on this correlation-tested subset will show only spatially coherent parent–adduct pairs.

## Related tools

- **mass2adduct** (R package providing corrPairsMSI() and corrPairsMSIchunks() functions for computing spatial correlation between ion pairs in MSI data) — https://github.com/kbseah/mass2adduct
- **Cardinal** (MSI data processing package; mass2adduct can convert Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects to msimat format for downstream correlation analysis)

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); subset(d.diff.annot.cor, matches=='Na adduct' & pval < 0.05)
```

## Evaluation signals

- Output data frame contains exactly one p-value per ion pair in the input massdiff object.
- P-values lie in the valid range [0, 1]; no NaN or infinite values unless a pair was skipped due to zero variance.
- Number of significant pairs (p < 0.05 after Bonferroni correction) is substantially smaller than the input massdiff size, indicating genuine filtering.
- Visualization with pointsAdducts(..., signif=TRUE) on the filtered massdiff object shows spatially coherent red (adduct) and blue (parent) point clusters in the mass spectrum plot, not scattered random overlap.
- Correlation coefficients for retained pairs are positive and moderate to strong (r > 0.5), consistent with co-localization.

## Limitations

- Memory requirements scale quadratically with the number of peaks in the massdiff object; corrPairsMSIchunks() must be used for hundreds or thousands of peak pairs to avoid out-of-memory crashes.
- Correlation testing assumes linear spatial co-variation; highly nonlinear or discontinuous spatial patterns may yield false negatives.
- Bonferroni correction is conservative when the number of tests is very large; consider alternative multiple-testing methods (e.g., false discovery rate) for exploratory analysis.
- Pearson correlation assumes bivariate normality; heavy-tailed or skewed intensity distributions may reduce power to detect true adducts.

## Evidence

- [methods] Test for significant correlations between mass peaks: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [methods] Validation via co-localization: "If they are truly related by molecular adduct formation, then their abundances should be correlated."
- [readme] corrPairsMSI function signature: "d.diff.DHBH2O.corr <- corrPairsMSI(d, d.diff.DHBH2O)"
- [readme] Bonferroni correction and p-value threshold: "By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [readme] Memory management for large datasets: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function `corrPairsMSIchunks` instead of"
