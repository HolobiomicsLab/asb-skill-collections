---
name: multiple-testing-correction-bonferroni
description: Use when when you have computed raw p-values for multiple independent statistical tests (e.g., Pearson correlation tests across all pairwise ion combinations in MSI data) and need to report which results remain significant after accounting for multiple comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3179
  tools:
  - mass2adduct
  - R
  - corrPairsMSI
  - corrPairsMSIchunks
  - mass2adduct (R package)
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
---

# Multiple-testing correction (Bonferroni)

## Summary

Apply Bonferroni correction to control false-positive rate when testing statistical significance across many pairwise comparisons in mass spectrometry imaging data. This correction adjusts p-value thresholds by the total number of tests performed, protecting against spurious findings when screening thousands of ion-pair correlations.

## When to use

When you have computed raw p-values for multiple independent statistical tests (e.g., Pearson correlation tests across all pairwise ion combinations in MSI data) and need to report which results remain significant after accounting for multiple comparisons. Bonferroni is appropriate when the number of tests is moderate (hundreds to low thousands) and you can afford conservative significance thresholds.

## When NOT to use

- When you have performed only a single or very few hypothesis tests—Bonferroni correction is overly conservative and unnecessary for small test counts.
- When test results are not independent (e.g., correlated ion pairs)—Bonferroni assumes independence and will be too stringent under positive correlation.
- When you wish to control false-discovery rate (FDR) rather than family-wise error rate—use Benjamini–Hochberg or similar FDR methods instead.

## Inputs

- massdiff object (annotated ion pairs with raw p-values from correlation tests)
- number of statistical tests performed (typically implicit in massdiff object length)
- significance threshold (default α = 0.05)

## Outputs

- massdiff object with Bonferroni-corrected Significance field (boolean)
- p-value threshold after correction (α / number of tests)
- subset of ion pairs meeting corrected significance

## How to apply

After computing raw p-values for each pairwise correlation test (e.g., via corrPairsMSI()), apply Bonferroni correction by dividing the significance threshold (typically α = 0.05) by the total number of tests performed. A result is considered significant if its raw p-value is less than α / (number of tests). The mass2adduct package applies this correction automatically in corrPairsMSI(), returning a boolean Significance field that indicates whether each ion pair meets the Bonferroni-corrected threshold. Report both raw p-values and the corrected significance status in results to allow downstream filtering and interpretation.

## Related tools

- **corrPairsMSI** (Computes two-tailed Pearson correlation tests for each ion pair and automatically applies Bonferroni correction to output significance field) — https://github.com/kbseah/mass2adduct
- **corrPairsMSIchunks** (Memory-efficient variant of corrPairsMSI for large datasets; also applies Bonferroni correction to output) — https://github.com/kbseah/mass2adduct
- **mass2adduct (R package)** (Host package providing corrPairsMSI and corrPairsMSIchunks functions with built-in Bonferroni correction) — https://github.com/kbseah/mass2adduct

## Examples

```
d.diff.annot.cor <- corrPairsMSI(d, d.diff.annot); # Returns massdiff object with raw P.value and Bonferroni-corrected Significance fields
```

## Evaluation signals

- Corrected significance threshold = α / (total number of ion pairs tested). Verify this calculation matches the reported threshold.
- All Significance boolean values in output massdiff object should be FALSE for raw p-values ≥ corrected threshold; TRUE only for raw p-values < corrected threshold.
- Raw p-values and corrected Significance field should both be present in output, allowing manual verification of correction logic.
- The number of significant ion pairs after correction should be substantially lower than before correction, reflecting the stringency of family-wise error control.
- Bonferroni-corrected results should be reproducible: identical inputs and parameters must yield identical Significance assignments across runs.

## Limitations

- Bonferroni correction is conservative, especially when the number of tests is large (thousands or more), and may fail to detect true signals.
- The correction assumes independence between tests; ion-pair correlations in MSI data may violate this assumption, leading to over-correction.
- For very large datasets (hundreds of thousands of ion pairs), the corrected significance threshold becomes extremely stringent, potentially yielding zero or very few significant results.
- The package applies Bonferroni correction at default α = 0.05 by default; custom thresholds may require manual adjustment of results post-hoc.

## Evidence

- [other] This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object.: "This performs a correlation test (by default two-tailed with Pearson's method) on each pair of peaks in the massdiff object."
- [other] Extract and report correlation Estimate, raw P.value, and Bonferroni-corrected Significance (boolean) fields in the output massdiff object.: "Extract and report correlation Estimate, raw P.value, and Bonferroni-corrected Significance (boolean) fields in the output massdiff object."
- [readme] By default the cutoff for significance is p=0.05 with Bonferroni correction.: "By default the cutoff for significance is p=0.05 with Bonferroni correction."
- [readme] Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction.: "Output is a data.frame with p-values for each ion pair. By default the cutoff for significance is p=0.05 with Bonferroni correction."
