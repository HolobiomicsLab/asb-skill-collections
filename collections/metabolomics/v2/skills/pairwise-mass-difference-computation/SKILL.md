---
name: pairwise-mass-difference-computation
description: Use when after loading preprocessed MSI intensity data (via msimat from CSV export) or a simple numeric vector of mass peak values, when you need to discover which masses in your dataset co-vary as parent–adduct pairs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - msimat
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

# Pairwise mass-difference tabulation from MSI data

## Summary

Compute all possible pairwise mass differences from an MSI data matrix to identify potential molecular adducts. This is the foundational step in mass spectrometry imaging adduct detection, transforming a peak list into a complete difference matrix for downstream binning and annotation.

## When to use

After loading preprocessed MSI intensity data (via msimat from CSV export) or a simple numeric vector of mass peak values, when you need to discover which masses in your dataset co-vary as parent–adduct pairs. Apply this skill before binning differences into a histogram, especially when matrix or salt ion adducts are suspected in your MALDI-MSI experiment.

## When NOT to use

- Input is a single mass value or fewer than two masses—massdiff requires at least two distinct masses to compute pairs.
- You already possess a pre-computed adduct table or difference matrix from external software; re-computing will be redundant.
- Your masses are not from the same acquisition instrument or have inconsistent precision/calibration, risking spurious pairwise matches.

## Inputs

- msimat object (preprocessed MSI data matrix from CSV file with peak intensities across pixels)
- numeric vector of mass values (simple list of m/z peaks, no intensity data)

## Outputs

- massdiff object (data.frame with columns: parent_mass, adduct_mass, mass_difference)
- massdiff data.frame (three columns: the two parent masses and the difference between them)

## How to apply

Load your MSI data into R as an msimat object (from a CSV file with specified separator, e.g., sep=';') or supply a numeric vector of mass values. Call the massdiff() function on this input; it enumerates all possible pairs of masses and computes the mass difference for each pair. The output is a data.frame-class massdiff object with three columns: parent ion A, adduct ion B, and their mass difference. These differences represent putative molecular adducts and will be binned into a histogram (typically using a bin width matching your instrument's mass precision, often ±0.01 Da) in the subsequent workflow step. The rationale is that systematic mass differences appearing many times across the peak list signal genuine adduct relationships rather than random noise.

## Related tools

- **mass2adduct** (R package that implements massdiff() function to compute pairwise mass differences from MSI data matrices and provides downstream adduct identification pipeline) — https://github.com/kbseah/mass2adduct
- **msimat** (Function within mass2adduct to load and parse MSI intensity data from CSV files (exported from MSiReader or SCiLS) into R data.frame format) — https://github.com/kbseah/mass2adduct
- **Cardinal** (Optional R package for pre-processing MSI data; MSProcessedImagingExperiment and MSContinuousImagingExperiment objects can be converted to msimat format via cardinal2msimat())
- **R** (Host language and environment for executing massdiff and subsequent analytical functions)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff)
```

## Evaluation signals

- Output massdiff object has exactly three columns (parent_mass, adduct_mass, mass_difference) and number of rows equals n*(n-1)/2 where n is the number of input masses
- All values in the mass_difference column are numeric, non-negative (or follow expected mass shift direction), and within a biologically plausible range (typically ±500 Da for common adducts)
- Subsequent histogram binning (hist(d.diff)) produces a distribution with recognizable peaks at known adduct mass windows (e.g., 18.01 Da for H₂O loss, 136.02 Da for DHB-H₂O)
- topAdducts() function on the binned histogram returns matches to reference adducts (from the built-in adducts or adducts2 datasets) with non-zero occurrence counts for abundant mass differences
- corrPairsMSI() test on identified parent–adduct pairs shows statistically significant spatial correlations (p < 0.05 after Bonferroni correction) in the imaging data, validating that pairs are not spurious

## Limitations

- Computational complexity scales as O(n²) with number of input masses; for very large peak lists (hundreds or thousands), memory usage and runtime become prohibitive. The package provides msimunging.pl (Perl script) to convert large CSV files to triplet format for more efficient storage and processing.
- Mass measurement error and instrumental precision are not intrinsically modeled during massdiff computation; differences must be binned post-hoc with a user-specified bin width matching the known mass accuracy of the instrument (e.g., ±0.01 Da for high-resolution MS). Choosing an inappropriate bin width will obscure or fragment genuine adduct signals.
- The function treats all mass differences equally without weighting by peak abundance or spatial coherence in the MSI dataset; spurious pairwise differences from low-intensity noise peaks will be counted alongside high-confidence adduct pairs. Filtering or weighting by intensity before massdiff() computation can mitigate this.
- No changelog or version tracking is provided in the package repository, limiting reproducibility auditing and traceability of methodological changes across versions.

## Evidence

- [other] massdiff-computes-pairwise-masses: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [other] massdiff-returns-dataframe: "d.diff <- massdiff(d) # Returns object of classes data.frame and massdiff"
- [other] msimat-import-csv: "d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";")"
- [intro] adducts-form-from-matrix-salt: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [readme] massdiff-output-structure: "Output is a `massdiff` object with three elements: the two parent masses and the difference between them."
- [readme] bin-width-precision-dependency: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [readme] large-file-handling: "Plain-text CSV files of MSI data exported by software such as SCILS or MSIreader can be large, on the order of several Gb. For many MSI data sets, a lot of this is "wasted" because the majority of"
