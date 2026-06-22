---
name: spectral-peak-parent-product-pairing
description: Use when you have mass spectrometry imaging data with a histogram of pairwise mass differences that have already been matched to known adducts (via adductMatch), and you need to retrieve the actual mass peak pairs corresponding to a specific adduct of interest—particularly when you want to test.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - corrPairsMSI
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

# spectral-peak-parent-product-pairing

## Summary

Identify and retrieve pairs of mass spectral peaks that represent parent ions and their derivative adduct ions by matching observed mass differences to a reference table of known chemical adducts. This skill bridges annotation (matching mass differences to known species) with spatial validation, enabling confirmation that putative parent–adduct pairs co-occur in imaging data.

## When to use

Apply this skill when you have mass spectrometry imaging data with a histogram of pairwise mass differences that have already been matched to known adducts (via adductMatch), and you need to retrieve the actual mass peak pairs corresponding to a specific adduct of interest—particularly when you want to test whether those pairs show spatial correlation, which would support the hypothesis that they are true molecular adducts rather than chance matches.

## When NOT to use

- You have not yet matched mass differences to a reference adduct table; use adductMatch first to annotate mass differences with known adduct names.
- You are working with a single list of mass peaks without pairwise differences; use massdiff to compute all pairwise mass differences before retrieving specific pairs.
- Your input is already a curated set of known parent–adduct assignments; there is no need to search for pairs by mass difference tolerance.

## Inputs

- massdiff object (output from massdiff() containing parent mass A, adduct mass B, and mass difference)
- target adduct mass (numeric, e.g. 136.01600 for DHB-H2O)
- tolerance window (mDa or ppm units)

## Outputs

- filtered massdiff object (subset of input massdiff containing only pairs matching the target adduct mass within tolerance)
- candidate parent–product ion pair list

## How to apply

Start with a massdiff object (containing all pairwise mass differences from your MSI data) and the mass value and tolerance window for the adduct you wish to investigate. Use the diffGetPeaks function to extract all parent and derivative ion peak pairs whose mass difference falls within the specified tolerance (specified in mDa or ppm) of your target adduct mass. The function returns a filtered massdiff object containing only the pairs matching that criterion. This subset can then be passed to corrPairsMSI to test whether the peaks in those pairs are spatially correlated across the imaging dataset—a strong signal that they represent true adduct formation rather than spurious mass matches. The tolerance window should be set based on your instrument's mass accuracy; the README example uses ±0.5 mDa (mDa=1 for a 1 mDa window).

## Related tools

- **mass2adduct** (R package containing diffGetPeaks function for retrieving parent–adduct ion pairs by mass difference; also provides massdiff object structure and corrPairsMSI for validation) — https://github.com/kbseah/mass2adduct
- **R** (Language and runtime environment for executing diffGetPeaks and corrPairsMSI functions)
- **corrPairsMSI** (Function (within mass2adduct) to test spatial correlation between retrieved parent–adduct pairs in MSI data, validating adduct hypothesis) — https://github.com/kbseah/mass2adduct

## Examples

```
d.diff.DHBH2O <- diffGetPeaks(d.diff, mass=136.01600, mDa=1); d.diff.DHBH2O.corr <- corrPairsMSI(d, d.diff.DHBH2O)
```

## Evaluation signals

- The returned filtered massdiff object contains only ion pairs whose mass difference falls within the specified tolerance (mDa or ppm) of the target adduct mass; verify by checking min/max mass difference in output.
- The number of retrieved pairs is non-zero and reasonable given the size of the original dataset and the selectivity of the tolerance window.
- When passed to corrPairsMSI, the retrieved pairs show significant spatial correlation (p < 0.05 with Bonferroni correction by default) across the imaging pixels, supporting the true adduct hypothesis.
- Spot-checks: manually verify that at least a sample of the retrieved pairs have mass differences visually close to the target adduct mass when plotted on the histogram.
- The output massdiff object retains the original structure (parent mass A, adduct mass B, difference) with the same column names, confirming successful filtering rather than object corruption.

## Limitations

- The function depends on accurate specification of the tolerance window (mDa or ppm); a window that is too narrow may fail to retrieve true adducts (especially if the instrument has lower mass resolution than assumed), while a window that is too wide will retrieve spurious matches.
- Mass differences are inherently imprecise due to measurement error and uncertainty; the diffGetPeaks function does not account for instrumental mass calibration drift or systematic bias, so results may vary if the mass calibration changes between regions of the imaging dataset.
- The skill assumes that adduct masses are invariant across the dataset. In MALDI-MSI, adducts can form inconsistently depending on pixel-level chemistry (matrix concentration, salt content, local pH), so some true parent–adduct pairs may not be retrieved if they only occur in a subset of pixels.
- For very large datasets, even the filtered massdiff object may be large; subsequent correlation testing with corrPairsMSI may require the corrPairsMSIchunks variant to avoid memory exhaustion.

## Evidence

- [readme] Find mass peaks associated with specific mass difference: "Find parent and derivative mass peaks associated with a specific molecular adduct, e.g. DHB-H2O (mass 136.01600), within a window of 1 mDa, i.e. +/- 0.5 mDa."
- [readme] diffGetPeaks function retrieves subset of massdiff: "d.diff.DHBH2O <- diffGetPeaks(d.diff, mass=136.01600, mDa=1)"
- [readme] Correlation testing validates parent–adduct pairs: "Test for spatial correlations between mass peaks in MS imaging data (imported with the `msimat` function). For example, we wish to see if what we believe to be pairs of parent- and derivative-ion"
- [readme] Spatial correlation indicates true adduct formation: "If they are truly related by molecular adduct formation, then their abundances should be correlated."
- [readme] Output of diffGetPeaks is massdiff subset: "Output is a subset of the original `d.diff` object."
