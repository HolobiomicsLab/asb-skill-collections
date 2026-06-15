---
name: adduct-ion-parent-ion-pairing-analysis
description: Use when when you have binned mass spectrometry imaging peaks and want to understand which detected mass-to-charge ratios represent the same metabolite in different ionization states (parent vs. adduct form).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mass2adduct
  - R
  - Cardinal
  - SCiLS
  - MSiReader
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- library(mass2adduct)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct
schema_version: 0.2.0
---

# Adduct-Ion Parent-Ion Pairing Analysis

## Summary

Identify and validate parent–adduct ion pairs in MALDI-MSI data by matching mass differences to known chemical adducts (e.g., sodium, potassium, matrix ions) and confirming spatial correlation between paired peaks across imaging pixels. This skill distinguishes true molecular adducts from spurious mass differences and illuminates metabolites that form abundant salt or matrix adducts.

## When to use

When you have binned mass spectrometry imaging peaks and want to understand which detected mass-to-charge ratios represent the same metabolite in different ionization states (parent vs. adduct form). Apply this skill when adduct formation is suspected to obscure metabolite identity—particularly in MALDI-MSI where matrix ions (e.g., DHB, CHCA) and sample salts (Na⁺, K⁺) readily form adducts with metabolites. Use it to recover 'dark metabolome' peaks that would otherwise be missed because they appear as distinct m/z values rather than as a single peak.

## When NOT to use

- When your data has not been peak-binned or m/z values have not been preprocessed (e.g., raw profile mode spectra where each spectrum is a separate array); massdiff() requires a peak list or binned matrix.
- When you have no spatial information (non-imaging MS data, or single-pixel/bulk spectra); corrPairsMSI() requires pixel-level intensity variation to compute meaningful correlations and cannot validate adducts on 1-D spectral data.
- When your mass difference histogram shows no enrichment at known adduct masses (e.g., flat distribution with no peaks >2–3× background); adductMatch() will report matches but with very low counts and high quantiles, indicating unreliable adduct assignment in that dataset.

## Inputs

- msimat object (preprocessed MSI data matrix with m/z values and pixel-wise intensities)
- massdiff object (output from massdiff() function listing all pairwise m/z differences)
- massdiffhist object (binned histogram of mass differences with user-specified bin width)

## Outputs

- data.frame of adductMatch() results (known adducts ranked by bin count and quantile)
- massdiff subset from diffGetPeaks() (parent and adduct m/z pairs within specified tolerance)
- correlation test result table from corrPairsMSI() (Pearson r, p-values, and significance status for each ion pair)
- annotated mass spectrum plot (optional, from pointsAdducts() showing parent ions in one color and adduct ions in contrasting color)

## How to apply

First, compute all pairwise mass differences from detected peaks using `massdiff()`, then bin them into a histogram with instrument-appropriate precision (typically 0.01 Da bin width). Next, match mass difference bins to a reference library of known adducts (built-in `adducts` or `adducts2` datasets) using `adductMatch()` to identify candidate parent–adduct pairs. For each candidate pair, extract the actual m/z values using `diffGetPeaks()` with a user-specified mass window (e.g., ±0.5 mDa or ppm tolerance). Finally, test spatial correlation between the intensity profiles of paired peaks across all imaging pixels using `corrPairsMSI()` with default two-tailed Pearson correlation and Bonferroni-corrected significance threshold (p < 0.05). Pairs showing both mass-difference match AND significant spatial correlation (high Pearson r, low corrected p-value) are validated parent–adduct relationships; reject pairs with poor spatial correlation, as they indicate coincidental mass differences rather than chemical associations.

## Related tools

- **mass2adduct** (R package providing massdiff(), adductMatch(), diffGetPeaks(), corrPairsMSI(), and pointsAdducts() functions for the full parent–adduct pairing and validation workflow) — https://github.com/kbseah/mass2adduct
- **Cardinal** (R package for MSI data preprocessing and peak binning; MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to mass2adduct's msimat format via cardinal2msimat()) — http://cardinalmsi.org/
- **SCiLS** (Commercial MSI software that exports peak intensity data as plain-text CSV files; output can be imported into msimat() for mass2adduct analysis)
- **MSiReader** (Open-source MSI software that exports peak intensity data as plain-text CSV files; output can be imported into msimat() for mass2adduct analysis)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); d.diff.annot <- adductMatch(d.diff.hist); d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); pointsAdducts(d, subset(d.diff.annot.cor, matches=='Na adduct'), which='adduct', signif=TRUE, pch=20, col='red')
```

## Evaluation signals

- adductMatch() output shows multiple known adducts with counts ≥3–5× the background count level and quantiles <0.95, indicating enrichment of true adduct mass differences above random noise.
- corrPairsMSI() returns Pearson correlation coefficients >0.5–0.7 with Bonferroni-corrected p-values <0.05 for validated parent–adduct pairs, confirming that paired ions co-vary spatially across pixels (evidence of shared metabolite origin).
- pointsAdducts() scatter plot shows minimal to no overlap between red (adduct) and blue (parent) point clouds for non-parent–adduct pairs, but clear spatial clustering for validated pairs, visually confirming the pairing.
- Subset of massdiff object returned by diffGetPeaks() with specified mass tolerance contains balanced numbers of parent and adduct peaks (approximately 1:1 ratio for true pairs), not orphaned single peaks.
- Cross-check: validated parent–adduct pairs match expected adduct formulas (e.g., [M+Na]⁺, [M+K]⁺, [M+matrix-H]⁺) based on known sample composition and instrument settings (positive vs. negative mode, matrix type).

## Limitations

- Spatial correlation testing (corrPairsMSI) is computationally expensive for datasets with hundreds or thousands of peaks; for large datasets, the alternative function corrPairsMSIchunks must be used to avoid memory exhaustion, processing pairs in serial chunks.
- The reference adduct library (built-in `adducts` and `adducts2` datasets) includes only common biological adducts and matrix ions; rare or unexpected adducts will not be matched and may be missed unless a custom adduct table is supplied.
- Histogram binning width is user-specified and depends on instrument mass accuracy; choosing an inappropriate bin width (too narrow or too wide) can cause true adducts to be split across bins or merged with spurious differences, leading to false negatives or false positives in adductMatch().
- The method assumes pixels with correlated ion pairs represent the same metabolite; confounding spatial correlation (e.g., two unrelated metabolites that happen to co-localize) can produce false-positive parent–adduct assignments if correlation alone is used without complementary validation (e.g., MS/MS, chemical standards).
- CSV export and import workflows (from SCiLS, MSiReader, or other third-party software) can introduce precision loss or format inconsistencies; large CSV files (several GB) may exceed available RAM during import and require Perl-based format conversion (msimunging.pl) before use.

## Evidence

- [methods] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above."
- [readme] Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function). Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function).: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [readme] If they are truly related by molecular adduct formation, then their abundances should be correlated. These putative pairs are found with the `diffGetPeaks` function (above).: "If they are truly related by molecular adduct formation, then their abundances should be correlated."
- [readme] Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction.: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [intro] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [readme] For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function `corrPairsMSIchunks` instead of `corrPairsMSI`.: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially."
