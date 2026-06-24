---
name: msi-data-matrix-import-and-validation
description: Use when you have MSI intensity data exported from MSiReader, SCiLS,
  or Cardinal as plain-text CSV files or as Cardinal MSProcessedImagingExperiment/MSContinuousImagingExperiment
  objects, and need to load it into R as a validated msimat object for mass difference
  and adduct analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - mass2adduct
  - R
  - Cardinal
  - msimunging.pl
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS
  data
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSI Data Matrix Import and Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Import mass spectrometry imaging (MSI) intensity data from CSV or Cardinal objects into R and validate the resulting matrix representation. This skill ensures data integrity and correct format conversion before downstream adduct detection and correlation analysis.

## When to use

You have MSI intensity data exported from MSiReader, SCiLS, or Cardinal as plain-text CSV files or as Cardinal MSProcessedImagingExperiment/MSContinuousImagingExperiment objects, and need to load it into R as a validated msimat object for mass difference and adduct analysis.

## When NOT to use

- Input data is already in msimat format or pre-loaded into R memory—skip import and proceed directly to massdiff().
- You have only a plain list of masses (no pixel intensity information) and do not need spatial correlation testing—use scan() directly instead.
- Data originates from non-imaging mass spectrometry (e.g., bulk liquid chromatography–mass spectrometry) with no spatial coordinates—this skill is specific to MSI.

## Inputs

- CSV file exported from MSiReader or SCiLS with intensity matrix (mass × pixel)
- Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (v2.2+, pre-processed with peakBin())
- Triplet format files (rows, cols, vals, peaks, spots) from msimunging.pl conversion

## Outputs

- msimat object (S3 class inheriting from data.frame) with mass spectrum and intensity matrix
- Validated mass spectrum plot showing total intensity per peak

## How to apply

Use the msimat() function to import CSV data with appropriate separator (typically semicolon for European-formatted exports). Specify the file path and sep parameter matching your file format. For Cardinal objects, pre-process with peakBin() first, then convert using cardinal2msimat(). After import, validate by inspecting the object class (should be 'msimat'), printing the summary, and comparing the resulting mass spectrum plot to the original to ensure no data corruption. For very large CSV files (several gigabytes), consider reformatting to triplet format using the provided msimunging.pl Perl script before import to avoid memory overflow.

## Related tools

- **mass2adduct** (R package providing msimat() import function, msimat class definition, and validation methods for MSI data) — https://github.com/kbseah/mass2adduct
- **Cardinal** (R package for preprocessing MSI data; data objects convertible to msimat format via cardinal2msimat()) — http://cardinalmsi.org/
- **msimunging.pl** (Perl script bundled in mass2adduct inst/ folder for reformatting large CSV files to triplet format before import) — https://github.com/kbseah/mass2adduct

## Examples

```
d <- msimat(system.file("extdata","msi.csv",package="mass2adduct"),sep=";"); class(d); print(d); plot(d)
```

## Evaluation signals

- Returned object has class 'msimat' (verify with class(d))
- print(d) produces a summary report with expected number of peaks and pixels
- plot(d) generates a mass spectrum matching the original instrument output or software visualization
- For Cardinal imports: mass spectrum from cardinal2msimat() matches plot of pre-processed Cardinal object
- For triplet imports: data reconstruction is lossless (compare sum of intensities or histogram with original CSV)

## Limitations

- CSV files must be exported from known sources (MSiReader, SCiLS) in plain-text format; other proprietary formats may fail.
- Cardinal conversion requires pre-processing with peakBin() and Cardinal v2.2+; earlier versions unsupported.
- For very large CSV files (>RAM capacity), msimunging.pl conversion is necessary but may still fail if file exceeds total system memory.
- Triplet format conversion with msimunging.pl is limited by available RAM; conversion of 40 Gb CSV on 32 Gb system unlikely to succeed.
- No built-in handling for missing data or NaN values; these should be imputed or filtered before import.

## Evidence

- [readme] MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format).: "MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format)"
- [readme] If the data matrix is very large, consider reformatting it: "If the data matrix is very large, consider reformatting it (see "Reformatting large CSV files" below). Import the data into R as a data.frame: d <- msimat("msi.csv", sep=";")"
- [readme] Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to mass2adduct's msimat format. However, the data must first be pre-processed, with peaks already binned with the peakBin() function from Cardinal.: "Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format. However, the data must first"
- [other] Load the example MSI data (msi.csv) from inst/extdata using the msimat() function with appropriate separator (semicolon).: "Load the example MSI data (msi.csv) from inst/extdata using the msimat() function with appropriate separator (semicolon)"
- [readme] Plain-text CSV files of MSI data exported by software such as SCILS or MSIreader can be large, on the order of several Gb. For many MSI data sets, a lot of this is "wasted" because the majority of peaks are only detected in a minority of pixels.: "Plain-text CSV files of MSI data exported by software such as SCILS or MSIreader can be large, on the order of several Gb. For many MSI data sets, a lot of this is "wasted" because the majority of"
