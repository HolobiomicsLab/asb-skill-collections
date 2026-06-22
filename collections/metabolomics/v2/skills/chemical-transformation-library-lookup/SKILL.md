---
name: chemical-transformation-library-lookup
description: Use when you have a histogram of mass differences (from pairwise comparisons of detected m/z values in MALDI-MS or MSI data) and need to annotate which differences correspond to known molecular adducts—particularly when investigating unexpected or ambiguous peaks in the mass spectrum, or when.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3431
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# Filter: match mass differences to known adducts via adductMatch

## Summary

Match observed mass differences from pairwise ion comparisons to a reference library of known chemical adducts by finding the closest-matching bin in a mass difference histogram. This enables annotation of MS peaks with their likely chemical identities (e.g., [M+Na]+, [M-H2O]+) and quantification of adduct prevalence in imaging datasets.

## When to use

Apply this skill when you have a histogram of mass differences (from pairwise comparisons of detected m/z values in MALDI-MS or MSI data) and need to annotate which differences correspond to known molecular adducts—particularly when investigating unexpected or ambiguous peaks in the mass spectrum, or when systematically characterizing the full set of adducts present in a complex sample like a MALDI matrix or biological tissue.

## When NOT to use

- If your reference adduct library is incomplete or not validated for your biological matrix or ionization method—adductMatch can only match against known entries, so novel adducts will be missed.
- If your mass difference histogram has not been binned with an appropriate bin width for your instrument's mass accuracy; unbinned or mis-binned data will produce spurious matches or fail to cluster true adducts together.
- If you need to identify adducts de novo without a reference table; use topAdducts() instead to rank mass differences by occurrence and manually validate the most abundant ones.

## Inputs

- massdiff histogram object (output from hist(massdiff(...)) with bins at user-defined width, e.g., 0.01 mDa)
- reference adduct table (data.frame with columns: name, formula, mass; e.g., mass2adduct::adducts or custom table)

## Outputs

- annotated massdiff object with 'matches' column linking observed mass differences to known adduct names
- summary table of matched adducts with counts per ion pair and quantile ranks

## How to apply

Load a massdiff histogram object (binned mass differences with user-specified bin width, typically 0.01 mDa, to account for instrument mass precision) and a reference adduct table (e.g., the built-in `adducts` or `adducts2` datasets in mass2adduct, which list biologically-relevant chemical species with name, formula, and exact mass). Apply the adductMatch() function to find, for each histogram bin, the closest-matching adduct mass from the reference table. The function reports the number of counts (ion pairs with that mass difference) and quantile rank for each match. Retain only matches with sufficient count support (typically n ≥ 2) to filter out noise. The output is an annotated massdiff object with an added 'matches' column listing the matched adduct name(s) for each significant mass difference.

## Related tools

- **mass2adduct** (R package providing adductMatch() function, massdiff() histogram generation, and reference adduct datasets (adducts, adducts2)) — https://github.com/kbseah/mass2adduct
- **R** (Runtime environment for executing mass2adduct workflows and adductMatch matching operations)
- **Cardinal** (Optional upstream MSI data processor; outputs can be converted to mass2adduct msimat format via cardinal2msimat() before adductMatch) — http://cardinalmsi.org/

## Examples

```
head(adductMatch(d.diff.hist))
```

## Evaluation signals

- Matched adducts have biologically plausible identities (e.g., [M+Na]+, [M+H]+, [M-H2O]+) consistent with the ionization method and sample matrix.
- High-count matches (n ≥ 2–5 ion pairs) show quantile ranks in the upper percentiles of the histogram, indicating they are among the most abundant mass differences observed.
- Matched adduct masses are within the bin width (e.g., ±0.005 mDa for 0.01 mDa bins) of the observed mass difference; verify by plotting histogram and overlay reference masses.
- Downstream correlation analysis (corrPairsMSI) confirms that parent and putative adduct ions show significant spatial co-localization (p < 0.05 with Bonferroni correction) in MSI pixels, supporting biological relevance.
- Summary report shows expected adduct types for the given matrix and tissue type; absence of expected adducts or dominance of unexpected adducts suggests reference table needs refinement or experimental conditions differ from literature.

## Limitations

- adductMatch relies on a complete and accurate reference library; unknown adducts or species not in the reference table will not be detected or will be misassigned to the closest matching entry.
- Mass measurement error and instrument calibration drift can cause observed mass differences to fall outside bin boundaries, leading to failure-to-match or mismatch to incorrect adducts; requires careful selection of bin width appropriate to instrument mass accuracy (typically ±5–10 ppm for TOF-MS).
- High-complexity samples with many overlapping adducts may produce multiple matches per histogram bin; the function reports the closest match but does not resolve ambiguities; manual or correlation-based filtering is required.
- The method does not account for intensity or relative abundance of adducts, only counts and quantiles; cannot distinguish between highly abundant true adducts and spurious low-intensity matches without additional filtering.
- Package changelog not available, limiting reproducibility tracking across versions; users should pin mass2adduct version in dependency files.

## Evidence

- [other] The adductMatch function identifies known adducts by finding the closest-matching bin in a mass difference histogram: "The adductMatch function identifies known adducts by finding the closest-matching bin in the mass difference histogram produced from pairwise mass comparisons"
- [other] Reference adduct table with built-in datasets listing biologically-relevant chemical species: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species"
- [other] Output includes matched adduct name and quantile ranks: "Generate a summary report showing matched adduct names, counts of ion pairs per adduct type, and quantile ranks"
- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks have that mass difference) and the quantile.: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks"
- [readme] Bin width selection based on instrument mass precision: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [other] Spatial correlation testing validates adduct assignment: "Test for correlations between parent and adduct ions—This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object."
