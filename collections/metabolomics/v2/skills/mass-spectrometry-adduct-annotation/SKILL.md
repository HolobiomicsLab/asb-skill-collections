---
name: mass-spectrometry-adduct-annotation
description: Use when you have tabulated pairwise mass differences from a MALDI-MS imaging dataset (via massdiff()) and need to identify which observed mass differences correspond to known chemical adducts (e.g., [M+H]+, [M+Na]+, [M-H2O]+).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3370
  tools:
  - mass2adduct
  - R
  - Cardinal
  - RDKit
  - Met-ID
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
- doi: 10.1021/acs.analchem.5c00633
  title: ''
- doi: 10.1021/acs.jcim.3c01082
  title: ''
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into memory during an R session.
- corrPairsMSI(d,d.diff.annot)
- Powered by RDKit
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct_cq
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mass2adduct_cq
schema_version: 0.2.0
---

# mass-spectrometry-adduct-annotation

## Summary

Annotate mass differences observed in MALDI-MS imaging data by matching them to known adduct species using histogram binning and reference tables. This skill enables identification of molecular adducts formed between target metabolites and matrix or salt ions, illuminating peaks that would otherwise remain unassigned in the mass spectrum.

## When to use

Apply this skill when you have tabulated pairwise mass differences from a MALDI-MS imaging dataset (via massdiff()) and need to identify which observed mass differences correspond to known chemical adducts (e.g., [M+H]+, [M+Na]+, [M-H2O]+). Use it after generating a mass difference histogram and before or alongside correlation testing to validate that apparent adduct pairs are spatially colocalized.

## When NOT to use

- Mass differences have not yet been computed or binned into a histogram; first run massdiff() and hist().
- Your instrument has not been characterized for mass accuracy; bin width selection requires knowledge of measurement error and precision.
- You are analyzing low-resolution MS data (e.g., TOF with ≥0.1 Da precision) where mass differences overlap too heavily for reliable adduct assignment.

## Inputs

- massdiff object (output from massdiff() function: data.frame with columns for parent mass, adduct mass, and mass difference)
- massdiffhist object (binned histogram from hist() applied to massdiff object)
- reference adduct table (data.frame with columns: name, formula, mass; built-in options are 'adducts' or 'adducts2', or user-supplied)

## Outputs

- annotated massdiff object with added 'matches' column listing matched adduct names
- summary data.frame from adductMatch() with columns: mass difference value, occurrence count, quantile rank, matched adduct name
- ranked table from topAdducts() sorted by occurrence count in descending order, with adduct annotations where applicable

## How to apply

First, bin all pairwise mass differences into a histogram using a bin width matched to your instrument's mass precision (typically 0.01 Da for high-resolution instruments). Then apply adductMatch() to find the closest-matching bin in the histogram for each entry in a reference adduct table (use the built-in 'adducts' or 'adducts2' datasets, or supply a custom data.frame with columns: name, formula, mass). The function reports the count of ion pairs per matched adduct and quantile ranks. Complementarily, run topAdducts() to rank all mass differences by occurrence in descending order and cross-reference them against the same adduct table to discover both known and potentially novel mass differences. Filter results to retain only matches that exceed a meaningful occurrence threshold (e.g., top 10 hits), and optionally correlate the parent and adduct ion abundances across pixels using corrPairsMSI() to validate true adduct associations.

## Related tools

- **mass2adduct** (R package providing adductMatch(), topAdducts(), massdiff(), and hist() functions for adduct detection and annotation) — https://github.com/kbseah/mass2adduct
- **R** (Statistical computing environment in which mass2adduct package is executed; required for data import, function calls, and histogram generation)
- **Cardinal** (Optional R package for preprocessing MSI data; outputs can be converted to mass2adduct's msimat format via cardinal2msimat()) — http://cardinalmsi.org/

## Examples

```
d.diff.hist <- hist(massdiff(d)); head(adductMatch(d.diff.hist)); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Matched adduct names correspond to biologically or chemically plausible species (e.g., [M+H]+, [M+Na]+, [M+K]+, [M-H2O]+) given the ionization mode and sample matrix.
- Occurrence counts for matched adducts are substantially higher than background noise (i.e., quantile ranks are not in the 95th+ percentile where all mass differences have few counts).
- Parent and matched adduct ion pairs show statistically significant spatial correlation (Pearson p < 0.05 with Bonferroni correction) in MSI pixel abundances, as confirmed by corrPairsMSI().
- Top-ranked mass differences from topAdducts() (e.g., n=10) include expected adducts for your sample matrix; novel peaks are interrogated for known mass shifts (e.g., isotope patterns, salt ions).
- Annotation does not create logically inconsistent peak assignments (e.g., the same mass peak assigned as both parent and adduct for different pairs without supporting correlation evidence).

## Limitations

- Adduct identification depends critically on bin width selection; mismatch between chosen bin width and true mass precision will cause false matches or missed assignments.
- The reference adduct tables ('adducts', 'adducts2') contain only biologically-relevant species; novel or unusual matrix-derived adducts may not be in the reference and will be ranked by topAdducts() but not annotated.
- High-abundance peaks can spuriously generate many pairwise mass differences, inflating occurrence counts for random mass differences; spatial correlation testing (corrPairsMSI()) is essential to distinguish true adducts.
- Memory constraints may arise for very large MSI datasets (hundreds to thousands of peaks); corrPairsMSIchunks() can mitigate this but processes serially.
- Quantile ranks are often very high because the majority of mass differences have zero to few counts, making it difficult to set a principled significance threshold without external knowledge of expected adduct abundance.

## Evidence

- [readme] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [other] The adductMatch function identifies known adducts by finding the closest-matching bin in a mass difference histogram produced from pairwise mass comparisons, enabling annotation of observed mass differences to known chemical species.: "The adductMatch function identifies known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks"
- [readme] topAdducts ranks mass differences by their occurrences in descending order and reports matches to known adducts if any are found.: "The function `topAdducts` performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts."
- [readme] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] Test for spatial correlations between mass peaks in MS imaging data to see if what we believe to be pairs of parent- and derivative-ion masses tend to occur together.: "For example, we wish to see if what we believe to be pairs of parent- and derivative-ion masses tend to occur together. If they are truly related by molecular adduct formation, then their abundances"
- [other] There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species.: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species"
