---
name: chemical-transformation-annotation
description: Use when after computing all pairwise mass differences from MS imaging peaks and binning them into a histogram, use this skill when you need to prioritize which mass differences are most likely to represent real chemical adducts (rather than noise or measurement artifacts) by ranking them by.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mass2adduct
  - R
  - Cardinal
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into memory during an R session.
- corrPairsMSI(d,d.diff.annot)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
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

# Filter: rank annotated mass differences by occurrence with topAdducts

## Summary

Rank pairwise mass differences from MS imaging data by occurrence frequency and annotate matches to known molecular adducts (e.g., [M+Na]+, [M–H2O]+). This identifies the most abundant chemical transformations between detected ions, revealing matrix and salt adducts that form during MALDI ionization.

## When to use

After computing all pairwise mass differences from MS imaging peaks and binning them into a histogram, use this skill when you need to prioritize which mass differences are most likely to represent real chemical adducts (rather than noise or measurement artifacts) by ranking them by co-occurrence frequency. Apply this when you have a preprocessed massdiff histogram object and want to discover both known adducts and previously uncharacterized mass shifts without exhaustive manual inspection.

## When NOT to use

- Input is raw MS intensity matrix or single mass spectrum — use massdiff() first to compute pairwise differences
- Mass differences have not been binned into a histogram — use hist() on the massdiff object before calling topAdducts
- You only want to match a known adduct list without ranking by frequency — use adductMatch() instead for direct reference lookup

## Inputs

- massdiff histogram object (class: massdiffhist, produced by hist(massdiff(...)))
- integer n specifying number of top hits to report (e.g., n=10)
- optional: custom adduct reference data frame (3 columns: name, formula, mass)

## Outputs

- ranked data frame with columns: mass difference (Da), occurrence count, quantile rank, matched adduct name (if found)
- data structure suitable for downstream hypothesis testing (e.g., spatial correlation of parent–adduct ion pairs)

## How to apply

Load a massdiff histogram object (produced by hist() applied to a massdiff data frame) into R. Call topAdducts(d.diff.hist, n=k) where k is the desired number of top-ranked hits to return (e.g., n=10). The function iterates through all binned mass differences in descending order of occurrence count, cross-references each against a built-in adduct reference table (mass2adduct's `adducts` or `adducts2` datasets) or a user-supplied custom adduct data frame (with columns: name, formula, mass), and returns a ranked data frame. Output columns include the mass difference value, occurrence count (how many peak pairs exhibit that difference), quantile rank, and matched adduct name if one is found within the histogram's bin width tolerance. The ranking is based on empirical frequency: mass differences observed in many peak pairs rank higher than those seen once or twice, making frequent shifts more discoverable than rare measurement noise.

## Related tools

- **mass2adduct** (R package providing topAdducts function, massdiff and hist methods, and built-in adduct reference datasets) — https://github.com/kbseah/mass2adduct
- **R** (runtime environment for loading histogram objects and executing topAdducts ranking)
- **Cardinal** (optional upstream tool for MSI preprocessing; outputs can be converted to msimat/massdiff format for use in this workflow) — http://cardinalmsi.org/

## Examples

```
topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Output data frame is sorted by occurrence count in descending order; highest-count mass difference appears in first row
- Quantile values are typically high (0.5–1.0) because most mass differences have zero or few counts; a quantile <0.1 indicates an outlier
- Matched adduct names in output row correspond to known biological adducts (e.g., Na+, K+, NH4+, or matrix-related ions); no matches are expected for rare, unmapped shifts
- Occurrence counts are non-negative integers and sum to total number of peak pairs in the original massdiff object
- Output has no missing values in mass difference or count columns; adduct name field is NA or blank only when no reference match exists within bin width

## Limitations

- Ranking is sensitive to histogram bin width choice; a bin width too large merges distinct adducts, too small creates artifactual fragmentation
- Built-in adduct reference tables (adducts, adducts2) are static and biologically biased toward common metabolite and matrix ions; rare or instrument-specific adducts will not be matched
- topAdducts reports only frequency rank, not statistical significance; a high-count mass difference may still be noise if peak pairs are uncorrelated in space (test with corrPairsMSI for validation)
- Quantile calculations assume binned histogram; unequal bin widths or sparse histograms may produce misleading quantile values
- No changelog tracking is available in the mass2adduct repository, limiting reproducibility and version-specific parameter interpretation

## Evidence

- [other] topAdducts ranks mass differences by their occurrences in descending order and reports matches to known adducts if any are found.: "`topAdducts` ranks mass differences by their occurrences, and reports them in descending order, as well as matches to known adducts, if any"
- [readme] The function processes a histogram object and returns a ranked, annotated table of mass differences with occurrence counts and adduct names.: "The function ranks all mass differences by the number of times they are observed, and report any matches to known adducts."
- [readme] Built-in reference tables exist for known adducts; users can supply custom adduct data frames.: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species"
- [readme] Downstream validation requires testing spatial correlation of parent and adduct ion pairs in the imaging data.: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [intro] Adducts form between target molecules and matrix or salt ions in MALDI-MS imaging.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
