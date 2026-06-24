---
name: ms2-spectrum-collection-from-data-dependent-acquisition
description: Use when you have DDA LC-MS/MS raw data (mzML format) with detected chromatographic
  peaks at a target m/z value and retention time window, and you need to build a high-confidence
  MS2 consensus spectrum for that peak to match against reference spectra (e.g., Metlin,
  GNPS).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MsBackendMgf
  - MsFeatures
  - xcms
  - Spectra
  techniques:
  - LC-MS
  - CE-MS
  license_tier: open
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
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

# MS2 Spectrum Collection from Data-Dependent Acquisition

## Summary

Extract and combine multiple MS2 fragmentation spectra associated with a chromatographic peak from DDA LC-MS/MS data to produce a consensus spectrum for compound annotation. This skill recovers clean precursor-fragment relationships that DDA naturally provides, enabling confident spectral matching against reference libraries.

## When to use

You have DDA LC-MS/MS raw data (mzML format) with detected chromatographic peaks at a target m/z value and retention time window, and you need to build a high-confidence MS2 consensus spectrum for that peak to match against reference spectra (e.g., Metlin, GNPS). Use this when a single MS2 scan is insufficient or noisy, and multiple fragmentation spectra of the same precursor have been acquired across the chromatographic apex.

## When NOT to use

- Input is DIA or SWATH data — those modalities fragment all ions within windows simultaneously, producing chimeric spectra with no clear precursor-fragment relationship; use DIA-specific peak detection methods instead.
- Only a single MS2 scan is available for the peak — consensus building requires multiple fragmentation spectra to be effective; a single spectrum should be used directly.
- You have already computed a feature table with grouped compound signals — this skill targets individual chromatographic peaks, not aggregated feature abundance matrices.

## Inputs

- DDA LC-MS/MS raw data file (mzML format)
- Target m/z value and retention time range
- Tolerance parameters (ppm window, typically 20 ppm)

## Outputs

- Consensus MS2 spectrum object (Spectra class)
- Precursor m/z and retention time metadata
- Combined peak list with fragment m/z and intensity values

## How to apply

First, load the DDA raw data and filter to the retention time range containing your peak of interest using filterRt(). Extract all chromatographic peaks at your target m/z (±20 ppm tolerance) using chromPeaks() with mz and ppm parameters. Retrieve all MS2 fragmentation spectra (msLevel=2) associated with the detected peak(s) using chromPeakSpectra(). Combine the multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', and minProp=0.8 (requiring 80% of peaks to be present across spectra to ensure robust fragment signals). The 'intersect' mode and high minProp threshold ensure that only reproducible fragments across multiple scans are retained, improving signal-to-noise and specificity for downstream spectral matching.

## Related tools

- **xcms** (Core package providing chromPeaks(), chromPeakSpectra(), and filterRt() functions to detect and extract MS2 spectra from DDA data) — https://github.com/sneumann/xcms
- **Spectra** (Data container and manipulation backend; combineSpectra() is implemented in Spectra to merge multiple MS2 spectra into consensus) — https://github.com/RforMassSpectrometry/Spectra
- **MsBackendMgf** (Backend for reading reference MS2 spectra from Metlin/GNPS MGF files for downstream similarity scoring)
- **MsFeatures** (Optional downstream tool for feature grouping and compounding if extending analysis to multiple features) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
dda_data_filt <- filterRt(dda_data, rt = c(230, 610)); peaks <- chromPeaks(dda_data_filt, mz = 304.1131, ppm = 20); spectra_ms2 <- chromPeakSpectra(dda_data_filt, msLevel = 2L); consensus <- combineSpectra(spectra_ms2, FUN = combinePeaks, ppm = 20, peaks = 'intersect', minProp = 0.8)
```

## Evaluation signals

- The consensus spectrum contains only fragment m/z values present in ≥80% of input MS2 spectra (minProp=0.8 threshold enforced); spot-check a few fragments to confirm they appear in the majority of scans.
- Precursor m/z and retention time metadata are retained and match the target peak location (e.g., m/z 304.1131 ±20 ppm, rt ~230–610 s range).
- Consensus spectrum intensity values are merged (summed or averaged per combinePeaks logic) and show improved signal relative to any single input MS2 scan.
- When plotted as a mirror plot against reference spectra using plotSpectraMirror(), the consensus spectrum shows visual alignment with the correct reference (e.g., Fenamiphos vs. Flumazenil); cosine similarity scores should be ≥0.7 for a confident match.
- The combined spectrum has fewer noise peaks and higher fragment intensity for authentic fragments compared to raw single MS2 scans, indicating successful denoising.

## Limitations

- DDA acquisition inherently covers only the top N most intense ions per cycle, leading to poor metabolite coverage and potential missed minor peaks.
- If chromatographic peaks are very narrow or few MS2 scans overlap the peak apex, consensus building may yield insufficient redundancy; minimum 2–3 MS2 scans per peak are recommended.
- The ppm tolerance (20 ppm) and minProp threshold (0.8) are empirically set and may need adjustment for very low-abundance or high-noise data; tighter thresholds reduce consensus quality but stricter thresholds may eliminate valid peaks.
- Reference library completeness and quality (e.g., Metlin, GNPS) affect annotation confidence; absent or poorly annotated compounds will not be reliably identified even with high-quality consensus spectra.

## Evidence

- [intro] DDA method description and trade-offs: "In this method the top N most intense ions (m/z values) from a MS1 scan are selected for fragmentation in the next N scans before the cycle starts again. This method allows to generate clean MS2"
- [intro] chromPeakSpectra function for extracting MS2 data: "Extract MS2 spectra associated with chromatographic peaks for annotation"
- [intro] combineSpectra parameters and rationale: "Combine multiple MS2 spectra into consensus spectrum using combinePeaks function"
- [intro] Workflow step: consensus spectrum construction with specific parameters: "Combine multiple MS2 spectra into a single consensus spectrum using combineSpectra() with FUN=combinePeaks, ppm=20, peaks='intersect', minProp=0.8"
- [intro] Compounding rationale for feature grouping and annotation: "*Compounding* aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity (and to aid in subsequent annotation steps)."
- [intro] Mirror plot and similarity scoring for spectrum matching: "Match experimental MS2 spectrum against reference database spectra using similarity metrics"
