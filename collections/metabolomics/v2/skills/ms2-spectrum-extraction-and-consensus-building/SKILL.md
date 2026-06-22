---
name: ms2-spectrum-extraction-and-consensus-building
description: Use when when you have DDA LC-MS/MS data (mzML format) with identified chromatographic peaks at a specific m/z (e.g., 304.1131) and multiple MS2 spectra fragmented from that precursor, and you need to produce a single high-confidence MS2 spectrum for comparison against reference databases (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - MsFeatures
  - Spectra
  - MsBackendMgf
  - MetaboCoreUtils
  - xcms
  techniques:
  - LC-MS
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(Spectra)
- library(MsBackendMgf)
- '%\VignetteDepends{xcms,MsDataHub,BiocStyle,pander,Spectra,MsBackendMgf,MetaboCoreUtils}'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS2 Spectrum Extraction and Consensus Building

## Summary

Extract MS2 spectra associated with chromatographic peaks detected in DDA LC-MS data, then combine multiple MS2 scans into a single consensus spectrum to improve signal-to-noise ratio and enable robust compound identification through spectral matching.

## When to use

When you have DDA LC-MS/MS data (mzML format) with identified chromatographic peaks at a specific m/z (e.g., 304.1131) and multiple MS2 spectra fragmented from that precursor, and you need to produce a single high-confidence MS2 spectrum for comparison against reference databases (e.g., Metlin, GNPS) to identify the compound.

## When NOT to use

- Input is already a single, high-quality MS2 spectrum — consensus building adds no value if only one scan is available.
- MS1-only data (no MS2 fragmentation data) — chromPeakSpectra() requires tandem data.
- Precursor m/z is not clearly separated from interferents in the same retention time window — poor peak detection will yield unreliable consensus spectra.

## Inputs

- DDA LC-MS/MS raw data (mzML format)
- Retention time range (seconds) containing the target chromatographic peak
- Target precursor m/z value
- Reference MS2 spectra in MGF format (e.g., Metlin ID 2724, 72445)

## Outputs

- Consensus MS2 spectrum (single aggregated fragmentation pattern)
- Similarity scores from compareSpectra() (dot-product values for each reference match)
- Mirror-plot visualization comparing consensus spectrum to reference spectra

## How to apply

First, detect chromatographic peaks in MS level 1 data using findChromPeaks() with CentWaveParam (e.g., snthresh=5, noise=100, ppm=10), filtering to the retention time window containing your peak of interest (e.g., 230–610 s). Next, extract all MS2 spectra associated with the detected chromatographic peak using chromPeakSpectra(), which retrieves fragmentations triggered by that precursor. Combine the multiple MS2 spectra into a single consensus spectrum using combineSpectra() with combinePeaks(), which aggregates peak m/z and intensities across scans. Finally, match the consensus spectrum against reference spectra (in MGF format) using compareSpectra() with the normalized dot-product method at 40 ppm tolerance to evaluate similarity scores and identify the compound.

## Related tools

- **xcms** (Peak detection (findChromPeaks), spectral extraction (chromPeakSpectra), data loading and filtering) — https://github.com/sneumann/xcms
- **Spectra** (In-memory representation, manipulation, and comparison of MS2 spectra)
- **MsBackendMgf** (Loading reference spectra from MGF (Mascot Generic Format) files)
- **MetaboCoreUtils** (compareSpectra() implementation with normalized dot-product similarity metric)
- **MsFeatures** (General MS feature grouping and metadata management)

## Examples

```
dda_data <- filterRt(dda_data, rt = c(230, 610)); peaks <- findChromPeaks(dda_data, CentWaveParam(snthresh=5, noise=100, ppm=10)); ms2_spec <- chromPeakSpectra(dda_data, peaks); consensus <- combineSpectra(ms2_spec, combinePeaks); similarity <- compareSpectra(consensus, reference_spectra, ppm=40)
```

## Evaluation signals

- Consensus MS2 spectrum contains expected fragment ions for the target compound (e.g., characteristic loss patterns for pesticides).
- Similarity score (dot-product) to the correct reference compound is significantly higher (e.g., >0.7) than to false positives, indicating unambiguous identification.
- Mirror plot visually shows strong peak alignment between consensus and reference spectrum, with major fragment m/z values matching within 40 ppm tolerance.
- Number of MS2 scans combined is > 1 and reflects the signal intensity across multiple chromatographic scans at the target m/z.
- Consensus spectrum m/z axis and intensity values are consistent with the source raw data (no NaN or negative intensities).

## Limitations

- Consensus building assumes all extracted MS2 scans derive from the same compound; co-isolation of multiple precursors in the same isolation window will produce a mixed spectrum.
- Low signal-to-noise in individual MS2 scans may not be fully recovered by consensus averaging; weak fragments risk being lost if present in only a minority of scans.
- Peak detection parameters (snthresh, noise, ppm) must be tuned for the specific instrument and sample matrix; suboptimal thresholds may miss genuine peaks or include noise artifacts.
- Spectrum matching relies on the availability and quality of reference MS2 spectra in MGF; compounds absent from Metlin or GNPS cannot be identified by this approach.

## Evidence

- [intro] Extract MS2 spectra associated with chromatographic peaks using chromPeakSpectra().: "Spectra for identified chromatographic peaks can be extracted with the `chromPeakSpectra()` method."
- [intro] Consensus building combines multiple MS2 scans via combineSpectra() and combinePeaks().: "We next reduce this to a single MS2 spectrum using the `combineSpectra()` method employing the `combinePeaks()` function"
- [intro] Spectral matching uses compareSpectra() with normalized dot-product and ppm tolerance.: "we can also calculate similarities between them with the `compareSpectra()` method"
- [intro] CentWaveParam used for peak detection with specific thresholds.: "findChromPeaks() method. Below we define the settings for a *centWave*-based peak detection"
- [other] The article demonstrates identification of m/z 304.1131 peak as Fenamiphos via MS2 similarity.: "The consensus MS2 spectrum from the chromatographic peak at m/z 304.1131 has high similarity to Fenamiphos but not to Flumazenil when compared using the normalized dot-product method with 40 ppm"
