---
name: mass-spectrometry-peak-pair-analysis
description: Use when you have preprocessed MSI data (as a CSV intensity matrix or Cardinal MSProcessedImagingExperiment object) and suspect that observed peaks include both parent ions and their adducts formed with matrix or salt species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mass2adduct
  - R
  - Cardinal
  - SCiLS
  - MSiReader
  - R (devtools, knitr, rmarkdown, pandoc)
  techniques:
  - MS-imaging
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-pair-analysis

## Summary

Identify and rank molecular adducts in mass spectrometry imaging by computing pairwise mass differences between all detected peaks, binning them into a histogram, and matching observed differences to known chemical species. This skill reveals adduct formation between target metabolites and matrix or salt ions, illuminating signals otherwise missed in standard peak annotation.

## When to use

Apply this skill when you have preprocessed MSI data (as a CSV intensity matrix or Cardinal MSProcessedImagingExperiment object) and suspect that observed peaks include both parent ions and their adducts formed with matrix or salt species. Use it to disambiguate the 'dark metabolome' of unexplained peaks in MALDI-MSI datasets and to validate putative adduct pairs using spatial correlation in imaging pixels.

## When NOT to use

- Input is unbinned, un-preprocessed raw instrument data (MS1 profiles)—preprocess and peak-bin first using Cardinal or comparable software.
- You are analyzing targeted metabolomics with a small, validated list of compounds—adduct detection is most valuable for discovery-mode untargeted MSI.
- Spatial information from imaging pixels is not available or is irrelevant to your biological question—correlation testing requires pixel-level intensity maps.

## Inputs

- msimat object (preprocessed MSI intensity matrix from CSV or Cardinal)
- massdiff object (pairwise mass differences between all peak pairs)
- mass difference histogram (binned massdiff with user-specified bin width)

## Outputs

- adductMatch result (counts and quantiles of known adducts)
- topAdducts ranking (mass differences ranked by occurrence with adduct annotations)
- corrPairsMSI result (p-values and correlation coefficients for spatial correlation of ion pairs)

## How to apply

First, load your preprocessed MSI intensity data as an msimat object (from CSV with delimiters like ';' or from Cardinal using cardinal2msimat()). Compute all pairwise mass differences using massdiff() to generate a data.frame with parent ion (A), adduct ion (B), and mass difference (diff) columns. Bin the resulting differences into a histogram using hist() with a bin width matched to your instrument's mass precision (e.g., 0.01 Da for Orbitrap-class instruments). Apply adductMatch() against the built-in adducts or adducts2 reference dataset to count occurrences and report quantile values for known chemical transformations. Use topAdducts() to rank mass differences by frequency and identify the highest-abundance unidentified differences. Finally, for confirmed adduct pairs, apply corrPairsMSI() or corrPairsMSIchunks() to test spatial correlation (Pearson, p < 0.05 with Bonferroni correction) between parent and derivative ion abundances across imaging pixels—true adducts will show significant co-localization.

## Related tools

- **mass2adduct** (Core package implementing massdiff(), adductMatch(), topAdducts(), corrPairsMSI(), corrPairsMSIchunks(), msimat(), and diffGetPeaks() functions for adduct detection, matching, and spatial validation) — https://github.com/kbseah/mass2adduct
- **Cardinal** (Preprocessing and peak-binning of raw MSI data before import into mass2adduct; MSProcessedImagingExperiment objects are converted to msimat format via cardinal2msimat()) — http://cardinalmsi.org/
- **SCiLS** (MSI data acquisition and export to plain-text CSV format compatible with msimat() import)
- **MSiReader** (MSI data acquisition and intensity export to CSV format for import into mass2adduct)
- **R (devtools, knitr, rmarkdown, pandoc)** (Execution environment; devtools used for installation from GitHub; knitr and rmarkdown required to build vignette documentation) — https://cran.r-project.org/

## Examples

```
d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); head(adductMatch(d.diff.hist)); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Histogram of mass differences exhibits peaks at known adduct mass values (e.g., 18.01 Da for [M+H2O], 136.016 Da for [M+DHB-H2O]); quantile values for matches are well-separated from baseline noise.
- topAdducts() output shows consistent ranking: highest-count mass differences align with biologically plausible adducts in the reference list (adducts or adducts2 dataset).
- corrPairsMSI() results show p-values < 0.05 (after Bonferroni correction) for putative parent–adduct pairs, indicating significant spatial co-localization in imaging pixels; unrelated peak pairs show p > 0.05.
- Pairwise differences that pass spatial correlation threshold reproduce known matrix or salt adducts (e.g., sodium [Na+], potassium [K+], ammonium [NH4+]) at expected molecular mass shifts.
- Filtered massdiff object (output of adductMatch() applied directly to massdiff) contains only pairs with validated adduct matches; no spurious mass differences remain in the output.

## Limitations

- Mass precision and bin width are critical: if instrument precision is unknown or bin width is misspecified (e.g., too wide for high-resolution data, too narrow for low-resolution data), adducts may be merged or split incorrectly, leading to missed or false matches.
- The built-in adducts and adducts2 datasets are static and biologically curated; users must supply custom adduct reference lists if analyzing non-biological samples or atypical ionization conditions.
- Spatial correlation testing (corrPairsMSI) requires pixel-level intensity maps and assumes adequate spatial sampling; datasets with very few pixels or extreme spatial heterogeneity may yield unstable correlation estimates.
- For very large MSI datasets (hundreds or thousands of peaks), corrPairsMSI() may exhaust RAM; corrPairsMSIchunks() is provided but introduces serial processing overhead.
- No changelog is provided in the repository, limiting version-specific troubleshooting or reproducibility across installation dates.

## Evidence

- [intro] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [methods] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument."
- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks have that mass difference) and the quantile.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts and the quantile."
- [readme] topAdducts` ranks mass differences by the number of times they are observed, and report any matches to known adducts.: "`topAdducts` ranks mass differences by the number of times they are observed, and report any matches to known adducts."
- [readme] Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function).: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [readme] If they are truly related by molecular adduct formation, then their abundances should be correlated.: "If they are truly related by molecular adduct formation, then their abundances should be correlated."
- [readme] By default the cutoff for significance is p=0.05 with Bonferroni correction.: "By default the cutoff for significance is p=0.05 with Bonferroni correction."
