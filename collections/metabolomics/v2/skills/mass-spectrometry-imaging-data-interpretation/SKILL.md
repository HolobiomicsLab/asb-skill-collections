---
name: mass-spectrometry-imaging-data-interpretation
description: Use when when you have preprocessed MALDI-MSI data (in msimat format)
  and want to determine whether abundant peaks are actually molecular adducts of simpler
  parent ions rather than distinct metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mass2adduct
  - R
  - Cardinal
  - SCiLS
  - MSiReader
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-imaging-data-interpretation

## Summary

A workflow for identifying and visualizing sodium adduct ions relative to their parent ions in MALDI-MSI data by computing pairwise mass differences, matching them to known adducts, testing spatial correlation, and overlaying adduct and parent peaks on mass spectra with color-coded scatter plots. This skill reveals ion relationships that would otherwise remain hidden in the 'dark metabolome'.

## When to use

When you have preprocessed MALDI-MSI data (in msimat format) and want to determine whether abundant peaks are actually molecular adducts of simpler parent ions rather than distinct metabolites. Apply this skill when visual inspection alone cannot distinguish overlapping adduct and parent peaks, or when you need to filter false positive identifications by leveraging spatial co-localization patterns across pixels.

## When NOT to use

- If you have not yet preprocessed your raw MSI data (still in imzML or vendor-proprietary format) — first run Cardinal peakBin() or equivalent binning before importing as msimat.
- If your instrument's mass precision or typical measurement error is unknown — you cannot set an appropriate histogram bin width, risking false positives or missed matches.
- If you are studying a single-pixel or very low-pixel-count dataset — spatial correlation testing requires sufficient variance across pixels to compute meaningful p-values.

## Inputs

- msimat object (preprocessed MSI data matrix with pixel coordinates and intensities)
- massdiff object (table of all pairwise mass differences and parent mass pairs)
- massdiff object annotated with adductMatch() results (matches to known adducts)
- massdiff object correlation-tested with corrPairsMSI() or corrPairsMSIchunks() (p-values per pair)

## Outputs

- scatter plot overlay of adduct ions (red, filled pch=20) and parent ions (blue, open pch=1)
- visual identification of red/blue overlap regions indicating spatially correlated ion pairs
- mass spectrum annotation with significant adduct-parent relationships marked
- filtered massdiff object containing only significant (p < 0.05) pairs

## How to apply

Begin by computing all pairwise mass differences from your MSI peak list using massdiff(), then bin the differences into a histogram with a bin width matching your instrument's mass precision (e.g., 0.01 m/z for high-resolution MS). Match histogram bins to known adducts (e.g., sodium, potassium, matrix-related species) using adductMatch(); if matches are weak, rank mass differences by frequency with topAdducts(). For each putative adduct-parent pair, test whether their pixel-wise intensities are spatially correlated using corrPairsMSI() or corrPairsMSIchunks() (for large datasets), applying a significance threshold (default p < 0.05 with Bonferroni correction). Finally, overlay the correlation-validated adduct and parent peaks on your mass spectrum using pointsAdducts() with which='adduct' (red, filled circles) and which='parent' (blue, open circles), restricting to signif=TRUE to show only statistically supported pairs. Red-blue overlap confirms ions sharing a spatial distribution characteristic of true adduct formation.

## Related tools

- **mass2adduct** (Provides the complete toolkit: msimat() for data import, massdiff() for pairwise difference computation, adductMatch() and topAdducts() for adduct identification, corrPairsMSI()/corrPairsMSIchunks() for spatial correlation testing, and pointsAdducts() for visualization overlay.) — https://github.com/kbseah/mass2adduct
- **R** (Host language for mass2adduct package; required for all functions and plot generation.)
- **Cardinal** (Optional upstream tool for MSI data preprocessing and peak binning; outputs can be converted to msimat format via cardinal2msimat().) — http://cardinalmsi.org/
- **SCiLS** (Alternative upstream MSI acquisition/export software; CSV output files can be imported directly into msimat().)
- **MSiReader** (Alternative upstream MSI acquisition/export software; CSV output files can be imported directly into msimat().)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); d.diff.annot <- adductMatch(d.diff.hist); d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); pointsAdducts(d, subset(d.diff.annot.cor, matches=='Na adduct'), which='adduct', signif=TRUE, pch=20, cex=0.5, col='red'); pointsAdducts(d, subset(d.diff.annot.cor, matches=='Na adduct'), which='parent', signif=TRUE, pch=1, cex=0.5, col='blue')
```

## Evaluation signals

- Histogram of mass differences shows clear peaks at known adduct mass windows (e.g., Na+ = 22.99 m/z); comparison to built-in adducts or adducts2 dataset confirms expected species.
- adductMatch() or topAdducts() reports high-frequency mass differences with statistically significant matches to chemical species relevant to your sample matrix.
- corrPairsMSI() returns p-values < 0.05 (after Bonferroni correction) for putative adduct-parent pairs, indicating pixel-wise intensity correlation supports the adduct hypothesis.
- pointsAdducts() scatter plot shows visually distinct red (adduct) and blue (parent) point clusters with substantial spatial overlap, confirming co-localization; absence of overlap suggests pairs are false positives.
- Subset of correlation-validated pairs aligns with independent metabolite identity (if available from MS/MS or other orthogonal methods), validating the adduct assignments.

## Limitations

- Spatial correlation testing assumes sufficient pixel coverage and intensity variance; very sparse or homogeneous datasets may yield uninformative p-values.
- Bin width selection for mass difference histogram is user-dependent and critical: too narrow gives noise, too wide loses resolution. No automated method is provided; instrument calibration and mass accuracy documentation are required.
- The built-in adducts and adducts2 reference datasets cover common biological matrix and salt adducts; rare or unexpected adduct species will not be detected without manual reference dataset extension.
- Computational memory scales quadratically with peak count (all pairwise comparisons); corrPairsMSI() may fail on datasets with >1000 peaks; corrPairsMSIchunks() mitigates but is slower.
- Visual overlap in pointsAdducts() scatter plots can be ambiguous in high-density regions; numeric p-values and signif=TRUE filtering are essential to distinguish true spatial correlation from chance overlap.

## Evidence

- [readme] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [readme] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above."
- [readme] Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function).: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [other] The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between sodium adducts and their corresponding parent ions.: "The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between"
