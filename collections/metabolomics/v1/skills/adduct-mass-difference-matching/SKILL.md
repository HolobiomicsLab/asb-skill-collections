---
name: adduct-mass-difference-matching
description: Use when you have computed a histogram of pairwise mass differences from MS imaging data and need to (1) identify which observed mass differences correspond to biologically relevant or chemically known adducts, or (2) rank the most frequently observed mass differences to discover dominant adduct.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct
schema_version: 0.2.0
---

# adduct-mass-difference-matching

## Summary

This skill matches observed mass differences from MS imaging data against a reference database of known molecular adducts (such as matrix or salt ions) to identify and rank abundant adduct species. It is applied after computing pairwise mass differences between all detected peaks and binning them into a histogram, using the mass2adduct package's adductMatch() and topAdducts() functions.

## When to use

Apply this skill when you have computed a histogram of pairwise mass differences from MS imaging data and need to (1) identify which observed mass differences correspond to biologically relevant or chemically known adducts, or (2) rank the most frequently observed mass differences to discover dominant adduct species in your sample. This is typical after baseline-corrected, peak-binned MSI data has been loaded and massdiff() has been applied.

## When NOT to use

- Do not use if you have not yet computed pairwise mass differences or created a binned histogram; adductMatch() requires a massdiffhist object as input.
- Do not use if your mass differences have already been validated by spatial correlation testing and you only wish to visualize or further filter results; this skill is diagnostic, not confirmatory.
- Do not use if your reference adduct list is incomplete or does not contain adducts relevant to your experimental context (e.g., matrix ions, salt ions, or metabolite modifications specific to your sample).

## Inputs

- massdiff object (data.frame with columns: A [parent ion mass], B [adduct ion mass], diff [mass difference])
- massdiffhist object (histogram of mass differences with counts per bin)
- reference adduct table (data.frame with columns: name, formula, mass; built-in options: adducts or adducts2)

## Outputs

- annotated adduct matches (data.frame with matched adduct names, formulas, masses, bin counts, and quantiles)
- ranked adduct list (data.frame from topAdducts() with top n mass differences ranked by occurrence and adduct annotations)

## How to apply

Load or construct a mass difference histogram object (massdiffhist class) from your preprocessed MSI data using hist(massdiff_object). Then apply adductMatch() with the built-in reference adduct database (adducts or adducts2) to find matches between histogram bins and known chemical species; adductMatch() reports counts and quantile values for each match, indicating how frequently each adduct mass difference appears. Optionally, apply topAdducts() to rank mass differences by occurrence in descending order and display the top n peaks with any adduct matches. The choice between adducts and adducts2 depends on whether you want a comprehensive or shorter list of biologically-relevant chemical species. Matches are made by finding the closest-matching bin in the histogram, so bin width (set during hist() via the binwidth parameter, typically 0.01 for instruments with ~10 ppm mass precision) critically affects specificity.

## Related tools

- **mass2adduct** (R package providing adductMatch() and topAdducts() functions for matching histogram mass differences to known adducts) — https://github.com/kbseah/mass2adduct
- **R** (Computing environment for loading, executing mass2adduct functions, and analyzing results)
- **Cardinal** (Optional upstream tool for preprocessing and peak-binning MSI data before conversion to msimat format for mass2adduct)

## Examples

```
d.diff.hist <- hist(massdiff(d), binwidth=0.01); head(adductMatch(d.diff.hist)); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- adductMatch() output contains quantile values (typically high, >0.9) reflecting that most mass differences have zero to few counts; absence of quantile column indicates failed matching.
- topAdducts() ranked list is in strict descending order by occurrence count; if not, check histogram binning and reference adduct table integrity.
- Matched adducts have chemically plausible mass differences relative to known matrix ions (e.g., DHB at ~154.06 m/z for positive MALDI) or common salt ions (e.g., Na+ at +22.99, K+ at +38.96); implausible matches indicate reference table errors.
- Histogram bin width and mass precision of the instrument are consistent (e.g., 0.01 Da for ~10 ppm instruments); mismatch causes false negatives or spurious matches.
- Sample size of counts per bin matches the number of unique ion pairs in the massdiff object; zero or unexpected count distributions suggest histogram construction error.

## Limitations

- adductMatch() relies on closest-matching bin in the histogram, so resolution and accuracy depend critically on bin width selection and instrument mass accuracy; misspecification can lead to false positives or missed adducts.
- The built-in adducts and adducts2 reference databases are curated for biologically-relevant species and may not include all possible chemical adducts; custom adduct tables must be manually created and validated.
- Mass difference matching alone does not confirm adduct identity; spatial correlation testing via corrPairsMSI() or corrPairsMSIchunks() is recommended to verify that putative parent and adduct ions are genuinely colocalized in the sample.
- Large datasets (hundreds or thousands of peaks) may require chunked processing; adductMatch() processes the entire histogram at once and does not offer memory-efficient alternatives for extremely large inputs.
- Quantile reporting in adductMatch() output can be misleading because it reflects the rank of that adduct mass difference relative to all observed differences, not statistical significance; high quantiles do not guarantee biological relevance.

## Evidence

- [other] The mass2adduct package implements a pipeline that computes mass difference objects, builds histograms of those differences, matches them to known adducts using adductMatch(), and ranks results with topAdducts() to identify the most abundant adducts.: "adductMatch() to the histogram with the built-in adducts or adducts2 reference dataset to match observed mass differences to known chemical species, reporting counts and quantile values"
- [readme] adductMatch() function behavior and match reporting mechanism: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks"
- [readme] topAdducts() function ranks and reports top mass differences with adduct matches: "topAdducts performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts."
- [readme] Built-in reference adduct datasets curated for biological relevance: "The package comes with a small data set of common molecular adducts, called `adducts` (use the command `help(adducts)` to see a description). Users can supply their own custom sets of adducts as long"
- [methods] Rationale for spatial validation after mass matching: "Now that we have a list of annotated massdiffs, we want to exploit the spatial information contained in the MSI data to test if each ion pair is actually spatially correlated in the sample."
- [readme] Bin width selection and instrument precision context: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
