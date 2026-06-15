---
name: sodium-adduct-detection-and-classification
description: Use when analyzing MALDI-mass spectrometry imaging data in which sodium or other alkali metal contamination is suspected, or when peak lists show unexplained mass differences in the range of ~20–25 Da (characteristic of Na adducts).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
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

# Sodium-Adduct Detection and Classification

## Summary

Identify and visually distinguish sodium adduct ions ([M+Na]+) from their parent metabolite ions in MALDI-MSI data by matching observed mass differences to known sodium adduct masses, then spatially correlating parent–adduct pairs to filter out false positives. This skill enables interrogation of the 'dark metabolome'—metabolites hidden as salt adducts in imaging datasets.

## When to use

Apply this skill when analyzing MALDI-mass spectrometry imaging data in which sodium or other alkali metal contamination is suspected, or when peak lists show unexplained mass differences in the range of ~20–25 Da (characteristic of Na adducts). The skill is most valuable when you have preprocessed MSI data with pixel-level intensities and want to recover metabolite identities obscured by adduct formation, particularly in imaging experiments where spatial colocalization can validate ion relationships.

## When NOT to use

- When MSI data lacks pixel-level intensity values or spatial coordinates; spatial correlation testing requires full imaging data, not summary mass lists.
- When your instrument's mass accuracy is substantially worse (lower ppm resolution) than the expected mass difference windows (e.g., ±0.5 mDa for Na adducts); histogramming will conflate distinct masses and adduct identification becomes unreliable.
- When the target ions are already known to NOT form adducts (e.g., already-desorbed cations or fragment ions with fixed charge); the workflow assumes neutral parent molecules capable of adducting.

## Inputs

- msimat object: preprocessed MSI data matrix with m/z values and pixel-level intensities
- massdiff object: pairwise mass differences computed from detected peaks
- massdiff histogram object: binned mass differences with user-defined bin width (e.g., 0.01 Da)
- adducts reference data frame: built-in 'adducts' or 'adducts2' datasets or user-supplied custom adduct list with columns 'name', 'formula', 'mass'

## Outputs

- Annotated massdiff object with adductMatch() results indicating which mass differences correspond to sodium adducts
- Spatially validated massdiff object after corrPairsMSI() filtering, containing only parent–adduct pairs with significant spatial correlation (p < 0.05 Bonferroni-corrected)
- Mass spectrum visualization plot with overlaid parent ions (blue circle outlines) and sodium adduct ions (red filled points) showing colocalization

## How to apply

First, compute all pairwise mass differences between detected m/z peaks using massdiff(), then bin them into a histogram (hist()) with a bin width matching your instrument's mass accuracy (e.g., 0.01 Da for high-resolution instruments). Use adductMatch() to search for known sodium adduct mass differences (typically +22.989 Da for [M+Na]+) in the histogram. For candidates matching Na adducts, extract the parent–adduct ion pairs using diffGetPeaks() or subset() operations. Critically, test spatial correlation between each parent and proposed adduct ion across all pixels using corrPairsMSI() with a significance threshold (default p < 0.05 with Bonferroni correction); this exploits MSI's spatial information to confirm that parent and adduct truly colocalize, reducing false-positive adduct assignments. Finally, visualize confirmed pairs on the mass spectrum using pointsAdducts() with which='adduct' (red points) and which='parent' (blue circles) to show overlap patterns.

## Related tools

- **mass2adduct** (Core R package providing massdiff(), hist(), adductMatch(), topAdducts(), diffGetPeaks(), corrPairsMSI(), corrPairsMSIchunks(), and pointsAdducts() functions for detecting and visualizing adducts in MSI data.) — https://github.com/kbseah/mass2adduct
- **Cardinal** (R package for preprocessing and peak-binning MSI data; MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to mass2adduct's msimat format via cardinal2msimat().) — http://cardinalmsi.org/
- **SCiLS** (Commercial MSI software; intensity data exported as CSV files can be imported into mass2adduct via msimat().)
- **MSiReader** (Open-source MSI software; intensity data exported as CSV files can be imported into mass2adduct via msimat().)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); d.diff.annot <- adductMatch(d.diff.hist); d.diff.annot.cor <- corrPairsMSI(d, subset(d.diff.annot, matches=='Na adduct')); pointsAdducts(d, d.diff.annot.cor, which='adduct', signif=TRUE, pch=20, cex=0.5, col='red')
```

## Evaluation signals

- The histogram of mass differences shows a distinct peak at +22.989 Da (or close match within bin width) with non-zero counts; topAdducts() ranks this mass difference in the top 10–20 hits by frequency.
- adductMatch() successfully assigns parent–adduct candidate pairs; the number of candidates is biologically reasonable (e.g., not implausibly high or zero if sodium contamination is expected).
- After corrPairsMSI(), the Pearson or Spearman correlation p-values for validated parent–adduct pairs are < 0.05 with Bonferroni correction; the fraction of initial candidates passing spatial validation is consistent with expected biology (typically >50% for true adducts in contaminated samples).
- pointsAdducts() visualization shows substantial spatial overlap between red (adduct) and blue (parent) point clusters across multiple imaging coordinates, rather than randomly scattered or segregated points.
- Manual spot-checking of raw MSI data at coordinates flagged as co-localizing parent–adduct pairs confirms visual colocalization in the raw ion images.

## Limitations

- The method relies on spatial correlation testing; samples with low pixel counts, high noise, or poor spatial resolution may yield unreliable correlations. Chunks of pixels with identical intensity patterns will appear correlated even if unrelated.
- Mass accuracy and histogram binning are critical; if bin width is too narrow, true adduct peaks will be split across bins; if too wide, distinct mass differences will merge. The user must set bin width appropriately for their instrument.
- For very large datasets (hundreds to thousands of peaks), corrPairsMSI() may exhaust system memory; the workaround is to use corrPairsMSIchunks() to process serially, but this is slower.
- The built-in 'adducts' and 'adducts2' reference datasets contain only common, biologically relevant adducts; unexpected or non-standard adducts (e.g., rare salt or contaminant combinations) will not be detected unless a custom reference is provided.
- The skill assumes adducts form via simple mass addition (e.g., [M+Na]+); it cannot detect or distinguish complex adducts, dimers, or other non-additive modifications.

## Evidence

- [intro] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [methods] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [methods] Match mass differences to known adducts by finding the closest-matching bin in the mass difference histogram.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram"
- [methods] Test if each ion pair is actually spatially correlated in the sample by exploiting the spatial information contained in the MSI data.: "Now that we have a list of annotated massdiffs, we want to exploit the spatial information contained in the MSI data to test if each ion pair is actually spatially correlated in the sample."
- [methods] Annotate the original mass spectrum to mark peaks corresponding to parent ions and adduct ions in different colors.: "You can annotate the original mass spectrum using a massdiff object, to mark peaks corresponding to parent ions and adduct ions in different colors."
- [other] pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of overlap patterns.: "The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern"
- [readme] For even larger datasets, use corrPairsMSIchunks() instead of corrPairsMSI() to avoid memory exhaustion.: "For even larger datasets (e.g. hundreds or thousands of peaks), you might run out of memory and crash. To avoid this, use `corrPairsMSIchunks` instead of `corrPairsMSI`"
- [readme] Built-in datasets 'adducts' and 'adducts2' list biologically-relevant chemical species that might occur in biological samples.: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples."
