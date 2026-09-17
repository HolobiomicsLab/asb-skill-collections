---
name: msi-data-format-interoperability
description: Use when your MSI data is stored in a Cardinal imaging experiment object
  (version 2.2+) that has already been peak-binned with peakBin(), and you want to
  run mass2adduct's massdiff() and adductMatch() pipeline without manually exporting
  to CSV;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mass2adduct
  - R
  - Cardinal
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
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

# Convert Cardinal MSI Objects to mass2adduct-Compatible Format

## Summary

Converts Cardinal's MSProcessedImagingExperiment or MSContinuousImagingExperiment objects to the msimat matrix format required by downstream mass2adduct analysis, enabling seamless integration of Cardinal-preprocessed MSI data into adduct detection pipelines.

## When to use

Your MSI data is stored in a Cardinal imaging experiment object (version 2.2+) that has already been peak-binned with peakBin(), and you want to run mass2adduct's massdiff() and adductMatch() pipeline without manually exporting to CSV; or your workflow already uses Cardinal for preprocessing and you wish to avoid intermediate file I/O.

## When NOT to use

- Your MSI data has not yet been peak-binned; cardinal2msimat() requires processed Cardinal objects with a defined peaklist, not raw imaging experiments.
- You are importing MSI data from non-Cardinal sources (e.g., MSiReader, SCiLS); use the CSV-based msimat() function instead.
- You only need to extract m/z values without pixel intensity information; use scan() on a plain-text mass list instead.

## Inputs

- Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (version 2.2+)
- Must be pre-processed with peak binning (peakBin() applied)
- ImzML or vendor-native MSI file loaded via readImzML()

## Outputs

- msimat object (mass intensity matrix with classes 'msimat' and 'data.frame')
- Rows represent m/z peaks, columns represent image pixels
- Preserves intensity values for downstream spatial correlation tests

## How to apply

After preprocessing your Cardinal object with normalize(), smoothSignal(), reduceBaseline(), peakBin(peaklist), and process(), pass the resulting MSProcessedImagingExperiment or MSContinuousImagingExperiment object to cardinal2msimat(). This function extracts the peak intensities and spatial coordinates, reformatting them into the msimat class (a matrix where rows are m/z values and columns are pixel locations). Verify the conversion succeeded by comparing the peak histogram from the original Cardinal object (plot(d_peaks)) with the msimat histogram (plot(d_msimat))—they should be visually identical. The output msimat object is then ready for massdiff() to compute all pairwise mass differences across pixels.

## Related tools

- **Cardinal** (Preprocesses raw MSI data (normalize, smooth, reduce baseline, peak bin) before format conversion) — http://cardinalmsi.org/
- **mass2adduct** (Receives msimat output to compute pairwise mass differences and match adducts) — https://github.com/kbseah/mass2adduct
- **R** (Execution environment; required for loading Cardinal and running cardinal2msimat())

## Examples

```
d <- readImzML("msi_file"); d_peaks <- d %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process(); d_msimat <- cardinal2msimat(d_peaks); d.diff <- massdiff(d_msimat)
```

## Evaluation signals

- Output object has class 'msimat' and can be printed with standard R print() to show row (m/z) and column (pixel) dimensions.
- Peak histogram from converted msimat (plot(d_msimat)) matches the histogram from the original Cardinal object (plot(d_peaks)) visually and quantitatively (same peak positions and relative heights).
- Intensity values are preserved: spot-check several m/z peaks by comparing intensity profiles in Cardinal vs. msimat using indexing (e.g., d_msimat[1, 1:10]).
- The msimat object is compatible with downstream mass2adduct functions: massdiff(d_msimat) runs without error and returns a massdiff object.
- Spatial dimensions match: number of columns in msimat equals the total number of pixels in the original Cardinal imaging experiment.

## Limitations

- Requires Cardinal version 2.2 or later; earlier versions lack MSProcessedImagingExperiment and MSContinuousImagingExperiment classes.
- Data must be pre-processed and peak-binned before conversion; raw, unpeak-binned Cardinal objects cannot be converted.
- Large MSI datasets (hundreds of thousands of peaks × millions of pixels) may consume significant memory even after conversion; consider sparse triplet format for very large files (via msimunging.pl).
- The conversion preserves only intensity information and peak lists; metadata such as scan times, instrument parameters, or custom annotations in the Cardinal object are not transferred to msimat.

## Evidence

- [readme] Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format. However, the data must first be pre-processed, with peaks already binned with the `peakBin()` function from Cardinal.: "Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format. However, the data must first"
- [methods] If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format: "If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format"
- [readme] Compare peak histograms from Cardinal vs mass2adduct, should look the same: "Compare peak histograms from Cardinal vs mass2adduct, should look the same"
- [readme] Pre-process and peak bin with existing peaklist: d_peaks <- d %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process; Convert to msimat format for mass2adduct: d_msimat <- cardinal2msimat(d_peaks): "d_peaks <- d %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process; d_msimat <- cardinal2msimat(d_peaks)"
- [methods] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
