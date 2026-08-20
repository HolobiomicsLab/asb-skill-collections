---
name: ion-trace-extraction-and-filtering
description: Use when you have CE-MS raw data (mzML or netCDF format) containing a known target analyte with a precise m/z value, and you need to isolate its signal within a defined effective mobility window (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MobilityTransformR
  - Spectra
  - xcms
  - MetaboCoreUtils
  - MSnbase
  - R
  techniques:
  - CE-MS
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("Spectra")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
- The MT of the peak will be determined by `findChromPeaks` from `xcms`.
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-trace-extraction-and-filtering

## Summary

Extract and filter ion traces from CE-MS raw data by m/z value and effective mobility window to isolate target analyte signals. This skill transforms raw electropherogram data into clean, mobility-resolved ion chromatograms suitable for peak detection and quantification.

## When to use

You have CE-MS raw data (mzML or netCDF format) containing a known target analyte with a precise m/z value, and you need to isolate its signal within a defined effective mobility window (e.g., 1000–2500 mm²/(kV·min)) to resolve it as a distinct peak and measure its retention time, intensity, and area on the mobility scale.

## When NOT to use

- Input data are already feature tables or pre-processed peak lists — use this skill only on raw electropherogram data.
- The target analyte m/z is unknown or poorly defined — ion trace extraction requires a precise mass value with specified tolerance.
- Your CE-MS system has not been calibrated or baseline-corrected — electroosmotic flow variations must be reliably characterized before mobility transformation.

## Inputs

- CE-MS raw data file in mzML or netCDF format
- Target analyte m/z value (e.g., 147.112806)
- Mass tolerance (ppm or absolute)
- Effective mobility window range (mm²/(kV·min))

## Outputs

- Extracted ion electropherogram (EIE) plotted on µeff axis
- Peak boundaries and retention time on µeff scale
- Data table with peak intensity and peak area
- Transformed CE-MS dataset with mobility-scale annotations

## How to apply

Load CE-MS raw data using Spectra or MSnbase, then apply effective mobility transformation to convert migration time to the µeff scale using MobilityTransformR (accounting for electroosmotic flow variations). Extract the ion trace for your target m/z (e.g., 147.112806 for Lysine) using xcms or MetaboCoreUtils with specified mass tolerance, then filter the extracted ion electropherogram to your mobility window of interest. Identify peak boundaries on the µeff axis and export the peak record (µeff-scale retention time, peak intensity, peak area) as a data table. The rationale is that effective mobility remains stable within a given electrophoretic system whereas migration times fluctuate; using the µeff scale produces highly reproducible peaks and enables reproducible cross-sample comparisons.

## Related tools

- **MobilityTransformR** (Transforms CE-MS migration time to effective mobility scale, accounting for electroosmotic flow variations) — https://github.com/LiesaSalzer/MobilityTransformR
- **Spectra** (Loads and manages CE-MS raw spectral data from mzML/netCDF files)
- **MSnbase** (Provides mass spectrometry data structures and handling for raw CE-MS data)
- **xcms** (Extracts ion traces and filters by m/z and mobility window)
- **MetaboCoreUtils** (Provides filtering and transformation utilities for metabolomics mass spectrometry data)

## Examples

```
# Load CE-MS data, transform to µeff scale, extract Lysine (m/z 147.112806) within 1000–2500 mm²/(kV·min), and export peak table
Library(MobilityTransformR); library(xcms)
mtx_data <- transformMobility(raw_data, eofCorrection=TRUE)
eie <- extractIon(mtx_data, mz=147.112806, ppm=5, mobRange=c(1000, 2500))
peaks <- findPeaks(eie, snthresh=5)
write.csv(peaks, 'lysine_peaks_ueff.csv')
```

## Evaluation signals

- Extracted ion electropherogram shows a single, well-defined peak (or expected multiplet) within the specified mobility window; peak boundaries are resolvable on the µeff axis.
- Peak retention time on µeff scale is consistent across replicate CE-MS runs of the same sample, demonstrating reproducibility inherent to the mobility scale.
- Peak intensity and area values are exported in a tabular format with matching µeff retention times and can be compared quantitatively across samples.
- Mass accuracy of the extracted m/z is within the specified tolerance (e.g., <5 ppm), confirming correct analyte identification.
- Effective mobility value falls within the expected range for the target compound in the given electrophoretic system; values outside typical ranges suggest transformation or calibration errors.

## Limitations

- Effective mobility transformation for CE-MS is not as straightforward as in CE-UV and requires careful handling of electroosmotic flow calibration.
- Peak resolution depends on the width of the effective mobility window; windows that are too narrow may exclude valid signal, while windows that are too broad may include background or co-migrating analytes.
- The skill requires a priori knowledge of the target analyte's m/z and approximate mobility; unknown or unexpected compounds may not be detected.
- Quality of the transformation depends on the accuracy of electroosmotic flow characterization within the CE-MS system; systematic EOF variations can degrade reproducibility.

## Evidence

- [other] Extract the ion trace for m/z 147.112806 with specified tolerance and filter to the mobility window 1000–2500 using xcms or MetaboCoreUtils.: "Extract the ion trace for m/z 147.112806 with specified tolerance and filter to the mobility window 1000–2500 using xcms or MetaboCoreUtils."
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] will result in highly reproducible peaks, which has already been shown in 2001: "will result in highly reproducible peaks, which has already been shown in 2001"
- [other] Apply effective mobility transformation to convert migration time to µeff scale using MobilityTransformR, accounting for electroosmotic flow variations.: "Apply effective mobility transformation to convert migration time to µeff scale using MobilityTransformR, accounting for electroosmotic flow variations."
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R"
