---
name: peak-detection-and-boundary-identification
description: Use when when you have CE-MS raw data (mzML or netCDF format) with extracted ion traces for target compounds and need to identify peak boundaries and extract quantitative peak properties (retention time on µeff scale, peak intensity, peak area) within a specified mobility window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-detection-and-boundary-identification

## Summary

Automated detection and localization of metabolite peaks on the effective mobility (µeff) scale in CE-MS data, with precise boundary identification to extract peak properties (intensity, area, migration position). This skill converts migration time-dependent electropherograms into mobility-normalized space where peaks become reproducible and comparable across runs despite electroosmotic flow variations.

## When to use

When you have CE-MS raw data (mzML or netCDF format) with extracted ion traces for target compounds and need to identify peak boundaries and extract quantitative peak properties (retention time on µeff scale, peak intensity, peak area) within a specified mobility window. Apply this skill after effective mobility transformation has been applied to the data, particularly when migration times show electroosmotic flow-induced fluctuations but you require stable, reproducible peak positions.

## When NOT to use

- Input data has not been transformed to the effective mobility scale; apply mobility transformation first.
- Migration time scale is acceptable for your analysis (e.g., single-run comparison); effective mobility is necessary only when comparing across multiple runs with varying electroosmotic flow.
- Extracted ion trace is already a processed feature table or quantified peak matrix; this skill is for raw signal detection, not post-processing.

## Inputs

- CE-MS raw data in mzML or netCDF format
- Effective mobility-transformed electropherogram data
- Extracted ion traces (EIC) for target m/z values with mass tolerance window
- Defined mobility window (e.g., 1000–2500 mm²/(kV·min))
- Peak detection parameters (e.g., signal-to-noise threshold, minimum peak width)

## Outputs

- Extracted ion electropherogram (EIE) chromatogram on µeff scale
- Peak boundary coordinates (start and end µeff positions)
- Data table with per-peak records: retention time on µeff scale, peak intensity, peak area
- Annotated peak list with resolved compound identities

## How to apply

Load the mobility-transformed CE-MS data and extract the ion trace for your target m/z with specified mass tolerance using xcms or MetaboCoreUtils. Restrict the extracted ion electropherogram to your defined mobility window (e.g., 1000–2500 mm²/(kV·min) for Lysine). Apply automated peak detection algorithms to identify peak boundaries on the µeff axis. For each detected peak, record the retention time position on the µeff scale, peak intensity (maximum signal), and integrated peak area. Validate that peaks are resolved as distinct entities within the mobility window and that peak boundaries do not overlap with background noise or adjacent peaks. Export peak records as a data table for downstream quantification or comparison.

## Related tools

- **MobilityTransformR** (Transforms CE-MS migration time data to effective mobility scale prior to peak detection) — https://github.com/LiesaSalzer/MobilityTransformR
- **xcms** (Filters and extracts ion traces within specified mobility windows; performs peak detection on chromatographic data)
- **MetaboCoreUtils** (Provides core metabolomics utilities for peak boundary identification and peak area/intensity extraction)
- **Spectra** (Loads and represents CE-MS spectral data in memory for efficient extraction and filtering)
- **MSnbase** (Legacy infrastructure for mass spectrometry data manipulation and chromatogram extraction)

## Examples

```
# After loading mobility-transformed data with MobilityTransformR:
# xcms::findChromPeaks(eic, param=CentWaveParam(mz=0.01)) to detect peaks,
# then extract peak table with xcms::chromPeaks() filtered to µeff range 1000–2500
```

## Evaluation signals

- Lysine (m/z 147.112806) or other target compound appears as a single resolved peak within the specified mobility window with no shoulder peaks or baseline noise intrusion.
- Peak boundaries are symmetrical or Gaussian-like in shape on the µeff scale; peak full width at half maximum (FWHM) is consistent within expected range for the capillary system.
- Peak intensity and area values are stable across replicate injections when plotted on the µeff scale, unlike migration time scale where they fluctuate due to electroosmotic flow.
- Exported peak records contain non-zero intensity and area; retention time on µeff scale falls within the declared mobility window and does not exceed system calibration bounds.
- No peaks are detected outside the declared mobility window; background signal between peaks is flat and below the signal-to-noise threshold used for detection.

## Limitations

- Peak detection accuracy depends on prior effective mobility transformation quality; systematic errors in µeff conversion will propagate to peak boundary errors.
- Overlapping peaks or co-eluting compounds within the mobility window may not be resolved as separate entities; Gaussian deconvolution is not addressed in the source workflow.
- The workflow assumes single-mode CE-MS (positive or negative); mixed-polarity data requires separate processing for positive and negative ions.
- Peak detection parameters (signal-to-noise threshold, minimum peak width) are not explicitly specified in the source workflow and must be optimized per analyte and system.
- Effective mobility remains stable only within the same electrophoretic system; instrument or buffer changes require re-calibration and may invalidate pre-existing µeff scales.

## Evidence

- [other] Extract the ion trace for m/z 147.112806 with specified tolerance and filter to the mobility window 1000–2500 using xcms or MetaboCoreUtils.: "Extract the ion trace for m/z 147.112806 with specified tolerance and filter to the mobility window 1000–2500 using xcms or MetaboCoreUtils."
- [other] Generate the extracted ion electropherogram and identify peak boundaries on the µeff axis.: "Generate the extracted ion electropherogram and identify peak boundaries on the µeff axis."
- [other] Export the peak record (retention time on µeff scale, peak intensity, peak area) as a data table.: "Export the peak record (retention time on µeff scale, peak intensity, peak area) as a data table."
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [intro] will result in highly reproducible peaks, which has already been shown in 2001: "Using effective mobility scale instead of migration time scale produces highly reproducible peaks"
