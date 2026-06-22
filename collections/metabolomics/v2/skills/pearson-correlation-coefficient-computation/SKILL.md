---
name: pearson-correlation-coefficient-computation
description: Use when after annotating mass-difference pairs with candidate adduct identities, compute correlations to test whether putative parent and adduct ion intensities co-vary across the imaging pixel grid. High positive correlation (with Bonferroni-corrected p-value < 0.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
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

# Pearson Correlation Coefficient Computation

## Summary

Compute two-tailed Pearson correlation coefficients and p-values for pairs of mass spectrometry imaging intensity vectors to assess whether candidate parent and adduct ion abundances co-vary spatially across pixels. This identifies statistically significant ion relationships that support molecular adduct hypotheses.

## When to use

After annotating mass-difference pairs with candidate adduct identities, compute correlations to test whether putative parent and adduct ion intensities co-vary across the imaging pixel grid. High positive correlation (with Bonferroni-corrected p-value < 0.05) strengthens the evidence that two peaks represent a true parent–adduct pair rather than random mass differences.

## When NOT to use

- Input intensity data are not spatially resolved (e.g., bulk MS without pixel coordinates); correlations will be meaningless without spatial structure.
- Ion pair list is not yet annotated with candidate adduct identities; run adductMatch() or topAdducts() first to identify plausible mass differences.
- Dataset is too large to fit even one pair of intensity vectors in memory; even corrPairsMSIchunks may fail if individual vectors exceed RAM.

## Inputs

- msimat object (MSI intensity matrix with peaks as columns, pixels/spectra as rows)
- massdiff object with annotated matches (candidate parent–adduct ion pairs)

## Outputs

- annotated massdiff object with appended columns: Estimate (correlation coefficient), P.value (uncorrected p-value), Significance (Bonferroni-corrected boolean flag)

## How to apply

Load the MSI intensity matrix (msimat object) and the adduct-annotated mass-difference table (massdiff object with matches column) into R. Call corrPairsMSI() to perform a two-tailed Pearson correlation test on each ion pair, computing correlation coefficients and raw p-values. Apply Bonferroni multiple-testing correction across all pairs; peaks with corrected p-value < 0.05 are flagged as significant. For datasets exceeding available memory, invoke corrPairsMSIchunks() instead, specifying mem.limit in GB and ncores for parallel processing to break the pairwise correlations into serial chunks. Extract and interpret the three output columns: Estimate (Pearson r), P.value (uncorrected), and Significance (boolean after correction).

## Related tools

- **mass2adduct** (R package providing corrPairsMSI and corrPairsMSIchunks functions for computing Pearson correlations on MSI ion pairs) — https://github.com/kbseah/mass2adduct
- **R** (Statistical computing environment hosting correlation function implementation)
- **Cardinal** (Optional upstream tool for MSI data processing; objects can be converted to msimat format for use with corrPairsMSI) — http://cardinalmsi.org/

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot)
```

## Evaluation signals

- Returned data.frame has exactly three new columns (Estimate, P.value, Significance) appended to input massdiff object; no rows dropped or reordered.
- Estimate values lie in range [−1, +1] (valid Pearson r); P.value and Significance columns contain no NA values for non-filtered pairs.
- Bonferroni-corrected significance threshold is 0.05 / (number of pairs); manually recompute a subset of correlations using cor.test() in base R to verify coefficient and uncorrected p-value match.
- Pairs flagged Significance=TRUE show high positive correlation (r typically > 0.5) and low uncorrected p-values (p < 0.05/n_pairs); opposite pattern for Significance=FALSE pairs.
- Output is identical when run on subsets of data (i.e., correlation of peaks A and B is deterministic regardless of which other peaks are in the matrix).

## Limitations

- Bonferroni correction is conservative when the number of pairs is very large (e.g., thousands); weak true signals may be missed. Alternative multiple-testing corrections are not exposed in the current interface.
- Pearson correlation assumes linear relationships and is sensitive to outliers; bimodal or heavily skewed intensity distributions may yield misleading coefficients.
- Spatial autocorrelation in the imaging pixel grid violates the independence assumption underlying standard p-value interpretation; adjacent pixels are not independent samples.
- corrPairsMSIchunks requires the user to manually specify mem.limit and ncores; poor choices can cause crashes or inefficient computation without diagnostic messages.
- No changelog is available for reproducibility tracking of function behavior across package versions.

## Evidence

- [other] corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks: "corrPairsMSI performs a two-tailed correlation test using Pearson's method on each pair of peaks in the annotated mass-difference object, generating correlation statistics for parent and adduct ion"
- [other] Extract correlation results: Estimate, P.value, and Significance: "Extract correlation results: Estimate (correlation coefficient), P.value (raw uncorrected p-value), and Significance (boolean flag after Bonferroni multiple-testing correction)."
- [other] corrPairsMSIchunks for large datasets with mem.limit and ncores: "For datasets exceeding available memory, invoke corrPairsMSIchunks instead, specifying mem.limit in GB and ncores for parallel processing to chunk the pairwise correlations."
- [readme] Test for spatial correlations between mass peaks in MS imaging data: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function)."
- [readme] Output is a data.frame with p-values for each ion pair; default cutoff for significance is p=0.05 with Bonferroni correction: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
