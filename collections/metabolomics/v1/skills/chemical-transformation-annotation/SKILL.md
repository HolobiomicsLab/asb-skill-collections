---
name: chemical-transformation-annotation
description: Use when you have computed a histogram of pairwise mass differences from MS peaks and want to determine which observed mass differences correspond to known chemical species such as matrix adducts (e.g. [M+Na]+, [M+K]+), salt ions, or neutral losses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - SCiLS
  - MSiReader
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

# Chemical Transformation Annotation

## Summary

Annotate observed mass differences in mass spectrometry imaging data by matching them to known chemical transformations (adducts, neutral losses, fragmentations) using reference databases. This identifies which molecular adducts or chemical species are responsible for peaks in the mass difference histogram.

## When to use

You have computed a histogram of pairwise mass differences from MS peaks and want to determine which observed mass differences correspond to known chemical species such as matrix adducts (e.g. [M+Na]+, [M+K]+), salt ions, or neutral losses. Use this when you need to annotate the 'dark metabolome' — peaks that represent chemical transformations rather than unmodified target molecules.

## When NOT to use

- Your input is a list of raw mass-to-charge (m/z) values without computed pairwise differences — first apply massdiff() to generate mass differences.
- You have not yet binned mass differences into a histogram — adductMatch() requires a histogram object with counts per bin, not raw continuous differences.
- You are working with unannotated custom mass differences outside the scope of known chemical adducts (e.g., instrument artifacts or undocumented modifications) — annotation requires a reference database of expected transformations.

## Inputs

- massdiffhist object (histogram of mass differences with counts per bin)
- massdiff data.frame (pairwise mass differences with A, B, diff columns)
- Reference adduct dataset (data.frame with name, formula, mass columns)

## Outputs

- Annotated histogram with matched adduct names and counts
- Ranked list of known adduct matches with occurrence statistics
- Filtered massdiff object containing only ion pairs with known adduct annotations

## How to apply

Apply the adductMatch() function to a mass difference histogram object (produced by hist() on a massdiff object) to match observed mass difference bins to a reference database of known adducts such as the built-in `adducts` or `adducts2` datasets. The function finds the closest-matching bin in the histogram for each known adduct, reporting the count (number of peak pairs with that mass difference) and quantile rank. Optionally, apply topAdducts() to rank mass differences by occurrence frequency and report matches to known adducts for the top n peaks, revealing which chemical transformations are most abundant. For individual ion pairs, apply adductMatch() directly to the massdiff data.frame to annotate and filter pairs with known matches. Reference datasets must be data.frames with three columns: name, formula, and mass.

## Related tools

- **mass2adduct** (Primary package providing adductMatch() and topAdducts() functions for annotation; also provides massdiff() and hist() for generating input histogram) — https://github.com/kbseah/mass2adduct
- **R** (Runtime environment for loading mass2adduct package and executing annotation functions)
- **SCiLS** (MSI software that exports CSV data files suitable for preprocessing before annotation workflow)
- **MSiReader** (MSI software that exports CSV data files suitable for preprocessing before annotation workflow)
- **Cardinal** (R package for MSI preprocessing; MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to msimat format required for mass2adduct)

## Examples

```
d.diff.hist <- hist(massdiff(d)); adductMatch(d.diff.hist); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- Matched adducts should have biologically plausible formulas and mass values; verify against literature (e.g., Na+ = 22.9898 Da, K+ = 38.9631 Da, common matrix ions).
- High-count mass differences (reported by topAdducts) should correspond to abundant, known chemical species; low-frequency matches may indicate noise or instrument artifacts.
- Quantile values from adductMatch() should be interpreted relative to the total distribution; expect high quantiles because most mass differences are rare.
- When applied to individual ion pairs (massdiff data.frame), the filtered output should contain only pairs where the observed mass difference falls within the histogram bin tolerance of a known adduct reference mass.
- Downstream spatial correlation analysis (corrPairsMSI) of annotated pairs should yield significant correlations (p < 0.05 with Bonferroni correction) if annotation is correct — parent and adduct ions should co-localize in the imaging data.

## Limitations

- Annotation accuracy depends on the completeness and correctness of the reference adduct database; rare or novel chemical transformations will not be detected.
- Mass difference histogram binning (default bin width typically 0.01 Da) must match instrument mass accuracy; bins that are too wide merge distinct adducts, too narrow create spurious gaps.
- High quantile values are expected because most mass differences occur infrequently, making it difficult to distinguish significant signals from random noise without spatial or correlation validation.
- The method assumes all peaks in the input data are true MS signals; low-abundance noise peaks can generate spurious mass differences that do not represent real adducts.
- Reference datasets (`adducts`, `adducts2`) are curated for biologically-relevant species in metabolomics; non-biological samples or exotic matrix systems may require custom reference datasets.

## Evidence

- [readme] The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram: "The following function looks for known adducts by finding the closest-matching bin in the mass difference histogram produced above. It reports the number of counts (i.e. how many pairs of MS peaks"
- [readme] topAdducts ranks mass differences by occurrence and reports matches to known adducts: "`topAdducts` performs the complementary function: Rank mass differences by the number of times they are observed, and report any matches to known adducts."
- [methods] Built-in reference datasets for known adducts in mass spectrometry: "There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples."
- [methods] Direct annotation of individual ion pairs with adductMatch: "We can match massdiffs to specific adduct types using the same function `adductMatch` that we applied to the histogram above."
- [intro] Adduct formation in mass spectrometry imaging context: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
