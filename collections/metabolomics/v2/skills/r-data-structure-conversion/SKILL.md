---
name: r-data-structure-conversion
description: Use when you have preprocessed MSI data in Cardinal format (post-peakBin) and need to apply mass2adduct's adduct-detection workflow, OR you have exported MSI intensity data as CSV from third-party software (SCiLS, MSiReader) and must convert it into a standardized R object for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3364
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - Cardinal
  - MSiReader
  - SCiLS
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
---

# Convert between R data structures for mass spectrometry imaging

## Summary

Convert mass spectrometry imaging data between different R object formats—namely Cardinal's MSProcessedImagingExperiment/MSContinuousImagingExperiment and mass2adduct's msimat format—to enable cross-tool interoperability while preserving peak-binned intensity information.

## When to use

You have preprocessed MSI data in Cardinal format (post-peakBin) and need to apply mass2adduct's adduct-detection workflow, OR you have exported MSI intensity data as CSV from third-party software (SCiLS, MSiReader) and must convert it into a standardized R object for downstream analysis of molecular adducts and spatial correlations.

## When NOT to use

- Your MSI data in Cardinal format has not yet been peak-binned; cardinal2msimat() requires the peakBin() step to have already been executed.
- Your CSV is not a plain-text, rectangular intensity matrix; msimat() assumes standard row (peaks) × column (pixel) layout with numeric intensities.
- You intend to preserve all pre-processing metadata and imaging coordinates beyond what msimat stores; msimat focuses on intensity values and mass labels, not full experimental provenance.

## Inputs

- Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (post-peakBin, pre-process)
- ImzML file (via Cardinal readImzML)
- CSV file exported from MSiReader or SCiLS (plain-text, intensity-export format)
- Plain-text file of mass values (one per line, for simple numeric vector input)

## Outputs

- msimat object (mass2adduct class with intensity matrix, mass vector, and pixel coordinates)
- R data.frame representation of MSI intensity data
- Standard R histogram object (when hist() is applied to massdiff output)

## How to apply

Load your MSI data using the appropriate source-specific function: use Cardinal's `readImzML()` followed by the standard preprocessing pipeline (normalize, smoothSignal, reduceBaseline), apply `peakBin()` with a pre-existing peaklist, then call `process()` to finalize the MSProcessedImagingExperiment object. Then convert directly to msimat format using the `cardinal2msimat()` function from mass2adduct. Alternatively, if starting from CSV (e.g., from SCiLS or MSiReader intensity export), load it directly using `msimat("filename.csv", sep=";")`, which creates a msimat object with explicit mass, pixel, and intensity columns. The choice of conversion path depends on your starting format: Cardinal objects require intermediate preprocessing before conversion; CSV files require only separator specification. Verify correct conversion by comparing mass spectra plots between the original and converted objects using `plot()`—they should be visually identical.

## Related tools

- **Cardinal** (Source MSI data format; used for preprocessing (normalize, smoothSignal, reduceBaseline, peakBin) before conversion to msimat) — http://cardinalmsi.org/
- **mass2adduct** (Target R package containing msimat class and cardinal2msimat() conversion function) — https://github.com/kbseah/mass2adduct
- **MSiReader** (Source software for exporting MSI intensity data as CSV; output can be imported via msimat())
- **SCiLS** (Source software for exporting MSI intensity data as CSV; output can be imported via msimat())
- **R** (Runtime environment for executing conversion functions and handling data structures)

## Examples

```
d_peaks <- readImzML("msi_file") %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process; d_msimat <- cardinal2msimat(d_peaks); plot(d_msimat)
```

## Evaluation signals

- Mass spectra plots from the original object and the converted msimat object are visually identical when rendered with plot()—same peak heights, positions, and relative intensities.
- The msimat object has three internal elements: mass vector, intensity matrix, and pixel coordinate mapping; verify structure with str() or class() returning 'msimat'.
- Downstream operations (e.g., massdiff, corrPairsMSI) execute without error and produce expected dimensionality—massdiff() returns a data.frame with three columns (parent mass A, adduct mass B, difference).
- Object size in memory is reasonable relative to the input dataset dimensions; if using triplet format for large matrices, verify with object.size() that redundant zeroes have been eliminated.
- No NaN, Inf, or unexpected NA values appear in the mass or intensity vectors after conversion.

## Limitations

- Cardinal conversion (cardinal2msimat) requires Cardinal ≥ 2.2 and the data must already be peak-binned; raw or partially processed Cardinal objects will fail or produce incorrect results.
- CSV import via msimat() assumes rectangular matrix format (peaks as rows, pixels as columns); ragged or transposed matrices require manual reformatting before import.
- Very large CSV files (several GB) may exceed available RAM even when using the triplet-format Perl script (msimunging.pl); no automatic chunking is applied during msimat() import—users must pre-filter or reformat offline.
- The msimat format does not preserve all Cardinal metadata (e.g., instrument parameters, full processing history); conversion is lossy in terms of provenance.
- If using the triplet format (rows, cols, vals, peaks, spots files) generated by msimunging.pl, all five files must be present and consistent; missing or corrupted files will cause msimat() to fail.

## Evidence

- [readme] Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to msimat format: "Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format."
- [readme] Data must be preprocessed and peak-binned before conversion: "However, the data must first be pre-processed, with peaks already binned with the `peakBin()` function from Cardinal."
- [readme] CSV files from third-party MSI software are imported via msimat with separator specification: "MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format)."
- [readme] msimat function loads data into R as a data.frame with specific class: "Import the data into R as a data.frame: d <- msimat("msi.csv", sep=";") class(d) # "msimat""
- [readme] Converted objects can be validated by comparing plots from source and target formats: "Compare peak histograms from Cardinal vs mass2adduct, should look the same plot(d_peaks) plot(d_msimat)"
- [readme] Large CSV files can be converted to triplet format offline using a Perl script: "A Perl script `msimunging.pl` (in the `inst/` subdirectory of the package source) is provided to do this format conversion before importing the files into R."
