---
name: mass-spectrum-histogram-interpretation
description: Use when after computing all pairwise mass differences from a mass spectrometry
  imaging dataset, when you need to identify which mass differences correspond to
  real molecular adducts (e.g., metabolite–matrix or metabolite–salt ions) rather
  than noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - SCiLS or MSiReader
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

# Mass-Spectrum Histogram Interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Bin calculated mass differences into a histogram with instrument-appropriate precision, then visually and statistically identify peaks representing abundant molecular adducts. This technique transforms raw pairwise mass differences into actionable annotations by matching histogram bins to known chemical transformations.

## When to use

After computing all pairwise mass differences from a mass spectrometry imaging dataset, when you need to identify which mass differences correspond to real molecular adducts (e.g., metabolite–matrix or metabolite–salt ions) rather than noise. Use this skill when the number of unique mass difference values is large and measurement uncertainty makes individual differences unreliable for matching to known adducts.

## When NOT to use

- Do not use if you have only a few peaks or very low mass resolution; histogram binning requires sufficient pairwise differences to form meaningful peaks.
- Do not use if your mass differences are already annotated or if you only need to identify a single known adduct; use diffGetPeaks() directly instead.
- Do not use if measurement error is unknown or unmeasurable; you cannot set an appropriate bin width without understanding instrument precision.

## Inputs

- massdiff object (data.frame with three columns: parent ion mass A, adduct ion mass B, mass difference diff)
- bin width parameter (numeric, instrument-dependent; e.g., 0.01 for typical MALDI instruments)
- reference adduct dataset (data.frame with columns name, formula, mass; built-in adducts or adducts2, or user-supplied)

## Outputs

- massdiffhist object (standard R histogram object with counts per bin)
- adductMatch result (data.frame with matched adduct names, formulas, masses, counts, and quantile values)
- topAdducts ranking (data.frame with top n mass differences ranked by count, with adduct matches if available)
- histogram plot (visual representation of mass difference distribution)

## How to apply

First, create a histogram of all pairwise mass differences using a bin width that reflects your instrument's known mass precision (e.g., 0.01 for high-resolution instruments; the README recommends this as a starting point). The histogram bundles measured differences that fall within measurement error, normalizing away misleading false precision. Next, apply adductMatch() to the histogram to count occurrences of bins matching known adducts from the built-in adducts or adducts2 reference datasets, reporting both raw counts and quantile values to gauge abundance. Then use topAdducts() to rank all histogram bins by occurrence frequency in descending order and identify matches to known adducts in the highest-abundance bins. Use the visual histogram plot to spot unexpected peaks or bimodal distributions that might indicate instrument calibration issues or unsuspected chemical transformations. Finally, evaluate whether the top-ranked mass differences make biological sense given your sample composition (e.g., common matrices like DHB should produce expected adducts).

## Related tools

- **mass2adduct** (Provides hist() method for massdiff objects, adductMatch() for bin-to-adduct matching, and topAdducts() for ranking; also supplies built-in adducts and adducts2 reference datasets.) — https://github.com/kbseah/mass2adduct
- **R** (Host language; hist() is base R function, used alongside mass2adduct package functions.)
- **SCiLS or MSiReader** (Upstream MSI data export software; data must be exported as CSV before import to mass2adduct.)
- **Cardinal** (Alternative upstream MSI processing software; MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to msimat format for mass2adduct.) — http://cardinalmsi.org/

## Examples

```
d.diff.hist <- hist(d.diff); adductMatch(d.diff.hist); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Histogram shows distinct, narrow peaks (not broad or flat distribution), indicating genuine mass differences stand out from noise.
- Top-ranked mass differences match known adducts (e.g., DHB-H2O at 136.01600, or common salt/matrix ions) in the reference dataset with high counts and low quantile values.
- Visual inspection of histogram reveals expected peaks for your known sample composition (e.g., if DHB matrix is used, should see DHB-related peaks).
- Quantile values for matched adducts are substantially lower than those of unmatched bins, confirming adduct matches are enriched in the tail of the distribution.
- topAdducts() output shows graceful decrease in counts with rank; absence of a few dominant peaks followed by many singletons suggests good separation of true adducts from noise.

## Limitations

- Bin width choice directly affects sensitivity and specificity; too narrow and bins fragment into noise, too wide and distinct adducts merge. The README recommends 0.01 as a starting point but does not provide data-driven guidance for all instruments.
- Reference adduct datasets (adducts, adducts2) are curated for biological relevance but may omit instrument-specific or non-biological adducts; custom adduct lists can be supplied but require manual curation.
- Histogram peak height alone does not prove adducts are real or spatially correlated; follow-up with corrPairsMSI() or corrPairsMSIchunks() to test spatial co-localization of parent and adduct ions in MSI pixels.
- Large datasets (hundreds or thousands of peaks) may cause memory issues during pairwise difference calculation; reformatting to triplet format with msimunging.pl Perl script is recommended but adds a preprocessing step.
- Quantile values are typically very high because most mass differences have zero counts; the quantile alone is not a reliable measure of adduct significance without comparison to the full distribution.

## Evidence

- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks have that mass difference) and the quantile.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks"
- [readme] `topAdducts` ranks mass differences by the number of times they are observed, and report any matches to known adducts: "`topAdducts` ranks mass differences by the number of times they are observed, and report any matches to known adducts"
- [other] Create a mass difference histogram using hist() on the massdiff object to identify peaks representing common chemical transformations.: "Create a mass difference histogram using hist() on the massdiff object to identify peaks representing common chemical transformations."
- [intro] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
