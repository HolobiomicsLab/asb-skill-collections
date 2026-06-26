---
name: histogram-peak-occurrence-analysis
description: Use when after you have computed a histogram of pairwise mass differences
  from MSI peak data and want to identify which mass shifts occur most frequently
  and whether they correspond to known chemical adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  tools:
  - mass2adduct
  - R
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
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into
  memory during an R session.
- corrPairsMSI(d,d.diff.annot)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct_cq
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct_cq
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

# Rank Mass Differences by Occurrence with topAdducts

## Summary

This skill ranks mass differences observed in MALDI-MS imaging data by their occurrence frequency and cross-references them against known chemical adducts. It surfaces the most abundant molecular adducts—which represent potential metabolite–matrix or metabolite–salt ion associations—from a binned mass difference histogram.

## When to use

Apply this skill after you have computed a histogram of pairwise mass differences from MSI peak data and want to identify which mass shifts occur most frequently and whether they correspond to known chemical adducts. This is the appropriate step when your analysis goal is to prioritize candidate adducts for downstream validation (e.g., spatial correlation testing) rather than exhaustively matching all peaks to a reference database.

## When NOT to use

- The input mass difference histogram has not been binned with an appropriate bin width for your instrument's mass accuracy; topAdducts will rank noisy or spurious differences.
- You only care about known adducts and do not need discovery of novel mass shifts; use `adductMatch()` instead for faster, reference-only matching.
- Your raw MSI data has not yet been pre-processed (peak-binned, baseline-corrected, normalized); topAdducts expects a validated histogram as input.

## Inputs

- massdiffhist object (output from hist() applied to a massdiff data frame)

## Outputs

- data.frame with columns: mass difference value, occurrence count, quantile rank, matched adduct name (or NA if no match)

## How to apply

Load a preprocessed mass difference histogram object (created by applying `hist()` to a `massdiff` object) into R. Call the `topAdducts()` function with the histogram and specify the number of top-ranked hits to return (e.g., `n=10`). The function internally ranks all observed mass differences by their occurrence counts in descending order, then cross-references each value against the built-in `adducts` (or user-supplied) reference table using a closest-match lookup (within histogram bin width). The output is a ranked data frame containing mass difference values, occurrence counts, quantile ranks, and matched adduct names or chemical formulas when a reference hit is found. The ranking by occurrence is the primary sorting criterion, making high-abundance mass shifts discoverable regardless of whether they match known adducts—a key advantage over `adductMatch()`, which only reports hits with known references.

## Related tools

- **mass2adduct** (R package providing the topAdducts function and supporting massdiff and hist methods for generating ranked adduct occurrence tables) — https://github.com/kbseah/mass2adduct
- **R** (Statistical computing environment in which mass2adduct functions are executed and histogram objects are manipulated)

## Examples

```
topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Output data frame contains n rows (matching the requested parameter) ranked by occurrence count in descending order, with no duplicate mass difference values.
- Quantile values increase monotonically from top to bottom (highest occurrence → lowest quantile; lowest occurrence → high quantile).
- All mass differences in the output fall within the range and bin-width resolution of the input histogram object.
- Adduct name matches (non-NA rows) correspond to mass differences within the closest-match tolerance of known adduct masses in the reference table; verify by manual spot-check against `adducts` or `adducts2` data set.
- When compared to full histogram, top-ranked entries account for a visually obvious peak or shoulder in the histogram plot.

## Limitations

- topAdducts relies on accurate binning during histogram creation; if bin width is too coarse, genuine adducts may merge; if too fine, random noise will appear as rare mass shifts.
- The function performs closest-match lookup against the reference adduct table, so unknown or non-standard adducts will not be annotated even if they rank highly by occurrence.
- Output quantile values are typically very high (close to 1) because most mass differences have zero or few counts; quantile alone is not a strong statistical signal of biological relevance.
- For very large MSI datasets (hundreds or thousands of peaks), memory constraints may prevent computation of the full pairwise mass difference matrix; users must use the Perl script `msimunging.pl` or chunked processing elsewhere before reaching topAdducts.

## Evidence

- [other] topAdducts ranks mass differences by their occurrences in descending order and reports matches to known adducts if any are found: "topAdducts ranks mass differences by their occurrences, and reports them in descending order, as well as matches to known adducts, if any"
- [other] The function ranks all mass differences by their occurrence counts in descending order and cross-references each against the built-in adducts or user-supplied adduct reference table: "Apply topAdducts function to the histogram object, specifying the number of top hits to return (e.g., n=10). The function ranks all mass differences by their occurrence counts in descending order and"
- [other] Output is a ranked table as a data frame containing mass difference values, occurrence counts, quantile ranks, and matched adduct names: "Output the ranked table as a data frame containing mass difference values, occurrence counts, quantile ranks, and matched adduct names (if applicable)"
- [readme] topAdducts performs the complementary function to adductMatch by ranking mass differences by occurrence and reporting matches to known adducts: "The function `topAdducts` performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts."
- [readme] The package includes two built-in datasets of biologically-relevant chemical species for adduct reference matching: "The package comes with a small data set of common molecular adducts, called `adducts` (use the command `help(adducts)` to see a description). Users can supply their own custom sets of adducts"
