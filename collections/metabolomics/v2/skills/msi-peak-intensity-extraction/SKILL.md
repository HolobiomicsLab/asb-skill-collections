---
name: msi-peak-intensity-extraction
description: Use when you have MSI intensity data exported from commercial software (MSiReader, SCiLS) or Cardinal processing pipelines as plain-text CSV files or Cardinal MSProcessedImagingExperiment/MSContinuousImagingExperiment objects, and you need to prepare it for mass-difference tabulation and adduct.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mass2adduct
  - R
  - Cardinal
  - MSiReader
  - SCiLS
  - msimunging.pl
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

# MSI Peak Intensity Extraction

## Summary

Extract and import mass spectrometry imaging (MSI) intensity matrices from vendor software exports or third-party formats into a standardized msimat object for downstream adduct analysis. This skill converts raw MSI data into a uniform computational representation suitable for pairwise mass-difference calculations and spatial correlation testing.

## When to use

You have MSI intensity data exported from commercial software (MSiReader, SCiLS) or Cardinal processing pipelines as plain-text CSV files or Cardinal MSProcessedImagingExperiment/MSContinuousImagingExperiment objects, and you need to prepare it for mass-difference tabulation and adduct identification in mass2adduct. Use this when your input is a two-dimensional matrix of pixel locations (rows, columns) and measured ion intensities across a defined m/z peak list.

## When NOT to use

- Your MSI data has not been peak-binned or has not undergone baseline removal and smoothing (use Cardinal pre-processing first).
- You have only a simple list of m/z values without pixel location or intensity information (use scan() to import as numeric vector instead).
- Your vendor format is binary (e.g., imzML or Bruker .d folders); convert to CSV export or use Cardinal's readImzML() first.

## Inputs

- CSV file exported from MSiReader or SCiLS (plain-text, comma- or semicolon-delimited, rows=pixels, columns=m/z peaks, values=ion intensities)
- Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (v2.2+, pre-processed with peakBin())
- Triplet format files: rows, cols, vals, peaks, spots (from msimunging.pl conversion of large CSV files)

## Outputs

- msimat object (R S3 object of class 'msimat' with matrix structure and metadata)
- Summary printout showing pixel count, peak count, and intensity range
- Mass spectrum plot of total intensities per peak across all pixels

## How to apply

Import the MSI intensity data using the msimat() constructor, specifying the CSV file path and appropriate field separator (typically ';' or ',') to parse vendor exports. If working with large files (several GB) that exceed available RAM, use the msimunging.pl Perl script to convert to triplet format (rows, cols, vals, peaks, spots files) before importing, which conserves memory by discarding zero entries. For Cardinal objects, first pre-process and peak-bin the data using peakBin(), then convert using cardinal2msimat(). Validate the import by plotting the resulting msimat object to confirm the mass spectrum matches the original vendor output; discrepancies indicate parsing errors or format incompatibilities. The output msimat object is then passed directly to massdiff() for pairwise mass-difference calculation.

## Related tools

- **mass2adduct** (Primary package providing msimat() constructor and downstream massdiff/corrPairsMSI workflow) — https://github.com/kbseah/mass2adduct
- **Cardinal** (Pre-processing and peak-binning of raw MSI data; provides MSProcessedImagingExperiment objects convertible to msimat via cardinal2msimat())
- **MSiReader** (Vendor software for exporting MSI intensity matrices as CSV files for import into msimat())
- **SCiLS** (Vendor software for exporting MSI intensity matrices as CSV files for import into msimat())
- **msimunging.pl** (Perl script for converting large CSV files to triplet format (rows, cols, vals, peaks, spots) to reduce memory footprint before msimat import)

## Examples

```
d <- msimat("msi.csv", sep=";"); class(d); print(d); plot(d)
```

## Evaluation signals

- msimat object class is confirmed with class(d) == 'msimat'.
- Mass spectrum plot from plot(d) matches the total-intensity spectrum from the vendor software or Cardinal output (same peak heights and m/z positions).
- Pixel count and peak count printed by print(d) match the source data dimensions (rows = spatial pixels, columns = m/z peaks).
- No NA or NaN values are present in the intensity matrix except where expected (e.g., pixels outside the tissue region).
- Downstream massdiff(d) executes without error and produces a data.frame with non-zero mass differences, confirming matrix integrity.

## Limitations

- Large CSV files (several GB) may exceed available RAM during direct import; msimunging.pl conversion is essential for datasets exceeding ~32 GB system memory, but the script itself may also fail if the input file size approaches available RAM.
- Cardinal conversion requires pre-processed objects with peakBin() already applied; raw Cardinal objects will not convert correctly.
- The msimat() function assumes rectangular matrix structure; irregular or sparse pixel layouts from non-rectangular MSI acquisitions may require manual matrix padding.
- No built-in support for alternative vendor formats (Bruker .d, Waters .raw); users must export to CSV or use intermediate conversion tools (Cardinal, MSConvert).

## Evidence

- [readme] CSV format and import method: "MSI data exported from the MSiReader software with the "intensity export" function, or from some other third party software that can output plain-text comma-delimited tables (CSV format)"
- [readme] msimat constructor and validation: "d <- msimat("msi.csv", sep=";"); class(d) # "msimat"; print(d) # Report a summary; plot(d) # Mass spectrum of total intensities per peak"
- [readme] Large file handling via triplet format: "If the data matrix is very large, consider reformatting it... Conversion to triplet format output gives five files, which correspond to the inputs required by the msimat() function in the R package -"
- [readme] Cardinal object conversion: "Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's msimat format... d_msimat <-"
- [readme] Memory efficiency rationale: "For many MSI data sets, a lot of this is "wasted" because the majority of peaks are only detected in a minority of pixels... the data can be represented in a "triplet" format rather than matrix"
