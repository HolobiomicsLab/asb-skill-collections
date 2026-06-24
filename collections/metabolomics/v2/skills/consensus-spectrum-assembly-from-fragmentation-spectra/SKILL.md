---
name: consensus-spectrum-assembly-from-fragmentation-spectra
description: Use when you have detected a single chromatographic peak in DDA LC-MS/MS
  data that generated multiple MS2 fragmentation spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Spectra
  - MsBackendMgf
  - MsFeatures
  - xcms
  techniques:
  - LC-MS
  - CE-MS
  license_tier: open
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- library(Spectra)
- library(MsBackendMgf)
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")`
  package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# consensus-spectrum-assembly-from-fragmentation-spectra

## Summary

Combine multiple MS2 fragmentation spectra acquired from the same chromatographic peak into a single consensus spectrum to improve signal-to-noise ratio and enable robust spectral matching against reference databases. This skill is essential when DDA LC-MS/MS data yields multiple scans of the same precursor ion, allowing aggregation of fragment intensities across scans to create a higher-confidence spectrum for compound annotation.

## When to use

Apply this skill when you have detected a single chromatographic peak in DDA LC-MS/MS data that generated multiple MS2 fragmentation spectra (e.g., from repeated fragmentation or multiple scan events at the same m/z and retention time), and you need a single high-confidence spectrum for database matching or annotation. Typical triggers: chromPeakSpectra() returns more than one MS2 spectrum for a single peak, or you observe weak individual MS2 scans that need aggregation to improve match scores against reference spectra like those in Metlin.

## When NOT to use

- Input is a single MS2 scan or spectrum — consensus assembly requires multiple spectra from the same peak; a single scan should be matched directly.
- Spectra originate from different precursor m/z values or non-overlapping retention times — combining unrelated spectra will produce a meaningless chimeric spectrum.
- Goal is to preserve individual scan information for quantification — consensus assembly loses scan-level intensity and retention time detail, unsuitable for targeted quantification workflows.

## Inputs

- MS2 fragmentation spectra (Spectra object at msLevel=2)
- Chromatographic peak detection results (from chromPeaks())
- Multiple MS2 scans from the same precursor m/z and retention time

## Outputs

- Consensus MS2 spectrum (single Spectra object)
- Merged fragment m/z and intensity values
- Annotation scores or mirror plots (from compareSpectra())

## How to apply

Extract all MS2 spectra associated with a detected chromatographic peak using chromPeakSpectra() at msLevel=2. Combine these spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, specifying ppm=20 for fragment mass tolerance, peaks='intersect' to retain fragments present across multiple spectra, and minProp=0.8 to require each fragment to be present in at least 80% of input spectra. The resulting consensus spectrum merges fragment m/z values and averages their intensities, producing a composite that typically exhibits improved signal-to-noise and higher similarity scores to reference spectra. Validate the consensus by computing compareSpectra similarity scores against known reference spectra; expect cosine similarity ≥0.7 for a confident match.

## Related tools

- **xcms** (Detects chromatographic peaks and retrieves associated MS2 spectra via chromPeakSpectra()) — https://github.com/sneumann/xcms
- **Spectra** (Provides the Spectra object container and combineSpectra() function for aggregating MS2 spectra and computing consensus) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMgf** (Loads reference MS2 spectra from MGF-formatted databases (Metlin) for comparison via compareSpectra()) — https://github.com/RforMassSpectrometry/MsBackendMgf
- **MsFeatures** (Optional feature grouping and refinement to ensure peaks are from the same compound before consensus assembly) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
combineSpectra(chromPeakSpectra(dda_data, msLevel = 2L), FUN = combinePeaks, ppm = 20, peaks = 'intersect', minProp = 0.8)
```

## Evaluation signals

- Consensus spectrum contains fragment m/z values present in ≥80% of input spectra (peaks='intersect', minProp=0.8 enforces this threshold).
- compareSpectra similarity score between consensus and reference spectrum is ≥0.7 (cosine similarity metric); score should be substantially higher than similarity of any individual input MS2 to the reference.
- Mirror plot visualization shows alignment of consensus fragment peaks with reference spectrum peaks; visually inspect for absence of chimeric peaks or artifactual m/z values not present in references.
- Consensus spectrum has more detected peaks and higher total intensity compared to individual input MS2 scans, indicating successful aggregation.
- Consensus annotation assignment matches expected compound identity (e.g., Fenamiphos for m/z 304.1131) and does not conflict with known retention time or precursor m/z from the experimental peak.

## Limitations

- Consensus assembly assumes all input MS2 spectra originate from the same precursor ion and compound; misaligned spectra (different m/z, retention time, or compound sources) contaminate the consensus with artifactual fragments.
- minProp threshold of 0.8 may be too stringent for spectra with low reproducibility or high noise, resulting in very sparse consensus spectra; conversely, lowering minProp risks including noise peaks. No universal threshold is appropriate across all data types.
- The combinePeaks approach relies on m/z matching within the specified ppm tolerance (20 ppm in the workflow); fragments differing by >20 ppm are treated as distinct, potentially creating duplicate peaks in the consensus if m/z calibration drift is present.
- Consensus spectra lose intensity information from individual scans and cannot be used for relative quantification; each input spectrum contributes equally regardless of acquisition quality or precursor intensity.
- Some manufacturers (e.g., Sciex) do not export or define precursor intensity, requiring estimation; this affects spectrum intensity normalization and may bias consensus assembly.

## Evidence

- [other] Combine multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8.: "Combine multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8."
- [other] Retrieve all MS2 fragmentation spectra associated with the detected peak(s) using chromPeakSpectra() at msLevel=2.: "Retrieve all MS2 fragmentation spectra associated with the detected peak(s) using chromPeakSpectra() at msLevel=2."
- [other] Compute compareSpectra similarity scores between the consensus spectrum and each reference spectrum using default or cosine similarity metric.: "Compute compareSpectra similarity scores between the consensus spectrum and each reference spectrum using default or cosine similarity metric."
- [intro] Extract MS2 spectra associated with chromatographic peaks for annotation: "Extract MS2 spectra associated with chromatographic peaks for annotation"
- [intro] In a typical LC-MS-based metabolomics experiment compounds eluting from the chromatography are first ionized before being measured by mass spectrometry (MS). During the ionization different ions generated from the same compound being detected as different features.: "compounds eluting from the chromatography are first ionized before being measured by mass spectrometry (MS). During the ionization different ions generated from the same compound being detected as"
- [other] The experimental consensus MS2 spectrum from the m/z 304.1131 chromatographic peak showed high similarity to Fenamiphos reference spectra but not to Flumazenil, with mirror plot visualization and compareSpectra scores confirming Fenamiphos as the match.: "The experimental consensus MS2 spectrum from the m/z 304.1131 chromatographic peak showed high similarity to Fenamiphos reference spectra but not to Flumazenil"
- [intro] In this method the top N most intense ions (m/z values) from a MS1 scan are selected for fragmentation in the next N scans before the cycle starts again. This method allows to generate clean MS2 spectra.: "In this method the top N most intense ions (m/z values) from a MS1 scan are selected for fragmentation in the next N scans"
