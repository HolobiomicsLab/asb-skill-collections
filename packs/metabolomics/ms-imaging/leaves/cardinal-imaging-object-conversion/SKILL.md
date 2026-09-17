---
name: cardinal-imaging-object-conversion
description: Use when you have mass spectrometry imaging data in Cardinal format (versions
  2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3173
  tools:
  - Cardinal
  - mass2adduct
  - R
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment`
  or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat`
  format
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

# cardinal-imaging-object-conversion

## Summary

Convert Cardinal MSI data objects (MSProcessedImagingExperiment or MSContinuousImagingExperiment) to mass2adduct's msimat format to enable downstream adduct detection and spatial correlation analysis. This skill bridges the Cardinal preprocessing ecosystem to mass2adduct's adduct identification pipeline.

## When to use

You have mass spectrometry imaging data in Cardinal format (versions 2.2 and above), already preprocessed with peak binning via Cardinal's peakBin() function, and you want to identify molecular adducts and test their spatial correlation using mass2adduct's massdiff() and adductMatch() functions.

## When NOT to use

- Input data has not been peak-binned with Cardinal's peakBin() function; conversion requires pre-binned peak lists.
- You are using Cardinal version < 2.2; cardinal2msimat() requires Cardinal ≥ 2.2 API compatibility.
- Data is already in msimat format or imported from CSV via msimat(); conversion is unnecessary.

## Inputs

- Cardinal MSProcessedImagingExperiment object (post-peakBin, version ≥2.2)
- Cardinal MSContinuousImagingExperiment object (post-peakBin, version ≥2.2)

## Outputs

- msimat object (containing binned mass list and pixel-wise intensity matrix)
- msimat S3 object compatible with mass2adduct functions (massdiff, adductMatch, corrPairsMSI)

## How to apply

Load a Cardinal ImzML file and apply Cardinal's preprocessing chain (normalize, smoothSignal, reduceBaseline, peakBin with an existing peaklist, and process). Pass the resulting MSProcessedImagingExperiment or MSContinuousImagingExperiment object to cardinal2msimat() to convert it to msimat format, which stores mass and pixel intensity data in a structure compatible with mass2adduct. The conversion preserves the spatial intensity information needed for downstream spatial correlation testing. Verify the conversion by comparing mass spectra plots from both the original Cardinal object and the resulting msimat object—they should be visually identical. The msimat object can then be piped directly into massdiff() to calculate all pairwise mass differences.

## Related tools

- **Cardinal** (Preprocesses and peak-bins MSI data from ImzML; provides MSProcessedImagingExperiment and MSContinuousImagingExperiment objects that serve as input to cardinal2msimat()) — http://cardinalmsi.org/
- **mass2adduct** (Consumes msimat objects output by cardinal2msimat() for adduct identification via massdiff() and adductMatch(); performs spatial correlation testing via corrPairsMSI()) — https://github.com/kbseah/mass2adduct

## Examples

```
d <- readImzML("msi_file"); d_peaks <- d %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process; d_msimat <- cardinal2msimat(d_peaks)
```

## Evaluation signals

- Mass spectrum plots from Cardinal object and converted msimat object are visually identical (same peak intensities and distribution).
- msimat object has class 'msimat' and contains three elements: peak masses (numeric vector), pixel coordinates (data.frame), and intensity matrix (numeric matrix).
- massdiff(msimat_object) executes without error and returns a massdiff object with expected number of pairwise differences.
- Pixel dimensions and mass axis ranges match between the original Cardinal object and the msimat object.
- downstream corrPairsMSI() and adductMatch() functions accept the msimat object without format-related errors.

## Limitations

- The data must be pre-processed and peak-binned before conversion; cardinal2msimat() does not perform normalization, baseline subtraction, or peak detection itself.
- Cardinal version 2.2 or later is required; earlier versions lack compatible MSProcessedImagingExperiment and MSContinuousImagingExperiment classes.
- Conversion assumes the Cardinal object has been fully processed; raw or partially processed experiments may not convert correctly or may produce uninformative results downstream.
- The msimat format discards metadata (e.g., instrument parameters, ion mode, acquisition settings) present in the original Cardinal object; only mass and intensity data are retained.

## Evidence

- [readme] Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects can be converted to mass2adduct's msimat format: "Cardinal `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's `msimat` format"
- [readme] Peak binning is a prerequisite for cardinal2msimat() conversion: "the data must first be pre-processed, with peaks already binned with the `peakBin()` function from Cardinal"
- [readme] Complete preprocessing workflow before conversion: "d_peaks <- d %>% normalize() %>% smoothSignal() %>% reduceBaseline() %>% peakBin(peaklist) %>% process"
- [readme] Verification approach by visual comparison of mass spectra: "Compare peak histograms from Cardinal vs mass2adduct, should look the same"
- [methods] cardinal2msimat() function enables the pipeline: "If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format"
