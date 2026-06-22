---
name: reference-database-tolerance-mapping
description: Use when you have calculated pairwise mass differences from MS peaks (via massdiff()) and binned them into a histogram, and now need to identify which observed mass differences correspond to known molecular adducts (e.g., [M+Na]+, [M+H]+, matrix-related species) rather than random noise.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - mass2adduct
  - R
  - Cardinal
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reference-Database Tolerance Mapping

## Summary

Match observed mass differences to known chemical adducts by finding the closest-matching bin in a mass difference histogram within a user-specified tolerance window. This skill annotates mass spectrometry peaks with their likely adduct identities, enabling metabolite annotation and validation.

## When to use

You have calculated pairwise mass differences from MS peaks (via massdiff()) and binned them into a histogram, and now need to identify which observed mass differences correspond to known molecular adducts (e.g., [M+Na]+, [M+H]+, matrix-related species) rather than random noise. This is essential when your goal is to annotate the 'dark metabolome'—peaks obscured by adduct formation—or validate parent–adduct ion relationships in MALDI-MSI datasets.

## When NOT to use

- Your mass differences have not yet been binned into a histogram (must call hist() first to account for measurement error and uncertainty)
- You are working with unbinned, raw mass differences without accounting for instrument precision—closest-bin matching requires a histogram structure
- Your reference adduct table is incomplete or lacks the required 'name', 'formula', 'mass' columns; the function depends on exact schema match

## Inputs

- massdiff object (data.frame with columns for parent mass A, adduct mass B, mass difference)
- mass difference histogram (output from hist() applied to massdiff)
- reference adduct table (data.frame with columns: name, formula, mass)

## Outputs

- annotated massdiff object with 'matches' column listing matched adduct names
- summary report with matched adduct names, counts per adduct type, and quantile ranks

## How to apply

Load a massdiff object (output from massdiff() containing pairwise mass A, B, and difference) and a reference adduct table (built-in 'adducts' or 'adducts2' datasets, or a custom data.frame with columns 'name', 'formula', 'mass'). Apply adductMatch() to find the closest-matching bin in the mass difference histogram for each observed mass difference, using the bin width set during histogram construction (typically 0.01 Da for high-resolution instruments). The function reports the count of ion pairs per adduct type and their quantile ranks. Filter results to retain only matches meeting your significance threshold. The rationale is that true molecular adducts will cluster tightly around reference mass values (within instrument precision), while random mass differences will scatter; the histogram bins aggregate this clustering, and closest-bin matching leverages the fact that molecular adducts are discrete, not continuous.

## Related tools

- **mass2adduct** (R package providing massdiff(), hist(), and adductMatch() functions for adduct identification workflow) — https://github.com/kbseah/mass2adduct
- **R** (Execution environment for mass2adduct package and adductMatch function)
- **Cardinal** (Optional: pre-processes MSI data and can convert MSProcessedImagingExperiment or MSContinuousImagingExperiment objects to mass2adduct's msimat format for downstream adduct matching) — http://cardinalmsi.org/

## Examples

```
head(adductMatch(d.diff.hist))
```

## Evaluation signals

- Matched adducts appear in the output with non-zero counts (not all matches will succeed; zero-count matches indicate poor reference-data alignment)
- Quantile ranks are reported for each matched adduct; high quantile values (>0.9) are expected because most mass differences are rare or zero-count
- Ion pairs with successful matches have a new 'matches' column populated with adduct names; unmatched pairs are absent or carry NA
- The number of unique adducts matched is ≤ the size of the reference table (sanity check: no spurious extra adducts invented)
- Downstream spatial correlation test (corrPairsMSI) shows significant Pearson correlation (p < 0.05 with Bonferroni correction) between parent and matched adduct ion intensities across pixels, validating the biological relevance of the match

## Limitations

- Matching quality depends critically on histogram bin width (set during hist() call); bin width must reflect true instrument mass precision. If bin width is too wide, multiple distinct adducts will collapse into one bin; if too narrow, true adducts will scatter across bins and fail to match.
- The function finds only the closest-matching bin; if the reference table is sparse or incomplete, true adducts may not be present and will be missed or matched to the nearest wrong entry.
- Quantile values are typically very high (skewed toward 1.0) because the majority of mass differences have zero or near-zero counts; this does not reflect biological confidence, only statistical rank. True adducts must be validated by spatial correlation (corrPairsMSI) or other downstream evidence.
- The method assumes adducts are discrete and well-separated in mass space; overlapping or near-identical adducts in the reference table may cause ambiguous or incorrect assignments.

## Evidence

- [other] The adductMatch function identifies known adducts by finding the closest-matching bin in a mass difference histogram produced from pairwise mass comparisons: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above."
- [other] Reference adduct tables contain biologically-relevant chemical species in standardized format: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species"
- [readme] Histogram binning is essential to handle measurement error and precision: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] Output includes matched adduct names, counts, and quantile ranks: "It reports the number of counts (i.e. how many pairs of MS peaks have that mass difference) and the quantile."
- [readme] Custom adduct tables follow a specific schema: "Users can supply their own custom sets of adducts as long as they are in the same format (as a data.frame with three columns: `name`, `formula`, `mass`)"
