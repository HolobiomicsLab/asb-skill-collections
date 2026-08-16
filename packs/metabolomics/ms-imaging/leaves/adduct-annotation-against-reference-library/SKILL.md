---
name: adduct-annotation-against-reference-library
description: Use when after computing a histogram of all pairwise mass differences from an MSI dataset, use this skill when you have observed mass difference peaks that may correspond to known adducts (e.g., [M+H]+, [M+Na]+, [M−H2O]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mass2adduct
  - R
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

# adduct-annotation-against-reference-library

## Summary

Match observed mass differences from MS imaging data against a curated reference library of known chemical adducts (e.g., matrix or salt ion complexes) to identify and annotate probable molecular adduct ion pairs. This skill bridges untargeted mass difference detection with chemical interpretation by assigning biological or instrumental significance to specific pairwise mass shifts.

## When to use

After computing a histogram of all pairwise mass differences from an MSI dataset, use this skill when you have observed mass difference peaks that may correspond to known adducts (e.g., [M+H]+, [M+Na]+, [M−H2O]+). Apply it to reduce the chemical ambiguity of mass shifts and to select ion pairs for downstream spatial correlation testing or intensity covariance analysis.

## When NOT to use

- Input is a raw list of observed mass peaks without pairwise differences computed—use massdiff() first.
- Mass precision of your instrument is unknown or very poor (>0.1 Da)—matching to a reference library will be unreliable.
- You have no spatial information in your MSI data and do not need to validate ion pairs via covariance—topAdducts alone may suffice without formal annotation.

## Inputs

- massdiffhist object (binned histogram of pairwise mass differences)
- reference adduct library (data.frame with columns: name, formula, mass)

## Outputs

- annotated massdiff object (massdiff with matched adduct names and metadata)
- adductMatch results (counts and quantiles for each reference adduct)
- topAdducts ranking (observed mass differences ranked by frequency with adduct matches)

## How to apply

Load a mass difference histogram (output from binning pairwise mass differences with user-specified bin width appropriate to your instrument's mass precision) and the reference adduct library (built-in `adducts` or `adducts2` datasets, or a custom data.frame with columns `name`, `formula`, `mass`). Use the `adductMatch()` function to find the closest-matching bin in the histogram for each reference adduct mass, reporting counts and quantiles. Optionally use `topAdducts()` to rank observed mass differences by frequency and report any matches to known adducts in descending order of prevalence. The matched adducts become annotated massdiff objects that can be used to filter ion pairs for spatial correlation testing (via `corrPairsMSI()`) or peak annotation on the mass spectrum (via `pointsAdducts()`).

## Related tools

- **mass2adduct** (R package providing adductMatch(), topAdducts(), and built-in adduct reference libraries (adducts, adducts2)) — https://github.com/kbseah/mass2adduct
- **R** (Language for executing adductMatch() and topAdducts() functions)

## Examples

```
adductMatch(d.diff.hist); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Matched adduct masses are within the bin width tolerance (e.g., ±0.005 Da for 0.01 Da bin width) of observed histogram peaks.
- Quantile values reported for matched adducts reflect their frequency relative to the full distribution of mass differences; high-frequency matches should have lower quantiles.
- Annotated ion pairs passed to corrPairsMSI() show significant spatial correlation (Bonferroni-corrected p < 0.05) at higher rates than random pairs, validating chemical relevance.
- topAdducts output ranks mass differences by observed count, with known chemical adducts (e.g., [M+H], [M+Na]) appearing in top ranks for biological sample types.
- pointsAdducts() visualization shows annotated adduct peaks (marked in user-specified color, e.g., red) at expected mass-to-charge positions on the mass spectrum.

## Limitations

- Matching relies on mass tolerance (bin width); incorrect bin width specification will cause false negatives or spurious matches.
- Reference libraries (adducts, adducts2) are fixed and biologically-focused; unusual or sample-specific adducts will not be detected—custom libraries can be supplied but require manual curation.
- High quantile values are typical (most mass differences have zero to few counts), making it difficult to assess statistical significance of individual matches without follow-up spatial correlation testing.
- No built-in mechanism to weight adduct assignments by prior probability or instrument/sample type; all reference adducts are treated equally.
- Ambiguity when multiple adducts have nearly identical masses; the function reports the closest match without flagging alternatives.

## Evidence

- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks have that mass difference) and the quantile.: "looks for known adducts by finding the closest-matching bin in the mass difference histogram"
- [readme] The procedure above (`adductMatch`) only looks for known adducts. What about peaks in the histogram which may not have a good match with the reference list? The function `topAdducts` performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts.: "topAdducts performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts"
- [other] There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples.: "two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species"
- [other] Annotate ion pairs by matching mass differences to the adducts2 reference set using adductMatch() to identify potential chemical transformations.: "matching mass differences to the adducts2 reference set using adductMatch() to identify potential chemical transformations"
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument"
