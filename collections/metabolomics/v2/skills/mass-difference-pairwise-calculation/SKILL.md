---
name: mass-difference-pairwise-calculation
description: Use when after importing MSI data as an msimat object and having a list of detected peak masses, but before annotating which mass differences correspond to biologically plausible adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - msimat
  - SCiLS
  - MSiReader
  techniques:
  - MS-imaging
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

# mass-difference-pairwise-calculation

## Summary

Compute all pairwise mass differences between detected peaks in mass spectrometry imaging data to identify candidate molecular adducts. This step generates a comprehensive map of mass gaps that may correspond to known chemical transformations (e.g., matrix or salt ion attachment).

## When to use

Apply this skill after importing MSI data as an msimat object and having a list of detected peak masses, but before annotating which mass differences correspond to biologically plausible adducts. Use when your goal is to exhaustively enumerate all possible molecular modifications present in the sample, or when you need to identify unexpected mass shifts that may indicate novel adducts or modifications.

## When NOT to use

- Input is a single mass value or fewer than two distinct peaks—pairwise comparison requires at least two peaks.
- You have already matched mass differences to known adducts and only want to filter by statistical significance—use corrPairsMSI() or topAdducts() instead.
- Your data are already annotated with explicit parent–adduct relationships from external metadata—this skill generates de novo candidates and is redundant if relationships are pre-assigned.

## Inputs

- msimat object (MSI intensity matrix with row names as mass-to-charge ratios)
- numeric vector of peak masses (alternative to msimat)

## Outputs

- massdiff object: data.frame with columns for mass1, mass2, and difference
- massdiffhist object: binned histogram of mass difference frequencies

## How to apply

Call the massdiff() function on your msimat object or numeric vector of peak masses to generate all possible pairwise combinations and their mass differences. The function returns a massdiff object (subclass of data.frame) containing three columns: the two parent masses and their difference. The output is unfiltered at this stage—it includes all possible pairs, even those with very low occurrence counts or biologically implausible differences. Bin the resulting mass differences into a histogram with a user-specified bin width (typically 0.01 Da for high-resolution instruments) to account for measurement error and uncertainty. This binning step is essential because raw mass differences are artificially precise and cannot be reliably compared to reference adduct values without collapsing nearby values into common bins.

## Related tools

- **mass2adduct** (R package that implements massdiff() and hist() functions for pairwise mass difference calculation and binning) — https://github.com/kbseah/mass2adduct
- **msimat** (Function to import MSI data from CSV format into R; output is input to massdiff()) — https://github.com/kbseah/mass2adduct
- **SCiLS** (MSI instrument control and analysis software; outputs CSV format readable by msimat())
- **MSiReader** (MSI data export tool; outputs plain-text CSV files compatible with mass2adduct workflow)

## Examples

```
d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff)
```

## Evaluation signals

- massdiff object is returned with three columns (mass1, mass2, difference); row count equals n*(n-1)/2 for n peaks
- massdiffhist histogram shows expected distribution of mass gaps; peaks in histogram align with known adduct reference masses after visual inspection or quantile matching
- Bin width is appropriate for instrument precision; typical value is 0.01 Da for high-resolution MS—verify this matches your instrument's mass accuracy specification
- No missing or NaN values in the difference column; all pairwise differences are finite and positive (or optionally, absolute values if direction does not matter)
- Downstream adductMatch() or topAdducts() calls on the histogram produce plausible matches (e.g., common ion attachments like [M+Na]+, [M+K]+, [M-H2O]+

## Limitations

- Computational complexity is O(n²) in the number of peaks; for datasets with hundreds or thousands of peaks, memory and runtime may become prohibitive. Use chunked processing (corrPairsMSIchunks) for very large datasets.
- Bin width selection is user-dependent and affects the histogram appearance and subsequent adduct matching. Too narrow bins preserve false-positive differences; too wide bins merge distinct adducts. No automated bin-width selection is provided; instrument mass accuracy must be known in advance.
- The massdiff object contains all pairwise differences without regard to occurrence frequency or biological plausibility. High-count spurious mass gaps (e.g., from noise or instrumental artifacts) are not filtered at this stage and may lead to false-positive adduct identifications downstream.
- If input is a simple numeric vector rather than msimat, spatial intensity information is lost; subsequent correlation testing with corrPairsMSI() cannot be performed.

## Evidence

- [readme] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] Output is a massdiff object with three elements: the two parent masses and the difference between them.: "Output is a massdiff object with three elements: the two parent masses and the difference between them."
- [methods] d.diff <- massdiff(d) # Returns object of classes data.frame and massdiff: "d.diff <- massdiff(d) # Returns object of classes data.frame and massdiff"
- [other] The following function generates all pairwise mass differences using massdiff() to create a massdiff object.: "Generate all pairwise mass differences using massdiff() to create a massdiff object."
