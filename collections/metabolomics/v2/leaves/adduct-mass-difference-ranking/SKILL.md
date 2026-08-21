---
name: adduct-mass-difference-ranking
description: Use when you have computed a histogram of mass differences from all pairwise
  mass comparisons in your MALDI-MS imaging dataset and need to prioritize which mass
  differences are most frequent and likely represent genuine molecular adducts (e.g.,
  metabolite + matrix ions) rather than noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  techniques:
  - mass-spectrometry
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

# adduct-mass-difference-ranking

## Summary

Rank observed mass differences by their occurrence frequency in MALDI-MS imaging data and annotate matches to known adduct species. This skill identifies abundant adduct signals that would otherwise be obscured in the metabolome by systematically counting pairwise mass differences and cross-referencing them against reference adduct tables.

## When to use

Apply this skill when you have computed a histogram of mass differences from all pairwise mass comparisons in your MALDI-MS imaging dataset and need to prioritize which mass differences are most frequent and likely represent genuine molecular adducts (e.g., metabolite + matrix ions) rather than noise. Use it after binning mass differences into a histogram with instrument-appropriate bin width (e.g., 0.01 Da for high-resolution MS) and before testing spatial correlations between parent and adduct ions.

## When NOT to use

- Input is raw, unbinned pairwise mass differences without histogram binning — use hist() first to account for measurement error and uncertainty.
- You already have a curated list of target adducts and only need to filter for those specific masses — use adductMatch() instead to find only known adducts.
- Mass precision is extremely high (sub-ppm, e.g., Orbitrap) but your histogram bin width is too coarse — topAdducts will merge distinct true adducts; adjust bin width before ranking.

## Inputs

- massdiffhist object (output from hist() applied to a massdiff data frame)
- reference adduct table (data.frame with columns: name, formula, mass; e.g., built-in 'adducts' or 'adducts2' datasets)

## Outputs

- ranked data.frame containing: mass difference values, occurrence counts, quantile ranks, matched adduct names (if any matches found)

## How to apply

Load a massdiff histogram object (produced by applying hist() to the output of massdiff() on an msimat object) into R. Apply the topAdducts function, specifying the number of top hits to return (e.g., n=10 for the ten most frequent mass differences). The function ranks all mass differences in descending order by their occurrence counts (bin heights in the histogram) and cross-references each observed mass difference against a reference adduct table (using the built-in 'adducts' or 'adducts2' datasets, or a user-supplied table in data.frame format with columns: name, formula, mass). The function reports the ranked mass differences with their occurrence counts, quantile ranks, and any matched adduct names. Output is a data.frame suitable for filtering, visualization, or downstream correlation testing to confirm spatial colocalization of parent and adduct ions.

## Related tools

- **mass2adduct** (R package providing topAdducts function and supporting functions (massdiff, hist, adductMatch) for ranking and annotating mass differences in MALDI-MS imaging data) — https://github.com/kbseah/mass2adduct
- **R** (Computing environment for loading massdiffhist objects and invoking topAdducts)

## Examples

```
topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Output data.frame has exactly 4+ columns (mass_difference, count, quantile, adduct_match) and row count ≤ n parameter supplied to topAdducts.
- Occurrence counts are in strictly descending order (rank invariant: count[i] ≥ count[i+1]).
- All matched adduct names correspond to entries in the reference table used; unmatched rows have NA or empty string in adduct_match column.
- Quantile values are between 0 and 1, and generally high (>0.5–1.0) because most mass differences have zero to few counts (as noted in README).
- Rank matches visual peaks in the histogram plot — top 1–5 rows should correspond to visually prominent histogram bins.

## Limitations

- topAdducts only ranks observed mass differences; it does not distinguish true adducts from random peaks without spatial correlation testing (use corrPairsMSI afterward).
- Matching relies on finding closest-matching bin in reference table — if bin width is too coarse, true adducts may be missed; if too fine, bins may not accumulate enough counts to rank high.
- Output quantile values are often unintuitive (close to 1.0) because the majority of mass differences have zero counts; quantile interpretation requires context from the full histogram.
- Built-in 'adducts' and 'adducts2' reference tables are limited to biologically-relevant species; users must supply custom adduct tables for non-standard ionization modes or matrix types.
- For very large datasets (hundreds or thousands of peaks), the function may consume substantial memory during histogram binning; no memory-chunking option is provided for topAdducts itself (chunking available only for corrPairsMSI).

## Evidence

- [other] topAdducts ranks mass differences by their occurrences in descending order and reports matches to known adducts if any are found.: "topAdducts ranks mass differences by their occurrences in descending order and reports matches to known adducts if any are found."
- [other] The function ranks all mass differences by their occurrence counts in descending order and cross-references each against the built-in adducts or user-supplied adduct reference table.: "The function ranks all mass differences by their occurrence counts in descending order and cross-references each against the built-in adducts or user-supplied adduct reference table (if available) to"
- [readme] The procedure above (adductMatch) only looks for known adducts. What about peaks in the histogram which may not have a good match with the reference list? The function topAdducts performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts.: "The function topAdducts performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts."
- [other] Output is a data frame containing mass difference values, occurrence counts, quantile ranks, and matched adduct names (if applicable).: "Output the ranked table as a data frame containing mass difference values, occurrence counts, quantile ranks, and matched adduct names (if applicable)."
- [readme] Note that quantile values will usually be quite high because the majority of mass differences have zero to few counts.: "Note that quantile values will usually be quite high because the majority of mass differences have zero to few counts."
