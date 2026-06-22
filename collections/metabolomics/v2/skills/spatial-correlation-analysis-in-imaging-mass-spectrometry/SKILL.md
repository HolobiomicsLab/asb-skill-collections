---
name: spatial-correlation-analysis-in-imaging-mass-spectrometry
description: Use when after annotating ion pairs with known adducts (using adductMatch or diffGetPeaks), use this skill to filter suspected adduct pairs by testing if their pixel-level intensity profiles are significantly correlated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3173
  tools:
  - mass2adduct
  - R
  - corrPairsMSI
  - corrPairsMSIchunks
  - msimat
  - adductMatch
  - diffGetPeaks
  - mass2adduct (R package)
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

# spatial-correlation-analysis-in-imaging-mass-spectrometry

## Summary

Test whether annotated ion pairs in mass spectrometry imaging data exhibit significant spatial covariance by computing two-tailed Pearson correlation coefficients across pixel intensities. This validates whether suspected parent–adduct relationships are supported by correlated abundance patterns in the tissue sample.

## When to use

After annotating ion pairs with known adducts (using adductMatch or diffGetPeaks), use this skill to filter suspected adduct pairs by testing if their pixel-level intensity profiles are significantly correlated. This is essential because mass difference alone is not sufficient evidence of true chemical relationships; spatial correlation in imaging data provides orthogonal validation that two peaks co-localize and co-vary in abundance.

## When NOT to use

- Input massdiff contains unannotated pairs without adduct matches; spatial correlation is most useful after enriching the candidate set with chemical knowledge.
- MSI data lacks pixel-level spatial structure or contains only bulk/averaged spectra rather than per-pixel intensities; correlation analysis requires variance across sampling locations.
- Dataset is too small (very few pixels or peaks) to support robust correlation estimation and multiple-testing correction.

## Inputs

- msimat object (pixel × mass intensity matrix)
- massdiff object with annotated ion pairs (data.frame with columns A, B, and adduct annotations)

## Outputs

- massdiff object augmented with columns: Estimate (Pearson r), P.value (raw), Significance (boolean, Bonferroni-corrected)

## How to apply

Load the original msimat object (the full MSI intensity data matrix with pixels as rows and mass peaks as columns) alongside the annotated massdiff object containing the ion pair candidates. Apply corrPairsMSI() to compute two-tailed Pearson correlation for each pair, which extracts the intensity vectors for both peaks from the msimat and tests spatial covariance. The function returns Estimate (correlation coefficient), raw P.value, and Bonferroni-corrected Significance (boolean, default α=0.05). For datasets with hundreds or thousands of peaks that exhaust memory, use corrPairsMSIchunks() instead to process pairs in serial batches. Filter the output to retain only pairs meeting your significance threshold (typically p<0.05 after Bonferroni correction); these represent ion pairs with statistically validated spatial correlation.

## Related tools

- **corrPairsMSI** (Primary function to compute two-tailed Pearson correlation and Bonferroni-corrected p-values for each annotated ion pair in msimat-format MSI data) — https://github.com/kbseah/mass2adduct
- **corrPairsMSIchunks** (Memory-efficient variant of corrPairsMSI for large datasets; processes pairs in serial batches to avoid exhausting RAM) — https://github.com/kbseah/mass2adduct
- **msimat** (Data structure and import function for MSI intensity matrices (pixels × masses), required input to correlation testing) — https://github.com/kbseah/mass2adduct
- **adductMatch** (Upstream function to annotate ion pairs with known adduct identities; output feeds into spatial correlation analysis) — https://github.com/kbseah/mass2adduct
- **diffGetPeaks** (Upstream function to extract ion pairs associated with a specific mass difference; alternative annotation source for correlation testing) — https://github.com/kbseah/mass2adduct
- **mass2adduct (R package)** (Complete package implementing the adduct detection and spatial validation pipeline) — https://github.com/kbseah/mass2adduct

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot)
```

## Evaluation signals

- Output massdiff object contains non-NA Estimate and P.value columns for each tested pair; no values should be missing except for pairs with insufficient variance.
- Bonferroni-corrected Significance column is boolean (TRUE/FALSE); FALSE values should predominate if no true spatial correlations exist; TRUE values indicate p < 0.05/n_pairs.
- Correlation Estimate values range between −1 and +1; positive values expected for true parent–adduct pairs (co-abundant); negative or near-zero values suggest non-specific mass differences.
- Distribution of raw P.values should be predominantly >0.05 for noise; a significant tail of low p-values (<0.05) indicates detected spatial correlations.
- Reproducibility: re-running corrPairsMSI on the same input data yields identical Estimate, P.value, and Significance columns (deterministic output).

## Limitations

- Bonferroni correction is conservative; with thousands of ion pairs, corrected significance thresholds become very stringent (p < 0.05/n_pairs), risking false negatives. Consider Benjamini–Hochberg FDR correction as an alternative if not available in the package.
- Pearson correlation assumes linear relationships; non-linear spatial covariance (e.g., threshold effects, saturation) may be missed.
- Requires per-pixel intensity values; cannot be applied to mass spectra that have been collapsed, normalized per-pixel, or pre-filtered in ways that remove intensity variance.
- Memory usage scales quadratically with peak count; corrPairsMSIchunks helps but is slower; very large datasets (thousands of peaks across millions of pixels) may still be impractical.
- Output p-values depend critically on the assumption of independent observations; if pixels are spatially autocorrelated (common in tissue imaging), effective sample size is inflated and p-values are overly optimistic.
- Correlation strength does not distinguish causal relationships; two peaks may correlate due to indirect biochemical relationships rather than direct adduct formation.

## Evidence

- [methods] This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object.: "This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object."
- [methods] Now that we have a list of annotated massdiffs, we want to exploit the spatial information contained in the MSI data to test if each ion pair is actually spatially correlated in the sample.: "Now that we have a list of annotated massdiffs, we want to exploit the spatial information contained in the MSI data to test if each ion pair is actually spatially correlated in the sample."
- [readme] Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction.: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [readme] For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function corrPairsMSIchunks instead of corrPairsMSI.: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function corrPairsMSIchunks instead of corrPairsMSI."
- [methods] The corrPairsMSI() function performs a two-tailed Pearson correlation test on each pair of peaks in the massdiff object to assess spatial correlation between parent and adduct ions.: "performs a two-tailed Pearson correlation test on each pair of peaks in the massdiff object to assess spatial correlation between parent and adduct ions"
